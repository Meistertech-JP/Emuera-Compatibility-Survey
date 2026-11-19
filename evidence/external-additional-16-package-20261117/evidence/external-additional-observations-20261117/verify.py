#!/usr/bin/env python3
"""Validate this profile offline; verify this code and the external helper against trusted hashes before execution."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
CASES=('GETBITBASE01','INRANGEBASE01','LIMITBASE01','SIGNBASE01','PRINTCCASE01','PRINTFORMCASE01','PRINTFORMLCASE01','PRINTFORMSCASE01','PRINTFORMSWCASE01','PRINTFORMWCASE01','PRINTLCASE01','PRINTVLCASE01','ENCODETOUNINEGATIVE01','ENCODETOUNIRANGE01','COLORNEGFAULT01','SQRTNEGFAULT01')
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
 t=PurePosixPath(s);need(not t.is_absolute() and all(x not in ('.','..') for x in t.parts) and '\\' not in s,'unsafe path');p=ROOT.joinpath(*t.parts);need(p.is_file(),'missing '+s)
 for a in [p,*p.parents]:
  if a==ROOT.parent:break
  need(not a.is_symlink(),'link')
 return p
def ref(x,expected):
 need(set(x)=={'path','size','sha256'} and x['path']==expected,'case/mode/role mismatch');p=file(expected);need(p.stat().st_size==x['size'] and sha(p)==x['sha256'],'asset hash/size mismatch');return p
def decode(p):
 b=p.read_bytes()
 if b.startswith(b'\xff\xfe'):return b.decode('utf-16')
 try:return b.decode('utf-8-sig')
 except UnicodeDecodeError:return b.decode('cp932')
def verify(pin,tool):
 need(re.fullmatch('[0-9a-f]{64}',pin or '') and sha(ROOT/'manifest.json')==pin,'external manifest pin mismatch')
 proc=subprocess.run([sys.executable,'-B',str(tool),'verify','--manifest',str(ROOT/'manifest.json'),'--root','bundle='+str(ROOT)],capture_output=True,text=True);need(proc.returncode==0,'inventory mismatch '+proc.stdout+proc.stderr)
 d=load(ROOT/'records.json');need(d['schema']=='external-additional-observations.v1','schema');rows=d['records'];need(tuple(x['case_id'] for x in rows)==CASES and [x['id'] for x in rows]==[f'C{i:03d}' for i in range(1,17)],'fixed case profile')
 for r in rows:
  rid=r['id'];fam=r['family'];need(r['source_type']=='historical_sha_matched_outside_freeze' and r['targets'],'source type/targets');ins=r['inputs']
  erb=decode(ref(ins['erb'],f'fixtures/{rid}/MAIN.ERB'));ref(ins['config'],f'fixtures/{rid}/emuera.config')
  if 'public_input_tape' in ins:ref(ins['public_input_tape'],f'fixtures/{rid}/input.txt')
  target_text=r['condition'].split(';',1)[0].split('\n',1)[0].strip();need(target_text in erb,'input condition mismatch')
  expected=['native-01','native-02','public'] if fam=='helper_error' else ['native','public'];need([x['mode'] for x in r['modes']]==expected,'mode order')
  if fam=='encode_error':need('historically unpinned' in r['modes'][0]['limitations'] and 'not independently pinned' in r['modes'][1]['limitations'],'missing probe/config limitation')
  for m in r['modes']:
   mode=m['mode'];channels=m['channels'];roles=[x['role'] for x in channels]
   need(roles==(['emuera_log'] if mode.startswith('native') else (['output_log'] if fam=='scalar_result' else ['output_log','stdout','stderr'] if fam=='print_text_logs' else ['stdout','stderr'])),'channel role set')
   for ch in channels:
    role=ch['role'];filename='emuera.log' if role=='emuera_log' else 'output.log' if fam=='scalar_result' else role+'.bin'
    raw=decode(ref(ch['file'],f'raw/{rid}/{mode}/{filename}'));need(ch['observed_lines']==raw.splitlines(),'raw lines mismatch')
   if mode.startswith('native') and fam=='scalar_result':
    lines=channels[0]['observed_lines'];need(any(x.startswith('RESULT=') for x in lines) and 'DONE' in lines,'scalar native marker')
   if mode=='public' and fam=='scalar_result':need(any(x.startswith('RESULT=') for x in channels[0]['observed_lines']) and 'DONE' in channels[0]['observed_lines'],'scalar public marker')
   if fam=='encode_error':
    s='\n'.join(x for ch in channels for x in ch['observed_lines']);need(('エラー' in s) if mode=='native' else ('E_INDEX' in s),'diagnostic absent');need(not any(x.startswith('RESULT=') for ch in channels for x in ch['observed_lines']),'fabricated result after error')
   if fam=='print_text_logs' and mode=='native':need(len(channels[0]['observed_lines'])>1,'no native log content')
 for p in ROOT.rglob('*.md'):
  for s in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):need(not re.match(r'\w+:',s),'external link');file((p.parent.relative_to(ROOT)/s.split('#',1)[0]).as_posix())
 print('PASS: external manifest, 16 distinct cases, case/mode/channel bindings, inputs, exact raw lines and links')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--inventory-tool',type=Path,required=True);a.add_argument('--pin',required=True);v=a.parse_args()
 try:verify(v.pin,v.inventory_tool.resolve())
 except (ValueError,OSError,KeyError,IndexError,TypeError,json.JSONDecodeError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
