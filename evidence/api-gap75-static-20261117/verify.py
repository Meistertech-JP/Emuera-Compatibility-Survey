"""Verify a bounded 75-target static projection without opening private sources."""
import argparse,hashlib,json,pathlib,re,sys
R=pathlib.Path(__file__).resolve().parent
COHORT_SHA='033e48ce51d9a343c9bac29cf6d9ff90853e4bae09c6c320a817fae500e10ba5'
EDGES_SHA='559c8d8a0669b27f86912e8a7253f67f7c68bdd86b18544e7b879860664b1d6a'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(x,msg):
 if not x:raise ValueError(msg)
def obj(pairs):
 d={}
 for k,v in pairs:
  require(k not in d,'duplicate JSON key');d[k]=v
 return d
def bad(x):raise ValueError('nonfinite JSON value')
def read(b):return json.loads(b,object_pairs_hook=obj,parse_constant=bad)
def digest(x):return sha(json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode('ascii'))
try:
 q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);q.add_argument('--verifier-sha256',required=True);a=q.parse_args()
 require(re.fullmatch(r'[a-f0-9]{64}',a.manifest_sha256) is not None and re.fullmatch(r'[a-f0-9]{64}',a.verifier_sha256) is not None,'pin format')
 require(sha((R/'verify.py').read_bytes())==a.verifier_sha256,'verifier hash')
 raw=(R/'manifest.json').read_bytes();require(sha(raw)==a.manifest_sha256,'manifest hash');require((R/'manifest.sha256').read_bytes()==(a.manifest_sha256+'\n').encode('ascii'),'checksum mismatch');m=read(raw)
 require(type(m) is dict and m.get('schema')=='api-gap-static-projection-v1' and type(m.get('sources')) is dict and type(m.get('artifacts')) is list,'manifest schema');sources=m['sources'];files={}
 for x in m['artifacts']:
  require(type(x) is dict and set(x)=={'path','size','sha256','method','source_ids'},'artifact schema');path=x['path'];require(type(path) is str and path and '\\' not in path and ':' not in path,'unsafe artifact path');pp=pathlib.PurePosixPath(path);require(not pp.is_absolute() and '..' not in pp.parts and pp.as_posix()==path,'unsafe artifact path');f=R.joinpath(*pp.parts);require(not f.is_symlink() and f.resolve().is_relative_to(R) and f.is_file(),'missing artifact');b=f.read_bytes();require(path not in files and type(x['size']) is int and len(b)==x['size'] and sha(b)==x['sha256'],'artifact duplicate or hash');files[path]=b
  require(type(x['source_ids']) is list and all(type(z) is str and z in sources for z in x['source_ids']),'artifact source IDs')
  if x['method']=='byte-identical copy':require(len(x['source_ids'])==1 and x['sha256']==sources[x['source_ids'][0]]['sha256'],'copy source hash')
 require({x.relative_to(R).as_posix() for x in R.rglob('*') if x.is_file()}==set(files)|{'manifest.json','manifest.sha256'},'artifact set')
 for k,v in sources.items():require(type(k) is str and type(v) is dict and re.fullmatch(r'[a-f0-9]{64}',v.get('sha256','')) and type(v.get('size')) is int and v['size']>=0,'source schema')
 data=read(files['records/targets.json']);require(type(data) is dict and set(data)=={'schema','scope','targets'} and data['schema']=='api-gap-static-targets-v1','records schema');rows=data['targets'];require(type(rows) is list and len(rows)==75,'target population');ids=[];edges=[];selected=0;unselected=0;function_present=0
 def ref(x,source):
  require(type(x) is dict and set(x)=={'source_id','pointer'} and x['source_id']==source and source in sources and type(x['pointer']) is str and re.fullmatch(r'/[A-Za-z0-9_~/-]+',x['pointer']) is not None,'source pointer')
 for x in rows:
  require(type(x) is dict and set(x)=={'target','lineage','native_registration','public_spec_presence','parent_outcome','case_roles','runtime_verification'},'target schema');t=x['target'];require(type(t) is dict and set(t)=={'kind','name'} and t['kind'] in ('expression_function','method_as_command') and type(t['name']) is str and re.fullmatch(r'[A-Z][A-Z0-9_]*',t['name']),'typed target');key=t['kind']+':'+t['name'];ids.append(key)
  l=x['lineage'];require(type(l) is dict and set(l)=={'target_ledger','adapter','matrix','contract','typed_readback'},'lineage schema');
  for field,sid in [('target_ledger','target_ledger'),('adapter','adapter'),('matrix','matrix'),('contract','contracts')]:ref(l[field],sid)
  rb=l['typed_readback'];require(type(rb) is dict and set(rb)=={'source_id','pointer'} and rb['source_id'] in sources and rb['source_id'].startswith('readback_') and rb['pointer']=='','readback source')
  n=x['native_registration'];require(type(n) is dict and set(n)=={'status','class','registration_line','signature_lines'} and n['status']=='source_registered' and type(n['class']) is str and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',n['class']) and type(n['registration_line']) is int and n['registration_line']>0 and type(n['signature_lines']) is list and n['signature_lines'] and all(type(v) is int and v>0 for v in n['signature_lines']),'native registration')
  s=x['public_spec_presence'];require(type(s) is dict and set(s)=={'function','command'} and type(s['function']) is bool and type(s['command']) is bool,'public spec types');require((not s['function']) if t['kind']=='expression_function' else (not s['command']),'typed availability inconsistency');function_present+=int(t['kind']=='method_as_command' and s['function'])
  require(x['parent_outcome']=='documented_difference' and x['runtime_verification']=='not_reverified_raw_not_included','runtime scope')
  cases=x['case_roles'];require(type(cases) is list and len(cases)>0,'missing case roles');seen=set()
  for c in cases:
   require(type(c) is dict and set(c)=={'case_id','case_register_pointer','matrix_proof_pointer','role','reason','readback_proof_pointer','source_reported_rejection_phase'},'case role schema');cid=c['case_id'];require(type(cid) is str and re.fullmatch(r'[A-Za-z0-9_.-]+',cid) and cid not in seen,'case ID duplicate or type');seen.add(cid);require(type(c['case_register_pointer']) is str and re.fullmatch(r'/records/[0-9]+',c['case_register_pointer']),'case register pointer');require(type(c['matrix_proof_pointer']) is str and re.fullmatch(l['matrix']['pointer']+r'/proof_cases/[0-9]+',c['matrix_proof_pointer']),'matrix proof pointer')
   if c['role']=='selected_by_typed_readback':
    selected+=1;require(c['reason']=='selected_by_readback' and type(c['readback_proof_pointer']) is str and re.fullmatch(r'/proofs/[0-9]+',c['readback_proof_pointer']) and c['source_reported_rejection_phase'] in ('runtime_unknown_function_resolution','load_unrecognized_exact_target_line'),'selected role')
   else:
    unselected+=1;require(c['role']=='parent_candidate_not_selected' and c['reason'] in ('earlier_or_setup_stop','diagnostic_boundary_or_shortcircuit_only','reason_not_specified') and c['readback_proof_pointer'] is None and c['source_reported_rejection_phase'] is None,'unselected role')
   edges.append([key,cid,c['role'],c['reason']])
 require(len(set(ids))==75 and digest(sorted(ids))==COHORT_SHA,'target duplicate or expected set');require(len(edges)==167 and selected==110 and unselected==57 and function_present==7 and digest(sorted(edges))==EDGES_SHA,'case role population');print(json.dumps({'pass':True,'typed_targets':len(ids),'parent_case_role_edges':len(edges),'selected_references':selected,'unselected_references':unselected,'method_targets_with_function_spec':function_present,'scope':'Static source and structured references only; no raw or historical execution verification.'}))
except (ValueError,KeyError,IndexError,TypeError,UnicodeError,OSError,RecursionError) as e:print(json.dumps({'pass':False,'error':str(e)}));sys.exit(2)
