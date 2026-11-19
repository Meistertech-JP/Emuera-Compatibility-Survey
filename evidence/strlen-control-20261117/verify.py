"""Verify the saved STRLEN case projection offline using Python 3 standard library."""
import argparse, hashlib, json, pathlib, re, sys
R=pathlib.Path(__file__).resolve().parent
HEX=re.compile(r'^[0-9a-f]{64}$')
def sha(b):return hashlib.sha256(b).hexdigest()
def check(condition,message):
 if not condition:raise ValueError(message)
def safe(rel):
 check(isinstance(rel,str) and '\\' not in rel and not pathlib.PurePosixPath(rel).is_absolute(),'invalid package path')
 path=R.joinpath(*pathlib.PurePosixPath(rel).parts);check(not path.is_symlink(),'symlink prohibited');resolved=path.resolve();check(resolved.is_relative_to(R) and resolved.is_file(),'missing or outside package: '+rel);return resolved
def main():
 q=argparse.ArgumentParser();q.add_argument('--manifest-sha256',required=True);a=q.parse_args()
 check(HEX.fullmatch(a.manifest_sha256) is not None,'invalid external manifest pin')
 checksum=safe('manifest.sha256').read_bytes().decode('ascii')
 check(re.fullmatch(r'[0-9a-f]{64}(?:\r?\n)?',checksum) is not None,'manifest.sha256 format')
 check(checksum.rstrip('\r\n')==a.manifest_sha256,'manifest.sha256 and external pin mismatch')
 mbytes=safe('manifest.json').read_bytes();check(sha(mbytes)==a.manifest_sha256,'manifest pin mismatch');m=json.loads(mbytes)
 check(m['schema']=='strlen-control-projection-v1','schema'); sources=m['sources'];assets=m['artifacts'];check(len({x['path'] for x in assets})==len(assets),'duplicate asset path')
 for k,v in sources.items():check(HEX.fullmatch(v['sha256']) is not None,'invalid source digest '+k)
 bypath={}
 for item in assets:
  b=safe(item['path']).read_bytes();check(sha(b)==item['sha256'] and len(b)==item['size'],'asset checksum: '+item['path']);bypath[item['path']]=b
  for ref in item['derived_from']:
   check(ref['source_id'] in sources and ref['source_sha256']==sources[ref['source_id']]['sha256'],'source mapping mismatch')
 expected=set(bypath)|{'manifest.json','manifest.sha256'}
 actual={x.relative_to(R).as_posix() for x in R.rglob('*') if x.is_file()}
 check(actual==expected,'unexpected or missing files')
 def j(name):return json.loads(bypath[name].decode('utf-8'))
 c=j('records/condition.json');r=j('records/result.json');link=j('records/relationship.json');e=j('records/execution.json')
 check(link['target']=={'kind':'command_or_syntax','name':'STRLEN'},'typed key')
 check(link['legacy_case_id']=='PARENT246_strlen-control' and link['registered_case_id']=='ARGBOUND246_strlen-control','case id')
 check(link['case_outcome']=='matched_scoped' and link['target_outcome']=='documented_difference' and link['historical_parent_review']=='finite_remaining_proof','verdicts')
 check(link['requirement_id']=='finite_boundary_error' and link['coverage']=='selected strlen-control only','scope')
 check(c['name']=='strlen-control' and c['call']=='STRLEN "abc"' and c['target_line']==9,'condition')
 fixture=bypath['fixture/SEARCHBOUND01.ERB'];check(sha(fixture)==c['fixture_sha256'],'fixture SHA');check(fixture.decode('cp932').splitlines()[8]==c['call'],'fixture call')
 expected_state=[919,818,5,1,173];check(r['verdict']=='matched_scoped' and r['state']==expected_state and r['done'] is True,'selected comparison')
 files={'native-01':('raw/native-01-emuera.log','utf-16'),'native-02':('raw/native-02-emuera.log','utf-16'),'public':('raw/public-stdout.bin','cp932')}
 check(set(e['modes'])==set(files),'execution modes')
 for mode,(rel,encoding) in files.items():
  raw=bypath[rel];obs=raw.decode(encoding);record=e['modes'][mode]
  check(sha(raw)==record['raw_sha256'],'raw link '+mode)
  check(record['fixture_sha256']==sha(fixture),'fixture link '+mode)
  check('BEGIN246 strlen-control' in obs and 'STATE246 A=919 B=818 R=5 N=1 F=173' in obs and 'DONE246' in obs,'raw markers '+mode)
  if mode.startswith('native'):check(record['exit_code_observed'] is False and record['natural_exit_observed'] is False,'native exit semantics')
  else:check(record['stdout_sha256']==sha(raw) and record['stderr_sha256']==sha(bypath['raw/public-stderr.bin']),'public receipt hash')
 check(len({e['modes'][mode]['config_sha256'] for mode in files})==1,'configuration hash mismatch')
 check(e['configuration_contents_disclosed'] is False and e['original_receipts_disclosed'] is False,'withheld data status')
 print(json.dumps({'pass':True,'checked_files':len(assets),'case':'ARGBOUND246_strlen-control','native_observations':2,'public_stdout_and_stderr':True,'selected_state':expected_state,'scope':'Integrity and selected stored observation only; no source authenticity, public clearance, full settings, historical runtime execution or target-wide reproof.'},ensure_ascii=False,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,IndexError,TypeError,OSError,UnicodeError) as ex:print(json.dumps({'pass':False,'error':str(ex)},ensure_ascii=False));sys.exit(2)
