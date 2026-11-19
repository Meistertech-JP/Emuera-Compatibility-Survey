"""Portable finite pure-expression comparison and evidence collection."""
import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import json
import locale
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

# Also resolve sibling modules when Python is started with -I.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import core
import native
import validator
import audit

HERE = Path(__file__).resolve().parent
NATIVE_SHA = "14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964"
PYZ_SHA = "8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35"
CONFIG_SHA = "f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc"
MAX_LOG = 8 * 1024 * 1024
TOOL_NAMES = ("harness.py", "core.py", "native.py", "validator.py", "audit.py")


def check_lock(folder, nonce):
    if os.path.lexists(folder / "MEASURE_LOCK.json"):
        raise RuntimeError("measurement lock exists")
    if validator.read(folder / "NATIVE_LOCK.json").get("nonce") != nonce:
        raise RuntimeError("native lock ownership changed")


@contextlib.contextmanager
def shared_lock(folder):
    folder = Path(folder).resolve(strict=True)
    if not folder.is_dir():
        raise ValueError("lock directory must exist")
    lock = folder / "NATIVE_LOCK.json"
    if os.path.lexists(lock) or os.path.lexists(folder / "MEASURE_LOCK.json"):
        raise RuntimeError("shared lock already exists")
    nonce = uuid.uuid4().hex
    fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"nonce": nonce, "pid": os.getpid(), "owner": "portable-harness",
                       "utc": datetime.now(timezone.utc).isoformat()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        check_lock(folder, nonce)
        yield nonce
    finally:
        try:
            if validator.read(lock).get("nonce") == nonce:
                lock.unlink()
            else:
                raise RuntimeError("lock ownership changed; lock retained")
        except (OSError, ValueError) as exc:
            raise RuntimeError("could not verify or release owned lock") from exc


def native_processes():
    code = ("[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); "
            "$ErrorActionPreference='Stop'; "
            "@(Get-CimInstance Win32_Process -Filter \"Name='Emuera1824+v24.exe'\" | "
            "Select-Object ProcessId,ExecutablePath) | ConvertTo-Json -Compress")
    proc = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", code],
                          capture_output=True, stdin=subprocess.DEVNULL, check=True, timeout=12)
    result = json.loads(proc.stdout.decode("utf-8").strip() or "[]")
    return result if isinstance(result, list) else [result]


def wait_for_native_absence(timeout=5.0):
    """Allow process enumeration to settle; never terminate an enumerated PID."""
    deadline = time.monotonic() + timeout
    while True:
        processes = native_processes()
        if not processes or time.monotonic() >= deadline:
            return processes
        time.sleep(0.25)


def bounded_read(path):
    if path.stat().st_size > MAX_LOG:
        raise ValueError("log exceeds 8 MiB")
    return path.read_bytes()


def validate_inputs(exe, pyz, config):
    if Path(exe).name.lower() != "emuera1824+v24.exe":
        raise ValueError("Native executable must be named Emuera1824+v24.exe")
    for path, expected in ((exe, NATIVE_SHA), (pyz, PYZ_SHA), (config, CONFIG_SHA)):
        if not Path(path).is_file() or validator.sha(path) != expected:
            raise ValueError("missing input or SHA-256 mismatch: " + Path(path).name)


def prepare_side(root, fixture, config, exe=None):
    root.mkdir(parents=True, exist_ok=False)
    (root / "ERB").mkdir()
    (root / "csv").mkdir()
    (root / "ERB" / "SEARCHBOUND01.ERB").write_bytes(fixture)
    shutil.copyfile(config, root / "emuera.config")
    if exe:
        shutil.copyfile(exe, root / "Emuera1824+v24.exe")
    return input_inventory(root)


def input_inventory(root):
    paths = [p for folder in ("ERB", "csv") for p in (root / folder).rglob("*") if p.is_file()]
    paths.append(root / "emuera.config")
    return {p.relative_to(root).as_posix(): validator.sha(p) for p in sorted(paths)}


