#!/usr/bin/env python3
"""Offline binding check. Check this file and the inventory helper against external hashes before running."""
import argparse,hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
MODES=('native-01','native-02','public-01')
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'duplicate key');d[k]=v
  return d
 return json.loads(p.read_text(encoding='utf8'),object_pairs_hook=pairs)
def file(path):
 t=PurePosixPath(path);need(not t.is_absolute() and all(x not in ('.','..') for x in t.parts) and '\\' not in path,'unsafe path')
 p=ROOT.joinpath(*t.parts);need(p.is_file(),'missing '+path)
 for q in [p,*p.parents]:
  if q==ROOT.parent:break
  need(not q.is_symlink(),'link')
 return p
def text(p):
 b=p.read_bytes()
 if b.startswith(b'\xff\xfe'):s=b.decode('utf-16')
 else:
  try:s=b.decode('utf-8-sig')
  except UnicodeDecodeError:s=b.decode('cp932')
 return s.replace('\r\n','\n')
def ref(x,path):
 need(set(x)=={'path','sha256','size'} and x['path']==path,'case/mode/role binding mismatch')
 p=file(path);need(p.stat().st_size==x['size'] and sha(p)==x['sha256'],'file hash/size mismatch')
 return p
def verify_archive(path,kind,profile,expected_sha):
 need(path.is_file() and sha(path)==expected_sha,'source archive SHA mismatch')
 members=profile['source_members'];wanted={k:v for k,v in members.items() if v['archive_kind']==kind};seen={}
 with zipfile.ZipFile(path) as z:
  for key,item in wanted.items():
   matches=[x for x in z.infolist() if x.filename==item['member']]
   need(len(matches)==1 and matches[0].file_size==item['size'],'source member missing, duplicated or wrong size')
   raw=z.read(matches[0]);need(hashlib.sha256(raw).hexdigest()==item['sha256'],'source member SHA mismatch');seen[key]=raw.decode('utf-8-sig').splitlines()
  count=0
  for case in profile['cases']:
   for ref in case['source_references']:
    if ref['source'] not in seen:continue
    start,end=ref['lines'];src=seen[ref['source']];need(type(start) is int and type(end) is int and 1<=start<=end<=len(src),'source line range outside member')
    excerpt=('\n'.join(src[start-1:end])+'\n').encode('utf8');need(hashlib.sha256(excerpt).hexdigest()==ref['line_excerpt_sha256'],'source line bytes mismatch');count+=1
 return len(wanted),count
def strict_size(value, label):
 need(type(value) is int and value >= 0, label+' must be a nonnegative integer')
def strict_line_range(value, label):
 need(type(value) is list and len(value)==2 and all(type(x) is int for x in value)
      and 1 <= value[0] <= value[1], label+' must be an ordered positive integer pair')
def strict_bool(value, label):
 need(type(value) is bool, label+' must be a boolean')
def strict_types(records, profile):
 """Check the actual numeric and boolean fields in the frozen v2 schemas."""
 for name,member in profile['source_members'].items(): strict_size(member['size'],'profile member size '+name)
 for case in profile['cases']:
  for ref in case['source_references']: strict_line_range(ref['lines'],'profile source lines')
 for name,member in records['source_members'].items(): strict_size(member['size'],'record member size '+name)
 comparison_flags=('native_repeat_trace_equal','native_repeat_observation_equal',
                   'native_public_events_equal','native_public_before_equal','native_public_done_equal',
                   'native_public_after_equal','exact_diagnostic_equality_claim','source_predictions_are_oracle')
 for case in records['records']:
  strict_line_range(case['input']['body_line_span'],'fixture body line span')
  for asset in case['input']['files'].values(): strict_size(asset['size'],'input file size')
  for ref in case['source_references']: strict_line_range(ref['lines'],'record source lines')
  for flag in comparison_flags: strict_bool(case['recorded_comparison'][flag],'comparison '+flag)
  for mode in case['modes']:
   for flag in ('before','done','diagnostic_present'): strict_bool(mode[flag],'mode '+flag)
   for channel in mode['channels']: strict_size(channel['size'],'channel size')
   line=mode['error_line']
   need(line is None or (type(line) is int and line > 0),'error line must be a positive integer or null')
   ending=mode['ending']
   if mode['mode'].startswith('native'):
    for flag in ('exited_after_5s','cleanup_terminate_ok'): strict_bool(ending[flag],'native ending '+flag)
   elif mode['mode']=='public-01':
    need(type(ending['returncode']) is int,'public returncode must be an integer')
    strict_bool(ending['timeout'],'public ending timeout')
   else: raise ValueError('unknown mode for strict types')

