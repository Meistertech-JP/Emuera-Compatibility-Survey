"""Offline verifier for two SPRITEMOVE typed records and four saved cases."""
import argparse,hashlib,json,pathlib,sys,re
R=pathlib.Path(__file__).resolve().parent
def h(b):return hashlib.sha256(b).hexdigest()
def ok(x,s):
 if not x:raise ValueError(s)
def unique_json_object(pairs):
 result={}
 for key,value in pairs:
  ok(key not in result,'duplicate JSON key');result[key]=value
 return result
def bad_json_constant(value):
 raise ValueError('non-finite JSON number')
def strict_json(data):
 return json.loads(data,object_pairs_hook=unique_json_object,parse_constant=bad_json_constant)
STATE_KEYS={'RET','R','ORDER','BEFORE_EXISTS','BEFORE_X','BEFORE_Y','EXISTS','X','Y'}
EXPECTED_CASES={
 'expression_function':{'SPRITEPOS221_spritemove-expression-existing','SPRITEPOS221_spritemove-expression-missing'},
 'method_as_command':{'SPRITEPOS221_spritemove-command-existing','SPRITEPOS221_spritemove-command-missing'},
}
def validate_observations(rows,case_id):
 ok(type(rows) is list,'observation list type')
 wanted=3 if case_id.endswith('-existing') else 1
 ok(len(rows)==wanted,'observation count per case')
 for i,row in enumerate(rows,1):
  ok(type(row) is dict and set(row)=={'id','state','RESULTS'},'observation object keys/type')
  ok(type(row['id']) is str and row['id']==f'O{i:02d}','observation id type/order')
  ok(type(row['RESULTS']) is str,'observation RESULTS type')
  state=row['state'];ok(type(state) is dict and set(state)==STATE_KEYS,'observation state keys/type')
  ok(all(type(value) is int for value in state.values()),'observation state integer type')
 return len(rows),sum(len(x['state'])+1 for x in rows)

# Parse only the recorded Oxx grammar. Continuations end at the recorded log
# separator; an unknown or ambiguous form fails closed, rather than being skipped.
def native_observations(raw,case_id):
 text=raw.decode('utf-16');lines=text.splitlines()
 case_name=case_id.removeprefix('SPRITEPOS221_')
 ok(sum(x=='BEGIN221 '+case_name for x in lines)==1 and lines.count('DONE221')==1,'native bounds')
 start=lines.index('BEGIN221 '+case_name);end=lines.index('DONE221');ok(start<end,'native bounds order')
 rows=[];fragments=None
 for line in lines[start+1:end]:
  if re.match(r'^O\d\d\s',line):
   ok(fragments is None,'unterminated observation');fragments=[line]
  elif line.startswith('※'):
   ok(fragments is not None,'orphan log separator')
   row=''.join(fragments);fragments=None
   pattern=(r'(O\d\d)\s+RET=(-?\d+)\s+R=(-?\d+)\s+RS=\[([^\]]*)\]\s+'
            r'ORDER=(-?\d+)\s+BEFORE_EXISTS=(-?\d+)\s+BEFORE_X=(-?\d+)\s+'
            r'BEFORE_Y=(-?\d+)\s+EXISTS=(-?\d+)\s+X=(-?\d+)\s+Y=(-?\d+)\s*')
   m=re.fullmatch(pattern,row);ok(m is not None,'native observation unparseable')
   names=['RET','R','ORDER','BEFORE_EXISTS','BEFORE_X','BEFORE_Y','EXISTS','X','Y']
   nums=[m[2],m[3],m[5],m[6],m[7],m[8],m[9],m[10],m[11]]
   rows.append({'id':m[1],'state':dict(zip(names,map(int,nums))),'RESULTS':m[4]})
  else:
   ok(fragments is not None and line!='','unexpected native line');fragments.append(line)
 ok(fragments is None and rows,'native incomplete observation')
 ok(len({x['id'] for x in rows})==len(rows),'duplicate native observation')
 return rows

