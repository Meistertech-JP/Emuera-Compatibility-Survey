from pathlib import Path
import ctypes as c,hashlib,json,subprocess,sys,time
from ctypes import wintypes as w
run=Path(sys.argv[1]).resolve();name='PyEmueraNative_STRLENSU_'+run.name+'_'+str(int(time.time()));u=c.WinDLL('user32',use_last_error=True);k=c.WinDLL('kernel32',use_last_error=True)
class SI(c.Structure):_fields_=[('cb',w.DWORD),('reserved',w.LPWSTR),('desktop',w.LPWSTR),('title',w.LPWSTR),('x',w.DWORD),('y',w.DWORD),('xsize',w.DWORD),('ysize',w.DWORD),('xcount',w.DWORD),('ycount',w.DWORD),('fill',w.DWORD),('flags',w.DWORD),('show',w.WORD),('reserved2count',w.WORD),('reserved2',c.c_void_p),('stdin',w.HANDLE),('stdout',w.HANDLE),('stderr',w.HANDLE)]
class PI(c.Structure):_fields_=[('process',w.HANDLE),('thread',w.HANDLE),('pid',w.DWORD),('tid',w.DWORD)]
u.CreateDesktopW.argtypes=[w.LPCWSTR,w.LPCWSTR,c.c_void_p,w.DWORD,w.DWORD,c.c_void_p];u.CreateDesktopW.restype=w.HANDLE;u.CloseDesktop.argtypes=[w.HANDLE]
k.CreateProcessW.argtypes=[w.LPCWSTR,w.LPWSTR,c.c_void_p,c.c_void_p,w.BOOL,w.DWORD,c.c_void_p,w.LPCWSTR,c.POINTER(SI),c.POINTER(PI)];k.CreateProcessW.restype=w.BOOL;k.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];k.GetExitCodeProcess.argtypes=[w.HANDLE,c.POINTER(w.DWORD)];k.TerminateProcess.argtypes=[w.HANDLE,w.UINT];k.TerminateProcess.restype=w.BOOL;k.CloseHandle.argtypes=[w.HANDLE]
exe=str(run/'Emuera1824+v24.exe');desk=u.CreateDesktopW(name,None,None,0,0x01FF,None);si=SI();si.cb=c.sizeof(SI);si.desktop='WinSta0\\'+name;pi=PI();cmd=c.create_unicode_buffer(subprocess.list2cmdline([exe]));created=bool(desk) and bool(k.CreateProcessW(exe,cmd,None,None,False,0,None,str(run),c.byref(si),c.byref(pi)))
r={'desktop':name,'desktop_created':bool(desk),'process_created':created,'pid':pi.pid if created else None,'command_line':subprocess.list2cmdline([exe]),'cwd':str(run),'synthetic_keyboard_events_sent':False,'fixture_sha256':hashlib.sha256((run/'ERB'/'SEARCHBOUND01.ERB').read_bytes()).hexdigest(),'native_exe_sha256':hashlib.sha256((run/'Emuera1824+v24.exe').read_bytes()).hexdigest(),'config_sha256':hashlib.sha256((run/'emuera.config').read_bytes()).hexdigest()}
if created:
 state=k.WaitForSingleObject(pi.process,5000);r['process_exited_after_5s']=state==0;code=w.DWORD();r['exit_code_observed']=bool(state==0 and k.GetExitCodeProcess(pi.process,c.byref(code)));r['exit_code']=code.value if r['exit_code_observed'] else None
 if state!=0:r['cleanup_terminate_ok']=bool(k.TerminateProcess(pi.process,1));k.WaitForSingleObject(pi.process,5000)
 k.CloseHandle(pi.thread);k.CloseHandle(pi.process)
r['files']=[{'path':str(p.relative_to(run)).replace('\\','/'),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(run.rglob('*')) if p.is_file()]
if desk:r['desktop_closed']=bool(u.CloseDesktop(desk))
(run/'probe.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,ensure_ascii=True))
