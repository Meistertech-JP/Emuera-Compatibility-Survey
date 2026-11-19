#!/usr/bin/env python3
"""Pinned B045 missing-CSV-template rerun. dry-run never starts an engine."""
from __future__ import annotations
import argparse, ctypes as c, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, time, uuid
from ctypes import wintypes as w
HERE=pathlib.Path(__file__).resolve().parent
DEFAULT_REPO_ROOT=HERE.parent
EVIDENCE_REL=pathlib.Path('evidence/csv-numeric-45-20261117')
CASE_ID='CSVNUM_RECORDED_CSVBASE_CMD_MISSING99_20261116'
CONDITION_ID='CSVBASE_CMD_MISSING99'
MANIFEST_SHA='de28a35ef39cb1f7950f5ad4808a642dfa8b1d442392ea7174b97949a22bb1d5'
BINDINGS_SHA='3f3405f9c29e8bad802f5d8f91c7dbb0461573f40353f4bd7d09ec7e8075d45f'
INDEX_SHA='c698b3caff1eb5a42190058b6bf4a95d716c8115639825919b2987d448fe48de'
NATIVE_SHA='14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964'
PYZ_SHA='8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35'
HARNESS_PINS={
 'harness.py':'f3bdff99ea6c496f9ef95a8f239e03c9ec013ffdf1ebf859415d9d664b6046a3',
 'native.py':'d632b8bf5bf2c8265dc09f5a827bdd6f49bcea96435e71d09e30bc6831382d77',
 'validator.py':'89e78bc6d1164afefd86e85a9c3ef793d2db6d25e51af6ecde71bccba4224de6',
 'core.py':'61672b122e332fbf27c4186aebabd461a2b72581637234a2e1e6f130cff77c62',
 'audit.py':'781a506da2e2f3a9b306ea1c293b6ff0cf5d374d26baafaf0fe7e6dca9e1ce0c',
 'capture_crop.py':'6ddc776c6f76d9de9332893afc0cff84955ff8603dbdb89919e7f5bac1803772',
}
INPUTS={
 'ERB/MAIN.ERB':'905672872831ba5f2cfb191e018e1bb0254f7b772e6fcf5e208a0dd2750c3235',
 'csv/CHARA10.CSV':'c4699a6a0e30cd621cf9b0adcb0ff3fb3a312b35fddd90611d9ed418a4093d5f',
 'emuera.config':'b2a753dee3820126d56cd380e5b696e145811f721dc80e9147b3a8670cfdd4f4',
}
MODES=('native-01','native-02','public-01')
EXPECTED_MARKERS=(
 'SETUP_EXPECT_NO10_AND_NUMERIC_INDICES_ONLY',
 'BEFORE_CSVBASE_CMD_MISSING99_0',
 'HELPER_1 COUNT=1 ORDER=1',
 'HELPER_2 COUNT=2 ORDER=12',
 'HELPER_3 COUNT=3 ORDER=123',
)
FORBIDDEN_MARKERS=('AFTER_CSVBASE_CMD_MISSING99_0','DONE_CSVBASE_CMD_MISSING99')

def need(ok,message):
    if not ok: raise ValueError(message)
