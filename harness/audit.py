"""Offline semantic audit for portable expression attempts; never starts engines."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat

import core
import validator


def same(actual, expected, label):
    # JSON representation distinguishes booleans from integers.
    if json.dumps(actual, sort_keys=True, ensure_ascii=True) != json.dumps(expected, sort_keys=True, ensure_ascii=True):
        raise ValueError("semantic mismatch: " + label)


def check_tree(root):
    """Reject links, junctions and special files before reading an attempt."""
    def walk(path):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError("link or reparse point in attempt")
        if stat.S_ISDIR(info.st_mode):
            with os.scandir(path) as entries:
                for entry in entries:
                    walk(Path(entry.path))
        elif not stat.S_ISREG(info.st_mode):
            raise ValueError("non-regular attempt member")
    walk(root)


def check_input_directories(root):
    erb, csv = root / "ERB", root / "csv"
    if not erb.is_dir() or not csv.is_dir():
        raise ValueError("missing fixture input directory")
    if {p.name for p in erb.iterdir()} != {"SEARCHBOUND01.ERB"} or any(csv.iterdir()):
        raise ValueError("unexpected fixture input directory contents")


def audit_attempt(h, attempt, plan, exe, pyz, config, selected, repeats, seal_sha256):
    """Recompute a complete attempt using a separately trusted seal hash.

    This checks consistency, not whether an untrusted producer ran an engine.
    Historical v1, incomplete and failed attempts are intentionally rejected.
    """
    if not isinstance(seal_sha256, str) or not re.fullmatch(r'[0-9a-f]{64}', seal_sha256):
        raise ValueError("a separately recorded lowercase SHA-256 of SEAL.json is required")
    root = Path(attempt).absolute()
    check_tree(root)
    if (root / "VALIDATION.json").exists():
        raise ValueError("unsealed VALIDATION.json is not allowed for reuse")
    same(validator.sha(root / "SEAL.json"), seal_sha256, "trusted seal hash")
    structural = validator.validate(root, expected_external=[])
    if not structural["valid"]:
        raise ValueError("invalid evidence inventory: " + str(structural["errors"]))
    request = h.request_for(plan, exe, pyz, config, selected, repeats)
    result = validator.read(root / "RESULT.json")
    expected_keys = {"schema", "status", "cases", "request", "native_sha256", "pyz_sha256",
                     "config_sha256", "plan_sha256", "python", "platform", "repeats", "stages",
                     "python_executable_sha256", "tool_sha256", "lock_released"}
    if not isinstance(result, dict) or set(result) != expected_keys:
        raise ValueError("unsupported or incomplete result envelope")
    same(result["schema"], "portable-expression-run.v2", "schema")
    same(result["request"], request, "whole-attempt request and input pins")
    for key in ("native_sha256", "pyz_sha256", "config_sha256", "plan_sha256", "python", "platform",
                "repeats", "python_executable_sha256", "tool_sha256"):
        same(result[key], request[key], key)
    same(result["lock_released"], True, "lock released")
    if validator.sha(root / "plan.json") != request["plan_sha256"]:
        raise ValueError("plan snapshot mismatch")
    cases = core.load_plan(plan, selected)
    groups = [("single", [cases[0]])]
    if len(cases) > 1:
        groups.append(("batch", cases))
    stages = result["stages"]
    if not isinstance(stages, list) or len(stages) != len(groups):
        raise ValueError("stage count")
    derived = []
    forced = False
    for stage, (name, group) in zip(stages, groups):
        keys = {"name", "native", "comparisons", "input_sha256", "py_inputs_before", "py_inputs_after",
                "pyz_sha256_before", "pyz_sha256_after", "py_returncode", "native_processes_before",
                "native_processes_after", "native_inputs_before", "native_inputs_after",
                "native_exe_sha256_before", "native_exe_sha256_after"}
        if not isinstance(stage, dict) or set(stage) != keys:
            raise ValueError("incomplete stage receipt")
        same(stage["name"], name, "stage order")
        data = core.fixture(group)
        inputs = {"ERB/SEARCHBOUND01.ERB": hashlib.sha256(data).hexdigest(),
                  "emuera.config": request["config_sha256"]}
        same(stage["input_sha256"], inputs, "stage input map")
        for key in ("py_inputs_before", "py_inputs_after"):
            same(stage[key], inputs, key)
        for key in ("pyz_sha256_before", "pyz_sha256_after"):
            same(stage[key], request["pyz_sha256"], key)
        same(stage["py_returncode"], 0, "Py exit code")
        py = root / name / "py"
        check_input_directories(py)
        if (py / "ERB/SEARCHBOUND01.ERB").read_bytes() != data:
            raise ValueError("Py fixture differs from plan")
        same(h.input_inventory(py), inputs, "actual Py inputs")
        for f in (py / "stdout.bin", py / "stderr.bin"):
            if not f.is_file():
                raise ValueError("missing Py output receipt")
        py_log = h.bounded_read(py / ".pyemuera/logs/emuera.log")
        for key in ("native", "comparisons", "native_processes_before", "native_processes_after",
                    "native_inputs_before", "native_inputs_after", "native_exe_sha256_before", "native_exe_sha256_after"):
            if not isinstance(stage[key], list) or len(stage[key]) != repeats:
                raise ValueError("incomplete Native repeats: " + key)
        comparisons = []
        for index in range(repeats):
            native = root / name / ("native-%02d" % (index + 1))
            check_input_directories(native)
            receipt = stage["native"][index]
            if not isinstance(receipt, dict) or set(receipt) != {"desktop_created", "process_created", "input_sent",
                                                                  "pid", "outcome", "exit_code", "desktop_closed"}:
                raise ValueError("incomplete Native receipt")
            for key, value in (("desktop_created", True), ("process_created", True), ("input_sent", False),
                               ("desktop_closed", True)):
                same(receipt[key], value, "Native " + key)
            if type(receipt["pid"]) is not int or receipt["pid"] <= 0:
                raise ValueError("invalid owned Native PID")
            if receipt["outcome"] == "natural_rc0":
                same(receipt["exit_code"], 0, "Native exit code")
            elif receipt["outcome"] == "forced_termination":
                same(receipt["exit_code"], None, "Native forced exit")
                forced = True
            else:
                raise ValueError("Native outcome incomplete")
            for key in ("native_processes_before", "native_processes_after"):
                same(stage[key][index], [], key)
            for key in ("native_inputs_before", "native_inputs_after"):
                same(stage[key][index], inputs, key)
            for key in ("native_exe_sha256_before", "native_exe_sha256_after"):
                same(stage[key][index], request["native_sha256"], key)
            if (native / "ERB/SEARCHBOUND01.ERB").read_bytes() != data:
                raise ValueError("Native fixture differs from plan")
            same(h.input_inventory(native), inputs, "actual Native inputs")
            same(validator.sha(native / "Emuera1824+v24.exe"), request["native_sha256"], "Native copy")
            compared = core.compare_logs(group, h.bounded_read(native / "emuera.log"), py_log)
            if any(row["status"] not in ("matched_scoped", "different") for row in compared["cases"]):
                raise ValueError("incomplete raw observations")
            same(stage["comparisons"][index], compared, "rederived verdict and observations")
            comparisons.append(compared)
        first = comparisons[0]["cases"]
        if any(c["cases"] != first for c in comparisons[1:]):
            raise ValueError("Native repeat observations differ")
        derived.append(first)
    if len(derived) > 1:
        same(derived[0][0], derived[1][0], "single/batch parity")
    same(result["cases"], derived[-1], "final verdicts")
    same(result["status"], "completed_with_forced_native_cleanup" if forced else "completed", "outcome")
    same(h.request_for(plan, exe, pyz, config, selected, repeats), request, "inputs after audit")
    same(validator.sha(root / "SEAL.json"), seal_sha256, "seal after audit")
    if not validator.validate(root, expected_external=[])["valid"]:
        raise ValueError("attempt changed during audit")
    return {"valid": True, "status": result["status"], "cases": derived[-1],
            "scope": "whole-attempt consistency; not authenticity or new engine execution"}
