"""Check the selected CSV numeric bundle against separately obtained pins.
Adapted from the 61-case saved-evidence verifier and shared file-set tool.
"""
import argparse,hashlib,json,pathlib,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
def sha(x):return hashlib.sha256(x).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def check(x,msg):
 if not x:raise ValueError(msg)
def asset(ref):
 p=pathlib.PurePosixPath(ref['path']);check(not p.is_absolute() and '..' not in p.parts and '\\' not in ref['path'] and ':' not in ref['path'],'unsafe path')
 q=HERE.joinpath(*p.parts);check(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(HERE.resolve()),'missing asset')
 b=q.read_bytes();check(len(b)==ref['size'] and sha(b)==ref['sha256'],'asset bytes mismatch');return b
def verify(doc,contract):
 check(doc['schema']=='csv-numeric-saved-evidence-1','schema')
 cases=doc['cases'];batch={x['batch_id']:x for x in doc['batches']};expected={x['case_id']:x for x in contract['cases']}
 check(len(cases)==len(batch)==len(expected)==45 and len({x['case_id'] for x in cases})==45 and set(expected)=={x['case_id'] for x in cases},'case identity')
 roles=0;count=0;rawpaths=set()
 for case in cases:
  e=expected[case['case_id']];check(sha(enc(case))==e['case_projection_sha256'],'case content')
  check(case['batch_id']==e['batch_id'] and case['parent_and_case_roles']==e['roles'] and case['registered_roles']==e['registered_roles'] and case['case_registry_verdict']==e['case_registry_verdict'],'case role/verdict')
  b=batch[case['batch_id']];check(b['case_ids']==[case['case_id']] and b['fixture_id']==case['source_condition_id'],'batch identity')
  check([x['mode'] for x in b['modes']]==['native-01','native-02','public-01'],'mode set')
  for m in b['modes']:
   name=m['mode'];q=e['modes'][name]
   check(m['fixture_id']==b['fixture_id']==q['fixture_id'] and m['raw']==q['raw'] and m['receipt']==q['receipt'] and m['inputs']==q['inputs'],'mode assets binding')
   check(m['natural_exit']==q['natural_exit'] and m['stderr'] is None and m['raw_binding_basis']=='case_record_and_group_manifest_and_saved_raw_readback','limitations')
   rawpaths.add(m['raw']['path']);asset(m['raw']);after=json.loads(asset(m['receipt']))
   check(after['source_condition_id']==b['fixture_id'] and after['mode']==name and after['selected_raw']=={'sha256':m['raw']['sha256'],'binding_basis':'case_record_and_group_manifest_and_saved_raw_readback'},'receipt identity/raw basis')
   inputs={x['relative_name']:x['sha256'] for x in m['inputs']};check(len(inputs)==len(m['inputs']) and after['fixture_inputs_before']==inputs==after['fixture_inputs_after'],'input relation')
   for x in m['inputs']:asset(x)
   check(type(after['recorded_returncode']) is int and after['recorded_returncode']==q['recorded_returncode'] and after['native_probe_selected']==q['native_probe_selected'] and after['native_natural_exit']==q['natural_exit'],'receipt values')
   if name.startswith('native'):
    probe=after['native_probe_selected'];check(isinstance(probe,dict) and probe['process_exited_after_5s'] is False and probe['exit_code_observed'] is False and probe['exit_code'] is None and probe['cleanup_terminate_ok'] is True and after['native_natural_exit']=='not_observed','native exit observation')
   else:check(after['native_probe_selected'] is None and after['native_natural_exit']=='not_applicable','public native field')
   count+=1
  roles+=len(case['parent_and_case_roles'])
 check(count==135 and len(rawpaths)==135 and roles==56,'counts')
 return {'result':'PASS_LIMITED','cases':45,'modes':count,'role_pairs':roles,'raw_paths':len(rawpaths),'native_natural_exit':'not_observed in 90 saved modes','limits':'No engine replay, independent origin authentication, privacy or rights approval.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--bindings-sha256',required=True);args=ap.parse_args()
 check(sha((HERE/'manifest.json').read_bytes())==args.manifest_sha256,'manifest pin');raw=(HERE/'expected-bindings.json').read_bytes();check(sha(raw)==args.bindings_sha256,'bindings pin')
 subprocess.run([sys.executable,'-B',str(HERE/'tools/file_set_manifest.py'),'verify','--root','evidence='+str(HERE),'--manifest',str(HERE/'manifest.json')],check=True)
 print(json.dumps(verify(json.loads((HERE/'index.json').read_bytes()),json.loads(raw)),ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError,subprocess.CalledProcessError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
