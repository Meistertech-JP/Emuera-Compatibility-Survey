"""Single offline verifier for a batch of grammar and supplemental evidence."""
import argparse,collections,hashlib,json,pathlib,re,sys

TRUSTED_CONTRACT_SHA256='e86f4f6f6874c114fd8eff5f513ae14ad7924153134297071a35ab5458d914ae'
ANCILLARY={'bindings.json','contract.json','verify.py','negative_checks.py','README.md','README.ja.md',
           'LICENSES/README.md','LICENSES/README.ja.md','LICENSES/Emuera1824-v24-license-original.txt',
           'LICENSES/PyEmuera-3.0.0-LICENSE.txt','LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md',
           'vendor/emuera/NOTICE.en.md','vendor/emuera/NOTICE.ja.md'}

def digest(b):return hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    def invalid(value):raise ValueError('non-finite JSON: '+value)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid)
def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def at(obj,pointer):
    for part in pointer.lstrip('/').split('/') if pointer else []:
        key=part.replace('~1','/').replace('~0','~')
        if isinstance(obj,dict):
            if key not in obj:return False,None
            obj=obj[key]
        elif isinstance(obj,list):
            try:obj=obj[int(key)]
            except (ValueError,IndexError):return False,None
        else:return False,None
    return True,obj
