"""Run fixed isolated input, error and RESULT-write witnesses."""
import argparse
import ctypes as c
from ctypes import wintypes as w
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

import core
import harness
import native
import validator

HERE = Path(__file__).resolve().parent
CASES = {
    "P35": ("fixtures/manual/P35/ERB/P35.ERB", "42"),
    "P36": ("fixtures/manual/P36/ERB/P36.ERB", "ABC"),
    "P35_OBS": ("fixtures/local/P35_OBS/ERB/P35_OBS.ERB", "42"),
    "P36_OBS": ("fixtures/local/P36_OBS/ERB/P36_OBS.ERB", "ABC"),
    "P38": ("fixtures/manual/P38/ERB/P38.ERB", None),
    "ARGUMENT": ("fixtures/local/ARGUMENT/ERB/ARGUMENT.ERB", None),
    "RESULT_WRITE": ("fixtures/local/RESULT_WRITE/ERB/RESULT_WRITE.ERB", None),
}
FIXTURE_SHA = {
    'P35': '1706ef111d20f7c813a3dd8ab24142cb2607578c41f78986b9de69290d012a19',
    'P36': '2387f9b30142c4b338c770e5f4cd782505f0b2e757a685599ad8adf79da74d9f',
    'P38': '8b2bf27fed8c6131fa8a2a22a57522cf4ce846b5d16ac78f4951f72d81581471',
    'ARGUMENT': '7c5a43f6c64d4f89168987eb3a26872abd5dc28a351c6c3fe3021e2249af37a6',
    'RESULT_WRITE': '5b7dd97209c2594152be804bde404db831759eb37473dbcf056711a6cda3461a',
    'P35_OBS': '9d2e5881804377198069621846ec63ddd629052afb2156e0fdb9733d47cd1368',
    'P36_OBS': '5113f3599e5a24b45842e8c93171cd61309c2e12985092e18be75c49c1dea2ef',
}


def observe_window(desk, desktop_name, pid, process_handle, output, input_text):
    user = c.WinDLL("user32", use_last_error=True)
    kernel = c.WinDLL("kernel32", use_last_error=True)
    callback = c.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
    user.EnumDesktopWindows.argtypes = [w.HANDLE, callback, w.LPARAM]
    user.EnumChildWindows.argtypes = [w.HWND, callback, w.LPARAM]
    user.GetWindowThreadProcessId.argtypes = [w.HWND, c.POINTER(w.DWORD)]
    user.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, c.c_int]
    user.SendMessageTimeoutW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM, w.UINT, w.UINT, c.POINTER(c.c_size_t)]
    user.SendMessageTimeoutW.restype = w.LPARAM
    user.PostMessageW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
    user.PostMessageW.restype = w.BOOL
    kernel.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
    kernel.WaitForSingleObject.restype = w.DWORD
    # The desktop and process handle were created by native.run, not discovered globally.
    time.sleep(6)
    if kernel.WaitForSingleObject(process_handle, 0) != 0x102:
        return {"status": "not_observed", "reason": "process_exited_before_capture"}
    parents = []
    @callback
    def visit(hwnd, _):
        found = w.DWORD()
        user.GetWindowThreadProcessId(hwnd, c.byref(found))
        if found.value == pid:
            parents.append(int(hwnd))
        return True
    if not user.EnumDesktopWindows(desk, visit, 0):
        raise OSError(c.get_last_error(), "EnumDesktopWindows failed")
    editors = []
    for parent in parents:
        @callback
        def child(hwnd, _):
            found = w.DWORD()
            user.GetWindowThreadProcessId(hwnd, c.byref(found))
            cls = c.create_unicode_buffer(256)
            user.GetClassNameW(hwnd, cls, len(cls))
            if found.value == pid and "RICHEDIT" in cls.value.upper():
                editors.append((int(hwnd), parent))
            return True
        user.EnumChildWindows(parent, child, 0)
    if len(editors) != 1:
        return {"status": "not_observed", "reason": "expected_one_owned_editor", "count": len(editors)}
    editor, parent = editors[0]
    observation = {"status": "captured", "owned_pid": pid, "input_sent": False}

    def capture(label):
        path = output / ("crop-" + label + ".bmp")
        run = subprocess.run([sys.executable, "-I", str(HERE / "capture_crop.py"), desktop_name,
                              str(parent), str(pid), str(path)], capture_output=True, timeout=15)
        observation[label + "_capture_returncode"] = run.returncode
        if run.returncode != 0 or not path.is_file():
            observation[label + "_capture_error"] = run.stderr.decode("utf-8", "replace")[-1000:]
            observation["status"] = "not_observed"
        else:
            observation[label + "_crop_sha256"] = validator.sha(path)
    capture("before")
    if input_text is not None:
        owner = w.DWORD()
        user.GetWindowThreadProcessId(editor, c.byref(owner))
        if owner.value != pid or kernel.WaitForSingleObject(process_handle, 0) != 0x102:
            raise RuntimeError("owned editor or process changed before input")
        value = c.create_unicode_buffer(input_text)
        result = c.c_size_t()
        sent = bool(user.SendMessageTimeoutW(editor, 0x000C, 0, c.cast(value, c.c_void_p).value,
                                              2, 3000, c.byref(result)))
        if not sent or not result.value:
            raise RuntimeError("setting owned editor text failed")
        down = bool(user.PostMessageW(editor, 0x0100, 13, 0x001C0001))
        up = bool(user.PostMessageW(editor, 0x0101, 13, 0xC01C0001))
        if not (down and up):
            raise RuntimeError("posting Enter to owned editor failed")
        observation["input_sent"] = True
        time.sleep(3)
        capture("after")
    return observation


