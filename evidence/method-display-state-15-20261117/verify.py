"""Verify fixed shared case bindings and saved history; no engine execution."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
TOOL_SHA='387204bdfe5288a967176c46549ec5e9c00b1a26466a9e8bee01846a98237366'
GETTERS={'GETCOLOR','GETDEFCOLOR','GETFOCUSCOLOR','GETBGCOLOR','GETDEFBGCOLOR','GETSTYLE','GETFONT','CURRENTALIGN','CURRENTREDRAW','LINEISEMPTY'}
SETTERS={'SETCOLOR':'GETCOLOR','SETBGCOLOR':'GETBGCOLOR','FONTSTYLE':'GETSTYLE','ALIGNMENT':'CURRENTALIGN','REDRAW':'CURRENTREDRAW'}
def check(v,msg):
    if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def asset(ref,expected):
    check(set(ref)=={'path','sha256','size','encoding'} and ref['path']==expected,'asset path or fields')
    path=PurePosixPath(ref['path']);check(not path.is_absolute() and '..' not in path.parts and '\\' not in str(path),'unsafe path')
    p=HERE.joinpath(*path.parts);check(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(HERE),'missing or unsafe asset')
    b=p.read_bytes();check(type(ref['size']) is int and ref['size']==len(b) and sha(b)==ref['sha256'],'asset hash')
    return b
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--verifier-sha256',required=True);a=ap.parse_args()
    manifest=HERE/'manifest.json';tool=HERE/'tools/file_set_manifest.py'
    check(sha(manifest.read_bytes())==a.manifest_sha256,'manifest pin');check(sha(Path(__file__).read_bytes())==a.verifier_sha256,'verifier pin');check(sha(tool.read_bytes())==TOOL_SHA,'common tool pin')
    subprocess.run([sys.executable,'-I','-B',str(tool),'verify','--manifest',str(manifest),'--root','evidence='+str(HERE)],check=True)
    d=json.loads((HERE/'index.json').read_bytes());check(d['schema']=='display-state-method150-shared-evidence-v1' and d['batch_id']=='DISPLAYSTATE01','schema or batch')
    conditions=d['conditions'];check(len(conditions)==20,'condition count');by_marker={x['marker']:x for x in conditions};check(len(by_marker)==20,'duplicate marker')
    for name in GETTERS:
        for phase in ('BASE','SET'):
            row=by_marker[phase+name];check(row['function']==name and row['phase']==phase and row['verdict']=='matched_scoped','condition identity')
            check(isinstance(row['observed_line'], str) and row['observed_line'].startswith(row['marker']+' '), 'condition marker/observation mismatch')
    modes=d['modes'];check([x['mode'] for x in modes]==['native-01','native-02','py'],'mode set');histories=[]
    for m in modes:
        mode=m['mode'];base='modes/'+mode;asset(m['fixture'],base+'/inputs/ERB/SEARCHBOUND01.ERB');asset(m['config'],base+'/inputs/emuera.config')
        raw=asset(m['history'],base+'/raw-history.bin');histories.append(raw);lines=raw.decode(m['history']['encoding']).splitlines()
        for c in conditions:check(sum(x.strip()==c['observed_line'] for x in lines)==1,'saved observation')
        check(sum(x.strip()=='DONE' for x in lines)==1,'DONE count')
        if mode.startswith('native'):
            check(m['receipt_projection']['natural_exit']=='not_observed_after_5_seconds' and m['receipt_projection']['exit_code']=='not_observed','native exit limitation')
        else:check(m['receipt_projection']['historical_pyz_pre_post']=='not_recorded_in_invocation','public build limitation')
    check(histories[0]==histories[1]==histories[2],'history bytes differ')
    cases=d['cases'];check(len(cases)==15 and len({c['case_id'] for c in cases})==15,'case count/duplicate');roles=set()
    for c in cases:
        target=c['typed_target'];kind=target['kind'];name=target['name'];key=(kind,name);check(key not in roles,'duplicate role');roles.add(key)
        check(c['case_id']==('DISPLAYSTATE_'+name if kind=='method_as_command' else 'DISPLAYSTATE_CMD_'+name),'case mapping')
        func=name if kind=='method_as_command' else SETTERS.get(name)
        check((kind=='method_as_command' and name in GETTERS) or (kind=='command_or_syntax' and name in SETTERS),'target')
        check(c['condition_markers']==['BASE'+func,'SET'+func] and c['batch_id']=='DISPLAYSTATE01' and c['recorded_verdict']=='matched_scoped' and c['execution_credit']=='shared_batch_only_not_a_separate_run','binding')
    check(roles=={('method_as_command',x) for x in GETTERS}|{('command_or_syntax',x) for x in SETTERS},'target set')
    print('PASS: 15 recorded case roles, one shared batch, 3 retained histories, 20 recorded observations; no engine execution')
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.CalledProcessError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