def compare_files(plan, native_log, py_log, selected=()):
    cases = core.load_plan(plan, selected)
    return core.compare_logs(cases, bounded_read(Path(native_log)), bounded_read(Path(py_log)))


def request_for(plan, exe, pyz, config, selected, repeats):
    if repeats not in (1, 2, 3) or type(repeats) is not int:
        raise ValueError("native repeats must be 1, 2 or 3")
    validate_inputs(exe, pyz, config)
    before = validator.sha(plan)
    cases = core.load_plan(plan, selected)
    if validator.sha(plan) != before:
        raise ValueError("plan changed during request")
    return {"schema": "portable-expression-request.v2", "plan_sha256": before,
            "selected": [c["case_id"] for c in cases], "repeats": repeats,
            "native_sha256": validator.sha(exe), "pyz_sha256": validator.sha(pyz),
            "config_sha256": validator.sha(config), "python": sys.version,
            "platform": sys.platform, "python_executable_sha256": validator.sha(sys.executable),
            "os_name": os.name, "os_version": list(sys.getwindowsversion()) if hasattr(sys, "getwindowsversion") else None,
            "preferred_encoding": locale.getpreferredencoding(False),
            "environment_sha256": core.digest(dict(os.environ)),
            "tool_sha256": {name: validator.sha(HERE / name) for name in TOOL_NAMES}}


