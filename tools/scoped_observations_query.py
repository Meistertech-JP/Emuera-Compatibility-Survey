"""Locate pinned, finite saved-observation projections; no raw replay."""
import hashlib
import json
from pathlib import Path
import stat

EIGHT = 'evidence/eight-scoped-observations-20261117'
DOLOOP = 'evidence/doloop259-20261117'
LEGACY50 = 'evidence/legacy50-selected-observations-20261117'
LEGACY50_PIN = ('file-set-manifest.json', 'ab2450876b2a2cad62c2e60744eb83f8e9779b1501f7016fa252344304b68101',
                'bundle', frozenset({'README.ja.md', 'README.md', 'selected-observations.json'}))
PINS = {
    EIGHT: ('MANIFEST.json', 'e80ffb9ccd0be5917fb85919aa129232fc733a8825c4f965872804607550a119',
            'observation', frozenset({'README.en.md', 'README.ja.md', 'SOURCE-INDEX.json',
                                      'SOURCE-INDEX.md', 'observations.json'})),
    DOLOOP: ('manifest.json', 'c46dcbaa2bbd57d6665fa17a498a9c497a3e73dbe3cbd2a4bb4c1307deb7e7e8',
             'evidence', frozenset({'README.ja.md', 'README.md', 'observation.json', 'source-digests.json'})),
}
# The eight-record projection lacks typed keys. This reviewed mapping is from
# the matching case-register core snapshot; it is independent of row numbers.
EIGHT_TARGETS = {
    'PRINTDWEMPTY01': (('command_or_syntax', 'PRINTDW'),),
    'PRINTDWSPACE01': (('command_or_syntax', 'PRINTDW'),),
    'ARRAY_BOUNDARY_NORMAL_CORRECTED_20261115': (('expression_function', 'MAXARRAY'), ('expression_function', 'MINARRAY'), ('expression_function', 'SUMARRAY')),
    'LEVEL_BOUNDARY_GETPALAMLV_NEGATIVE_20261115': (('expression_function', 'GETPALAMLV'),),
    'LEVEL_BOUNDARY_GETPALAMLV_SIZEPLUS1_20261115': (('expression_function', 'GETPALAMLV'),),
    'LEVEL_BOUNDARY_GETEXPLV_NEGATIVE_20261115': (('expression_function', 'GETEXPLV'),),
    'LEVEL_BOUNDARY_GETEXPLV_SIZEPLUS1_20261115': (('expression_function', 'GETEXPLV'),),
    'SAVECHARA_FINITE_BOUNDARIES_EVALUATION_ORDER_20261115': (('command_or_syntax', 'SAVECHARA'),),
}
DO_CASE = 'DOLOOP259_BREAK_SUPPRESSION'
DO_TARGETS = (('command_or_syntax', 'DO'), ('command_or_syntax', 'LOOP'),
              ('structural_syntax', 'DO'), ('structural_syntax', 'LOOP'))
REGISTER_SNAPSHOT_SHA256 = '8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94'
REGISTER_CORE_SHA256 = 'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903'
REGISTER_MANIFEST_SHA256 = 'dabf8f4509100ebd19689fac92fe88d2aba7a5843a2542134c5d91741b88fddb'
REGISTER = 'evidence/case-register-2898-20261117'
RAW_SCOPE = 'Selected saved projection; original raw files are not included; no new execution or independent reproduction.'


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _json(data):
    def reject(_):
        raise ValueError('non-finite JSON value')
    return json.loads(data.decode('utf-8'), object_pairs_hook=_pairs, parse_constant=reject)


def _safe_path(root, relative):
    """Reject symlinks and Windows reparse points in every existing component."""
    path = root
    parts = relative.split('/')
    if any(p in ('', '.', '..') or '\\' in p for p in parts):
        raise ValueError('unsafe path')
    for part in [None, *parts]:
        if part is not None:
            path = path / part
        try:
            info = path.lstat()
        except FileNotFoundError:
            return None
        if (stat.S_ISLNK(info.st_mode) or
                getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)):
            raise ValueError('link or reparse point')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes root')
    return path


