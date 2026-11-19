"""Test explicit integrity and semantic mutations in owned temporary copies."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent
q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);q.add_argument('--verifier-sha256',required=True);a=q.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def seal(root,m):
 b=(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();(root/'manifest.json').write_bytes(b);pin=sha(b);(root/'manifest.sha256').write_bytes((pin+'\n').encode('ascii'));return pin
def change_record(root,rel,edit):
 p=root/rel;obj=json.loads(p.read_bytes());edit(obj);b=(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();p.write_bytes(b);m=json.loads((root/'manifest.json').read_bytes());x=next(x for x in m['artifacts'] if x['path']==rel);x['sha256']=sha(b);x['size']=len(b);return seal(root,m)
expected={
 'raw_modified':'artifact hash', 'missing_fixture':'missing cases/', 'wrong_manifest':'manifest.sha256 and external pin mismatch',
 'typed_key_swap':'acceptance identity', 'public_success_invented':'rejection class', 'cases_swapped':'case/mode path',
 'natural_exit_invented':'case scope', 'value_parity_invented':'scope', 'relative_operation_invented':'static position operation',
 'selected_value_forged':'native selected state mismatch', 'selected_state_swapped':'native selected state mismatch',
 'raw_resealed':'byte copy digest mismatch', 'raw_and_source_resealed':'copy source bindings', 'copy_method_forged':'copy method/source',
 'checksum_tampered':'manifest.sha256 and external pin mismatch', 'checksum_missing':'missing manifest.sha256',
 'checksum_invalid':'manifest.sha256 format', 'checksum_and_pin_wrong':'manifest hash', 'wrong_verifier':'verifier hash',
 'balanced_duplicate_cases':'case ID population', 'target_duplicate_case_ids':'target case IDs', 'unexpected_case_id':'case ID population',
 'state_true':'record state keys/types', 'state_false':'record state keys/types', 'state_float_one':'record state keys/types', 'state_float_zero':'record state keys/types',
 'state_missing_key':'record state keys/types', 'state_extra_key':'record state keys/types',
 'results_not_string':'record observation ID/RESULTS type', 'observation_id_not_string':'record observation ID/RESULTS type',
}
results=[]
with tempfile.TemporaryDirectory(prefix='spritesetpos-negative-',dir=R.parent) as tmp:
 for name,reason in expected.items():
  d=pathlib.Path(tmp)/name;shutil.copytree(R,d);pin=a.manifest_sha256;vpin=a.verifier_sha256
  if name=='raw_modified':
   f=next((d/'cases').rglob('native-01.log'));f.write_bytes(f.read_bytes()+b'x')
  elif name=='missing_fixture':next((d/'cases').rglob('SEARCHBOUND01.ERB')).unlink()
  elif name=='wrong_manifest':pin='0'*64
  elif name=='typed_key_swap':pin=change_record(d,'records/targets.json',lambda x:x[0]['target'].__setitem__('kind','method_as_command'))
  elif name=='public_success_invented':pin=change_record(d,'records/cases.json',lambda x:x[0].__setitem__('public_runtime_success',True))
  elif name=='cases_swapped':pin=change_record(d,'records/cases.json',lambda x:x[0]['raw_paths'].__setitem__('native-01',x[1]['raw_paths']['native-01']))
  elif name=='natural_exit_invented':pin=change_record(d,'records/cases.json',lambda x:x[0].__setitem__('native_natural_exit_observed',True))
  elif name=='value_parity_invented':pin=change_record(d,'records/targets.json',lambda x:x[0].__setitem__('public_value_parity_claimed',True))
  elif name=='relative_operation_invented':pin=change_record(d,'records/targets.json',lambda x:x[0]['static_contract'].__setitem__('native_position_operation','relative_offset'))
  elif name=='selected_value_forged':pin=change_record(d,'records/cases.json',lambda x:x[0]['native_selected_observations'][0]['state'].__setitem__('RET',99))
  elif name=='selected_state_swapped':
   def swap(x):
    s=x[0]['native_selected_observations'];s[0]['state'],s[1]['state']=s[1]['state'],s[0]['state']
   pin=change_record(d,'records/cases.json',swap)
  elif name in ('raw_resealed','raw_and_source_resealed'):
   m=json.loads((d/'manifest.json').read_bytes());entry=next(x for x in m['artifacts'] if x['path'].endswith('/raw/native-01.log'));f=d/entry['path'];raw=f.read_bytes()+b'x';f.write_bytes(raw);entry['sha256']=sha(raw);entry['size']=len(raw)
   if name=='raw_and_source_resealed':
    ref=entry['derived_from'][0];ref['source_sha256']=sha(raw);m['sources'][ref['source_id']]['sha256']=sha(raw)
   pin=seal(d,m)
  elif name=='copy_method_forged':
   m=json.loads((d/'manifest.json').read_bytes());next(x for x in m['artifacts'] if x['path'].endswith('/raw/native-01.log'))['method']='newly authored';pin=seal(d,m)
  elif name=='checksum_tampered':(d/'manifest.sha256').write_bytes(('0'*64+'\n').encode())
  elif name=='checksum_missing':(d/'manifest.sha256').unlink()
  elif name=='checksum_invalid':(d/'manifest.sha256').write_bytes(b'invalid checksum\n')
  elif name=='checksum_and_pin_wrong':pin='0'*64;(d/'manifest.sha256').write_bytes((pin+'\n').encode())
  elif name=='wrong_verifier':vpin='0'*64
  elif name=='balanced_duplicate_cases':
   mp=d/'manifest.json';m=json.loads(mp.read_bytes());cp=d/'records/cases.json';tp=d/'records/targets.json';cases=json.loads(cp.read_bytes());targets=json.loads(tp.read_bytes())
   ex=next(x for x in cases if x['case_id'].endswith('-expression-existing'));cm=next(x for x in cases if x['case_id'].endswith('-command-missing'))
   cases=[ex,ex,cm,cm]
   for t in targets:t['case_ids']=[ex['case_id']]*2 if t['target']['kind']=='expression_function' else [cm['case_id']]*2
   for path,obj in [('records/cases.json',cases),('records/targets.json',targets)]:
    raw=(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();(d/path).write_bytes(raw);entry=next(x for x in m['artifacts'] if x['path']==path);entry['sha256']=sha(raw);entry['size']=len(raw)
   pin=seal(d,m)
  elif name=='target_duplicate_case_ids':pin=change_record(d,'records/targets.json',lambda x:x[0].__setitem__('case_ids',[x[0]['case_ids'][0]]*2))
  elif name=='unexpected_case_id':pin=change_record(d,'records/cases.json',lambda x:x[0].__setitem__('case_id',x[0]['case_id']+'-other'))
  elif name in ('state_true','state_false','state_float_one','state_float_zero'):
   value={'state_true':True,'state_false':False,'state_float_one':1.0,'state_float_zero':0.0}[name];ix=1 if name in ('state_false','state_float_zero') else 0
   pin=change_record(d,'records/cases.json',lambda x:x[ix]['native_selected_observations'][0]['state'].__setitem__('RET',value))
  elif name=='state_missing_key':pin=change_record(d,'records/cases.json',lambda x:x[0]['native_selected_observations'][0]['state'].pop('RET'))
  elif name=='state_extra_key':pin=change_record(d,'records/cases.json',lambda x:x[0]['native_selected_observations'][0]['state'].__setitem__('EXTRA',1))
  elif name=='results_not_string':pin=change_record(d,'records/cases.json',lambda x:x[0]['native_selected_observations'][0].__setitem__('RESULTS',1))
  elif name=='observation_id_not_string':pin=change_record(d,'records/cases.json',lambda x:x[0]['native_selected_observations'][0].__setitem__('id',1))
  p=subprocess.run([sys.executable,'-I','-B',str(d/'verify.py'),'--manifest-sha256',pin,'--verifier-sha256',vpin],cwd=d.parent,text=True,capture_output=True)
  try:res=json.loads(p.stdout)
  except ValueError:res={}
  results.append({'test':name,'rejected':p.returncode!=0 and res.get('pass') is False and reason in res.get('error',''),'error':res.get('error')})
print(json.dumps({'pass':all(x['rejected'] for x in results),'tests':results,'scope':'Specified mutations only; no source authenticity, rights or runtime proof.'},ensure_ascii=False,indent=2))
if not all(x['rejected'] for x in results):sys.exit(2)
