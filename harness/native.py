"""Windows isolated-desktop process control; termination uses only our process handle."""
import ctypes as c
from ctypes import wintypes as w
import subprocess
import time
import uuid


def run(exe, cwd, timeout=5, observe=None):
    if not hasattr(c, "WinDLL"):
        raise RuntimeError("Native execution requires Windows")
    user = c.WinDLL("user32", use_last_error=True)
    kernel = c.WinDLL("kernel32", use_last_error=True)

    class Startup(c.Structure):
        _fields_ = [("cb", w.DWORD), ("reserved", w.LPWSTR), ("desktop", w.LPWSTR),
                    ("title", w.LPWSTR), ("x", w.DWORD), ("y", w.DWORD),
                    ("xsize", w.DWORD), ("ysize", w.DWORD), ("xcount", w.DWORD),
                    ("ycount", w.DWORD), ("fill", w.DWORD), ("flags", w.DWORD),
                    ("show", w.WORD), ("reserved2count", w.WORD), ("reserved2", c.c_void_p),
                    ("stdin", w.HANDLE), ("stdout", w.HANDLE), ("stderr", w.HANDLE)]

    class Process(c.Structure):
        _fields_ = [("process", w.HANDLE), ("thread", w.HANDLE), ("pid", w.DWORD), ("tid", w.DWORD)]

    user.CreateDesktopW.argtypes = [w.LPCWSTR, w.LPCWSTR, c.c_void_p, w.DWORD, w.DWORD, c.c_void_p]
    user.CreateDesktopW.restype = w.HANDLE
    user.CloseDesktop.argtypes = [w.HANDLE]
    user.CloseDesktop.restype = w.BOOL
    kernel.CreateProcessW.argtypes = [w.LPCWSTR, w.LPWSTR, c.c_void_p, c.c_void_p, w.BOOL,
                                     w.DWORD, c.c_void_p, w.LPCWSTR, c.POINTER(Startup), c.POINTER(Process)]
    kernel.CreateProcessW.restype = w.BOOL
    kernel.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
    kernel.WaitForSingleObject.restype = w.DWORD
    kernel.GetExitCodeProcess.argtypes = [w.HANDLE, c.POINTER(w.DWORD)]
    kernel.GetExitCodeProcess.restype = w.BOOL
    kernel.TerminateProcess.argtypes = [w.HANDLE, w.UINT]
    kernel.TerminateProcess.restype = w.BOOL
    kernel.CloseHandle.argtypes = [w.HANDLE]
    name = "EmueraHarness_" + uuid.uuid4().hex
    desk = user.CreateDesktopW(name, None, None, 0, 0x01FF, None)
    if not desk:
        raise OSError(c.get_last_error(), "CreateDesktopW failed")
    proc = Process()
    receipt = {"desktop_created": True, "process_created": False, "input_sent": False}
    try:
        startup = Startup()
        startup.cb = c.sizeof(Startup)
        startup.desktop = "WinSta0\\" + name
        command = c.create_unicode_buffer(subprocess.list2cmdline([str(exe)]))
        if not kernel.CreateProcessW(str(exe), command, None, None, False, 0, None,
                                     str(cwd), c.byref(startup), c.byref(proc)):
            raise OSError(c.get_last_error(), "CreateProcessW failed")
        receipt.update(process_created=True, pid=proc.pid)
        if observe is not None:
            receipt["observation"] = observe(desk, name, proc.pid, proc.process)
            receipt["input_sent"] = bool(receipt["observation"].get("input_sent", False))
        state = kernel.WaitForSingleObject(proc.process, int(timeout * 1000))
        if state == 0:
            code = w.DWORD()
            if not kernel.GetExitCodeProcess(proc.process, c.byref(code)):
                raise OSError(c.get_last_error(), "GetExitCodeProcess failed")
            receipt.update(outcome="natural_rc0" if code.value == 0 else "natural_nonzero", exit_code=code.value)
        elif state == 0x102:
            if not kernel.TerminateProcess(proc.process, 1):
                raise OSError(c.get_last_error(), "TerminateProcess failed")
            if kernel.WaitForSingleObject(proc.process, 5000) != 0:
                raise RuntimeError("owned process termination not confirmed")
            receipt.update(outcome="forced_termination", exit_code=None)
        else:
            raise OSError(c.get_last_error(), "process wait failed")
    finally:
        if proc.process:
            # The handle refers only to the process created above, even if its PID is reused.
            if kernel.WaitForSingleObject(proc.process, 0) == 0x102:
                receipt["finally_terminate_ok"] = bool(kernel.TerminateProcess(proc.process, 1))
                receipt["finally_wait_ok"] = kernel.WaitForSingleObject(proc.process, 5000) == 0
            kernel.CloseHandle(proc.thread)
            kernel.CloseHandle(proc.process)
        receipt["desktop_closed"] = bool(user.CloseDesktop(desk))
    if not receipt["desktop_closed"]:
        raise RuntimeError("desktop close not confirmed")
    return receipt