def _register(root):
    """Only use the reviewed mapping with its exact, internally valid snapshot."""
    try:
        directory = _safe_path(root, REGISTER)
        if directory is None:
            return None, 'REGISTER_NOT_INSTALLED'
        if not directory.is_dir():
            return None, 'REGISTER_INCONSISTENT'
        paths = {name: _safe_path(root, REGISTER + '/' + name)
                 for name in ('manifest.json', 'core.jsonl', 'cases.jsonl')}
        if any(p is None for p in paths.values()):
            return None, 'REGISTER_MISSING_FILES'
        if any(not p.is_file() for p in paths.values()):
            return None, 'REGISTER_INCONSISTENT'
        manifest_bytes = paths['manifest.json'].read_bytes()
        manifest = _json(manifest_bytes)
        if (not isinstance(manifest, dict) or manifest.get('schema') not in
                ('case-register-neutral-screened-draft-v1', 'case-register-neutral-screened-draft-v2')):
            return None, 'REGISTER_INCONSISTENT'
        payload = {n: paths[n].read_bytes() for n in ('core.jsonl', 'cases.jsonl')}
        for name, raw in payload.items():
            entry = manifest['files'][name]
            if (type(entry['size']) is not int or len(raw) != entry['size'] or
                    hashlib.sha256(raw).hexdigest() != entry['sha256']):
                return None, 'REGISTER_INCONSISTENT'
        if (hashlib.sha256(manifest_bytes).hexdigest() != REGISTER_MANIFEST_SHA256 or
                hashlib.sha256(payload['core.jsonl']).hexdigest() != REGISTER_CORE_SHA256 or
                hashlib.sha256(payload['cases.jsonl']).hexdigest() != REGISTER_SNAPSHOT_SHA256):
            return None, 'REGISTER_SNAPSHOT_MISMATCH'
        cores = [_json(line) for line in payload['core.jsonl'].splitlines()]
        details = [_json(line) for line in payload['cases.jsonl'].splitlines()]
        if len(cores) != 2898 or len(details) != len(cores) or manifest.get('records') != len(cores):
            return None, 'REGISTER_INCONSISTENT'
        rows = {}
        for core, detail in zip(cores, details):
            cid = core['case_id']
            if cid in rows or any(core[key] != detail[key] for key in ('case_id', 'targets', 'scenario_verdict')):
                return None, 'REGISTER_INCONSISTENT'
            rows[cid] = core
        for cid, targets in (*EIGHT_TARGETS.items(), (DO_CASE, DO_TARGETS)):
            if tuple((v['kind'], v['name']) for v in rows[cid]['targets']) != targets:
                return None, 'REGISTER_INCONSISTENT'
        return rows, 'AVAILABLE'
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, UnicodeError):
        return None, 'REGISTER_INCONSISTENT'


def _load_bundle(root, relative, pin=None):
    name, expected, root_name, expected_files = pin if pin is not None else PINS[relative]
    try:
        folder = _safe_path(root, relative)
        if folder is None:
            return None, {'state': 'NOT_INSTALLED'}
        if not folder.is_dir():
            raise ValueError('unsafe bundle directory')
        missing = [f for f in (name, *sorted(expected_files))
                   if _safe_path(root, relative + '/' + f) is None]
        if missing:
            return None, {'state': 'MISSING_FILES', 'files': [relative + '/' + f for f in missing]}
        manifest_path = folder / name
        if not manifest_path.is_file():
            raise ValueError('unsafe manifest')
        raw = manifest_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('manifest pin mismatch')
        manifest = _json(raw)
        if (manifest.get('schema') != 'selected-file-set.v1' or manifest.get('roots') != [root_name]
                or manifest.get('manifest_location') != {'root': root_name, 'path': name}):
            raise ValueError('manifest structure')
        entries = manifest.get('files')
        if not isinstance(entries, list) or len(entries) != len(expected_files):
            raise ValueError('manifest entries')
        files = {}
        for entry in entries:
            if not isinstance(entry, dict) or entry.get('root') != root_name:
                raise ValueError('manifest entry')
            rel = entry.get('path')
            if rel not in expected_files or rel in files:
                raise ValueError('manifest path')
            source = folder / rel
            if not source.is_file():
                raise ValueError('unsafe entry')
            data = source.read_bytes()
            if (type(entry.get('size')) is not int or len(data) != entry['size']
                    or hashlib.sha256(data).hexdigest() != entry.get('sha256')):
                raise ValueError('file hash mismatch')
            files[rel] = data
        return files, {'state': 'AVAILABLE', 'manifest': relative + '/' + name,
                       'manifest_sha256': expected}
    except (OSError, ValueError, TypeError, AttributeError, UnicodeError):
        return None, {'state': 'INCONSISTENT'}