def verify(pin,tool,profile_pin,native_source,py_source):
 need(re.fullmatch('[0-9a-f]{64}',pin or '') and sha(ROOT/'manifest.json')==pin,'external manifest pin mismatch')
 need(re.fullmatch('[0-9a-f]{64}',profile_pin or '') and sha(ROOT/'source-profile.json')==profile_pin,'external source-profile pin mismatch')
 manifest=load(ROOT/'manifest.json')
 for item in manifest['files']: strict_size(item['size'],'manifest file size')
 p=subprocess.run([sys.executable,'-B',str(tool),'verify','--manifest',str(ROOT/'manifest.json'),'--root','bundle='+str(ROOT)],capture_output=True,text=True)
 need(p.returncode==0,'inventory mismatch '+p.stderr+p.stdout)
 d=load(ROOT/'records.json'); need(d['schema']=='operator265-observations.v2','schema')
 rows=d['records'];need(len(rows)==23 and [r['id'] for r in rows]==[f'C{i:03d}' for i in range(1,24)],'profile IDs')
 need(len({r['source_marker'] for r in rows})==23,'duplicate case marker')
 profile=load(ROOT/'source-profile.json');need(profile['schema']=='operator265-independent-source-profile.v1' and len(profile['cases'])==23 and len(profile['source_members'])==27,'source-profile schema')
 strict_types(d,profile)
 need(d['source_members']==profile['source_members'],'source member identity differs from externally pinned profile')
 need(sum(len(x['source_references']) for x in profile['cases'])==71,'source reference count')
 for r,expected in zip(rows,profile['cases']):
  need(r['id']==expected['id'] and r['registry_case_id']==expected['registry_case_id'],'source-profile case mismatch')
  need(r['associated_typed_keys']==expected['associated_typed_keys'],'typed-key metadata differs from externally pinned profile')
  refs=expected['source_references'];need(all(set(x)=={'source','lines','line_excerpt_sha256'} and re.fullmatch('[0-9a-f]{64}',x['line_excerpt_sha256']) for x in refs),'source-profile reference schema')
  need(r['source_references']==[{'source':x['source'],'lines':x['lines']} for x in refs],'source references differ from externally pinned profile')
 need(d['engines']=={'native_exe_sha256':'14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964','native_archive_sha256':'fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a','public_pyz_sha256':'8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35'},'engine pin mismatch')
 env=load(ROOT/'environment.json');need(env['schema']=='operator265-engine-identification.v1' and env['native']['name']=='Emuera1824+v24' and env['native']['executable_sha256']==d['engines']['native_exe_sha256'] and env['native']['archive_sha256']==d['engines']['native_archive_sha256'] and env['public']['name']=='PyEmuera' and env['public']['version']=='3.0.0' and env['public']['sha256']==d['engines']['public_pyz_sha256'],'environment identity mismatch')
 for r in rows:
  rid=r['id'];marker=r['source_marker'];need(r['registry_case_id']=='OPISOLATED265_'+marker,'case registry binding')
  inp=r['input'];need(inp['csv_files']==[] and set(inp['files'])=={'emuera.config','ERB/REVIEW.ERB','ERB/REVIEW.ERH'},'input role set')
  for rel,v in inp['files'].items():ref(v,f'fixtures/{rid}/{rel}')
  erb=text(file(f'fixtures/{rid}/ERB/REVIEW.ERB')).splitlines();lo,hi=inp['body_line_span']
  need(hi<=len(erb) and erb[lo-1:hi]==inp['body'],'fixture condition mismatch')
  need([x['mode'] for x in r['modes']]==list(MODES),'mode set/order')
  need(all(x['kind']=='assignment_syntax' and isinstance(x['name'],str) for x in r['associated_typed_keys']),'associated typed keys')
  for o in r['modes']:
   mode=o['mode'];names=['emuera.log'] if mode.startswith('native') else ['verified.stdout.bin','verified.stderr.bin']
   need(len(o['channels'])==len(names),'channel set')
   channels=[text(ref(v,f'raw/{rid}/{mode}/{name}')) for v,name in zip(o['channels'],names)]
   alltext='\n'.join(channels)
   # The trace is exclusively native emuera.log or public stdout. Stderr is
   # inspected for diagnostics only; no ordering across channels is asserted.
   trace=[x.strip() for x in channels[0].splitlines() if x.strip()]
   before='REVIEW BEFORE '+marker;done='REVIEW DONE '+marker
   need(trace.count(before)==int(o['before']) and trace.count(done)==int(o['done']),'BEFORE/DONE count mismatch')
   events=[x for x in trace if x.startswith('EVENT ')]
   after=[x for x in trace if x.startswith(('REVIEW AFTER ','REVIEW VECTOR ','REVIEW STRCELLS '))]
   sequence=[x for x in trace if x==before or x==done or x.startswith(('EVENT ','REVIEW AFTER ','REVIEW VECTOR ','REVIEW STRCELLS '))]
   need(o['events']==events,'ordered event sequence/count mismatch')
   need(o['after']==after,'ordered after sequence/count mismatch')
   need(o['trace_sequence']==sequence,'ordered trace sequence/count mismatch')
   status=o['status']
   if status=='REACHED_DONE':need(o['before'] and o['done'] and not o['diagnostic_present'],'DONE status mismatch')
   elif status=='REACHED_STOP_WITH_DIAGNOSTIC':need(o['before'] and not o['done'] and o['diagnostic_present'] and not o['after'],'stop status mismatch')
   elif status=='PREENTRY_OR_UNREACHED_STOP_WITH_DIAGNOSTIC':need(not o['before'] and not o['done'] and o['diagnostic_present'] and not o['events'] and not o['after'],'preentry status mismatch')
   else:raise ValueError('unexpected status')
   if o['diagnostic_present']:
    need(('エラー' in alltext or '警告' in alltext) if mode.startswith('native') else re.search(r'\bE_[A-Z]+\b',alltext),'diagnostic missing')
    ln=o['error_line'];need(isinstance(ln,int) and 0<ln<=len(erb) and erb[ln-1].strip()==o['error_source'].strip(),'error source does not match fixture')
    need(o['afterstop_state']=='UNOBSERVED','invented post-error state')
   if mode.startswith('native'):need(o['ending']=={'natural_exit':'unobserved','exited_after_5s':False,'cleanup_terminate_ok':True},'native termination mismatch')
  a,b,pub=r['modes'];cmp=r['recorded_comparison']
  expected={'native_repeat_trace_equal':a['channels'][0]['sha256']==b['channels'][0]['sha256'],'native_repeat_observation_equal':all(a[k]==b[k] for k in ('status','before','after','done','events','error_line','error_source')),'native_public_events_equal':a['events']==pub['events'],'native_public_before_equal':a['before']==pub['before'],'native_public_done_equal':a['done']==pub['done'],'native_public_after_equal':a['after']==pub['after'],'native_error_source':a['error_source'],'public_error_source':pub['error_source'],'native_status':a['status'],'public_status':pub['status'],'exact_diagnostic_equality_claim':False,'source_predictions_are_oracle':False,'semantic_verdict':'PARENT_ADJUDICATION_REQUIRED'}
  need(cmp==expected,'recorded comparison mismatch')
 links=load(ROOT/'case-links.json');need(links['schema']=='operator265-case-links.v1' and len(links['cases'])==23,'case link profile')
 for i,(r,x) in enumerate(zip(rows,links['cases'])):
  need(x['case_id']==r['registry_case_id'] and x['record_id']==r['id'] and x['pointer']=='/records/'+str(i),'case link mismatch')
  for lang in ('ja','en'):
   need(x[lang]=='OBSERVATIONS_'+lang+'.md#'+r['id'].lower(),'case anchor mismatch')
   need('<a id="'+r['id'].lower()+'"></a>' in (ROOT/('OBSERVATIONS_'+lang+'.md')).read_text(encoding='utf8'),'missing case anchor')
  for rref in r['source_references']:
   need(rref['source'] in d['source_members'] and len(rref['lines'])==2,'source reference')
 for doc in ROOT.rglob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf8')):
   if re.match(r'https?://',link):continue
   need(not re.match(r'\w+:',link),'unsupported external link');file((doc.parent.relative_to(ROOT)/link.split('#',1)[0]).as_posix())
 checks=[]
 for path,kind,expected in ((native_source,'Emuera1824+v24.zip',d['engines']['native_archive_sha256']),(py_source,'PyEmuera-3.0.0.pyz',d['engines']['public_pyz_sha256'])):
  if path is None:checks.append(kind+': source bytes NOT RUN')
  else:
   members,refs=verify_archive(path,kind,profile,expected);checks.append(kind+f': {members} members / {refs} line ranges verified')
 print('PASS: inventory, external profile binding, engine IDs, 23 cases, 69 modes, ordered markers and local links; '+'; '.join(checks))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--inventory-tool',type=Path,required=True);a.add_argument('--pin',required=True);a.add_argument('--profile-pin',required=True);a.add_argument('--native-source-zip',type=Path);a.add_argument('--py-source-pyz',type=Path);z=a.parse_args()
 try:verify(z.pin,z.inventory_tool.resolve(),z.profile_pin,z.native_source_zip,z.py_source_pyz)
 except (ValueError,OSError,KeyError,IndexError,TypeError,UnicodeError,zipfile.BadZipFile,json.JSONDecodeError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
