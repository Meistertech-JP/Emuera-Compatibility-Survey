"""Verify saved 28-case bindings; adapted from the 96-case verifier."""
import argparse,collections,hashlib,json,pathlib,re,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
def sha(x):return hashlib.sha256(x).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def check(x,msg):
 if not x:raise ValueError(msg)
def asset(ref):
 name=ref['path'];p=pathlib.PurePosixPath(name);check(not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name,'unsafe asset path');q=HERE.joinpath(*p.parts);check(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(HERE.resolve()),'missing asset');b=q.read_bytes();check(len(b)==ref['size'] and sha(b)==ref['sha256'],'asset sha/size');return b
def verify(doc,expected,refs):
 check(doc['schema']=='selected-three-group-evidence-1','schema');cases=doc['cases'];batch={x['batch_id']:x for x in doc['batches']};expect={x['case_id']:x for x in expected['cases']};eb={x['batch_id']:x for x in expected['batches']};refmap={x['id']:x for x in refs['references']}
 check(len(cases)==len(expect)==28 and len({x['case_id'] for x in cases})==28 and {x['case_id'] for x in cases}==set(expect),'case set');check(len(batch)==len(eb)==28 and set(batch)==set(eb) and len(refmap)==len(refs['references']),'batch/reference set')
 count=0;rawpaths=set()
 for bid,b in batch.items():
  check(enc(b)==enc(eb[bid]),'batch binding');check([x['mode'] for x in b['modes']]==['native-01','native-02','public-01'],'mode set')
  for m in b['modes']:
   prefix='assets/'+bid+'/'+m['mode']+'/';check(m['raw']['path']==prefix+'raw.bin' and m['receipt']['path']==prefix+'receipt.json' and all(i['path']==prefix+'inputs/'+i['relative_name'] for i in m['inputs']),'mode local path')
   check(m['raw']['path'] not in rawpaths,'raw path reused');rawpaths.add(m['raw']['path']);asset(m['raw']);receipt=json.loads(asset(m['receipt']));ins={i['relative_name']:i['sha256'] for i in m['inputs']}
   check(receipt['mode']==m['mode'] and receipt['case_id']==b['case_ids'][0] and receipt['identity_basis']==m['identity_basis'],'receipt case/mode')
   check(receipt['inputs_before']==ins==receipt['inputs_after'] and len(ins)==len(m['inputs']) and 'emuera.config' in ins,'inputs')
   for i in m['inputs']:asset(i)
   check(receipt['selected_raw']=={'sha256':m['raw']['sha256'],'binding_basis':'case_evidence_group_manifest_and_saved_readback'},'raw binding')
   check(type(receipt['recorded_returncode']) is int and receipt['native_natural_exit']==m['native_natural_exit'],'returncode')
   if m['mode'].startswith('native'):check(m['native_natural_exit']=='not_established_from_receipt','native exit')
   else:check(m['native_natural_exit']=='not_applicable','public exit field')
   count+=1
 roles=0;groups=collections.Counter()
 for c in cases:
  x=expect[c['case_id']];check(sha(enc(c))==x['case_projection_sha256'] and c['batch_id']==x['batch_id'] and c['parent_and_case_roles']==x['roles'] and c['record']['scenario_verdict']==x['scenario_verdict'],'case/role/record')
  b=batch[c['batch_id']];check(b['case_ids']==[c['case_id']],'case batch');check(all(r in refmap for r in re.findall(r'\bref:(R\d{5})\b',json.dumps(c,ensure_ascii=False))),'missing reference ID');groups[c['group']]+=1;roles+=len(c['parent_and_case_roles'])
  required={'call-jump-event-comparison':'ERB/REVIEW.ERB','print-d-style-comparison':'ERB/MAIN.ERB','list-owner-completion':'ERB/LISTBOUND.ERB'}
  check(c['group'] in required,'group')
  for m in b['modes']:
   check({required[c['group']],'emuera.config'}<=set(i['relative_name'] for i in m['inputs']),'fixture/config')
   receipt=json.loads(asset(m['receipt']))
   if c['group']=='list-owner-completion':
    check(m['identity_basis']=='case_evidence_and_source_path_receipt_has_no_case_or_mode' and 'source_condition_id' not in receipt and 'source_declared_mode' not in receipt,'legacy receipt identity')
   else:
    check(m['identity_basis']=='case_evidence_source_path_and_receipt_case_mode' and receipt['source_declared_mode']==m['mode'] and isinstance(receipt['source_condition_id'],str) and receipt['source_condition_id'],'receipt identity')
 for r in refmap.values():
  check(r['availability'] in ('included_derivative','not_included'),'ref status')
  if r['availability']=='included_derivative':asset(r['asset'])
  else:check(r['asset'] is None,'not-included reference')
 check(count==84 and roles==39 and groups=={'call-jump-event-comparison':12,'print-d-style-comparison':6,'list-owner-completion':10},'counts')
 return {'result':'PASS_LIMITED','cases':28,'batches':28,'modes':84,'role_pairs':39,'limitations':'Saved evidence bindings only; no engine replay, natural exit or rights approval inferred.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--bindings-sha256',required=True);a=ap.parse_args();check(sha((HERE/'manifest.json').read_bytes())==a.manifest_sha256,'manifest pin');b=(HERE/'expected-bindings.json').read_bytes();check(sha(b)==a.bindings_sha256,'bindings pin');subprocess.run([sys.executable,'-B',str(HERE/'tools/file_set_manifest.py'),'verify','--root','evidence='+str(HERE),'--manifest',str(HERE/'manifest.json')],check=True);print(json.dumps(verify(json.loads((HERE/'index.json').read_bytes()),json.loads(b),json.loads((HERE/'references.json').read_bytes())),ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError,subprocess.CalledProcessError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
