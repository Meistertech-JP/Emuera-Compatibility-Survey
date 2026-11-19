#!/usr/bin/env python3
"""Verify the external manifest pin, file inventory, and condition/mode bindings."""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent
MODES=('native-01','native-02','public-01')
CASE_BINDINGS_SHA256='c8e4ee585dd9c2310ab915da8da5489226d7735b4cfb930d652fb46b22db2463'
def need(value,message):
    if not value: raise ValueError(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def readjson(p):
    def pairs(xs):
        d={}
        for k,v in xs:
            need(k not in d,'duplicate JSON key'); d[k]=v
        return d
    return json.loads(p.read_text(encoding='utf8'),object_pairs_hook=pairs)
def safe(root,path):
    x=PurePosixPath(path)
    need(not x.is_absolute() and all(p not in ('..','.') for p in x.parts) and '\\' not in path,'unsafe path')
    p=root.joinpath(*x.parts)
    for c in [p,*p.parents]:
        if c==root.parent: break
        need(not c.is_symlink(),'symlink')
    need(p.is_file(),'missing file '+path)
    return p
def text(p):
    b=p.read_bytes()
    if b.startswith(b'\xff\xfe'): s=b.decode('utf-16')
    else:
        try: s=b.decode('utf-8-sig')
        except UnicodeDecodeError: s=b.decode('cp932')
    return s.replace('\r\n','\n')
def verify(peer,tool,pin,peer_pin,tool_pin):
    manifest=ROOT/'manifest.json'
    need(re.fullmatch('[0-9a-f]{64}',pin or '') is not None,'external pin required')
    need(digest(manifest)==pin,'external pin mismatch')
    need(re.fullmatch('[0-9a-f]{64}',peer_pin or '') is not None,'external peer pin required')
    need(re.fullmatch('[0-9a-f]{64}',tool_pin or '') is not None,'external tool pin required')
    need(tool.is_file() and not tool.is_symlink() and digest(tool)==tool_pin,'external tool pin mismatch')
    peer_manifest=peer/'file-set-manifest.json'
    need(digest(peer_manifest)==peer_pin,'external peer pin mismatch')
    p=subprocess.run([sys.executable,'-B',str(tool),'verify','--manifest',str(manifest),'--root','bundle='+str(ROOT)],capture_output=True,text=True)
    need(p.returncode==0,'file inventory failed')
    p=subprocess.run([sys.executable,'-B',str(tool),'verify','--manifest',str(peer_manifest),'--root','evidence='+str(peer)],capture_output=True,text=True)
    need(p.returncode==0,'peer file inventory failed')
    binding_file=ROOT/'case-bindings.json'
    need(digest(binding_file)==CASE_BINDINGS_SHA256,'case bindings pin mismatch')
    bindings=readjson(binding_file); need(bindings['schema']=='find-element-case-bindings.v1','case binding schema')
    d=readjson(ROOT/'conditions.json'); need(d['schema']=='find-element-observations.v2','schema')
    fs={x['id']:x for x in d['fixtures']}; cs=d['conditions']
    need(len(d['fixtures'])==len(fs)==61 and len(cs)==len(bindings['cases'])==64 and [x['id'] for x in cs]==[f'C{i:03d}' for i in range(1,65)],'profile count or IDs')
    need(len({x['source_marker'] for x in cs})==64,'duplicate marker')
    peer_data=peer/'data'; peer_case=d['peer_case']
    cases=[json.loads(x) for x in (peer_data/'cases.jsonl').read_text(encoding='utf8').splitlines()]
    pc=[x for x in cases if x['case_id']==peer_case]; need(len(pc)==1,'peer case')
    modes={x['mode_id']:x for x in map(json.loads,(peer_data/'modes.jsonl').read_text(encoding='utf8').splitlines())}
    pms={m:modes[pc[0]['modes'][m]['mode_id']] for m in MODES}
    used=set()
    def ref(x, expected, mode=None, rel=None):
        need(type(x) is dict and set(x)=={'root','path','sha256','size'} and type(x['size']) is int,'reference fields or size type')
        if x['root']=='bundle':
            need(x['path']==expected,'fixture/mode/role path mismatch')
            p=safe(ROOT,x['path'])
        else:
            need(x['root']=='peer' and mode in MODES,'unexpected peer reference')
            pm=pms[mode]; need(pm['mode']==mode and pm['fixture_id']=='R0_BAD_EMPTY','peer mode binding')
            r=pm['raw'] if rel is None else next(q for q in pm['inputs'] if q['relative_name']==rel)
            need(x['path']==r['path'] and x['sha256']==r['sha256'],'peer reference binding')
            p=safe(peer_data,x['path'])
        need(p.stat().st_size==x['size'] and digest(p)==x['sha256'],'file pin mismatch')
        return p
    for c, binding in zip(cs,bindings['cases']):
        need(all(c[k]==binding[k] for k in ('id','source_marker','registered_case_id','fixture','target')),'case binding mismatch')
        need([m['mode'] for m in binding['modes']]==list(MODES),'bound mode order mismatch')
        f=c['fixture']; used.add(f); need(f in fs,'missing fixture')
        fix=fs[f]; marker=c['source_marker']; inputs=fix['inputs']; need(fix['csv_files']==[],'CSV assumption')
        for rel in ('ERB/MAIN.ERB','emuera.config'):
            ref(inputs[rel],f'fixtures/{f}/{rel}','native-01',rel)
        erb=text(ref(inputs['ERB/MAIN.ERB'],f'fixtures/{f}/ERB/MAIN.ERB','native-01','ERB/MAIN.ERB'))
        need('BEFORE '+marker in erb and c['target']['name'] in erb,'fixture lacks marker/target')
        need(c['target']['kind'] in ('expression_function','method_as_command') and c['target']['name'] in ('FINDELEMENT','FINDLASTELEMENT'),'typed target')
        condition=c['condition']; target=c['target']; kind=target['kind']
        need(type(condition) is dict and all(type(condition[k]) is int for k in ('start','end','selector','size')) and type(condition['gate']) is bool,'condition types')
        comparison=c['recorded_comparison']
        need(type(comparison) is dict and all(type(comparison[k]) is bool for k in ('native2_consistent','same_return_or_error_class','same_helper_order','same_diagnostic_text')),'comparison types')
        need(target['form']==('EXPR' if kind=='expression_function' else 'CMD'),'target form mismatch')
        segment=erb.split('PRINTL BEFORE '+marker+'\n',1)[1].split('PRINTFORML AFTER '+marker,1)[0]
        expected=('ZZFSOUT = '+target['name']+'(' if kind=='expression_function' else target['name']+' ZZFSARR,')
        need(expected in segment,'fixture invocation mismatch')
        need('#DIMS ZZFSARR,'+str(condition['size']) in erb and len(condition['array'])==condition['size'],'array size')
        for i,v in enumerate(condition['array']):
            need(re.search(r'^ZZFSARR:'+str(i)+r'\s*=\s*'+re.escape(v)+r'\s*$',erb,re.M) is not None,'fixture array mismatch')
        for slot,field in ((2,'pattern'),(3,'start'),(4,'end'),(5,'selector')):
            helper=re.search(r'PRINTFORML ARG '+re.escape(marker)+r' SLOT='+str(slot)+r' COUNT=\{A\} ORDER=\{B\}\s*\nRETURNF ([^\n\r]*)',erb)
            need(helper is not None,'fixture helper absent')
            value=helper.group(1).strip()
            want='"'+condition[field]+'"' if slot==2 else str(condition[field])
            need(value==want,'fixture helper condition mismatch')
        need([x['mode'] for x in c['observations']]==list(MODES),'mode order or membership')
        for o, bound_mode in zip(c['observations'],binding['modes']):
            mode=o['mode']; need(o['fixture']==f,'mode fixture mismatch')
            need(mode==bound_mode['mode'] and json.dumps(o['termination'],sort_keys=True,ensure_ascii=False)==json.dumps(bound_mode['termination'],sort_keys=True,ensure_ascii=False),'termination binding mismatch')
            need(type(o['condition_marker_observed']) is bool,'condition marker type')
            if mode=='public-01': need(type(o['termination']) is dict and type(o['termination']['process_returncode']) is int,'public termination type')
            if mode.startswith('native'):
                t=o['termination'];need(t=={'exit_observed':False,'exit_code':None,'exited_after_5s':False,'cleanup_terminate_ok':True} and type(t['exit_observed']) is bool and type(t['exited_after_5s']) is bool and type(t['cleanup_terminate_ok']) is bool,'native termination mismatch')
            rname='emuera.log' if mode.startswith('native') else 'stdout.bin'
            raw=text(ref(o['raw'],f'raw/{f}/{mode}/{rname}',mode))
            if o['raw']['root']=='peer': need(marker=='R0_BAD_EMPTY_0','peer case misuse')
            for key in ('BEFORE','ARG','AFTER','EVAL','ARRAY'):
                for line in o[key]: need(line in raw and marker in line,'raw marker mismatch')
            need(o['BEFORE']==['BEFORE '+marker] and o['condition_marker_observed'] is True and o['callee_body_from_before']=='NOT_ESTABLISHED_BY_BEFORE_MARKER' and 'target_reached' not in o,'condition marker semantics mismatch')
            if o['ARG']:
                need(o['ARG'][-1].endswith('ORDER='+o['helper_order_observed']),'helper order')
            if mode=='public-01': diagtext=text(ref(o['stderr'],f'raw/{f}/{mode}/stderr.bin'))
            else: diagtext=raw
            if o['outcome']=='return':
                need(len(o['AFTER'])==len(o['EVAL'])==len(o['ARRAY'])==1 and o['diagnostic'] is None,'return markers')
                match=re.fullmatch(r'AFTER \S+ R=(-?\d+) SK=([01]) OUT=(-?\d+)',o['AFTER'][0]); need(match is not None,'after format')
                result,sk,local=map(int,match.groups()); post=o['poststate'];
                need(type(post) is dict and type(post['RESULT']) is int and type(post['RESULTS_sentinel_preserved']) is bool and type(post['expression_local']) is int,'poststate types')
                need(post['RESULT']==result and post['RESULTS_sentinel_preserved']==bool(sk) and post['expression_local']==local,'poststate mismatch')
                need(type(o['value']) is int and o['value']==(local if c['target']['kind']=='expression_function' else result),'return value type or mismatch')
                need(o['ARRAY']==['ARRAY '+marker+' ['+'|'.join(post['array'])+']'] and post['array']==condition['array'],'observed array mismatch')
                need(o['EVAL']==['EVAL '+marker+' COUNT='+str(len(o['ARG']))+' ORDER='+o['helper_order_observed']],'evaluation marker mismatch')
            else:
                need(o['outcome'] in ('regex_error','range_error') and not o['AFTER'] and o['value'] is None and isinstance(o['poststate'],str) and o['poststate'].startswith('unobserved'), 'error/poststate mismatch')
                need(isinstance(o['diagnostic'],str) and o['diagnostic'] in diagtext,'diagnostic absent')
                expected_diagnostic=('正規表現' if o['outcome']=='regex_error' else '範囲外') if mode.startswith('native') else ('E_REGEX' if o['outcome']=='regex_error' else 'E_INDEX')
                need(expected_diagnostic in o['diagnostic'],'diagnostic classification mismatch')
        obs=c['observations']; cmp=c['recorded_comparison']
        need(cmp['same_return_or_error_class']==((obs[0]['outcome'],obs[0]['value'])==(obs[2]['outcome'],obs[2]['value'])),'comparison outcome mismatch')
        need(cmp['same_helper_order']==(obs[0]['helper_order_observed']==obs[2]['helper_order_observed']),'comparison helper mismatch')
        native_keys=('BEFORE','ARG','AFTER','EVAL','ARRAY','outcome','value','diagnostic','helper_order_observed','poststate','termination','condition_marker_observed','callee_body_from_before')
        native2_consistent=all(obs[0][key]==obs[1][key] for key in native_keys)
        need(cmp['native2_consistent'] is native2_consistent,'native repeat comparison mismatch')
        same_diagnostic_text=(obs[0]['diagnostic']==obs[2]['diagnostic'])
        need(cmp['same_diagnostic_text'] is same_diagnostic_text,'diagnostic text comparison mismatch')
        observed_difference=not (cmp['same_return_or_error_class'] and cmp['same_helper_order'] and same_diagnostic_text)
        need(observed_difference,'classification outside reviewed 64-condition profile')
        need(cmp['classification']=='documented_difference','classification mismatch')
    need(len(used)==61,'fixture coverage')
    def mdlink(x,label): return f'[{label}]({x["path"]})' if x['root']=='bundle' else 'peer'
    table=[]
    for c in cs:
        fi=fs[c['fixture']];cond=c['condition'];target=c['target'];obs=c['observations']
        description=f"{target['name']} {target['form']}; {cond['label']}; pattern `{cond['pattern']}`; [{cond['start']},{cond['end']}); selector {cond['selector']}"
        values=[mdlink(o['raw'],str(o['value']) if o['outcome']=='return' else o['outcome'])+'; '+str(o['helper_order_observed']) for o in obs]
        table.append('| '+c['id']+' | '+description+' | '+mdlink(fi['inputs']['ERB/MAIN.ERB'],c['fixture'])+' | '+' | '.join(values)+' |')
    for name in ('OBSERVATIONS_ja.md','OBSERVATIONS_en.md'):
        rows=[line for line in (ROOT/name).read_text(encoding='utf8').splitlines() if re.match(r'^\| C\d{3} \|',line)]
        need(rows==table,'observation table mismatch')
    layout=ROOT.parent.parent
    external={'../../LICENSES/README.ja.md','../../LICENSES/README.md','../../LICENSES/Emuera1824-v24-license-original.txt','../../LICENSES/PyEmuera-3.0.0-LICENSE.txt','../../vendor/emuera/NOTICE.ja.md','../../vendor/emuera/NOTICE.en.md','../observation-adapter-183-20261117/README.ja.md','../observation-adapter-183-20261117/README.md'}
    need(peer.resolve()==(ROOT.parent/'observation-adapter-183-20261117').resolve(),'peer must be sibling in the evidence layout')
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf8')):
            need(not re.match(r'\w+:',target),'external link not supported')
            target=target.split('#',1)[0]
            if target in external:
                rel=target[6:] if target.startswith('../../') else 'evidence/'+target[3:]
                safe(layout,rel)
            else: safe(path.parent,target)
    print('PASS: external pin, inventory, peer bindings, 64 conditions, 61 fixtures, 192 condition/modes, local links')

if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('--peer',type=Path,required=True,help='existing observation-adapter-183 bundle'); a.add_argument('--inventory-tool',type=Path,required=True); a.add_argument('--pin',required=True); a.add_argument('--peer-pin',required=True); a.add_argument('--tool-pin',required=True); z=a.parse_args()
    try: verify(z.peer.absolute(),z.inventory_tool.absolute(),z.pin,z.peer_pin,z.tool_pin)
    except OSError: print('FAIL: required file unavailable or unreadable',file=sys.stderr); sys.exit(1)
    except (ValueError,KeyError,IndexError,StopIteration,TypeError,json.JSONDecodeError) as e: print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
