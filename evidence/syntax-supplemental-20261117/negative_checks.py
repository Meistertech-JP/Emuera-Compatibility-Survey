"""Reproduce the independent review mutations on one disposable copy."""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,tempfile

def sha(b):return hashlib.sha256(b).hexdigest()
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
p=argparse.ArgumentParser();p.add_argument('--manifest-sha',required=True);p.add_argument('--bindings-sha',required=True);p.add_argument('--contract-sha',required=True);p.add_argument('--verifier-sha',required=True);a=p.parse_args()
src=pathlib.Path(__file__).resolve().parent
def invoke(root,mh,bh,ch):
    return subprocess.run([sys.executable,'-I','-B',str(root/'verify.py'),'--manifest-sha',mh,'--bindings-sha',bh,'--contract-sha',ch,'--verifier-sha',a.verifier_sha],capture_output=True,text=True)
baseline=invoke(src,a.manifest_sha,a.bindings_sha,a.contract_sha)
if baseline.returncode:raise SystemExit('baseline failed: '+baseline.stderr)
scenarios={
 'swap_both_cases_all_modes_reseal':'typed case contract mismatch',
 'unobserved_false_reseal':'unobserved/type contract mismatch',
 'unobserved_integer_reseal':'unobserved/type contract mismatch',
 'fabricated_post_error_state_reseal':'unobserved field fabricated',
 'case_and_assets_removed_reseal':'trusted case population mismatch',
 'grammar_unknown_fabricated_reseal':'unobserved/type contract mismatch',
 'other_boolean_changed_to_integer_reseal':'typed case contract mismatch',
 'mode_raw_paths_swapped_both_reseal':'typed case contract mismatch',
 'contract_replaced_and_repinned':'trusted contract pin mismatch',
 'zero_size_changed_to_boolean_reseal':'file entry type',
 'missing_file':'bundle file set mismatch',
 'extra_file':'bundle file set mismatch',
 'wrong_external_manifest_pin':'manifest pin mismatch',
}
results=[]
with tempfile.TemporaryDirectory(prefix='review-negative-',dir=src.parent) as td:
    root=pathlib.Path(td)/'bundle';shutil.copytree(src,root)
    mp=root/'manifest.json';bp=root/'bindings.json';cp=root/'contract.json';sp=root/'manifest.sha256'
    originals={q:q.read_bytes() for q in (mp,bp,cp,sp)}
    def persist(m,b,contract=None):
        bh=sha(enc(b));bp.write_bytes(enc(b));entry=next(x for x in m['files'] if x['path']=='bindings.json');entry.update({'sha256':bh,'size':len(enc(b))})
        ch=a.contract_sha
        if contract is not None:
            data=enc(contract);cp.write_bytes(data);ch=sha(data);entry=next(x for x in m['files'] if x['path']=='contract.json');entry.update({'sha256':ch,'size':len(data)})
        data=enc(m);mp.write_bytes(data);mh=sha(data);sp.write_bytes((mh+'  manifest.json\n').encode('ascii'));return mh,bh,ch
    for label,reason in scenarios.items():
        for q,data in originals.items():q.write_bytes(data)
        m=json.loads(originals[mp]);b=json.loads(originals[bp]);mh,bh,ch=a.manifest_sha,a.bindings_sha,a.contract_sha;removed={};extra=None
        no=next(x for x in m['cases'] if x['source_case_id']=='at-duplicate-NO');yes=next(x for x in m['cases'] if x['source_case_id']=='at-duplicate-YES')
        bn=next(x for x in b['cases'] if x['key']==no['key']);by=next(x for x in b['cases'] if x['key']==yes['key'])
        if label=='swap_both_cases_all_modes_reseal':
            no['runs'],yes['runs']=yes['runs'],no['runs'];bn['runs'],by['runs']=by['runs'],bn['runs'];mh,bh,ch=persist(m,b)
        elif label in ('unobserved_false_reseal','unobserved_integer_reseal','fabricated_post_error_state_reseal'):
            obs=no['runs']['native-01']['observed']
            if label=='unobserved_false_reseal':obs['no_post_error_state']=False
            elif label=='unobserved_integer_reseal':obs['no_post_error_state']=1
            else:obs['post_error_state']=123
            mh,bh,ch=persist(m,b)
        elif label=='case_and_assets_removed_reseal':
            paths=set()
            for run in no['runs'].values():
                paths.update(run[r] for r in ('raw','stderr','receipt'));paths.update(x['path'] for x in run['inputs'])
            if len(paths)!=15:raise SystemExit('unexpected label asset count')
            for name in paths:
                q=root/name;removed[q]=q.read_bytes();q.unlink()
            m['cases']=[x for x in m['cases'] if x['key']!=no['key']];b['cases']=[x for x in b['cases'] if x['key']!=no['key']];m['files']=[x for x in m['files'] if x['path'] not in paths];mh,bh,ch=persist(m,b)
        elif label=='grammar_unknown_fabricated_reseal':
            g=next(x for x in m['cases'] if x['family']=='colon_grammar');g['source_context']['postfatal_unprinted_state']='KNOWN';mh,bh,ch=persist(m,b)
        elif label=='other_boolean_changed_to_integer_reseal':
            g=next(x for x in m['cases'] if x['family']=='colon_grammar' and x['runs']['native-01']['observed']['setup_binding_valid'] is True);g['runs']['native-01']['observed']['setup_binding_valid']=1;mh,bh,ch=persist(m,b)
        elif label=='mode_raw_paths_swapped_both_reseal':
            g=next(x for x in m['cases'] if x['family']=='colon_grammar');gb=next(x for x in b['cases'] if x['key']==g['key']);x=g['runs'];y=gb['runs'];x['native-01']['raw'],x['native-02']['raw']=x['native-02']['raw'],x['native-01']['raw'];y['native-01']['raw'],y['native-02']['raw']=y['native-02']['raw'],y['native-01']['raw'];mh,bh,ch=persist(m,b)
        elif label=='contract_replaced_and_repinned':
            contract=json.loads(originals[cp]);contract['case_count']=23;mh,bh,ch=persist(m,b,contract)
        elif label=='zero_size_changed_to_boolean_reseal':
            entry=next(x for x in m['files'] if type(x['size']) is int and x['size']==0);entry['size']=False;mh,bh,ch=persist(m,b)
        elif label=='missing_file':
            q=root/no['runs']['native-01']['raw'];removed[q]=q.read_bytes();q.unlink()
        elif label=='extra_file':extra=root/'unexpected.txt';extra.write_bytes(b'extra\n')
        else:mh='0'*64
        z=invoke(root,mh,bh,ch)
        if z.returncode==0 or reason not in z.stderr:raise SystemExit('unexpected result '+label+': '+z.stderr)
        results.append({'test':label,'expected_rejection':reason,'returncode':z.returncode,'diagnostic':z.stderr.strip()})
        for q,data in removed.items():q.write_bytes(data)
        if extra:extra.unlink()
    for q,data in originals.items():q.write_bytes(data)
    m=json.loads(originals[mp]);g=next(x for x in m['cases'] if x['family']=='colon_grammar');r1=g['runs']['native-01'];r2=g['runs']['native-02'];name='emuera.config';f1=root/next(x['path'] for x in r1['inputs'] if x['name']==name);f2=root/next(x['path'] for x in r2['inputs'] if x['name']==name);one,two=f1.read_bytes(),f2.read_bytes()
    if one!=two:raise SystemExit('identical-byte control requires equal inputs')
    f1.write_bytes(two);f2.write_bytes(one);z=invoke(root,a.manifest_sha,a.bindings_sha,a.contract_sha)
    if z.returncode:raise SystemExit('identical-byte control failed: '+z.stderr)
    results.append({'test':'identical_bytes_control','returncode':0,'meaning':'identical byte replacement cannot establish original execution identity'})
print(json.dumps(results,ensure_ascii=False,indent=2))
