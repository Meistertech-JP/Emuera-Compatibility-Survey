"""Offline verification of eleven scoped evidence cases; Python standard library only."""
import argparse,hashlib,json,pathlib,re,sys
R=pathlib.Path(__file__).resolve().parent; H=re.compile(r'^[a-f0-9]{64}$')
EXPECTED={'ARGBOUND245_empty':'diagnostic_difference','ARGBOUND245_hole_middle':'diagnostic_difference','ARGBOUND245_string_numeric':'diagnostic_difference','ARGBOUND245_triple':'continuation_difference','ARGBOUND245_trailing_hole':'continuation_difference','ARGBOUND245_single':'reached_match','ARGBOUND245_dead_string':'skipped_match','ARGBOUND245_dead_hole':'skipped_match','ARGBOUND246_copychara-control':'matched_state','ARGBOUND246_copychara-trailing':'continuation_difference_246','ARGBOUND246_strlen-trailing':'matched_state'}
def sha(b):return hashlib.sha256(b).hexdigest()
def check(x,msg):
 if not x:raise ValueError(msg)
def path(rel):
 p=pathlib.PurePosixPath(rel);check(not p.is_absolute() and '..' not in p.parts and '\\' not in rel,'unsafe path');f=R.joinpath(*p.parts);check(not f.is_symlink() and f.resolve().is_relative_to(R) and f.is_file(),'missing/unsafe '+rel);return f

def main():
 q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);a=q.parse_args()
 check(H.fullmatch(a.manifest_sha256) is not None,'invalid external manifest pin')
 checksum=path('manifest.sha256').read_bytes().decode('ascii')
 check(re.fullmatch(r'[0-9a-f]{64}(?:\r?\n)?',checksum) is not None,'manifest.sha256 format')
 check(checksum.rstrip('\r\n')==a.manifest_sha256,'manifest.sha256 and external pin mismatch')
 mb=path('manifest.json').read_bytes();check(sha(mb)==a.manifest_sha256,'manifest pin');m=json.loads(mb);check(m['schema']=='legacy-case-batch-v1','schema')
 assets=m['artifacts'];src=m['sources'];check(len({x['path'] for x in assets})==len(assets),'duplicate path');cache={}
 for x in assets:
  b=path(x['path']).read_bytes();check(sha(b)==x['sha256'] and len(b)==x['size'],'asset hash '+x['path']);cache[x['path']]=b
  for q in x['derived_from']:check(q['source_id'] in src and src[q['source_id']]['sha256']==q['source_sha256'],'source reference')
 actual={f.relative_to(R).as_posix() for f in R.rglob('*') if f.is_file()};check(actual==set(cache)|{'manifest.json','manifest.sha256'},'unexpected file set')
 counts={};seen=[]
 for entry in m['cases']:
  cid=entry['case_id'];seen.append(cid);r=json.loads(cache[entry['record']]);group=r['group'];check(cid in EXPECTED and EXPECTED[cid]==group,'case group '+cid)
  check(r['case_id']==cid and r['legacy_case_id']==cid.replace('ARGBOUND','PARENT',1),'case alias')
  name=cid.split('_',1)[1];family=245 if cid.startswith('ARGBOUND245_') else 246
  check(r['condition']['name']==name,'condition case')
  target='ADDCOPYCHARA' if family==245 else 'COPYCHARA' if name.startswith('copychara') else 'STRLEN'
  check(r['target']=={'kind':'command_or_syntax','name':target},'typed target');check(r['target_outcome']==('documented_difference' if target=='STRLEN' else 'different_scoped'),'target outcome')
  check(r['necessary_comparison_complete'] is True and r['configuration_contents_disclosed'] is False and r['original_receipts_disclosed'] is False,'scope flags')
  fixture=cache[r['fixture_path']];check(sha(fixture)==r['condition']['fixture_sha256'],'fixture sha');lines=fixture.decode('cp932').splitlines();line=r['condition']['target_line'];check(0<line<=len(lines),'line index')
  if family==246:check(lines[line-1]==r['condition']['call'],'246 invocation')
  else:check(lines[line-1]=='ADDCOPYCHARA'+(' '+r['condition']['arguments'] if r['condition']['arguments'] else ''),'245 invocation')
  runs=r['runs'];check(set(runs)=={'native-01','native-02','public'},'modes');states=[];done=[]
  for mode in ['native-01','native-02','public']:
   x=runs[mode];expected_path='cases/'+cid+'/raw/'+('native-01-emuera.log' if mode=='native-01' else 'native-02-emuera.log' if mode=='native-02' else 'public-stdout.bin');check(x['raw_path']==expected_path,'case/mode raw path');raw=cache[x['raw_path']];check(sha(raw)==x['raw_sha256'] and x['fixture_sha256']==sha(fixture),'raw fixture link '+cid)
   text=raw.decode('utf-16' if mode.startswith('native') else 'cp932');marker='245' if family==245 else '246';check('BEGIN'+marker+' '+name in text,'case marker '+cid)
   isdone=('DONE'+marker in text);check(isdone==x['done'],'done marker '+cid);done.append(isdone)
   if mode.startswith('native'):check(x['natural_exit_observed'] is False,'natural exit')
   if family==245:
    for line_text in x['selected_lines']:check(line_text in text,'selected marker '+cid)
   if x['error'] is not None:
    error=x['error'];errtext=text if mode.startswith('native') else cache[r['public_stderr_path']].decode('cp932');check(error['body'] in errtext,'error body '+cid)
    if mode=='public':check(error['code'] in errtext,'error code '+cid)
   if family==246 and x['state'] is not None:
    s=x['state'];check('STATE246 A=%s B=%s R=%s N=%s F=%s'%tuple(s) in text,'state '+cid);states.append(s)
  if group in ('matched_state','reached_match','skipped_match'):check(r['case_verdict']=='matched_scoped' and done==[True,True,True],'match semantics')
  if group=='diagnostic_difference':check(r['case_verdict']=='different_scoped' and done==[False,False,False] and all(runs[z]['error'] is not None for z in runs),'diagnostic difference')
  if group in ('continuation_difference','continuation_difference_246'):check(r['case_verdict']=='different_scoped' and done==[True,True,False] and runs['public']['error'] is not None,'continuation difference')
  if group=='matched_state':check(len(states)==3 and states[0]==states[1]==states[2],'state equality')
  if group=='skipped_match':check(r['dead_branch_only'] is True and r['target_runtime_entered'] is False and lines[line-2]=='IF 0','dead branch scope')
  if group=='reached_match':check(r['dead_branch_only'] is False and r['target_runtime_entered'] is True,'reached scope')
  check(r['fixture_path']=='cases/'+cid+'/fixture/SEARCHBOUND01.ERB' and r['public_stderr_path']=='cases/'+cid+'/raw/public-stderr.bin','case fixture/stderr path');check(sha(cache[r['public_stderr_path']])==r['public_stderr_sha256'],'stderr hash');check(len({runs[z]['config_sha256'] for z in runs})==1,'mode config hash')
  counts[group]=counts.get(group,0)+1
 check(len(seen)==11 and set(seen)==set(EXPECTED),'case set')
 print(json.dumps({'pass':True,'cases_verified':len(seen),'files_checked':len(assets),'groups':counts,'scope':'Saved records only; no engine execution, full configuration, original record authentication, rights clearance or target-wide proof.'},ensure_ascii=False,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,TypeError,OSError,UnicodeError) as e:print(json.dumps({'pass':False,'error':str(e)},ensure_ascii=False));sys.exit(2)
