"""Read-only, partial adapter for selected acceptance-chain layouts.

The selected audit snapshot and all followed references must have explicit SHA-256
pins. A checked hash is not a compatibility verdict or an original-coverage proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat
import sys

AUDIT_SCHEMA = 'read-only-uniform-acceptance-chain-audit-1'
SUPPORTED = {'parent-target-finite-scope-adjudication-1',
             'phase2-target-parent-acceptance/v1',
             'original-return-three-parent-acceptance-1',
             'target-finite-comparison-adjudication-1'}
HEX = re.compile(r'[0-9a-f]{64}\Z')
REPARSE = getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)


class EvidenceError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise EvidenceError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_json(path, expected):
    def pairs(items):
        obj = {}
        for key, value in items:
            require(key not in obj, 'duplicate JSON key')
            obj[key] = value
        return obj
    def reject(value):
        raise EvidenceError('invalid JSON value: '+value)
    def finite(value):
        result = float(value)
        require(math.isfinite(result), 'nonfinite JSON number')
        return result
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==expected, 'hash mismatch while reading JSON')
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs,
                      parse_float=finite, parse_constant=reject)


def no_link(path):
    for part in reversed((path, *path.parents)):
        info = part.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not (getattr(info,'st_file_attributes',0) & REPARSE),
                'symbolic link or reparse point rejected')


def safe_name(value):
    require(isinstance(value,str) and value, 'missing reference path')
    name = value.replace('\\','/')
    require(not name.startswith('/') and ':' not in name and '\x00' not in name, 'absolute or unsafe path')
    parts = name.split('/')
    require(all(x not in ('','.','..') for x in parts), 'noncanonical reference path')
    require(PurePosixPath(name).as_posix()==name, 'noncanonical reference path')
    return name


def pinned(root, name, expected, role, checks):
    name = safe_name(name)
    require(isinstance(expected,str) and HEX.fullmatch(expected), 'missing or invalid declared SHA-256: '+role)
    require(not any(item['path'].casefold()==name.casefold() for item in checks), 'duplicate referenced path: '+role)
    path = root.joinpath(*name.split('/'))
    no_link(path)
    require(path.is_file(), 'reference is not a file: '+role)
    actual = sha(path)
    require(actual==expected, 'hash mismatch: '+role)
    checks.append({'role':role, 'path':name, 'sha256':expected, 'status':'hash_matched'})
    return path


def targets_equal(value, target):
    return isinstance(value,dict) and value.get('kind')==target['kind'] and value.get('name')==target['name']


def resolve_pointer(document, pointer):
    if pointer == '':
        return document
    require(isinstance(pointer,str) and pointer.startswith('/') and pointer != '/', 'unsupported acceptance pointer')
    node = document
    for part in pointer[1:].split('/'):
        part = part.replace('~1','/').replace('~0','~')
        if isinstance(node,list):
            require(part.isdigit(), 'unsupported acceptance pointer')
            node = node[int(part)]
        else:
            require(isinstance(node,dict) and part in node, 'unsupported acceptance pointer')
            node = node[part]
    return node


def require_case_binding(row, cases):
    require(isinstance(cases,list) and cases and all(isinstance(c,str) and c for c in cases), 'invalid case IDs')
    require(len(set(cases))==len(cases), 'duplicate case ID')
    links = row.get('case_role_links')
    require(isinstance(links,list), 'case role links absent')
    for case in cases:
        matches = [x for x in links if isinstance(x,dict) and x.get('case_id')==case]
        require(len(matches)==1 and matches[0].get('registered_typed_target_matches') is True,
                'case target binding missing or ambiguous')


def column_fixture(root, audit_name, audit_data, row, doc, target, checks):
    """Read only the PRINTC/PRINTLC column-boundary manifest layout."""
    expected_cases = {
        'PRINTC': 'COLUMN_PRINTC_EMPTY_SHORT_EQUAL_20261115',
        'PRINTLC': 'COLUMN_PRINTLC_EMPTY_SHORT_EQUAL_20261115',
    }
    expected_case = expected_cases[target['name']]
    require(doc.get('decision') == 'necessary_comparison_complete', 'unsupported column decision')
    require(doc.get('comparison_outcome') == row.get('row_outcome') == 'matched_in_finite_scope',
            'column acceptance outcome mismatch')
    require(doc.get('case_ids') == [expected_case], 'column acceptance case mismatch')
    require_case_binding(row, [expected_case])
    link = next(x for x in row['case_role_links'] if x.get('case_id') == expected_case)
    pointer = link.get('register_pointer')
    require(isinstance(pointer, str) and re.fullmatch(r'/records/(0|[1-9][0-9]*)', pointer),
            'invalid case register pointer')
    require(link.get('register_snapshot') == 'snapshot/CASE_SCENARIO_REGISTER.json',
            'unsupported case register locator')
    pins = audit_data.get('root_capture_pins')
    require(isinstance(pins, dict), 'case register pin absent')
    register_name = (PurePosixPath(safe_name(audit_name)).parent /
                     'snapshot/CASE_SCENARIO_REGISTER.json').as_posix()
    register_path = pinned(root, register_name, pins.get('CASE_SCENARIO_REGISTER.json'),
                           'case_register_snapshot', checks)
    register = parse_json(register_path, pins['CASE_SCENARIO_REGISTER.json'])
    records = register.get('records') if isinstance(register, dict) else None
    index = int(pointer.rsplit('/', 1)[1])
    require(isinstance(records, list) and index < len(records), 'case register pointer missing')
    case = records[index]
    require(isinstance(case, dict) and case.get('case_id') == expected_case and
            target in case.get('targets', []) and case.get('scenario_verdict') == 'matched_scoped',
            'case register identity, typed target or verdict mismatch')

    acceptance_dir = PurePosixPath(safe_name(row['acceptance']['path'])).parent
    manifest_name = safe_name(doc.get('manifest_path'))
    require(manifest_name == (acceptance_dir / 'MANIFEST.json').as_posix(),
            'unsupported column manifest base')
    mf = pinned(root, manifest_name, doc.get('manifest_sha256'), 'column_manifest', checks)
    manifest = parse_json(mf, doc['manifest_sha256'])
    entries = manifest.get('files') if isinstance(manifest, dict) else None
    require(isinstance(entries, list) and entries, 'column manifest files missing')
    by_name = {}
    for entry in entries:
        require(isinstance(entry, dict), 'invalid manifest member')
        name = safe_name(entry.get('path'))
        require(name.casefold() not in by_name, 'duplicate manifest member')
        require(type(entry.get('size')) is int and entry['size'] >= 0, 'invalid manifest size')
        require(isinstance(entry.get('sha256'), str) and HEX.fullmatch(entry['sha256']),
                'invalid manifest hash')
        by_name[name.casefold()] = entry

    def member(name, role):
        entry = by_name.get(name.casefold())
        require(entry is not None and entry['path'] == name, 'missing exact manifest member: '+role)
        path = pinned(root, (acceptance_dir / name).as_posix(), entry['sha256'], role, checks)
        require(path.stat().st_size == entry['size'], 'manifest member size mismatch: '+role)
        return path, entry['sha256']

    comp_path, comp_hash = member('COMPARISON.json', 'column_comparison')
    comp = parse_json(comp_path, comp_hash)
    require(comp.get('verdict') == 'matched_scoped' and
            comp.get('raw_native_repeat_equal') is True and comp.get('raw_public_equal') is True and
            comp.get('state_sentinels_match') is True, 'unsupported column comparison')
    values = [('EMPTY', '', 0), ('SHORT', 'ABC', 3),
              ('EQUAL', 'ABCDEFGHIJKLMNOPQRSTUVWXY', 25)]
    expected = [{'target': n, 'id': n+'_'+suffix, 'value': value, 'ascii_width': width}
                for n in ('PRINTC', 'PRINTLC') for suffix, value, width in values]
    require(comp.get('cases') == expected, 'column comparison condition mismatch')
    texts = comp.get('texts')
    require(isinstance(texts, dict) and set(texts) == {'native-01', 'native-02', 'public-01'},
            'column comparison modes differ')
    modes, fixtures, configs, decoded, pyz = [], [], [], [], []
    for mode in ('native-01', 'native-02', 'public-01'):
        fixture, fixture_hash = member(mode+'/ERB/SEARCHBOUND01.ERB', mode+':fixture')
        config, config_hash = member(mode+'/emuera.config', mode+':config')
        raw_name = mode+'/emuera.log' if mode.startswith('native-') else mode+'/.pyemuera/logs/emuera.log'
        raw, raw_hash = member(raw_name, mode+':outputlog')
        before, before_hash = member(mode+'/RECEIPT_BEFORE.json', mode+':receipt_before')
        after, after_hash = member(mode+'/RECEIPT_AFTER.json', mode+':receipt_after')
        member(mode+'/stdout.bin', mode+':stdout')
        member(mode+'/stderr.bin', mode+':stderr')
        before_doc, after_doc = parse_json(before, before_hash), parse_json(after, after_hash)
        expected_inputs = {'ERB/SEARCHBOUND01.ERB': fixture_hash, 'emuera.config': config_hash}
        require(before_doc.get('inputs_before') == after_doc.get('inputs_before') ==
                after_doc.get('inputs_after') == expected_inputs, 'receipt input pins differ')
        require(before_doc.get('argv') == after_doc.get('argv'), 'receipt command differs')
        pyz_hash = before_doc.get('pyz_before')
        require(isinstance(pyz_hash, str) and HEX.fullmatch(pyz_hash) and
                pyz_hash == after_doc.get('pyz_before') == after_doc.get('pyz_after'),
                'recorded PyEmuera pin differs')
        pyz.append(pyz_hash)
        if mode.startswith('native-'):
            argv = before_doc.get('argv')
            require(isinstance(argv, list) and argv and isinstance(argv[-1], str) and
                    argv[-1].replace('\\', '/').rstrip('/').split('/')[-1] == mode,
                    'native receipt mode mismatch')
            probe_path, probe_hash = member(mode+'/probe.json', mode+':probe')
            probe = parse_json(probe_path, probe_hash)
            exe, exe_hash = member(mode+'/Emuera1824+v24.exe', mode+':native_executable')
            require(probe.get('fixture_sha256') == fixture_hash and probe.get('config_sha256') == config_hash and
                    probe.get('native_exe_sha256') == exe_hash == before_doc.get('exe_before') ==
                    after_doc.get('exe_before') and probe.get('process_created') is True and
                    probe.get('cwd', '').replace('\\', '/').rstrip('/').split('/')[-1] == mode,
                    'native probe or mode mismatch')
            natural_exit = 'unobserved' if probe.get('exit_code_observed') is False else 'not_assessed'
            cleanup = probe.get('cleanup_terminate_ok')
        else:
            require(after_doc.get('returncode') == 0 and before_doc.get('exe_before') is None,
                    'public receipt status mismatch')
            natural_exit, cleanup = 'not_assessed', None
        raw_bytes = raw.read_bytes()
        require(hashlib.sha256(raw_bytes).hexdigest() == raw_hash, 'raw changed while reading')
        text = raw_bytes.decode('utf-16')
        require(text == texts[mode], 'comparison text differs from mode raw')
        decoded.append(text)
        fixture_bytes, config_bytes = fixture.read_bytes(), config.read_bytes()
        require(hashlib.sha256(fixture_bytes).hexdigest() == fixture_hash and
                hashlib.sha256(config_bytes).hexdigest() == config_hash,
                'input changed while reading')
        fixtures.append(fixture_bytes)
        configs.append(config_bytes)
        modes.append({'name': mode, 'fixture_sha256': fixture_hash, 'config_sha256': config_hash,
                      'outputlog_sha256': raw_hash, 'receipt': 'declared hashes matched',
                      'natural_exit': natural_exit, 'cleanup_terminate_ok': cleanup,
                      'public_returncode': after_doc.get('returncode') if mode == 'public-01' else None})
    require(fixtures[0] == fixtures[1] == fixtures[2] and configs[0] == configs[1] == configs[2],
            'shared input bytes differ')
    require(decoded[0] == decoded[1] == decoded[2], 'mode output differs')
    require(len(set(pyz)) == 1, 'recorded PyEmuera pins differ')
    config_lines = configs[0].decode('cp932').splitlines()
    widths = [line.split(':', 1)[1].strip() for line in config_lines
              if ':' in line and line.split(':', 1)[0].strip() == 'PRINTCの文字数']
    require(widths == ['25'], 'column width config differs or is ambiguous')
    fixture_lines = [line for line in fixtures[0].decode('utf-8-sig').splitlines()
                     if line.strip() and not line.lstrip().startswith(';')]
    expected_fixture = ['@SYSTEM_TITLE', 'RESULT = 777', 'RESULTS = SENTINEL']
    for n in ('PRINTC', 'PRINTLC'):
        for suffix, value, _ in values:
            ident = n+'_'+suffix
            expected_fixture.extend(['PRINTL '+ident+'_BEGIN', n+(' '+value if value else ''),
                                     'PRINTL |'+ident+'_END',
                                     'PRINTFORML '+ident+'_STATE R={RESULT} S=[%RESULTS%]'])
    expected_fixture.extend(['PRINTL COLUMN_DONE', 'OUTPUTLOG', 'QUIT'])
    require(fixture_lines == expected_fixture, 'fixture condition body or execution order mismatch')
    lines = decoded[0].splitlines()
    cursor, fixture_cursor, selected = 0, 0, []
    for n in ('PRINTC', 'PRINTLC'):
        for suffix, value, width in values:
            ident = n+'_'+suffix
            command = n + (' '+value if value else '')
            begin, end = 'PRINTL '+ident+'_BEGIN', 'PRINTL |'+ident+'_END'
            require(fixture_lines.count(begin) == fixture_lines.count(end) == 1,
                    'fixture markers missing or ambiguous')
            try:
                start = fixture_lines.index(begin, fixture_cursor)
                stop = fixture_lines.index(end, start+1)
            except ValueError:
                raise EvidenceError('fixture condition order mismatch')
            require(fixture_lines[start+1:stop] == [command], 'fixture condition body mismatch')
            state = 'PRINTFORML '+ident+'_STATE R={RESULT} S=[%RESULTS%]'
            require(stop+1 < len(fixture_lines) and fixture_lines[stop+1] == state,
                    'fixture state observation missing')
            fixture_cursor = stop+2
            rendered = '' if not value else value.rjust(25) if n == 'PRINTC' else value.ljust(25)+' '
            for wanted in (ident+'_BEGIN', rendered+'|'+ident+'_END', ident+'_STATE R=777 S=[SENTINEL]'):
                try:
                    cursor = lines.index(wanted, cursor)+1
                except ValueError:
                    raise EvidenceError('column output marker, padding or sentinel mismatch')
            if n == target['name']:
                selected.append({'condition': suffix, 'input_text': value,
                                 'rendered_text': rendered, 'RESULT': 777, 'RESULTS': 'SENTINEL'})
    require('COLUMN_DONE' in lines[cursor:], 'column completion marker absent')
    return {'status': 'PARTIAL', 'target': target, 'source_outcome': row.get('row_outcome'),
            'declared_outcome': doc['comparison_outcome'], 'acceptance_schema': doc['schema'],
            'case_ids': [expected_case], 'shared_fixture': True, 'modes': modes,
            'selected_observations': selected,
            'recorded_pyz_sha256': pyz[0], 'checked': checks, 'gaps': row['gaps'],
            'limitations': ['Selected PRINTC/PRINTLC serialized text and sentinels only; no pixel/UI equality.',
                            'Two Native and one public modes share the fixture; cases and conditions are not separate launches.',
                            'Native natural exit was not established by this check.',
                            'PyEmuera pyz bytes are not included in the manifest or verified by this adapter.',
                            'Original requirements and broader acceptance semantics remain unproved.',
                            'The original recorded verdict is not changed.']}


def adapt(root, audit_path, expected_audit_sha, kind, name):
    root = Path(root).absolute()
    no_link(root)
    require(root.is_dir(), 'root is not a directory')
    checks = []
    audit = pinned(root, audit_path, expected_audit_sha, 'audit_snapshot', checks)
    data = parse_json(audit, expected_audit_sha)
    require(isinstance(data,dict) and data.get('schema')==AUDIT_SCHEMA and isinstance(data.get('rows'),list),
            'unsupported audit envelope')
    target = {'kind':kind,'name':name}
    require(all(isinstance(v,str) and v for v in target.values()), 'invalid typed target')
    rows = [x for x in data['rows'] if isinstance(x,dict) and targets_equal(x.get('target'),target)]
    require(len(rows)==1, 'target missing or ambiguous')
    row = rows[0]
    require(isinstance(row.get('gaps'),list) and isinstance(row.get('errors'),list), 'audit gap/error fields absent')
    require(not row['errors'], 'source audit recorded errors')
    acceptance = row.get('acceptance')
    if acceptance is None:
        return {'status':'UNSUPPORTED', 'target':target, 'source_outcome':row.get('row_outcome'),
                'checked':checks, 'gaps':row['gaps'], 'limitations':['no recognized typed acceptance']}
    require(isinstance(acceptance,dict) and isinstance(acceptance.get('record_pointer'),str), 'unsupported acceptance pointer')
    schema = acceptance.get('schema')
    if schema not in SUPPORTED:
        return {'status':'UNSUPPORTED', 'target':target, 'source_outcome':row.get('row_outcome'),
                'checked':checks, 'gaps':row['gaps'], 'limitations':['unsupported acceptance schema']}
    if schema == 'target-finite-comparison-adjudication-1' and not (
            kind == 'command_or_syntax' and name in ('PRINTC', 'PRINTLC')):
        return {'status':'UNSUPPORTED', 'target':target, 'source_outcome':row.get('row_outcome'),
                'checked':checks, 'gaps':row['gaps'],
                'limitations':['column layout is restricted to PRINTC and PRINTLC']}
    acceptance_file = pinned(root,acceptance.get('path'),acceptance.get('sha256'),'acceptance',checks)
    document = parse_json(acceptance_file, acceptance['sha256'])
    doc = resolve_pointer(document, acceptance['record_pointer'])
    require(isinstance(doc,dict) and doc.get('schema')==schema and targets_equal(doc.get('target'),target),
            'acceptance schema or typed target mismatch')
    if schema == 'target-finite-comparison-adjudication-1':
        return column_fixture(root, audit_path, data, row, doc, target, checks)
    case_ids = doc.get('case_ids')
    modes = []
    limitations = ['partial integrity/identity checks only; original requirements and compatibility are not reproven',
                   'registered modes do not establish process launch counts',
                   'case-role links are read from the pinned audit snapshot, not independently rechecked against the case register',
                   'acceptance remains the source record; no verdict is upgraded']
    outcome = doc.get('comparison_outcome')
    if schema == 'parent-target-finite-scope-adjudication-1':
        require(doc.get('decision')=='necessary_comparison_complete', 'unsupported decision')
        require(outcome==row.get('row_outcome'), 'acceptance outcome differs from audit row')
        compfile = pinned(root,doc.get('comparison_path'),doc.get('comparison_sha256'),'comparison',checks)
        comp = parse_json(compfile,doc['comparison_sha256'])
        require(isinstance(comp,dict) and comp.get('schema')=='native-public-command-comparison-1' and targets_equal(comp.get('target'),target),
                'comparison schema or typed target mismatch')
        require(comp.get('scoped_outcome')==outcome, 'comparison outcome differs')
        case_ids = comp.get('case_ids')
        require_case_binding(row,case_ids)
        fixture = comp.get('fixture')
        require(isinstance(fixture,dict), 'fixture missing')
        pinned(root,fixture.get('path'),fixture.get('sha256'),'fixture',checks)
        require(isinstance(fixture.get('config_sha256'),str) and HEX.fullmatch(fixture['config_sha256']), 'missing config pin')
        runs = comp.get('runs')
        require(isinstance(runs,dict) and runs, 'runs missing')
        comp_rel = safe_name(doc['comparison_path'])
        base = PurePosixPath(comp_rel).parent
        for mode, run in sorted(runs.items()):
            require(isinstance(mode,str) and isinstance(run,dict), 'invalid mode')
            if re.fullmatch(r'native-final-[0-9]{2}',mode):
                logname, config_key = 'emuera.log','config_sha256'
            elif re.fullmatch(r'public-receipted-[0-9]{2}',mode):
                logname, config_key = 'outputlog.bin','config_sha256_before_after'
            else:
                raise EvidenceError('unsupported comparison mode: '+mode)
            require(run.get('fixture_sha256_before_after')==fixture['sha256'], 'fixture pin differs by mode')
            require(run.get(config_key)==fixture['config_sha256'], 'config pin differs by mode')
            pinned(root,(base/mode/logname).as_posix(),run.get('outputlog_sha256'),'mode_output:'+mode,checks)
            pinned(root,(base/mode/'emuera.config').as_posix(),run.get(config_key),'mode_config:'+mode,checks)
            receipt = safe_name(run.get('receipt'))
            require(receipt == mode+'/receipt.json', 'unsupported receipt locator')
            # Receipt has a locator but no declared SHA in this comparison: no pin is invented.
            modes.append({'name':mode,'outputlog':'hash_matched','config':'hash_matched','receipt':'unpinned'})
        limitations += ['receipt locators have no declared SHA in this comparison',
                        'comparison is not promoted to an independently declared readback',
                        'Native natural exit is not inferred']
    elif schema == 'phase2-target-parent-acceptance/v1':
        require(doc.get('accepted') is True, 'acceptance flag is not true')
        require_case_binding(row,case_ids)
        refs = row.get('readbacks')
        require(isinstance(refs,list) and len(refs)==1 and isinstance(refs[0],dict), 'expected one declared readback')
        rbfile = pinned(root,refs[0].get('path'),refs[0].get('sha256'),'readback',checks)
        rb = parse_json(rbfile,refs[0]['sha256'])
        require(isinstance(rb,dict) and rb.get('acceptance_sha256')==acceptance['sha256'], 'readback backlink mismatch')
        if rb.get('schema')=='parent-acceptance-readback-1':
            require(targets_equal(rb.get('target'),target), 'readback typed target mismatch')
            require(rb.get('case_ids')==case_ids, 'readback case IDs differ')
            require(rb.get('comparison_outcome')==row.get('row_outcome'), 'readback outcome differs from audit row')
            outcome = rb['comparison_outcome']
            limitations.append('readback outcome is a recorded parent classification, not an independent raw replay')
        elif 'schema' not in rb and 'case_ids_registered_for_exact_target' in rb:
            require(rb.get('valid') is True and rb.get('case_ids_registered_for_exact_target')==case_ids,
                    'readback case IDs or validity differ')
            for side in ('native','public'):
                key = side+'_replicates'
                require(type(rb.get(key)) is int and rb[key]>=0, 'invalid recorded replicate count')
                modes.append({'name':side,'recorded_replicates':rb[key], 'individual_raw_pins':'not provided here'})
            outcome = None
            limitations.append('readback has no declared outcome; audit row outcome is not promoted into it')
        else:
            raise EvidenceError('unsupported phase2 readback layout')
        limitations += ['raw artifacts and unlocated hash-only references were not verified',
                        'Native natural exit is not inferred']
    else:
        require(doc.get('decision')=='necessary_comparison_complete' and outcome==row.get('row_outcome'),
                'current acceptance decision or outcome differs')
        require_case_binding(row,case_ids)
        ref = doc.get('readback')
        require(isinstance(ref,dict), 'current readback reference missing')
        audit_refs = row.get('readbacks')
        require(isinstance(audit_refs,list) and len(audit_refs)==1 and
                safe_name(audit_refs[0].get('path'))==safe_name(ref.get('path')) and
                audit_refs[0].get('sha256')==ref.get('sha256'), 'audit/readback reference mismatch')
        readback_file = pinned(root,ref.get('path'),ref.get('sha256'),'readback',checks)
        readback = parse_json(readback_file,ref['sha256'])
        require(isinstance(readback,dict) and isinstance(readback.get('observations'),list), 'unsupported current readback')
        for case in case_ids:
            found = [x for x in readback['observations'] if isinstance(x,dict) and x.get('case_id')==case]
            require(len(found)==1 and isinstance(found[0].get('targets'),list) and name in found[0]['targets'],
                    'current observation identity mismatch')
            runs = found[0].get('runs')
            require(isinstance(runs,list) and runs, 'current modes missing')
            seen = set()
            for run in runs:
                mode = run.get('mode')
                require(isinstance(mode,str) and re.fullmatch(r'(?:native|public)-[0-9]{2}',mode) and mode not in seen,
                        'unsupported or duplicate current mode')
                seen.add(mode)
                for role in ('raw','stderr','receipt','probe'):
                    item = run.get(role)
                    if role=='probe' and item is None:
                        continue
                    require(isinstance(item,dict), 'mode artifact missing: '+role)
                    pinned(root,item.get('path'),item.get('sha256'),mode+':'+role,checks)
                modes.append({'name':mode,'case_id':case,'artifacts':'declared hashes matched'})
        limitations += ['other readback observations and artifacts were not checked',
                        'readback target-name list is not an independent typed-target proof',
                        'Native natural exit is not inferred']
    return {'status':'PARTIAL', 'target':target, 'source_outcome':row.get('row_outcome'),
            'declared_outcome':outcome, 'acceptance_schema':schema, 'case_ids':case_ids,
            'modes':modes, 'checked':checks, 'gaps':row['gaps'], 'limitations':limitations}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--audit',required=True,help='audit snapshot path relative to root')
    p.add_argument('--audit-sha256',required=True)
    p.add_argument('--kind',required=True)
    p.add_argument('--name',required=True)
    a=p.parse_args(argv)
    try:
        result = adapt(a.root,a.audit,a.audit_sha256,a.kind,a.name)
        print(json.dumps(result,ensure_ascii=True,indent=2))
        return 2  # PARTIAL and UNSUPPORTED are never reported as a pass.
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as exc:
        print(json.dumps({'status':'INVALID','error':str(exc)},ensure_ascii=True),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