def execute(plan, exe, pyz, config, lock_dir, out, selected=(), repeats=1):
    if sys.platform != "win32":
        raise RuntimeError("Native execution requires Windows")
    if repeats not in (1, 2, 3):
        raise ValueError("native repeats must be 1, 2 or 3")
    exe, pyz, config, plan = (Path(p).resolve(strict=True) for p in (exe, pyz, config, plan))
    lock_dir = Path(lock_dir).resolve(strict=True)
    out = Path(out).absolute()
    request = request_for(plan, exe, pyz, config, selected, repeats)
    plan_hash = request["plan_sha256"]
    cases = core.load_plan(plan, selected)
    run_key = uuid.uuid4().hex
    attempt = out / ("attempt-" + run_key)
    result = {"schema": "portable-expression-run.v2", "status": "failure", "cases": [], "request": request,
              "native_sha256": NATIVE_SHA, "pyz_sha256": PYZ_SHA, "config_sha256": CONFIG_SHA,
              "plan_sha256": plan_hash, "python": sys.version, "platform": sys.platform,
              "repeats": repeats, "stages": [], "python_executable_sha256": validator.sha(sys.executable),
              "tool_sha256": request["tool_sha256"]}
    with shared_lock(lock_dir) as nonce:
        if native_processes():
            raise RuntimeError("Native process already running; refused")
        attempt.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(plan, attempt / "plan.json")
        try:
            if validator.sha(attempt / "plan.json") != plan_hash:
                raise RuntimeError("plan changed while being copied")
            # Keep representative single and full-batch observations separate.
            groups = [("single", [cases[0]])]
            if len(cases) > 1:
                groups.append(("batch", cases))
            for stage_name, stage_cases in groups:
                check_lock(lock_dir, nonce)
                data = core.fixture(stage_cases)
                stage = {"name": stage_name, "native": [], "comparisons": []}
                result["stages"].append(stage)
                public_dir = attempt / stage_name / "py"
                expected_inputs = prepare_side(public_dir, data, config)
                stage["input_sha256"] = expected_inputs
                stage["py_inputs_before"] = input_inventory(public_dir)
                before_pyz = validator.sha(pyz)
                stage["pyz_sha256_before"] = before_pyz
                py = subprocess.run([sys.executable, "-I", str(pyz), "--debug", "."], cwd=public_dir,
                                    stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
                (public_dir / "stdout.bin").write_bytes(py.stdout)
                (public_dir / "stderr.bin").write_bytes(py.stderr)
                stage["py_returncode"] = py.returncode
                stage["pyz_sha256_after"] = validator.sha(pyz)
                stage["py_inputs_after"] = input_inventory(public_dir)
                if (py.returncode != 0 or stage["pyz_sha256_after"] != before_pyz or before_pyz != PYZ_SHA
                        or stage["py_inputs_after"] != expected_inputs):
                    raise RuntimeError("PyEmuera execution failed or binary changed")
                pylog = bounded_read(public_dir / ".pyemuera" / "logs" / "emuera.log")
                for index in range(repeats):
                    check_lock(lock_dir, nonce)
                    if native_processes():
                        raise RuntimeError("Native process already running; refused")
                    stage.setdefault("native_processes_before", []).append([])
                    native_dir = attempt / stage_name / ("native-%02d" % (index + 1))
                    if prepare_side(native_dir, data, config, exe) != expected_inputs:
                        raise RuntimeError("side input mismatch")
                    stage.setdefault("native_inputs_before", []).append(input_inventory(native_dir))
                    copied_exe = native_dir / "Emuera1824+v24.exe"
                    if validator.sha(copied_exe) != NATIVE_SHA:
                        raise RuntimeError("copied Native hash mismatch")
                    stage.setdefault("native_exe_sha256_before", []).append(validator.sha(copied_exe))
                    native_error = None
                    try:
                        receipt = native.run(copied_exe, native_dir)
                        stage["native"].append(receipt)
                    except (OSError, ValueError, RuntimeError) as exc:
                        native_error = exc
                        stage.setdefault("native_errors", []).append(str(exc))
                    # Never terminate processes discovered by name or path.
                    remaining = wait_for_native_absence()
                    stage.setdefault("native_processes_after", []).append(remaining)
                    if remaining:
                        raise RuntimeError("Native process remains after owned-process cleanup")
                    if native_error is not None:
                        raise RuntimeError("Native execution failed: " + str(native_error)) from native_error
                    if receipt["outcome"] not in ("natural_rc0", "forced_termination"):
                        raise RuntimeError("Native process failed")
                    for side in (native_dir, public_dir):
                        current = input_inventory(side)
                        if current != expected_inputs:
                            raise RuntimeError("fixture or config changed during execution")
                    stage.setdefault("native_inputs_after", []).append(input_inventory(native_dir))
                    stage["py_inputs_after"] = input_inventory(public_dir)
                    if validator.sha(copied_exe) != NATIVE_SHA:
                        raise RuntimeError("Native binary changed during execution")
                    stage.setdefault("native_exe_sha256_after", []).append(validator.sha(copied_exe))
                    stage["comparisons"].append(core.compare_logs(stage_cases,
                                                  bounded_read(native_dir / "emuera.log"), pylog))
                    check_lock(lock_dir, nonce)
                first = stage["comparisons"][0]["cases"]
                if any(c["cases"] != first for c in stage["comparisons"][1:]):
                    raise RuntimeError("Native repeat observations differ")
                if any(c["status"] in ("missing", "failure") for c in first):
                    raise RuntimeError("comparison observations incomplete")
            if len(groups) > 1:
                single = result["stages"][0]["comparisons"][0]["cases"][0]
                batch = result["stages"][1]["comparisons"][0]["cases"][0]
                if single != batch:
                    raise RuntimeError("single and batch observations differ")
            result["cases"] = result["stages"][-1]["comparisons"][0]["cases"]
            validate_inputs(exe, pyz, config)
            if validator.sha(plan) != plan_hash:
                raise RuntimeError("plan changed during execution")
            if (any(validator.sha(HERE / name) != value for name, value in result["tool_sha256"].items())
                    or validator.sha(sys.executable) != result["python_executable_sha256"]):
                raise RuntimeError("harness or Python executable changed during execution")
            result["status"] = ("completed_with_forced_native_cleanup" if any(
                n["outcome"] == "forced_termination" for s in result["stages"] for n in s["native"])
                else "completed")
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            result["error"] = str(exc)
    # Seal only after the lock manager has verified and released its own lock.
    # If release fails, raw files remain unsealed and the error propagates.
    result["lock_released"] = True
    validator.write(attempt / "RESULT.json", result)
    validator.seal(attempt)
    if result["status"] != "failure":
        try:
            audit.audit_attempt(sys.modules[__name__], attempt, plan, exe, pyz, config, selected,
                                repeats, validator.sha(attempt / "SEAL.json"))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise RuntimeError("post-seal semantic audit failed; attempt retained: " + str(attempt) + "; " + str(exc)) from exc
    return attempt, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    plan = subs.add_parser("plan", help="validate a plan and report generated fixture hash")
    plan.add_argument("plan", type=Path)
    plan.add_argument("--case", action="append", default=[])
    comp = subs.add_parser("compare", help="compare saved raw logs without starting engines")
    comp.add_argument("plan", type=Path)
    comp.add_argument("native_log", type=Path)
    comp.add_argument("py_log", type=Path)
    comp.add_argument("--case", action="append", default=[])
    run = subs.add_parser("run", help="run both pinned engines on Windows")
    run.add_argument("plan", type=Path)
    run.add_argument("--native", required=True, type=Path)
    run.add_argument("--pyz", required=True, type=Path)
    run.add_argument("--config", type=Path, default=HERE / "fixtures" / "emuera.config")
    run.add_argument("--lock-dir", required=True, type=Path)
    run.add_argument("--out", required=True, type=Path)
    run.add_argument("--repeat-native", type=int, choices=(1, 2, 3), default=1)
    run.add_argument("--case", action="append", default=[])
    check = subs.add_parser("validate", help="check a sealed attempt's file inventory")
    check.add_argument("attempt", type=Path)
    for command in ("audit", "resume"):
        verify = subs.add_parser(command, help="offline semantic " + command + " of a whole attempt")
        verify.add_argument("attempt", type=Path)
        verify.add_argument("plan", type=Path)
        verify.add_argument("--native", required=True, type=Path)
        verify.add_argument("--pyz", required=True, type=Path)
        verify.add_argument("--config", type=Path, default=HERE / "fixtures" / "emuera.config")
        verify.add_argument("--repeat-native", type=int, choices=(1, 2, 3), default=1)
        verify.add_argument("--case", action="append", default=[])
        verify.add_argument("--seal-sha256", required=True, help="separately trusted SHA-256 of SEAL.json")
    args = parser.parse_args()
    try:
        if args.command == "plan":
            cases = core.load_plan(args.plan, args.case)
            result = {"cases": [c["case_id"] for c in cases],
                      "fixture_sha256": hashlib.sha256(core.fixture(cases)).hexdigest()}
        elif args.command == "compare":
            result = compare_files(args.plan, args.native_log, args.py_log, args.case)
        elif args.command == "validate":
            result = validator.validate(args.attempt, expected_external=[])
        elif args.command in ("audit", "resume"):
            result = audit.audit_attempt(sys.modules[__name__], args.attempt, args.plan, args.native,
                                         args.pyz, args.config, args.case, args.repeat_native, args.seal_sha256)
            result["reused"] = args.command == "resume"
        else:
            attempt, result = execute(args.plan, args.native, args.pyz, args.config, args.lock_dir,
                                      args.out, args.case, args.repeat_native)
            print("attempt:", attempt, file=sys.stderr)
            print("SEAL.json SHA-256:", validator.sha(attempt / "SEAL.json"), file=sys.stderr)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        if result.get("valid") is False or result.get("status") == "failure":
            return 1
        if args.command == "compare" and any(c["status"] in ("missing", "failure") for c in result["cases"]):
            return 1
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