def _match(cid, targets, term, kind):
    by_case = cid.upper() == term
    matched = [{'kind': k, 'name': n} for k, n in targets
               if (kind is None or k.upper() == kind) and (by_case or n.upper() == term)]
    if by_case and kind is None:
        matched = [{'kind': k, 'name': n} for k, n in targets]
    return by_case, matched


def _legacy50_lookup(root, term, kind, case_projection_override=None):
    """Use only this independently pinned selection, never historical acceptance rows."""
    files, state = _load_bundle(root, LEGACY50, LEGACY50_PIN)
    if files is None:
        return [], state
    try:
        folder = _safe_path(root, LEGACY50)
        if {p.name for p in folder.iterdir()} != set(LEGACY50_PIN[3]) | {LEGACY50_PIN[0]}:
            raise ValueError('unexpected bundle member')
        if case_projection_override is not None:
            return [], {'state': 'REGISTER_OVERRIDE_NOT_CHECKED', 'bundle_integrity': 'AVAILABLE',
                        'register_scope': 'EXPLICIT_CASE_PROJECTION_OVERRIDE'}
        doc = _json(files['selected-observations.json'])
        getter, operator, runs = doc['getter'], doc['operator_normal'], doc['runs']
        if (doc['schema'] != 'legacy50-selected-observations/v1' or
                doc['raw_and_fixture_included'] is not False or doc['selected_target_count'] != 27 or
                getter['target_count'] != 14 or getter['case_count'] != 23 or
                operator['target_count'] != 13 or len(getter['cases']) != 23 or
                len(operator['cases']) != 4):
            raise ValueError('selection identity')
        if not isinstance(runs, dict):
            raise ValueError('invalid runs')
        ids, getter_targets, operator_targets, markers = set(), set(), set(), 0
        candidates = []

        def check_case(row):
            cid = row['case_id']
            if not isinstance(cid, str) or not cid or cid.upper() in ids:
                raise ValueError('duplicate or invalid case ID')
            ids.add(cid.upper())
            if row['original_verdict'] not in ('matched_scoped', 'different_scoped'):
                raise ValueError('invalid selected verdict')
            return cid

        def checked_runs(observations, expected_ids):
            if not isinstance(observations, list) or len(observations) != 3:
                raise ValueError('observation count')
            run_ids = [o['run_id'] for o in observations]
            if len(set(run_ids)) != 3 or set(run_ids) != set(expected_ids):
                raise ValueError('shared run binding')
            if [runs[x]['engine'] for x in run_ids].count('Native') != 2 or [runs[x]['engine'] for x in run_ids].count('Py') != 1:
                raise ValueError('run engines')
            if any(runs[x]['natural_exit'] != 'unobserved' for x in run_ids if runs[x]['engine'] == 'Native'):
                raise ValueError('native exit scope')
            return run_ids

        def selected_runs(run_ids):
            # JSON Pointer escaping is required even if the current IDs are simple.
            return [{'pointer': '/runs/' + x.replace('~', '~0').replace('/', '~1'), 'value': runs[x]}
                    for x in run_ids]

        for i, row in enumerate(getter['cases']):
            cid = check_case(row)
            target = row['target']
            key = (target['kind'], target['name'])
            if key[0] not in ('expression_function', 'method_as_command') or not isinstance(key[1], str) or not key[1]:
                raise ValueError('getter target')
            getter_targets.add(key)
            form = row['condition']['form']
            if form not in ('expression', 'method') or (form == 'expression') != (key[0] == 'expression_function'):
                raise ValueError('getter form')
            expected = [f'getter-{form}-native-01', f'getter-{form}-native-02', f'getter-{form}-public-01']
            run_ids = checked_runs(row['observations'], expected)
            if any(not isinstance(o['state'], dict) for o in row['observations']):
                raise ValueError('getter state')
            prefix = '/getter/cases/' + str(i)
            by_case, targets = _match(cid, (key,), term, kind)
            if targets:
                candidates.append((cid, by_case, targets, row, prefix,
                    [{'pointer': prefix + '/' + k, 'value': row[k]} for k in ('condition', 'observations', 'limits')]
                    + [{'pointer': '/getter/' + k, 'value': getter[k]} for k in
                       ('configured_native_rgb', 'observation_field_meanings', 'unobserved')]
                    + selected_runs(run_ids)))

        for i, row in enumerate(operator['cases']):
            cid = check_case(row)
            if not cid.startswith('OPNORMAL273_E'):
                raise ValueError('operator case')
            fixture = cid.split('_')[-1]
            expected = [fixture + '-retained-native-1', fixture + '-retained-native-2', fixture + '-fresh-py']
            prefix = '/operator_normal/cases/' + str(i)
            found, targets, used = [], [], []
            marker_names = set()
            for j, marker in enumerate(row['marker_observations']):
                key = (marker['target']['kind'], marker['target']['name'])
                if key[0] != 'operator' or not isinstance(key[1], str) or not key[1]:
                    raise ValueError('operator target')
                operator_targets.add(key)
                name = marker['marker']
                if not isinstance(name, str) or not name or name in marker_names:
                    raise ValueError('duplicate marker')
                marker_names.add(name)
                if not isinstance(marker['condition_statements'], list) or not isinstance(marker['referenced_helpers'], dict):
                    raise ValueError('marker condition')
                run_ids = checked_runs(marker['observations'], expected)
                if any(not isinstance(o['observed_marker'], str) for o in marker['observations']):
                    raise ValueError('marker observation')
                markers += 1
                by_case, matched = _match(cid, (key,), term, kind)
                if matched:
                    found.append({'pointer': prefix + '/marker_observations/' + str(j), 'value': marker})
                    if matched[0] not in targets:
                        targets.append(matched[0])
                    used = run_ids
            if found:
                candidates.append((cid, cid.upper() == term, targets, row, prefix,
                                   found + [{'pointer': prefix + '/' + key, 'value': row[key]}
                                            for key in ('initial_topology', 'stderr_notice', 'limitations') if key in row]
                                   + [{'pointer': '/operator_normal/' + key, 'value': operator[key]}
                                      for key in ('marker_field_meanings', 'unobserved')]
                                   + selected_runs(used)))

        if len(getter_targets) != 14 or len(operator_targets) != 13 or markers != 71:
            raise ValueError('selected target or marker count')
        path = LEGACY50 + '/selected-observations.json'
        result = [{'bundle': 'legacy50_selected', 'case_id': cid,
                   'match_basis': 'CASE_ID' if by_case else 'TYPED_TARGET',
                   'matched_targets': targets, 'original_verdict': row['original_verdict'],
                   'record': {'path': path, 'pointer': prefix}, 'selected': selected,
                   'record_scope': 'The record pointer identifies the case; for operator target searches only selected markers match that target.',
                   'raw_scope': 'Selected projection values only; raw logs, fixtures and receipts are not included; no new execution or independent reproduction.',
                   'execution_scope': 'Run IDs are shared across rows or markers in the same fixture, not independent runs per target. Native natural exit and exit code are unobserved.',
                   'historical_acceptance_scope': 'Later selected observations; the earlier typed acceptance source remains unidentified.'}
                  for cid, by_case, targets, row, prefix, selected in candidates]
        return result, state
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, UnicodeError):
        return [], {'state': 'INCONSISTENT'}


