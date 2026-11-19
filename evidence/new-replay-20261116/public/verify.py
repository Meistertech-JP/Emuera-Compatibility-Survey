"""Offline check of the selected public replay evidence; no engines are started."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import math
import re
import sys
import struct

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    def pairs(items):
        obj = {}
        for key, value in items:
            require(key not in obj, 'duplicate JSON key')
            obj[key] = value
        return obj
    def number(value):
        result = float(value)
        require(math.isfinite(result), 'nonfinite JSON number')
        return result
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_float=number, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def lines(path):
    data = path.read_bytes()
    return data.decode('utf-16' if data.startswith((b'\xff\xfe', b'\xfe\xff')) else 'ascii', errors='strict').splitlines()


def file_set(root):
    result = set()
    for path in root.rglob('*'):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError('symlink rejected: '+rel)
        if path.is_file() and rel != 'manifest.json':
            result.add(rel)
    return result


def verify_manifest():
    manifest = read_json(ROOT/'manifest.json')
    require(set(manifest) == {'schema','files'} and manifest['schema'] == 'replay-evidence-manifest.v1', 'manifest schema')
    require(isinstance(manifest['files'],list), 'manifest files')
    seen = set()
    for row in manifest['files']:
        require(isinstance(row,dict) and set(row)=={'path','size','sha256'}, 'file record')
        name = row['path']
        require(isinstance(name,str) and name and '\\' not in name and ':' not in name, 'unsafe path')
        pp = PurePosixPath(name)
        require(not pp.is_absolute() and '..' not in pp.parts and pp.as_posix()==name, 'unsafe path')
        require(name.casefold() not in seen, 'duplicate path')
        seen.add(name.casefold())
        path = ROOT/name
        require(path.is_file() and not path.is_symlink(), 'missing file: '+name)
        require(type(row['size']) is int and path.stat().st_size==row['size'], 'size mismatch: '+name)
        require(re.fullmatch(r'[0-9a-f]{64}',row['sha256']) and digest(path)==row['sha256'], 'hash mismatch: '+name)
    require(seen=={x.casefold() for x in file_set(ROOT)}, 'file set mismatch')


def unique_ordered(text, markers):
    require(all(text.count(x)==1 for x in markers), 'missing or duplicate marker')
    indices = [text.index(x) for x in markers]
    require(indices == sorted(indices), 'marker order')


def expression_rows(plan, raw):
    text = lines(raw)
    require(text.count('ZZBATCH_DONE') == 1, 'missing final marker')
    rows = {}
    previous = -1
    for case in plan:
        name = case['case_id']
        tag = 'ZZBATCH_' + name
        fields = ['value','result0','result1','results']
        prefix = [tag+'_BEGIN']
        start = text.index(prefix[0]) if text.count(prefix[0])==1 else -1
        end = text.index(tag+'_END') if text.count(tag+'_END')==1 else -1
        require(previous < start < end < text.index('ZZBATCH_DONE'), 'expression marker order')
        segment = text[start+1:end]
        require(len(segment)==4, 'expression field count')
        values = {}
        for field, line in zip(fields, segment):
            pattern = re.escape(tag+'_OBS_'+field+'=[')+r'([^\]\r\n]*)\]'
            found = re.fullmatch(pattern, line)
            require(found is not None, 'invalid field '+field)
            values[field] = found.group(1)
        rows[name] = values
        previous = end
    all_markers = [x for x in text if x.startswith('ZZBATCH_')]
    require(len(all_markers)==len(plan)*6+1, 'extra expression markers')
    return rows


def verify_expression():
    success = ROOT/'expression/successful-rerun'
    plan_doc = read_json(success/'plan.json')
    require(plan_doc['schema']=='pyemuera.batch-plan.v1', 'plan schema')
    plan = plan_doc['cases']
    expected_ids = ['AUTO_V2_EXPR_001_ABS','AUTO_V2_ACCEPT_STRFINDU_EMPTY_END','AUTO_V2_ACCEPT_STRFIND_EMPTY_END']
    require([x['case_id'] for x in plan]==expected_ids, 'unexpected case selection')
    require([x['typed_key'] for x in plan]==['expression_function:ABS','expression_function:STRFINDU','expression_function:STRFIND'], 'typed keys')
    expected_native = ['7','-1','-1']
    expected_py = ['7','3','3']
    result = read_json(success/'result.json')
    require(result['status']=='completed_with_forced_native_cleanup' and result['native_repeats']==2, 'rerun status')
    require(result['lock_released'] is True and len(result['stages'])==2, 'lock/stages')
    for stage in result['stages']:
        require(stage['native_outcomes']==['forced_termination']*2 and stage['desktop_closed']==[True]*2
                and stage['native_processes_after_empty']==[True]*2 and stage['py_returncode']==0, 'native outcomes')
    for stage, selected in [('single',plan[:1]),('batch',plan)]:
        folder = success/stage
        fixture = (folder/'fixture.ERB').read_bytes()
        require(fixture.endswith(b'QUIT\r\n') and b'PRINTL ZZBATCH_DONE\r\n' in fixture, 'fixture markers')
        for case in selected:
            require(case['expression'].encode('cp932') in fixture, 'fixture expression missing')
        observations = []
        for name in ('native-01.log','native-02.log','py.log'):
            observations.append(expression_rows(selected, folder/name))
        for i, case in enumerate(selected):
            key = case['case_id']
            for side in range(3):
                values = observations[side][key]
                require(values['value']==(expected_native[i] if side<2 else expected_py[i]), 'expression value')
                require([values['result0'],values['result1'],values['results']]==['701','702','AUTO_SENT'], 'sentinels')
            if stage=='batch':
                row = result['case_results'][i]
                require(row['case_id']==key and row['status']==('matched_scoped' if i==0 else 'different'), 'stored result status')
                require(row['native']['observations']==observations[0][key] and row['py']['observations']==observations[2][key], 'stored observations')


def verify_local():
    for name, py_rc in [('state-write',0)]:
        folder=ROOT/'local'/name
        receipt=read_json(folder/'result.json')
        require(receipt['py_returncode']==py_rc and digest(folder/'fixture.ERB')==receipt['fixture_sha256'], 'state fixture/rc')
        markers=['BEFORE_RESULT=[701]','BEFORE_RESULTS=[AUTO_SENT]','AFTER_RESULT=[42]','AFTER_RESULTS=[123]','OBSERVATIONS_DONE']
        for side in ('native','py'):
            unique_ordered(lines(folder/(side+'.log')),markers)
        require(receipt['native_outcome']=='forced_termination' and receipt['native_natural_exit']=='unobserved', 'state outcome')
    for name, marker in [('input-number-logged','INPUT_RESULT=[42]'),('input-string-logged','INPUT_RESULTS=[ABC]')]:
        folder=ROOT/'local'/name
        receipt=read_json(folder/'result.json')
        require(digest(folder/'fixture.ERB')==receipt['fixture_sha256'], 'input fixture hash')
        for side in ('native','py'):
            require(lines(folder/(side+'.log')).count(marker)==1, 'input log marker')
    for name, value in [('input-number','42'),('input-string','[ABC]')]:
        folder=ROOT/'local'/name
        receipt=read_json(folder/'result.json')
        require(digest(folder/'fixture.ERB')==receipt['fixture_sha256'], 'input fixture hash')
        require(value in lines(folder/'py-stdout.bin'), 'input stdout')
    for name in ('input-number','input-string','input-number-logged','input-string-logged'):
        receipt=read_json(ROOT/'local'/name/'result.json')
        require(receipt['input_sent'] is True and receipt['native_outcome']=='forced_termination'
                and receipt['native_natural_exit']=='unobserved' and receipt['py_returncode']==0
                and receipt['lock_released'] is True and receipt['inputs_unchanged'] is True, 'input receipt')
        require(receipt['native_crop']=='included: native/crop-before.bmp and native/crop-after.bmp', 'crop availability')
    for name in ('argument','syntax-stop'):
        folder=ROOT/'local'/name
        record=read_json(folder/'result.json')
        require(digest(folder/'fixture.ERB')==record['fixture_sha256'], 'diagnostic fixture hash')
        require(record['py_returncode']==1 and record['native_outcome']=='forced_termination'
                and 'original private process receipt' in record['verification_limit'], 'diagnostic limitation')
    config=read_json(ROOT/'configuration.json')
    require(config['provided'] is True and config['path']=='config/emuera.config' and config['fixture_config_sha256']==CONFIG_PIN, 'config availability')



# Fixed from the separately reviewed source artifacts; no original receipt is published.
REVIEWED_PINS = {'local/argument/native-diagnostic.log': '716ced97c6e253c89e29ade1e095b172e43aa843184537d5e381ee7af05b1098', 'local/argument/native/crop-before.bmp': 'edfc4210232e391488e2590a81555f9024651fe86d7d4f56ea658c659489eca6', 'local/argument/py-stderr.bin': 'f8353b374baa221fde6b781edb222b7994bc6dd87b5bc4ba8ceb566d5d621d57', 'local/input-number-logged/native/crop-after.bmp': 'c027a297280396c2f51668a68642067cf51f837092fadcfa526473f3788cfd86', 'local/input-number-logged/native/crop-before.bmp': 'fe886fa04cd6c1934ada81c858ab04fa6374854db6517f4ea53d1cab135f6ac9', 'local/input-number/native/crop-after.bmp': '3a952580c11fe7ec21aa86427a6504b038b0b8a0493be56d19abb927b5303a49', 'local/input-number/native/crop-before.bmp': 'fe886fa04cd6c1934ada81c858ab04fa6374854db6517f4ea53d1cab135f6ac9', 'local/input-string-logged/native/crop-after.bmp': '4faf74c775a56a14f53334a3e1dcc1f6502fa0f42a0927c2dea9d1829bf55971', 'local/input-string-logged/native/crop-before.bmp': 'fe886fa04cd6c1934ada81c858ab04fa6374854db6517f4ea53d1cab135f6ac9', 'local/input-string/native/crop-after.bmp': 'fb424f017daa4c7ceb7654943520707f6b1325d9aeca59ae8d32154fdee0b049', 'local/input-string/native/crop-before.bmp': 'fe886fa04cd6c1934ada81c858ab04fa6374854db6517f4ea53d1cab135f6ac9', 'local/syntax-stop/native-diagnostic.log': 'e6b93d9b10029ecaa8f2547958966fbeaf08434a29c3fd5408e402b8b011e978', 'local/syntax-stop/native/crop-before.bmp': '48a6f6f06b9f4254e687f43547db07c3af2743768d78453348985baf5f66eec6', 'local/syntax-stop/py-stderr.bin': '5d90a6b83c990185dc36caeebb7d006325129f852ddd97adf69a5a2b2b295437'}
REVIEWED_PINS.update({
    'local/argument/py-stdout.bin': '3b338d59074d61e6637618f66f06da51cefd3af867fe64c1d911b045b3ee602a',
    'local/syntax-stop/py-stdout.bin': '349ce4891601bef407c5852e88135a16b75a3d1fd5afbd41173c8bf7ed956265',
})
CONFIG_PIN = 'f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc'
LICENSE_PINS = {
    'LICENSES/Emuera1824-v24-license-original.txt': 'ce1134568e4a9fd56d4831c37dceb82050009e90349394f3f05a03a668500a06',
    'LICENSES/PyEmuera-3.0.0-LICENSE.txt': 'b33bbcc5a0d1ace88bfb1d3f9443337ce4b1030a68396430c53b1563203d63f0',
    'LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md': 'cdb1dfe80b9ffe1defc575c280ac8bd2b82d44f6c81ad50a10671f0dbf284edb',
}

def verify_reviewed_artifacts():
    require(digest(ROOT/'config/emuera.config')==CONFIG_PIN, 'reviewed configuration hash')
    for name, expected in LICENSE_PINS.items():
        require(digest(ROOT/name)==expected, 'license hash: '+name)
    for name, expected in REVIEWED_PINS.items():
        path = ROOT/name
        require(digest(path)==expected, 'reviewed evidence hash: '+name)
        if name.endswith('.bmp'):
            data=path.read_bytes()
            require(len(data)==896054 and data[:2]==b'BM' and struct.unpack_from('<I',data,2)[0]==len(data), 'BMP header')
            require(struct.unpack_from('<I',data,10)[0]==54 and struct.unpack_from('<I',data,14)[0]==40, 'BMP format')
            require(struct.unpack_from('<iiHHI',data,18)==(700,320,1,32,0), 'BMP dimensions')
    for name in ('argument','syntax-stop'):
        native=(ROOT/'local'/name/'native-diagnostic.log').read_bytes().decode('utf-16',errors='strict')
        encoding='cp932' if name=='argument' else 'utf-8'
        py=(ROOT/'local'/name/'py-stderr.bin').read_bytes().decode(encoding,errors='strict')
        require(native.count('BEFORE')==1 and '3\u884c\u76ee' in native, 'native diagnostic markers')
        require(('E_ARGUMENT' if name=='argument' else 'E_SYNTAX') in py, 'py diagnostic marker')
    require(lines(ROOT/'local/argument/py-stdout.bin')==['Now Loading...', 'BEFORE'], 'argument Py stdout')
    require(lines(ROOT/'local/syntax-stop/py-stdout.bin')==['Now Loading...'], 'syntax Py stdout')
    # Do not infer image text or natural process termination from bytes or seals.


def main():
    try:
        verify_manifest()
        verify_expression()
        verify_local()
        verify_reviewed_artifacts()
        print('PASS: public file inventory, hashes and selected offline observations')
        print('LIMIT: image content requires human review; private originals, original seals and engine execution not verified')
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, UnicodeError) as exc:
        print('FAIL:', str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
