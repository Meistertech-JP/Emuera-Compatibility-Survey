
"""Collect case-bound observations from the publication candidate."""
from collections import defaultdict
from functools import cache
from hashlib import sha256
import json
from pathlib import PurePosixPath
import re

BATCH_INDEXES = ('csv-numeric-45', 'printdata-61', 'remaining-96', 'selected-51',
                 'target-priority-28', 'print-kd-shared-82', 'multi-group-101',
                 'multi-group-second-72')
# Each tuple names a reviewed case collection and its case-level observation fields.
COLLECTIONS = (
    ('compound-trailing-comma', 'records.json', 'records', 'modes recorded_comparison limitations'),
    ('console-background-24', 'records.json', 'cases', 'native_01_selected_rows native_02_selected_rows public_error_recorded public_target_reach unobserved modes'),
    ('delchara-diagnostics', 'records.json', 'cases', 'selected_checkpoints native_diagnostic py_diagnostic post_error_state modes'),
    ('doloop259', 'observation.json', '.', 'observations runs unobserved limitations'),
    ('eight-scoped-observations', 'observations.json', 'records', 'facts summary_ja summary_en'),
    ('external-additional-16-package', 'evidence/external-additional-observations-20261117/records.json', 'records', 'modes scope'),
    ('external-scalar-29-package', 'evidence/external-scalar-observations-20261117/records.json', 'records', 'native pyemuera comparison limitations'),
    ('find-element-string-64', 'conditions.json', 'conditions', 'observations recorded_comparison'),
    ('graphics-38-cases', 'cases.json', 'cases', 'original later_observations new_cross_engine_verdict'),
    ('graphics-gui-observations', 'cases.json', 'cases', 'native_history selected_history_lines images japanese_summary english_summary py_comparison'),
    ('legacy50-selected-observations', 'selected-observations.json', 'getter.cases', '*'),
    ('legacy50-selected-observations', 'selected-observations.json', 'operator_normal.cases', '*'),
    ('lineisempty-acceptance', 'record.json', '.', 'recorded_selected_lines modes comparison scope_limits'),
    ('loadglobal-corrupt', 'records.json', '.', 'observed evidence_files limitations'),
    ('nine-saved-observations', 'data/records.json', 'cases', 'observation modes scope'),
    ('normal-observation-access', 'observations.json', 'cases', 'observations recorded_comparison_axes'),
    ('operator-264', 'observations.json', 'cases', 'modes diagnostic_text_equal operator_body_credit all_values_equivalence'),
    ('operator-265', 'records.json', 'records', 'modes recorded_comparison limitations'),
    ('operator-normal-6', 'index.json', 'cases', 'native public selected_normal_markers selected_marker_comparison comparison_scope'),
    ('platform-input-16', 'records.json', 'cases', 'native_selected_rows public_selected_rows public_error_code unverified modes'),
    ('printdb15', 'records/case.json', '.', 'comparison_recorded modes limitations'),
    ('spritemove', 'records/cases.json', '*', 'native_selected_observations public_rejection_code public_rejection_phase raw_paths limits'),
    ('spritesetpos', 'records/cases.json', '*', 'native_selected_observations public_rejection_code public_rejection_phase raw_paths limits'),
    ('stopped-state-observations', 'observations.json', 'cases', 'native pyemuera interpretation'),
    ('wait-c15', 'observations.json', 'records', 'markers native_observation native_diagnostic py_diagnostic scope'),
)

OUTPUT_KEYS = {
    'raw', 'raw_path', 'observation_raw', 'native_raw', 'history', 'native_history',
    'raw_paths', 'stdout', 'stderr', 'output_log', 'emuera_log', 'native_log',
    'channels', 'outputs', 'evidence_files', 'images', 'before_crop', 'after_crop',
    'image', 'image_before', 'image_after', 'crop', 'native_crop', 'public_stderr_path',
}
OUTPUT_ROLES = OUTPUT_KEYS | {'raw_stdout', 'raw_stderr', 'outputlog', 'screen', 'log'}
IMAGE_TYPES = {'.png', '.bmp', '.jpg', '.jpeg', '.webp'}
NONOUTPUT = {'fixture', 'config', 'configuration', 'receipt', 'input', 'inputs', 'engine', 'source', 'csv_files'}
PRIVATE_TEXT = re.compile(r'(?i)(?:[a-z]:[\\/](?:users[\\/]|private_dev[\\/])|\\\\\\\\[^\\\s]+\\(?:users|private_dev)\\)')


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines()]


def case_id(row):
    return row.get('case_id') or row.get('registered_case_id') or row.get('registry_case_id')


def pick(row, names):
    return {name: row[name] for name in names.split() if name in row}


def safe_text(value):
    if isinstance(value, str):
        return None if PRIVATE_TEXT.search(value) else value
    if isinstance(value, list):
        return [v for item in value if (v := safe_text(item)) is not None]
    if isinstance(value, dict):
        return {k: v for k, item in value.items() if not PRIVATE_TEXT.search(k)
                and (v := safe_text(item)) is not None}
    return value