def file(root,name):
    need(isinstance(name,str) and name and '\\' not in name and ':' not in name,'unsafe path')
    p=pathlib.PurePosixPath(name);need(not p.is_absolute() and p.as_posix()==name and '..' not in p.parts,'unsafe path')
    q=root.joinpath(*p.parts);need(q.resolve().is_relative_to(root) and q.is_file() and not q.is_symlink(),'missing or unsafe: '+name);return q
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent);p.add_argument('--manifest-sha',required=True);p.add_argument('--bindings-sha',required=True);p.add_argument('--contract-sha',required=True);p.add_argument('--verifier-sha',required=True);a=p.parse_args();root=a.root.resolve()
    need(pathlib.Path(__file__).resolve()==(root/'verify.py').resolve(),'wrong verifier location')
    need(digest(file(root,'verify.py').read_bytes())==a.verifier_sha.lower(),'verifier pin mismatch')
    raw=file(root,'manifest.json').read_bytes();mh=digest(raw);need(mh==a.manifest_sha.lower(),'manifest pin mismatch')
    need(file(root,'manifest.sha256').read_bytes()==(mh+'  manifest.json\n').encode('ascii'),'checksum mismatch')
    m=strict_json(raw);bb=file(root,'bindings.json').read_bytes();need(digest(bb)==a.bindings_sha.lower(),'bindings pin mismatch');bind=strict_json(bb)
    cb=file(root,'contract.json').read_bytes();need(digest(cb)==a.contract_sha.lower()==TRUSTED_CONTRACT_SHA256,'trusted contract pin mismatch');contract=strict_json(cb)
    need(type(m) is dict and set(m)=={'schema','scope','limits','cases','files'} and type(m['cases']) is list and type(m['files']) is list,'manifest structure')
    for entry in m['files']:
        need(type(entry) is dict and set(entry)=={'path','sha256','size'} and type(entry['path']) is str and type(entry['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}',entry['sha256']) is not None and type(entry['size']) is int and entry['size']>=0,'file entry type')
    need(m['schema']=='common-grammar-supplemental-evidence-v3' and bind['schema']=='common-evidence-bindings-v1' and contract['schema']=='common-evidence-trusted-contract-v2','schema')
    byid={x['key']:x for x in m['cases']};bound={x['key']:x for x in bind['cases']};need(len(byid)==len(m['cases']) and len(bound)==len(bind['cases']),'duplicate case');need(set(byid)==set(bound),'case set mismatch')
    trusted={x['key']:x for x in contract['cases']};need(len(trusted)==len(contract['cases'])==24 and set(byid)==set(trusted),'trusted case population mismatch')
    need(type(contract['case_count']) is int and contract['case_count']==24,'trusted count mismatch')
    need(dict(collections.Counter(c['family'] for c in byid.values()))==contract['family_counts']=={'colon_grammar':16,'supplemental_label':8},'trusted family counts')
    need(digest(canonical(m['scope']))==contract['scope_sha256'] and digest(canonical(m['limits']))==contract['limits_sha256'],'scope contract mismatch')
    paths={}
    for k,c in byid.items():
        t=trusted[k]
        for rule in t['unobserved_required']:
            present,value=at(c,rule['pointer']);expected=rule['value'];kind={'boolean':bool,'string':str}[rule['type']]
            need(present and type(value) is kind and type(expected) is kind and value==expected,'unobserved/type contract mismatch: '+k+rule['pointer'])
        for pointer in t['unobserved_forbidden']:
            present,_=at(c,pointer);need(not present,'unobserved field fabricated: '+k+pointer)
        need(digest(canonical(c))==t['case_content_sha256'],'typed case contract mismatch: '+k)
        need(digest(canonical(bound[k]))==t['binding_content_sha256'],'trusted binding contract mismatch: '+k)
        b=bound[k];need(c['family']==b['family'] and c['case_id']==b['case_id'] and c['source_case_id']==b['source_case_id'] and c['parent_ids']==b['parent_ids'],'case or parent substitution')
        need(set(c['runs'])==set(b['runs'])=={'native-01','native-02','public-01'},'mode set')
        for mode,run in c['runs'].items():
            br=b['runs'][mode];need(run['mode']==mode and run['identity_basis']==br['identity_basis'],'mode identity')
            prefix='assets/'+c['family']+'/'+c['case_id']+'/'+mode+'/'
            for role in ('raw','stderr','receipt'):
                expected=prefix+('receipt.json' if role=='receipt' else role+'.bin')
                need(run[role]==br[role]['path']==expected,'role path mismatch');paths[run[role]]=br[role]['sha256']
            inputs={i['name']:i['path'] for i in run['inputs']};need(len(inputs)==len(run['inputs']),'duplicate inputs');need(set(inputs)==set(br['inputs']),'input set')
            for name,path in inputs.items():
                need(path==br['inputs'][name]['path']==prefix+'input/'+name,'input role mismatch');paths[path]=br['inputs'][name]['sha256']
    need(len(paths)==sum(3+len(x['inputs']) for c in byid.values() for x in c['runs'].values()),'role paths not unique')
    entries={e['path']:e for e in m['files']};need(len(entries)==len(m['files']),'duplicate listed file')
    expected=set(paths)|ANCILLARY;need(set(entries)==expected,'manifest file set mismatch')
    actual=set()
    for q in root.rglob('*'):
        need(not q.is_symlink(),'symlink forbidden')
        if q.is_file():actual.add(q.relative_to(root).as_posix())
    need(actual==expected|{'manifest.json','manifest.sha256'},'bundle file set mismatch')
    for name,e in entries.items():
        data=file(root,name).read_bytes();need(len(data)==e['size'] and digest(data)==e['sha256'],'artifact hash mismatch: '+name)
        if name in paths:need(digest(data)==paths[name],'role binding hash mismatch: '+name)
    for c in byid.values():
        for mode,run in c['runs'].items():
            receipt=strict_json(file(root,run['receipt']).read_bytes());before=receipt.get('inputs_before',{});after=receipt.get('inputs_after',{})
            need(canonical(before)==canonical(after) and set(before)=={x['name'] for x in run['inputs']},'receipt input set mismatch')
            for item in run['inputs']:need(before[item['name']]==digest(file(root,item['path']).read_bytes()),'receipt input hash mismatch')
            if 'mode' in receipt:need(receipt['mode']==mode,'receipt mode mismatch')
            if 'case_id' in receipt:need(receipt['case_id']==c['source_case_id'],'receipt case mismatch')
            if 'fixture' in receipt:need(receipt['fixture']==c['source_case_id'],'receipt fixture mismatch')
    print('PASS: '+str(len(byid))+' cases, '+str(sum(len(c['runs']) for c in byid.values()))+' saved modes; no engine execution.')
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,OSError,UnicodeError,TypeError,json.JSONDecodeError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
