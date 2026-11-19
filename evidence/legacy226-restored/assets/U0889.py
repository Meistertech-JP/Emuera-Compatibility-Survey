import ctypes as c
import hashlib
from ctypes import wintypes as w
import json
import subprocess
import shutil
import sys
import time
import uuid
from pathlib import Path

u = c.WinDLL("user32", use_last_error=True)
k = c.WinDLL("kernel32", use_last_error=True)
class STARTUPINFO(c.Structure):
    _fields_ = [("cb", w.DWORD), ("reserved", w.LPWSTR), ("desktop", w.LPWSTR),
                ("title", w.LPWSTR), ("x", w.DWORD), ("y", w.DWORD),
                ("xsize", w.DWORD), ("ysize", w.DWORD), ("xcount", w.DWORD),
                ("ycount", w.DWORD), ("fill", w.DWORD), ("flags", w.DWORD),
                ("show", w.WORD), ("reserved2count", w.WORD), ("reserved2", c.c_void_p),
                ("stdin", w.HANDLE), ("stdout", w.HANDLE), ("stderr", w.HANDLE)]
class PROCESSINFO(c.Structure):
    _fields_ = [("process", w.HANDLE), ("thread", w.HANDLE), ("pid", w.DWORD), ("tid", w.DWORD)]
u.CreateDesktopW.argtypes = [w.LPCWSTR, w.LPCWSTR, c.c_void_p, w.DWORD, w.DWORD, c.c_void_p]
u.CreateDesktopW.restype = w.HANDLE
u.CloseDesktop.argtypes = [w.HANDLE]
k.CreateProcessW.argtypes = [w.LPCWSTR, w.LPWSTR, c.c_void_p, c.c_void_p, w.BOOL, w.DWORD,
                             c.c_void_p, w.LPCWSTR, c.POINTER(STARTUPINFO), c.POINTER(PROCESSINFO)]
k.CreateProcessW.restype = w.BOOL
k.TerminateProcess.argtypes = [w.HANDLE, w.UINT]
k.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
k.CloseHandle.argtypes = [w.HANDLE]
CALLBACK = c.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
u.EnumDesktopWindows.argtypes = [w.HANDLE, CALLBACK, w.LPARAM]
u.GetWindowThreadProcessId.argtypes = [w.HWND, c.POINTER(w.DWORD)]
u.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, c.c_int]
u.GetWindowTextW.argtypes = [w.HWND, w.LPWSTR, c.c_int]
u.EnumChildWindows.argtypes = [w.HWND, CALLBACK, w.LPARAM]
u.SendMessageTimeoutW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM, w.UINT, w.UINT, c.POINTER(c.c_size_t)]
u.SendMessageTimeoutW.restype = w.LPARAM
u.PostMessageW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
name = "PyEmueraProbe_" + uuid.uuid4().hex
root = Path(__file__).resolve().parent
evidence_root = root
case_dir = evidence_root / "native-cases"
native = "--native" in sys.argv
# Explicit generic case selection: reject ambiguous or unsafe names before creating a process.
import re
input_options = [arg for arg in sys.argv[1:] if arg.startswith("--input-text-hex=")]
if len(input_options) > 1:
    raise SystemExit("Specify at most one --input-text-hex=HEX")
input_text = None
if input_options:
    raw_hex = input_options[0].split("=", 1)[1]
    if not re.fullmatch(r"[0-9a-fA-F]{0,512}", raw_hex) or len(raw_hex) % 2:
        raise SystemExit("Input text must be bounded even-length UTF-8 hex")
    try:
        input_text = bytes.fromhex(raw_hex).decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise SystemExit("Input text must be valid UTF-8")
    if any(ch in input_text for ch in ("\0", "\r", "\n")):
        raise SystemExit("Input text must not contain NUL or line breaks")
    if not native or "--send-input" not in sys.argv or not any(arg.startswith("--case=") for arg in sys.argv[1:]):
        raise SystemExit("Explicit input requires --native, --send-input, and --case=NAME")
    if "--japanese" in sys.argv or "--invalid-first" in sys.argv:
        raise SystemExit("Explicit input cannot be combined with preset inputs")