q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);a=q.parse_args()
try:
 mb=(R/'manifest.json').read_bytes();ok(h(mb)==a.manifest_sha256,'manifest hash');ok((R/'manifest.sha256').read_bytes()==(a.manifest_sha256+'\n').encode('ascii'),'bundled checksum mismatch');m=strict_json(mb);ok(m['schema']=='spritemove-finite-projection-v6','schema');files={}
 for x in m['artifacts']:
  p=pathlib.PurePosixPath(x['path']);ok(not p.is_absolute() and '..' not in p.parts and '\\' not in x['path'],'unsafe path');f=R.joinpath(*p.parts);ok(not f.is_symlink() and f.resolve().is_relative_to(R) and f.is_file(),'missing '+x['path']);b=f.read_bytes();ok(h(b)==x['sha256'] and len(b)==x['size'],'artifact hash '+x['path']);ok(x['path'] not in files,'duplicate file');files[x['path']]=b
  for z in x['derived_from']:ok(z['source_id'] in m['sources'] and m['sources'][z['source_id']]['sha256']==z['source_sha256'],'source mapping')
  if x['method']=='byte-identical copy':ok(len(x['derived_from'])==1 and x['sha256']==x['derived_from'][0]['source_sha256'],'byte-identical source hash')
 ok({p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}==set(files)|{'manifest.json','manifest.sha256'},'file set')
 artifacts={x['path']:x for x in m['artifacts']};targets=strict_json(files['records/targets.json']);cases=strict_json(files['records/cases.json']);ok(type(targets) is list and type(cases) is list and len(targets)==2 and len(cases)==4,'population')
 ok(all(type(c) is dict and type(c.get('case_id')) is str for c in cases),'case record id type')
 ids=[c['case_id'] for c in cases];all_expected=set().union(*EXPECTED_CASES.values());ok(len(ids)==len(set(ids)) and set(ids)==all_expected,'global case ID uniqueness/set')
 for c in cases:
  k=c.get('target');ok(type(k) is dict and set(k)=={'kind','name'} and all(type(v) is str for v in k.values()),'case target type/keys');ok(k['kind'] in EXPECTED_CASES and k['name']=='SPRITEMOVE' and c['case_id'] in EXPECTED_CASES[k['kind']],'case target identity')
 expected={'expression_function':('/rows/0','/rows/34','E_FUNCTION','runtime_unknown_function_resolution'),'method_as_command':('/rows/38','/rows/104','E_LOAD','load_unrecognized_exact_target_line')}
 seen=set();observation_count=0;field_count=0;record_observation_count=0;record_field_count=0
 for t in targets:
  ok(type(t) is dict and type(t.get('target')) is dict and set(t['target'])=={'kind','name'} and all(type(v) is str for v in t['target'].values()),'typed target keys/type');kind=t['target']['kind'];ok(kind in expected and kind not in seen and t['target']['name']=='SPRITEMOVE','typed key');seen.add(kind);ap,mp,code,phase=expected[kind]
  ok(t['adapter_pointer']==ap and t['matrix_pointer']==mp and t['outcome']=='documented_difference','acceptance identity')
  ok(t['static_contract']['return_type']=='Int64' and t['static_contract']['argument_types']==['string','Int64','Int64'],'static contract')
  ok(t['static_contract']['form_role']==('expression_value' if kind=='expression_function' else 'method_result_routing') and t['static_contract']['native_result_destination']==('expression_value' if kind=='expression_function' else 'RESULT'),'form role');ok(t['static_contract']['classification']=='source_only' and t['public_positive_runtime_observed'] is False and t['public_value_parity_claimed'] is False,'scope')
  case_ids=t['case_ids'];ok(type(case_ids) is list and all(type(x) is str for x in case_ids) and len(case_ids)==2 and len(set(case_ids))==2 and set(case_ids)==EXPECTED_CASES[kind],'target case ID uniqueness/set')
  my=[c for c in cases if c['target']==t['target']];ok(len(my)==2 and {c['case_id'] for c in my}==EXPECTED_CASES[kind],'case target mapping')
  for c in my:
   ok(c['public_rejection_phase']==phase and c['public_rejection_code']==code and c['public_runtime_success'] is False,'rejection class')
   ok(c['case_id'].startswith('SPRITEPOS221_spritemove-'+('expression-' if kind=='expression_function' else 'command-')),'case id form')
   base='cases/'+c['case_id']+'/'
   ok(c['fixture_path']==base+'fixture/SEARCHBOUND01.ERB' and c['raw_paths']=={'native-01':base+'raw/native-01.log','native-02':base+'raw/native-02.log','public-stdout':base+'raw/public-stdout.bin','public-stderr':base+'raw/public-stderr.bin'},'case/mode path')
   ok(all(artifacts[path]['method']=='byte-identical copy' for path in [c['fixture_path']]+list(c['raw_paths'].values())),'case artifact provenance method')
   ok(c['case_verdict']=='different_scoped' and c['native_natural_exit_observed'] is False and c['pixels_observed'] is False,'case scope')
   rows,fields=validate_observations(c['native_selected_observations'],c['case_id']);record_observation_count+=rows;record_field_count+=fields
   fixture=files[c['fixture_path']];ok(h(fixture)==c['fixture_sha256'] and (b'B=SPRITEMOVE(' if kind=='expression_function' else b'SPRITEMOVE ZZ221NAME()') in fixture,'fixture form')
   for mode in ['native-01','native-02']:
    raw=files[c['raw_paths'][mode]];observed=native_observations(raw,c['case_id']);rows,fields=validate_observations(observed,c['case_id']);ok(observed==c['native_selected_observations'],'native selected observations');observation_count+=rows;field_count+=fields
   err=files[c['raw_paths']['public-stderr']].decode('cp932');ok(code in err,'public error');ok(c['raw_paths']['public-stdout'] in files,'public stdout')
   ok(c['configuration_contents_disclosed'] is False and c['sprite_assets_disclosed'] is False,'withheld inputs')
   pins=c['configuration_pins'];ok({v['mode'] for v in pins}=={'native-01','native-02','public'} and len(pins)==3 and len({v['sha256'] for v in pins})==1,'configuration pins')
   for v in pins+c['withheld_resources']:ok(v['source_id'] in m['sources'] and m['sources'][v['source_id']]['sha256']==v['sha256'],'withheld source pin')
   ok(len(c['withheld_resources'])==(4 if c['case_id'].endswith('-existing') else 0),'sprite inputs')
 ok(seen==set(expected),'missing target');ok((record_observation_count,record_field_count,observation_count,field_count)==(8,80,16,160),'verified population counts');print(json.dumps({'pass':True,'typed_targets':len(seen),'cases':len(ids),'case_record_observations_checked':record_observation_count,'case_record_integer_values_checked':record_observation_count*len(STATE_KEYS),'case_record_string_results_checked':record_observation_count,'native_observations_checked':observation_count,'native_integer_values_checked':observation_count*len(STATE_KEYS),'native_string_results_checked':observation_count,'native_values_checked':field_count,'scope':'Checks saved fixtures, output hashes and all selected Native observations in the bounded Oxx grammar. Static source authenticity and configuration/resource contents require withheld original evidence; no public success or value parity established.'},ensure_ascii=False))
except (ValueError,KeyError,TypeError,UnicodeError,OSError) as e:print(json.dumps({'pass':False,'error':str(e)},ensure_ascii=False));sys.exit(2)