def run_case(case_id, exe, pyz, config, lock_dir, out):
    if sys.platform != "win32":
        raise RuntimeError("Windows required")
    if case_id not in CASES:
        raise ValueError("unknown fixed case")
    exe, pyz, config = (Path(p).resolve(strict=True) for p in (exe, pyz, config))
    lock_dir = Path(lock_dir).resolve(strict=True)
    fixture_rel, text = CASES[case_id]
    fixture = HERE / fixture_rel
    harness.validate_inputs(exe, pyz, config)
    fixture_sha = validator.sha(fixture)
    if fixture_sha != FIXTURE_SHA[case_id]:
        raise ValueError('fixture SHA-256 mismatch')
    tools = {p.name: validator.sha(p) for p in (HERE/'local_cases.py', HERE/'capture_crop.py',
             HERE/'native.py', HERE/'harness.py', HERE/'core.py', HERE/'validator.py')}
    target = Path(out).absolute() / (case_id + "-" + uuid.uuid4().hex)
    report = {"schema": "portable-local-case.v1", "case": case_id, "status": "failure",
              "fixture_sha256": fixture_sha, "config_sha256": harness.CONFIG_SHA,
              "native_sha256": harness.NATIVE_SHA, "pyz_sha256": harness.PYZ_SHA,
              "tool_sha256": tools, "input": text, "scope": "bounded case; visual review separate"}
    with harness.shared_lock(lock_dir) as nonce:
        if harness.native_processes():
            raise RuntimeError("Native already running")
        target.mkdir(parents=True, exist_ok=False)
        try:
            runs = {}
            for side in ("native", "py"):
                folder = target / side
                folder.mkdir()
                (folder / 'ERB').mkdir()
                (folder / 'csv').mkdir()
                shutil.copyfile(fixture, folder / 'ERB' / (case_id + '.ERB'))
                shutil.copyfile(config, folder / 'emuera.config')
                runs[side] = folder
            before = {side: harness.input_inventory(folder) for side, folder in runs.items()}
            if before['native'] != before['py']:
                raise RuntimeError("side inputs differ")
            report['inputs_before'] = before
            py = subprocess.run([sys.executable, '-I', str(pyz), '--debug', '.'], cwd=runs['py'],
                                input=((text + '\n').encode() if text is not None else b'\n'),
                                capture_output=True, timeout=30)
            (runs['py']/'stdout.bin').write_bytes(py.stdout)
            (runs['py']/'stderr.bin').write_bytes(py.stderr)
            report['py_returncode'] = py.returncode
            shutil.copyfile(exe, runs['native']/'Emuera1824+v24.exe')
            executable = runs['native']/'Emuera1824+v24.exe'
            if validator.sha(executable) != harness.NATIVE_SHA:
                raise RuntimeError("copied Native binary mismatch")
            harness.check_lock(lock_dir, nonce)
            if harness.native_processes():
                raise RuntimeError("Native already running")
            error = None
            try:
                observer = None if case_id == 'RESULT_WRITE' else lambda desk, name, pid, handle: observe_window(
                    desk, name, pid, handle, runs['native'], text)
                report['native'] = native.run(executable, runs['native'], observe=observer)
            except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
                error = str(exc)
                report['native_error'] = error
            remaining = harness.wait_for_native_absence()
            report['native_processes_after'] = remaining
            if remaining or error:
                raise RuntimeError("Native failure or remaining process: " + str(error))
            harness.check_lock(lock_dir, nonce)
            after = {side: harness.input_inventory(folder) for side, folder in runs.items()}
            report['inputs_after'] = after
            if after != before or validator.sha(executable) != harness.NATIVE_SHA:
                raise RuntimeError("inputs or Native binary changed")
            harness.validate_inputs(exe, pyz, config)
            if validator.sha(fixture) != fixture_sha or any(validator.sha(HERE/name) != value for name, value in tools.items()):
                raise RuntimeError("fixture or tool changed")
            if case_id == 'RESULT_WRITE':
                nlog = runs['native']/'emuera.log'
                plog = runs['py']/'.pyemuera/logs/emuera.log'
                def observations(path, side):
                    decoded, encoding = core.decode_log(harness.bounded_read(path), side)
                    lines = decoded.replace('\r\n', '\n').split('\n')
                    markers = ['BEFORE_RESULT=[701]', 'BEFORE_RESULTS=[AUTO_SENT]',
                               'AFTER_RESULT=[42]', 'AFTER_RESULTS=[123]', 'OBSERVATIONS_DONE']
                    return {"encoding": encoding, "markers": {x: lines.count(x) for x in markers},
                            "ordered": all(lines.count(x) == 1 for x in markers) and
                            [lines.index(x) for x in markers] == sorted(lines.index(x) for x in markers)}
                report['native_observations'] = observations(nlog, 'native')
                report['py_observations'] = observations(plog, 'py')
                report['status'] = ('observed' if py.returncode == 0 else 'observed_with_py_nonzero') if (
                    report['native_observations']['ordered'] and report['py_observations']['ordered']) else 'not_observed'
            else:
                # A successful capture API is not evidence that pixels are readable.
                observation = report['native'].get('observation', {})
                report['status'] = ('visual_review_required' if observation.get('status') == 'captured'
                                    and (text is None or observation.get('input_sent')) else 'not_observed')
        except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
            report['error'] = str(exc)
    report['lock_released'] = True
    validator.write(target/'RESULT.json', report)
    validator.seal(target)
    return target, report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case', required=True, choices=sorted(CASES))
    p.add_argument('--native', required=True, type=Path)
    p.add_argument('--pyz', required=True, type=Path)
    p.add_argument('--config', type=Path, default=HERE/'fixtures/emuera.config')
    p.add_argument('--lock-dir', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    a = p.parse_args()
    try:
        target, result = run_case(a.case, a.native, a.pyz, a.config, a.lock_dir, a.out)
        print(json.dumps({'attempt': str(target), 'result': result}, ensure_ascii=True, indent=2))
        return 1 if result['status'] == 'failure' else 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
