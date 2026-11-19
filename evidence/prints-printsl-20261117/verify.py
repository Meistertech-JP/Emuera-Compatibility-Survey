"""Verify a bounded saved-observation bundle against independently obtained pins."""
import argparse
import hashlib
import json
import pathlib
import re
import sys

ROLE_BINDINGS_SHA256 = '45d16c506754761144467b42b635b7a3eb8637dfdd5cb435b490443737f139b5'
FIXTURES = {'PRINTS':'d5c54374f9de7708330f51619fe30600e284c25a2e121ef76239671886ef2059',
            'PRINTSL':'3c6c2d80371b06d122619b6a37ae5422f05d594223f214ad17a1d3037023cadc'}
CONFIG = 'f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc'
MODES = ('native-01','native-02','public-01')
ANCILLARY = {'verify.py','negative_checks.py','README.md','README.ja.md','role-bindings.json',
             'LICENSES/README.md','LICENSES/README.ja.md',
             'LICENSES/Emuera1824-v24-license-original.txt','LICENSES/PyEmuera-3.0.0-LICENSE.txt',
             'LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md',
             'vendor/emuera/NOTICE.en.md','vendor/emuera/NOTICE.ja.md'}

def require(ok, message):
    if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def expected_roles(name, mode):
    base=f'cases/{name}/{mode}/'
    roles={'fixture':base+'input/ERB/MAIN.ERB','config':base+'input/emuera.config',
           'raw':base+'observation/raw.bin','stderr':base+'observation/stderr.bin','receipt':base+'receipt.json'}
    if mode.startswith('native'): roles['probe']=base+'probe.json'
    return roles