sample_options = [arg for arg in sys.argv[1:] if arg.startswith("--capture-samples=")]
if len(sample_options) > 1:
    raise SystemExit("Specify at most one --capture-samples=N")
sample_text = sample_options[0].split("=", 1)[1] if sample_options else "1"
if not re.fullmatch(r"[1-5]", sample_text):
    raise SystemExit("Capture sample count must be an integer from 1 to 5")
sample_count = int(sample_text)
if sample_options and not native:
    raise SystemExit("Capture samples require --native")
case_options = [arg for arg in sys.argv[1:] if arg.startswith("--case=")]
if len(case_options) > 1:
    raise SystemExit("Specify at most one --case=NAME")
case_arg = case_options[0][len("--case="):] if case_options else None
if case_arg is not None:
    if not re.fullmatch(r"[A-Z][A-Z0-9]{0,31}", case_arg):
        raise SystemExit("Invalid case name; use uppercase letters and digits only")
    fixture = evidence_root / "variants" / case_arg
    if not (fixture / "ERB").is_dir() or not (fixture / "csv").is_dir() or not any((fixture / "ERB").glob("*.ERB")):
        raise SystemExit("Unknown or incomplete case: " + case_arg)
    selector_line = next(line for line in Path(__file__).read_text(encoding="utf-8").splitlines() if line.startswith("case = "))
    flags = set(re.findall(r'"(--[a-z0-9]+)" in sys\.argv', selector_line))
    flags.add("--p35")
    if any(flag in sys.argv for flag in flags):
        raise SystemExit("Do not mix --case=NAME with legacy case-selection flags")
