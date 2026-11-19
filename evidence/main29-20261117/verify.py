"""Verify the fixed Main29 repository evidence and shared license pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

STAGES=('single-01','batch','full-batch')
MODES=('native-01','native-02','py')
SENTINELS={'result0':'701','result1':'702','results':'AUTO_SENT'}
MAX_FILE=32*1024*1024

FIXED_PLAN_SHA='b8c779e50928bfff74540b68afd2354522981109db490827b0fae89b2d157abb'
FIXED_PROFILE={'schema': 'main29-neutral-profile.v2', 'case_count': 29, 'case_ids': ['CASE001', 'CASE002', 'CASE003', 'CASE004', 'CASE005', 'CASE006', 'CASE007', 'CASE008', 'CASE009', 'CASE010', 'CASE011', 'CASE012', 'CASE013', 'CASE014', 'CASE015', 'CASE016', 'CASE017', 'CASE018', 'CASE019', 'CASE020', 'CASE021', 'CASE022', 'CASE023', 'CASE024', 'CASE025', 'CASE026', 'CASE027', 'CASE028', 'CASE029'], 'typed_keys': ['expression_function:ABS', 'expression_function:MIN', 'expression_function:MIN', 'expression_function:MAX', 'expression_function:MAX', 'expression_function:LIMIT', 'expression_function:LIMIT', 'expression_function:LIMIT', 'expression_function:LIMIT', 'expression_function:INRANGE', 'expression_function:INRANGE', 'expression_function:INRANGE', 'expression_function:INRANGE', 'expression_function:LOG', 'expression_function:LOG', 'expression_function:LOG', 'expression_function:LOG', 'expression_function:LOG10', 'expression_function:LOG10', 'expression_function:LOG10', 'expression_function:LOG10', 'expression_function:STRCOUNT', 'expression_function:STRCOUNT', 'expression_function:REPLACE', 'expression_function:REPLACE', 'expression_function:TOSTR', 'expression_function:TOSTR', 'expression_function:TOSTR', 'expression_function:TOSTR'], 'representative_case': 'CASE001', 'representative_function': 'ABS'}
FIXED_LICENSES={'LICENSES/Emuera1824-v24-license-original.txt': 'ce1134568e4a9fd56d4831c37dceb82050009e90349394f3f05a03a668500a06', 'LICENSES/PyEmuera-3.0.0-LICENSE.txt': 'b33bbcc5a0d1ace88bfb1d3f9443337ce4b1030a68396430c53b1563203d63f0', 'LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md': 'cdb1dfe80b9ffe1defc575c280ac8bd2b82d44f6c81ad50a10671f0dbf284edb', 'vendor/emuera/NOTICE.en.md': 'd2bdcf230079fe30afbd6c3b12b5d149cf27e680d46e77171fda599f675adb86', 'vendor/emuera/NOTICE.ja.md': 'f83446be611435eb8277d2f5d61325fbd9b35588001e294e07c2a0da6577aa9d', 'LICENSES/README.md': '83471da854ca4e08678105cc3712ce7a877c3693175d2348bea89aba78356261', 'LICENSES/README.ja.md': '1df6f4e1d4d6788b8b723a48544d65e0854a1c5f2694786b7f740b367d080c52'}
README_EN='# Main29: limited legacy expression observations\r\n\r\n[日本語](README.ja.md)\r\n\r\nThis repository evidence directory contains 29 cases in one full batch and separate single and representative batch stages for CASE001 (ABS) only. Each stage retains Native-01, Native-02 and Py roles. `matched_scoped` records the selected expression value and RESULT/RESULTS snapshots; it does not establish acceptance of a parent target, resolve known differences, or establish full compatibility. GUI, input, fatal/load-error conditions and other unobserved conditions are outside this evidence.\r\n\r\nThis neutral-ID derivation comes from an old-format real-engine attempt and a separately retained v3 legacy audit; it is not a new v3 run. Old logs have no `ZZBATCH_DONE`; the last case END is the historical rule. Native natural exit and exit code were not observed: owned processes were forcibly terminated after observation. Py\'s original stdout/stderr and full original scope records are not included. When Native roles have identical bytes, the evidence files alone cannot authenticate which execution produced each copy; role binding follows separately retained private receipts and provenance.\r\n\r\nNative raw/config are associated with Emuera1824+v24 and the Py log with PyEmuera. The repository\'s [license index](../../LICENSES/README.md), [Emuera original license](../../LICENSES/Emuera1824-v24-license-original.txt), [Emuera notice](../../vendor/emuera/NOTICE.en.md), [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [PyEmuera third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md) are outside this directory. The linked Emuera notice describes a different distribution unit containing a separate source ZIP; this evidence directory contains no such ZIP. Its packaging statements concern that separate unit, not this directory. Survey fixtures, derived data, documentation and new tools follow the repository\'s [component license index](../../LICENSES/README.md); third-party notices retain their separate terms as listed there.\r\n\r\nFor offline verification obtain trusted SHA-256 pins for `verify.py` and `manifest.json` through an authenticated independent channel. Compare the verifier before executing it; files or values delivered together are not an independent trust source. Python 3.10 or later, from this evidence directory:\r\n\r\n```text\r\npython -c "import hashlib,sys; sys.exit(0 if hashlib.sha256(open(sys.argv[1],\'rb\').read()).hexdigest()==sys.argv[2] else 1)" verify.py <TRUSTED_VERIFIER_SHA256>\r\npython -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>\r\n```\r\n\r\nStop if the first command exits nonzero. The verifier checks the fixed 29-case profile, evidence file set, fixture, raw observations, outcomes and verdicts, and the fixed hashes of the shared repository license files. It starts no engine and does not authenticate the historical producer or replay the entire legacy audit. Original-source verification requires separately retained private records. The directory alone is not a complete standalone distribution: provide the linked repository license and notice files with the appropriate relative layout. Rights, privacy, release selection and authenticated pin distribution require separate review.\r\n'
README_JA='# Main29：旧形式の限定された式観測\r\n\r\n[English](README.md)\r\n\r\nこのリポジトリ内の証拠ディレクトリは、29ケースの全件バッチと、CASE001（ABS）だけの単独・代表バッチを別stageとして保持します。各stageにNative-01、Native-02、Pyの各modeがあります。`matched_scoped` は選択式の値とRESULT／RESULTSの有限観測であり、親対象全体の受入、既知差分の解消、全互換性を意味しません。GUI・入力・fatal/load errorなどの未観測条件は対象外です。\r\n\r\n旧形式の実機attemptと別保全のv3 legacy監査から中立IDへ派生したもので、新しいv3実行ではありません。旧rawに `ZZBATCH_DONE` はなく、最終case ENDが当時の観測規則です。Nativeの自然終了と終了コードは未観測で、観測後に所有プロセスを強制終了しました。元Pyのstdout/stderrと元scope全文は同梱していません。Nativeの2 modeが同じbytesの場合、証拠ファイルだけではそれぞれの実行を認証できず、対応は別保全の非公開receiptと来歴に基づきます。\r\n\r\nNative raw・configはEmuera1824+v24、PyログはPyEmueraに関係します。リポジトリ共通の[ライセンス一覧](../../LICENSES/README.ja.md)、[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[PyEmuera第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)はこのディレクトリの外にあります。リンク先Emuera NOTICEは別のsource ZIPを含む別配布単位の説明です。この証拠ディレクトリにそのZIPはなく、NOTICEの同梱に関する記述は別配布単位のものであって、このディレクトリの構成を示しません。調査fixture・派生データ・文書・新規ツールの権利条件は、リポジトリ共通の[権利表示](../../LICENSES/README.ja.md)の対象範囲と、そこに掲げる第三者表示の個別条件に従います。\r\n\r\nオフライン検証では認証された独立経路から `verify.py` と `manifest.json` の信頼するSHA-256を入手し、実行前にverifierを照合します。同じ配布物内の値は独立した信頼源ではありません。Python 3.10以上で、この証拠ディレクトリから実行します。\r\n\r\n```text\r\npython -c "import hashlib,sys; sys.exit(0 if hashlib.sha256(open(sys.argv[1],\'rb\').read()).hexdigest()==sys.argv[2] else 1)" verify.py <TRUSTED_VERIFIER_SHA256>\r\npython -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>\r\n```\r\n\r\n最初のコマンドが非0なら中止してください。verifierは固定29件profile、証拠ファイル集合、fixture、raw観測、終了形態・判定と、リポジトリ共通licenseファイルの固定ハッシュを照合します。エンジンは起動せず、実行者の真正性や過去のlegacy監査の全範囲は証明しません。原票照合には別保全の非公開記録が必要です。このディレクトリ単体は完結した配布物ではなく、必要なリポジトリ共通ライセンス・NOTICEを正しい相対配置で同伴させてください。権利・privacy・公開対象選定と認証されたpin配布には別途レビューが必要です。\r\n'

def fail(message):
    raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def filehash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def as_json(value):
    return (json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')

def identical(a,b):
    return as_json(a)==as_json(b)

def read_json(path):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                fail('duplicate JSON key')
            result[k] = v
        return result
    def reject(value):
        fail('nonfinite JSON number')
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=reject, parse_float=lambda value: reject(value) if not __import__('math').isfinite(float(value)) else float(value))

def no_links(root):
    def visit(p):
        info = p.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            fail('link/reparse point')
        if stat.S_ISDIR(info.st_mode):
            with os.scandir(p) as entries:
                for e in entries:
                    visit(Path(e.path))
        elif not stat.S_ISREG(info.st_mode):
            fail('non-regular evidence file')
    visit(Path(root))

def safe_path(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        fail('unsafe relative path')
    p = PurePosixPath(relative)
    if p.is_absolute() or p.as_posix() != relative or any(x in ('', '.', '..') for x in p.parts):
        fail('unsafe relative path')
    return Path(root).joinpath(*p.parts)

def check_manifest(root, expected_sha, source=False):
    root = Path(root)
    no_links(root)
    if source:
        if filehash(root/'SEAL.json') != expected_sha:
            fail('source seal hash mismatch')
        seal = read_json(root/'SEAL.json')
        if set(seal) != {'schema', 'manifest_sha256'} or seal['schema'] != 'pyemuera-evidence-seal-v2':
            fail('source seal schema')
        if seal['manifest_sha256'] != filehash(root/'MANIFEST.json'):
            fail('source manifest seal mismatch')
        manifest = read_json(root/'MANIFEST.json')
        if set(manifest) != {'schema', 'files', 'external_inputs'} or manifest['schema'] != 'pyemuera-evidence-manifest-v2':
            fail('source manifest schema')
        excluded = {'MANIFEST.json', 'SEAL.json'}
    else:
        if filehash(root/'manifest.json') != expected_sha:
            fail('trusted manifest hash mismatch')
        manifest = read_json(root/'manifest.json')
        if set(manifest) != {'schema', 'files'} or manifest['schema'] != 'main29-neutral-repo-evidence.v3':
            fail('derived manifest schema')
        excluded = {'manifest.json'}
    if not isinstance(manifest['files'], list):
        fail('invalid inventory')
    seen = set()
    for row in manifest['files']:
        if not isinstance(row, dict) or set(row) != {'path', 'size', 'sha256'}:
            fail('invalid file entry')
        path = safe_path(root, row['path'])
        key = row['path'].casefold()
        if key in seen or row['path'] in excluded or type(row['size']) is not int or row['size'] < 0:
            fail('duplicate or invalid file entry')
        seen.add(key)
        if not path.is_file() or path.stat().st_size != row['size'] or filehash(path) != row['sha256']:
            fail('inventory mismatch')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != {r['path'] for r in manifest['files']} | excluded:
        fail('missing or extra file')
    return manifest

def check_privacy_text(text):
    patterns = (r'(?i)\b[a-z]:[\\/]', r'(?i)(?:users[\\/]|/home/)[a-z0-9_.-]+',
                r'(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b',
                r'(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\b\s*["\x27]?\s*[:=]\s*["\x27]?[^\s,;"\x27}\]]{4,}',
                r'(?i)\b[0-9a-f]{64}\b')
    if any(re.search(p, text) for p in patterns):
        fail('privacy screen hit; manual review required')

def fixture(cases):
    decl = {}
    for c in cases:
        decl['ZZAV0' if c['value_type'] == 'numeric' else 'ZZAS0'] = '#DIM ' if c['value_type'] == 'numeric' else '#DIMS '
        decl['ZZAR00'] = '#DIM '; decl['ZZAR01'] = '#DIM '; decl['ZZAR02'] = '#DIMS '
    lines = ['@SYSTEM_TITLE'] + [v+k for k,v in decl.items()]
    for c in cases:
        target = 'ZZAV0=' if c['value_type'] == 'numeric' else "ZZAS0 '= "
        lines += ['RESULT:0=701', 'RESULT:1=702', 'RESULTS \'= "AUTO_SENT"', target+c['expression'],
                  'ZZAR00=RESULT:0', 'ZZAR01=RESULT:1', "ZZAR02 '= RESULTS"]
        tag = 'ZZBATCH_'+c['case_id']
        lines += ['PRINTL '+tag+'_BEGIN',
                  'PRINTFORML '+tag+'_OBS_value=['+('{ZZAV0}' if c['value_type']=='numeric' else '%ZZAS0%')+']',
                  'PRINTFORML '+tag+'_OBS_result0=[{ZZAR00}]', 'PRINTFORML '+tag+'_OBS_result1=[{ZZAR01}]',
                  'PRINTFORML '+tag+'_OBS_results=[%ZZAR02%]', 'PRINTL '+tag+'_END']
    return ('\r\n'.join(lines+['OUTPUTLOG', 'QUIT'])+'\r\n').encode('cp932', errors='strict')

def parse_raw(data, cases):
    if len(data)>MAX_FILE or not data.startswith(b'\xff\xfe'):
        fail('unsupported raw encoding/size')
    text = data.decode('utf-16-le', errors='strict')[1:]
    if b'\xff\xfe'+text.encode('utf-16-le') != data or '\n' in text.replace('\r\n', ''):
        fail('noncanonical UTF-16/line endings')
    lines = text.split('\r\n')
    if lines[:1] != ['Now Loading...'] or lines[-1:] != ['']:
        fail('unexpected raw header/trailing bytes')
    lines = lines[1:-1]
    if len(lines) != len(cases)*6 or any(x == 'ZZBATCH_DONE' for x in lines):
        fail('unexpected legacy markers')
    observations = []
    for i,c in enumerate(cases):
        tag = 'ZZBATCH_'+c['case_id']
        block = lines[6*i:6*i+6]
        if block[0] != tag+'_BEGIN' or block[5] != tag+'_END':
            fail('missing/order/duplicate legacy markers')
        values = {}
        for index, name in enumerate(('value','result0','result1','results'),1):
            prefix = tag+'_OBS_'+name+'=['
            if not block[index].startswith(prefix) or not block[index].endswith(']'):
                fail('invalid observation marker')
            v = block[index][len(prefix):-1]
            if name != 'value' or c['value_type'] == 'numeric':
                if name != 'results' and (not re.fullmatch(r'0|-?[1-9][0-9]{0,18}', v) or not -(2**63) <= int(v) < 2**63):
                    fail('invalid numeric observation')
            values[name] = v
        if any(values[k] != v for k,v in SENTINELS.items()):
            fail('sentinel changed; unsupported verdict')
        observations.append({'status':'observed','observations':values})
    return observations

def result_rows(cases, parsed):
    rows=[]
    for i,c in enumerate(cases):
        native=[parsed[0][i],parsed[1][i]]; py=parsed[2][i]
        if native[0]!=native[1] or native[0]!=py:
            fail('observations differ or Native repeats disagree')
        rows.append({'case_id':c['case_id'],'typed_key':c['typed_key'],'status':'matched_scoped',
                     'native':native,'py':py,'native_repeats_agree':True})
    return rows

def summary_for(count):
    return {'schema':'neutral-legacy-expression-summary.v1','case_count':count,'stages':list(STAGES),
            'modes_per_stage':list(MODES),'representative_count':1,
            'status':'completed_with_forced_native_cleanup','scope':'exact expression and RESULT/RESULTS snapshots',
            'final_marker_rule':'last_case_END_only','historical_v3_legacy_audit':'previously_recorded_not_reexecuted',
            'not_observed':['Native natural exit','GUI and input','fatal and load errors','all conditions of all cases']}

def verify_bundle(root, manifest_sha):
    root=Path(root).absolute()
    no_links(root)
    root=root.resolve(strict=True)
    if not re.fullmatch(r'[0-9a-f]{64}',manifest_sha):fail('invalid trusted manifest SHA')
    manifest=check_manifest(root,manifest_sha)
    if filehash(root/'plan.json') != FIXED_PLAN_SHA:
        fail('fixed 29-case plan mismatch')
    if not identical(read_json(root/'PROFILE.json'),FIXED_PROFILE):
        fail('fixed 29-case profile mismatch')
    repo=root.parent.parent
    for name,expected_sha in FIXED_LICENSES.items():
        path=safe_path(repo,name)
        current=repo
        for component in PurePosixPath(name).parts:
            current=current/component
            info=current.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400:
                fail('shared license link or reparse point')
        if not path.is_file() or filehash(path)!=expected_sha:
            fail('shared repository license or notice mismatch')
    if (root/'README.md').read_bytes()!=README_EN.encode('utf-8') or (root/'README.ja.md').read_bytes()!=README_JA.encode('utf-8'):
        fail('unexpected explanatory text')
    plan=read_json(root/'plan.json')
    if not isinstance(plan,dict) or set(plan)!={'schema','cases'} or plan['schema']!='neutral-legacy-expression-plan.v1':
        fail('invalid neutral plan')
    cases=plan['cases']
    if not isinstance(cases,list) or len(cases)!=29 or [c.get('case_id') for c in cases]!=FIXED_PROFILE['case_ids'] or [c.get('typed_key') for c in cases]!=FIXED_PROFILE['typed_keys']:fail('fixed 29-case ID/typed key set mismatch')
    for i,c in enumerate(cases,1):
        if (not isinstance(c,dict) or set(c)!={'case_id','typed_key','expression','value_type'}
                or c['case_id']!='CASE%03d'%i or c['value_type'] not in ('numeric','string')
                or not isinstance(c['typed_key'],str) or not re.fullmatch(r'expression_function:[A-Z][A-Z0-9_]*',c['typed_key'])
                or not isinstance(c['expression'],str) or not c['expression'] or '\r' in c['expression'] or '\n' in c['expression']):
            fail('invalid neutral case')
        check_privacy_text(c['expression'])
    if not identical(read_json(root/'summary.json'),summary_for(len(cases))):
        fail('summary does not preserve observation scope')
    required={'README.md','README.ja.md','plan.json','summary.json','PROFILE.json','verify.py'}
    reference_config=None; rows_by_stage=[]
    for stage in STAGES:
        group=cases if stage=='full-batch' else cases[:1]
        parsed=[]
        for mode in MODES:
            prefix=stage+'/'+mode+'/'; required.update(prefix+x for x in ('raw.log','fixture.erb','emuera.config','mode.json'))
            raw=(root/prefix/'raw.log').read_bytes(); erb=(root/prefix/'fixture.erb').read_bytes(); config=(root/prefix/'emuera.config').read_bytes()
            if erb!=fixture(group):fail('derived fixture differs from derived plan')
            if reference_config is None:reference_config=config
            if config!=reference_config:fail('mode configs differ')
            check_privacy_text(erb.decode('cp932'));check_privacy_text(raw.decode('utf-16'));check_privacy_text(config.decode('cp932'))
            expected=({'side':'py','outcome':'natural_rc0','natural_exit_observed':True,'exit_code':0} if mode=='py'
                      else {'side':'native','outcome':'forced_termination','natural_exit_observed':False,
                            'exit_code':None,'owned_desktop_created':True,'desktop_closed':True,'input_sent':False})
            if not identical(read_json(root/prefix/'mode.json'),expected):fail('mode outcome changed')
            parsed.append(parse_raw(raw,group))
        rows=result_rows(group,parsed)
        expected_stage={'schema':'neutral-legacy-expression-stage.v1','name':stage,'cases':[c['case_id'] for c in group],
                        'modes':list(MODES),'rows':rows}
        if not identical(read_json(root/(stage+'/stage.json')),expected_stage):fail('stage observations or verdicts differ')
        required.add(stage+'/stage.json');rows_by_stage.append(rows)
    if rows_by_stage[0][0]!=rows_by_stage[1][0] or rows_by_stage[0][0]!=rows_by_stage[2][0]:
        fail('representative stage parity mismatch')
    if {x['path'] for x in manifest['files']}!=required:fail('unexpected derived file set')
    return {'valid':True,'cases':len(cases),'stages':3,'modes':9,
            'scope':'neutral derived observations; not historical authenticity or full v3 audit'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--verifier-sha256',required=True)
    args=parser.parse_args()
    try:
        here=Path(__file__).resolve().parent
        if not re.fullmatch(r'[0-9a-f]{64}',args.verifier_sha256) or filehash(Path(__file__))!=args.verifier_sha256:
            fail('trusted verifier hash mismatch')
        result=verify_bundle(here,args.manifest_sha256)
        print(json.dumps(result,ensure_ascii=True,indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError,IndexError,UnicodeError) as exc:
        print('refused: '+str(exc),file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