def sha_bytes(data): return hashlib.sha256(data).hexdigest()
def sha_file(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def jsonl(path):return [json.loads(line) for line in pathlib.Path(path).read_text(encoding='utf-8').splitlines() if line]
def under(child,parent):
    try:pathlib.Path(child).resolve().relative_to(pathlib.Path(parent).resolve());return True
    except ValueError:return False

def evidence_root(candidate_root):return pathlib.Path(candidate_root).resolve()/EVIDENCE_REL

def input_inventory(root):
    root=pathlib.Path(root)
    expected=set(INPUTS)
    actual=set()
    for top in ('ERB','csv'):
        folder=root/top
        need(folder.is_dir() and not folder.is_symlink(),'missing/linked input directory: '+str(folder))
        for p in folder.rglob('*'):
            need(not p.is_symlink(),'symlink in fixture inputs: '+str(p))
            if p.is_file():actual.add(p.relative_to(root).as_posix())
    config=root/'emuera.config'
    need(config.is_file() and not config.is_symlink(),'missing/linked config')
    actual.add('emuera.config')
    need(actual==expected,'unexpected or missing fixture paths: '+repr(sorted(actual^expected)))
    values={name:sha_file(root/name) for name in sorted(expected)}
    need(values==INPUTS,'fixture/config SHA mismatch: '+json.dumps(values,sort_keys=True))
    return values

def check_engine_code(candidate_root):
    h=pathlib.Path(candidate_root)/'harness'
    need(h.is_dir(),'candidate harness directory missing')
    for name,pin in HARNESS_PINS.items():
        path=h/name
        need(path.is_file() and not path.is_symlink() and sha_file(path)==pin,'harness dependency pin mismatch: '+name)
    return h

def verify_bundle(candidate_root):
    root=evidence_root(candidate_root)
    need(root.is_dir(),'CSV evidence package missing: '+str(root))
    for rel,pin in (('manifest.json',MANIFEST_SHA),('expected-bindings.json',BINDINGS_SHA),('index.json',INDEX_SHA)):
        path=root/rel
        need(path.is_file() and not path.is_symlink() and sha_file(path)==pin,'external package pin mismatch: '+rel)
    cmd=[sys.executable,'-B',str(root/'verify.py'),'--manifest-sha256',MANIFEST_SHA,'--bindings-sha256',BINDINGS_SHA]
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    checked=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',timeout=120,env=env)
    need(checked.returncode==0,'published CSV offline verifier failed: '+checked.stderr[-3000:])
    doc=json.loads((root/'index.json').read_text(encoding='utf-8'))
    case=next((x for x in doc['cases'] if x.get('case_id')==CASE_ID),None)
    need(case is not None,'pinned B045 case missing')
    need(case['source_condition_id']==CONDITION_ID and case['batch_id']=='B045','B045 identity mismatch')
    need(case['case_registry_verdict']=='different_scoped','registered verdict changed')
    need(case['parent_and_case_roles']==[{'kind':'method_as_command','name':'CSVBASE'}],'typed case role mismatch')
    cond=case['condition']
    need(cond['fixture_id']==CONDITION_ID and cond['fatal'] is True and cond['sp_enabled'] is False,'condition scope mismatch')
    need(len(cond['targets'])==1 and cond['targets'][0]['kind']=='method_as_command' and cond['targets'][0]['name']=='CSVBASE' and cond['targets'][0]['arguments']==[99,0,0] and cond['targets'][0]['target_line']==8,'target condition mismatch')
    readback=case['saved_semantic_readback']
    need(readback['actual_stop_line']==8 and readback['postfatal_state_inferred'] is False,'saved stop/postfatal scope mismatch')
    need(readback['classification']=='unaffected_selected_error_observation','saved readback classification changed')
    need(readback['helpers']==['HELPER_1 COUNT=1 ORDER=1','HELPER_2 COUNT=2 ORDER=12','HELPER_3 COUNT=3 ORDER=123'],'saved helper sequence mismatch')
    need(cond['targets'][0]['expected_source_selected']=='missing template after helpers123 before index' and cond['targets'][0]['expected_helpers']==3 and cond['targets'][0]['expected_order']=='123','selected expected target semantics changed')
    need(len(readback['selected_marker_comparisons'])==2,'selected marker comparison count mismatch')
    for comparison in readback['selected_marker_comparisons']:
        need(comparison['native_markers']==list(EXPECTED_MARKERS)==comparison['public_markers'],'saved marker sequence differs from fixed runner contract')
    result={}
    batch=next((x for x in doc['batches'] if x.get('batch_id')=='B045'),None)
    need(batch is not None and batch['fixture_id']==CONDITION_ID and batch['case_ids']==[CASE_ID],'B045 batch linkage mismatch')
    need([x['mode'] for x in batch['modes']]==list(MODES),'B045 mode set mismatch')
    expected_saved_outcomes={}
    for mode in MODES:
        path=root/'assets/B045'/mode/'inputs'
        actual=input_inventory(path)
        receipt=json.loads((root/'assets/B045'/mode/'receipt.json').read_text(encoding='utf-8'))
        need(receipt['source_condition_id']==CONDITION_ID and receipt['mode']==mode,'mode receipt identity mismatch: '+mode)
        need(receipt['fixture_inputs_before']==INPUTS==receipt['fixture_inputs_after'],'mode receipt input mismatch: '+mode)
        need(receipt['case_fatal_isolated_process'] is True and receipt['sp_enabled_gate'] is False,'mode receipt condition mismatch: '+mode)
        batch_mode=next(x for x in batch['modes'] if x['mode']==mode)
        need(batch_mode['fixture_id']==CONDITION_ID and batch_mode['raw']['sha256']==receipt['selected_raw']['sha256'],'batch mode/raw receipt mismatch: '+mode)
        expected_saved_outcomes[mode]={'returncode':receipt['recorded_returncode'],'native_probe':receipt['native_probe_selected'],'natural_exit':receipt['native_natural_exit']}
        result[mode]={'inputs':actual,'saved_raw_sha256':receipt['selected_raw']['sha256'],'saved_returncode':receipt['recorded_returncode'],'saved_native_natural_exit':receipt['native_natural_exit']}
    need(expected_saved_outcomes['native-01']['native_probe']['process_exited_after_5s'] is False and expected_saved_outcomes['native-02']['native_probe']['process_exited_after_5s'] is False,'saved Native timing basis changed')
    need(expected_saved_outcomes['public-01']['returncode']==1,'saved Public returncode basis changed')
    return {'root':str(root),'manifest_sha256':MANIFEST_SHA,'bindings_sha256':BINDINGS_SHA,'index_sha256':INDEX_SHA,'bundle_verifier_stdout':checked.stdout.strip(),'case_id':CASE_ID,'source_condition_id':CONDITION_ID,'batch_id':'B045','registered_case_verdict':'different_scoped','typed_target':{'kind':'method_as_command','name':'CSVBASE'},'arguments':[99,0,0],'target_line':8,'expected_markers':list(EXPECTED_MARKERS),'expected_absent_markers':list(FORBIDDEN_MARKERS),'diagnostic_baseline_available':False,'postfatal_state':'UNOBSERVED','modes':result}

def validate_binary(path,expected,label,native=False):
    p=pathlib.Path(path).resolve(strict=True)
    need(p.is_file() and not p.is_symlink(),label+' is not a regular file')
    if native:need(p.name=='Emuera1824+v24.exe','Native binary must be named Emuera1824+v24.exe')
    need(sha_file(p)==expected,label+' SHA mismatch')
    return p

def output_location(out_root,candidate_root):
    out=pathlib.Path(out_root).expanduser().absolute().resolve()
    need(not under(out,candidate_root),'output root must not be inside candidate')
    return out

def dry_run(candidate_root,out_root,native_path=None,pyz_path=None):
    info=verify_bundle(candidate_root);harness_dir=check_engine_code(candidate_root)
    bins={'native':'not_checked','pyz':'not_checked'}
    if native_path is not None:bins['native']={'path':str(validate_binary(native_path,NATIVE_SHA,'Native',True)),'sha256':NATIVE_SHA}
    if pyz_path is not None:bins['pyz']={'path':str(validate_binary(pyz_path,PYZ_SHA,'PyZ')),'sha256':PYZ_SHA}
    out=output_location(out_root,candidate_root)
    plan={'schema':'csv-b045-rerun-dry-run.v1','engine_started':False,'repo_root':str(pathlib.Path(candidate_root).resolve()),'evidence_root':info.pop('root'),'harness_root':str(harness_dir.resolve()),'out_root':str(out),'binaries':bins,'case':info}
    return plan

def import_harness(candidate_root):
    h=check_engine_code(candidate_root)
    sys.path.insert(0,str(h))
    import harness, native, core, validator
    return harness,native,core,validator

def decode_markers(raw,side,core):
    try:text,encoding=core.decode_log(raw,side)
    except Exception as exc:return {'status':'NOT_OBSERVED','decode_error':str(exc),'expected':{m:0 for m in EXPECTED_MARKERS},'forbidden':{m:None for m in FORBIDDEN_MARKERS},'ordered':False}
    lines=text.replace('\r\n','\n').split('\n')
    counts={m:sum(line==m for line in lines) for m in EXPECTED_MARKERS}
    forbidden={m:sum(m in line for line in lines) for m in FORBIDDEN_MARKERS}
    positions=[lines.index(m) for m in EXPECTED_MARKERS if counts[m]==1]
    ordered=all(counts[m]==1 for m in EXPECTED_MARKERS) and positions==sorted(positions)
    observed=ordered and all(value==0 for value in forbidden.values())
    return {'status':'OBSERVED' if observed else 'NOT_OBSERVED','encoding':encoding,'expected_counts':counts,'forbidden_counts':forbidden,'ordered':ordered,'selected_postfatal_state':'UNOBSERVED'}

def capture_native_window(desk,desktop_name,pid,process_handle,output,helper):
    """Read-only capture of one visible surface owned by native.run's process."""
    started_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    started=time.monotonic()
    def finish(data):
        data.setdefault('capture_started_utc',started_at)
        data['capture_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        data['capture_elapsed_seconds']=round(time.monotonic()-started,3)
        data['input_sent']=False
        return data
    try:
        user=c.WinDLL('user32',use_last_error=True)
        kernel=c.WinDLL('kernel32',use_last_error=True)
        callback=c.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)
        user.EnumDesktopWindows.argtypes=[w.HANDLE,callback,w.LPARAM]
        user.EnumChildWindows.argtypes=[w.HWND,callback,w.LPARAM]
        user.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)]
        user.GetClassNameW.argtypes=[w.HWND,w.LPWSTR,c.c_int]
        kernel.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD]
        time.sleep(6)
        if kernel.WaitForSingleObject(process_handle,0)!=0x102:
            return finish({'status':'not_observed','reason':'owned_process_exited_before_capture','owned_pid':pid})
        parents=[]
        @callback
        def visit(hwnd,_):
            owner=w.DWORD();user.GetWindowThreadProcessId(hwnd,c.byref(owner))
            if owner.value==pid:parents.append(int(hwnd))
            return True
        if not user.EnumDesktopWindows(desk,visit,0):
            raise OSError(c.get_last_error(),'EnumDesktopWindows failed or access denied')
        rich=[]
        for parent in parents:
            @callback
            def child(hwnd,_):
                owner=w.DWORD();user.GetWindowThreadProcessId(hwnd,c.byref(owner))
                cls=c.create_unicode_buffer(256);user.GetClassNameW(hwnd,cls,len(cls))
                if owner.value==pid and 'RICHEDIT' in cls.value.upper():rich.append(parent)
                return True
            user.EnumChildWindows(parent,child,0)
        if len(rich)!=1:
            return finish({'status':'not_observed','reason':'owned_rich_edit_count_not_one','count':len(rich),'owned_pid':pid})
        parent=rich[0]
        crop=pathlib.Path(output)/'native-display-crop.bmp'
        cmd=[sys.executable,'-B','-I',str(helper),desktop_name,str(parent),str(pid),str(crop)]
        env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
        try:
            result=subprocess.run(cmd,capture_output=True,timeout=15,env=env)
        except subprocess.TimeoutExpired as exc:
            return finish({'status':'not_observed','reason':'capture_helper_timeout','owned_pid':pid,'stderr':(exc.stderr or b'').decode('utf-8','replace')[-1000:]})
        if result.returncode!=0 or not crop.is_file():
            return finish({'status':'not_observed','reason':'capture_helper_failed_or_permission_denied','owned_pid':pid,'capture_returncode':result.returncode,'stdout':result.stdout.decode('utf-8','replace')[-1000:],'stderr':result.stderr.decode('utf-8','replace')[-1000:]})
        data=crop.read_bytes()
        return finish({'status':'captured','review_status':'VISUAL_REVIEW_REQUIRED','owned_pid':pid,'owned_window_handle':parent,'crop_path':crop.name,'crop_bytes':len(data),'crop_sha256':sha_bytes(data),'capture_returncode':result.returncode,'capture_stdout':result.stdout.decode('utf-8','replace')[-1000:]})
    except Exception as exc:
        return finish({'status':'not_observed','reason':'capture_exception_or_permission_denied','error':repr(exc),'owned_pid':pid})

