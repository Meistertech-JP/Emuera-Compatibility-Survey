"""Offline verifier for two SPRITESETPOS typed records and four saved cases."""
import argparse,hashlib,json,pathlib,re,sys
R=pathlib.Path(__file__).resolve().parent
COPY_BINDINGS_SHA256='97afc10abd2eeb413908b99249ecd5a25af95b8adeb2fb0f20d1bf8ce6ce46ab'
EXPECTED_CASES={
 'expression_function':{'SPRITEPOS221_spritesetpos-expression-existing','SPRITEPOS221_spritesetpos-expression-missing'},
 'method_as_command':{'SPRITEPOS221_spritesetpos-command-existing','SPRITEPOS221_spritesetpos-command-missing'},
}
STATE_KEYS={'RET','R','ORDER','BEFORE_EXISTS','BEFORE_X','BEFORE_Y','EXISTS','X','Y'}
def h(b):return hashlib.sha256(b).hexdigest()
def ok(x,s):
 if not x:raise ValueError(s)
q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);q.add_argument('--verifier-sha256',required=True);a=q.parse_args()
try:
 ok(re.fullmatch(r'[0-9a-f]{64}',a.manifest_sha256) is not None and re.fullmatch(r'[0-9a-f]{64}',a.verifier_sha256) is not None,'pin format')
 ok(h((R/'verify.py').read_bytes())==a.verifier_sha256,'verifier hash')
 checksum=R/'manifest.sha256';ok(not checksum.is_symlink() and checksum.is_file(),'missing manifest.sha256');cs=checksum.read_bytes().decode('ascii');ok(re.fullmatch(r'[0-9a-f]{64}(?:\r?\n)?',cs) is not None,'manifest.sha256 format');ok(cs.rstrip('\r\n')==a.manifest_sha256,'manifest.sha256 and external pin mismatch')
 mp=R/'manifest.json';ok(not mp.is_symlink() and mp.is_file(),'missing manifest.json');mb=mp.read_bytes();ok(h(mb)==a.manifest_sha256,'manifest hash');m=json.loads(mb);ok(m['schema']=='spritesetpos-finite-projection-v1','schema');files={};copy_bindings={}
 for x in m['artifacts']:
  p=pathlib.PurePosixPath(x['path']);ok(not p.is_absolute() and '..' not in p.parts and '\\' not in x['path'],'unsafe path');f=R.joinpath(*p.parts);ok(not f.is_symlink() and f.resolve().is_relative_to(R) and f.is_file(),'missing '+x['path']);b=f.read_bytes();ok(h(b)==x['sha256'] and len(b)==x['size'],'artifact hash '+x['path']);ok(x['path'] not in files,'duplicate file');files[x['path']]=b
  for z in x['derived_from']:ok(z['source_id'] in m['sources'] and m['sources'][z['source_id']]['sha256']==z['source_sha256'],'source mapping')
  if x['path'].startswith('cases/') or x['path'].startswith(('LICENSES/','vendor/emuera/')):
   ok(x['method']=='byte-identical copy' and len(x['derived_from'])==1,'copy method/source')
   z=x['derived_from'][0];ok(x['sha256']==z['source_sha256'],'byte copy digest mismatch')
   copy_bindings[x['path']]={'source_id':z['source_id'],'source_sha256':z['source_sha256']}
 ok(len(copy_bindings)==25 and h(json.dumps(copy_bindings,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))==COPY_BINDINGS_SHA256,'copy source bindings')
 ok({p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}==set(files)|{'manifest.json','manifest.sha256'},'file set')
 targets=json.loads(files['records/targets.json']);cases=json.loads(files['records/cases.json']);ok(type(targets) is list and type(cases) is list and len(targets)==2 and len(cases)==4,'population')
 ok(all(type(c) is dict and type(c.get('case_id')) is str for c in cases),'case ID type')
 ids=[c['case_id'] for c in cases];ok(len(set(ids))==4 and set(ids)==set().union(*EXPECTED_CASES.values()),'case ID population')
 expected={'expression_function':('/rows/1','/rows/35','E_FUNCTION','runtime_unknown_function_resolution'),'method_as_command':('/rows/39','/rows/105','E_LOAD','load_unrecognized_exact_target_line')}
 seen=set();observations=0;state_values=0;record_observations=0;record_numeric_values=0;record_results=0
 for t in targets:
  kind=t['target']['kind'];ok(kind in expected and kind not in seen and t['target']['name']=='SPRITESETPOS','typed key');seen.add(kind);ap,mp,code,phase=expected[kind]
  ok(t['adapter_pointer']==ap and t['matrix_pointer']==mp and t['outcome']=='documented_difference','acceptance identity')
  ok(t['static_contract']['native_position_operation']=='absolute_set','static position operation');ok(t['static_contract']['return_type']=='Int64' and t['static_contract']['argument_types']==['string','Int64','Int64'],'static contract')
  ok(t['static_contract']['form_role']==('expression_value' if kind=='expression_function' else 'method_result_routing') and t['static_contract']['native_result_destination']==('expression_value' if kind=='expression_function' else 'RESULT'),'form role');ok(t['static_contract']['classification']=='source_only' and t['public_positive_runtime_observed'] is False and t['public_value_parity_claimed'] is False,'scope')
  declared=t['case_ids'];ok(type(declared) is list and len(declared)==2 and all(type(x) is str for x in declared) and len(set(declared))==2 and set(declared)==EXPECTED_CASES[kind],'target case IDs')
  my=[c for c in cases if c['target']==t['target']];ok(len(my)==2 and {c['case_id'] for c in my}==EXPECTED_CASES[kind],'case target mapping')
  for c in my:
   ok(c['public_rejection_phase']==phase and c['public_rejection_code']==code and c['public_runtime_success'] is False,'rejection class')
   ok(c['case_id'].startswith('SPRITEPOS221_spritesetpos-'+('expression-' if kind=='expression_function' else 'command-')),'case id form')
   base='cases/'+c['case_id']+'/'
   ok(c['fixture_path']==base+'fixture/SEARCHBOUND01.ERB' and c['raw_paths']=={'native-01':base+'raw/native-01.log','native-02':base+'raw/native-02.log','public-stdout':base+'raw/public-stdout.bin','public-stderr':base+'raw/public-stderr.bin'},'case/mode path')
   ok(c['case_verdict']=='different_scoped' and c['native_natural_exit_observed'] is False and c['pixels_observed'] is False,'case scope')
   selected=c['native_selected_observations'];expected_count=3 if c['case_id'].endswith('-existing') else 1
   ok(type(selected) is list and len(selected)==expected_count,'record observation count')
   for index,row in enumerate(selected,1):
    ok(type(row) is dict and set(row)=={'id','state','RESULTS'},'record observation keys')
    ok(type(row['id']) is str and row['id']=='O%02d'%index and type(row['RESULTS']) is str,'record observation ID/RESULTS type')
    state=row['state'];ok(type(state) is dict and set(state)==STATE_KEYS and all(type(value) is int for value in state.values()),'record state keys/types')
    record_observations+=1;record_numeric_values+=len(state);record_results+=1
   fixture=files[c['fixture_path']];ok(h(fixture)==c['fixture_sha256'] and (b'B=SPRITESETPOS(' if kind=='expression_function' else b'SPRITESETPOS ZZ221NAME()') in fixture,'fixture form')
   for mode in ['native-01','native-02']:
    raw=files[c['raw_paths'][mode]].decode('utf-16');ok('DONE221' in raw and 'O01' in raw,'native marker')
    extracted=[]
    for match in re.finditer(r'(?m)^(O\d\d)\s',raw):
     frag=raw[match.start():];frag=re.split(r'(?m)^\u203b|^DONE221|^O\d\d\s',frag[len(match.group(0)):],maxsplit=1)[0];frag=re.sub(r'\r?\n','',frag)
     pairs=re.findall(r'\b(RET|R|ORDER|BEFORE_EXISTS|BEFORE_X|BEFORE_Y|EXISTS|X|Y)=(-?\d+)',frag);state={k:int(v) for k,v in pairs};rs=re.search(r'\bRS=\[([^\]]*)\]',frag)
     ok(len(pairs)==len(state)==9 and rs is not None,'native state fields');extracted.append({'id':match[1],'state':state,'RESULTS':rs[1]});observations+=1;state_values+=len(state)+1
    ok(extracted==c['native_selected_observations'],'native selected state mismatch')
   err=files[c['raw_paths']['public-stderr']].decode('cp932');ok(code in err,'public error');ok(c['raw_paths']['public-stdout'] in files,'public stdout')
   ok(c['configuration_contents_disclosed'] is False and c['sprite_assets_disclosed'] is False,'withheld inputs')
   pins=c['configuration_pins'];ok({v['mode'] for v in pins}=={'native-01','native-02','public'} and len(pins)==3 and len({v['sha256'] for v in pins})==1,'configuration pins')
   for v in pins+c['withheld_resources']:ok(v['source_id'] in m['sources'] and m['sources'][v['source_id']]['sha256']==v['sha256'],'withheld source pin')
   ok(len(c['withheld_resources'])==(4 if c['case_id'].endswith('-existing') else 0),'sprite inputs')
 ok(seen==set(expected) and record_observations==8 and record_numeric_values==72 and record_results==8 and observations==16 and state_values==160,'target/observation count');print(json.dumps({'pass':True,'typed_targets':2,'cases':4,'record_observations':record_observations,'record_integer_values':record_numeric_values,'record_string_results':record_results,'native_observations':observations,'native_values':state_values,'byte_copies':len(copy_bindings),'scope':'Stored source pins and saved observations only; no historical authentication, rights clearance, full settings or public value parity.'},ensure_ascii=False))
except (ValueError,KeyError,TypeError,UnicodeError,OSError) as e:print(json.dumps({'pass':False,'error':str(e)},ensure_ascii=False));sys.exit(2)