case = case_arg if case_arg is not None else "PRINTDATAW01" if "--printdataw01" in sys.argv else "E12B" if "--e12b" in sys.argv else "E12" if "--e12" in sys.argv else "E143F" if "--e143f" in sys.argv else "UNIMP05" if "--unimp05" in sys.argv else "UNIMP06" if "--unimp06" in sys.argv else "UNIMP03" if "--unimp03" in sys.argv else "UNIMP04" if "--unimp04" in sys.argv else "UNIMP01" if "--unimp01" in sys.argv else "UNIMP02" if "--unimp02" in sys.argv else "PRINT02" if "--print02" in sys.argv else "PRINT01" if "--print01" in sys.argv else "PRINTW01" if "--printw01" in sys.argv else "LOCAL01" if "--local01" in sys.argv else "GLOBAL03" if "--global03" in sys.argv else "TERNARY01" if "--ternary01" in sys.argv else "TARGET01" if "--target01" in sys.argv else "UNARY03" if "--unary03" in sys.argv else "UNARY02" if "--unary02" in sys.argv else "UNARY01" if "--unary01" in sys.argv else "ORDER02" if "--order02" in sys.argv else "ORDER03" if "--order03" in sys.argv else "ORDER01" if "--order01" in sys.argv else "E143E" if "--e143e" in sys.argv else "LOGFILE02" if "--logfile02" in sys.argv else "LOGFILE01" if "--logfile01" in sys.argv else "CHARA01" if "--chara01" in sys.argv else "LOGIC03" if "--logic03" in sys.argv else "LOGIC02" if "--logic02" in sys.argv else "LOGIC01" if "--logic01" in sys.argv else "P38B" if "--p38b" in sys.argv else "DECL30" if "--decl30" in sys.argv else "DECL29" if "--decl29" in sys.argv else "E143D" if "--e143d" in sys.argv else "DECL28" if "--decl28" in sys.argv else "DECL27" if "--decl27" in sys.argv else "DECL26" if "--decl26" in sys.argv else "DECL25" if "--decl25" in sys.argv else "DECL24" if "--decl24" in sys.argv else "DECL23" if "--decl23" in sys.argv else "RANDOM02" if "--random02" in sys.argv else "RANDOM01" if "--random01" in sys.argv else "DECL22" if "--decl22" in sys.argv else "DECL19" if "--decl19" in sys.argv else "DECL20" if "--decl20" in sys.argv else "DECL21" if "--decl21" in sys.argv else "DECL18" if "--decl18" in sys.argv else "DECL17" if "--decl17" in sys.argv else "DECL15" if "--decl15" in sys.argv else "DECL16" if "--decl16" in sys.argv else "DECL12" if "--decl12" in sys.argv else "DECL13" if "--decl13" in sys.argv else "DECL14" if "--decl14" in sys.argv else "DECL11" if "--decl11" in sys.argv else "DECL09" if "--decl09" in sys.argv else "DECL10" if "--decl10" in sys.argv else "DECL08" if "--decl08" in sys.argv else "DECL07" if "--decl07" in sys.argv else "DECL06" if "--decl06" in sys.argv else "DECL05" if "--decl05" in sys.argv else "DECL03" if "--decl03" in sys.argv else "DECL04" if "--decl04" in sys.argv else "DECL01" if "--decl01" in sys.argv else "DECL02" if "--decl02" in sys.argv else "METHODCMD10" if "--methodcmd10" in sys.argv else "METHODCMD11" if "--methodcmd11" in sys.argv else "METHODCMD12" if "--methodcmd12" in sys.argv else "METHODCMD09" if "--methodcmd09" in sys.argv else "GLOBAL02" if "--global02" in sys.argv else "GLOBAL01" if "--global01" in sys.argv else "E56C" if "--e56c" in sys.argv else "E56D" if "--e56d" in sys.argv else "E56E" if "--e56e" in sys.argv else "E56F" if "--e56f" in sys.argv else "E56G" if "--e56g" in sys.argv else "E56B" if "--e56b" in sys.argv else "E10" if "--e10" in sys.argv else "E52" if "--e52" in sys.argv else "E53" if "--e53" in sys.argv else "E56" if "--e56" in sys.argv else "METHODCMD08" if "--methodcmd08" in sys.argv else "METHODCMD07" if "--methodcmd07" in sys.argv else "METHODCMD05" if "--methodcmd05" in sys.argv else "METHODCMD06" if "--methodcmd06" in sys.argv else "METHODCMD04" if "--methodcmd04" in sys.argv else "METHODCMD03" if "--methodcmd03" in sys.argv else "METHODCMD02" if "--methodcmd02" in sys.argv else "METHODCMD01" if "--methodcmd01" in sys.argv else "ASSIGN02" if "--assign02" in sys.argv else "ASSIGN01" if "--assign01" in sys.argv else "E165B" if "--e165b" in sys.argv else "E165C" if "--e165c" in sys.argv else "E134B" if "--e134b" in sys.argv else "E135B" if "--e135b" in sys.argv else "P31" if "--p31" in sys.argv else "P32" if "--p32" in sys.argv else "GETCONFIG03" if "--getconfig03" in sys.argv else "GETCONFIG02" if "--getconfig02" in sys.argv else "GETCONFIG01" if "--getconfig01" in sys.argv else "POWER05" if "--power05" in sys.argv else "POWER04" if "--power04" in sys.argv else "POWER03" if "--power03" in sys.argv else "POWER02" if "--power02" in sys.argv else "POWER01" if "--power01" in sys.argv else "E55" if "--e55" in sys.argv else "LOOP04" if "--loop04" in sys.argv else "LOOP03" if "--loop03" in sys.argv else "LOOP02" if "--loop02" in sys.argv else "LOOP01" if "--loop01" in sys.argv else "E11B" if "--e11b" in sys.argv else "E143C" if "--e143c" in sys.argv else "E143B" if "--e143b" in sys.argv else "E117" if "--e117" in sys.argv else "P36" if "--p36" in sys.argv else "P35"
case_dir = evidence_root / "native-cases" / (case + "-" + uuid.uuid4().hex[:8])
# Refuse mistyped case flags instead of silently running the default P35.
import re
known_flags = set(re.findall(r'"(--[a-z0-9]+)" in sys\.argv', Path(__file__).read_text(encoding="utf-8")))
known_flags.update({"--printdataw01", "--native", "--send-input", "--p35", "--japanese", "--invalid-first", "--send-second"})
unknown_flags = [x for x in sys.argv[1:] if x.startswith("--") and x not in known_flags and x not in case_options and x not in sample_options and x not in input_options]
if unknown_flags:
    raise SystemExit("Unrecognized option(s): " + ", ".join(unknown_flags))
