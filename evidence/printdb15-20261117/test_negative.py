"""Test bounded integrity and non-invention in disposable private copies."""
import pathlib,json,hashlib,sys,argparse,shutil,tempfile,subprocess
R=pathlib.Path(__file__).resolve().parent;q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);q.add_argument('--verifier-sha256',required=True);a=q.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
def change(d,rel,edit,source=False):
 p=d/rel;edit(p);b=p.read_bytes();mp=d/'manifest.json';m=json.loads(mp.read_bytes());a=next(x for x in m['artifacts'] if x['path']==rel);a['sha256']=sha(b);a['size']=len(b)
 if source:
  sid=a['derived_from'][0]['source_id'];m['sources'][sid]['sha256']=sha(b);m['sources'][sid]['size']=len(b)
  for x in m['artifacts']:
   for ref in x['derived_from']:
    if ref['source_id']==sid:ref['source_sha256']=sha(b)
 mb=enc(m);mp.write_bytes(mb);pin=sha(mb);(d/'manifest.sha256').write_bytes((pin+'\n').encode());return pin
def editjson(f,fn):
 x=json.loads(f.read_bytes());fn(x);f.write_bytes(enc(x))
def rawchange(f):
 x=f.read_bytes().decode('utf-16');assert 'NO_BLOCK_IDX=99 RNG=43' in x;f.write_bytes(x.replace('NO_BLOCK_IDX=99 RNG=43','NO_BLOCK_IDX=88 RNG=43',1).encode('utf-16'))
tests=[('raw_unsealed','artifact SHA'),('raw_resealed','copy source SHA'),('source_and_raw_resealed','native selected values or warning'),('mode_raw_swap','native raw role'),('mode_receipt_swap','mode identity'),('duplicate_target','typed target'),('invent_native_exit','native unobserved exit'),('invent_public_warning','saved scope'),('integer_boolean','integer values'),('private_receipt_field','native receipt fields'),('wrong_pin','manifest pin'),('checksum_changed','checksum'),('config_wrong_source','configuration source identity'),('config_samehash_other_mode','configuration source identity'),('ledger_wrong_pointer','target provenance'),('readback_wrong_pointer','target provenance'),('acceptance_wrong_source','target provenance')];out=[]
with tempfile.TemporaryDirectory(prefix='printdb15-negative-',dir=R.parent) as td:
 for name,expected in tests:
  d=pathlib.Path(td)/name;shutil.copytree(R,d);pin=a.manifest_sha256;case='records/case.json';targets='records/targets.json';raw='cases/PRINTDB15/native-01/raw/emuera.log';receipt='cases/PRINTDB15/native-01/receipt.json'
  if name=='raw_unsealed':(d/raw).write_bytes((d/raw).read_bytes()+b'x')
  elif name=='raw_resealed':pin=change(d,raw,rawchange)
  elif name=='source_and_raw_resealed':pin=change(d,raw,rawchange,True)
  elif name=='mode_raw_swap':pin=change(d,case,lambda p:editjson(p,lambda x:x['modes']['native-01']['raw'].__setitem__('native_log','cases/PRINTDB15/native-02/raw/emuera.log')))
  elif name=='mode_receipt_swap':pin=change(d,case,lambda p:editjson(p,lambda x:x['modes']['native-01'].__setitem__('receipt','cases/PRINTDB15/native-02/receipt.json')))
  elif name=='duplicate_target':pin=change(d,targets,lambda p:editjson(p,lambda x:x.__setitem__(1,x[0].copy())))
  elif name=='invent_native_exit':pin=change(d,receipt,lambda p:editjson(p,lambda x:x.__setitem__('natural_exit_observed',True)))
  elif name=='invent_public_warning':pin=change(d,case,lambda p:editjson(p,lambda x:x['observed'].__setitem__('public_no_display_warning_seen_in_saved_streams',True)))
  elif name=='integer_boolean':pin=change(d,case,lambda p:editjson(p,lambda x:x['observed']['empty_item'].__setitem__('index',False)))
  elif name=='private_receipt_field':pin=change(d,receipt,lambda p:editjson(p,lambda x:x.__setitem__('pid',12345)))
  elif name=='config_wrong_source':pin=change(d,case,lambda p:editjson(p,lambda x:x['modes']['native-01'].__setitem__('configuration_source_id','S004')))
  elif name=='config_samehash_other_mode':pin=change(d,case,lambda p:editjson(p,lambda x:x['modes']['native-01'].__setitem__('configuration_source_id','S013')))
  elif name=='ledger_wrong_pointer':pin=change(d,targets,lambda p:editjson(p,lambda x:x[0].__setitem__('ledger_pointer','/rows/651')))
  elif name=='readback_wrong_pointer':pin=change(d,targets,lambda p:editjson(p,lambda x:x[0].__setitem__('readback_case_pointer','/old_own_case_ids/0')))
  elif name=='acceptance_wrong_source':pin=change(d,targets,lambda p:editjson(p,lambda x:x[0].__setitem__('acceptance_source_id','S006')))
  elif name=='wrong_pin':pin='0'*64
  else:(d/'manifest.sha256').write_text('0'*64+'\n',encoding='ascii')
  z=subprocess.run([sys.executable,'-I','-B',str(d/'verify.py'),'--manifest-sha256',pin,'--verifier-sha256',a.verifier_sha256],cwd=d.parent,text=True,capture_output=True)
  try:r=json.loads(z.stdout)
  except ValueError:r={}
  out.append({'test':name,'rejected':z.returncode!=0 and r.get('pass') is False and expected in r.get('error',''),'error':r.get('error'),'expected':expected})
print(json.dumps({'pass':all(x['rejected'] for x in out),'tests':out,'scope':'Specified mutations only; a regenerated source catalog/pin still needs original evidence or independent trusted pin.'},ensure_ascii=False))
if not all(x['rejected'] for x in out):sys.exit(2)
