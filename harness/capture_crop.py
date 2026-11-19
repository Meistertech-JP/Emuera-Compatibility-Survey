"""Capture a bounded crop of a verified owned window on a private desktop."""
import ctypes as c
from ctypes import wintypes as w
from pathlib import Path
import struct
import sys


def main():
    desktop, parent_text, pid_text, output = sys.argv[1:]
    parent, expected_pid = int(parent_text), int(pid_text)
    user = c.WinDLL("user32", use_last_error=True)
    gdi = c.WinDLL("gdi32", use_last_error=True)
    user.OpenDesktopW.argtypes = [w.LPCWSTR, w.DWORD, w.BOOL, w.DWORD]
    user.OpenDesktopW.restype = w.HANDLE
    user.SetThreadDesktop.argtypes = [w.HANDLE]
    user.SetThreadDesktop.restype = w.BOOL
    desk = user.OpenDesktopW(desktop, 0, False, 0x01FF)
    if not desk or not user.SetThreadDesktop(desk):
        raise OSError(c.get_last_error(), "cannot attach capture thread")
    user.GetWindowThreadProcessId.argtypes = [w.HWND, c.POINTER(w.DWORD)]
    owner = w.DWORD()
    user.GetWindowThreadProcessId(parent, c.byref(owner))
    if owner.value != expected_pid:
        raise ValueError("parent window does not belong to owned process")
    callback = c.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
    user.EnumChildWindows.argtypes = [w.HWND, callback, w.LPARAM]
    user.GetWindowRect.argtypes = [w.HWND, c.POINTER(w.RECT)]
    candidates = []
    @callback
    def visit(hwnd, _):
        owner = w.DWORD()
        user.GetWindowThreadProcessId(hwnd, c.byref(owner))
        rect = w.RECT()
        if owner.value == expected_pid and user.GetWindowRect(hwnd, c.byref(rect)):
            width, height = rect.right - rect.left, rect.bottom - rect.top
            if 700 <= width <= 4096 and 400 <= height <= 4096:
                candidates.append((hwnd, width, height))
        return True
    user.EnumChildWindows(parent, visit, 0)
    if not candidates:
        raise ValueError("owned display surface not found")
    target, width, height = candidates[0]
    user.GetWindowDC.argtypes = [w.HWND]
    user.GetWindowDC.restype = w.HDC
    user.ReleaseDC.argtypes = [w.HWND, w.HDC]
    user.PrintWindow.argtypes = [w.HWND, w.HDC, w.UINT]
    user.PrintWindow.restype = w.BOOL
    gdi.CreateCompatibleDC.argtypes = [w.HDC]
    gdi.CreateCompatibleDC.restype = w.HDC
    gdi.CreateCompatibleBitmap.argtypes = [w.HDC, c.c_int, c.c_int]
    gdi.CreateCompatibleBitmap.restype = w.HBITMAP
    gdi.SelectObject.argtypes = [w.HDC, w.HANDLE]
    gdi.SelectObject.restype = w.HANDLE
    gdi.GetDIBits.argtypes = [w.HDC, w.HBITMAP, w.UINT, w.UINT, c.c_void_p, c.c_void_p, w.UINT]
    gdi.DeleteObject.argtypes = [w.HANDLE]
    gdi.DeleteDC.argtypes = [w.HDC]
    hdc = user.GetWindowDC(target)
    mem = gdi.CreateCompatibleDC(hdc)
    bitmap = gdi.CreateCompatibleBitmap(hdc, width, height)
    if not hdc or not mem or not bitmap:
        raise OSError(c.get_last_error(), "cannot create capture bitmap")
    old = gdi.SelectObject(mem, bitmap)
    try:
        if not user.PrintWindow(target, mem, 2):
            raise OSError(c.get_last_error(), "PrintWindow failed")
        class Header(c.Structure):
            _fields_ = [("size", w.DWORD), ("width", c.c_long), ("height", c.c_long),
                        ("planes", w.WORD), ("bits", w.WORD), ("compression", w.DWORD),
                        ("image_size", w.DWORD), ("xppm", c.c_long), ("yppm", c.c_long),
                        ("used", w.DWORD), ("important", w.DWORD)]
        hdr = Header(c.sizeof(Header), width, -height, 1, 32, 0, 0, 0, 0, 0, 0)
        buf = c.create_string_buffer(width * height * 4)
        if gdi.GetDIBits(mem, bitmap, 0, height, buf, c.byref(hdr), 0) != height:
            raise OSError(c.get_last_error(), "GetDIBits failed")
        # Console output is bottom-aligned; persist only the lower-left display crop.
        cw, ch = min(width, 700), min(height, 320)
        raw = buf.raw
        top = height - ch
        rows = [raw[y * width * 4:y * width * 4 + cw * 4] for y in range(height - 1, top - 1, -1)]
        bits = b"".join(rows)
        header = struct.pack("<2sIHHI", b"BM", 54 + len(bits), 0, 0, 54)
        dib = struct.pack("<IiiHHIIiiII", 40, cw, ch, 1, 32, 0, len(bits), 0, 0, 0, 0)
        Path(output).write_bytes(header + dib + bits)
        print("crop_written", cw, ch)
    finally:
        gdi.SelectObject(mem, old)
        gdi.DeleteObject(bitmap)
        gdi.DeleteDC(mem)
        user.ReleaseDC(target, hdc)


if __name__ == "__main__":
    main()