def copy_pinned_inputs(evidence,mode,work):
    source=evidence/'assets'/'B045'/mode/'inputs'
    values=input_inventory(source)
    shutil.copytree(source,work)
    after=input_inventory(work)
    need(after==values==INPUTS,'copied workdir input mismatch: '+mode)
    return values

def run_attempt(candidate_root,native_path,pyz_path,lock_dir,out_root,timeout):
    import harness,native,core,validator
    candidate=pathlib.Path(candidate_root).resolve()
    evidence=pathlib.Path(verify_bundle(candidate)['root'])
    native_src=validate_binary(native_path,NATIVE_SHA,'Native',True)
    pyz_src=validate_binary(pyz_path,PYZ_SHA,'PyZ')
    lock=pathlib.Path(lock_dir).expanduser().resolve(strict=True)
    need(lock.is_dir(),'lock-dir must be an existing directory')
    need(not under(lock,candidate),'lock-dir must be outside repository root')
    out=output_location(out_root,candidate);out.mkdir(parents=True,exist_ok=True)
    attempt=out/('B045-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:10])
    attempt.mkdir(parents=False,exist_ok=False)
    report={'attempt_directory':str(attempt),'schema':'csv-b045-rerun-attempt.v1','case_id':CASE_ID,'source_condition_id':CONDITION_ID,'batch_id':'B045','registered_verdict':'different_scoped','typed_target':{'kind':'method_as_command','name':'CSVBASE'},'arguments':[99,0,0],'target_line':8,'sp_enabled_gate':False,'fatal':True,'postfatal_state':'UNOBSERVED','expected_markers':list(EXPECTED_MARKERS),'expected_absent_markers':list(FORBIDDEN_MARKERS),'diagnostic_baseline_available':False,'expected_public_returncode_from_saved_receipt':1,'expected_native_saved_probe':'separate historical probe: still running at 5s, cleanup terminated; natural exit unobserved','repo_root':str(candidate),'evidence_manifest_sha256':MANIFEST_SHA,'expected_bindings_sha256':BINDINGS_SHA,'index_sha256':INDEX_SHA,'native_sha256':NATIVE_SHA,'pyz_sha256':PYZ_SHA,'harness_code_sha256':HARNESS_PINS,'python_version':sys.version,'python_executable_sha256':sha_file(sys.executable),'platform':sys.platform,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'diagnostic_status':'UNVERIFIED_NO_PINNED_EXPECTED_DIAGNOSTIC','status':'NOT_OBSERVED','modes':[],'failure_reasons':[]}
    mode_records=[];residual_abort=False;abort_remaining=False;lock_context_clean_exit=False;lock_integrity_state={'failed':False}
    try:
        with harness.shared_lock(lock) as nonce:
            report['lock_nonce_sha256']=sha_bytes(nonce.encode('ascii'))
            report['lock_checks']={}
            def record_lock_check(label,target=None):
                try:
                    harness.check_lock(lock,nonce)
                except Exception as exc:
                    lock_integrity_state['failed']=True
                    entry={'status':'FAIL','error':repr(exc)}
                    (target.setdefault('lock_checks',{}) if target is not None else report['lock_checks'])[label]=entry
                    raise
                entry={'status':'PASS'}
                (target.setdefault('lock_checks',{}) if target is not None else report['lock_checks'])[label]=entry
            record_lock_check('after_acquire')
            initial=harness.native_processes();report['native_processes_before']=initial
            if initial:raise RuntimeError('Native process already exists; no mode started')
            for mode in MODES:
                rec={'mode':mode,'status':'NOT_OBSERVED','mode_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_hashes_before':{},'input_hashes_after':{},'native_processes_before':None,'native_processes_after':None,'engine_output_files':[],'diagnostic_status':'UNVERIFIED_NO_PINNED_EXPECTED_DIAGNOSTIC'}
                work=attempt/mode
                try:
                    record_lock_check('before_mode',rec)
                    inputs=copy_pinned_inputs(evidence,mode,work);rec['input_hashes_before']=inputs
                    if mode.startswith('native'):
                        local_exe=work/'Emuera1824+v24.exe';shutil.copyfile(native_src,local_exe)
                        rec['native_exe_sha256_before']=sha_file(local_exe)
                        rec['native_processes_before']=harness.native_processes()
                        if rec['native_processes_before']:raise RuntimeError('Native already running before '+mode)
                        record_lock_check('before_launch',rec)
                        call_started=datetime.datetime.now(datetime.timezone.utc).isoformat();call_clock=time.monotonic()
                        try:
                            rec['native_receipt']=native.run(local_exe,work,observe=lambda desk,name,pid,handle:capture_native_window(desk,name,pid,handle,work,candidate/'harness'/'capture_crop.py'))
                        except Exception as exc:
                            rec['native_error']=repr(exc)
                        finally:
                            rec['native_call_started_utc']=call_started
                            rec['native_call_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
                            rec['native_call_elapsed_seconds']=round(time.monotonic()-call_clock,3)
                        rec['native_exe_sha256_after']=sha_file(local_exe) if local_exe.is_file() else None
                        rec['native_processes_after']=harness.wait_for_native_absence()
                        record_lock_check('after_process',rec)
                        log=work/'emuera.log';observation=rec.get('native_receipt',{}).get('observation',{})
                        crop_available=observation.get('status')=='captured' and (work/observation.get('crop_path','')).is_file()
                        if crop_available:
                            crop_path=observation['crop_path'];rec['engine_output_files'].append({'path':crop_path,'bytes':observation['crop_bytes'],'sha256':observation['crop_sha256'],'capture':'owned-window crop; no automatic text/OCR decision'})
                        if log.is_file():
                            raw=log.read_bytes();rec['engine_output_files'].append({'path':'emuera.log','bytes':len(raw),'sha256':sha_bytes(raw),'capture':'Native application log; native.py does not pipe console stdout/stderr'})
                            rec['marker_observation']=decode_markers(raw,'native',core)
                        elif crop_available:
                            rec['marker_observation']={'status':'VISUAL_REVIEW_REQUIRED','reason':'Native diagnostic and markers require visual inspection; no pinned expected diagnostic is available','crop_path':crop_path,'selected_postfatal_state':'UNOBSERVED'}
                        else:
                            rec['marker_observation']={'status':'NOT_OBSERVED','reason':observation.get('reason','Native log and owned-window crop unavailable'),'capture_observation':observation,'expected_counts':{m:0 for m in EXPECTED_MARKERS}}
                        rec['native_forced_termination']=bool(rec.get('native_receipt',{}).get('outcome')=='forced_termination')
                        rec['native_exit_code']=rec.get('native_receipt',{}).get('exit_code')
                        if rec['native_processes_after']:residual_abort=True
                    else:
                        local_pyz=work/'PyEmuera.pyz';shutil.copyfile(pyz_src,local_pyz)
                        rec['pyz_sha256_before']=sha_file(local_pyz)
                        rec['native_processes_before']=harness.native_processes()
                        if rec['native_processes_before']:raise RuntimeError('Native residual before Public mode')
                        record_lock_check('before_launch',rec)
                        try:
                            proc=subprocess.run([sys.executable,'-B','-I',str(local_pyz),'--debug','.'],cwd=work,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                            rec['py_returncode']=proc.returncode;rec['py_termination']='process_returned';stdout=proc.stdout;stderr=proc.stderr
                        except subprocess.TimeoutExpired as exc:
                            rec['py_returncode']=None;rec['py_termination']='timeout_killed_by_subprocess_run';stdout=exc.stdout or b'';stderr=exc.stderr or b''
                        (work/'stdout.bin').write_bytes(stdout);(work/'stderr.bin').write_bytes(stderr)
                        rec['engine_output_files'] += [{'path':'stdout.bin','bytes':len(stdout),'sha256':sha_bytes(stdout),'capture':'subprocess stdout'}, {'path':'stderr.bin','bytes':len(stderr),'sha256':sha_bytes(stderr),'capture':'subprocess stderr'}]
                        rec['diagnostic_streams']={'stdout_sha256':sha_bytes(stdout),'stderr_sha256':sha_bytes(stderr),'interpretation':'UNVERIFIED_NO_PINNED_EXPECTED_DIAGNOSTIC'}
                        rec['marker_observation']=decode_markers(stdout,'py',core)
                        plog=work/'.pyemuera/logs/emuera.log'
                        if plog.is_file():
                            b=plog.read_bytes();rec['engine_output_files'].append({'path':'.pyemuera/logs/emuera.log','bytes':len(b),'sha256':sha_bytes(b),'capture':'PyEmuera OUTPUTLOG if emitted'})
                        rec['pyz_sha256_after']=sha_file(local_pyz) if local_pyz.is_file() else None
                        rec['native_processes_after']=harness.wait_for_native_absence()
                        record_lock_check('after_process',rec)
                        if rec['native_processes_after']:residual_abort=True
                    rec['input_hashes_after']=harness.input_inventory(work)
                    rec['inputs_unchanged']=rec['input_hashes_after']==inputs==INPUTS
                    rec['binary_unchanged']=(rec.get('native_exe_sha256_before')==rec.get('native_exe_sha256_after') if mode.startswith('native') else rec.get('pyz_sha256_before')==rec.get('pyz_sha256_after'))
                    markers=rec.get('marker_observation',{})
                    if mode.startswith('native'):
                        execution_shape_ok=rec.get('native_receipt',{}).get('outcome')=='forced_termination'
                    else:
                        execution_shape_ok=rec.get('py_termination')=='process_returned' and rec.get('py_returncode')==1
                    if not execution_shape_ok:
                        rec['status']='EXECUTION_FAILURE_OR_INCOMPLETE'
                    elif markers.get('status')=='OBSERVED' and rec['inputs_unchanged'] and rec['binary_unchanged']:
                        rec['status']='MARKERS_OBSERVED_DIAGNOSTIC_UNVERIFIED'
                    elif markers.get('status')=='VISUAL_REVIEW_REQUIRED' and rec['inputs_unchanged'] and rec['binary_unchanged']:
                        rec['status']='VISUAL_REVIEW_REQUIRED'
                    else:
                        rec['status']='NOT_OBSERVED'
                    # Validate ownership after every mode; errors abort remaining launches.
                    record_lock_check('after_mode',rec)
                except Exception as exc:
                    rec['error']=repr(exc);rec['status']='FAILED';report['failure_reasons'].append(mode+': '+repr(exc));abort_remaining=True
                rec['mode_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
                mode_records.append(rec);report['modes']=mode_records
                if residual_abort:
                    report['failure_reasons'].append('Native process residual; remaining modes were not launched');abort_remaining=True
                if abort_remaining:break
            report['native_processes_final']=harness.wait_for_native_absence()
            record_lock_check('after_final_process_check')
        lock_context_clean_exit=True
    except Exception as exc:
        report['runner_error']=repr(exc);report['failure_reasons'].append(repr(exc))
    report['lock_context_clean_exit']=lock_context_clean_exit
    report['lock_released_after_context']=not (lock/'NATIVE_LOCK.json').exists() and not (lock/'MEASURE_LOCK.json').exists()
    completed={r['mode'] for r in mode_records}
    for mode in MODES:
        if mode not in completed:report['modes'].append({'mode':mode,'status':'NOT_RUN','reason':'prior failure, lock/process issue, or runner error'})
    native_modes=[r for r in report['modes'] if r['mode'].startswith('native')]
    public=next((r for r in report['modes'] if r['mode']=='public-01'),{})
    marker_complete=(len(native_modes)==2 and all(r.get('marker_observation',{}).get('status') in ('OBSERVED','VISUAL_REVIEW_REQUIRED') for r in native_modes) and public.get('marker_observation',{}).get('status')=='OBSERVED')
    outcome_matches=(len(native_modes)==2 and all(r.get('native_receipt',{}).get('outcome')=='forced_termination' for r in native_modes) and public.get('py_returncode')==1 and public.get('py_termination')=='process_returned')
    inputs_ok=all(r.get('inputs_unchanged') is True and r.get('binary_unchanged') is True for r in report['modes'] if r.get('status') not in ('NOT_RUN','FAILED'))
    no_residual=report.get('native_processes_final')==[]
    integrity_ok=not lock_integrity_state['failed'] and report.get('runner_error') is None and report['lock_context_clean_exit'] is True and report['lock_released_after_context'] is True and all(v.get('status')=='PASS' for v in report.get('lock_checks',{}).values())
    execution_ok=not report['failure_reasons'] and all(r.get('status') not in ('FAILED','NOT_RUN') for r in report['modes'])
    any_visual=any(r.get('marker_observation',{}).get('status')=='VISUAL_REVIEW_REQUIRED' for r in native_modes)
    any_unobserved=not marker_complete
    if not integrity_ok:
        report['status']='INTEGRITY_FAILURE'
    elif not execution_ok or not outcome_matches or not inputs_ok or not no_residual:
        report['status']='EXECUTION_FAILURE_OR_INCOMPLETE'
    elif any_unobserved:
        report['status']='NOT_OBSERVED_OR_INCOMPLETE'
    elif any_visual:
        report['status']='VISUAL_REVIEW_REQUIRED'
    else:
        # No independently pinned expected diagnostic exists in the saved record set.
        report['status']='DIAGNOSTIC_UNVERIFIED'
    report['diagnostics_verified']=False
    report['status_note']='Markers and termination do not validate diagnostic identity. No expected Native/Py diagnostic contract is pinned by the saved B045 records; a scoped-difference conclusion is withheld.'
    report['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result_path=attempt/'RESULT.json';validator.write(result_path,report);validator.seal(attempt)
    checked=validator.validate(attempt);validator.write(attempt/'VALIDATION.json',checked);need(checked['valid'],'attempt evidence seal validation failed')
    report['seal_sha256']=sha_file(attempt/'SEAL.json')
    print(json.dumps({'status':report['status'],'attempt':str(attempt),'seal_sha256':report['seal_sha256'],'mode_statuses':{r['mode']:r['status'] for r in report['modes']},'diagnostics_verified':report['diagnostics_verified'],'failure_reasons':report['failure_reasons']},ensure_ascii=False,indent=2))
    return 0 if report['status']=='OBSERVED_SCOPED_DIFFERENCE' else 1

def main(argv=None):
    global harness,native,core,validator
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
    def common(p):
        p.add_argument('--repo-root',dest='candidate_root',type=pathlib.Path,default=DEFAULT_REPO_ROOT)
        p.add_argument('--out-root',type=pathlib.Path,required=True)
        p.add_argument('--native',type=pathlib.Path,required=True)
        p.add_argument('--pyz',type=pathlib.Path,required=True)
    dry=sub.add_parser('dry-run',help='verify pinned bundle/inputs and print plan; never launches engines');common(dry)
    run=sub.add_parser('run',help='run the single pinned B045 condition in three isolated workdirs');common(run)
    run.add_argument('--lock-dir',type=pathlib.Path,required=True)
    run.add_argument('--timeout-seconds',type=int,default=30)
    a=ap.parse_args(argv)
    try:
        plan=dry_run(a.candidate_root,a.out_root,a.native,a.pyz)
        if a.command=='dry-run':
            print(json.dumps(plan,ensure_ascii=False,indent=2));return 0
        need(a.native is not None and a.pyz is not None,'run requires --native and --pyz')
        need(1<=a.timeout_seconds<=180,'timeout-seconds must be 1..180')
        # Import pinned candidate process/lock helpers only after dry preflight.
        harness,native,core,validator=import_harness(a.candidate_root)
        return run_attempt(a.candidate_root,a.native,a.pyz,a.lock_dir,a.out_root,a.timeout_seconds)
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())

