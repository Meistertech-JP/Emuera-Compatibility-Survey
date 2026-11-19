from pathlib import Path
import argparse,collections,hashlib,json,re,subprocess,sys
O=Path(__file__).resolve().parent;TOOL=O/'tools/file_set_manifest.py';h=lambda x:hashlib.sha256(x).hexdigest()
def fail(msg):raise ValueError(msg)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--manifest-sha256',required=True);parser.add_argument('--bindings-sha256',required=True);parser.add_argument('--tool-sha256',required=True);a=parser.parse_args();B=O;manifest=B/'manifest.json'
 if not re.fullmatch(r'[0-9a-f]{64}',a.tool_sha256) or h(TOOL.read_bytes())!=a.tool_sha256:fail('external tool pin mismatch')
 binding_bytes=(B/'bindings.json').read_bytes()
 if not re.fullmatch(r'[0-9a-f]{64}',a.bindings_sha256) or h(binding_bytes)!=a.bindings_sha256:fail('external bindings pin mismatch')
 binding=json.loads(binding_bytes)
 if not re.fullmatch(r'[0-9a-f]{64}',a.manifest_sha256) or h(manifest.read_bytes())!=a.manifest_sha256:fail('external manifest pin mismatch')
 r=subprocess.run([sys.executable,'-I','-B',str(TOOL),'verify','--manifest',str(manifest),'--root','bundle='+str(B)],capture_output=True,text=True)
 if r.returncode:fail('file set rejected: '+r.stderr.strip())
 cases=[json.loads(x) for x in (B/'cases.jsonl').read_bytes().splitlines()];conditions=json.loads((B/'conditions.json').read_bytes());comp=json.loads((B/'comparison.json').read_bytes());modes=json.loads((B/'modes.json').read_bytes())
 if len(cases)!=21 or len({(x['target']['kind'],x['target']['name']) for x in cases})!=21 or len({x['case_id'] for x in cases})!=21:fail('case count or duplication')

 if binding.get('schema')!='display-state-case-bindings.v1':fail('bindings schema')
 bound=binding.get('cases');excluded=binding.get('excluded_case')
 if not isinstance(bound,list) or len(bound)!=21 or not isinstance(excluded,dict):fail('bindings count')
 case_ids=[x['case_id'] for x in cases]; binding_ids=[x['case_id'] for x in bound]
 if len(set(binding_ids))!=21 or set(case_ids)!=set(binding_ids):fail('bindings case set')
 if any(set(x)!={'case_id','target','association_basis','condition_markers','recorded_verdict'} for x in bound):fail('bindings case fields')
 bmap={x['case_id']:x for x in bound}
 for c in cases:
  x=bmap[c['case_id']]
  for key in ('target','association_basis','condition_markers','recorded_verdict'):
   if c[key]!=x[key]:fail('case target or marker binding')
 if excluded!={'case_id':'DISPLAYCOMMAND179_STRLEN','target':{'kind':'command_or_syntax','name':'STRLEN'},'condition_markers':['STATE130','STATE131']}:fail('excluded case binding')
 if excluded['case_id'] in case_ids or any(x['target']==excluded['target'] for x in cases):fail('excluded case selected')
 if len(conditions)!=138 or [x['marker'] for x in conditions]!=['STATE'+str(i) for i in range(138)] or comp['conditions']!=conditions or comp['observation_count']!=138 or comp['verdict']!='matched_scoped':fail('conditions or recorded comparison')
 if modes['selected_cases']!=21 or modes['conditions']!=138 or modes['shared_batch'] is not True or modes['source_case_and_markers_do_not_prove_target_reach'] is not True or modes['native_natural_exit_observed'] is not False or modes['not_selected_but_in_shared_fixture']!='command_or_syntax:STRLEN':fail('scope metadata')
 condition_by_marker={x['marker']:x for x in conditions}
 for c in cases:
  name=c['target']['name'];kind=c['target']['kind'];basis=c['association_basis']
  if c['recorded_verdict']!='matched_scoped' or c['shared_modes']!=['native-01','native-02','public-01'] or c['target_reach']!='NOT_INFERRED_FROM_ROLE_MARKER_OR_SHARED_BATCH' or c['independent_run_per_case'] is not False:fail('case scope')
  if basis=='condition_function_name' and kind=='expression_function':expected=[x['marker'] for x in conditions if x.get('function')==name];n=13
  elif basis=='condition_command_name' and kind=='command_or_syntax':expected=[x['marker'] for x in conditions if x.get('command')==name];n=2
  elif basis=='condition_preceding_command' and kind=='command_or_syntax':expected=[x['marker'] for x in conditions if (x.get('preceding_command') or '').split(' ',1)[0]==name];n=10
  else:fail('unknown association')
  if len(expected)!=n or c['condition_markers']!=expected:fail('case markers '+name)
 records=modes['mode_records']
 if [x['mode'] for x in records]!=['native-01','native-02','public-01']:fail('modes')
 raw_hashes=[];fixtures=[];configs=[]
 for mode in records:
  for kind in ('fixture','config','raw'):
   rel=mode[kind];expected='modes/'+mode['mode']+'/'+{'fixture':'fixture.erb','config':'emuera.config','raw':'raw.log'}[kind]
   if rel!=expected or h((B/rel).read_bytes())!=mode[kind+'_sha256']:fail('mode file '+kind)
  fixtures.append(mode['fixture_sha256']);configs.append(mode['config_sha256']);raw_hashes.append(mode['raw_sha256'])
  if mode['case_run_scope']!='SHARED_BATCH_NOT_21_INDEPENDENT_RUNS' or mode['done_marker_in_raw'] is not True:fail('shared mode scope')
  state=mode['recorded_process']
  if mode['mode'].startswith('native-') and (state['process_created'] is not True or state['natural_exit_observed'] is not False or state['alive_after_5s'] is not True or state['cleanup_terminate_ok'] is not True or state['exit_code'] is not None):fail('native exit scope')
  if mode['mode']=='public-01' and (state['returncode']!=0 or state['inputs_before_after_equal'] is not True or state['pyz_before_after_equal'] is not True):fail('public receipt scope')
  raw=(B/mode['raw']).read_bytes().decode('utf-16').splitlines();seen=[]
  for line in raw:
   m=re.match(r'^(STATE\d+)\s+(.+)$',line)
   if m:seen.append((m[1],m[2]))
  if [v[0] for v in seen]!=[x['marker'] for x in conditions] or raw.count('DONE')!=1:fail('raw marker sequence')
  for (marker,value),cond in zip(seen,conditions):
   label=(cond['function'] if 'function'in cond else 'LENGTH')+'='
   if not value.startswith(label):fail('raw marker label '+marker)
 if len(set(raw_hashes))!=1 or len(set(fixtures))!=1 or len(set(configs))!=1 or modes['raw_byte_equality'] is not True:fail('mode byte equality')
 fixture=(B/records[0]['fixture']).read_bytes().decode('cp932').splitlines();marklines={}
 for i,line in enumerate(fixture):
  m=re.search(r'\b(STATE\d+)\b',line)
  if m:
   if m[1] in marklines:fail('fixture marker duplicate')
   marklines[m[1]]=i
 if set(marklines)!=set(condition_by_marker):fail('fixture markers')
 for c in conditions:
  i=marklines[c['marker']];line=fixture[i]
  if 'function'in c:
   if c['function']+'()' not in line or c['function']+'=' not in line:fail('getter fixture marker')
  elif i<1 or not re.match(r'^'+re.escape(c['command'])+r'(?:\s|$)',fixture[i-1]):fail('command fixture marker')
 bystage=collections.defaultdict(list)
 for c in conditions:
  if 'stage'in c:bystage[c['stage']].append(c)
 if len(bystage)!=13 or any(len(v)!=10 for v in bystage.values()):fail('stage counts')
 prior_end=-1
 for stage,items in bystage.items():
  first=marklines[items[0]['marker']];cmd=items[0]['preceding_command']
  if cmd and cmd not in [s.strip() for s in fixture[prior_end+1:first]]:fail('stage preceding command '+stage)
  prior_end=marklines[items[-1]['marker']]
 print('PASS: pinned case/target/marker bindings and fixture/raw structure; historical verdict retained; expected values NOT independently checked; no target-reach inference')
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,OSError,UnicodeError,TypeError,json.JSONDecodeError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
