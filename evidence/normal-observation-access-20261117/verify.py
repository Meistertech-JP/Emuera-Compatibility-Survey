"""Check this projection against the separately supplied evidence directory.

Hashes establish byte consistency only, not execution authenticity or rights.
"""
import argparse, hashlib, importlib.util, json, pathlib, re, sys

EXPECTED={'C196_04','C196_05','C196_06','C196_07','C196_13','C196_14','C196_15','C196_16','C196_18','C196_19'}
MODES=('native-01','native-02','public-01')
TOOL_SHA256='387204bdfe5288a967176c46549ec5e9c00b1a26466a9e8bee01846a98237366'
SCOPE='10 selected conditions in one shared batch; two Native modes and one Py mode; not independent case executions'
LIMITATIONS=['Native natural termination was not observed.',
             'The original acceptance record, comparison sheet and original receipts are not included.',
             'Internal argument values are unobserved.',
             'These ordinary-condition observations do not establish behavior for fault conditions or full command compatibility.',
             'History bytes and mode labels retain their separate roles; raw layout differences are not normalized.']
def digest(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        if k in d: raise ValueError('duplicate JSON key')
        d[k]=v
    return d
def load(path): return json.loads(path.read_text(encoding='utf-8-sig'),object_pairs_hook=pairs)
def check(ok, why):
    if not ok: raise ValueError(why)
def run(observation_file,evidence):
    d=load(observation_file); check(d.get('schema')=='normal-observation-c196-v1','schema')
    check(d.get('scope')==SCOPE and d.get('limitations')==LIMITATIONS,'scope or limitations')
    check(d['source_index']=='../multi-group-101-20261117/index.json','index reference')
    group=evidence/'multi-group-101-20261117'; raw=(group/'index.json').read_bytes()
    check(digest(raw)==d['source_index_sha256'],'index SHA')
    index=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=pairs)
    batch=next(x for x in index['batches'] if x.get('group')=='printplain-single-20261113-196')
    check(len(d['cases'])==10,'case count'); seen=set()
    for record in d['cases']:
        cond=record['condition']['id']; check(cond in EXPECTED and cond not in seen,'case ID'); seen.add(cond)
        case=next(c for c in batch['cases'] if cond in c.get('conditions',[]))
        detail=next(x for x in case['selected_condition_details'] if x['id']==cond)
        check(record['case_id']==case['case_id'] and record['target']==case['roles'] and record['condition']==detail,'case mapping')
        check(record['recorded_verdict']==case['verdict'] and record['recorded_comparison_axes']==case['recorded_comparison_axes'],'recorded classification')
        check([x['mode'] for x in record['observations']]==list(MODES),'mode order')
        for obs in record['observations']:
            mode=next(x for x in batch['modes'] if x['mode']==obs['mode'])
            check(obs['engine']==('PyEmuera' if obs['mode']=='public-01' else 'Emuera'),'engine label')
            check(obs['mode_source_record_kind']==mode['receipt_projection']['source_kind'] and obs['mode_source_record_sha256']==mode['receipt_projection']['source_receipt_sha256'],'mode source record binding')
            for role in ('history','fixture','config'):
                asset=next(x for x in mode['assets'] if x.get('role')==role and x.get('status')=='included')
                check(obs[role]=='../multi-group-101-20261117/'+asset['path'] and obs[role+'_sha256']==asset['sha256'],'asset pointer')
                p=group/asset['path']; b=p.read_bytes()
                check(len(b)==asset['size'] and digest(b)==asset['sha256'],'asset integrity')
                if role=='history': history=b
            a,b=obs['byte_span']; check(type(a) is int and type(b) is int and 0<=a<b<=len(history) and a%2==0 and b%2==0,'byte span')
            block=history[a:b].decode('utf-16-le')
            check(block==obs['raw_block'] and block.startswith(cond+'_BEGIN\r\n') and block.endswith(cond+'_END\r\n'),'raw block')
            lines=block.splitlines(); states=[x for x in lines if x.startswith(cond+'_STATE ')]
            check(len(states)==1 and states[0]==obs['state_line'] and obs['encoding']=='utf-16','state line')
    check(seen==EXPECTED,'case set')
    return 'OK: 10 conditions, 30 mode records; integrity only'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--evidence-root',type=pathlib.Path,required=True); p.add_argument('--manifest-sha256',required=True,help='Trusted manifest SHA-256 from an independent source'); p.add_argument('--data',type=pathlib.Path,default=pathlib.Path(__file__).with_name('observations.json')); a=p.parse_args()
    try:
        check(re.fullmatch(r'[0-9a-fA-F]{64}',a.manifest_sha256) is not None,'invalid manifest pin')
        manifest=a.data.parent/'manifest.json'
        check(digest(manifest.read_bytes())==a.manifest_sha256.lower(),'manifest pin mismatch')
        tool=a.evidence_root.parent/'tools/file_set_manifest.py'
        check(tool.is_file() and not tool.is_symlink() and digest(tool.read_bytes())==TOOL_SHA256,'verification tool unavailable or inconsistent')
        spec=importlib.util.spec_from_file_location('normal_manifest_verifier',tool)
        verifier=importlib.util.module_from_spec(spec)
        old=sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode=True; spec.loader.exec_module(verifier)
        finally: sys.dont_write_bytecode=old
        verifier.verify(manifest,{'evidence':a.data.parent})
        print(run(a.data,a.evidence_root))
    except (ValueError,KeyError,StopIteration,IndexError,TypeError,OSError,UnicodeError):
        print('FAIL: evidence or verification tool is unavailable or inconsistent',file=sys.stderr); return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