if native and case_arg is None:
    selector_line = next(line for line in Path(__file__).read_text(encoding="utf-8").splitlines() if line.startswith("case = "))
    selectors = set(re.findall(r'"(--[a-z0-9]+)" in sys\.argv', selector_line)) | {"--p35", "--printdataw01"}
    if not any(flag in sys.argv for flag in selectors):
        raise SystemExit("Specify --case=NAME or an explicit legacy case flag")
send_input = "--send-input" in sys.argv
if native:
    case_dir.mkdir()
    template = evidence_root / "raw"
    for filename in ("Emuera1824+v24.exe", "emuera.config"):
        shutil.copy2(template / filename, case_dir / filename)
    shutil.copytree(evidence_root / "variants" / case / "ERB", case_dir / "ERB")
    shutil.copytree(evidence_root / "variants" / case / "csv", case_dir / "csv")
    if case == "LOGFILE02":
        (case_dir / "emuera.log").mkdir()
    if case == "DECL28":
        config_path = case_dir / "emuera.config"
        data = config_path.read_bytes()
        old_setting = "セーブデータをバイナリ形式で保存する:NO".encode("cp932")
        new_setting = "セーブデータをバイナリ形式で保存する:YES".encode("cp932")
        assert data.count(old_setting) == 1
        config_path.write_bytes(data.replace(old_setting, new_setting))
    if case == "LOADREAD01":
        shutil.copy2(root / "inputs" / "LOADREAD01" / "save00.sav", case_dir / "save00.sav")  # Public derivative: relocated seed; preserve its original bytes.
    if case == "GLOBAL02":
        prior = json.loads((root / "runs" / "global-01" / "comparison.json").read_text(encoding="utf-8"))
        seed = (root / prior["native_probe"]).parent / "global.sav"
        expected = prior["native_candidate_save_files"]["global.sav"]
        assert hashlib.sha256(seed.read_bytes()).hexdigest() == expected
        shutil.copy2(seed, case_dir / "global.sav")
        assert hashlib.sha256((case_dir / "global.sav").read_bytes()).hexdigest() == expected
def input_manifest():
    return {str(f.relative_to(case_dir)).replace("\\", "/"): hashlib.sha256(f.read_bytes()).hexdigest()
            for folder in ("ERB", "csv") for f in sorted((case_dir / folder).rglob("*")) if f.is_file()}
before_manifest = input_manifest() if native else None
desk = u.CreateDesktopW(name, None, None, 0, 0x01FF, None)
info = PROCESSINFO()
report = {"desktop": name, "desktop_created": bool(desk), "no_input_sent": True}
def native_artifact_hashes():
    return {filename: hashlib.sha256((case_dir / filename).read_bytes()).hexdigest()
            for filename in ("Emuera1824+v24.exe", "emuera.config")}
if native:
    report["native_artifact_sha256_before"] = native_artifact_hashes()
