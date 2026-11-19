#!/usr/bin/env python3
"""Verify frozen DELCHARA records and raw excerpts using separate trusted pins."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
IDS=('BOUNDARY241_delete_empty_normalized','BOUNDARY241_delete_negative','BOUNDARY241_delete_duplicate_retry')
SPECS = {
 'C01': {'condition':'index zero with zero registered characters','initial':0,'line':16,'statement':'DELCHARA 0','diagnostic':'存在しない登録キャラクタ(0)を削除しようとしました'},
 'C02': {'condition':'negative deletion index','initial':3,'line':23,'statement':'DELCHARA -1','diagnostic':'存在しない登録キャラクタ(-1)を削除しようとしました'},
 'C03': {'condition':'duplicate index failure after all argument helpers; snapshots precede validation','initial':3,'line':23,'statement':'DELCHARA H241A(),H241B()','diagnostic':'同一の登録キャラクタ番号(1)が複数回指定されました'},
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def safe(p):
 need(isinstance(p,str) and '\\' not in p and ':' not in p,'unsafe path');q=PurePosixPath(p);need(not q.is_absolute() and '..' not in q.parts and bool(q.parts),'unsafe path')
 x=ROOT
 for part in q.parts:
  x=x/part;need(not x.is_symlink(),'link')
 need(x.resolve().is_relative_to(ROOT.resolve()) and x.is_file(),'missing or outside file');return x
def ref(o,expected):
 need(set(o)=={'path','size','sha256'} and o['path']==expected,'case/mode/file binding')
 p=safe(o['path']);need(p.stat().st_size==o['size'] and sha(p)==o['sha256'],'asset SHA/size');return p
def main():
 a=argparse.ArgumentParser();a.add_argument('--manifest-sha256',required=True);a.add_argument('--profile-sha256',required=True);a.add_argument('--helper-sha256',required=True);v=a.parse_args()
 for p in (v.manifest_sha256,v.profile_sha256,v.helper_sha256):need(re.fullmatch('[0-9a-f]{64}',p or ''),'invalid external pin')
 need(sha(ROOT/'manifest.json')==v.manifest_sha256 and sha(ROOT/'profile.json')==v.profile_sha256 and sha(ROOT/'tools/file_set_manifest.py')==v.helper_sha256,'external pin mismatch')
 proc=subprocess.run([sys.executable,'-I','-B',str(ROOT/'tools/file_set_manifest.py'),'verify','--root','bundle='+str(ROOT),'--manifest',str(ROOT/'manifest.json')],capture_output=True,text=True)
 need(proc.returncode==0,'manifest mismatch')
 profile=json.loads((ROOT/'profile.json').read_text(encoding='utf8'));need(profile['schema']=='delchara-profile-1' and sha(ROOT/'records.json')==profile['records_sha256'],'fixed record profile mismatch')
 d=json.loads((ROOT/'records.json').read_text(encoding='utf8'));need(d['schema']=='delchara-diagnostics-1' and len(d['cases'])==3 and tuple(x['case_id'] for x in d['cases'])==IDS,'case profile')
 for i,c in enumerate(d['cases'],1):
  alias=f'C{i:02d}';need(c['id']==alias and c['target']=={'kind':'command_or_syntax','name':'DELCHARA'} and c['case_verdict']=='matched_scoped','case identity/role')
  need(c['comparison_scope']=='pre_error_or_argument_helper_checkpoints_and_stop_line' and c['post_error_state']=='UNOBSERVED','scope mismatch')
  spec=SPECS[alias]
  need(c.get('condition')==spec['condition'] and type(c.get('stop_line')) is int and c['stop_line']==spec['line'] and c.get('statement')==spec['statement'],'fixed condition mismatch')
  native_expected=[f"SEARCHBOUND01.ERBの{spec['line']}行目でエラーが発生しました:Emuera1824+v24",'エラー内容：'+spec['diagnostic']]
  py_expected=[f"ERB/SEARCHBOUND01.ERB:{spec['line']}: E_CHARACTER: Invalid/duplicate character index",f"  at @SYSTEM_TITLE ERB/SEARCHBOUND01.ERB:{spec['line']}"]
  need(type(c.get('native_diagnostic')) is list and c['native_diagnostic']==native_expected,'native diagnostic profile mismatch')
  need(type(c.get('py_diagnostic')) is list and c['py_diagnostic']==py_expected,'Py diagnostic profile mismatch')
  ins=c['inputs'];roles={'ERB/SEARCHBOUND01.ERB':f'assets/fixtures/{alias}/SEARCHBOUND01.ERB','csv/CHARA0.CSV':'assets/common/csv/CHARA0.CSV','csv/CHARA10.CSV':'assets/common/csv/CHARA10.CSV','csv/CHARA20.CSV':'assets/common/csv/CHARA20.CSV','emuera.config':'assets/common/emuera.config'}
  need(set(ins)==set(roles),'input roles');[ref(ins[k],p) for k,p in roles.items()]
  modes=c['modes'];need([m['mode'] for m in modes]==['native-01','native-02','py'],'mode identity')
  for m in modes:
   mode=m['mode'];raw=ref(m['observation_raw'],f'assets/raw/{alias}/{mode}/'+('emuera.log' if mode.startswith('native') else 'stdout.bin'))
   b=raw.read_bytes();t=b.decode('utf-16' if mode.startswith('native') else 'cp932');observed=[line for line in t.splitlines() if line.startswith('OBS241 ')]
   need(observed==c['selected_checkpoints'],'selected checkpoints changed')
   need(bool(observed) and observed[0].startswith(f"OBS241 BEFORE N={spec['initial']} "),'initial character count mismatch')
   if mode.startswith('native'):
    actual=[line for line in t.splitlines() if line.startswith('SEARCHBOUND01.ERBの') or line.startswith('エラー内容：')]
    need(actual==native_expected,'Native raw diagnostic mismatch')
    need(m['natural_exit']=='UNOBSERVED','Native exit claim')
   else:
    err=ref(m['stderr'],f'assets/raw/{alias}/py/stderr.bin').read_bytes().decode('utf-8-sig')
    actual=[line for line in err.splitlines() if line.startswith('ERB/SEARCHBOUND01.ERB:') or line.startswith('  at @SYSTEM_TITLE')]
    need(actual==py_expected,'Py raw diagnostic mismatch')
  fixture=ref(ins['ERB/SEARCHBOUND01.ERB'],roles['ERB/SEARCHBOUND01.ERB']).read_text(encoding='utf-8-sig').splitlines()
  need(fixture[c['stop_line']-1].strip()==c['statement'],'fixture stop line mismatch')
  setup=fixture[:c['stop_line']-1]
  if spec['initial']==0:need(not any(x.strip().startswith('ADDCHARA ') for x in setup),'unexpected character setup')
  else:need('ADDCHARA 0,10,20' in setup,'character setup mismatch')
  if alias=='C03':
   a=fixture.index('@H241A');b=fixture.index('@H241B');need(a<b and 'RETURNF 1' in fixture[a:b] and 'RETURNF 1' in fixture[b:],'duplicate helper setup mismatch')
  need(profile['bindings'][i-1]=={'case_id':c['case_id'],'condition':c['id'],'stop_line':c['stop_line'],'statement':c['statement'],'condition_text':c['condition']},'fixed condition binding')
 print('PASS: fixed profile, manifest, 3 cases, 9 mode references, exact raw checkpoints, diagnostics, inputs and stop lines')
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,OSError,IndexError,TypeError,UnicodeError) as exc:print('FAIL:',exc,file=sys.stderr);sys.exit(1)
