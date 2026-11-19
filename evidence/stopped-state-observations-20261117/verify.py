#!/usr/bin/env python3
"""Verify the bounded public observation profile without original raw bytes."""
import hashlib,json,re,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
OBS_SHA256='90d58796f600e37f210aa88e6418fbc001075ce5894f7b39edefa17fa8ecb4b3'
PINS={'swap-error-native-uia':'efdfe0c3a132fe6c89affd64f04ff6344f39e04f966d027452021ad2c1de32c1','swap-error-py-error-json':'ef9bc01618888d8936dac9c1e77f6fe9f09c09a176069989c93eb22ba1935e8b','numeric-error-native-uia':'844ccb79c65cccd61d06c9a9f869ea144190e67dea20358cc4e26eded493079a','numeric-error-py-error-json':'d4a6edc78164afe43772a51bf80dcc412deecb78f124567bf2b95327d5440b96'}
def fail(s): raise ValueError(s)
def safe(s):
 if not isinstance(s,str) or not s or '\\' in s: fail('invalid relative path')
 p=PurePosixPath(s)
 if p.is_absolute() or '..' in p.parts or re.match(r'^[A-Za-z]:',s): fail('unsafe path')
 return p
def validate(d):
 if d.get('schema')!='stopped-state-observations-1' or len(d.get('cases',[]))!=4: fail('schema/count')
 cs={(x.get('case_id'),x.get('condition')):x for x in d['cases']}
 expected={('SWAP_STOPPED_STATE_DIRECT_READBACK_20261116','normal-control'),('SWAP_STOPPED_STATE_DIRECT_READBACK_20261116','invalid-second-index-stop'),('NUM_ASSIGN_STOPPED_STATE_CONTROL_20261116','normal-control'),('NUM_ASSIGN_STOPPED_STATE_BADINDEX_20261116','bad-index-stop')}
 if len(cs)!=4 or set(cs)!=expected: fail('case/condition binding')
 for (cid,cond),c in cs.items():
  key=[{'kind':'command_or_syntax','name':'SWAP'}] if cid.startswith('SWAP_') else [{'kind':'assignment_syntax','name':'='}]
  if c.get('targets')!=key: fail('typed key')
  for engine in ('native','pyemuera'):
   p=c[engine].get('processes')
   if type(p) is not int or p!=1: fail('strict process count')
  if cond.endswith('stop'):
   if c['native'].get('natural_exit')!='UNOBSERVED' or c['pyemuera'].get('natural_exit')!='UNOBSERVED': fail('natural exit overclaim')
   if c.get('stop',{}).get('after_marker') is not False: fail('after marker')
 if cs[('NUM_ASSIGN_STOPPED_STATE_BADINDEX_20261116','bad-index-stop')]['pyemuera'].get('inferred_effective_cells')!={'ZZV:0':0,'ZZV:1':0}: fail('Py inference')
 for cid,cond in (('SWAP_STOPPED_STATE_DIRECT_READBACK_20261116','invalid-second-index-stop'),('NUM_ASSIGN_STOPPED_STATE_BADINDEX_20261116','bad-index-stop')):
  diag=cs[(cid,cond)].get('diagnostics')
  if diag is None or diag.get('category')!='array_index_out_of_range': fail('missing diagnostic summary')
  for engine in ('native','pyemuera'):
   x=diag.get(engine,{})
   if x.get('source_pin_id') not in PINS or x.get('source_sha256')!=PINS[x['source_pin_id']]: fail('diagnostic source pin mismatch')
  if cid.startswith('SWAP_'):
   if diag['pyemuera'].get('code')!='E_INDEX' or type(diag['pyemuera'].get('line')) is not int or diag['pyemuera']['line']!=5: fail('SWAP Py error')
   if '1,000,000' not in diag['native']['summary'] or '1000000' not in diag['pyemuera']['summary']: fail('SWAP diagnostic values')
  else:
   if diag['pyemuera'].get('code')!='E_INDEX' or type(diag['pyemuera'].get('line')) is not int or diag['pyemuera']['line']!=14: fail('numeric Py error')
   if 'index 2' not in diag['native']['summary'] or 'ZZV(2,)' not in diag['pyemuera']['summary']: fail('numeric diagnostic values')
 if 'LOCAL/REF' not in ' '.join(d.get('limits',[])): fail('scope limits')
 return True
def verify():
 raw=(ROOT/'observations.json').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=OBS_SHA256: fail('independent observations pin')
 m=json.loads((ROOT/'manifest.json').read_bytes())
 if m.get('schema')!='stopped-state-public-bundle-1': fail('manifest schema')
 listed=set()
 for f in m.get('public_files',[]):
  pth=safe(f['path']).as_posix();listed.add(pth);p=(ROOT/pth).resolve();b=p.read_bytes()
  if ROOT.resolve() not in p.parents or not p.is_file() or p.is_symlink(): fail('unsafe/missing public file')
  if len(b)!=f['bytes'] or hashlib.sha256(b).hexdigest()!=f['sha256']: fail('manifest file hash '+pth)
 if {p.name for p in ROOT.iterdir() if p.is_file() and p.name!='manifest.json'}!=listed: fail('unlisted public file')
 d=json.loads(raw);validate(d)
 leak=re.compile(r'(?i)(?:[A-Z]:\\|/Users/|/home/|\\\\[^\\]+\\)')
 for n in ('README_ja.md','README_en.md','observations.json'):
  t=(ROOT/n).read_text(encoding='utf-8')
  if leak.search(t): fail('absolute path leak')
  for dest in re.findall(r'\]\(([^)]+)\)',t):
   if re.match(r'(?i)^(?:https?:|mailto:|[A-Z]:|/|\\\\)',dest): fail('non-relative link')
   leaf=dest.split('#',1)[0]
   if leaf and not (ROOT/leaf).resolve().is_file(): fail('broken relative link')
 return {'status':'PASS','conditions':4,'diagnostic_pins':len(PINS),'checks':['independent observation hash','manifest file hashes and sizes','relative links','strict process types','diagnostic source pin/value bindings','Native direct versus Py map/inference','unobserved limits'],'raw_sha_revalidation':'NOT_POSSIBLE_WITHOUT_EXCLUDED_SOURCE_BYTES'}
if __name__=='__main__':
 try: print(json.dumps(verify(),indent=2))
 except Exception as e: print('FAIL:',e,file=sys.stderr);sys.exit(1)
