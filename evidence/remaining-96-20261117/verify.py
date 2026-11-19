"""Check three-group saved evidence with separately supplied integrity pins.
Adapted from the existing 45-case verifier; no engine replay.
"""
import argparse,collections,hashlib,json,pathlib,re,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def check(v,msg):
 if not v:raise ValueError(msg)
def asset(ref):
 name=ref['path'];p=pathlib.PurePosixPath(name);check(not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name,'unsafe asset path');q=HERE.joinpath(*p.parts)
 check(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(HERE.resolve()),'missing asset');raw=q.read_bytes();check(len(raw)==ref['size'] and sha(raw)==ref['sha256'],'asset SHA/size');return raw
def verify(doc,expected,refs):
 check(doc['schema']=='saved-three-group-evidence-1','schema')
 cases=doc['cases'];batches=doc['batches'];expectcase={x['case_id']:x for x in expected['cases']};expectbatch={x['batch_id']:x for x in expected['batches']};bm={x['batch_id']:x for x in batches};refmap={x['id']:x for x in refs['references']}
 check(len(cases)==len(expectcase)==96 and len({x['case_id'] for x in cases})==96 and {x['case_id'] for x in cases}==set(expectcase),'case identity')
 check(len(bm)==len(expectbatch)==81 and set(bm)==set(expectbatch) and len(refmap)==len(refs['references']),'batch/reference identity')
 modes=0;paths=set();membership=collections.defaultdict(set)
 for bid,b in bm.items():
  check(enc(b)==enc(expectbatch[bid]),'batch asset or case set mismatch')
  check([m['mode'] for m in b['modes']]==['native-01','native-02','public-01'],'batch mode set')
  for m in b['modes']:
   prefix='assets/'+bid+'/'+m['mode']+'/'
   check(m['raw']['path']==prefix+'raw.bin' and m['receipt']['path']==prefix+'receipt.json' and all(x['path']==prefix+'inputs/'+x['relative_name'] for x in m['inputs']),'mode-local path binding')
   check(m['fixture_id']==b['fixture_id'] and m['raw']['path'] not in paths,'mode fixture/raw uniqueness');paths.add(m['raw']['path']);asset(m['raw']);r=json.loads(asset(m['receipt']))
   check(r['fixture_id']==m['fixture_id'] and r['mode']==m['mode'] and r['selected_raw']=={'sha256':m['raw']['sha256'],'binding_basis':m['raw_binding_basis']},'receipt/raw relation')
   ins={x['relative_name']:x['sha256'] for x in m['inputs']};check(len(ins)==len(m['inputs']) and r['inputs_before']==ins==r['inputs_after'],'inputs')
   for x in m['inputs']:asset(x)
   check(type(r['recorded_returncode']) is int and r['native_natural_exit']==m['native_natural_exit'],'receipt outcome')
   if m['mode'].startswith('native'):check(r['native_natural_exit']=='not_established_from_receipt','native natural-exit inference')
   else:check(r['native_natural_exit']=='not_applicable','public native field')
   modes+=1
 rolecount=0;groups=collections.Counter();gate=0;unicode_mode_refs=0;unicode_receipts=set()
 for c in cases:
  e=expectcase[c['case_id']];check(sha(enc(c))==e['case_projection_sha256'] and c['batch_id']==e['batch_id'] and c['parent_and_case_roles']==e['roles'] and c['record']['scenario_verdict']==e['scenario_verdict'],'case/role/semantics mismatch')
  b=bm[c['batch_id']];membership[c['batch_id']].add(c['case_id']);check(c['case_id'] in b['case_ids'],'case batch')
  rolecount+=len(c['parent_and_case_roles']);groups[c['group']]+=1
  if c['group']=='string-slice-repaired-comparison':check(c['case_id']==b['fixture_id'],'slice case/fixture')
  if c['group']=='csv-remaining-execution':check(c['saved_semantic_readback']['preparation']['id']==b['fixture_id'] and c['case_id']=='CSV_REMAINING_'+b['fixture_id']+'_20261116','csv case/fixture')
  if c['group']=='unicode-codeunit-followup':
   observation=c['record']['observation_points_and_comparison'];sem=c['saved_semantic_readback'];condition=sem['condition']
   check(observation['id']==condition['id'] and observation['fixture']==condition['fixture']==b['fixture_id'] and observation['target']==condition['target'] and observation['target'] in c['parent_and_case_roles'] and sem['scenario_verdict']==c['record']['scenario_verdict'],'unicode condition/role/batch')
   unicode_mode_refs+=len(b['modes']);unicode_receipts.update(m['receipt']['path'] for m in b['modes'])
   if b['fixture_id']=='ACTUAL_GATE':gate+=1
 for bid,b in bm.items():check(membership[bid]==set(b['case_ids']),'batch membership')
 for r in refmap.values():
  check(r['availability'] in ('included_derivative','not_included'),'reference status')
  if r['availability']=='included_derivative':asset(r['asset'])
  else:check(r['asset'] is None,'unavailable reference')
 check(groups=={'string-slice-repaired-comparison':36,'csv-remaining-execution':32,'unicode-codeunit-followup':28} and modes==243 and rolecount==114,'counts')
 check(unicode_mode_refs==84 and len(unicode_receipts)==39 and gate==6,'unicode sharing')
 return {'result':'PASS_LIMITED','cases':96,'batches':81,'modes':243,'case_mode_references':288,'roles':114,'unicode_cases':28,'unicode_mode_references':84,'unicode_receipts':39,'actual_gate_cases':6,'limits':'Saved records only; no reach, native natural termination, rights or origin authentication inferred.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--bindings-sha256',required=True);a=p.parse_args()
 check(sha((HERE/'manifest.json').read_bytes())==a.manifest_sha256,'manifest pin');bb=(HERE/'expected-bindings.json').read_bytes();check(sha(bb)==a.bindings_sha256,'bindings pin')
 subprocess.run([sys.executable,'-B',str(HERE/'tools/file_set_manifest.py'),'verify','--root','evidence='+str(HERE),'--manifest',str(HERE/'manifest.json')],check=True)
 print(json.dumps(verify(json.loads((HERE/'index.json').read_bytes()),json.loads(bb),json.loads((HERE/'references.json').read_bytes())),ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError,subprocess.CalledProcessError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