def resolve(root,name):
    require(isinstance(name,str) and bool(name) and '\\' not in name and ':' not in name, 'unsafe path')
    p=pathlib.PurePosixPath(name)
    require(not p.is_absolute() and p.as_posix()==name and all(x not in ('','.','..') for x in p.parts), 'unsafe path')
    dest=root.joinpath(*p.parts)
    require(dest.resolve().is_relative_to(root), 'outside bundle')
    require(dest.is_file() and not dest.is_symlink(), 'missing: '+name)
    return dest
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--manifest-sha',required=True,help='manifest SHA-256 supplied by an independent trust channel')
    parser.add_argument('--verifier-sha',required=True,help='verifier SHA-256 supplied by an independent trust channel')
    args=parser.parse_args();root=args.root.resolve()
    require(pathlib.Path(__file__).resolve()==(root/'verify.py').resolve(), 'verifier must belong to bundle')
    require(sha(resolve(root,'verify.py').read_bytes())==args.verifier_sha.lower(),'verifier digest mismatch')
    content=resolve(root,'manifest.json').read_bytes();manifest_sha=sha(content)
    require(manifest_sha==args.manifest_sha.lower(),'manifest digest mismatch')
    checksum=resolve(root,'manifest.sha256').read_bytes()
    require(checksum==(manifest_sha+'  manifest.json\n').encode('ascii'),'manifest.sha256 mismatch')
    m=json.loads(content);require(m['schema']=='prints-printsl-private-evidence-bundle-v2','schema')
    role_paths={}
    for name in FIXTURES:
        for mode in MODES:
            for role,path in expected_roles(name,mode).items():role_paths[(name,mode,role)]=path
    expected_files=set(role_paths.values())|ANCILLARY
    entries=m['files']; names=[e['path'] for e in entries]
    require(len(names)==len(set(names)),'duplicate listed path')
    require(set(names)==expected_files,'manifest file set mismatch')
    found=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink forbidden')
        if p.is_file():found.add(p.relative_to(root).as_posix())
    require(found==expected_files|{'manifest.json','manifest.sha256'},'bundle file set mismatch')
    data={}
    for e in entries:
        raw=resolve(root,e['path']).read_bytes()
        require(len(raw)==e['size'] and sha(raw)==e['sha256'],'artifact mismatch: '+e['path'])
        data[e['path']]=raw
    require(sha(data['role-bindings.json'])==ROLE_BINDINGS_SHA256,'role bindings trust pin mismatch')
    bindings=json.loads(data['role-bindings.json'])
    require(bindings['schema']=='prints-printsl-recorded-role-bindings-v1','role binding schema')
    keyed={}
    for item in bindings['bindings']:
        key=(item['target'],item['mode'],item['role'])
        require(key not in keyed,'duplicate role binding');keyed[key]=item
    require(set(keyed)==set(role_paths),'role binding set mismatch')
    for key,path in role_paths.items():
        item=keyed[key]
        require(item['path']==path,'trusted role path mismatch')
        require(sha(data[path])==item['artifact_sha256'],'trusted role digest mismatch')
    require(set(m['cases'])==set(FIXTURES),'target set')
    for name,c in m['cases'].items():
        require(c['target']=={'kind':'command_or_syntax','name':name},'typed target')
        case_id='PRINTS_CURRENT_'+name+'_COUNTED_SKIP_20261116'
        require(c['case_id']==case_id and c['source_case_id']==name+'_COUNTED_SKIP','case substitution')
        require(case_id in c['acceptance']['case_ids'],'acceptance case link')
        require(c['acceptance']['comparison_outcome']=='matched_in_finite_scope','acceptance outcome')
        require(c['comparison']['scenario_verdict']=='matched_scoped' and c['comparison']['selected_outputs_and_state_equal'] is True,'comparison')
        require(set(c['runs'])==set(MODES),'mode set')
        markers=selected=None
        for mode in MODES:
            run=c['runs'][mode];require(run['case_id']==name+'_COUNTED_SKIP' and run['mode']==mode,'attempt identity')
            paths=expected_roles(name,mode)
            for role,path in paths.items():require(run.get(role)==path,'mode role path mismatch: '+name+'/'+mode+'/'+role)
            if mode=='public-01':require('probe' not in run and run.get('probe_status')=='not present in retained public run; not inferred','public probe status')
            fixture=data[paths['fixture']];config=data[paths['config']]
            require(sha(fixture)==FIXTURES[name] and sha(config)==CONFIG,'fixture or config mismatch')
            require(re.search(r'^'+name+r' ZZS\(',fixture.decode('utf-8-sig'),re.MULTILINE) is not None,'fixture command')
            receipt=json.loads(data[paths['receipt']]);require(receipt['case_id']==name+'_COUNTED_SKIP' and receipt['mode']==mode,'receipt identity')
            for phase in ('inputs_before','inputs_after'):
                require(receipt[phase]['ERB/MAIN.ERB']==sha(fixture) and receipt[phase]['emuera.config']==sha(config),'receipt input binding')
            require(receipt['pyz_before'] and receipt['pyz_before']==receipt['pyz_after'] and receipt['returncode']==0,'runner pin/result')
            enc='utf-16' if mode.startswith('native') else 'cp932';require(run['raw_encoding']==enc,'encoding')
            lines=data[paths['raw']].decode(enc).splitlines()
            for group in ('markers','selected_output_lines'):
                require(all(s in lines for s in run[group]),'observation absent: '+group)
                pos=[lines.index(s) for s in run[group]];require(pos==sorted(pos),'observation ordering: '+group)
            if markers is None:markers,selected=run['markers'],run['selected_output_lines']
            else:require(markers==run['markers'] and selected==run['selected_output_lines'],'cross-run comparison')
            if mode.startswith('native'):
                probe=json.loads(data[paths['probe']]);require(probe['fixture_sha256']==sha(fixture) and probe['config_sha256']==sha(config),'probe input')
                require(receipt['native_before'] and receipt['native_before']==receipt['native_after']==probe['native_exe_sha256'],'native engine pin')
                require(probe['exit_code_observed'] is False and probe['exit_code'] is None and probe['process_exited_after_5s'] is False,'native exit unobserved')
    print(f'PASS: {len(expected_files)+2} exact files; 34 role paths; 2 targets, 2 cases, 6 saved runs. No engine executed.')
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,UnicodeError,TypeError,json.JSONDecodeError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
