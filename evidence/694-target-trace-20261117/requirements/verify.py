"""Offline integrity and link checks for this fixed staging projection."""
import argparse, collections, hashlib, json, pathlib, re, sys
EXPECTED={'requirements.jsonl':'dfb37832a1aca187edb0de8948d74da1d1bb3bc365d865445d93155a381bd8ca','targets.jsonl':'81c7f04116860417ea733e25700f2688d2df2980b2554ab70b70de59fb43ad1e','index.json':'6661746bbc887dcf42f0f247f55851f2ce7f3114a2bd6fca6629bf283a874307','case-id-crosswalk.json':'adcbd778a7cdd07b1a87db81e2771263bdcaa7a552f251c67928a834087df678'}
HEX=re.compile(r'[0-9a-f]{64}\Z')
def digest(b): return hashlib.sha256(b).hexdigest()
def require(condition, message):
 if not condition: raise ValueError(message)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--verifier-sha256',required=True);ap.add_argument('--survey',help='Optional separately supplied pinned survey JSON');a=ap.parse_args()
 require(bool(HEX.fullmatch(a.manifest_sha256)) and bool(HEX.fullmatch(a.verifier_sha256)),'invalid external pin')
 root=pathlib.Path(__file__).resolve().parent
 require(digest(pathlib.Path(__file__).read_bytes())==a.verifier_sha256,'verifier pin mismatch')
 manifest_bytes=(root/'manifest.json').read_bytes();require(digest(manifest_bytes)==a.manifest_sha256,'manifest pin mismatch')
 manifest=json.loads(manifest_bytes);require(manifest['schema']=='requirements-staging-manifest-v1','manifest schema')
 files=manifest['files'];required={'requirements.jsonl','targets.jsonl','index.json','verify.py','README.ja.md','README.en.md','case-id-crosswalk.json'}
 require(set(files)==required,'manifest file set');require({p.name for p in root.iterdir()}==required|{'manifest.json'},'extra or missing file')
 for name,meta in files.items():
  p=root/name;require(p.is_file() and not p.is_symlink(),'file type '+name);data=p.read_bytes();require(len(data)==meta['size'] and digest(data)==meta['sha256'],'file digest '+name)
 for name,h in EXPECTED.items():require(digest((root/name).read_bytes())==h,'fixed index digest '+name)
 index=json.loads((root/'index.json').read_bytes());targets=[json.loads(x) for x in (root/'targets.jsonl').read_text(encoding='utf-8').splitlines()];rows=[json.loads(x) for x in (root/'requirements.jsonl').read_text(encoding='utf-8').splitlines()]
 require(index['schema']=='verification-requirements-index-v2' and index['targets']==len(targets)==694 and index['requirements']==len(rows)==3359,'counts')
 keys=set(); links={};seen_cases=set()
 for i,t in enumerate(targets,1):
  key=(t['typed_key']['kind'],t['typed_key']['name']);require(key not in keys,'duplicate typed key');keys.add(key)
  require(t['source_record_id']==f'TARGET{i:04d}','target ID');require(t['existing_projection']['source']=='survey_projection' and t['existing_projection']['pointer']==f'/targets/{i-1}','projection pointer')
  for r in t['case_roles']: seen_cases.add(r['case'])
  for rid in t['requirement_ids']:require(rid not in links,'duplicate target link');links[rid]=key
 counts=collections.Counter()
 for i,r in enumerate(rows,1):
  rid=f'REQ{i:04d}';require(r['requirement_id']==rid and r['source_record_id']==rid,'duplicate or invalid requirement ID')
  key=(r['typed_key']['kind'],r['typed_key']['name']);require(links.get(rid)==key,'requirement target link')
  require(bool(HEX.fullmatch(r['original_text_sha256'])),'source text hash');status=r['text_status'];counts[status]+=1
  if status in ('verbatim','neutralized'):
   require('withheld_reason' not in r and digest(r['verification_requirement'].encode('utf-8'))==r['derived_text_sha256'],'derived text hash')
   if status=='verbatim':require(r['original_text_sha256']==r['derived_text_sha256'],'verbatim text hash')
  else:require(status=='withheld' and 'verification_requirement' not in r and 'derived_text_sha256' not in r and bool(r.get('withheld_reason')),'withheld text')
  for role in r['case_roles']:
   require(role['field'] in {'case_ids','case_id','matching_case_ids','difference_case_ids','accepted_case_ids','independent_gap_case_ids'},'case field');require(role['role'] in {'TARGET_LISTED_IN_CASE','RECORDED_ALIAS_PRIVATE_REVIEW','REGISTERED_CONTEXT_OR_OTHER_TARGET'},'case role');seen_cases.add(role['case'])
 require(len(links)==len(rows) and dict(counts)==index['text_counts'],'link or text counts')
 require(seen_cases=={f'CASE{i:05d}' for i in range(1,index['case_aliases']+1)},'case alias set')
 cross=json.loads((root/'case-id-crosswalk.json').read_bytes());require(cross['schema']=='recorded-case-alias-crosswalk-v1' and cross['source']=='survey_projection','case crosswalk schema')
 require(cross['survey_sha256']==index['source_documents']['survey_projection']['sha256'],'case survey hash');mapping=cross['mappings'];require(len(mapping)==index['case_crosswalk_count']==11,'case crosswalk count')
 require(len({x['case_id'] for x in mapping})==len(mapping) and len({x['case_alias'] for x in mapping})==len(mapping),'case crosswalk duplicates')
 require(all(x['case_alias'] in seen_cases for x in mapping),'unknown case alias')
 if a.survey:
  data=pathlib.Path(a.survey).read_bytes();require(digest(data)==cross['survey_sha256'],'survey digest');survey=json.loads(data);ids={z['case_id'] for v in survey.values() if isinstance(v,list) for z in v if isinstance(z,dict) and isinstance(z.get('case_id'),str)};ids.update(c for t in survey['targets'] for c in t['case_ids']);require(all(x['case_id'] in ids for x in mapping),'case ID missing from survey')
 print('OK: 694 targets; 3359 requirements; '+str(len(seen_cases))+' case aliases; '+json.dumps(dict(counts),sort_keys=True)+'; survey '+('verified' if a.survey else 'not supplied'))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,TypeError,OSError,json.JSONDecodeError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
