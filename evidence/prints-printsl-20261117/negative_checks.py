"""Reproduce the review findings and test the corresponding rejections."""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

def digest(data):return hashlib.sha256(data).hexdigest()
def write_manifest(root,m):
    raw=(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    (root/'manifest.json').write_bytes(raw);h=digest(raw)
    (root/'manifest.sha256').write_bytes((h+'  manifest.json\n').encode('ascii'))
    return h
def invoke(root,mh,vh):
    return subprocess.run([sys.executable,'-B',str(root/'verify.py'),'--root',str(root),'--manifest-sha',mh,'--verifier-sha',vh],capture_output=True,text=True)

p=argparse.ArgumentParser();p.add_argument('--manifest-sha',required=True);p.add_argument('--verifier-sha',required=True);args=p.parse_args()
source=pathlib.Path(__file__).resolve().parent
baseline=invoke(source,args.manifest_sha,args.verifier_sha)
if baseline.returncode:raise SystemExit('baseline failed: '+baseline.stderr)
scenarios={
 'mode_raw_reference_swap_repin':'mode role path mismatch',
 'cross_case_raw_reference_swap_repin':'mode role path mismatch',
 'extra_unlisted_file':'bundle file set mismatch',
 'extra_listed_file_repin':'manifest file set mismatch',
 'missing_listed_file':'bundle file set mismatch',
 'manifest_sha256_tamper':'manifest.sha256 mismatch',
 'wrong_external_manifest_pin':'manifest digest mismatch',
 'wrong_external_verifier_pin':'verifier digest mismatch',
 'manifest_tamper':'manifest digest mismatch',
 'raw_byte_tamper':'artifact mismatch',
 'case_id_swap_repin':'case substitution',
 'fixture_substitution_repin':'trusted role digest mismatch',
 'role_bindings_swap_repin':'role bindings trust pin mismatch',
}
for role in ('fixture','config','stderr','receipt','probe'):
    scenarios['mode_'+role+'_reference_swap_repin']='mode role path mismatch'
out=[]
with tempfile.TemporaryDirectory(prefix='negative-checks-',dir=source.parent) as tmp:
    for label,reason in scenarios.items():
        dest=pathlib.Path(tmp)/label;shutil.copytree(source,dest)
        path=dest/'manifest.json';m=json.loads(path.read_text(encoding='utf-8'));mh=args.manifest_sha;vh=args.verifier_sha
        one=m['cases']['PRINTS']['runs']['native-01'];two=m['cases']['PRINTS']['runs']['native-02']
        if label=='mode_raw_reference_swap_repin':
            one['raw'],two['raw']=two['raw'],one['raw'];mh=write_manifest(dest,m)
        elif label=='cross_case_raw_reference_swap_repin':
            other=m['cases']['PRINTSL']['runs']['native-01'];one['raw'],other['raw']=other['raw'],one['raw'];mh=write_manifest(dest,m)
        elif label in ('extra_unlisted_file','extra_listed_file_repin'):
            (dest/'unexpected.txt').write_text('unlisted\n',encoding='utf-8')
            if label=='extra_listed_file_repin':
                data=(dest/'unexpected.txt').read_bytes();m['files'].append({'path':'unexpected.txt','size':len(data),'sha256':digest(data)});mh=write_manifest(dest,m)
        elif label=='missing_listed_file':(dest/one['receipt']).unlink()
        elif label=='manifest_sha256_tamper':(dest/'manifest.sha256').write_text('0'*64+'  manifest.json\n',encoding='ascii')
        elif label=='wrong_external_manifest_pin':mh='0'*64
        elif label=='wrong_external_verifier_pin':vh='0'*64
        elif label=='manifest_tamper':path.write_bytes(path.read_bytes()+b' ')
        elif label=='raw_byte_tamper':
            raw=dest/one['raw'];raw.write_bytes(raw.read_bytes()+b'X')
        elif label=='case_id_swap_repin':
            m['cases']['PRINTS']['case_id']=m['cases']['PRINTSL']['case_id'];mh=write_manifest(dest,m)
        elif label=='fixture_substitution_repin':
            target=one['fixture'];foreign=m['cases']['PRINTSL']['runs']['native-01']['fixture'];raw=(dest/foreign).read_bytes();(dest/target).write_bytes(raw)
            entry=next(x for x in m['files'] if x['path']==target);entry['sha256']=digest(raw);entry['size']=len(raw);mh=write_manifest(dest,m)
        elif label=='role_bindings_swap_repin':
            bp=dest/'role-bindings.json';r=json.loads(bp.read_text(encoding='utf-8'));a=next(x for x in r['bindings'] if x['target']=='PRINTS' and x['mode']=='native-01' and x['role']=='raw');b=next(x for x in r['bindings'] if x['target']=='PRINTS' and x['mode']=='native-02' and x['role']=='raw');a['path'],b['path']=b['path'],a['path']
            raw=(json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8');bp.write_bytes(raw);entry=next(x for x in m['files'] if x['path']=='role-bindings.json');entry['sha256']=digest(raw);entry['size']=len(raw);mh=write_manifest(dest,m)
        elif label.startswith('mode_') and label.endswith('_reference_swap_repin'):
            role=label[len('mode_'):-len('_reference_swap_repin')]
            one[role],two[role]=two[role],one[role];mh=write_manifest(dest,m)
        result=invoke(dest,mh,vh)
        if result.returncode==0 or reason not in result.stderr:raise SystemExit('wrong negative outcome '+label+': '+result.stderr)
        out.append({'test':label,'expected_rejection':reason,'returncode':result.returncode,'diagnostic':result.stderr.strip()})
    # Byte-identical file replacement is intentionally an indistinguishable control.
    dest=pathlib.Path(tmp)/'identical_bytes_control';shutil.copytree(source,dest)
    m=json.loads((dest/'manifest.json').read_text(encoding='utf-8'));a=dest/m['cases']['PRINTS']['runs']['native-01']['raw'];b=dest/m['cases']['PRINTS']['runs']['native-02']['raw']
    first=a.read_bytes();second=b.read_bytes()
    if first!=second:raise SystemExit('control setup: raw bytes differ')
    a.write_bytes(second);b.write_bytes(first);result=invoke(dest,args.manifest_sha,args.verifier_sha)
    if result.returncode:raise SystemExit('identical-byte control unexpectedly rejected: '+result.stderr)
    out.append({'test':'identical_bytes_control','expected':'PASS; bytes alone cannot prove separate execution identity','returncode':result.returncode,'diagnostic':result.stdout.strip()})
print(json.dumps(out,ensure_ascii=False,indent=2))
