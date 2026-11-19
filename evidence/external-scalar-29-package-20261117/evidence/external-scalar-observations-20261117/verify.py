#!/usr/bin/env python3
"""Offline bundle check; compare this code and inventory helper against external pins before execution."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
CASES=('ARRAYMSORTBASE01','CBRTBASE01','COLORNAMEBASE01','ENCODETOUNIASCII01','ENCODETOUNIEMPTY01','ENCODETOUNIKANA01','EXPONENTBASE01','GETCONFIGNUM01','GETCONFIGSTR01','GETNUMBASE01','GETNUMCASE01','INRANGEARRAYBASE01','LOG10BASE01','LOGBASE01','MAXBASE01','MINBASE01','POWERBASE01','SAVENOSBASE01','SQRTBASE01','STRFINDBASE01','STRFINDUBASE01','STRLENSUBASE01','SUBSTRINGBASE01','SUBSTRINGUBASE01','TOHALFBASE01','TOINTBASE01','TOLOWERBASE01','TOSTRBASE01','TOUPPERBASE01')
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(p.read_text(encoding='utf8'),object_pairs_hook=pairs)
def file(s):
 t=PurePosixPath(s);need(not t.is_absolute() and all(a not in ('.','..') for a in t.parts) and '\\' not in s,'unsafe path')
 p=ROOT.joinpath(*t.parts);need(p.is_file(),'missing '+s)
 for a in [p,*p.parents]:
  if a==ROOT.parent:break
  need(not a.is_symlink(),'link')
 return p
def ref(r,expected):
 need(set(r)=={'path','size','sha256'} and r['path']==expected,'case/mode/role path mismatch');p=file(expected)
 need(p.stat().st_size==r['size'] and sha(p)==r['sha256'],'asset pin mismatch');return p
def decode(p):
 b=p.read_bytes()
 if b.startswith(b'\xff\xfe'):return b.decode('utf-16')
 try:return b.decode('utf-8-sig')
 except UnicodeDecodeError:return b.decode('cp932')
def verify(pin,tool):
 need(re.fullmatch('[0-9a-f]{64}',pin or '') and sha(ROOT/'manifest.json')==pin,'external manifest pin mismatch')
 proc=subprocess.run([sys.executable,'-B',str(tool),'verify','--manifest',str(ROOT/'manifest.json'),'--root','bundle='+str(ROOT)],capture_output=True,text=True)
 need(proc.returncode==0,'inventory mismatch '+proc.stdout+proc.stderr)
 d=load(ROOT/'records.json');need(d['schema']=='external-scalar-observations.v1','schema')
 rs=d['records'];need(tuple(r['case_id'] for r in rs)==CASES and [r['id'] for r in rs]==[f'C{i:03d}' for i in range(1,len(CASES)+1)],'profile case set or order')
 need(len(rs)==29,'29 records')
 c005=next(r for r in rs if r['id']=='C005');need(c005['recorded_scope']=='One recorded empty-string input at index 0; both saved mode logs contain RESULT=-1. This records the observed value for this input only; no generally defined sentinel is asserted.','C005 scope correction')
 c012=next(r for r in rs if r['id']=='C012');need(c012['recorded_scope']=='One recorded 1D numeric array [2,5,8,9], index range [0,4), and value bounds 2 and 9. Saved logs report Native RESULT=3 and PyEmuera RESULT=4. The cited Native source interpretation (>=2 and <9) is attributed to the original comparison and source citation; this record does not independently establish a general boundary rule.','C012 scope correction')
 need(c012.get('comparison')=='different_result_line; source interpretation attributed to original comparison','C012 comparison attribution')
 need(c012.get('interpretation_note')=='The saved raw lines report VALUES=2,5,8,9 and different RESULT values. That the PyEmuera count of 4 includes value 9 is an inference from those lines and the recorded input, not a separately emitted per-element count or a fresh re-execution.','C012 inference note')
 for r in rs:
  rid=r['id'];need(r['external_source']=='historical_record_sha_matches_not_frozen','wrong provenance state')
  ins=r['inputs'];erb=decode(ref(ins['erb'],f'fixtures/{rid}/MAIN.ERB'));ref(ins['config'],f'fixtures/{rid}/emuera.config')
  need(r['expression'] in erb and r['typed_targets'],'fixture expression / typed target')
  seen=set()
  for c in ins['csv']:
   rel=PurePosixPath(c['relative']);need(len(rel.parts)==2 and rel.parts[0].lower()=='csv' and rel.name not in seen,'CSV path');seen.add(rel.name)
   ref(c['file'],f'fixtures/{rid}/'+rel.as_posix())
  for key in ('native','pyemuera'):
   v=r[key];p=ref(v['raw'],f'raw/{rid}/'+('native' if key=='native' else 'public')+'/emuera.log');t=decode(p);actual=[x for x in t.splitlines() if x!='Now Loading...']
   need(v['observed_lines']==actual and v['result_line'] in actual and 'DONE' in actual and v['done'] is True,'observed raw mismatch')
  need(r['native']['natural_exit']=='not established' and r['pyemuera']['returncode']==0,'termination claim')
  expected_comparison='different_result_line; source interpretation attributed to original comparison' if r['id']=='C012' else ('equal_result_line' if r['native']['result_line']==r['pyemuera']['result_line'] else 'different_result_line')
  need(r['comparison']==expected_comparison,'comparison mismatch')
 for p in ROOT.rglob('*.md'):
  for s in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
   need(not re.match(r'\w+:',s),'external link');file((p.parent.relative_to(ROOT)/s.split('#',1)[0]).as_posix())
 print('PASS: external manifest, 29 cases, C005/C012 corrected scope and inference note, separate native/public paths, input and raw markers, local links')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--inventory-tool',type=Path,required=True);a.add_argument('--pin',required=True);x=a.parse_args()
 try:verify(x.pin,x.inventory_tool.resolve())
 except (ValueError,OSError,KeyError,IndexError,TypeError,json.JSONDecodeError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
