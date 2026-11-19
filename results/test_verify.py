#!/usr/bin/env python3
"""Offline integrity negative controls using disposable candidate copies."""
import pathlib,tempfile,shutil,subprocess,sys,json,hashlib
root=pathlib.Path(__file__).resolve().parent.parent
results=[]
with tempfile.TemporaryDirectory(prefix='verify-controls-',dir=root/'results') as tmp:
 dest=pathlib.Path(tmp);(dest/'results').mkdir();(dest/'differences').mkdir()
 for f in ['results/verify.py','results/survey.json','results/manifest.json','differences/catalog.json']: shutil.copyfile(root/f,dest/f)
 def run():return subprocess.run([sys.executable,'-B',str(dest/'results/verify.py')],capture_output=True,text=True)
 def reset():
  for f in ['results/survey.json','results/manifest.json','differences/catalog.json']: shutil.copyfile(root/f,dest/f)
 def reseal(name):
  p=dest/'results/manifest.json';m=json.loads(p.read_bytes());b=(dest/name).read_bytes();m['files'][name]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)};p.write_text(json.dumps(m),encoding='utf-8')
 def change(name,fn):
  p=dest/name;d=json.loads(p.read_bytes());fn(d);p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8');reseal(name)
 def record(label,expected_ok):
  r=run();results.append({'control':label,'pass':(r.returncode==0)==expected_ok,'diagnostic':r.stderr.strip()})
 record('isolated_offline',True)
 (dest/'results/survey.json').write_bytes((dest/'results/survey.json').read_bytes()+b' ');record('altered_hash',False)
 reset();change('results/survey.json',lambda d:d['main_scenarios'][0].update(scenario_verdict='unverified'));record('resealed_wrong_verdict_count',False)
 reset();change('results/survey.json',lambda d:d['main_scenarios'][0].update(case_id=d['main_scenarios'][1]['case_id']));record('resealed_duplicate_case',False)
 reset();change('differences/catalog.json',lambda d:d['main_scenarios'].pop());record('resealed_difference_missing',False)
 reset();change('results/survey.json',lambda d:d['grammar_cases'][0].update(phase='C:\\Users\\private'));record('resealed_private_path',False)
print(json.dumps({'status':'PASS' if all(x['pass'] for x in results) else 'FAIL','controls':results},ensure_ascii=False,indent=2))
sys.exit(0 if all(x['pass'] for x in results) else 1)
