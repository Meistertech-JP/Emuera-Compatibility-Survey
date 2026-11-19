"""Fail-closed integrity and raw-observation tests in disposable private copies."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent
q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);a=q.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def encode(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def reseal(d,rel,edit,replace_source=False):
 path=d/rel;edit(path);b=path.read_bytes();mp=d/'manifest.json';m=json.loads(mp.read_text(encoding='utf-8'))
 artifact=next(x for x in m['artifacts'] if x['path']==rel);artifact['sha256']=sha(b);artifact['size']=len(b)
 if replace_source:
  sid=artifact['derived_from'][0]['source_id'];m['sources'][sid]['sha256']=sha(b);m['sources'][sid]['size']=len(b)
  for x in m['artifacts']:
   for ref in x['derived_from']:
    if ref['source_id']==sid:ref['source_sha256']=sha(b)
 mb=encode(m);mp.write_bytes(mb);pin=sha(mb);(d/'manifest.sha256').write_bytes((pin+'\n').encode('ascii'));return pin
def edit_json(path,fn):
 x=json.loads(path.read_text(encoding='utf-8'));fn(x);path.write_bytes(encode(x))
def edit_raw(path,old,new):
 s=path.read_bytes().decode('utf-16');assert old in s;path.write_bytes(s.replace(old,new,1).encode('utf-16'))
cases=[('raw_modified','artifact hash'),('missing_fixture','missing '),('wrong_manifest','manifest hash'),('typed_key_swap','acceptance identity'),('public_success_invented','rejection class'),('cases_swapped','case/mode path'),('natural_exit_invented','case scope'),('value_parity_invented','scope'),('checksum_modified','bundled checksum mismatch'),('resealed_raw_source_conflict','byte-identical source hash'),('resealed_record_ret','native selected observations'),('resealed_record_results','native selected observations'),('resealed_raw_and_source','native selected observations'),('resealed_unparseable_raw','native observation unparseable'),('resealed_method_relabel','case artifact provenance method'),
 ('duplicate_case_and_target','global case ID uniqueness/set'),('duplicate_target_only','target case ID uniqueness/set'),('duplicate_case_only','global case ID uniqueness/set'),('unknown_case_id','global case ID uniqueness/set'),('nonstring_case_id','case record id type'),
 ('state_bool','observation state integer type'),('state_float','observation state integer type'),('state_string','observation state integer type'),('state_null','observation state integer type'),('state_missing_key','observation state keys/type'),('state_extra_key','observation state keys/type'),('state_wrong_container','observation state keys/type'),('state_nonfinite','non-finite JSON number'),
 ('observation_extra_key','observation object keys/type'),('observation_missing_key','observation object keys/type'),('observation_id_integer','observation id type/order'),('observation_results_integer','observation RESULTS type'),('observation_duplicate_id','observation id type/order'),('observations_wrong_container','observation list type'),('duplicate_json_field','duplicate JSON key')]
results=[]
with tempfile.TemporaryDirectory(prefix='spritemove-v6-negative-',dir=R.parent) as td:
 for name,expected in cases:
  d=pathlib.Path(td)/name;shutil.copytree(R,d);pin=a.manifest_sha256
  targets='records/targets.json';records='records/cases.json'
  if name=='raw_modified':
   p=next((d/'cases').rglob('native-01.log'));p.write_bytes(p.read_bytes()+b'x')
  elif name=='missing_fixture':next((d/'cases').rglob('SEARCHBOUND01.ERB')).unlink()
  elif name=='wrong_manifest':pin='0'*64
  elif name=='checksum_modified':(d/'manifest.sha256').write_text('0'*64+'\n',encoding='ascii')
  elif name=='resealed_method_relabel':
   mp=d/'manifest.json';m=json.loads(mp.read_text(encoding='utf-8'));next(x for x in m['artifacts'] if x['path'].endswith('native-01.log'))['method']='newly authored';mb=encode(m);mp.write_bytes(mb);pin=sha(mb);(d/'manifest.sha256').write_bytes((pin+'\n').encode('ascii'))
  elif name=='duplicate_case_and_target':
   pin=reseal(d,records,lambda p:edit_json(p,lambda x:x.__setitem__(1,x[0].copy())))
   pin=reseal(d,targets,lambda p:edit_json(p,lambda x:x[0]['case_ids'].__setitem__(1,x[0]['case_ids'][0])))
  elif name=='duplicate_target_only':pin=reseal(d,targets,lambda p:edit_json(p,lambda x:x[0]['case_ids'].__setitem__(1,x[0]['case_ids'][0])))
  elif name=='duplicate_case_only':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[1].__setitem__('case_id',x[0]['case_id'])))
  elif name=='unknown_case_id':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[1].__setitem__('case_id','unknown')))
  elif name=='nonstring_case_id':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0].__setitem__('case_id',1)))
  elif name in ('state_bool','state_float','state_string','state_null','state_nonfinite'):
   values={'state_bool':True,'state_float':1.0,'state_string':'1','state_null':None,'state_nonfinite':float('nan')}
   pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0]['state'].__setitem__('RET',values[name])))
  elif name=='state_missing_key':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0]['state'].pop('RET')))
  elif name=='state_extra_key':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0]['state'].__setitem__('EXTRA',1)))
  elif name=='state_wrong_container':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0].__setitem__('state',[])))
  elif name=='observation_extra_key':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0].__setitem__('EXTRA',1)))
  elif name=='observation_missing_key':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0].pop('RESULTS')))
  elif name=='observation_id_integer':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0].__setitem__('id',1)))
  elif name=='observation_results_integer':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0].__setitem__('RESULTS',1)))
  elif name=='observation_duplicate_id':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][1].__setitem__('id','O01')))
  elif name=='observations_wrong_container':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0].__setitem__('native_selected_observations',{})))
  elif name=='duplicate_json_field':
   def duplicate_key(p):
    text=p.read_text(encoding='utf-8');assert '"RET": 1,' in text;p.write_text(text.replace('"RET": 1,','"RET": 1,\n        "RET": 1,',1),encoding='utf-8',newline='\n')
   pin=reseal(d,records,duplicate_key)
  elif name=='typed_key_swap':pin=reseal(d,targets,lambda p:edit_json(p,lambda x:x[0]['target'].__setitem__('kind','method_as_command')))
  elif name=='public_success_invented':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0].__setitem__('public_runtime_success',True)))
  elif name=='cases_swapped':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['raw_paths'].__setitem__('native-01',x[1]['raw_paths']['native-01'])))
  elif name=='natural_exit_invented':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0].__setitem__('native_natural_exit_observed',True)))
  elif name=='value_parity_invented':pin=reseal(d,targets,lambda p:edit_json(p,lambda x:x[0].__setitem__('public_value_parity_claimed',True)))
  elif name=='resealed_record_ret':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0]['state'].__setitem__('RET',99)))
  elif name=='resealed_record_results':pin=reseal(d,records,lambda p:edit_json(p,lambda x:x[0]['native_selected_observations'][0].__setitem__('RESULTS','changed')))
  else:
   c=json.loads((d/records).read_text(encoding='utf-8'))[0];rel=c['raw_paths']['native-01']
   invalid=name=='resealed_unparseable_raw'
   pin=reseal(d,rel,lambda p:edit_raw(p,'RET=1','RET=?' if invalid else 'RET=9'),replace_source=name!='resealed_raw_source_conflict')
  proc=subprocess.run([sys.executable,'-I','-B',str(d/'verify.py'),'--manifest-sha256',pin],cwd=d.parent,text=True,capture_output=True)
  try:r=json.loads(proc.stdout)
  except ValueError:r={}
  rejected=proc.returncode!=0 and r.get('pass') is False and expected in r.get('error','')
  results.append({'test':name,'rejected_at_expected_check':rejected,'error':r.get('error'),'expected':expected})
print(json.dumps({'pass':all(x['rejected_at_expected_check'] for x in results),'tests':results,'scope':'Specific mutations; a new pin cannot authenticate a rewritten source reference. No rights or runtime proof.'},ensure_ascii=False))
if not all(x['rejected_at_expected_check'] for x in results):sys.exit(2)
