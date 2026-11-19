"""Exercise integrity and case separation using disposable owned copies."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent;q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);a=q.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def update(root,fn):
 p=root/'manifest.json';m=json.loads(p.read_text(encoding='utf-8'));fn(m);b=(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();p.write_bytes(b);pin=sha(b);(root/'manifest.sha256').write_text(pin+'\n',encoding='ascii');return pin
def record(root,cid,fn):
 rel='cases/'+cid+'/record.json';p=root/rel;r=json.loads(p.read_text(encoding='utf-8'));fn(r);b=(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();p.write_bytes(b)
 def edit(m):
  a=next(x for x in m['artifacts'] if x['path']==rel);a['sha256']=sha(b);a['size']=len(b)
 return update(root,edit)
expected={
 'raw_modified':'asset hash cases/ARGBOUND245_empty/raw/native-01-emuera.log',
 'fixture_missing':'missing/unsafe cases/ARGBOUND245_empty/fixture/SEARCHBOUND01.ERB',
 'wrong_manifest_pin':'manifest.sha256 and external pin mismatch',
 'cross_case_raw':'asset hash cases/ARGBOUND245_single/raw/public-stdout.bin',
 'cross_case_resealed':'case/mode raw path',
 'cross_mode_same_bytes':'case/mode raw path',
 'dead_branch_promoted':'dead branch scope',
 'case_verdict_changed':'diagnostic difference',
 'stderr_missing':'missing/unsafe cases/ARGBOUND246_copychara-trailing/raw/public-stderr.bin',
 'checksum_tampered':'manifest.sha256 and external pin mismatch',
 'checksum_format':'manifest.sha256 format',
 'checksum_missing':'missing/unsafe manifest.sha256',
 'checksum_and_pin_wrong':'manifest pin',
}
results=[]
with tempfile.TemporaryDirectory(prefix='batch-negative-',dir=R.parent) as tmp:
 for name in expected:
  d=pathlib.Path(tmp)/name;shutil.copytree(R,d);pin=a.manifest_sha256
  if name=='raw_modified':
   f=d/'cases/ARGBOUND245_empty/raw/native-01-emuera.log';f.write_bytes(f.read_bytes()+b'x')
  elif name=='fixture_missing':(d/'cases/ARGBOUND245_empty/fixture/SEARCHBOUND01.ERB').unlink()
  elif name=='wrong_manifest_pin':pin='0'*64
  elif name=='cross_case_raw':
   x=d/'cases/ARGBOUND245_single/raw/public-stdout.bin';x.write_bytes((d/'cases/ARGBOUND245_dead_hole/raw/public-stdout.bin').read_bytes())
  elif name=='cross_case_resealed':
   pin=record(d,'ARGBOUND245_single',lambda x:x['runs']['native-01'].__setitem__('raw_path','cases/ARGBOUND245_dead_hole/raw/native-01-emuera.log'))
  elif name=='cross_mode_same_bytes':
   pin=record(d,'ARGBOUND245_single',lambda x:x['runs']['native-01'].__setitem__('raw_path',x['runs']['native-02']['raw_path']))
  elif name=='dead_branch_promoted':pin=record(d,'ARGBOUND245_dead_hole',lambda x:x.__setitem__('target_runtime_entered',True))
  elif name=='case_verdict_changed':pin=record(d,'ARGBOUND245_empty',lambda x:x.__setitem__('case_verdict','matched_scoped'))
  elif name=='stderr_missing':(d/'cases/ARGBOUND246_copychara-trailing/raw/public-stderr.bin').unlink()
  elif name=='checksum_tampered':(d/'manifest.sha256').write_text('0'*64+'\n',encoding='ascii')
  elif name=='checksum_format':(d/'manifest.sha256').write_text(pin+' extra\n',encoding='ascii')
  elif name=='checksum_missing':(d/'manifest.sha256').unlink()
  elif name=='checksum_and_pin_wrong':
   pin='0'*64;(d/'manifest.sha256').write_text(pin+'\n',encoding='ascii')
  x=subprocess.run([sys.executable,'-I','-B',str(d/'verify.py'),'--manifest-sha256',pin],cwd=d.parent,capture_output=True,text=True)
  try:result=json.loads(x.stdout)
  except ValueError:result={}
  results.append({'case':name,'rejected':x.returncode!=0 and result.get('pass') is False and expected[name] in result.get('error',''),'error':result.get('error')})
print(json.dumps({'tests':results,'pass':all(x['rejected'] for x in results),'scope':'Specified mutations only; no historical execution, rights or privacy proof.'},ensure_ascii=False,indent=2))
if not all(x['rejected'] for x in results):sys.exit(2)
