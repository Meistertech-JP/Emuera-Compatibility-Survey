"""Check the pinned bundle and its finite saved-marker bindings; no engine replay."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TOOL_SHA256 = '387204bdfe5288a967176c46549ec5e9c00b1a26466a9e8bee01846a98237366'
TARGETS = {
    'OPNORMAL273_E143': {'+'},
    'OPNORMAL273_E145': {'/', '%'},
    'OPNORMAL273_E138': {'&', '|', '^'},
    'OPNORMAL273_E140': {'&&', '||', '^^', '!&', '!|'},
    'OPNORMAL273_E141': {'==', '!=', '>', '<', '>=', '<='},
    'OPNORMAL273_E144': {'?', '#'},
}

def check(value, message):
    if not value:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def asset(ref, expected_path):
    check(set(ref) == {'path', 'sha256', 'bytes', 'encoding'}, 'asset fields')
    name = ref['path']; path = PurePosixPath(name)
    check(name == expected_path and not path.is_absolute() and '..' not in path.parts and '\\' not in name, 'asset path')
    obj = HERE.joinpath(*path.parts)
    check(obj.is_file() and not obj.is_symlink() and obj.resolve().is_relative_to(HERE), 'asset missing or unsafe')
    raw = obj.read_bytes()
    check(type(ref['bytes']) is int and len(raw) == ref['bytes'] and sha(raw) == ref['sha256'], 'asset SHA or size')
    return raw.decode(ref['encoding'])

def check_markers(text, expected):
    lines = text.splitlines(); positions = []
    for marker in expected:
        found = [i for i, line in enumerate(lines) if line.strip() == marker]
        check(len(found) == 1, 'marker count')
        positions.append(found[0])
    check(positions == sorted(positions), 'marker order')
    done = [i for i, line in enumerate(lines) if line.strip() == 'DONE']
    check(len(done) == 1 and (not positions or done[0] > positions[-1]), 'DONE count or order')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--verifier-sha256', required=True)
    parser.add_argument('--bindings-sha256', required=True)
    args = parser.parse_args()
    manifest = HERE/'manifest.json'
    check(sha(manifest.read_bytes()) == args.manifest_sha256, 'manifest pin')
    check(sha(Path(__file__).read_bytes()) == args.verifier_sha256, 'verifier pin')
    binding_bytes = (HERE/'bindings.json').read_bytes()
    check(sha(binding_bytes) == args.bindings_sha256, 'bindings pin')
    bindings = json.loads(binding_bytes)
    tool = HERE/'tools/file_set_manifest.py'
    check(sha(tool.read_bytes()) == TOOL_SHA256, 'shared tool pin')
    subprocess.run([sys.executable, '-I', '-B', str(tool), 'verify', '--manifest', str(manifest), '--root', 'evidence='+str(HERE)], check=True)
    data = json.loads((HERE/'index.json').read_bytes())
    check(data['schema'] == 'operator-normal273-saved-evidence-v1', 'schema')
    cases = data['cases']
    check(len(cases) == 6 and len({c['case_id'] for c in cases}) == 6 and {c['case_id'] for c in cases} == set(TARGETS), 'case set')
    check(set(bindings) == {'schema', 'source_register_sha256', 'cases'} and bindings['schema'] == 'operator-normal273-case-bindings-v1', 'bindings schema')
    check(isinstance(bindings['source_register_sha256'], str) and len(bindings['source_register_sha256']) == 64 and all(c in '0123456789abcdef' for c in bindings['source_register_sha256']), 'source register SHA')
    bound = bindings['cases']
    check(isinstance(bound, list) and len(bound) == 6 and len({x['case_id'] for x in bound}) == 6, 'binding case set')
    by_case = {x['case_id']: x for x in bound}
    check(set(by_case) == set(TARGETS), 'binding case IDs')
    marker_count = 0
    for case in cases:
        current_binding = {
            'case_id': case['case_id'], 'typed_targets': case['typed_targets'],
            'case_register_pointer': case['case_register_pointer'],
            'fixture_sha256': case['inputs']['fixture']['sha256'],
            'config_sha256': case['inputs']['config']['sha256'],
            'selected_normal_markers': case['selected_normal_markers'],
            'public_stdout_sha256': case['public']['stdout']['sha256'],
            'public_stderr_sha256': case['public']['stderr']['sha256'],
            'public_pyz_sha256_before': case['public']['public_pyz_sha256_before'],
            'public_pyz_sha256_after': case['public']['public_pyz_sha256_after'],
            'native': [{'mode': n['mode'], 'raw_sha256': n['raw']['sha256'],
                        'exe_sha256_recorded_and_retained': n['exe_sha256_recorded_and_retained']} for n in case['native']],
        }
        check(current_binding == by_case[case['case_id']], 'case source binding')
        cid = case['case_id']; base = 'assets/'+cid
        targets = case['typed_targets']
        check(all(x['kind'] == 'operator' for x in targets) and len(targets) == len(TARGETS[cid]) and {x['name'] for x in targets} == TARGETS[cid], 'typed targets')
        check(case['recorded_conditions']['full_environment_and_input_equivalence'] == 'not_established' and case['recorded_conditions']['public_vs_historical_public_build_identity'] == 'not_established', 'condition limits')
        check(case['public']['stdin'] == 'inherited; content_not_recorded', 'public input limit')
        asset(case['inputs']['fixture'], base+'/inputs/ERB/SEARCHBOUND01.ERB')
        asset(case['inputs']['config'], base+'/inputs/emuera.config')
        markers = case['selected_normal_markers']
        check(isinstance(markers, list) and markers and all(isinstance(s,str) and s for s in markers) and len(set(markers)) == len(markers), 'markers')
        check_markers(asset(case['public']['stdout'],base+'/public/stdout.bin'), markers)
        asset(case['public']['stderr'],base+'/public/stderr.bin')
        native = case['native']
        check(len(native) == 2 and [n['mode'] for n in native] == ['native-01','native-02'], 'native modes')
        for n in native:
            check(n['recorded_execution_time_utc'] is None and n['execution_time_limit'] == 'not_present_in_retained_probe_receipt', 'native time limit')
            check(n['natural_exit'] == 'not_observed_after_5_seconds; cleanup_recorded', 'native exit limit')
            check_markers(asset(n['raw'],base+'/'+n['mode']+'/emuera.log'), markers)
        marker_count += len(markers)
    check(marker_count == 108, 'selected marker count')
    print('PASS: separately pinned case source bindings; 6 cases, 19 typed targets, 108 selected markers in 3 saved outputs per case; no engine execution or full-condition equivalence')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