def collect(root, survey, native, recovery):
    evidence = root / 'evidence'
    universe = {r['case_id']: r for collection in ('main_scenarios', 'grammar_cases', 'supplemental_modes')
                for r in survey[collection]}
    ids = {name.casefold(): name for name in universe}
    main_ids = {r['case_id'] for r in survey['main_scenarios']}
    records = []
    texts = {}
    sources = defaultdict(set)

    def group(name):
        matches = sorted(evidence.glob(name + '-2026*'))
        if len(matches) != 1:
            raise ValueError(f'Expected one bundle for {name}: {matches}')
        return matches[0]

    @cache
    def read_asset(folder, path, digest, encoding):
        relative = PurePosixPath(path)
        if relative.is_absolute() or any(x in ('..', '.') or ':' in x or '\\' in x for x in relative.parts):
            return None
        full = folder.joinpath(*relative.parts)
        if not full.is_file() or not full.resolve().is_relative_to(evidence.resolve()):
            return None
        body = full.read_bytes()
        observed_hash = sha256(body).hexdigest()
        if digest and observed_hash != digest:
            raise ValueError(f'Observation hash mismatch: {full.relative_to(root)}')
        suffix = full.suffix.lower()
        item = {'path': full.relative_to(root).as_posix(), 'sha256': observed_hash, 'size': len(body)}
        if suffix in IMAGE_TYPES:
            return dict(item, image=True)
        if not body:
            return None
        guesses = ([encoding] if encoding else [])
        if body.startswith((b'\xff\xfe', b'\xfe\xff')):
            guesses.append('utf-16')
        guesses.extend(('utf-8-sig', 'cp932'))
        for codec in guesses:
            try:
                decoded = body.decode(codec)
            except (UnicodeError, LookupError):
                continue
            if any(ord(c) < 32 and c not in '\r\n\t\x1b' for c in decoded) or PRIVATE_TEXT.search(decoded):
                continue
            texts.setdefault(observed_hash, decoded.replace('\r\n', '\n').replace('\r', '\n'))
            return dict(item, encoding=codec)
        return None

    def output_assets(folder, fields):
        found = {}
        def walk(node, label='', mode='', allowed=False):
            if isinstance(node, list):
                for item in node:
                    walk(item, label, mode, allowed)
            elif isinstance(node, dict):
                if isinstance(node.get('mode'), str):
                    mode = node['mode']
                role = node.get('role', label)
                pin = node.get('sha256')
                if not isinstance(pin, str):
                    pin = None
                path = node.get('path')
                if isinstance(path, str) and (allowed or role in OUTPUT_ROLES):
                    walk_path(path, pin, node.get('encoding'), role, mode)
                for field, value in node.items():
                    if field in NONOUTPUT or field in {'path', 'sha256', 'encoding', 'role'}:
                        continue
                    next_mode = field if re.fullmatch(r'(?:native|public|py)(?:[-_][\w-]+)?', field) else mode
                    if field in OUTPUT_KEYS and isinstance(value, str):
                        walk_path(value, node.get(field + '_sha256'), None, field, next_mode)
                    elif isinstance(value, (dict, list)):
                        walk(value, field, next_mode, allowed or field in OUTPUT_KEYS or role in OUTPUT_ROLES)
        def walk_path(path, digest, encoding, role, mode):
            asset = read_asset(folder, path, digest, encoding)
            if asset:
                found[mode, asset['path']] = dict(asset, role=role, mode=mode)
        walk(fields)
        return list(found.values())

    def add(name, source, fields=None, modes=None, shared=False, folder=None, label=None):
        if not isinstance(name, str):
            return
        canonical = ids.get(name.casefold(), name)
        folder = folder or source.parent
        fields = safe_text(fields or {})
        assets = output_assets(folder, {'fields': fields, 'modes': modes or []})
        if not fields and not assets:
            return
        row = {'id': canonical, 'roles': universe.get(canonical, {}).get('targets', []),
               'source': source.relative_to(root).as_posix(), 'fields': fields,
               'assets': assets, 'shared': shared, 'label': label}
        records.append(row)
        sources[row['source']].add(canonical)

    for name in BATCH_INDEXES:
        folder = group(name)
        source = folder / 'index.json'
        doc = load(source)
        cases = {r['case_id']: r for r in doc.get('cases', [])}
        for batch in doc['batches']:
            rows = batch.get('cases') or [cases.get(i, {'case_id': i}) for i in batch['case_ids']]
            for row in rows:
                add(case_id(row), source,
                    pick(row, 'saved_semantic_readback condition interpretation semantics_scope'),
                    batch['modes'], shared=len(rows) > 1)

    adapter = group('observation-adapter-183') / 'data'
    modes = {row['mode_id']: row for row in lines(adapter / 'modes.jsonl')}
    batches = {row['batch_id']: row for row in lines(adapter / 'batches.jsonl')}
    source = adapter / 'cases.jsonl'
    for row in lines(source):
        batch = batches[row['batch_id']]
        add(row['case_id'], source, {}, [modes[m['mode_id']] for m in row['modes'].values()],
            shared=len(batch['case_ids']) > 1)

    for name, filename, selector, fields in COLLECTIONS:
        folder = group(name)
        source = folder / filename
        doc = load(source)
        if selector == '.':
            rows = [doc]
        elif selector == '*':
            rows = doc
        else:
            rows = doc
            for step in selector.split('.'):
                rows = rows[step]
        for row in rows:
            add(case_id(row), source, row if fields == '*' else pick(row, fields),
                folder=folder if name in ('printdb15', 'spritemove', 'spritesetpos') else source.parent)

    for name, filename in (('compound-assignment-10', 'records.json'), ('method-display-state-15', 'index.json'),
                           ('display-state-21', 'bindings.json')):
        folder = group(name)
        source = folder / filename
        doc = load(source)
        if 'conditions' in doc:
            conditions, mode_records = doc['conditions'], doc['modes']
        else:
            conditions = load(folder / 'conditions.json')
            mode_records = load(folder / 'modes.json')['mode_records']
        for row in doc['cases']:
            markers = set(row['condition_markers'])
            add(case_id(row), source, {'selected_conditions': [c for c in conditions if c['marker'] in markers]},
                mode_records, shared=True)

    folder = group('main29')
    for source in sorted(folder.glob('*/stage.json')):
        doc = load(source)
        for row in doc['rows']:
            add(case_id(row), source, pick(row, 'native py native_repeats_agree'), shared=len(doc['rows']) > 1)
    folder = group('legacy11')
    for source in sorted(folder.glob('cases/*/record.json')):
        row = load(source)
        add(case_id(row), source, pick(row, 'runs public_stderr_path public_stderr_sha256 comparison_limits'), folder=folder)

    for name in ('syntax-supplemental', 'prints-printsl'):
        folder = group(name)
        source = folder / 'manifest.json'
        doc = load(source)
        cases = doc['cases']
        for row in (cases.values() if isinstance(cases, dict) else cases):
            add(case_id(row), source, pick(row, 'original_conclusion comparison runs'))

    folder = group('strlen-control')
    source = folder / 'records/result.json'
    relationship = load(folder / 'records/relationship.json')
    output = load(source)
    output['outputs'] = [item for item in load(folder / 'manifest.json')['artifacts']
                         if item['path'].startswith('raw/')]
    add(case_id(relationship), source, output, folder=folder)

    folder = group('twaitzero-observation')
    source = folder / 'manifest.json'
    files = [item for item in load(source)['files'] if item['path'].startswith('raw/')]
    add('TWAITZERO01', source, {
        'source_note': 'Saved screen after the Enter probe and PyEmuera output. '
                       'Native natural exit and actual input consumption were not established.',
        'outputs': files,
    })

    # These later run descriptions do not give an exact registered scenario ID.
    # Keep their records browsable under separate labels and outside the denominator.
    folder = group('wait-release')
    source = folder / 'observations.json'
    for row in load(source)['records']:
        add('WAIT-RELEASE/' + row['command'], source, row)

    folder = group('graphics-native-saved')
    source = folder / 'manifest.json'
    runs = defaultdict(list)
    for item in load(source)['files']:
        parts = PurePosixPath(item['path']).parts
        if len(parts) == 4 and parts[0] == 'assets' and parts[2] == 'raw':
            runs[parts[1]].append(dict(item, mode=PurePosixPath(parts[3]).stem))
    for condition, outputs in sorted(runs.items()):
        add('GRAPHICS-NATIVE/' + condition, source, {'outputs': outputs})

    # A registered case counts once regardless of the number of bundles, modes, or repeats.
    pinned_native = {ids.get(row['id'].casefold(), row['id']) for row in native['rows']
                     if row['observations'] or any(
                         a['role'] in OUTPUT_ROLES and (a['sha256'] in native['texts'] or a['role'].startswith('image'))
                         for m in row['native'] + row['py'] for a in m['assets'])}
    recovery_ids = {ids.get(row['id'].casefold(), row['id']) for row in recovery if
                    (row['type'] != 'projection' and row['fields']) or row['fields'].get('recovered')}
    with_result = pinned_native | recovery_ids | {row['id'] for row in records}
    with_raw = {row['id'] for row in records if row['assets']} | {
        ids.get(row['id'].casefold(), row['id']) for row in native['rows'] if any(
            a['role'] in OUTPUT_ROLES and (a['sha256'] in native['texts'] or a['role'].startswith('image'))
            for m in row['native'] + row['py'] for a in m['assets'])}
    coverage = {
        'mainTotal': len(main_ids), 'mainReadable': len(with_result & main_ids),
        'mainRaw': len(with_raw & main_ids), 'mainExcerptOnly': len((with_result - with_raw) & main_ids),
        'mainPrevious': len((pinned_native | recovery_ids) & main_ids),
        'caseIds': sorted(with_result), 'mainCaseIds': sorted(with_result & main_ids),
        'mainRawCaseIds': sorted(with_raw & main_ids),
        'sourceCounts': {path: len(cases) for path, cases in sorted(sources.items())},
    }
    return {'records': records, 'texts': texts, 'coverage': coverage}

