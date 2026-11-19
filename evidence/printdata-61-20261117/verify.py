import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

HERE=pathlib.Path(__file__).resolve().parent
BUNDLE=HERE
CONTRACT=HERE/'expected-bindings.json'
TOOL=HERE/'tools/file_set_manifest.py'

def sha(b):return hashlib.sha256(b).hexdigest()
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def check(ok,msg):
    if not ok:raise ValueError(msg)
def safe_file(root,ref):
    name=ref['path'];p=pathlib.PurePosixPath(name)
    check(p.as_posix()==name and not p.is_absolute() and '..' not in p.parts and ':' not in name and '\\' not in name,'unsafe path')
    f=root.joinpath(*p.parts);check(f.resolve().is_relative_to(root.resolve()) and f.is_file() and not f.is_symlink(),'missing or unsafe asset')
    raw=f.read_bytes();check(len(raw)==ref['size'] and sha(raw)==ref['sha256'],'asset SHA or size')
    return raw

def verify_data(doc,contract,root):
    check(doc['schema']=='saved-case-evidence-index-1','schema')
    cases=doc['cases'];batches=doc['batches'];expected={x['case_id']:x for x in contract['cases']}
    check(len(cases)==len(batches)==len(expected)==61 and len({x['case_id'] for x in cases})==61,'case set')
    check(set(expected)=={x['case_id'] for x in cases},'case identity set')
    bm={x['batch_id']:x for x in batches};check(len(bm)==61,'batch set')
    modes_checked=0;role_count=0
    for case in cases:
        cid=case['case_id'];exp=expected[cid]
        check(sha(encoded(case))==exp['case_projection_sha256'],'case content or verdict')
        check(case['batch_id']==exp['batch_id'] and case['parent_and_case_roles']==exp['roles'] and case['held_context_roles']==exp['held_context_roles'],'case role or batch binding')
        check(case['scenario_verdict']==exp['scenario_verdict'],'scenario verdict')
        batch=bm[case['batch_id']];check(batch['case_ids']==[cid],'batch case relation')
        runs=batch['modes'];check([x['mode'] for x in runs]==['native-01','native-02','public-01'],'mode set')
        fixture_shas=[]
        for run in runs:
            mode=run['mode'];e=exp['mode_expected'][mode]
            check(run['fixture_id']==batch['fixture_id']==e['fixture_id'],'mode fixture identity')
            check(run['raw']['path']==e['raw_path'] and run['receipt_before']['path']==e['receipt_before_path'] and run['receipt_after']['path']==e['receipt_after_path'],'mode asset role path')
            check(run['raw']['sha256']==e['raw_sha256'] and run['receipt_before']['sha256']==e['receipt_before_sha256'] and run['receipt_after']['sha256']==e['receipt_after_sha256'],'mode asset digest')
            check({x['relative_name']:x['sha256'] for x in run['inputs']}==e['input_shas'] and {x['relative_name']:x['path'] for x in run['inputs']}==e['input_paths'],'input identity')
            before=json.loads(safe_file(root,run['receipt_before']));after=json.loads(safe_file(root,run['receipt_after']))
            safe_file(root,run['raw'])
            check(before['fixture']==after['fixture']==run['fixture_id'] and before['mode']==after['mode']==mode,'receipt fixture and mode')
            rawname='emuera.log' if mode.startswith('native-') else 'stdout.bin'
            check(after['outputs'][rawname]==run['raw']['sha256'],'receipt raw relation')
            check(before['inputs_before']==after['inputs_before']==after['inputs_after']==e['input_shas'],'receipt input relation')
            for entry in run['inputs']:safe_file(root,entry)
            fixture_shas.append(e['input_shas']['ERB/MAIN.ERB'])
            stderr=run['stderr'];check((stderr['path'] if stderr else None)==e['stderr_path'],'stderr role path')
            if stderr:safe_file(root,stderr)
            modes_checked+=1
        check(len(set(fixture_shas))==1,'cross-engine fixture SHA')
        role_count+=len(case['parent_and_case_roles'])
    check(modes_checked==183 and role_count==288,'mode or role count')
    return {'result':'PASS_LIMITED','cases':len(cases),'batches':len(batches),'mode_runs':modes_checked,'target_case_roles':role_count,
      'limitations':'Bindings derive from saved records and need an independent pin; no runtime, rights or publication approval.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--bindings-sha256',required=True);a=ap.parse_args()
    check(sha((BUNDLE/'manifest.json').read_bytes())==a.manifest_sha256,'manifest pin')
    raw=CONTRACT.read_bytes();check(sha(raw)==a.bindings_sha256,'bindings pin')
    subprocess.run([sys.executable,'-B',str(TOOL),'verify','--root','evidence='+str(BUNDLE),'--manifest',str(BUNDLE/'manifest.json')],check=True)
    print(json.dumps(verify_data(json.loads((BUNDLE/'index.json').read_text(encoding='utf8')),json.loads(raw),BUNDLE),ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError,subprocess.CalledProcessError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
