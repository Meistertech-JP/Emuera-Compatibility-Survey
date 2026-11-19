#!/usr/bin/env python3
"""Read-only local verification of the representative evidence bundle."""
import hashlib,json,pathlib,re,sys
C=pathlib.Path(__file__).resolve().parents[2]
E=C/'evidence/representative-20261116'; D=C/'differences/representative-20261116'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def get(p):return json.loads(p.read_bytes())
def main():
 m=get(E/'manifest.json');catalog=get(D/'catalog.json');require(m['schema']=='representative-evidence-manifest-v1','manifest schema');require(catalog['schema']=='representative-finite-differences-v1','catalog schema')
 entries=m['evidence_files']; paths=[x['path'] for x in entries];require(len(paths)==len(set(paths))==36,'asset uniqueness/count');declared=set(paths)
 actual={x.relative_to(C).as_posix() for x in E.rglob('*') if x.is_file() and x.name!='manifest.json'};require(actual==declared,'evidence file set')
 sensitive=re.compile(r'(?i)(?:[a-z]:[\\/]|\\\\|/users/|/home/|bearer\s|api[_-]?key|password|private_dev)')
 for x in entries:
  r=pathlib.PurePosixPath(x['path']);require(not r.is_absolute() and '..' not in r.parts and r.parts[:2]==('evidence','representative-20261116'),'unsafe path');f=C.joinpath(*r.parts);require(f.is_file() and not f.is_symlink(),'missing file');b=f.read_bytes();require(len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256'],'hash '+x['path']);require(f.suffix.lower() not in ['.exe','.dll','.pyz','.zip'],'executable')
  if f.suffix.lower()=='.bmp':require(b[:2]==b'BM','bitmap header')
  else:
   enc=x['encoding'];enc='utf-8' if enc=='utf-8 JSON derived' else enc;s=b.decode(enc,errors='strict');require(not sensitive.search(s),'sensitive text '+x['path'])
 cases=catalog['cases'];require(len(cases)==4 and len({x['id'] for x in cases})==4,'cases');require({x['id'] for x in cases}=={'COLON_NORMAL_COMPAT_RAND_YES','COLON_RAND_ZERO_COMPAT_YES','P38','GMF_LEX_LONE_EQUALS'},'case ids')
 catpaths=[]
 for x in cases:
  require(x['reproducibility']=='not_established' and 'complete_original_configuration_not_in_candidate' in x['unresolved'],'unsupported reproducibility')
  for f in x['evidence']:
   require(f in entries and f['path'].split('/')[2]==x['id'],'case evidence mapping');catpaths.append(f['path'])
 require(len(catpaths)==36 and set(catpaths)==declared,'catalog coverage')
 def txt(case,name,enc='utf-8'):return (E/case/name).read_bytes().decode(enc)
 for case in ['COLON_NORMAL_COMPAT_RAND_YES','COLON_RAND_ZERO_COMPAT_YES']:
  for i in (1,2):
   s=txt(case,'raw/native-0'+str(i)+'-emuera.log','utf-16');require('OBS_RAND_ZERO=0' in s and 'DONE_'+case in s,'native zero/done');
   if case=='COLON_NORMAL_COMPAT_RAND_YES':require('OBS_RAND_BARE=0' in s,'native bare')
  s=txt(case,'raw/public-stdout.bin');e=txt(case,'raw/public-stderr.bin');require('BEFORE_'+case in s and 'AFTER_'+case not in s and 'OBS_RAND_ZERO=' not in s and 'E_ARGUMENT: RAND:n requires n > 0' in e,'public RAND observation')
  require(get(E/case/'fixture/config-observed.json')['CompatiRAND']=='YES','config observation')
  for mode in ['native-01','public-01']:
   r=get(E/case/('receipts/'+mode+'.json'))
   for path,h in r['inputs_before'].items():
    if path=='emuera.config':continue
    f=E/case/'fixture'/path;require(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==h,'receipt input hash')
 p=txt('P38','raw/public-stdout.txt');e=txt('P38','raw/public-stderr.txt');require('BEFORE' not in p and 'Now Loading' in p and 'E_SYNTAX: Unclosed IF' in e,'P38 public')
 for i in (1,2):
  n=txt('GMF_LEX_LONE_EQUALS','raw/native-0'+str(i)+'-actual-final-log.bin','utf-16');require('GM_BEFORE' in n and 'GM_AFTER' not in n and 'A=1=2' in n and "'=='" in n,'malformed native')
 s=txt('GMF_LEX_LONE_EQUALS','raw/public-stdout.bin','cp932');e=txt('GMF_LEX_LONE_EQUALS','raw/public-stderr.bin');require('GM_BEFORE' in s and 'GM_AFTER' not in s and "Unexpected expression character '=' at column 2: 1=2" in e,'malformed public')
 for doc in ['README.ja.md','README.en.md']:
  text=(D/doc).read_text(encoding='utf-8');require(not sensitive.search(text),'sensitive prose')
  for target in re.findall(r'\]\(([^)]+)\)',text):
   require(not target.startswith(('http:','https:','/')),'external/absolute link');require((D/target).resolve().exists(),'broken link '+target)
 require(not sensitive.search((D/'catalog.json').read_text(encoding='utf-8')),'sensitive catalog')
 print(json.dumps({'status':'PASS','cases':len(cases),'asset_files':len(entries),'claims':'selected raw markers and settings checked','reproducibility':'not_established','scope':'offline bundle integrity; no engine execution'},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
