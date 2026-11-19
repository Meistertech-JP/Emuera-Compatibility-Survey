"""Exercise negative shapes on isolated owned copies only."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent;h=lambda b:hashlib.sha256(b).hexdigest();enc=lambda x:(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);q.add_argument('--verifier-sha256',required=True);a=q.parse_args();results=[]
with tempfile.TemporaryDirectory(prefix='api75-negative-',dir=R.parent) as td:
 for name in ('wrong_manifest','checksum_changed','target_missing','target_duplicate','wrong_kind_type','spec_boolean_as_integer','case_removed','case_duplicate_within_target','role_promoted','source_pointer_removed','copy_source_mismatch'):
  d=pathlib.Path(td)/name;shutil.copytree(R,d);pin=a.manifest_sha256
  if name=='wrong_manifest':pin='0'*64
  elif name=='checksum_changed':(d/'manifest.sha256').write_bytes(b'0'*64+b'\n')
  else:
   mp=d/'manifest.json';m=json.loads(mp.read_bytes());p=d/'records/targets.json';x=json.loads(p.read_bytes());r=x['targets']
   if name=='target_missing':r.pop()
   elif name=='target_duplicate':r[-1]=r[0]
   elif name=='wrong_kind_type':r[0]['target']['kind']=True
   elif name=='spec_boolean_as_integer':r[0]['public_spec_presence']['function']=0
   elif name=='case_removed':r[0]['case_roles'].pop()
   elif name=='case_duplicate_within_target':r[0]['case_roles'].append(r[0]['case_roles'][0])
   elif name=='role_promoted':
    c=next(c for z in r for c in z['case_roles'] if c['role']=='parent_candidate_not_selected');c['role']='selected_by_typed_readback';c['reason']='selected_by_readback';c['readback_proof_pointer']='/proofs/0';c['source_reported_rejection_phase']='runtime_unknown_function_resolution'
   elif name=='source_pointer_removed':r[0]['lineage']['adapter'].pop('pointer')
   if name=='copy_source_mismatch':
    z=next(z for z in m['artifacts'] if z['method']=='byte-identical copy');sid=z['source_ids'][0];m['sources'][sid]['sha256']='0'*64
   else:
    b=enc(x);p.write_bytes(b);z=next(z for z in m['artifacts'] if z['path']=='records/targets.json');z['size']=len(b);z['sha256']=h(b)
   mb=enc(m);mp.write_bytes(mb);pin=h(mb);(d/'manifest.sha256').write_bytes((pin+'\n').encode('ascii'))
  proc=subprocess.run([sys.executable,'-I','-B',str(d/'verify.py'),'--manifest-sha256',pin,'--verifier-sha256',a.verifier_sha256],cwd=td,capture_output=True,text=True)
  try:res=json.loads(proc.stdout)
  except ValueError:res={}
  results.append({'case':name,'rejected':proc.returncode!=0 and res.get('pass') is False,'error':res.get('error')})
print(json.dumps({'pass':all(z['rejected'] for z in results),'tests':results,'scope':'Listed mutations only; no runtime or authenticity proof.'}));sys.exit(0 if all(z['rejected'] for z in results) else 2)