try:
    if not desk:
        report["desktop_error"] = c.get_last_error()
    else:
        startup = STARTUPINFO()
        startup.cb = c.sizeof(startup)
        startup.desktop = "WinSta0\\" + name
        application = str(case_dir / "Emuera1824+v24.exe") if native else sys.executable
        args = [application, "-Debug"] if native else [application, "-c", "import tkinter as t; w=t.Tk(); w.title('isolated probe'); w.mainloop()"]
        report["mode"] = "native" if native else "tk_test"
        command = c.create_unicode_buffer(subprocess.list2cmdline(args))
        ok = k.CreateProcessW(application, command, None, None, False, 0, None, str(case_dir) if native else None, c.byref(startup), c.byref(info))
        report["create_process_ok"] = bool(ok)
        if not ok:
            report["process_error"] = c.get_last_error()
        else:
            report["pid"] = info.pid
            time.sleep(6)
            found = []
            @CALLBACK
            def visit(hwnd, unused):
                pid = w.DWORD()
                u.GetWindowThreadProcessId(hwnd, c.byref(pid))
                found.append({"hwnd": int(hwnd), "pid": pid.value})
                return True
            report["enumeration_ok"] = bool(u.EnumDesktopWindows(desk, visit, 0))
            report["windows"] = found
            report["own_windows"] = [x for x in found if x["pid"] == info.pid]
            if native:
                children = []
                @CALLBACK
                def child_visit(hwnd, unused):
                    cls = c.create_unicode_buffer(256)
                    title = c.create_unicode_buffer(512)
                    u.GetClassNameW(hwnd, cls, len(cls))
                    u.GetWindowTextW(hwnd, title, len(title))
                    pid = w.DWORD()
                    u.GetWindowThreadProcessId(hwnd, c.byref(pid))
                    children.append({"hwnd": int(hwnd), "pid": pid.value, "class": cls.value, "title": title.value})
                    return True
                parent_of = {}
                for window in report["own_windows"]:
                    before = len(children)
                    u.EnumChildWindows(window["hwnd"], child_visit, 0)
                    for child in children[before:]:
                        parent_of[child["hwnd"]] = window["hwnd"]
                report["children"] = children
                # Read displayed text from owned RichEdit controls; no full screenshot is retained.
                control_texts = []
                for child in children:
                    if child["pid"] == info.pid and "RICHEDIT" in child["class"]:
                        length = c.c_size_t()
                        ok_len = bool(u.SendMessageTimeoutW(child["hwnd"], 0x000E, 0, 0, 2, 2000, c.byref(length)))
                        if ok_len and 0 <= length.value <= 200000:
                            buf_text = c.create_unicode_buffer(length.value + 1)
                            got = c.c_size_t()
                            ok_text = bool(u.SendMessageTimeoutW(child["hwnd"], 0x000D, len(buf_text), c.cast(buf_text, c.c_void_p).value, 2, 2000, c.byref(got)))
                            control_texts.append({"hwnd": child["hwnd"], "length": length.value, "ok": ok_text, "text": buf_text.value if ok_text else None})
                report["rich_edit_text"] = control_texts
                editors = [x for x in children if "RICHEDIT" in x["class"] and x["pid"] == info.pid]
                if native and case == "LOGFILE02":
                    failure = [x for x in children if x["pid"] == info.pid and x["class"] == "Static" and x["title"] == "ログの出力に失敗しました"]
                    buttons = [x for x in children if x["pid"] == info.pid and x["class"] == "Button" and x["title"] == "OK"]
                    if len(failure) == 1 and len(buttons) == 1 and parent_of[failure[0]["hwnd"]] == parent_of[buttons[0]["hwnd"]]:
                        dialog = parent_of[buttons[0]["hwnd"]]
                        cap_dialog = subprocess.run([sys.executable, str(root / "capture_dialog.py"), "dialog-" + case + "-" + name[-8:], str(dialog), name], capture_output=True, text=True, timeout=15)
                        report["dialog_capture_returncode"] = cap_dialog.returncode
                        report["dialog_capture_output"] = cap_dialog.stdout + cap_dialog.stderr
                        report["owned_dialog_button_posted"] = bool(u.PostMessageW(buttons[0]["hwnd"], 0x00F5, 0, 0))
                        if report["owned_dialog_button_posted"]:
                            report["no_input_sent"] = False
                        time.sleep(2)
                if native and (case_arg is not None or case in ("E12B", "E12", "E143F", "UNIMP05", "UNIMP06", "UNIMP03", "UNIMP04", "UNIMP01", "UNIMP02", "PRINT02", "PRINT01", "PRINTW01", "LOCAL01", "GLOBAL03", "TERNARY01", "TARGET01", "UNARY03", "UNARY01", "UNARY02", "ORDER02", "ORDER03", "ORDER01", "E143E", "LOGFILE02", "LOGFILE01", "CHARA01", "LOGIC03", "LOGIC02", "LOGIC01", "P38B", "DECL30", "DECL29", "E143D", "DECL28", "DECL27", "DECL26", "DECL25", "DECL24", "DECL23", "RANDOM02", "RANDOM01", "DECL22", "DECL19", "DECL20", "DECL21", "DECL18", "DECL17", "DECL15", "DECL16", "DECL12", "DECL13", "DECL14", "DECL11", "DECL09", "DECL10", "DECL08", "DECL07", "DECL06", "DECL05", "DECL03", "DECL04", "DECL01", "DECL02", "METHODCMD10", "METHODCMD11", "METHODCMD12", "METHODCMD09", "GLOBAL02", "GLOBAL01", "E56C", "E56D", "E56E", "E56F", "E56G", "E56B", "E10", "E52", "E53", "E56", "METHODCMD08", "METHODCMD07", "METHODCMD05", "METHODCMD06", "METHODCMD04", "METHODCMD03", "METHODCMD02", "METHODCMD01", "ASSIGN02", "ASSIGN01", "E165B", "E165C", "E134B", "E135B", "P31", "P32", "E117", "E143B", "E143C", "E11B", "E55", "POWER01", "POWER02", "POWER03", "POWER04", "POWER05", "LOOP01", "LOOP02", "LOOP03", "LOOP04", "GETCONFIG01", "GETCONFIG02", "GETCONFIG03")) and len(editors) == 1:
                    parent = parent_of[editors[0]["hwnd"]]
                    cap = subprocess.run([sys.executable, str(root / "capture_one.py"), "fresh-" + case + "-" + name[-8:], str(parent), name], capture_output=True, text=True, timeout=15)
                    report["capture_returncode"] = cap.returncode
                    report["capture_output"] = cap.stdout + cap.stderr
                    report["capture_samples"] = [{"sample": 1, "returncode": cap.returncode, "output": cap.stdout + cap.stderr}]
                    for sample in range(2, sample_count + 1):
                        time.sleep(1)
                        sample_tag = "fresh-" + case + "-sample" + str(sample) + "-" + name[-8:]
                        sampled = subprocess.run([sys.executable, str(root / "capture_one.py"), sample_tag, str(parent), name], capture_output=True, text=True, timeout=15)
                        report["capture_samples"].append({"sample": sample, "returncode": sampled.returncode, "output": sampled.stdout + sampled.stderr})
                if send_input and len(editors) == 1:
                    editor = editors[0]["hwnd"]
                    parent = parent_of[editor]
                    invalid_probe = "--invalid-first" in sys.argv and case == "P35"
                    value = input_text if input_text is not None else "ABC" if invalid_probe else "42" if case == "P35" else "日本語テスト" if "--japanese" in sys.argv else "ABC"
                    if input_options:
                        report["requested_input_utf8_hex"] = raw_hex.lower()
                    buf = c.create_unicode_buffer(value)
                    result = c.c_size_t()
                    ok_text = bool(u.SendMessageTimeoutW(editor, 0x000C, 0, c.cast(buf, c.c_void_p).value, 2, 3000, c.byref(result)))
                    report["set_text_ok"] = ok_text
                    report["set_text_result"] = result.value
                    if ok_text and result.value:
                        report["keydown_posted"] = bool(u.PostMessageW(editor, 0x0100, 13, 0x001C0001))
                        report["keyup_posted"] = bool(u.PostMessageW(editor, 0x0101, 13, 0xC01C0001))
                        if case == "PRINTDATAW01":
                            time.sleep(2)
                            early_log = case_dir / "debug" / "console.log"
                            report["wait_phase_log_before_resume"] = early_log.read_bytes().decode("cp932", errors="replace") if early_log.is_file() else None
                            report["wait_phase_process_alive"] = k.WaitForSingleObject(info.process, 0) != 0
                            crop_path = root / "native-wait-crop.png"
                            crop_run = subprocess.run([sys.executable, str(root / "capture_crop_only.py"), "PRINTDATAW01-midwait", str(parent), name, str(crop_path)], capture_output=True, text=True, timeout=20)
                            report["wait_crop_capture_returncode"] = crop_run.returncode
                            report["wait_crop_capture_output"] = crop_run.stdout + crop_run.stderr
                            report["wait_crop_file"] = str(crop_path) if crop_path.is_file() else None
                            report["wait_resume_keydown"] = bool(u.PostMessageW(editor, 0x0100, 13, 0x001C0001))
                            report["wait_resume_keyup"] = bool(u.PostMessageW(editor, 0x0101, 13, 0xC01C0001))
                            time.sleep(2)
                            report["wait_phase_log_after_resume"] = early_log.read_bytes().decode("cp932", errors="replace") if early_log.is_file() else None
                        if case == "LOADREAD01" and "--send-second" in sys.argv:
                            time.sleep(2)
                            buf_second = c.create_unicode_buffer("100")
                            result_second = c.c_size_t()
                            report["second_set_text_ok"] = bool(u.SendMessageTimeoutW(editor, 0x000C, 0, c.cast(buf_second, c.c_void_p).value, 2, 3000, c.byref(result_second)))
                            report["second_set_text_result"] = result_second.value
                            if report["second_set_text_ok"] and result_second.value:
                                report["second_keydown_posted"] = bool(u.PostMessageW(editor, 0x0100, 13, 0x001C0001))
                                report["second_keyup_posted"] = bool(u.PostMessageW(editor, 0x0101, 13, 0xC01C0001))
                        report["no_input_sent"] = False
                        time.sleep(10)
                        if invalid_probe:
                            mid = subprocess.run([sys.executable, str(root / "capture_one.py"), "invalid-P35-" + name[-8:], str(parent), name], capture_output=True, text=True, timeout=15)
                            report["invalid_capture_returncode"] = mid.returncode
                            report["invalid_capture_output"] = mid.stdout + mid.stderr
                            buf2 = c.create_unicode_buffer("42")
                            result2 = c.c_size_t()
                            ok2 = bool(u.SendMessageTimeoutW(editor, 0x000C, 0, c.cast(buf2, c.c_void_p).value, 2, 3000, c.byref(result2)))
                            report["second_set_ok"] = ok2 and bool(result2.value)
                            if report["second_set_ok"]:
                                report["second_keydown_posted"] = bool(u.PostMessageW(editor, 0x0100, 13, 0x001C0001))
                                report["second_keyup_posted"] = bool(u.PostMessageW(editor, 0x0101, 13, 0xC01C0001))
                                time.sleep(3)
                        cap = subprocess.run([sys.executable, str(root / "capture_one.py"), "isolated-" + case + "-" + name[-8:], str(parent), name], capture_output=True, text=True, timeout=15)
                        report["capture_returncode"] = cap.returncode
                        report["capture_output"] = cap.stdout + cap.stderr
                if native and case in ("DEBUGPRINT01", "PRINTDATAW01"):
                    time.sleep(1)
                    debug_tops = []
                    @CALLBACK
                    def debug_top_visit(hwnd, unused):
                        pid = w.DWORD()
                        u.GetWindowThreadProcessId(hwnd, c.byref(pid))
                        title = c.create_unicode_buffer(512)
                        u.GetWindowTextW(hwnd, title, len(title))
                        if pid.value == info.pid:
                            debug_tops.append({"hwnd": int(hwnd), "title": title.value})
                        return True
                    u.EnumDesktopWindows(desk, debug_top_visit, 0)
                    report["debug_toplevel_windows"] = debug_tops
                    closing = [x for x in debug_tops if "デバッグ" in x["title"] or "Debug" in x["title"]]
                    report["debug_dialog_close_posted"] = [bool(u.PostMessageW(x["hwnd"], 0x0010, 0, 0)) for x in closing]
                    time.sleep(2)
                    log_path = case_dir / "debug" / "console.log"
                    report["debug_console_log_exists"] = log_path.is_file()
                    if log_path.is_file():
                        report["debug_console_log"] = log_path.read_text(encoding="cp932", errors="replace")
finally:
    if info.process:
        wait_state = k.WaitForSingleObject(info.process, 0)
        report["process_signaled_before_cleanup"] = wait_state == 0
        exit_code = w.DWORD()
        if wait_state == 0 and hasattr(k, "GetExitCodeProcess"):
            k.GetExitCodeProcess.argtypes = [w.HANDLE, c.POINTER(w.DWORD)]
            k.GetExitCodeProcess.restype = w.BOOL
            report["process_exit_code_observed"] = bool(k.GetExitCodeProcess(info.process, c.byref(exit_code)))
            report["process_exit_code"] = exit_code.value
        if wait_state != 0:
            k.TerminateProcess(info.process, 0)
        k.WaitForSingleObject(info.process, 5000)
        k.CloseHandle(info.thread)
        k.CloseHandle(info.process)
    if desk:
        report["closed_desktop"] = bool(u.CloseDesktop(desk))
    if native:
        report["input_sha256_before"] = before_manifest
        report["input_sha256_after"] = input_manifest()
        report["native_artifact_sha256_after"] = native_artifact_hashes()
    (case_dir / "probe.json" if native else root / "DESKTOP_CREATEPROCESS_PROBE.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report))