def lookup(term, root, kind=None, case_projection_override=None):
    """Return (matches, independent bundle states); exact IDs or typed names."""
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, term = term.split(':', 1)
        if kind and kind != typed_kind:
            return [], {'eight_scoped': {'state': 'INVALID_QUERY'},
                        'doloop259': {'state': 'INVALID_QUERY'},
                        'legacy50_selected': {'state': 'INVALID_QUERY'}}
        kind = typed_kind
    root = Path(root)
    states, matches = {}, []
    # The parent query may use an arbitrary separately pinned projection. Do
    # not silently compare this module's current snapshot to a different one.
    if case_projection_override is not None:
        register, register_state = None, 'REGISTER_OVERRIDE_NOT_CHECKED'
    else:
        register, register_state = _register(root)
    for label, folder in (('eight_scoped', EIGHT), ('doloop259', DOLOOP)):
        files, state = _load_bundle(root, folder)
        states[label] = state
        if files is None:
            continue
        if register is None:
            states[label] = {'state': register_state, 'bundle_integrity': 'AVAILABLE',
                             'register_scope': ('EXPLICIT_CASE_PROJECTION_OVERRIDE' if
                                 case_projection_override is not None else 'CANDIDATE_REGISTER')}
            continue
        try:
            if folder == EIGHT:
                doc = _json(files['observations.json'])
                records = doc['records']
                ids = [r['case_id'] for r in records]
                if (doc.get('schema') != 'eight-case-independent-observations.v1'
                        or doc.get('source_register_sha256') != REGISTER_SNAPSHOT_SHA256
                        or len(ids) != 8 or len(set(ids)) != 8 or set(ids) != set(EIGHT_TARGETS)):
                    raise ValueError('eight case identity')
                found = []
                for i, row in enumerate(records):
                    cid = row['case_id']
                    if row['scenario_verdict'] != register[cid]['scenario_verdict']:
                        raise ValueError('register verdict mismatch')
                    by_case, targets = _match(cid, EIGHT_TARGETS[cid], term, kind)
                    if not targets:
                        continue
                    # Return the original values plus their precise JSON pointers.
                    found.append({'bundle': label, 'case_id': cid,
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_TARGET',
                        'matched_targets': targets, 'original_verdict': row['scenario_verdict'],
                        'record': {'path': folder + '/observations.json', 'pointer': '/records/' + str(i)},
                        'selected': [{'pointer': '/records/' + str(i) + '/' + key, 'value': row[key]}
                                     for key in ('facts', 'run_counts')],
                        'raw_scope': RAW_SCOPE,
                        'execution_scope': 'Run counts are per record or per condition as recorded; ARRAY six subobservations share the same runs, not six independent sets.'})
            else:
                doc = _json(files['observation.json'])
                typed = tuple((x['kind'], x['name']) for x in doc['typed_targets'])
                if (doc['case_id'] != DO_CASE or typed != DO_TARGETS or
                        doc['original_verdict'] != register[DO_CASE]['scenario_verdict']):
                    raise ValueError('DOLOOP identity')
                by_case, targets = _match(DO_CASE, typed, term, kind)
                found = []
                if targets:
                    found.append({'bundle': label, 'case_id': DO_CASE,
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_TARGET',
                        'matched_targets': targets, 'original_verdict': doc['original_verdict'],
                        'record': {'path': folder + '/observation.json', 'pointer': ''},
                        'selected': [{'pointer': '/' + key, 'value': doc[key]} for key in
                                     ('conditions', 'observations', 'runs', 'unobserved', 'limitations')],
                        'raw_scope': RAW_SCOPE,
                        'execution_scope': 'One case and shared fixture: two Native and one public run; four typed targets do not imply four executions.'})
            matches.extend(found)
        except (KeyError, ValueError, TypeError, AttributeError, UnicodeError):
            states[label] = {'state': 'INCONSISTENT'}
    legacy, states['legacy50_selected'] = _legacy50_lookup(root, term, kind, case_projection_override)
    matches.extend(legacy)
    return matches, states
