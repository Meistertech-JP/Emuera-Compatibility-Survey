"""Negative integrity tests for this projection. Creates and removes only own temporary copies."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent
q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);a=q.parse_args()
def h(b):return hashlib.sha256(b).hexdigest()
def verify(root,pin):
 p=subprocess.run([sys.executable,'-I','-B',str(root/'verify.py'),'--manifest-sha256',pin],cwd=root.parent,capture_output=True,text=True)
 try: body=json.loads(p.stdout)
 except ValueError:body={'error':'invalid verifier output'}
 return p.returncode,body
def change_manifest(root,edit):
 p=root/'manifest.json';m=json.loads(p.read_text(encoding='utf-8'));edit(m);b=(json.dumps(m,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8');p.write_bytes(b);pin=h(b);(root/'manifest.sha256').write_text(pin+'\n',encoding='ascii');return pin
results=[]
expected={
 'native_raw_modified':'asset checksum: raw/native-01-emuera.log',
 'fixture_missing':'missing or outside package: fixture/SEARCHBOUND01.ERB',
 'manifest_pin_wrong':'manifest.sha256 and external pin mismatch',
 'source_hash_mismatch':'source mapping mismatch',
 'derived_state_tampered':'selected comparison',
 'stderr_missing':'missing or outside package: raw/public-stderr.bin',
 'checksum_file_tampered':'manifest.sha256 and external pin mismatch',
 'checksum_file_invalid_format':'manifest.sha256 format',
 'checksum_file_missing':'missing or outside package: manifest.sha256',
 'checksum_and_pin_wrong':'manifest pin mismatch',
}
with tempfile.TemporaryDirectory(prefix='strlen-negative-',dir=R.parent) as t:
 for name in expected:
  d=pathlib.Path(t)/name;shutil.copytree(R,d);pin=a.manifest_sha256
  if name=='native_raw_modified':
   f=d/'raw/native-01-emuera.log';f.write_bytes(f.read_bytes()+b'X')
  elif name=='fixture_missing':(d/'fixture/SEARCHBOUND01.ERB').unlink()
  elif name=='manifest_pin_wrong':pin='0'*64
  elif name=='source_hash_mismatch':
   def edit(m):next(x for x in m['artifacts'] if x['path']=='fixture/SEARCHBOUND01.ERB')['derived_from'][0]['source_sha256']='0'*64
   pin=change_manifest(d,edit)
  elif name=='derived_state_tampered':
   f=d/'records/result.json';v=json.loads(f.read_text(encoding='utf-8'));v['state'][2]=999;b=(json.dumps(v,sort_keys=True,indent=2)+'\n').encode();f.write_bytes(b)
   def edit(m):
    v=next(x for x in m['artifacts'] if x['path']=='records/result.json');v['sha256']=h(b);v['size']=len(b)
   pin=change_manifest(d,edit)
  elif name=='stderr_missing':(d/'raw/public-stderr.bin').unlink()
  elif name=='checksum_file_tampered':(d/'manifest.sha256').write_text('0'*64+'\n',encoding='ascii')
  elif name=='checksum_file_invalid_format':(d/'manifest.sha256').write_text(pin+' extra\n',encoding='ascii')
  elif name=='checksum_file_missing':(d/'manifest.sha256').unlink()
  elif name=='checksum_and_pin_wrong':
   pin='0'*64;(d/'manifest.sha256').write_text(pin+'\n',encoding='ascii')
  rc,body=verify(d,pin);results.append({'case':name,'rejected':rc!=0 and body.get('pass') is False and expected[name] in body.get('error',''),'error':body.get('error')})
print(json.dumps({'tests':results,'pass':all(x['rejected'] for x in results),'scope':'Specified mutations only; no historical, legal, privacy or runtime verification.'},ensure_ascii=False,indent=2))
if not all(x['rejected'] for x in results):sys.exit(2)
