import ctypes as c, sys
from ctypes import wintypes as w
from pathlib import Path
from PIL import Image
u=c.windll.user32; g=c.windll.gdi32
u.OpenDesktopW.argtypes=[w.LPCWSTR,w.DWORD,w.BOOL,w.DWORD];u.OpenDesktopW.restype=w.HANDLE
u.SetThreadDesktop.argtypes=[w.HANDLE]
if len(sys.argv)!=5: raise SystemExit('usage: case hwnd desktop output.png')
case,hs,desktop,out=sys.argv[1:]
desk=u.OpenDesktopW(desktop,0,False,0x01FF)
if not desk or not u.SetThreadDesktop(desk): raise SystemExit('cannot attach isolated desktop')
hwnd=int(hs)
class RECT(c.Structure): _fields_=[('left',w.LONG),('top',w.LONG),('right',w.LONG),('bottom',w.LONG)]
r=RECT()
if not u.GetWindowRect(hwnd,c.byref(r)): raise SystemExit('GetWindowRect failed')
width,height=r.right-r.left,r.bottom-r.top
if width<120 or height<100: raise SystemExit(f'window too small: {width}x{height}')
hdc=u.GetWindowDC(hwnd); mem=g.CreateCompatibleDC(hdc); bmp=g.CreateCompatibleBitmap(hdc,width,height); old=g.SelectObject(mem,bmp)
printed=u.PrintWindow(hwnd,mem,2)
class BIH(c.Structure): _fields_=[('size',w.DWORD),('width',w.LONG),('height',w.LONG),('planes',w.WORD),('bits',w.WORD),('compression',w.DWORD),('image_size',w.DWORD),('xppm',w.LONG),('yppm',w.LONG),('used',w.DWORD),('important',w.DWORD)]
info=BIH();info.size=c.sizeof(BIH);info.width=width;info.height=-height;info.planes=1;info.bits=32
raw=c.create_string_buffer(width*height*4)
lines=g.GetDIBits(mem,bmp,0,height,raw,c.byref(info),0)
if not lines: raise SystemExit('GetDIBits failed')
# Keep only the client/display area: title and outer frame are excluded. Full pixels stay in memory only.
image=Image.frombytes('RGBA',(width,height),raw.raw,'raw','BGRA')
client=image.crop((6,26,width-6,height-6))
# The single candidate is rendered near the lower-left of the Emuera text area. Retain only that line.
crop=client.crop((0,380,min(width-12,420),510)).convert('RGB')
Path(out).parent.mkdir(parents=True,exist_ok=True);crop.save(out,optimize=True)
print({'case':case,'print_window':bool(printed),'window':(width,height),'retained_crop':crop.size,'output':out})
g.SelectObject(mem,old);g.DeleteObject(bmp);g.DeleteDC(mem);u.ReleaseDC(hwnd,hdc);u.CloseDesktop(desk)
