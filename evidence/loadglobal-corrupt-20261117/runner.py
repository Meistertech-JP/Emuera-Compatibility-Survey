#!/usr/bin/env python3
"""Bounded LOADGLOBAL rerun; dry-run is read-only and starts no engine."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,re,shutil,stat,subprocess,sys,time

HERE=Path(__file__).resolve().parent
BUNDLE=HERE
NATIVE_SHA='14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964'
PYZ_SHA='8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35'
HARNESS_PINS={
 'harness.py':'f3bdff99ea6c496f9ef95a8f239e03c9ec013ffdf1ebf859415d9d664b6046a3',
 'native.py':'d632b8bf5bf2c8265dc09f5a827bdd6f49bcea96435e71d09e30bc6831382d77',
 'core.py':'61672b122e332fbf27c4186aebabd461a2b72581637234a2e1e6f130cff77c62',
 'validator.py':'89e78bc6d1164afefd86e85a9c3ef793d2db6d25e51af6ecde71bccba4224de6',
 'audit.py':'781a506da2e2f3a9b306ea1c293b6ff0cf5d374d26baafaf0fe7e6dca9e1ce0c',
}
INPUTS={
 'ERB/SEARCHBOUND01.ERB':'2b4bdfe59743906e2d8e65310663cb73c433dd3025f76262cea7f34b0ab17e02',
 'ERB/GLOBAL205.ERH':'822d11bc9a96a4fa705664ecfde784ecdc9c522b9b4258bfe163f1595869e5a3',
 'emuera.config':'f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc',
}
SAVE_PINS={'native':'0350f7dde4d161714a29785b825b9bc96937ec9baf0075b5a6b9c8df2ad82539','public':'991f88eb242fefbe97358d1bbf027332d437c9fe25de5f0593626c9fd00daca9'}
FIELDS=('RESULT','GLOBAL0','GLOBAL1','GLOBALS0','GLOBALS1','USER0','USER1','USER2','USERS0','USERS1')

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def check_harness(harness_dir):
    for name,pin in HARNESS_PINS.items():
        p=harness_dir/name;need(p.is_file() and not is_link(p) and sha(p)==pin,'harness pin mismatch: '+name)
def is_link(p):
    st=p.lstat()
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st,'st_file_attributes',0) & 0x400)
def existing_directory(path,label):
    p=Path(path).expanduser().absolute()
    need(p.is_dir(),label+' must be an existing directory')
    for part in (p,*p.parents):need(not is_link(part),label+' contains a link or junction')
    return p.resolve(strict=True)
def context(repository_root,harness_dir,out_root):
    repo=existing_directory(repository_root,'repository root')
    harness=existing_directory(harness_dir,'harness directory')
    out=existing_directory(out_root,'output root')
    need(harness==repo/'harness','harness directory must be repository-root/harness')
    need(HERE==repo/'evidence/loadglobal-corrupt-20261117','bundle must be installed in the specified repository')
    need(not out.is_relative_to(repo) and not repo.is_relative_to(out),'output root must be separate from repository')
    return repo,harness,out
def normalized_sha(value):
    need(re.fullmatch(r'[0-9a-fA-F]{64}',value) is not None,'manifest SHA must be hex')
    return value.lower()
def check_bundle(manifest_sha):
    manifest_sha=normalized_sha(manifest_sha)
    manifest=BUNDLE/'manifest.json';need(manifest.is_file() and not is_link(manifest) and sha(manifest)==manifest_sha,'bundle manifest pin mismatch')
    m=json.loads(manifest.read_text(encoding='utf8'));need(m['schema']=='loadglobal-case-bundle.v1','bundle manifest schema')
    recorded={r['path']:r for r in m['files']};need(len(recorded)==len(m['files']),'duplicate manifest path')
    actual={p.relative_to(BUNDLE).as_posix() for p in BUNDLE.rglob('*') if p.is_file() and p!=manifest}
    need(actual==set(recorded),'bundle file set changed')
    for rel,row in recorded.items():
        p=BUNDLE/rel;need(not p.is_symlink() and p.resolve().is_relative_to(BUNDLE.resolve()),'unsafe bundle path')
        need(p.stat().st_size==row['size'] and sha(p)==row['sha256'],'bundle file mismatch: '+rel)
    for rel,pin in INPUTS.items():need(sha(BUNDLE/'fixture'/rel)==pin,'fixture pin mismatch')
    for mode,pin in SAVE_PINS.items():need(sha(BUNDLE/'fixture'/mode/('global.sav' if mode=='native' else 'global.json'))==pin,'save pin mismatch')
    return len(recorded)
def check_engine(path,pin,label):
    p=Path(path).expanduser();need(not p.is_symlink(),'engine path is a symlink')
    p=p.resolve(strict=True);need(p.is_file() and sha(p)==pin,label+' SHA mismatch')
    if label=='native':need(p.name.lower()=='emuera1824+v24.exe','native executable name mismatch')
    return p
def load_harness(harness_dir):
    check_harness(harness_dir)
    names=('harness','native','core','validator','audit')
    loaded=[n for n in names if n in sys.modules]
    if loaded:
        need(len(loaded)==len(names),'partially loaded harness modules')
    else:
        sys.dont_write_bytecode=True;sys.path.insert(0,str(harness_dir))
        import harness,native
    for name in names:
        need(Path(sys.modules[name].__file__).resolve()==harness_dir/(name+'.py'),'imported module is outside pinned harness')
    check_harness(harness_dir)
    return sys.modules['harness'],sys.modules['native']
def make_inputs(root):
    root.mkdir(exist_ok=False)
    for mode in ('native','public'):
        dst=root/mode;(dst/'ERB').mkdir(parents=True);(dst/'csv').mkdir()
        for rel,pin in INPUTS.items():
            shutil.copyfile(BUNDLE/'fixture'/rel,dst/rel);need(sha(dst/rel)==pin,'prepared input mismatch')
    shutil.copyfile(BUNDLE/'fixture/native/global.sav',root/'native/global.sav')
    save=root/'public/.pyemuera/saves';save.mkdir(parents=True)
    shutil.copyfile(BUNDLE/'fixture/public/global.json',save/'global.json')
    for mode,path in (('native',root/'native/global.sav'),('public',save/'global.json')):need(sha(path)==SAVE_PINS[mode],'prepared save mismatch')
def snapshot_save(src,dst):
    if not src.is_file():return {'state':'NOT_PRESENT'}
    need(not src.is_symlink(),'save path is symlink');dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dst);return {'state':'PRESENT','path':dst.relative_to(dst.parents[2]).as_posix(),'sha256':sha(dst),'size':dst.stat().st_size}
def parse_log(path):
    if not path.is_file():return {'state':'NOT_OBSERVED','fields':{},'continued':None}
    try:lines=path.read_bytes().decode('utf-16').splitlines()
    except (UnicodeError,OSError):return {'state':'DECODE_ERROR','fields':{},'continued':None}
    data={}
    for line in lines:
        if line.startswith('CORRUPT_') and '=' in line:
            k,v=line.split('=',1)
            if k in data:return {'state':'DUPLICATE_FIELD','fields':data,'continued':None}
            data[k]=v
    expected={'CORRUPT_'+x for x in FIELDS}
    return {'state':'COMPLETE' if expected==set(data) and 'CORRUPT_LOAD_CONTINUED' in lines else 'INCOMPLETE','fields':data,'continued':'CORRUPT_LOAD_CONTINUED' in lines}
def public_run(pyz,folder):
    start=time.monotonic()
    try:
        p=subprocess.run([sys.executable,'-I','-B',str(pyz),'--debug','.'],cwd=folder,stdin=subprocess.DEVNULL,capture_output=True,timeout=30)
        stdout,stderr=p.stdout,p.stderr;status={'outcome':'exited','returncode':p.returncode}
    except subprocess.TimeoutExpired as e:
        stdout,stderr=e.stdout or b'',e.stderr or b'';status={'outcome':'timeout_owned_child_terminated','returncode':None}
    (folder/'captured.stdout.bin').write_bytes(stdout);(folder/'captured.stderr.bin').write_bytes(stderr)
    status['elapsed_seconds']=round(time.monotonic()-start,3)
    status['stderr_utf8_display']=stderr.decode('utf8',errors='replace')
    return status
def dry_run(repository_root,harness_dir,out_root,manifest_sha,native_path=None,pyz_path=None,lock_dir=None):
    manifest_sha=normalized_sha(manifest_sha)
    repo,harness_dir,out=context(repository_root,harness_dir,out_root)
    count=check_bundle(manifest_sha);check_harness(harness_dir)
    engines={'native':'NOT_CHECKED','pyz':'NOT_CHECKED'}
    if native_path:engines['native']={'sha256':sha(check_engine(native_path,NATIVE_SHA,'native'))}
    if pyz_path:engines['pyz']={'sha256':sha(check_engine(pyz_path,PYZ_SHA,'pyz'))}
    if lock_dir is not None:
        lock=existing_directory(lock_dir,'lock directory')
        need(not lock.is_relative_to(repo) and not repo.is_relative_to(lock),'lock directory must be separate from repository')
        lock_state={'directory_exists':True,'native_lock_present':os.path.lexists(lock/'NATIVE_LOCK.json'),'measurement_lock_present':os.path.lexists(lock/'MEASURE_LOCK.json')}
    else:lock_state={'state':'EXPLICIT_SHARED_LOCK_DIR_REQUIRED_FOR_RUN'}
    plan={'native':{'save_destination':'native/global.sav','save_sha256':SAVE_PINS['native']},'public':{'save_destination':'public/.pyemuera/saves/global.json','save_sha256':SAVE_PINS['public']}}
    return {'schema':'loadglobal-isolated-dry-run.v1','case_id':'LOADGLOBAL_CORRUPT_TRUNCATION_20261115','engine_started':False,'shared_lock_acquired':False,'files_written':False,'bundle_manifest_sha256':manifest_sha,'bundle_files_verified':count,'harness_pins':HARNESS_PINS,'engine_binaries':engines,'input_plan':plan,'lock':lock_state,'native_process_control':'repository harness/native.py: isolated desktop and owned process handle','run_requirements':'explicit shared lock, new attempt name, both pinned engine paths'}

def execute(repository_root,harness_dir,out_root,manifest_sha,native_path,pyz_path,lock_dir,attempt_name):
    need(sys.platform=='win32','run requires Windows')
    manifest_sha=normalized_sha(manifest_sha)
    need(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,60}',attempt_name) is not None,'unsafe attempt name')
    repo,harness_dir,out=context(repository_root,harness_dir,out_root)
    check_bundle(manifest_sha);check_harness(harness_dir);h,n=load_harness(harness_dir)
    exe=check_engine(native_path,NATIVE_SHA,'native');pyz=check_engine(pyz_path,PYZ_SHA,'pyz')
    lock=existing_directory(lock_dir,'lock directory')
    need(not lock.is_relative_to(repo) and not repo.is_relative_to(lock),'lock directory must be separate from repository')
    attempt=out/attempt_name;need(not os.path.lexists(attempt),'attempt already exists')
    result={'schema':'loadglobal-isolated-attempt.v1','status':'FAILURE','case_id':'LOADGLOBAL_CORRUPT_TRUNCATION_20261115','started_utc':datetime.now(timezone.utc).isoformat(),'repository_root':str(repo),'harness_directory':str(harness_dir),'output_root':str(out),'lock_directory':str(lock),'bundle_manifest_sha256':manifest_sha,'harness_pins':HARNESS_PINS,'native_sha256':NATIVE_SHA,'pyz_sha256':PYZ_SHA,'python_executable_sha256':sha(sys.executable),'lock_release':'UNCONFIRMED','native':{},'public':{},'limits':['GUI diagnostic unobserved','comparison only within specified own-format truncated files','recorded output is not a full compatibility verdict']}
    error=None
    try:
        with h.shared_lock(lock) as nonce:
            h.check_lock(lock,nonce)
            if h.native_processes():raise RuntimeError('Native process already running; refused')
            make_inputs(attempt)
            native_dir=attempt/'native';public_dir=attempt/'public'
            native_save=native_dir/'global.sav';py_save=public_dir/'.pyemuera/saves/global.json'
            result['native']['save_before']=snapshot_save(native_save,attempt/'snapshots/before/native-global.sav')
            result['public']['save_before']=snapshot_save(py_save,attempt/'snapshots/before/public-global.json')
            try:
                copied=native_dir/'Emuera1824+v24.exe';shutil.copyfile(exe,copied)
                need(sha(copied)==NATIVE_SHA and sha(exe)==NATIVE_SHA,'native exe changed')
                h.check_lock(lock,nonce)
                if h.native_processes():raise RuntimeError('Native process appeared; refused')
                native_error=None
                try:
                    result['native']['receipt']=n.run(copied,native_dir,timeout=5)
                except Exception as exc:
                    native_error=exc
                    result['native']['error_type']=type(exc).__name__
                    result['native']['error']=str(exc)
                remaining=h.wait_for_native_absence()
                result['native']['remaining_same_name_processes']=remaining
                if remaining:raise RuntimeError('Native process remains after owned-process cleanup')
                if native_error is not None:raise RuntimeError('Native execution failed after cleanup check') from native_error
                h.check_lock(lock,nonce)
                need(sha(copied)==NATIVE_SHA and sha(exe)==NATIVE_SHA,'native exe changed during run')
                result['native']['log']=parse_log(native_dir/'emuera.log')
                h.check_lock(lock,nonce)
                result['public']['receipt']=public_run(pyz,public_dir)
                h.check_lock(lock,nonce)
                need(sha(pyz)==PYZ_SHA,'PyEmuera artifact changed during run')
                result['public']['log']=parse_log(public_dir/'.pyemuera/logs/emuera.log')
                result['public']['diagnostic_e_save_in_stderr']=b'E_SAVE' in (public_dir/'captured.stderr.bin').read_bytes()
                h.check_lock(lock,nonce)
                a=result['native']['log'];b=result['public']['log']
                result['selected_comparison']={'state':'OBSERVED' if a['state']==b['state']=='COMPLETE' else 'INCOMPLETE','same_fields':a['fields']==b['fields'] if a['state']==b['state']=='COMPLETE' else None}
                pub=result['public']['receipt']; native_receipt=result['native']['receipt']
                if pub['outcome']=='timeout_owned_child_terminated':result['status']='PY_TIMEOUT'
                elif pub['returncode']!=0:result['status']='PY_NONZERO'
                elif native_receipt['outcome']=='natural_nonzero':result['status']='NATIVE_NONZERO'
                elif a['state']==b['state']=='COMPLETE':result['status']='CAPTURED'
                else:result['status']='INCOMPLETE'
            finally:
                result['native']['save_after']=snapshot_save(native_save,attempt/'snapshots/after/native-global.sav')
                result['public']['save_after']=snapshot_save(py_save,attempt/'snapshots/after/public-global.json')
                for mode in ('native','public'):
                    result[mode]['fixture_sha256_after']={rel:sha(attempt/mode/rel) if (attempt/mode/rel).is_file() else None for rel in INPUTS}
                    result[mode]['csv_empty_after']=(attempt/mode/'csv').is_dir() and not any((attempt/mode/'csv').iterdir())
                    if result[mode]['fixture_sha256_after']!=INPUTS or not result[mode]['csv_empty_after']:
                        result['status']='FAILURE';result['integrity_error']='fixture or CSV changed'
                result['native'].setdefault('log',parse_log(native_dir/'emuera.log'))
                result['public'].setdefault('log',parse_log(public_dir/'.pyemuera/logs/emuera.log'))
    except Exception as exc:
        error=exc;result['status']='FAILURE';result['error_type']=type(exc).__name__;result['error']=str(exc)
    else:result['lock_release']='CONFIRMED_BY_SHARED_LOCK'
    finally:
        if attempt.is_dir():
            result['harness_sha256_after']={k:sha(harness_dir/k) if (harness_dir/k).is_file() else None for k in HARNESS_PINS}
            if result['harness_sha256_after']!=HARNESS_PINS:
                result['status']='FAILURE';result['integrity_error']='harness changed'
            result['python_executable_sha256_after']=sha(sys.executable)
            if result['python_executable_sha256_after']!=result['python_executable_sha256']:
                result['status']='FAILURE';result['integrity_error']='Python executable changed'
            try:result['retained_file_inventory_before_result']=h.validator.inventory(attempt)
            except Exception as exc:
                result['status']='FAILURE';result['inventory_error']=str(exc)
            dump(attempt/'RESULT.json',result)
    if error is not None:raise RuntimeError('attempt failed; partial evidence retained when created') from error
    public_receipt=result['public'].get('receipt',{})
    if result['status']=='CAPTURED':exit_code=0
    elif result['status']=='PY_TIMEOUT':exit_code=124
    elif result['status']=='PY_NONZERO' and isinstance(public_receipt.get('returncode'),int) and 0<public_receipt['returncode']<256:exit_code=public_receipt['returncode']
    else:exit_code=1
    return {'attempt':str(attempt),'status':result['status'],'lock_release':result['lock_release'],'exit_code':exit_code}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group();group.add_argument('--dry-run',action='store_true');group.add_argument('--run',action='store_true')
    p.add_argument('--repository-root',required=True);p.add_argument('--harness-dir',required=True)
    p.add_argument('--out-root',required=True);p.add_argument('--manifest-sha256',required=True)
    p.add_argument('--native');p.add_argument('--pyz');p.add_argument('--lock-dir');p.add_argument('--attempt-name')
    a=p.parse_args()
    if a.run:
        if not all((a.native,a.pyz,a.lock_dir,a.attempt_name)):p.error('--run requires --native, --pyz, --lock-dir, and --attempt-name')
        out=execute(a.repository_root,a.harness_dir,a.out_root,a.manifest_sha256,a.native,a.pyz,a.lock_dir,a.attempt_name)
    else:out=dry_run(a.repository_root,a.harness_dir,a.out_root,a.manifest_sha256,a.native,a.pyz,a.lock_dir)
    print(json.dumps(out,ensure_ascii=True,indent=2))
    if a.run:raise SystemExit(out['exit_code'])
if __name__=='__main__':main()
