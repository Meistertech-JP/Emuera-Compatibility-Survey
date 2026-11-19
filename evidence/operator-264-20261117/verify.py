"""Verify the pinned operator-observation bundle and its recorded raw text."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import re

ROOT=Path(__file__).resolve().parent
def digest(data):return hashlib.sha256(data).hexdigest()
def require(ok,why):
 if not ok:raise ValueError(why)
def read_file(name, expected):
 p=PurePosixPath(name)
 require(name and not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name and p.as_posix()==name,'unsafe asset path')
 f=ROOT.joinpath(*p.parts).resolve();require(f.is_relative_to(ROOT.resolve()) and f.is_file(),'missing/outside asset')
 b=f.read_bytes();require(digest(b)==expected,'asset SHA mismatch')
 return b
def decode(data):
 if data.startswith((b'\xff\xfe',b'\xfe\xff')):return data.decode('utf-16')
 try:return data.decode('utf-8-sig')
 except UnicodeError:return data.decode('cp932')
def run(pin, verifier_pin):
 require(re.fullmatch('[0-9a-fA-F]{64}',pin) is not None,'invalid manifest SHA')
 require(re.fullmatch('[0-9a-fA-F]{64}',verifier_pin) is not None,'invalid verifier SHA')
 m=ROOT/'manifest.json';require(digest(m.read_bytes())==pin.lower(),'external manifest SHA mismatch')
 path=ROOT/'tools/file_set_manifest.py';require(digest(path.read_bytes())==verifier_pin.lower(),'external verifier SHA mismatch')
 spec=importlib.util.spec_from_file_location('file_set_manifest',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 mod.verify(m,{'evidence':ROOT})
 d=json.loads((ROOT/'observations.json').read_text(encoding='utf8'))
 require(d['schema']=='operator-264-saved-observations-v1' and len(d['cases'])==24,'case set')
 seen=set();no_trace=0
 for case in d['cases']:
  cid=case['case_id'];require(cid not in seen,'duplicate case');seen.add(cid)
  require(cid=='OPISOLATED264_'+case['unit_id'] and case['planned_id'].startswith('C264-'),'case identity')
  require(case['verdict'] in {'MATCHED_UNCALLED_CONTINUATION_NO_BODY_CREDIT','MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED','OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE','MATCHED_REACHED_EMITTED_STATE'},'unknown recorded verdict')
  require(case['scenario_verdict']==('different_scoped' if case['verdict']=='OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE' else 'matched_scoped'),'scenario verdict mismatch')
  require(len(case['modes'])==3 and {x['mode'] for x in case['modes']}=={'native-01','native-02','public-01'},'mode set')
  for mode in case['modes']:
   require(mode['engine']==('PyEmuera' if mode['mode']=='public-01' else 'Emuera'),'engine label')
   for role in ('fixture','header','config'):
    x=mode[role];read_file(x['path'],x['sha256'])
   texts=[];trace=mode['trace']
   if trace is None:
    no_trace+=1;require(mode['trace_lines']==[],'unobserved trace has lines')
   else:
    text=decode(read_file(trace['path'],trace['sha256']));require(text.splitlines()==mode['trace_lines'],'trace differs');texts.extend(text.splitlines())
    require(mode['before']==any('REVIEW BEFORE ' in x for x in mode['trace_lines']),'before marker differs')
    require(mode['done']==any('REVIEW DONE ' in x for x in mode['trace_lines']),'done marker differs')
   require(all(x in mode['trace_lines'] for x in mode['event_lines']),'event line not in trace')
   require(all(x in mode['trace_lines'] for x in mode['observed_state_lines']),'state line not in trace')
   diagnostic=mode['stderr']
   if diagnostic is not None:texts.append(decode(read_file(diagnostic['path'],diagnostic['sha256'])))
   require(all(any(reason in text for text in texts) for reason in mode['exact_reason_lines']),'diagnostic not found in raw')
 require(no_trace==2,'unobserved trace count')
 return 'PASS: 24 cases, 72 modes; integrity and raw-text correspondence only'
def main():
 p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--verifier-sha256',required=True);a=p.parse_args()
 try:print(run(a.manifest_sha256,a.verifier_sha256))
 except (ValueError,KeyError,IndexError,TypeError,OSError,UnicodeError) as e:print('FAIL:',e);return 1
 return 0
if __name__=='__main__':raise SystemExit(main())
