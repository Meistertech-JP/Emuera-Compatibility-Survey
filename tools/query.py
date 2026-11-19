"""Browse the neutral index without access to the original survey directory."""
from pathlib import Path, PurePosixPath
import argparse
import codecs
import hashlib
import importlib.util
import io
import json
import re
import stat
import sys
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def _stdout_supports_utf8():
    """Configure byte-backed stdout or accept a text-only StringIO."""
    stream = sys.stdout
    if isinstance(stream, io.StringIO):
        return True

    def is_utf8():
        try:
            return codecs.lookup(stream.encoding).name == 'utf-8'
        except Exception:
            return False

    if is_utf8():
        return True
    try:
        stream.reconfigure(encoding='utf-8')
    except Exception:
        return False
    return is_utf8()

def _reference(path, root, *, pointer=None, line=None):
    """Only expose a usable candidate-relative path; overrides may be private."""
    try:
        relative = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        relative = None
    return {'path': relative, 'pointer': pointer, 'line_1based': line,
            'location': 'CANDIDATE_RELATIVE' if relative else 'EXTERNAL_STAGING_NOT_LINKED'}


def _rows(path):
    with path.open(encoding='utf-8') as stream:
        lines = stream.read().splitlines()
    if any(not line.strip() for line in lines):
        raise ValueError('blank JSONL line would make record references ambiguous')
    return [json.loads(line) for line in lines]


_ANCHOR82_MANIFEST_SHA256 = 'c768fd1b034665330f0e250af828803284187e3d2a9623ca962ff1af0c56843b'
_SELECTED51_MANIFEST_SHA256 = 'f118ba30e6a04625764ed29ed0e260ace315748343d78d7e6161b8b10d9e0a78'


class BundleIntegrityError(ValueError):
    """A present collection is incomplete or does not match its pinned inventory."""


def _pinned_bundle_member(path, manifest_sha256, label):
    """Read once and bind a selected file to the pinned bundle manifest, not to a publisher."""
    directory = path.parent
    try:
        info = directory.lstat()
    except FileNotFoundError:
        return None  # The whole collection is not installed.
    reparse = getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)
    def linked(item):
        return stat.S_ISLNK(item.st_mode) or bool(getattr(item, 'st_file_attributes', 0) & reparse)
    if linked(info) or not stat.S_ISDIR(info.st_mode):
        raise BundleIntegrityError(label + ' bundle directory is unavailable or unsafe')
    try:
        def read_regular(member):
            item = member.lstat()
            if linked(item) or not stat.S_ISREG(item.st_mode):
                raise BundleIntegrityError(label + ' bundle file is unavailable or unsafe')
            return member.read_bytes()
        manifest_bytes = read_regular(directory / 'manifest.json')
        if hashlib.sha256(manifest_bytes).hexdigest() != manifest_sha256:
            raise BundleIntegrityError(label + ' manifest pin mismatch')
        manifest = json.loads(manifest_bytes)
        if not isinstance(manifest, dict) or manifest.get('schema') != 'selected-file-set.v1' or not isinstance(manifest.get('files'), list):
            raise BundleIntegrityError(label + ' manifest format invalid')
        entries = [e for e in manifest['files'] if isinstance(e, dict)
                   and e.get('root') == 'evidence' and e.get('path') == path.name]
        if len(entries) != 1:
            raise BundleIntegrityError(label + ' manifest member missing or duplicated')
        payload = read_regular(path)
        entry = entries[0]
        if (type(entry.get('size')) is not int or entry['size'] != len(payload)
                or entry.get('sha256') != hashlib.sha256(payload).hexdigest()):
            raise BundleIntegrityError(label + ' member size or hash mismatch')
        return payload
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BundleIntegrityError(label + ' manifest or member unavailable or invalid') from exc


def _matches(role, term, kind):
    return role.get('name', '').upper() == term and (kind is None or role.get('kind', '').upper() == kind)


_NATIVE_ORACLE_ROOT_MANIFEST_SHA256 = '8402363141573da0d184fb0545005c7072f9b6f85c26f712c029ef96c34bdace'
_NATIVE_ORACLE_SELECTION_SHA256 = '963ad0324142c2cb14695078a8c97df157f062db14f39215fe27af3ad4c3f057'
_NATIVE_ORACLE_OPERATOR268_MANIFEST_SHA256 = '0851d0fe584d85d529e8799f63c0d6c6cda8fb9f02153fd1c0018d0f23260382'
_NATIVE_ORACLE_OPERATOR268_OBSERVATIONS_SHA256 = '5d49f3bad751e2142ea33560b4d19b2642b16a1b3a4d9e75f8481bb4870f7189'
_NATIVE_ORACLE_RELATIVE_ROOT = 'evidence/native-oracle-20261117'
_NATIVE_ORACLE_OPERATOR268_RELATIVE_DIR = 'evidence/operator-268-20261117'


def _native_oracle_path(root, collection_root, relative):
    """Resolve one pinned native-oracle path without permitting traversal or links."""
    if not isinstance(relative, str):
        raise ValueError('unsafe native-oracle relative path')
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or '..' in path.parts
            or '\\' in relative or ':' in relative or path.as_posix() != relative):
        raise ValueError('unsafe native-oracle relative path')
    candidate = collection_root.joinpath(*path.parts)
    if (candidate.is_symlink() or not candidate.is_file()
            or not candidate.resolve().is_relative_to(collection_root.resolve())
            or not candidate.resolve().is_relative_to(root.resolve())):
        raise ValueError('native-oracle member unavailable')
    return candidate


def _native_oracle_result(term, target_term, kind, root):
    """Return only selected native-oracle rows whose index/source pins are readable."""
    collection_root = root / _NATIVE_ORACLE_RELATIVE_ROOT
    manifest = collection_root / 'manifest.json'
    selection = collection_root / 'results/native-oracle-selection.jsonl'

    def unavailable(state, reason, indexed_rows=None):
        return [], {'state': state, 'reason': reason, 'indexed_rows': indexed_rows,
                    'matched_rows': 0, 'publisher_authentication': 'NOT_ESTABLISHED',
                    'scope': 'selected native-oracle index rows only; not a complete raw-observation inventory'}

    try:
        try:
            collection_root.lstat()
        except FileNotFoundError:
            # A broken or non-directory evidence parent is not an uninstalled collection.
            parent = collection_root.parent
            try:
                parent.lstat()
            except FileNotFoundError:
                return unavailable('NOT_PRESENT', 'COLLECTION_DIRECTORY_NOT_FOUND')
            if parent.is_symlink() or not parent.is_dir():
                raise ValueError('native-oracle parent is unavailable')
            return unavailable('NOT_PRESENT', 'COLLECTION_DIRECTORY_NOT_FOUND')
        if (collection_root.is_symlink() or not collection_root.is_dir()
                or manifest.is_symlink() or selection.is_symlink()
                or not manifest.is_file() or not selection.is_file()
                or not manifest.resolve().is_relative_to(root.resolve())
                or not selection.resolve().is_relative_to(root.resolve())):
            raise ValueError('native-oracle index incomplete')
        manifest_bytes = manifest.read_bytes()
        selection_bytes = selection.read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != _NATIVE_ORACLE_ROOT_MANIFEST_SHA256:
            raise ValueError('native-oracle root manifest pin mismatch')
        if hashlib.sha256(selection_bytes).hexdigest() != _NATIVE_ORACLE_SELECTION_SHA256:
            raise ValueError('native-oracle selection pin mismatch')
        root_manifest = json.loads(manifest_bytes)
        if root_manifest.get('schema') != 'selected-file-set.v1':
            raise ValueError('native-oracle root manifest schema mismatch')
        member_rows = root_manifest.get('files')
        if not isinstance(member_rows, list):
            raise ValueError('native-oracle root manifest entries missing')
        members = {x['path']: x for x in member_rows}
        if len(members) != len(member_rows):
            raise ValueError('duplicate native-oracle manifest path')
        index_entry = members.get('results/native-oracle-selection.jsonl')
        if (not index_entry or index_entry.get('sha256') != _NATIVE_ORACLE_SELECTION_SHA256
                or index_entry.get('size') != len(selection_bytes)):
            raise ValueError('native-oracle selection manifest binding mismatch')
        lines = selection_bytes.decode('utf-8').splitlines()
        if any(not line.strip() for line in lines):
            raise ValueError('blank native-oracle selection line')
        indexed = [json.loads(line) for line in lines]
        if len(indexed) != 113:
            raise ValueError('native-oracle selection row count mismatch')
        for row in indexed:
            if (not isinstance(row.get('id'), str) or not isinstance(row.get('roles'), list)
                    or not isinstance(row.get('source'), dict) or not isinstance(row.get('source', {}).get('path'), str)
                    or not isinstance(row.get('source', {}).get('sha256'), str)):
                raise ValueError('native-oracle selection row malformed')

        query_term = (term or '').upper()
        matches = []
        for line_number, row in enumerate(indexed, 1):
            case_match = (bool(query_term and row['id'].upper() == query_term)
                          and (kind is None or any(role.get('kind', '').upper() == kind
                                                   for role in row['roles'])))
            target_match = bool(target_term) and any(_matches(role, target_term, kind) for role in row['roles'])
            if term is None or case_match or target_match:
                matches.append((line_number, row))

        verified_sources = {}
        for _, row in matches:
            source = row['source']
            relative = source['path']
            member = members.get(relative)
            if not member or member.get('sha256') != source['sha256']:
                raise ValueError('native-oracle source is not bound by collection manifest')
            source_file = _native_oracle_path(root, collection_root, relative)
            if (source_file.stat().st_size != member.get('size')
                    or hashlib.sha256(source_file.read_bytes()).hexdigest() != source['sha256']):
                raise ValueError('native-oracle source hash mismatch')
            if relative not in verified_sources:
                verified_sources[relative] = json.loads(source_file.read_bytes())
            pointer = source.get('pointer')
            if not isinstance(pointer, str) or (pointer and not pointer.startswith('/')):
                raise ValueError('invalid native-oracle source pointer')
            value = verified_sources[relative]
            for part in pointer.split('/')[1:] if pointer else []:
                if re.search(r'~(?![01])', part):
                    raise ValueError('invalid native-oracle source pointer escape')
                part = part.replace('~1', '/').replace('~0', '~')
                if isinstance(value, list):
                    if not re.fullmatch(r'0|[1-9][0-9]*', part):
                        raise ValueError('invalid native-oracle array index')
                    value = value[int(part)]
                elif isinstance(value, dict):
                    value = value[part]
                else:
                    raise ValueError('native-oracle source pointer is not traversable')

        op268_rows = [row for _, row in matches if row.get('bundle') == 'operator-268-20261117']
        op268_detail = {}
        if op268_rows:
            inner_dir = collection_root / _NATIVE_ORACLE_OPERATOR268_RELATIVE_DIR
            inner_manifest = inner_dir / 'manifest.json'
            if (inner_dir.is_symlink() or inner_manifest.is_symlink() or not inner_manifest.is_file()
                    or not inner_manifest.resolve().is_relative_to(root.resolve())
                    or hashlib.sha256(inner_manifest.read_bytes()).hexdigest() != _NATIVE_ORACLE_OPERATOR268_MANIFEST_SHA256):
                raise ValueError('operator268 inner manifest unavailable or mismatched')
            inner = json.loads(inner_manifest.read_text(encoding='utf-8'))
            if inner.get('schema') != 'opcont268-files-v1' or len(inner.get('files', [])) != 7:
                raise ValueError('operator268 manifest scope mismatch')
            inner_paths = {}
            for item in inner['files']:
                relative = item.get('path')
                if not isinstance(relative, str) or relative in inner_paths:
                    raise ValueError('operator268 manifest path duplicate or malformed')
                file_path = _native_oracle_path(root, inner_dir, relative)
                if (file_path.stat().st_size != item.get('size')
                        or hashlib.sha256(file_path.read_bytes()).hexdigest() != item.get('sha256')):
                    raise ValueError('operator268 manifest member mismatch')
                inner_paths[relative] = item
            if set(inner_paths) != {
                    'LICENSES/Emuera1824-v24-license-original.txt',
                    'LICENSES/PyEmuera-3.0.0-LICENSE.txt',
                    'LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md',
                    'observations.json', 'README.ja.md', 'README.md', 'verify.py'}:
                raise ValueError('operator268 selected member set mismatch')
            observation_path = inner_dir / 'observations.json'
            if hashlib.sha256(observation_path.read_bytes()).hexdigest() != _NATIVE_ORACLE_OPERATOR268_OBSERVATIONS_SHA256:
                raise ValueError('operator268 observations pin mismatch')
            observations = json.loads(observation_path.read_text(encoding='utf-8'))
            cases = observations.get('cases', [])
            run_scope = observations.get('run_scope', {})
            if (observations.get('schema') != 'opcont268-selected-observations-v1'
                    or len(cases) != 33 or run_scope.get('native_runs') != 2
                    or run_scope.get('pyemuera_runs') != 1 or run_scope.get('shared_fixture') is not True
                    or run_scope.get('conditions_in_fixture') != 35
                    or run_scope.get('selected_cases') != 33):
                raise ValueError('operator268 observation scope mismatch')
            for row in op268_rows:
                source = row['source']
                pointer = source.get('pointer', '')
                if (source.get('path') != _NATIVE_ORACLE_OPERATOR268_RELATIVE_DIR + '/observations.json'
                        or source.get('sha256') != _NATIVE_ORACLE_OPERATOR268_OBSERVATIONS_SHA256
                        or not isinstance(pointer, str) or not pointer.startswith('/cases/')):
                    raise ValueError('operator268 observation pointer mismatch')
                try:
                    index = int(pointer.split('/')[2])
                except (ValueError, IndexError):
                    raise ValueError('operator268 observation pointer malformed')
                if pointer != f'/cases/{index}' or index < 0 or index >= len(cases):
                    raise ValueError('operator268 observation pointer out of range')
                case = cases[index]
                modes = case.get('modes', {})
                if (case.get('case_id') != row['id'] or case.get('typed_keys') != row['roles']
                        or row.get('reach_state') != 'recorded_projection_without_raw'
                        or 'operator268_projection_without_raw' not in row.get('limits', [])
                        or row.get('shared') is not True
                        or len(row.get('native', [])) != 2 or len(row.get('py', [])) != 1
                        or set(modes) != {'native-01', 'native-02', 'public-01'}):
                    raise ValueError('operator268 indexed row does not match selected observation')
                op268_detail[row['id']] = {
                    'observation_path': 'evidence/native-oracle-20261117/' + source['path'],
                    'observation_sha256': source['sha256'], 'observation_pointer': pointer,
                    'observation_form': 'SELECTED_PROJECTION', 'raw_included': False,
                    'fixture_included': False, 'config_included': False, 'shared_runs': True,
                    'inner_manifest_path': 'evidence/native-oracle-20261117/' + _NATIVE_ORACLE_OPERATOR268_RELATIVE_DIR + '/manifest.json',
                    'inner_manifest_sha256': _NATIVE_ORACLE_OPERATOR268_MANIFEST_SHA256,
                    'bundle_readme_en': 'evidence/native-oracle-20261117/' + _NATIVE_ORACLE_OPERATOR268_RELATIVE_DIR + '/README.md',
                    'bundle_readme_ja': 'evidence/native-oracle-20261117/' + _NATIVE_ORACLE_OPERATOR268_RELATIVE_DIR + '/README.ja.md',
                    'native_run_count': 2, 'pyemuera_run_count': 1,
                    'publisher_authentication': 'NOT_ESTABLISHED',
                }

        output = []
        for line_number, row in matches:
            source = row['source']
            item = {'case_id': row['id'], 'typed_targets': row['roles'], 'bundle': row['bundle'],
                    'stage': row.get('stage'),
                    'difference_attributed_to_case': row['difference_attributed_to_case'],
                    'selected_condition': row['condition'],
                    'selected_observations': row['observations'],
                    'selected_fields_scope': 'SELECTION_INDEX_VALUES_SOURCE_SEMANTIC_EQUIVALENCE_NOT_VERIFIED',
                    'selection_index_path': 'evidence/native-oracle-20261117/results/native-oracle-selection.jsonl',
                    'selection_index_line_1based': line_number,
                    'selection_index_sha256': _NATIVE_ORACLE_SELECTION_SHA256,
                    'reach_state': row.get('reach_state'), 'comparison': row.get('comparison'),
                    'shared': row.get('shared'), 'limits': row.get('limits', []),
                    'source': {'path': 'evidence/native-oracle-20261117/' + source['path'],
                               'sha256': source['sha256'], 'pointer': source.get('pointer')},
                    'native_oracle_readme_en': 'evidence/native-oracle-20261117/docs/native-oracle.md',
                    'native_oracle_readme_ja': 'evidence/native-oracle-20261117/docs/native-oracle.ja.md',
                    'publisher_authentication': 'NOT_ESTABLISHED'}
            if row['id'] in op268_detail:
                item['observation_scope'] = op268_detail[row['id']]
            output.append(item)
        return output, {'state': 'AVAILABLE', 'reason': None, 'indexed_rows': len(indexed),
                        'matched_rows': len(output), 'publisher_authentication': 'NOT_ESTABLISHED',
                        'scope': 'selected native-oracle index rows only; not a complete raw-observation inventory'}
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, UnicodeError, json.JSONDecodeError):
        return unavailable('INCONSISTENT', 'COLLECTION_INDEX_OR_MATCHED_SOURCE_INVALID')


_OPERATOR265_MANIFEST_SHA256 = '01a195a73539c189d9250e22fc03d972944238f20f729462c0525b47d2cea1e7'
_OPERATOR265_PROFILE_SHA256 = 'f505a02918b72be1cf56675b693388fd3006c23beba771a3ed802b866282dd47'
_OPERATOR265_VERIFIER_SHA256 = '7a60a0978ec8d5eda535ff989ca4a03d14390bf536d87d58345d816163b3df9e'
_OPERATOR265_PARENT_PINS = {
    'results/survey.json': '499652bad50c7e39576df8cbbc7d718d2aabd23d3c79298c8dfbdfd6dca4501f',
    'differences/catalog.json': '5a67e49af3008b671d37b27f5fbac746fb7677d9d1cdc982b9d278ced38b4754',
    'evidence/case-register-2898-20261117/cases.jsonl': '8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94',
    'evidence/case-register-2898-20261117/core.jsonl': 'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903',
    'evidence/case-register-2898-20261117/manifest.json': 'dabf8f4509100ebd19689fac92fe88d2aba7a5843a2542134c5d91741b88fddb',
}

_FIND_ELEMENT_MANIFEST_SHA256 = '12cb770fd4d60c2874c1854372c3856cc9227ede0f8fe2c007464ae1bacd1a5a'
_FIND_ELEMENT_SOURCE_PINS = {
    'results/survey.json': '499652bad50c7e39576df8cbbc7d718d2aabd23d3c79298c8dfbdfd6dca4501f',
    'differences/catalog.json': '5a67e49af3008b671d37b27f5fbac746fb7677d9d1cdc982b9d278ced38b4754',
    'evidence/case-register-2898-20261117/cases.jsonl': '8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94',
    'evidence/case-register-2898-20261117/core.jsonl': 'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903',
    'evidence/case-register-2898-20261117/manifest.json': 'dabf8f4509100ebd19689fac92fe88d2aba7a5843a2542134c5d91741b88fddb',
    'evidence/observation-adapter-183-20261117/data/cases.jsonl': '1bea5c6cf6cc593a0c150f195477a25da9d233a5d97170d4c5b0371d294e5581',
    'evidence/observation-adapter-183-20261117/data/modes.jsonl': '97ec7c600e4ddbc75ef07af15453770cefe8971f0efed76a099d2d1759ff0ed1',
    'evidence/observation-adapter-183-20261117/file-set-manifest.json': '673cce3f0c5c539b68711b592f42f9280a4f5b88a29e86974c224f004d40c79c',
}

def _validate_findelement_collection(root, folder, collection, entries):
    """Bind each condition to the fixed main, target and parent case snapshots."""
    expected = {
        'id': 'findelement64',
        'directory': 'evidence/find-element-string-64-20261117',
        'manifest_root': 'bundle',
        'record_file': 'conditions.json',
        'record_pointer': '/conditions',
        'registered_cases': 64,
        'condition_mode_references': 192,
        'unique_parent_mode_ids': 183,
        'source_pins': _FIND_ELEMENT_SOURCE_PINS,
    }
    for key, value in expected.items():
        if collection.get(key) != value:
            raise ValueError('FINDELEMENT collection profile mismatch: ' + key)
    if collection.get('manifest_sha256') != _FIND_ELEMENT_MANIFEST_SHA256:
        raise ValueError('FINDELEMENT manifest pin mismatch')
    for rel, pin in _FIND_ELEMENT_SOURCE_PINS.items():
        path = root / rel
        if (not path.is_file() or path.is_symlink() or
                hashlib.sha256(path.read_bytes()).hexdigest() != pin):
            raise ValueError('FINDELEMENT parent snapshot pin mismatch: ' + rel)

    def rows(rel):
        return [json.loads(line) for line in (root / rel).read_text(encoding='utf8').splitlines()]

    survey = json.loads((root / 'results/survey.json').read_text(encoding='utf8'))
    catalog = json.loads((root / 'differences/catalog.json').read_text(encoding='utf8'))
    conditions_path = folder / 'conditions.json'
    bindings_path = folder / 'case-bindings.json'
    conditions = json.loads(conditions_path.read_text(encoding='utf8'))
    bindings = json.loads(bindings_path.read_text(encoding='utf8'))
    if conditions.get('schema') != 'find-element-observations.v2' or len(conditions.get('conditions', [])) != 64:
        raise ValueError('FINDELEMENT condition profile mismatch')
    if bindings.get('schema') != 'find-element-case-bindings.v1' or len(bindings.get('cases', [])) != 64:
        raise ValueError('FINDELEMENT case binding profile mismatch')

    survey_rows = survey['main_scenarios']
    catalog_rows = catalog['main_scenarios']
    core_rows = rows('evidence/case-register-2898-20261117/core.jsonl')
    register_rows = rows('evidence/case-register-2898-20261117/cases.jsonl')
    parent_rows = rows('evidence/observation-adapter-183-20261117/data/cases.jsonl')
    parent_modes = rows('evidence/observation-adapter-183-20261117/data/modes.jsonl')
    core_by_id = {x['case_id']: (i, x) for i, x in enumerate(core_rows)}
    register_by_id = {x['case_id']: (i, x) for i, x in enumerate(register_rows)}
    parent_by_id = {x['case_id']: (i, x) for i, x in enumerate(parent_rows)}
    modes_by_id = {x['mode_id']: (i, x) for i, x in enumerate(parent_modes)}
    survey_by_id = {x['case_id']: (i, x) for i, x in enumerate(survey_rows)}
    catalog_by_id = {x['case_id']: (i, x) for i, x in enumerate(catalog_rows)}
    targets_by_key = {(x['kind'], x['name']): (i, x) for i, x in enumerate(survey['targets'])}
    if len(entries) != 64 or len(survey_by_id) != len(survey_rows) or len(parent_by_id) != len(parent_rows):
        raise ValueError('FINDELEMENT case profile cardinality')

    unique_modes = {}
    for i, (condition, binding, entry) in enumerate(zip(conditions['conditions'], bindings['cases'], entries)):
        cid = condition['registered_case_id']
        typed = {'kind': condition['target']['kind'], 'name': condition['target']['name']}
        expected_entry = {
            'condition_id': condition['id'],
            'case_id': cid,
            'target': typed,
            'source_marker': condition['source_marker'],
            'fixture_id': condition['fixture'],
            'form': condition['target']['form'],
            'record': 'evidence/find-element-string-64-20261117/conditions.json',
            'observation_pointer': '/conditions/' + str(i),
            'manifest': 'evidence/find-element-string-64-20261117/manifest.json',
            'collection_id': 'findelement64',
            'search_aliases': [condition['id']],
        }
        if any(entry.get(k) != v for k, v in expected_entry.items()):
            raise ValueError('FINDELEMENT index condition binding mismatch: ' + condition['id'])
        if (binding['id'] != condition['id'] or binding['registered_case_id'] != cid or
                binding['fixture'] != condition['fixture'] or binding['target'] != condition['target'] or
                binding['source_marker'] != condition['source_marker']):
            raise ValueError('FINDELEMENT bundle case binding mismatch: ' + condition['id'])

        si, sr = survey_by_id[cid]
        ci, cr = catalog_by_id[cid]
        ri, rr = core_by_id[cid]
        fi, fr = register_by_id[cid]
        pi, pr = parent_by_id[cid]
        ti, tr = targets_by_key[(typed['kind'], typed['name'])]
        sp = '/main_scenarios/' + str(si)
        cp = '/main_scenarios/' + str(ci)
        if (entry.get('case_verdict') != sr['scenario_verdict'] or
                entry.get('target_outcome') != tr['comparison_outcome'] or
                entry.get('acceptance_case_listed') is not True or entry.get('parent_case_listed') is not True or
                entry.get('main_case') != {'path':'results/survey.json','pointer':sp,'scenario_verdict':sr['scenario_verdict']} or
                entry.get('target_judgment') != {'path':'differences/catalog.json','pointer':cp,'verdict':cr['verdict']} or
                sr['scenario_verdict'] != cr['verdict'] or typed not in sr['targets'] or typed not in cr['targets']):
            raise ValueError('FINDELEMENT main/target judgment binding mismatch: ' + cid)
        if (entry.get('target_summary') != {'path':'results/survey.json','pointer':'/targets/'+str(ti),
                'status':tr['status'],'comparison_outcome':tr['comparison_outcome']} or cid not in tr['case_ids']):
            raise ValueError('FINDELEMENT typed target summary mismatch: ' + cid)
        if (rr['survey_pointer'] != sp or rr['scenario_verdict'] != sr['scenario_verdict'] or typed not in rr['targets'] or
                fr['survey_pointer'] != sp or fr['scenario_verdict'] != sr['scenario_verdict'] or
                entry['case_register']['core'] != {'path':'evidence/case-register-2898-20261117/core.jsonl',
                    'line':ri+1,'survey_pointer':rr['survey_pointer'],'scenario_verdict':rr['scenario_verdict'],
                    'targets':rr['targets'],'trace_aliases':rr['trace_aliases']} or
                entry['case_register']['full'] != {'path':'evidence/case-register-2898-20261117/cases.jsonl',
                    'line':fi+1,'projection_state':fr['projection_state'],'withheld_count':fr['withheld_count']}):
            raise ValueError('FINDELEMENT parent case register binding mismatch: ' + cid)
        if (typed not in pr['case_roles'] or pr['record']['case_id'] != cid or
                entry['parent_observation_case'].get('path') != 'evidence/observation-adapter-183-20261117/data/cases.jsonl' or
                entry['parent_observation_case'].get('line') != pi+1 or
                entry['parent_observation_case'].get('batch_id') != pr['batch_id'] or
                entry['parent_observation_case'].get('case_roles') != pr['case_roles']):
            raise ValueError('FINDELEMENT parent observation acceptance mismatch: ' + cid)
        mode_refs = entry['parent_observation_case'].get('modes')
        observations = condition['observations']
        if len(mode_refs) != 3 or len(observations) != 3:
            raise ValueError('FINDELEMENT mode cardinality mismatch: ' + cid)
        for j, (mode_ref, observation, mode_name) in enumerate(zip(mode_refs, observations, ('native-01','native-02','public-01'))):
            parent_ref = pr['modes'][mode_name]
            mode_id = parent_ref['mode_id']
            mi, mode_row = modes_by_id[mode_id]
            want = {'mode':mode_name,'mode_id':mode_id,
                    'condition_observation_pointer':f'/conditions/{i}/observations/{j}',
                    'parent_case_observation_pointer':parent_ref['observation_pointer'],
                    'parent_mode_record':{'path':'evidence/observation-adapter-183-20261117/data/modes.jsonl','line':mi+1},
                    'parent_fixture_id':mode_row['fixture_id'],'raw_path':observation['raw']['path'],
                    'raw_root':observation['raw']['root'],'raw_sha256':observation['raw']['sha256']}
            if (mode_ref != want or observation['mode'] != mode_name or mode_row['mode'] != mode_name or
                    mode_row['raw']['sha256'] != observation['raw']['sha256'] or
                    mode_row['fixture_id'] != pr['record']['fixtures_and_initial_state']['source_fixture']):
                raise ValueError('FINDELEMENT mode identity/role binding mismatch: ' + cid + '/' + mode_name)
            previous = unique_modes.setdefault(mode_id, (mode_name, mode_row['fixture_id'], mode_row['raw']['sha256']))
            if previous != (mode_name, mode_row['fixture_id'], mode_row['raw']['sha256']):
                raise ValueError('FINDELEMENT shared mode identity conflict: ' + mode_id)
    if len(unique_modes) != 183:
        raise ValueError('FINDELEMENT distinct parent mode count mismatch')


def _validate_operator265_collection(root, folder, collection, entries):
    """Validate one case row per registered case; typed roles do not multiply executions."""
    expected = {'id':'operator265','directory':'evidence/operator-265-20261117',
        'manifest_root':'bundle','record_file':'records.json','record_pointer':'/records',
        'registered_cases':23,'recorded_modes':69,
        'external_profile_file':'source-profile.json',
        'external_profile_sha256':_OPERATOR265_PROFILE_SHA256,
        'source_pins':_OPERATOR265_PARENT_PINS}
    if any(collection.get(k)!=v for k,v in expected.items()):
        raise ValueError('operator265 fixed collection profile mismatch')
    if collection.get('manifest_sha256') != _OPERATOR265_MANIFEST_SHA256:
        raise ValueError('operator265 manifest pin mismatch')
    for rel,pin in _OPERATOR265_PARENT_PINS.items():
        p=root/rel
        if not p.is_file() or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:
            raise ValueError('operator265 parent snapshot pin mismatch: '+rel)
    verifier_path=folder/'verify.py'
    if not verifier_path.is_file() or verifier_path.is_symlink() or hashlib.sha256(verifier_path.read_bytes()).hexdigest()!=_OPERATOR265_VERIFIER_SHA256:
        raise ValueError('operator265 verifier pin mismatch')
    helper=_normal_verified_tool()
    manifest_pin=_OPERATOR265_MANIFEST_SHA256
    profile_pin=_OPERATOR265_PROFILE_SHA256
    run=subprocess.run([sys.executable,'-B',str(verifier_path),'--inventory-tool',str(helper),
        '--pin',manifest_pin,'--profile-pin',profile_pin],capture_output=True,text=True)
    if run.returncode:
        raise ValueError('operator265 bundle verifier failed')
    data=json.loads((folder/'records.json').read_text(encoding='utf8'))
    if data.get('schema')!='operator265-observations.v2' or len(data.get('records',[]))!=23 or len(entries)!=23:
        raise ValueError('operator265 record cardinality/schema mismatch')
    survey=json.loads((root/'results/survey.json').read_text(encoding='utf8'))
    sm={x['case_id']:x for x in survey['main_scenarios']}
    core=_rows(root/'evidence/case-register-2898-20261117/core.jsonl')
    full=_rows(root/'evidence/case-register-2898-20261117/cases.jsonl')
    cm={x['case_id']:(i,x) for i,x in enumerate(core)}
    fm={x['case_id']:(i,x) for i,x in enumerate(full)}
    if len({x['registry_case_id'] for x in data['records']})!=23:
        raise ValueError('operator265 registered case IDs are not unique')
    for i,(r,e) in enumerate(zip(data['records'],entries)):
        cid=r['registry_case_id']
        if cid not in sm or cid not in cm or cid not in fm:
            raise ValueError('operator265 case missing from candidate register: '+cid)
        si=next(j for j,x in enumerate(survey['main_scenarios']) if x['case_id']==cid)
        ci,cr=cm[cid]; fi,fr=fm[cid]
        keys=r['associated_typed_keys']
        want_modes=[{'mode':m['mode'],'raw_files':[{'path':c['path'],'size':c['size'],'sha256':c['sha256']} for c in m['channels']],
                     'trace_recorded':bool(m.get('trace_sequence'))} for m in r['modes']]
        if keys!=sm[cid]['targets'] or keys!=cr['targets'] or keys!=fr['targets']:
            raise ValueError('operator265 typed role disagrees with registered case: '+cid)
        if (e.get('collection_id')!='operator265' or e.get('case_id')!=cid or e.get('registered_case_id')!=cid or
            e.get('case_alias')!=r['id'] or e.get('typed_keys')!=keys or e.get('source_marker')!=r['source_marker'] or
            e.get('case_verdict')!=sm[cid]['scenario_verdict'] or e.get('acceptance_case_listed') is not True or
            e.get('main_case')!={'path':'results/survey.json','pointer':cr['survey_pointer'],'scenario_verdict':cr['scenario_verdict']} or
            e.get('observation_pointer')!='/records/'+str(i) or e.get('record')!='evidence/operator-265-20261117/records.json' or
            e.get('actual_modes')!=want_modes or e.get('manifest_root')!='bundle' or
            e.get('execution_scope')!='ONE_REGISTERED_CASE_WITH_THREE_RECORDED_MODES; TYPED_KEYS_ARE_ASSOCIATED_ROLES_NOT_SEPARATE_EXECUTIONS' or
            e.get('parent_observation_adapter')!='NOT_REGISTERED_IN_183_CASE_ADAPTER'):
            raise ValueError('operator265 index-to-record mismatch: '+cid)
        if e.get('case_register',{}).get('core')!={'path':'evidence/case-register-2898-20261117/core.jsonl','line':ci+1,
              'survey_pointer':cr['survey_pointer'],'scenario_verdict':cr['scenario_verdict'],'targets':cr['targets']}:
            raise ValueError('operator265 core case pointer mismatch: '+cid)
        if e.get('case_register',{}).get('full')!={'path':'evidence/case-register-2898-20261117/cases.jsonl','line':fi+1,
              'projection_state':fr['projection_state'],'withheld_count':fr['withheld_count']}:
            raise ValueError('operator265 full case pointer mismatch: '+cid)


_EXTERNAL16_OUTER_SHA256 = '5548ed01d2729f0fced4565a4962d18c72e4531510f8c7f4558a1e216b7a7a40'
_EXTERNAL16_INNER_SHA256 = 'ae10d8c5c32b980973a00ae08fdc8f37daf7d4cd1a452434f01980a5615e1fa4'
_EXTERNAL16_VERIFIER_SHA256 = 'd35b15684923e1905048cfa69319f8a8c7c17d3d269fc51f78d5467b397ea43c'
_EXTERNAL16_HELPER_SHA256 = '387204bdfe5288a967176c46549ec5e9c00b1a26466a9e8bee01846a98237366'
_EXTERNAL16_PARENT_PINS = {
 'results/survey.json':'499652bad50c7e39576df8cbbc7d718d2aabd23d3c79298c8dfbdfd6dca4501f',
 'evidence/case-register-2898-20261117/core.jsonl':'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903',
 'evidence/case-register-2898-20261117/cases.jsonl':'8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94',
 'evidence/case-register-2898-20261117/manifest.json':'dabf8f4509100ebd19689fac92fe88d2aba7a5843a2542134c5d91741b88fddb',
 'evidence/observation-adapter-183-20261117/data/cases.jsonl':'1bea5c6cf6cc593a0c150f195477a25da9d233a5d97170d4c5b0371d294e5581',
}

def _validate_external16_collection(root, folder, collection, entries):
    expected={'id':'external16','directory':'evidence/external-additional-16-package-20261117',
      'manifest_file':'package-manifest.json','manifest_root':'package','manifest_sha256':_EXTERNAL16_OUTER_SHA256,
      'outer_manifest_sha256':_EXTERNAL16_OUTER_SHA256,
      'inner_directory':'evidence/external-additional-16-package-20261117/evidence/external-additional-observations-20261117',
      'inner_manifest_file':'manifest.json','inner_manifest_sha256':_EXTERNAL16_INNER_SHA256,'inner_manifest_root':'bundle',
      'verifier_sha256':_EXTERNAL16_VERIFIER_SHA256,'helper_sha256':_EXTERNAL16_HELPER_SHA256,
      'source_pins':_EXTERNAL16_PARENT_PINS,'registered_cases':16,'recorded_modes':34,'recorded_channels':54}
    if any(collection.get(k)!=v for k,v in expected.items()): raise ValueError('external16 fixed profile mismatch')
    for rel,pin in _EXTERNAL16_PARENT_PINS.items():
        p=root/rel
        if not p.is_file() or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:
            raise ValueError('external16 parent snapshot pin mismatch: '+rel)
    helper=folder/'tools/file_set_manifest.py';inner=folder/'evidence/external-additional-observations-20261117';verifier=inner/'verify.py'
    for p,pin,label in ((helper,_EXTERNAL16_HELPER_SHA256,'helper'),(verifier,_EXTERNAL16_VERIFIER_SHA256,'verifier')):
        if not p.is_file() or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:
            raise ValueError('external16 '+label+' pin mismatch')
    inner_manifest=inner/'manifest.json'
    if not inner_manifest.is_file() or inner_manifest.is_symlink() or hashlib.sha256(inner_manifest.read_bytes()).hexdigest()!=_EXTERNAL16_INNER_SHA256:
        raise ValueError('external16 inner manifest pin mismatch')
    proc=subprocess.run([sys.executable,'-B',str(helper),'verify','--manifest',str(folder/'package-manifest.json'),'--root','package='+str(folder)],capture_output=True,text=True)
    if proc.returncode: raise ValueError('external16 outer package inventory failed')
    proc=subprocess.run([sys.executable,'-B',str(verifier),'--inventory-tool',str(helper),'--pin',_EXTERNAL16_INNER_SHA256],capture_output=True,text=True)
    if proc.returncode: raise ValueError('external16 inner observation verifier failed')
    data=json.loads((inner/'records.json').read_text(encoding='utf8'))
    if data.get('schema')!='external-additional-observations.v1' or len(data.get('records',[]))!=16 or len(entries)!=16:
        raise ValueError('external16 fixed record profile mismatch')
    survey=json.loads((root/'results/survey.json').read_text(encoding='utf8'))
    sm={x['case_id']:x for x in survey['main_scenarios']}
    core=_rows(root/'evidence/case-register-2898-20261117/core.jsonl');full=_rows(root/'evidence/case-register-2898-20261117/cases.jsonl')
    cm={x['case_id']:(i,x) for i,x in enumerate(core)};fm={x['case_id']:(i,x) for i,x in enumerate(full)}
    parent_ids={x['case_id'] for x in _rows(root/'evidence/observation-adapter-183-20261117/data/cases.jsonl')}
    if len({x['case_id'] for x in data['records']})!=16: raise ValueError('external16 case IDs are not unique')
    mode_total=channel_total=0
    for i,(r,e) in enumerate(zip(data['records'],entries)):
        cid=r['case_id']
        if cid not in sm or cid not in cm or cid not in fm: raise ValueError('external16 case missing from candidate registration: '+cid)
        ci,cr=cm[cid];fi,fr=fm[cid];keys=r['targets']
        if keys!=sm[cid]['targets'] or keys!=cr['targets'] or keys!=fr['targets']:
            raise ValueError('external16 typed roles mismatch: '+cid)
        want_modes=[{'mode':m['mode'],'raw_files':[{'role':c['role'],'path':c['file']['path'],'size':c['file']['size'],'sha256':c['file']['sha256'],'observed_lines':c['observed_lines']} for c in m['channels']],'limitations':m['limitations']} for m in r['modes']]
        mode_total+=len(want_modes);channel_total+=sum(len(m['raw_files']) for m in want_modes)
        if (e.get('collection_id')!='external16' or e.get('case_id')!=cid or e.get('registered_case_id')!=cid or e.get('case_alias')!=r['id'] or
            e.get('typed_keys')!=keys or e.get('family')!=r['family'] or e.get('condition')!=r['condition'] or e.get('source_type')!=r['source_type'] or e.get('scope')!=r['scope'] or e.get('inputs')!=r['inputs'] or
            e.get('case_verdict')!=sm[cid]['scenario_verdict'] or e.get('acceptance_case_listed') is not True or
            e.get('main_case')!={'path':'results/survey.json','pointer':cr['survey_pointer'],'scenario_verdict':cr['scenario_verdict']} or
            e.get('observation_pointer')!='/records/'+str(i) or e.get('actual_modes')!=want_modes or
            e.get('record_root')!='bundle' or e.get('manifest_root')!='package' or e.get('inner_manifest_root')!='bundle' or
            e.get('execution_scope')!='ONE_REGISTERED_CASE_WITH_RECORDED_MODES; TYPED_KEYS_ARE_ASSOCIATED_ROLES_NOT_SEPARATE_EXECUTIONS' or
            e.get('raw_status')!='SAVED_RAW_INCLUDED; ORIGINAL_SOURCE_AND_SOME_RECEIPTS_NOT_INCLUDED_OR_UNAVAILABLE' or
            e.get('parent_observation_adapter')!=('REGISTERED' if cid in parent_ids else 'NOT_REGISTERED_IN_183_CASE_ADAPTER')):
            raise ValueError('external16 index-to-record mismatch: '+cid)
        if e.get('case_register',{}).get('core')!={'path':'evidence/case-register-2898-20261117/core.jsonl','line':ci+1,'survey_pointer':cr['survey_pointer'],'scenario_verdict':cr['scenario_verdict'],'targets':cr['targets']}:
            raise ValueError('external16 core pointer mismatch: '+cid)
        if e.get('case_register',{}).get('full')!={'path':'evidence/case-register-2898-20261117/cases.jsonl','line':fi+1,'projection_state':fr['projection_state'],'withheld_count':fr['withheld_count']}:
            raise ValueError('external16 full pointer mismatch: '+cid)
    if mode_total!=34 or channel_total!=54: raise ValueError('external16 mode/channel cardinality mismatch')


def _validate_external29_collection(root, folder, collection, entries):
    expected={'id':'external29','directory':'evidence/external-scalar-29-package-20261117','manifest_file':'package-manifest.json',
      'manifest_root':'bundle','registered_cases':29,'recorded_modes':58,
      'source_pins':{'results/survey.json':'499652bad50c7e39576df8cbbc7d718d2aabd23d3c79298c8dfbdfd6dca4501f','evidence/case-register-2898-20261117/core.jsonl':'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903','evidence/case-register-2898-20261117/cases.jsonl':'8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94'}}
    for k,v in expected.items():
        if collection.get(k)!=v: raise ValueError('external29 fixed profile mismatch: '+k)
    inner=folder/'evidence/external-scalar-observations-20261117'
    if hashlib.sha256((inner/'manifest.json').read_bytes()).hexdigest()!='dcc5a5ece93d7c4f1daaeaaa2549eae7820375011e064242ae0d6288007df9a0': raise ValueError('external29 inner manifest pin mismatch')
    helper=folder/'tools/file_set_manifest.py'; verifier=inner/'verify.py'
    if hashlib.sha256(helper.read_bytes()).hexdigest()!='387204bdfe5288a967176c46549ec5e9c00b1a26466a9e8bee01846a98237366' or hashlib.sha256(verifier.read_bytes()).hexdigest()!='1e0504debcc2e4b344ff5a45b7a8e012a6e7095a172c7374ff97af7fc8b2a8c0': raise ValueError('external29 verifier/helper pin mismatch')
    proc=subprocess.run([sys.executable,'-B',str(verifier),'--inventory-tool',str(helper),'--pin','dcc5a5ece93d7c4f1daaeaaa2549eae7820375011e064242ae0d6288007df9a0'],capture_output=True,text=True)
    if proc.returncode: raise ValueError('external29 inner package verifier failed')
    data=json.loads((inner/'records.json').read_text(encoding='utf-8'))
    rs=data.get('records',[])
    if data.get('schema')!='external-scalar-observations.v1' or len(rs)!=29 or len(entries)!=29: raise ValueError('external29 record count/schema')
    survey={x['case_id']:x for x in json.loads((root/'results/survey.json').read_text(encoding='utf-8'))['main_scenarios']}
    for i,(r,e) in enumerate(zip(rs,entries)):
        cid=r['case_id']
        if (e.get('collection_id')!='external29' or e.get('case_id')!=cid or e.get('registered_case_id')!=cid or e.get('case_alias')!=r['id'] or e.get('observation_pointer')!=f'/records/{i}' or e.get('typed_keys')!=r['typed_targets'] or e.get('comparison')!=r['comparison'] or e.get('main_case',{}).get('scenario_verdict')!=survey.get(cid,{}).get('scenario_verdict')): raise ValueError('external29 index/record/candidate binding: '+cid)


_TWAITZERO01_MANIFEST_SHA256 = '010701eecf0df8e396441b43368bb01ee6fa47752653d335fd5be35a4c436acc'
_TWAITZERO01_PARENT_PINS = {'results/survey.json': '499652bad50c7e39576df8cbbc7d718d2aabd23d3c79298c8dfbdfd6dca4501f',
 'differences/catalog.json': '5a67e49af3008b671d37b27f5fbac746fb7677d9d1cdc982b9d278ced38b4754',
 'evidence/case-register-2898-20261117/core.jsonl': 'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903',
 'evidence/case-register-2898-20261117/cases.jsonl': '8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94'}
_TWAITZERO01_COLLECTION = {'id': 'twaitzero01',
 'directory': 'evidence/twaitzero-observation-20261117',
 'manifest_sha256': '010701eecf0df8e396441b43368bb01ee6fa47752653d335fd5be35a4c436acc',
 'manifest_root': 'bundle',
 'registered_cases': 1,
 'source_pins': {'results/survey.json': '499652bad50c7e39576df8cbbc7d718d2aabd23d3c79298c8dfbdfd6dca4501f',
                 'differences/catalog.json': '5a67e49af3008b671d37b27f5fbac746fb7677d9d1cdc982b9d278ced38b4754',
                 'evidence/case-register-2898-20261117/core.jsonl': 'c504c99806036be2b092ecdf9c22a29cfd9f78d8f5de8b58a9ad44fb05970903',
                 'evidence/case-register-2898-20261117/cases.jsonl': '8d3a3dd1b3e87403df8e518461fbe12439bd1810195c29d4eb2747fd9e8efb94'},
 'readable_documents': []}
_TWAITZERO01_ENTRY = {'collection_id': 'twaitzero01',
 'case_id': 'TWAITZERO01',
 'target': {'kind': 'command_or_syntax', 'name': 'TWAIT'},
 'typed_keys': [{'kind': 'command_or_syntax', 'name': 'TWAIT'}],
 'historical_case_ids': [],
 'case_verdict': 'different_scoped',
 'target_outcome': 'documented_difference',
 'acceptance_case_listed': True,
 'readme_ja': 'evidence/twaitzero-observation-20261117/README.ja.md',
 'readme_en': 'evidence/twaitzero-observation-20261117/README.md',
 'record': 'evidence/twaitzero-observation-20261117/README.ja.md',
 'record_type': 'BILINGUAL_OBSERVATION_README',
 'observation_pointer': None,
 'manifest': 'evidence/twaitzero-observation-20261117/manifest.json',
 'condition': 'TWAIT 0,1; native input 42 and Enter posted; Py --debug --wait '
              'with empty input tape',
 'native_screen_crop': 'evidence/twaitzero-observation-20261117/raw/native-after-input-crop.png',
 'py_stdout': 'evidence/twaitzero-observation-20261117/raw/pyemuera-stdout.bin',
 'py_stderr': 'evidence/twaitzero-observation-20261117/raw/pyemuera-stderr.bin',
 'scope': 'ONE_CASE; NATIVE_CROP_AND_PY_OUTPUT; '
          'INPUT_CONSUMPTION_AND_NATIVE_NATURAL_EXIT_UNOBSERVED',
 'original_comparison_and_input_event_receipt': 'NOT_INCLUDED'}


def _validate_twaitzero01_collection(root, folder, collection, entries):
    # This is a fixed single case, not a shared-batch role inference.
    if collection != _TWAITZERO01_COLLECTION or entries != [_TWAITZERO01_ENTRY]:
        raise ValueError('TWAITZERO01 fixed binding mismatch')
    if collection['manifest_sha256'] != _TWAITZERO01_MANIFEST_SHA256:
        raise ValueError('TWAITZERO01 manifest pin mismatch')
    for rel, expected in _TWAITZERO01_PARENT_PINS.items():
        path = root / rel
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('TWAITZERO01 parent snapshot mismatch')
    survey = json.loads((root / 'results/survey.json').read_text(encoding='utf8'))
    catalog = json.loads((root / 'differences/catalog.json').read_text(encoding='utf8'))
    wanted = {'kind': 'command_or_syntax', 'name': 'TWAIT'}
    cases = [x for x in survey['main_scenarios'] if x['case_id'] == 'TWAITZERO01']
    targets = [x for x in survey['targets'] if x['kind'] == wanted['kind'] and x['name'] == wanted['name']]
    differences = [x for x in catalog['main_scenarios'] if x['case_id'] == 'TWAITZERO01']
    if len(cases) != 1 or cases[0]['targets'] != [wanted] or cases[0]['scenario_verdict'] != 'different_scoped':
        raise ValueError('TWAITZERO01 survey case mismatch')
    if len(targets) != 1 or targets[0]['comparison_outcome'] != 'documented_difference' or 'TWAITZERO01' not in targets[0]['case_ids']:
        raise ValueError('TWAIT target mismatch')
    if len(differences) != 1 or differences[0]['targets'] != [wanted] or differences[0]['verdict'] != 'different_scoped':
        raise ValueError('TWAITZERO01 catalog mismatch')
    for file in ('core.jsonl', 'cases.jsonl'):
        rows = [r for r in _rows(root / 'evidence/case-register-2898-20261117' / file) if r['case_id'] == 'TWAITZERO01']
        if len(rows) != 1 or rows[0]['targets'] != [wanted] or rows[0]['scenario_verdict'] != 'different_scoped':
            raise ValueError('TWAITZERO01 register mismatch')
    erb = (folder / 'fixture/ERB/TWAITZERO01.ERB').read_text(encoding='utf8')
    stdout = (folder / 'raw/pyemuera-stdout.bin').read_bytes()
    stderr = (folder / 'raw/pyemuera-stderr.bin').read_bytes()
    if 'TWAIT 0,1' not in erb or b'BEFORE_TWAIT_ZERO' not in stdout or b'AFTER_TWAIT_ZERO' in stdout or b'E_UNSUPPORTED' not in stderr:
        raise ValueError('TWAITZERO01 retained input or output mismatch')


def _supplemental_evidence(term, target_term, kind, root, allow_partial=False):
    """Find case roles from a separately pinned, multi-collection evidence index."""
    index = root / 'results/evidence-supplement-20261117.json'
    marker = root / 'results/evidence-supplement-20261117.marker'
    def present(p):
        return p.exists() or p.is_symlink()
    if not present(index) and not present(marker):
        return [], {'index': 'NOT_INSTALLED', 'collections': {}, 'readable_documents': {}}
    try:
        if (not index.is_file() or index.is_symlink() or not marker.is_file() or marker.is_symlink()
                or not index.resolve().is_relative_to(root.resolve())
                or not marker.resolve().is_relative_to(root.resolve())):
            raise ValueError('supplemental index incomplete')
        if marker.read_bytes() != b'supplemental-evidence-index-v1\n':
            raise ValueError('supplemental installation marker mismatch')
        raw = index.read_bytes()
        if hashlib.sha256(raw).hexdigest() != '41556bd8c20ad55bcd0f17784dc577ba2b5d1489c9bebc163e31d3b75d6ec243':
            raise ValueError('supplemental index pin mismatch')
        data = json.loads(raw)
        if data.get('schema') != 'supplemental-evidence-index-v1':
            raise ValueError('supplemental schema')
        collections, entries = data['collections'], data['entries']
        ids = [c['id'] for c in collections]
        if (ids != ['operator264', 'findelement64', 'operator265', 'external16', 'external29', 'twaitzero01'] or len(ids) != len(set(ids)) or
                len(entries) != 168 or
                sum(e.get('collection_id') == 'operator264' for e in entries) != 35 or
                sum(e.get('collection_id') == 'findelement64' for e in entries) != 64 or
                sum(e.get('collection_id') == 'operator265' for e in entries) != 23 or
                sum(e.get('collection_id') == 'external16' for e in entries) != 16 or
                sum(e.get('collection_id') == 'external29' for e in entries) != 29 or
                sum(e.get('collection_id') == 'twaitzero01' for e in entries) != 1 or
                any(e['collection_id'] not in ids for e in entries)):
            raise ValueError('supplemental collection binding')
        tool = _normal_verified_tool()
        spec = importlib.util.spec_from_file_location('supplement_file_set_manifest', tool)
        verifier = importlib.util.module_from_spec(spec)
        old = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = True
            spec.loader.exec_module(verifier)
        finally:
            sys.dont_write_bytecode = old
        verifier.check_path_components(index)
        verifier.check_path_components(marker)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        if not allow_partial:
            raise
        return [], {'index': 'INCONSISTENT', 'collections': {}, 'readable_documents': {}}
    results, states, document_states = [], {}, {}
    for collection in collections:
        ident = collection['id']
        try:
            name = collection['directory']
            path = PurePosixPath(name)
            if (not isinstance(name, str) or not name or path.is_absolute() or '..' in path.parts
                    or '\\' in name or ':' in name or path.as_posix() != name
                    or len(path.parts) != 2 or path.parts[0] != 'evidence'):
                raise ValueError('unsafe supplemental collection path')
            folder = root.joinpath(*path.parts)
            manifest_file = collection.get('manifest_file', 'manifest.json')
            manifest = folder / manifest_file
            if (not folder.is_dir() or folder.is_symlink() or not manifest.is_file() or manifest.is_symlink()
                    or not folder.resolve().is_relative_to(root.resolve())):
                raise ValueError('supplemental collection missing')
            if hashlib.sha256(manifest.read_bytes()).hexdigest() != collection['manifest_sha256']:
                raise ValueError('supplemental collection manifest pin mismatch')
            verifier.check_path_components(manifest)
            manifest_root = collection.get('manifest_root', 'evidence')
            if ident == 'findelement64' and manifest_root != 'bundle':
                raise ValueError('FINDELEMENT manifest root mismatch')
            if manifest_root not in ('evidence', 'bundle', 'package'):
                raise ValueError('unsupported supplemental manifest root')
            verifier.verify(manifest, {manifest_root: folder})
            collection_entries = [e for e in entries if e['collection_id'] == ident]
            if ident == 'findelement64':
                _validate_findelement_collection(root, folder, collection, collection_entries)
            elif ident == 'operator265':
                _validate_operator265_collection(root, folder, collection, collection_entries)
            elif ident == 'external16':
                _validate_external16_collection(root, folder, collection, collection_entries)
            elif ident == 'external29':
                _validate_external29_collection(root, folder, collection, collection_entries)
            elif ident == 'twaitzero01':
                _validate_twaitzero01_collection(root, folder, collection, collection_entries)
            for entry in collection_entries:
                if entry['manifest'] != name + '/' + collection.get('manifest_file', 'manifest.json') or any(
                        not entry[k].startswith(name + '/') for k in ('record', 'readme_ja', 'readme_en')):
                    raise ValueError('supplemental entry is outside collection')
                typed_roles = entry.get('typed_keys', [entry['target']])
                typed_hit = any(_matches(role, target_term, kind) for role in typed_roles)
                role_kind_ok = kind is None or any(role.get('kind','').upper() == kind for role in typed_roles)
                if (typed_hit or
                    (role_kind_ok and
                     term in {entry['case_id'].upper(), *(x.upper() for x in entry['historical_case_ids']),
                              *(x.upper() for x in entry.get('search_aliases', []))})):
                    results.append(entry)
            states[ident] = 'AVAILABLE'
        except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
            if not allow_partial:
                raise
            results = [e for e in results if e['collection_id'] != ident]
            states[ident] = 'INCONSISTENT'
        if states[ident] != 'AVAILABLE':
            document_states[ident] = 'NOT_CHECKED'
            continue
        docs = collection.get('readable_documents', [])
        if not docs:
            document_states[ident] = 'NOT_PROVIDED'
            continue
        try:
            files = []
            for doc in docs:
                name = doc['path']
                path = PurePosixPath(name)
                if (not isinstance(name, str) or not name or path.is_absolute() or '..' in path.parts
                        or '\\' in name or ':' in name or path.as_posix() != name
                        or len(path.parts) != 3 or path.parts[0] != 'docs'):
                    raise ValueError('unsafe readable document path')
                files.append(root.joinpath(*path.parts))
            if not any(p.exists() or p.is_symlink() for p in files):
                document_states[ident] = 'NOT_INSTALLED'
                continue
            contents = []
            for doc, path in zip(docs, files):
                if (not path.is_file() or path.is_symlink() or
                        not path.resolve().is_relative_to(root.resolve())):
                    raise ValueError('readable document missing')
                verifier.check_path_components(path)
                raw_doc = path.read_bytes()
                if hashlib.sha256(raw_doc).hexdigest() != doc['sha256']:
                    raise ValueError('readable document pin mismatch')
                contents.append(raw_doc.decode('utf-8-sig'))
            for entry in (e for e in results if e['collection_id'] == ident):
                case = entry['case_id']
                if not re.fullmatch(r'[A-Za-z0-9_-]+', case):
                    raise ValueError('unsafe case anchor')
                if not all(re.search(r'^## ' + re.escape(case) + r'\s*$', text, re.MULTILINE) for text in contents):
                    raise ValueError('readable case section missing')
                entry['readable_documents'] = [
                    {'language': doc['language'], 'path': doc['path'], 'anchor': case.lower(), 'sha256': doc['sha256']}
                    for doc in docs]
            document_states[ident] = 'AVAILABLE'
        except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, UnicodeError):
            if not allow_partial:
                raise
            for entry in (e for e in results if e['collection_id'] == ident):
                entry.pop('readable_documents', None)
            document_states[ident] = 'INCONSISTENT'
    return results, {'index': 'AVAILABLE', 'collections': states, 'readable_documents': document_states}


def _normal_verified_tool():
    tool = Path(__file__).with_name('file_set_manifest.py')
    if (not tool.is_file() or tool.is_symlink()
            or hashlib.sha256(tool.read_bytes()).hexdigest() != '387204bdfe5288a967176c46549ec5e9c00b1a26466a9e8bee01846a98237366'):
        raise ValueError('normal observations verification tool unavailable or inconsistent')
    return tool


def _normal_observations_196(term, root, kind):
    """Link ten conditions to verified observations in one shared batch."""
    folder = root / 'evidence/normal-observation-access-20261117'
    if not folder.exists() and not folder.is_symlink():
        return [], 'NOT_INSTALLED'
    source = root / 'evidence/multi-group-101-20261117'
    if (not folder.is_dir() or folder.is_symlink() or not source.is_dir() or source.is_symlink()
            or not folder.resolve().is_relative_to(root.resolve())
            or not source.resolve().is_relative_to(root.resolve())):
        raise ValueError('normal observations bundle or dependency is unsafe or missing')
    manifest, record, script = folder / 'manifest.json', folder / 'observations.json', folder / 'verify.py'
    source_manifest = source / 'manifest.json'
    if not all(p.is_file() for p in (manifest, record, script, source_manifest, folder / 'README.md')):
        raise ValueError('normal observations bundle or dependency is incomplete')
    tool = _normal_verified_tool()
    spec = importlib.util.spec_from_file_location('query_file_set_manifest', tool)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    verifier.check_path_components(manifest)
    verifier.check_path_components(source_manifest)
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != '80d4d6e17e52adc22a64728c21ced8cdfbd76db2ca0f4096ca4d45e37986ac00':
        raise ValueError('normal observations manifest snapshot mismatch')
    if hashlib.sha256(source_manifest.read_bytes()).hexdigest() != 'fa6e64a7f32295d2a1d82d8a815c5b697f55a080ed7980393eb2f5aac0189030':
        raise ValueError('normal observations dependency manifest snapshot mismatch')
    verifier.verify(manifest, {'evidence': folder})
    verifier.verify(source_manifest, {'evidence': source})
    # The sealed projection's verifier checks every case, source index and referenced raw byte span.
    spec = importlib.util.spec_from_file_location('query_normal_observations_196', script)
    module = importlib.util.module_from_spec(spec)
    no_bytecode = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = no_bytecode
    try:
        module.run(record, root / 'evidence')
    except StopIteration as exc:
        raise ValueError('normal observations case binding mismatch') from exc
    doc = json.loads(record.read_bytes())
    results = []
    for i, case in enumerate(doc['cases']):
        by_case = case['case_id'].upper() == term
        by_condition = case['condition']['id'].upper() == term
        roles = case['target']
        matched = ([r for r in roles if kind is None or r['kind'].upper() == kind]
                   if by_case or by_condition else [r for r in roles if _matches(r, term, kind)])
        if not matched:
            continue
        modes = []
        for j, obs in enumerate(case['observations']):
            # verify.py has checked that each path is exactly the pinned source asset path.
            history = root / 'evidence' / obs['history'].removeprefix('../')
            fixture = root / 'evidence' / obs['fixture'].removeprefix('../')
            config = root / 'evidence' / obs['config'].removeprefix('../')
            modes.append({'mode': obs['mode'], 'engine': obs['engine'],
                          'mode_source_record_kind': obs['mode_source_record_kind'],
                          'mode_source_record_sha256': obs['mode_source_record_sha256'],
                          'history': _reference(history, root), 'history_sha256': obs['history_sha256'],
                          'byte_span': obs['byte_span'], 'fixture': _reference(fixture, root),
                          'config': _reference(config, root),
                          'observation': _reference(record, root, pointer=f'/cases/{i}/observations/{j}')})
        results.append({'collection': 'normal_observations_196', 'case_id': case['case_id'],
                        'condition_id': case['condition']['id'],
                        'match_basis': 'CASE_ID' if by_case else ('CONDITION_ID' if by_condition else 'TYPED_ROLE'),
                        'matched_case_roles': matched, 'recorded_verdict': case['recorded_verdict'],
                        'sharing_scope': 'ONE_SHARED_BATCH_NOT_TEN_INDEPENDENT_EXECUTIONS',
                        'native_natural_exit': 'NOT_OBSERVED', 'internal_argument_value': 'UNOBSERVED',
                        'original_records': 'ACCEPTANCE_COMPARISON_AND_RECEIPTS_NOT_INCLUDED',
                        'scope': 'ORDINARY_CONDITIONS_NOT_FAULT_BEHAVIOR_OR_FULL_COMPATIBILITY',
                        'record': _reference(record, root, pointer=f'/cases/{i}'),
                        'manifest': _reference(manifest, root), 'bundle_readme': _reference(folder / 'README.md', root),
                        'source_index': _reference(source / 'index.json', root), 'modes': modes})
    return results, 'AVAILABLE'


def _graphics_38(term, root, kind):
    """Link the historical cases to their bounded Native observations."""
    folder = root / 'evidence/graphics-38-cases-20261117'
    if not folder.exists() and not folder.is_symlink():
        return [], 'NOT_INSTALLED'
    if not folder.is_dir() or folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
        raise ValueError('graphics 38 bundle path is unsafe')
    manifest, record = folder / 'manifest.json', folder / 'cases.json'
    if not manifest.is_file() or not record.is_file():
        raise ValueError('graphics 38 bundle is incomplete')
    if hashlib.sha256(manifest.read_bytes()).hexdigest() != '302ec4e002d496edbc140e3e462d58af1529329fb1d071734e9fcf6c541d387b':
        raise ValueError('graphics 38 manifest snapshot mismatch')
    spec = importlib.util.spec_from_file_location('query_file_set_manifest',
                                                  Path(__file__).with_name('file_set_manifest.py'))
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    verifier.verify(manifest, {'evidence': folder})
    doc = json.loads(record.read_bytes())
    cases = doc['cases']
    if (doc.get('schema') != 'graphics-38-historical-and-followup-v1'
            or type(doc.get('historical_case_verdicts_changed')) is not int
            or doc['historical_case_verdicts_changed'] != 0
            or type(doc.get('new_cross_engine_verdicts')) is not int
            or doc['new_cross_engine_verdicts'] != 0
            or not isinstance(cases, list) or len(cases) != 38
            or len({c['case_id'].upper() for c in cases}) != 38):
        raise ValueError('graphics 38 case set mismatch')

    def asset_ref(asset):
        name = asset['path']
        if (not isinstance(name, str) or not name or '\\' in name
                or any(part in ('', '.', '..') for part in name.split('/'))):
            raise ValueError('graphics 38 asset path mismatch')
        path = folder / name
        if not path.is_file() or not path.resolve().is_relative_to(folder.resolve()):
            raise ValueError('graphics 38 asset missing or unsafe')
        data = path.read_bytes()
        if (type(asset['size']) is not int or len(data) != asset['size']
                or hashlib.sha256(data).hexdigest() != asset['sha256']):
            raise ValueError('graphics 38 asset hash mismatch')
        return {'sha256': asset['sha256'], 'record': _reference(path, root)}

    results = []
    later_ids = {'GMUTATE231_gclear-expr-missing-invalid-color',
                 'GMUTATE231_gclear-method-missing-invalid-color'}
    for i, case in enumerate(cases):
        cid, targets, original = case['case_id'], case['typed_targets'], case['original']
        if (not isinstance(targets, list) or not targets
                or any(not isinstance(t, dict) or set(t) != {'kind', 'name'}
                       or not isinstance(t['kind'], str) or not isinstance(t['name'], str)
                       or not t['kind'] or not t['name'] for t in targets)
                or len({(t['kind'], t['name']) for t in targets}) != len(targets)
                or case['historical_verdict'] != 'unverified'
                or case['new_cross_engine_verdict'] != 'not_assessed'
                or original['native_natural_exit'] != 'not_observed'
                or not isinstance(original['native_raw'], list) or len(original['native_raw']) != 2
                or not isinstance(case['later_observations'], list)
                or len(case['later_observations']) != (1 if cid in later_ids else 0)):
            raise ValueError('graphics 38 case scope mismatch')
        by_case = cid.upper() == term
        matched = ([t for t in targets if kind is None or t['kind'].upper() == kind]
                   if by_case else [t for t in targets if _matches(t, term, kind)])
        if not matched:
            continue
        original_refs = {'fixture': asset_ref(original['fixture']),
                         'config': asset_ref(original['config']),
                         'assets': [asset_ref(x) for x in original['assets']],
                         'native_raw': [asset_ref(x) for x in original['native_raw']]}
        later = []
        for j, followup in enumerate(case['later_observations']):
            if (followup['identity'] != 'subsequent independent recorded run'
                    or followup['native_natural_exit'] != 'not_observed'
                    or followup['post_error_state'] != 'not_observed'
                    or followup['public_engine_comparison'] != 'not_assessed'):
                raise ValueError('graphics 38 followup scope mismatch')
            later.append({'relationship': 'SEPARATE_SUBSEQUENT_NATIVE_RUN',
                          'record': _reference(record, root, pointer=f'/cases/{i}/later_observations/{j}'),
                          'fixture': asset_ref(followup['fixture']), 'config': asset_ref(followup['config']),
                          'native_raw': asset_ref(followup['native_raw']), 'crop': asset_ref(followup['crop']),
                          'natural_exit': 'NOT_OBSERVED', 'post_error_state': 'NOT_OBSERVED',
                          'cross_engine_comparison': 'NOT_ASSESSED',
                          'historical_diagnostic': 'OLD_CLASSIFICATION_UNOBSERVED_BUT_ORIGINAL_RAW_HAS_DIAGNOSTIC_CAUSE_UNKNOWN',
                          'crop_scope': 'DOWNSCALED_CROP_NOT_ORIGINAL_RESOLUTION_PIXEL_PROOF',
                          'matching_bytes_scope': 'DO_NOT_ESTABLISH_SAME_ATTEMPT'})
        results.append({'collection': 'graphics_38_saved', 'case_id': cid,
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                        'matched_case_roles': matched, 'historical_verdict': 'unverified',
                        'verdict_scope': 'ORIGINAL_CASE_NOT_CHANGED_BY_NATIVE_OBSERVATIONS',
                        'observation_scope': 'SAVED_NATIVE_SELECTED_OBSERVATIONS_NOT_CROSS_ENGINE_VERDICT',
                        'target_reach': 'NOT_INFERRED_FROM_CASE_ROLE',
                        'native_natural_exit': 'NOT_OBSERVED',
                        'original_registry': 'FULL_ORIGINAL_NOT_INCLUDED_NEUTRAL_TEXT_PROJECTION',
                        'py_raw': 'NOT_INCLUDED_TARGET_MAY_BE_UNREACHED',
                        'pixels': 'SELECTED_IMAGE_POINTS_NOT_GUI_OR_ALL_PIXELS',
                        'record': _reference(record, root, pointer=f'/cases/{i}'),
                        'manifest': _reference(manifest, root),
                        'bundle_readme': _reference(folder / 'README.md', root),
                        'english_cases': _reference(folder / 'CASES_en.md', root),
                        'original': original_refs, 'later_observations': later})
    return results, 'AVAILABLE'


def _wait_observations(term, root, kind):
    """Link later observations without changing the historical C15 verdict."""
    bundles = (
        ('wait_release', 'wait-release-20261117', 'wait-release-observations-v1',
         '10754035ee0b76910ad86383556db55c5a7e293ff6c156c443771a6268f219bb'),
        ('wait_c15', 'wait-c15-20261117', 'wait-c15-observations-v1',
         'a2e004352b4259b69dbf7243e2884e64cea443007ed2ad1a4a8d3f7234228aae'),
    )
    cases = {'PRINTVKW': 'PRINTVKWC15', 'PRINTVDW': 'PRINTVDWC15'}
    results, states = [], {}
    verifier = None
    for label, dirname, schema, manifest_sha in bundles:
        folder = root / 'evidence' / dirname
        if not folder.exists() and not folder.is_symlink():
            states[label] = 'NOT_INSTALLED'
            continue
        if not folder.is_dir() or folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
            raise ValueError('wait observation bundle path is unsafe')
        manifest, record = folder / 'manifest.json', folder / 'observations.json'
        if not manifest.is_file() or not record.is_file():
            raise ValueError('wait observation bundle is incomplete')
        if hashlib.sha256(manifest.read_bytes()).hexdigest() != manifest_sha:
            raise ValueError('wait observation manifest snapshot mismatch')
        if verifier is None:
            spec = importlib.util.spec_from_file_location('query_file_set_manifest',
                                                          Path(__file__).with_name('file_set_manifest.py'))
            verifier = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(verifier)
        verifier.verify(manifest, {'evidence': folder})
        doc = json.loads(record.read_bytes())
        rows = doc['records']
        ids = [r['command'] if label == 'wait_release' else r['case_id'] for r in rows]
        expected = set(cases) if label == 'wait_release' else set(cases.values())
        if doc.get('schema') != schema or len(rows) != 2 or len(set(ids)) != 2 or set(ids) != expected:
            raise ValueError('wait observation record set mismatch')
        for i, row in enumerate(rows):
            command = row['command'] if label == 'wait_release' else row['case_id'][:-3]
            case_id = cases[command]
            by_case = term == case_id
            target = {'kind': 'command_or_syntax', 'name': command}
            if not ((by_case and (kind is None or kind == 'COMMAND_OR_SYNTAX'))
                    or _matches(target, term, kind)):
                continue
            results.append({
                'collection': label + '_subsequent_observation',
                'case_id': case_id, 'matched_case_roles': [target],
                'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'historical_verdict': 'unverified',
                'historical_verdict_scope': 'ORIGINAL_SURVEY_UNCHANGED',
                'relationship': ('RELATED_COMMAND_DIFFERENT_FIXTURE_NOT_C15_REPLAY'
                                 if label == 'wait_release' else
                                 'SUBSEQUENT_OBSERVATION_USING_C15_FIXTURE'),
                'native_natural_exit': 'NOT_OBSERVED_PROCESS_TERMINATED_AFTER_OBSERVATION',
                'input_scope': 'NATIVE_GUI_ENTER_AND_PY_STDIN_EMPTY_LINE_DIFFER',
                'unobserved': (['input_timing', 'cross_engine_pixel_equality', 'other_arguments']
                               if label == 'wait_release' else
                               ['post_fault_state', 'cross_engine_pixel_equality', 'other_inputs_and_arguments']),
                'record': _reference(record, root, pointer='/records/' + str(i)),
                'manifest': _reference(manifest, root),
                'bundle_readme': _reference(folder / 'README.md', root),
                'native_history': _reference(folder / (command if label == 'wait_release' else case_id)
                                             / 'native-history.bin', root),
            })
        states[label] = 'AVAILABLE'
    return results, states


def _method_display_state_15(term, root, kind):
    """Link case150 records without turning a shared batch into 15 runs."""
    folder = root / 'evidence/method-display-state-15-20261117'
    if not folder.exists():
        return [], 'NOT_INSTALLED'
    if not folder.is_dir() or folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
        raise ValueError('method display bundle path is unsafe')
    paths = {name: folder / name for name in ('index.json', 'manifest.json', 'README.md')}
    if not all(p.is_file() for p in paths.values()):
        raise ValueError('method display bundle is incomplete')
    index_bytes = paths['index.json'].read_bytes()
    if (hashlib.sha256(index_bytes).hexdigest() != 'fe0e3915e3d9a9660e9827eaf353dcdaa8c84e8760e58722da9a6836127cde84'
            or hashlib.sha256(paths['manifest.json'].read_bytes()).hexdigest() != '08108633f30191b65c11cfa9385d07966921f72df98f8f68c16e25e6ad6a7b00'):
        raise ValueError('method display snapshot mismatch')
    doc = json.loads(index_bytes)
    cases, conditions, modes = doc['cases'], doc['conditions'], doc['modes']
    if (doc.get('schema') != 'display-state-method150-shared-evidence-v1'
            or doc.get('batch_id') != 'DISPLAYSTATE01'
            or not isinstance(cases, list) or len(cases) != 15
            or len({c['case_id'] for c in cases}) != 15
            or len({(c['typed_target']['kind'], c['typed_target']['name']) for c in cases}) != 15
            or not isinstance(conditions, list) or len(conditions) != 20
            or len({c['marker'] for c in conditions}) != 20
            or [m['mode'] for m in modes] != ['native-01', 'native-02', 'py']):
        raise ValueError('method display case or mode set mismatch')
    by_marker = {c['marker']: i for i, c in enumerate(conditions)}
    refs = {}
    for i, mode in enumerate(modes):
        name = mode['mode']
        state = mode['receipt_projection']
        if ((name.startswith('native-') and
             (state['natural_exit'] != 'not_observed_after_5_seconds' or state['exit_code'] != 'not_observed'
              or state['cleanup'] != 'recorded_success'))
                or (name == 'py' and
                    (state['historical_pyz_pre_post'] != 'not_recorded_in_invocation'
                     or state['stdin'] != 'inherited; content_not_recorded'))):
            raise ValueError('method display process scope mismatch')
        refs[name] = {'mode_record': _reference(paths['index.json'], root, pointer='/modes/'+str(i))}
        for field, suffix in (('fixture', 'inputs/ERB/SEARCHBOUND01.ERB'),
                              ('config', 'inputs/emuera.config'), ('history', 'raw-history.bin')):
            asset = mode[field]
            relative = 'modes/'+name+'/'+suffix
            path = folder / relative
            if (asset.get('path') != relative or type(asset.get('size')) is not int
                    or not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(folder.resolve())):
                raise ValueError('method display asset path mismatch')
            raw = path.read_bytes()
            if len(raw) != asset['size'] or hashlib.sha256(raw).hexdigest() != asset['sha256']:
                raise ValueError('method display asset hash mismatch')
            refs[name][field] = {'sha256': asset['sha256'], 'record': _reference(path, root)}
    if any(len({refs[name][field]['sha256'] for name in refs}) != 1
           for field in ('fixture', 'config', 'history')):
        raise ValueError('method display shared bytes mismatch')
    unobserved = ['native_natural_exit', 'gui_rendering', 'font_drawing', 'input_layout',
                  'other_settings', 'public_execution_time_pyz_before_after']
    if doc['unobserved'] != unobserved:
        raise ValueError('method display unobserved scope mismatch')
    results = []
    for i, case in enumerate(cases):
        target, cid = case['typed_target'], case['case_id']
        markers = case['condition_markers']
        if (case['batch_id'] != 'DISPLAYSTATE01' or case['recorded_verdict'] != 'matched_scoped'
                or case['execution_credit'] != 'shared_batch_only_not_a_separate_run'
                or case['relationship'] not in ('getter_two_snapshots', 'setting_transition_observed_through_getter')
                or not isinstance(markers, list) or len(markers) != 2
                or len(set(markers)) != 2 or any(x not in by_marker for x in markers)):
            raise ValueError('method display case binding mismatch')
        by_case = cid.upper() == term
        matched = ((kind is None or target['kind'].upper() == kind) if by_case
                   else _matches(target, term, kind))
        if not matched:
            continue
        results.append({'collection': 'method_display_state_15_saved', 'case_id': cid,
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                        'matched_case_roles': [target], 'recorded_verdict': case['recorded_verdict'],
                        'verdict_scope': 'HISTORICAL_CASE_SCOPED_NOT_NEW_TARGET_ACCEPTANCE',
                        'batch_id': case['batch_id'], 'shared_batch_case_count': 15,
                        'sharing_scope': 'ONE_RECORDED_BATCH_NOT_15_INDEPENDENT_CASE_RUNS',
                        'target_reach': 'NOT_INFERRED_FROM_CASE_ROLE_OR_SHARED_BATCH',
                        'relationship': case['relationship'], 'condition_markers': markers,
                        'condition_records': [_reference(paths['index.json'], root,
                                                         pointer='/conditions/'+str(by_marker[m])) for m in markers],
                        'comparison_scope': 'RECORDED_OBSERVATIONS_NOT_INDEPENDENTLY_DERIVED_EXPECTATIONS',
                        'saved_modes': ['native-01', 'native-02', 'py'], 'mode_references': refs,
                        'public_stdin': 'INHERITED_CONTENT_NOT_RECORDED',
                        'native_input': 'ISOLATED_GUI_NO_SYNTHETIC_KEYS_RECORDED',
                        'input_pin_scope': 'RETAINED_BYTES_NOT_INDEPENDENT_PUBLIC_PRE_POST_PROOF',
                        'public_pyz_sha_scope': 'COMPARISON_DECLARED_EXECUTION_TIME_BEFORE_AFTER_NOT_ESTABLISHED',
                        'native_natural_exit_by_mode': {'native-01': 'NOT_OBSERVED_CLEANUP_RECORDED',
                                                        'native-02': 'NOT_OBSERVED_CLEANUP_RECORDED'},
                        'source_materials': 'ORIGINAL_REGISTER_COMPARISON_CONDITIONS_REVIEW_NOT_INCLUDED',
                        'reseal_limit': 'NEW_MANIFEST_OR_INDEX_PIN_DOES_NOT_PROVE_ORIGINAL_SOURCE_AGREEMENT',
                        'target_unobserved': unobserved,
                        'record': _reference(paths['index.json'], root, pointer='/cases/'+str(i)),
                        'manifest': _reference(paths['manifest.json'], root),
                        'bundle_readme': _reference(paths['README.md'], root)})
    return results, 'AVAILABLE'


def _operator_normal_6(term, root, kind):
    """Find v2 case bindings without implying replay or complete condition equality."""
    folder = root / 'evidence/operator-normal-6-20261117'
    if not folder.exists():
        return [], 'NOT_INSTALLED'
    if not folder.is_dir() or folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
        raise ValueError('operator normal bundle path is unsafe')
    paths = {n: folder / n for n in ('index.json', 'bindings.json', 'manifest.json', 'README.md')}
    if not all(p.is_file() for p in paths.values()):
        raise ValueError('operator normal bundle is incomplete')
    binding_bytes = paths['bindings.json'].read_bytes()
    if (hashlib.sha256(binding_bytes).hexdigest() != '3f6e241505473fa4095e6c240fe081da7882b178487d051d680a4039ce40bc5a'
            or hashlib.sha256(paths['manifest.json'].read_bytes()).hexdigest() != 'e28dafc22e15b276e522be31d8e8fd3fdac8b654430ee9fc260e0e22c319ebb3'):
        raise ValueError('operator normal snapshot mismatch')
    binding = json.loads(binding_bytes)
    doc = json.loads(paths['index.json'].read_bytes())
    cases = doc['cases']
    if (doc.get('schema') != 'operator-normal273-saved-evidence-v1'
            or binding.get('schema') != 'operator-normal273-case-bindings-v1'
            or binding.get('source_register_sha256') != '32f008d1e6ebf6a373a080484b8a493d173bcff6b911249d8b6bf6e894295195'
            or not isinstance(cases, list) or len(cases) != 6
            or not isinstance(binding.get('cases'), list) or len(binding['cases']) != 6
            or len({c['case_id'] for c in cases}) != 6):
        raise ValueError('operator normal case set mismatch')
    bound = {c['case_id']: c for c in binding['cases']}
    if len(bound) != 6 or set(bound) != {c['case_id'] for c in cases}:
        raise ValueError('operator normal bindings mismatch')
    binding_index = {c['case_id']: i for i, c in enumerate(binding['cases'])}
    roles_seen = set()
    results = []
    expected_unobserved = ['full_stdin_content', 'other_external_inputs', 'native_natural_exit',
                           'postfatal_state', 'full_diagnostic_equivalence', 'all_target_acceptance',
                           'pixel_or_visual_equivalence']

    def checked_asset(asset, relative, expected_sha):
        path = folder / relative
        if (asset.get('path') != relative or asset.get('sha256') != expected_sha
                or type(asset.get('bytes')) is not int or not path.is_file() or path.is_symlink()
                or not path.resolve().is_relative_to(folder.resolve())):
            raise ValueError('operator normal asset reference mismatch')
        raw = path.read_bytes()
        if len(raw) != asset['bytes'] or hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ValueError('operator normal asset hash mismatch')
        return {'sha256': expected_sha, 'record': _reference(path, root)}

    for i, case in enumerate(cases):
        cid = case['case_id']
        native = case['native']
        if (not isinstance(native, list) or len(native) != 2
                or [n['mode'] for n in native] != ['native-01', 'native-02']):
            raise ValueError('operator normal mode mismatch')
        current = {'case_id': cid, 'typed_targets': case['typed_targets'],
                   'case_register_pointer': case['case_register_pointer'],
                   'fixture_sha256': case['inputs']['fixture']['sha256'],
                   'config_sha256': case['inputs']['config']['sha256'],
                   'selected_normal_markers': case['selected_normal_markers'],
                   'public_stdout_sha256': case['public']['stdout']['sha256'],
                   'public_stderr_sha256': case['public']['stderr']['sha256'],
                   'public_pyz_sha256_before': case['public']['public_pyz_sha256_before'],
                   'public_pyz_sha256_after': case['public']['public_pyz_sha256_after'],
                   'native': [{'mode': n['mode'], 'raw_sha256': n['raw']['sha256'],
                               'exe_sha256_recorded_and_retained': n['exe_sha256_recorded_and_retained']}
                              for n in native]}
        limits = case['recorded_conditions']
        if (current != bound[cid] or case['public']['mode'] != 'public-refresh'
                or case['public']['stdin'] != 'inherited; content_not_recorded'
                or case['public']['stderr_scope'] != 'nonfatal_OUTPUTLOG_bounded_text_history_notice_not_diagnostic_parity'
                or limits['full_environment_and_input_equivalence'] != 'not_established'
                or limits['public_vs_historical_public_build_identity'] != 'not_established'
                or limits['unobserved'] != expected_unobserved
                or case['comparison_scope'] != 'selected_normal_markers_only_not_all_lines_or_behavior'
                or any(n['input_channel'] != 'gui_separate_desktop; synthetic_keyboard_events_sent_false'
                       or n['natural_exit'] != 'not_observed_after_5_seconds; cleanup_recorded'
                       or n['execution_time_limit'] != 'not_present_in_retained_probe_receipt'
                       or n['recorded_execution_time_utc'] is not None for n in native)):
            raise ValueError('operator normal binding or scope mismatch')
        for role in case['typed_targets']:
            key = (role['kind'], role['name'])
            if role['kind'] != 'operator' or key in roles_seen:
                raise ValueError('operator normal duplicate or invalid role')
            roles_seen.add(key)
        base = 'assets/' + cid
        inputs = {
            'fixture': checked_asset(case['inputs']['fixture'], base+'/inputs/ERB/SEARCHBOUND01.ERB', bound[cid]['fixture_sha256']),
            'config': checked_asset(case['inputs']['config'], base+'/inputs/emuera.config', bound[cid]['config_sha256']),
        }
        outputs = {'public-refresh': {
            'stdout': checked_asset(case['public']['stdout'], base+'/public/stdout.bin', bound[cid]['public_stdout_sha256']),
            'stderr': checked_asset(case['public']['stderr'], base+'/public/stderr.bin', bound[cid]['public_stderr_sha256'])}}
        for n, b in zip(native, bound[cid]['native']):
            outputs[n['mode']] = {'raw': checked_asset(n['raw'], base+'/'+n['mode']+'/emuera.log', b['raw_sha256'])}
        by_case = cid.upper() == term
        matched = ([r for r in case['typed_targets'] if kind is None or r['kind'].upper() == kind]
                   if by_case else [r for r in case['typed_targets'] if _matches(r, term, kind)])
        if not matched and not (by_case and kind is None):
            continue
        results.append({'collection': 'operator_normal_6_saved', 'case_id': cid,
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                        'matched_case_roles': matched,
                        'recorded_verdict': None,
                        'verdict_scope': 'NOT_PRESENT_IN_THIS_INDEX_NOT_A_NEW_ACCEPTANCE',
                        'saved_modes': ['public-refresh', 'native-01', 'native-02'],
                        'public_stdin': 'INHERITED_CONTENT_NOT_RECORDED',
                        'native_input': 'SEPARATE_GUI_DESKTOP_NO_SYNTHETIC_KEYS_RECORDED',
                        'native_natural_exit_by_mode': {'native-01': 'NOT_OBSERVED_CLEANUP_RECORDED',
                                                        'native-02': 'NOT_OBSERVED_CLEANUP_RECORDED'},
                        'complete_condition_equivalence': 'NOT_ESTABLISHED',
                        'historical_public_build_identity': 'NOT_ESTABLISHED',
                        'public_stderr_scope': 'NONFATAL_OUTPUTLOG_NOTICE_NOT_DIAGNOSTIC_PARITY',
                        'target_reach': 'NOT_INFERRED_FROM_CASE_ROLE',
                        'unobserved': expected_unobserved,
                        'selected_marker_scope': 'RECORDED_NORMAL_SUBSET_QUERY_DOES_NOT_REVERIFY_MARKERS',
                        'selected_marker_count': len(case['selected_normal_markers']),
                        'source_register': {'sha256': binding['source_register_sha256'],
                                            'pointer': bound[cid]['case_register_pointer'],
                                            'availability': 'ORIGINAL_REGISTER_NOT_INCLUDED'},
                        'inputs': inputs, 'outputs_by_mode': outputs,
                        'record': _reference(paths['index.json'], root, pointer='/cases/'+str(i)),
                        'binding_record': _reference(paths['bindings.json'], root,
                                                     pointer='/cases/'+str(binding_index[cid])),
                        'manifest': _reference(paths['manifest.json'], root),
                        'bundle_readme': _reference(paths['README.md'], root)})
    if len(roles_seen) != 19:
        raise ValueError('operator normal target count mismatch')
    return results, 'AVAILABLE'


def _display_state_21(term, root, kind):
    """Link the selected records and explicitly distinguish the excluded STRLEN."""
    folder = root / 'evidence/display-state-21-20261117'
    if not folder.exists():
        return [], 'NOT_INSTALLED'
    required = {name: folder / name for name in
                ('cases.jsonl', 'bindings.json', 'conditions.json', 'comparison.json', 'modes.json', 'README.md')}
    if not all(path.is_file() for path in required.values()):
        raise ValueError('display-state bundle is incomplete')
    binding_bytes = required['bindings.json'].read_bytes()
    if hashlib.sha256(binding_bytes).hexdigest() != 'a5ecfdb285fde3beac35d3e58647b63e989823865b74cbb250c43ad59bfbbd7e':
        raise ValueError('display-state bindings snapshot mismatch')
    binding = json.loads(binding_bytes)
    cases = _rows(required['cases.jsonl'])
    conditions = json.loads(required['conditions.json'].read_text(encoding='utf-8'))
    comparison = json.loads(required['comparison.json'].read_text(encoding='utf-8'))
    modes = json.loads(required['modes.json'].read_text(encoding='utf-8'))
    excluded = {'case_id': 'DISPLAYCOMMAND179_STRLEN',
                'target': {'kind': 'command_or_syntax', 'name': 'STRLEN'},
                'condition_markers': ['STATE130', 'STATE131']}
    if (binding.get('schema') != 'display-state-case-bindings.v1' or binding.get('excluded_case') != excluded
            or not isinstance(binding.get('cases'), list) or len(binding['cases']) != 21 or len(cases) != 21
            or len({c['case_id'] for c in cases}) != 21
            or len({(c['target']['kind'], c['target']['name']) for c in cases}) != 21
            or len(conditions) != 138 or [c['marker'] for c in conditions] != ['STATE' + str(i) for i in range(138)]
            or comparison['conditions'] != conditions or comparison['observation_count'] != 138
            or comparison['verdict'] != 'matched_scoped'
            or modes['schema'] != 'display-state-shared-modes-prototype.v1'
            or modes['reported_comparison_verdict'] != 'matched_scoped' or modes['raw_byte_equality'] is not True
            or modes['selected_cases'] != 21 or modes['conditions'] != 138 or modes['shared_batch'] is not True
            or modes['source_case_and_markers_do_not_prove_target_reach'] is not True
            or modes['native_natural_exit_observed'] is not False
            or modes['not_selected_but_in_shared_fixture'] != 'command_or_syntax:STRLEN'):
        raise ValueError('display-state bundle scope mismatch')
    if ([conditions[i].get('command') for i in (130, 131)] != ['STRLEN', 'STRLEN']
            or [conditions[i].get('empty') for i in (130, 131)] != [False, True]):
        raise ValueError('display-state excluded condition mismatch')
    bound = {b['case_id']: b for b in binding['cases']}
    if (len(bound) != 21 or set(bound) != {c['case_id'] for c in cases}
            or excluded['case_id'] in bound or any(c['target'] == excluded['target'] for c in cases)):
        raise ValueError('display-state case set mismatch')
    binding_index = {b['case_id']: i for i, b in enumerate(binding['cases'])}
    for c in cases:
        if ({k: c[k] for k in ('case_id', 'target', 'association_basis', 'condition_markers', 'recorded_verdict')}
                != bound[c['case_id']] or c['recorded_verdict'] != 'matched_scoped'
                or c['shared_modes'] != ['native-01', 'native-02', 'public-01']
                or c['target_reach'] != 'NOT_INFERRED_FROM_ROLE_MARKER_OR_SHARED_BATCH'
                or c['independent_run_per_case'] is not False or _has_private_path(c)):
            raise ValueError('display-state case binding mismatch')
        name, role, basis = c['target']['name'], c['target']['kind'], c['association_basis']
        if basis == 'condition_function_name' and role == 'expression_function':
            markers = [x['marker'] for x in conditions if x.get('function') == name]
        elif basis == 'condition_command_name' and role == 'command_or_syntax':
            markers = [x['marker'] for x in conditions if x.get('command') == name]
        elif basis == 'condition_preceding_command' and role == 'command_or_syntax':
            markers = [x['marker'] for x in conditions if (x.get('preceding_command') or '').split(' ', 1)[0] == name]
        else:
            raise ValueError('display-state association basis mismatch')
        if not markers or c['condition_markers'] != markers:
            raise ValueError('display-state condition markers mismatch')
    mode_rows = modes['mode_records']
    if [m['mode'] for m in mode_rows] != ['native-01', 'native-02', 'public-01']:
        raise ValueError('display-state mode set mismatch')
    mode_refs = {}
    for mode in mode_rows:
        name = mode['mode']
        state = mode['recorded_process']
        if (mode['case_run_scope'] != 'SHARED_BATCH_NOT_21_INDEPENDENT_RUNS'
                or mode['done_marker_in_raw'] is not True
                or (name.startswith('native-') and
                    (state['natural_exit_observed'] is not False or state['alive_after_5s'] is not True
                     or state['cleanup_terminate_ok'] is not True or state['exit_code'] is not None))):
            raise ValueError('display-state mode observation mismatch')
        refs = {}
        for field, filename in (('fixture', 'fixture.erb'), ('config', 'emuera.config'), ('raw', 'raw.log')):
            rel = 'modes/' + name + '/' + filename
            path = folder / rel
            if (mode[field] != rel or not path.is_file() or not path.resolve().is_relative_to(folder.resolve())
                    or hashlib.sha256(path.read_bytes()).hexdigest() != mode[field + '_sha256']):
                raise ValueError('display-state mode file mismatch')
            refs[field] = {'sha256': mode[field + '_sha256'], 'record': _reference(path, root)}
        mode_refs[name] = refs
    if any(len({mode_refs[name][field]['sha256'] for name in mode_refs}) != 1
           for field in ('fixture', 'config', 'raw')):
        raise ValueError('display-state shared mode bytes mismatch')
    shared = {'collection': 'display_state_21_saved', 'shared_batch_case_count': 21,
              'saved_modes': ['native-01', 'native-02', 'public-01'],
              'sharing_scope': 'ONE_RECORDED_BATCH_NOT_21_INDEPENDENT_RUNS',
              'target_reach': 'NOT_INFERRED_FROM_ROLE_MARKER_OR_SHARED_BATCH',
              'expected_values': '138_VALUES_NOT_INDEPENDENTLY_CHECKED',
              'gui_rendering': 'NOT_OBSERVED',
              'native_natural_exit_by_mode': {'native-01': 'NOT_OBSERVED_CLEANUP_RECORDED',
                                              'native-02': 'NOT_OBSERVED_CLEANUP_RECORDED'},
              'mode_references': mode_refs, 'conditions_record': _reference(required['conditions.json'], root),
              'comparison_record': _reference(required['comparison.json'], root),
              'mode_record': _reference(required['modes.json'], root),
              'bundle_readme': _reference(required['README.md'], root)}
    matches = []
    for i, c in enumerate(cases):
        by_case = c['case_id'].upper() == term
        matched = ((kind is None or c['target']['kind'].upper() == kind) if by_case
                   else _matches(c['target'], term, kind))
        if not matched:
            continue
        matches.append({**shared, 'case_id': c['case_id'], 'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                        'matched_parent_roles': [c['target']], 'recorded_verdict': c['recorded_verdict'],
                        'verdict_scope': 'HISTORICAL_CASE_NOT_INDEPENDENT_EXPECTED_VALUE_VALIDATION',
                        'condition_markers': c['condition_markers'], 'association_basis': c['association_basis'],
                        'record': _reference(required['cases.jsonl'], root, line=i + 1),
                        'binding_record': _reference(required['bindings.json'], root,
                                                     pointer='/cases/' + str(binding_index[c['case_id']]))})
    by_case = excluded['case_id'].upper() == term
    matched = ((kind is None or excluded['target']['kind'].upper() == kind) if by_case
               else _matches(excluded['target'], term, kind))
    if matched:
        matches.append({**shared, 'collection': 'display_state_21_scope', 'case_id': excluded['case_id'],
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE', 'matched_parent_roles': [],
                        'scope_target': excluded['target'], 'condition_markers': excluded['condition_markers'],
                        'selection_status': 'OUTSIDE_21_NOT_A_CLAIM_OF_NONOBSERVATION', 'recorded_verdict': None,
                        'record': _reference(required['bindings.json'], root, pointer='/excluded_case')})
    return matches, 'AVAILABLE'


def _console_background_24(term, root, kind):
    """Find saved CBG cases without treating setup failures or receipts as replay."""
    folder = root / 'evidence/console-background-24-20261117'
    if not folder.exists():
        return [], 'NOT_INSTALLED'
    if not folder.is_dir() or folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
        raise ValueError('console background bundle path is unsafe')
    path = folder / 'records.json'
    if not all((folder / name).is_file() for name in ('records.json', 'README.md', 'manifest.json')):
        raise ValueError('console background bundle is incomplete')
    doc = json.loads(path.read_text(encoding='utf-8'))
    cases = doc['cases']
    if (not isinstance(cases, list) or len(cases) != 24
            or len({c['case_id'] for c in cases}) != 24
            or sum(c['recorded_verdict'] == 'unverified' for c in cases) != 2
            or sum(len(c['modes']) for c in cases) != 72):
        raise ValueError('console background case or mode set mismatch')
    results = []
    for i, case in enumerate(cases):
        by_case = case['case_id'].upper() == term
        matched = ([r for r in case['roles'] if kind is None or r['kind'].upper() == kind]
                   if by_case else [r for r in case['roles'] if _matches(r, term, kind)])
        if not matched and not (by_case and kind is None):
            continue
        modes = case['modes']
        if [m['mode'] for m in modes] != ['native-01', 'native-02', 'public-01']:
            raise ValueError('console background mode binding mismatch')
        if ((case['case_kind'] == 'setup') != (case['recorded_verdict'] == 'unverified')
                or (case['case_kind'] == 'setup'
                    and case['public_target_reach'] != 'not_established_setup_or_load_stopped')):
            raise ValueError('console background setup scope mismatch')
        mode_refs = {}
        for mode in modes:
            name = mode['mode']
            native = name.startswith('native-')
            if (mode['source_receipt_included'] is not False
                    or mode['source_receipt_sha256_scope'] != 'original_receipt_not_included'
                    or mode['native_natural_exit'] != ('not_observed_cleanup_separate' if native else 'not_applicable')
                    or mode['input_identity_basis'] != ('native_probe_declared_fixture_and_config' if native else 'public_receipt_before_after')):
                raise ValueError('console background receipt or exit scope mismatch')
            expected = {'fixture', 'config', 'raw', 'derived_receipt'} | (set() if native else {'stderr'})
            if set(mode['evidence']) != expected:
                raise ValueError('console background evidence set mismatch')
            prefix = 'assets/C%03d/%s/' % (i + 1, name)
            paths = {'fixture': prefix + 'inputs/ERB/SEARCHBOUND01.ERB',
                     'config': prefix + 'inputs/emuera.config',
                     'raw': prefix + ('native-history.bin' if native else 'public-stdout.bin'),
                     'derived_receipt': prefix + 'receipt.json'}
            if not native:
                paths['stderr'] = prefix + 'public-stderr.bin'
            refs = {}
            for label, rel in paths.items():
                asset = mode['evidence'][label]
                target = folder / rel
                if (asset.get('status') != 'included' or asset.get('path') != rel
                        or not target.is_file() or target.is_symlink()
                        or not target.resolve().is_relative_to(folder.resolve())):
                    raise ValueError('console background evidence missing or unsafe')
                if label in ('fixture', 'config', 'raw', 'stderr') and asset.get('sha256') != mode[label + '_sha256']:
                    raise ValueError('console background evidence SHA reference mismatch')
                refs[label] = {'sha256': asset['sha256'], 'record': _reference(target, root)}
            refs['input_identity_basis'] = mode['input_identity_basis']
            refs['source_receipt'] = 'NOT_INCLUDED_SELECTED_FIELDS_IN_DERIVED_RECEIPT'
            refs['case_mode_identity'] = 'DERIVED_FROM_CASE_PLAN_COMPARISON_AND_SOURCE_PATH'
            mode_refs[name] = refs
        results.append({'collection': 'console_background_24_saved', 'case_id': case['case_id'],
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                        'matched_parent_roles': matched, 'recorded_parent_roles': case['roles'],
                        'recorded_verdict': case['recorded_verdict'],
                        'verdict_scope': 'SAVED_CASE_NOT_TARGET_ACCEPTANCE',
                        'case_kind': case['case_kind'], 'fixture_id': case['fixture_id'],
                        'saved_modes': [m['mode'] for m in modes],
                        'collection_case_mode_references': 72,
                        'sharing_scope': 'CASE_MODE_BINDINGS_NOT_PROOF_OF_INDEPENDENT_RUNS_OR_FULL_CONDITION_EQUALITY',
                        'native_selected_rows_by_mode': {'native-01': case['native_01_selected_rows'],
                                                         'native-02': case['native_02_selected_rows']},
                        'public_error_recorded': case['public_error_recorded'],
                        'public_target_reach': case['public_target_reach'],
                        'native_natural_exit': 'NOT_OBSERVED_CLEANUP_SEPARATE',
                        'target_reach': 'NOT_INFERRED_FROM_CASE_ROLE_OR_RECEIPT',
                        'unobserved': case['unobserved'],
                        'actual_button_selection': 'NOT_OBSERVED_SEE_BUNDLE_README',
                        'mode_references': mode_refs,
                        'record': _reference(path, root, pointer='/cases/' + str(i)),
                        'bundle_readme': _reference(folder / 'README.md', root)})
    return results, 'AVAILABLE'



def saved_observations(term, root, printdata_override=None, observation_override=None, kind=None, allow_partial=False):
    """Find saved cases without exporting private original records or source paths."""
    normal_folder = root / 'evidence/normal-observation-access-20261117'
    if normal_folder.exists() or normal_folder.is_symlink():
        # This helper is shared by other collections, so check it before any of them imports it.
        _normal_verified_tool()
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    printpath = Path(printdata_override) if printdata_override else root / 'evidence/printdata-61-20261117/index.json'
    obsroot = Path(observation_override) if observation_override else root / 'evidence/observation-adapter-183-20261117/data'
    results, console_background_state = _console_background_24(term, root, kind)
    availability = {'console_background_24': console_background_state}
    if printpath.is_file():
        doc = json.loads(printpath.read_text(encoding='utf-8'))
        if doc.get('schema') != 'saved-case-evidence-index-1':
            raise ValueError('unsupported PRINTDATA saved index schema')
        batches = {b['batch_id']: b for b in doc['batches']}
        if len(batches) != len(doc['batches']):
            raise ValueError('duplicate saved batch ID')
        if len({c['case_id'] for c in doc['cases']}) != len(doc['cases']):
            raise ValueError('duplicate saved case ID')
        for i, case in enumerate(doc['cases']):
            batch = batches[case['batch_id']]
            by_case = case['case_id'].upper() == term
            by_fixture = any(r['fixture_id'].upper() == term for r in batch['modes'])
            if by_case or by_fixture:
                direct = [r for r in case['parent_and_case_roles'] if kind is None or r['kind'].upper() == kind]
                held = [r for r in case['held_context_roles'] if kind is None or r['kind'].upper() == kind]
            else:
                direct = [r for r in case['parent_and_case_roles'] if _matches(r, term, kind)]
                held = [r for r in case['held_context_roles'] if _matches(r, term, kind)]
            if not (direct or held or ((by_case or by_fixture) and kind is None)):
                continue
            if case['case_id'] not in batch['case_ids']:
                raise ValueError('case not linked to its recorded batch')
            results.append({'collection': 'printdata_saved', 'case_id': case['case_id'],
                'match_basis': 'CASE_ID' if by_case else ('FIXTURE_ID' if by_fixture else 'TYPED_ROLE'),
                'matched_parent_roles': direct, 'matched_held_context_roles': held,
                'recorded_parent_roles': case['parent_and_case_roles'],
                'held_context_roles': case['held_context_roles'],
                'recorded_verdict': case['scenario_verdict'],
                'recorded_condition_context': case['fixtures_and_initial_state']['condition'].get('context'),
                'preparation_runtime_observation': case['fixtures_and_initial_state']['condition'].get('runtime_observation'),
                'preparation_not_run_is_saved_run_status': False,
                'saved_modes': [r['mode'] for r in batch['modes']],
                'fixture_id_by_mode': {r['mode']: r['fixture_id'] for r in batch['modes']},
                'fixture_identity_scope': 'RECORDED_FIXTURE_ID_NOT_FULL_CONDITION_OR_CONFIG_EQUALITY',
                'shared_batch_case_ids': batch['case_ids'],
                'shared_batch_case_count': len(batch['case_ids']),
                'sharing_scope': 'RECORDED_BATCH_ONLY_SAME_SHA_DOES_NOT_PROVE_SAME_RUN_OR_CONDITION',
                'target_reach': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'record': _reference(printpath, root, pointer='/cases/'+str(i))})
        availability['printdata_saved'] = 'AVAILABLE'
    else:
        if printdata_override:
            raise ValueError('explicit PRINTDATA index is unavailable')
        availability['printdata_saved'] = 'NOT_INSTALLED'
    required = [obsroot/'cases.jsonl', obsroot/'batches.jsonl', obsroot/'modes.jsonl']
    if obsroot.is_dir():
        if not all(p.is_file() for p in required):
            raise ValueError('observation source is incomplete')
        cases, batch_rows, mode_rows = map(_rows, required)
        batches = {b['batch_id']: b for b in batch_rows}
        modes = {m['mode_id']: m for m in mode_rows}
        if len(batches) != len(batch_rows) or len(modes) != len(mode_rows):
            raise ValueError('duplicate observation batch or mode ID')
        if len({c['case_id'] for c in cases}) != len(cases):
            raise ValueError('duplicate observation case ID')
        for i, case in enumerate(cases):
            by_case = case['case_id'].upper() == term
            by_fixture = any(modes.get(ref['mode_id'], {}).get('fixture_id', '').upper() == term for ref in case['modes'].values())
            if by_case or by_fixture:
                roles = [r for r in case['case_roles'] if kind is None or r['kind'].upper() == kind]
            else:
                roles = [r for r in case['case_roles'] if _matches(r, term, kind)]
            if not (roles or ((by_case or by_fixture) and kind is None)):
                continue
            batch = batches[case['batch_id']]
            if case['case_id'] not in batch['case_ids']:
                raise ValueError('case not linked to its recorded batch')
            saved_modes = []
            fixtures = {}
            for mode, reference in case['modes'].items():
                mode_id = reference['mode_id']
                record = modes[mode_id]
                if record['mode'] != mode:
                    raise ValueError('observation mode identity mismatch')
                batch_ids = batch['native_02_mode_ids'] if mode == 'native-02' else [batch[mode.replace('-', '_')+'_mode_id']]
                if mode_id not in batch_ids:
                    raise ValueError('observation mode not linked to batch')
                saved_modes.append(mode)
                fixtures[mode] = record['fixture_id']
            source = case.get('record', case.get('source_case_record', {}))
            results.append({'collection': 'observation_saved', 'case_id': case['case_id'],
                'match_basis': 'CASE_ID' if by_case else ('FIXTURE_ID' if by_fixture else 'TYPED_ROLE'),
                'matched_parent_roles': roles, 'matched_held_context_roles': [],
                'recorded_parent_roles': case['case_roles'], 'held_context_roles': [],
                'recorded_verdict': case.get('scenario_verdict', source.get('scenario_verdict')),
                'recorded_condition_context': None,
                'saved_modes': saved_modes,
                'not_in_saved_mode_index': [m for m in ('native-01', 'native-02', 'public-01') if m not in saved_modes],
                'fixture_id_by_mode': fixtures, 'shared_batch_case_ids': batch['case_ids'],
                'fixture_identity_scope': 'RECORDED_FIXTURE_ID_NOT_FULL_CONDITION_OR_CONFIG_EQUALITY',
                'shared_batch_case_count': len(batch['case_ids']),
                'sharing_scope': 'RECORDED_SHARED_BATCH_NOT_PROOF_SAME_CONDITION_ROLE_REACH_OR_EXECUTION_COUNT',
                'target_reach': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'record': _reference(required[0], root, line=i+1)})
        availability['observation_saved'] = 'AVAILABLE'
    else:
        if observation_override:
            raise ValueError('explicit observation directory is unavailable')
        availability['observation_saved'] = 'NOT_INSTALLED'
    csvpath = root / 'evidence/csv-numeric-45-20261117/index.json'
    if csvpath.is_file():
        csv = json.loads(csvpath.read_text(encoding='utf-8'))
        if csv.get('schema') != 'csv-numeric-saved-evidence-1':
            raise ValueError('unsupported CSV numeric saved index schema')
        batches = {b['batch_id']: b for b in csv['batches']}
        if len(batches) != len(csv['batches']) or len({c['case_id'] for c in csv['cases']}) != len(csv['cases']):
            raise ValueError('duplicate CSV case or batch ID')
        for i, case in enumerate(csv['cases']):
            direct_roles = case['parent_and_case_roles']
            direct_keys = {(r['kind'], r['name']) for r in direct_roles}
            registered_only = [r for r in case['registered_roles'] if (r['kind'], r['name']) not in direct_keys]
            by_case = case['case_id'].upper() == term
            if by_case:
                matched_direct = [r for r in direct_roles if kind is None or r['kind'].upper() == kind]
                matched_registered = [r for r in registered_only if kind is None or r['kind'].upper() == kind]
            else:
                matched_direct = [r for r in direct_roles if _matches(r, term, kind)]
                matched_registered = [r for r in registered_only if _matches(r, term, kind)]
            if not (matched_direct or matched_registered or (by_case and kind is None)):
                continue
            batch = batches[case['batch_id']]
            if case['case_id'] not in batch['case_ids'] or batch['fixture_id'] != case['source_condition_id']:
                raise ValueError('CSV case not linked to its recorded batch')
            results.append({'collection': 'csv_numeric_saved', 'case_id': case['case_id'],
                'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'matched_parent_roles': matched_direct,
                'matched_registered_only_roles': matched_registered,
                'recorded_parent_roles': direct_roles, 'recorded_registered_only_roles': registered_only,
                'recorded_verdict': case['case_registry_verdict'],
                'verdict_scope': 'CASE_REGISTRY_NOT_TARGET_ACCEPTANCE',
                'partial_preparation_affected': case['partial_preparation_affected'],
                'executor_comparison_status': case['executor_comparison_status'],
                'parent_review_artifact': case['parent_review_artifact'],
                'separate_sp_repair_cases': 'FOUR_LATER_CASES_NOT_INCLUDED_IN_THIS_BUNDLE',
                'saved_modes': [m['mode'] for m in batch['modes']],
                'fixture_id_by_mode': {m['mode']: m['fixture_id'] for m in batch['modes']},
                'fixture_identity_scope': 'RECORDED_FIXTURE_ID_NOT_FULL_CONDITION_OR_CONFIG_EQUALITY',
                'native_natural_exit_by_mode': {m['mode']: m['natural_exit'] for m in batch['modes'] if m['mode'].startswith('native-')},
                'shared_batch_case_ids': batch['case_ids'], 'shared_batch_case_count': len(batch['case_ids']),
                'sharing_scope': 'RECORDED_BATCH_ONLY_SAME_SHA_DOES_NOT_PROVE_SAME_RUN_OR_CONDITION',
                'target_reach': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'record': _reference(csvpath, root, pointer='/cases/'+str(i))})
        availability['csv_numeric_saved'] = 'AVAILABLE'
    else:
        availability['csv_numeric_saved'] = 'NOT_INSTALLED'
    remainingpath = root / 'evidence/remaining-96-20261117/index.json'
    if remainingpath.is_file():
        if not (remainingpath.parent / 'references.json').is_file():
            raise ValueError('remaining-96 references unavailable')
        doc = json.loads(remainingpath.read_text(encoding='utf-8'))
        if doc.get('schema') != 'saved-three-group-evidence-1':
            raise ValueError('unsupported remaining-96 saved index schema')
        batches = {b['batch_id']: (i, b) for i, b in enumerate(doc['batches'])}
        if len(batches) != len(doc['batches']) or len({c['case_id'] for c in doc['cases']}) != len(doc['cases']):
            raise ValueError('duplicate remaining-96 case or batch ID')
        for i, case in enumerate(doc['cases']):
            direct = case['parent_and_case_roles']
            direct_keys = {(r['kind'], r['name']) for r in direct}
            registered_only = [r for r in case['registered_roles'] if (r['kind'], r['name']) not in direct_keys]
            by_case = case['case_id'].upper() == term
            if by_case:
                matched = [r for r in direct if kind is None or r['kind'].upper() == kind]
                matched_registered = [r for r in registered_only if kind is None or r['kind'].upper() == kind]
            else:
                matched = [r for r in direct if _matches(r, term, kind)]
                matched_registered = [r for r in registered_only if _matches(r, term, kind)]
            if not (matched or matched_registered or (by_case and kind is None)):
                continue
            batch_index, batch = batches[case['batch_id']]
            if case['case_id'] not in batch['case_ids']:
                raise ValueError('remaining-96 case not linked to its recorded batch')
            modes = batch['modes']
            if ([m['mode'] for m in modes] != ['native-01', 'native-02', 'public-01'] or
                    any(m['fixture_id'] != batch['fixture_id'] for m in modes)):
                raise ValueError('remaining-96 batch mode or fixture mismatch')
            condition = case['record'].get('observation_points_and_comparison')
            condition_id = condition.get('id') if isinstance(condition, dict) else None
            if case['group'] == 'unicode-codeunit-followup':
                semantic_condition = case['saved_semantic_readback']['condition']
                if (not isinstance(condition, dict) or condition_id != semantic_condition['id'] or
                        condition['fixture'] != batch['fixture_id'] or condition['fixture'] != semantic_condition['fixture'] or
                        condition['target'] != semantic_condition['target'] or condition['target'] not in direct):
                    raise ValueError('remaining-96 Unicode condition or role mismatch')
            results.append({'collection': 'remaining_96_saved', 'case_id': case['case_id'],
                'group': case['group'], 'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'matched_parent_roles': matched, 'matched_registered_only_roles': matched_registered,
                'recorded_parent_roles': direct, 'recorded_registered_only_roles': registered_only,
                'recorded_verdict': case['record']['scenario_verdict'],
                'verdict_scope': 'CASE_REGISTER_NOT_NEW_TARGET_ACCEPTANCE',
                'adjudication_timing': ('EXECUTION_PARENT_REVIEW_PENDING_LATER_CASE_REGISTER_VERDICT_SEPARATE'
                                        if case['group'] == 'string-slice-repaired-comparison' else 'SEE_SAVED_RECORD'),
                'recorded_condition_id': condition_id,
                'saved_modes': [m['mode'] for m in modes], 'fixture_id': batch['fixture_id'],
                'shared_batch_case_ids': batch['case_ids'], 'shared_batch_case_count': len(batch['case_ids']),
                'sharing_scope': 'RECORDED_BATCH_NOT_PROOF_OF_SEPARATE_RUNS_OR_TARGET_REACH',
                'target_reach': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'target_return': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'native_natural_exit_by_mode': {m['mode']: m['native_natural_exit'] for m in modes if m['mode'].startswith('native-')},
                'raw_binding_basis_by_mode': {m['mode']: m['raw_binding_basis'] for m in modes},
                'omitted_materials': 'ORIGINAL_RECEIPTS_STDERR_EXECUTABLES_COMPLETE_PARENT_RECORDS_AND_OTHER_OUTPUTS_NOT_INCLUDED',
                'record': _reference(remainingpath, root, pointer='/cases/'+str(i)),
                'batch_record': _reference(remainingpath, root, pointer='/batches/'+str(batch_index)),
                'references': _reference(remainingpath.parent/'references.json', root)})
        availability['remaining_96_saved'] = 'AVAILABLE'
    else:
        availability['remaining_96_saved'] = 'NOT_INSTALLED'
    selectedpath = root / 'evidence/selected-51-20261117/index.json'
    selected_bytes = _pinned_bundle_member(selectedpath, _SELECTED51_MANIFEST_SHA256, 'selected-51')
    if selected_bytes is not None:
        if not all((selectedpath.parent / name).is_file() for name in ('references.json', 'README.md')):
            raise ValueError('selected-51 references or README unavailable')
        doc = json.loads(selected_bytes)
        if doc.get('schema') != 'selected-three-group-evidence-1':
            raise ValueError('unsupported selected-51 saved index schema')
        batches = {b['batch_id']: (i, b) for i, b in enumerate(doc['batches'])}
        if len(batches) != len(doc['batches']) or len({c['case_id'] for c in doc['cases']}) != len(doc['cases']):
            raise ValueError('duplicate selected-51 case or batch ID')
        for i, case in enumerate(doc['cases']):
            direct = case['parent_and_case_roles']
            direct_keys = {(r['kind'], r['name']) for r in direct}
            registered_only = [r for r in case['registered_roles'] if (r['kind'], r['name']) not in direct_keys]
            by_case = case['case_id'].upper() == term
            if by_case:
                matched = [r for r in direct if kind is None or r['kind'].upper() == kind]
                matched_registered = [r for r in registered_only if kind is None or r['kind'].upper() == kind]
            else:
                matched = [r for r in direct if _matches(r, term, kind)]
                matched_registered = [r for r in registered_only if _matches(r, term, kind)]
            if not (matched or matched_registered or (by_case and kind is None)):
                continue
            batch_index, batch = batches[case['batch_id']]
            if batch['case_ids'] != [case['case_id']]:
                raise ValueError('selected-51 case not linked to its recorded batch')
            modes = batch['modes']
            if [m['mode'] for m in modes] != ['native-01', 'native-02', 'public-01']:
                raise ValueError('selected-51 batch mode mismatch')
            inputs_by_mode = {}
            for m in modes:
                prefix = 'assets/' + case['batch_id'] + '/' + m['mode'] + '/inputs/'
                inputs = []
                for item in m['inputs']:
                    name = item['relative_name']
                    if (not isinstance(name, str) or not name or ':' in name or '\\' in name or
                            any(part in ('', '.', '..') for part in name.split('/')) or
                            item['path'] != prefix + name or not (selectedpath.parent / item['path']).is_file()):
                        raise ValueError('selected-51 input path missing or inconsistent')
                    inputs.append({'relative_name': name, 'sha256': item['sha256'],
                                   'record': _reference(selectedpath.parent / item['path'], root)})
                names = [item['relative_name'] for item in inputs]
                required = ({'ERB/CASE.ERB', 'ERB/ARRAYMSORT176.ERH', 'ERB/ENDPOINT_READBACK.ERH', 'emuera.config'}
                            if case['group'] == 'array-aggregate-method-endpoints'
                            else {'ERB/SEARCHBOUND01.ERB', 'emuera.config'})
                if len(names) != len(set(names)) or not required.issubset(names):
                    raise ValueError('selected-51 input set incomplete')
                inputs_by_mode[m['mode']] = inputs
            condition = case['record'].get('observation_points_and_comparison')
            condition_id = condition.get('id') if isinstance(condition, dict) else None
            if case['group'] == 'array-aggregate-method-endpoints' and (
                    not isinstance(condition, dict) or condition.get('target') not in direct):
                raise ValueError('selected-51 condition role mismatch')
            results.append({'collection': 'selected_51_saved', 'case_id': case['case_id'],
                'group': case['group'], 'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'matched_parent_roles': matched, 'matched_registered_only_roles': matched_registered,
                'recorded_parent_roles': direct, 'recorded_registered_only_roles': registered_only,
                'recorded_verdict': case['record']['scenario_verdict'],
                'verdict_scope': 'CASE_REGISTER_NOT_NEW_TARGET_ACCEPTANCE',
                'recorded_condition_id': condition_id,
                'saved_modes': [m['mode'] for m in modes], 'inputs_by_mode': inputs_by_mode,
                'input_scope': 'MODE_SPECIFIC_SAVED_INPUTS_NOT_PROOF_SAME_RUN_OR_CONDITION',
                'identity_basis_by_mode': {m['mode']: m['identity_basis'] for m in modes},
                'shared_batch_case_ids': batch['case_ids'], 'shared_batch_case_count': len(batch['case_ids']),
                'target_reach': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'target_return': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'native_natural_exit_by_mode': {m['mode']: m['native_natural_exit'] for m in modes if m['mode'].startswith('native-')},
                'omitted_materials': 'ORIGINAL_RECEIPTS_STDERR_EXECUTABLES_COMPLETE_PARENT_RECORDS_AND_OTHER_OUTPUTS_NOT_INCLUDED',
                'record': _reference(selectedpath, root, pointer='/cases/'+str(i)),
                'batch_record': _reference(selectedpath, root, pointer='/batches/'+str(batch_index)),
                'references': _reference(selectedpath.parent/'references.json', root),
                'source_manifest': 'NOT_INCLUDED_SEE_BUNDLE_README',
                'bundle_readme': _reference(selectedpath.parent/'README.md', root)})
        availability['selected_51_saved'] = 'AVAILABLE'
    else:
        availability['selected_51_saved'] = 'NOT_INSTALLED'
    prioritypath = root / 'evidence/target-priority-28-20261117/index.json'
    if prioritypath.is_file():
        if not all((prioritypath.parent / name).is_file() for name in ('references.json', 'README.md')):
            raise ValueError('target-priority-28 references or README unavailable')
        doc = json.loads(prioritypath.read_text(encoding='utf-8'))
        if doc.get('schema') != 'selected-three-group-evidence-1':
            raise ValueError('unsupported target-priority-28 saved index schema')
        batches = {b['batch_id']: (i, b) for i, b in enumerate(doc['batches'])}
        if len(batches) != len(doc['batches']) or len({c['case_id'] for c in doc['cases']}) != len(doc['cases']):
            raise ValueError('duplicate target-priority-28 case or batch ID')
        for i, case in enumerate(doc['cases']):
            direct = case['parent_and_case_roles']
            direct_keys = {(r['kind'], r['name']) for r in direct}
            registered_only = [r for r in case['registered_roles'] if (r['kind'], r['name']) not in direct_keys]
            by_case = case['case_id'].upper() == term
            if by_case:
                matched = [r for r in direct if kind is None or r['kind'].upper() == kind]
                matched_registered = [r for r in registered_only if kind is None or r['kind'].upper() == kind]
            else:
                matched = [r for r in direct if _matches(r, term, kind)]
                matched_registered = [r for r in registered_only if _matches(r, term, kind)]
            if not (matched or matched_registered or (by_case and kind is None)):
                continue
            batch_index, batch = batches[case['batch_id']]
            modes = batch['modes']
            if batch['case_ids'] != [case['case_id']] or [m['mode'] for m in modes] != ['native-01', 'native-02', 'public-01']:
                raise ValueError('target-priority-28 case or mode binding mismatch')
            legacy = case['group'] == 'list-owner-completion'
            basis = ('case_evidence_and_source_path_receipt_has_no_case_or_mode' if legacy
                     else 'case_evidence_source_path_and_receipt_case_mode')
            mode_refs = {}
            for mode in modes:
                name = mode['mode']
                if mode['identity_basis'] != basis or mode['native_natural_exit'] != ('not_established_from_receipt' if name.startswith('native-') else 'not_applicable'):
                    raise ValueError('target-priority-28 receipt identity or exit scope mismatch')
                prefix = 'assets/' + case['batch_id'] + '/' + name + '/'
                def ref(item, expected):
                    if item['path'] != expected or not (prioritypath.parent / expected).is_file():
                        raise ValueError('target-priority-28 asset missing or inconsistent')
                    return {'sha256': item['sha256'], 'record': _reference(prioritypath.parent / expected, root)}
                raw = ref(mode['raw'], prefix + 'raw.bin')
                receipt = ref(mode['receipt'], prefix + 'receipt.json')
                inputs = {}
                for item in mode['inputs']:
                    rel = item['relative_name']
                    if (not isinstance(rel, str) or not rel or ':' in rel or '\\' in rel or
                            any(part in ('', '.', '..') for part in rel.split('/')) or rel in inputs):
                        raise ValueError('unsafe or duplicate target-priority-28 input')
                    inputs[rel] = ref(item, prefix + 'inputs/' + rel)
                fixture = {'call-jump-event-comparison': 'ERB/REVIEW.ERB',
                           'print-d-style-comparison': 'ERB/MAIN.ERB',
                           'list-owner-completion': 'ERB/LISTBOUND.ERB'}.get(case['group'])
                if fixture is None or set(inputs) != {fixture, 'emuera.config'}:
                    raise ValueError('target-priority-28 input set mismatch')
                mode_refs[name] = {'raw': raw, 'derived_receipt': receipt, 'inputs': inputs,
                                   'identity_basis': mode['identity_basis']}
            observation = case['record'].get('observation_points_and_comparison', '')
            uncalled = legacy and isinstance(observation, str) and 'This case is uncalled' in observation
            results.append({'collection': 'target_priority_28_saved', 'case_id': case['case_id'],
                'group': case['group'], 'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'matched_parent_roles': matched, 'matched_registered_only_roles': matched_registered,
                'recorded_parent_roles': direct, 'recorded_registered_only_roles': registered_only,
                'recorded_verdict': case['record']['scenario_verdict'],
                'verdict_scope': 'CASE_REGISTER_NOT_NEW_TARGET_ACCEPTANCE',
                'recorded_case_scope': 'UNCALLED_AS_RECORDED' if uncalled else 'SEE_CASE_RECORD',
                'parent_readback_scope': ('NOT_INCLUDED_SHARED_GROUP_SUMMARY_NOT_CASE_OBSERVATION'
                                          if legacy else 'NOT_INCLUDED'),
                'source_receipt_case_mode': ('NOT_DECLARED_BINDING_FROM_CASE_EVIDENCE_AND_SOURCE_PATH'
                                             if legacy else 'DECLARED_IN_SOURCE_RECEIPT'),
                'saved_modes': [m['mode'] for m in modes], 'mode_references': mode_refs,
                'native_natural_exit_by_mode': {m['mode']: m['native_natural_exit'] for m in modes if m['mode'].startswith('native-')},
                'target_reach': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'target_return': 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH',
                'post_fatal_state': 'NOT_INFERRED_SEE_CASE_RECORD',
                'sharing_scope': 'RECORDED_BATCH_NOT_PROOF_OF_SAME_OR_INDEPENDENT_EXECUTIONS',
                'omitted_materials': 'ORIGINAL_RECEIPTS_ARGV_STDERR_EXECUTABLES_COMPLETE_PARENT_RECORDS_AND_OTHER_OUTPUTS_NOT_INCLUDED',
                'record': _reference(prioritypath, root, pointer='/cases/'+str(i)),
                'batch_record': _reference(prioritypath, root, pointer='/batches/'+str(batch_index)),
                'references': _reference(prioritypath.parent/'references.json', root),
                'bundle_readme': _reference(prioritypath.parent/'README.md', root)})
        availability['target_priority_28_saved'] = 'AVAILABLE'
    else:
        availability['target_priority_28_saved'] = 'NOT_INSTALLED'
    kdpath = root / 'evidence/print-kd-shared-82-20261117/index.json'
    if kdpath.is_file():
        scopepath = kdpath.parent / 'scope.json'
        if not scopepath.is_file() or not (kdpath.parent / 'README.md').is_file():
            raise ValueError('PRINT K/D shared scope or README unavailable')
        doc = json.loads(kdpath.read_text(encoding='utf-8'))
        scope = json.loads(scopepath.read_text(encoding='utf-8'))
        if doc.get('schema') != 'printkd212-shared-saved-evidence-1':
            raise ValueError('unsupported PRINT K/D shared index schema')
        cases = doc['cases']
        if len(cases) != 82 or len({c['case_id'] for c in cases}) != 82 or len(doc['batches']) != 1:
            raise ValueError('PRINT K/D shared case or batch set mismatch')
        batch = doc['batches'][0]
        if (len(batch['case_ids']) != 82 or set(batch['case_ids']) != {c['case_id'] for c in cases}
                or [m['mode'] for m in batch['modes']] != ['native-01', 'native-02', 'py']
                or any(c['batch_id'] != batch['batch_id'] for c in cases)):
            raise ValueError('PRINT K/D shared batch binding mismatch')
        omitted = scope['unselected_conditions']
        if (scope['shared_source_condition_count'] != 88 or scope['selected_condition_count'] != 81
                or scope['selected_aggregate_case_count'] != 1 or len(omitted) != 7
                or len({x['condition_id'] for x in omitted}) != 7
                or len({x['case_id'] for x in omitted}) != 7
                or {x['case_id'] for x in omitted} & {c['case_id'] for c in cases}):
            raise ValueError('PRINT K/D selected and unselected scope mismatch')
        outputs = {}
        for mode in batch['modes']:
            expected = {'history', 'stdout'} if mode['mode'] == 'py' else {'history'}
            if set(mode['outputs']) != expected:
                raise ValueError('PRINT K/D shared output kinds mismatch')
            for output, asset in mode['outputs'].items():
                rel = asset['path']
                if (not isinstance(rel, str) or not rel.startswith('assets/') or ':' in rel or '\\' in rel
                        or any(part in ('', '.', '..') for part in rel.split('/'))
                        or not (kdpath.parent / rel).is_file()):
                    raise ValueError('PRINT K/D shared output missing or unsafe')
                outputs[mode['mode'] + '_' + output] = {
                    'sha256': asset['sha256'], 'record': _reference(kdpath.parent / rel, root)}
        shared = {'shared_batch_id': batch['batch_id'], 'shared_batch_case_count': 82,
                  'saved_modes': ['native-01', 'native-02', 'py'],
                  'sharing_scope': 'ONE_RECORDED_BATCH_NOT_82_INDEPENDENT_RUNS_OR_TARGET_REACH',
                  'target_reach': 'NOT_INFERRED_FROM_CASE_ROLE_OR_SHARED_BATCH',
                  'native_natural_exit': 'NOT_OBSERVED_CLEANUP_IS_SEPARATE',
                  'shared_output_references': outputs,
                  'batch_record': _reference(kdpath, root, pointer='/batches/0'),
                  'scope_record': _reference(scopepath, root),
                  'bundle_readme': _reference(kdpath.parent / 'README.md', root)}
        for i, case in enumerate(cases):
            direct = case['roles']
            direct_keys = {(r['kind'], r['name']) for r in direct}
            registered_only = [r for r in case['registered_roles'] if (r['kind'], r['name']) not in direct_keys]
            by_case = case['case_id'].upper() == term
            if by_case:
                matched = [r for r in direct if kind is None or r['kind'].upper() == kind]
                matched_registered = [r for r in registered_only if kind is None or r['kind'].upper() == kind]
            else:
                matched = [r for r in direct if _matches(r, term, kind)]
                matched_registered = [r for r in registered_only if _matches(r, term, kind)]
            if not (matched or matched_registered or (by_case and kind is None)):
                continue
            relation = case['relationship']
            relation_kind = relation['kind']
            if relation_kind == 'case_condition_exact':
                condition = relation['condition_id']
                comparison = relation['comparison']
                if comparison['condition']['id'] != condition:
                    raise ValueError('PRINT K/D case condition mismatch')
                empty_single = comparison['category'] == 'empty_single_serialized_line_lifecycle'
                if empty_single and relation['byte_references']['public-stdout']['comparison_raw_block_span'] is not None:
                    raise ValueError('PRINT K/D empty SINGLE stdout scope mismatch')
                comparison_ref = _reference(kdpath, root, pointer='/cases/'+str(i)+'/relationship/comparison')
                byte_refs = _reference(kdpath, root, pointer='/cases/'+str(i)+'/relationship/byte_references')
            elif relation_kind == 'aggregate_interaction_not_setter_identity':
                condition, empty_single, comparison_ref, byte_refs = None, False, None, None
            else:
                raise ValueError('unsupported PRINT K/D case relationship')
            results.append({**shared, 'collection': 'print_kd_shared_82_saved',
                'case_id': case['case_id'], 'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'matched_parent_roles': matched, 'matched_registered_only_roles': matched_registered,
                'recorded_parent_roles': direct, 'recorded_registered_only_roles': registered_only,
                'recorded_verdict': case['record']['scenario_verdict'],
                'verdict_scope': 'CASE_REGISTER_NOT_NEW_TARGET_ACCEPTANCE',
                'case_relationship': relation_kind, 'condition_id': condition,
                'forcekana_setter_failure': 'NOT_INFERRED_FROM_AGGREGATE_INTERACTION',
                'public_history_stdout_scope': ('EMPTY_SINGLE_HISTORY_AND_STDOUT_BLANK_LINE_BYTES_DIFFER'
                    if empty_single else ('DISTINCT_OUTPUTS_NO_SINGLE_COMPARISON_BLOCK_FOR_AGGREGATE'
                    if relation_kind == 'aggregate_interaction_not_setter_identity'
                    else 'DISTINCT_OUTPUTS_COMPARISON_BLOCK_FROM_HISTORY')),
                'record': _reference(kdpath, root, pointer='/cases/'+str(i)),
                'comparison_record': comparison_ref, 'byte_references_record': byte_refs})
        for i, item in enumerate(omitted):
            by_case = item['case_id'].upper() == term
            target = item['target']
            matched = ([target] if (kind is None or target['kind'].upper() == kind) else []) if by_case else (
                       [target] if _matches(target, term, kind) else [])
            if not (matched or (by_case and kind is None)):
                continue
            if item['selection_status'] != 'OUTSIDE_THIS_82_CASE_SELECTION_NOT_A_CLAIM_OF_NONOBSERVATION':
                raise ValueError('PRINT K/D unselected condition status mismatch')
            results.append({**shared, 'collection': 'print_kd_shared_82_scope',
                'case_id': item['case_id'], 'condition_id': item['condition_id'],
                'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                'matched_parent_roles': [], 'scope_target': target,
                'selection_status': item['selection_status'], 'recorded_verdict': None,
                'record': _reference(scopepath, root, pointer='/unselected_conditions/'+str(i))})
        availability['print_kd_shared_82'] = 'AVAILABLE'
    else:
        availability['print_kd_shared_82'] = 'NOT_INSTALLED'

    display, display_state = _display_state_21(term, root, kind)
    results.extend(display)
    availability['display_state_21'] = display_state
    operator, operator_state = _operator_normal_6(term, root, kind)
    results.extend(operator)
    availability['operator_normal_6'] = operator_state
    method_display, method_display_state = _method_display_state_15(term, root, kind)
    results.extend(method_display)
    availability['method_display_state_15'] = method_display_state
    wait, wait_states = _wait_observations(term, root, kind)
    results.extend(wait)
    availability.update(wait_states)
    graphics, graphics_state = _graphics_38(term, root, kind)
    results.extend(graphics)
    availability['graphics_38'] = graphics_state
    try:
        normal, normal_state = _normal_observations_196(term, root, kind)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        if not allow_partial:
            raise
        normal, normal_state = [], 'INCONSISTENT'
    results.extend(normal)
    availability['normal_observations_196'] = normal_state
    return results, availability

_PRIVATE_PATH = re.compile(
    r"(?i)(?<![a-z0-9_])[a-z]:[\\/]|\\\\[a-z0-9_.-]+\\|"
    r"(?:^|[\s\"\x27])/(?:home|users|tmp|var|root|mnt|workspace|work|media)/|"
    r"(?<![a-z0-9_])private[\\/]"
)
_CORE_KEYS = {'case_id', 'targets', 'scenario_verdict', 'survey_pointer', 'trace_aliases',
              'target_positions_outside_694', 'runtime_observation_context'}


def _has_private_path(value):
    if isinstance(value, str):
        return _PRIVATE_PATH.search(value) is not None
    if isinstance(value, list):
        return any(_has_private_path(x) for x in value)
    if isinstance(value, dict):
        return any(_has_private_path(k) or _has_private_path(v) for k, v in value.items())
    return False


def _json_pointer(doc, pointer):
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError('invalid saved pointer')
    value = doc
    for part in pointer[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def _snapshot(root, relpath, expected):
    path = root / relpath
    if not path.is_file():
        return None, 'NOT_INSTALLED'
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        return None, 'SNAPSHOT_MISMATCH'
    return json.loads(raw), 'MATCHING_SNAPSHOT'


def case_register_projection(term, root, override=None, kind=None):
    """Find screened core rows; detailed draft fields are never emitted."""
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    directory = Path(override) if override else root / 'evidence/case-register-2898-20261117'
    if not directory.exists():
        if override:
            raise ValueError('explicit case projection is unavailable')
        return [], {'state': 'NOT_INSTALLED'}
    manifest = json.loads((directory / 'manifest.json').read_bytes())
    if manifest.get('schema') not in ('case-register-neutral-screened-draft-v1', 'case-register-neutral-screened-draft-v2'):
        raise ValueError('unsupported case projection schema')
    core_path, detail_path = directory / 'core.jsonl', directory / 'cases.jsonl'
    core_raw, detail_raw = core_path.read_bytes(), detail_path.read_bytes()
    for name, raw in (('core.jsonl', core_raw), ('cases.jsonl', detail_raw)):
        if hashlib.sha256(raw).hexdigest() != manifest['files'][name]['sha256']:
            raise ValueError('case projection hash mismatch')
    core_lines, detail_lines = core_raw.decode('utf-8').splitlines(), detail_raw.splitlines()
    if any(not line.strip() for line in core_lines) or any(not line.strip() for line in detail_lines):
        raise ValueError('blank case projection line')
    rows = [json.loads(line) for line in core_lines]
    ids = [r['case_id'].upper() for r in rows]
    if (len(rows) != manifest['records'] or len(detail_lines) != len(rows)
            or len(set(ids)) != len(ids)):
        raise ValueError('case projection count or ID conflict')
    survey, survey_state = _snapshot(root, 'results/survey.json', manifest['candidate_survey_sha256'])
    trace, trace_state = _snapshot(root, 'evidence/694-target-trace-20261117/projection.json',
                                   manifest['candidate_trace_sha256'])
    matches = []
    for i, row in enumerate(rows):
        if set(row) != _CORE_KEYS:
            raise ValueError('unsupported core fields')
        by_case = row['case_id'].upper() == term
        roles = ([r for r in row['targets'] if kind is None or r['kind'].upper() == kind]
                 if by_case else [r for r in row['targets'] if _matches(r, term, kind)])
        if not (roles or (by_case and kind is None)):
            continue
        if _has_private_path(row):
            raise ValueError('case core has a private path')
        detail = json.loads(detail_lines[i])
        if any(detail.get(k) != row[k] for k in _CORE_KEYS):
            raise ValueError('case detail and core disagree')
        state = detail['projection_state']
        withheld, neutralized = detail['withheld_count'], detail['neutralized_key_count']
        if (state != 'AUTOMATED_SCREENING_INDEPENDENT_REVIEW_PENDING' or
                type(withheld) is not int or withheld < 0 or
                type(neutralized) is not int or neutralized < 0):
            raise ValueError('unsupported projection review state')
        original_fields = detail['fields']
        markers = {}
        for name in ('evidence', 'review'):
            if name not in original_fields:
                markers[name] = None
                continue
            marker = original_fields[name]
            if (not isinstance(marker, dict) or set(marker) != {'$case_projection_withheld'} or
                    not isinstance(marker['$case_projection_withheld'], str) or
                    not re.fullmatch(r'[a-z0-9_+]+', marker['$case_projection_withheld'])):
                raise ValueError('unsupported non-included marker')
            markers[name] = marker
        survey_ref = None
        if survey is not None:
            target = _json_pointer(survey, row['survey_pointer'])
            if (target['case_id'] != row['case_id'] or target['targets'] != row['targets']
                    or target['scenario_verdict'] != row['scenario_verdict']):
                raise ValueError('case and survey record disagree')
            survey_ref = _reference(root / 'results/survey.json', root, pointer=row['survey_pointer'])
        trace_refs = []
        if trace is not None:
            for alias in row['trace_aliases']:
                target = _json_pointer(trace, alias['trace_pointer'])
                if (target['relation'] != 'CANDIDATE_SURVEY_CASE_ID' or
                        target['candidate_survey_case_id'] != row['case_id'] or
                        target['alias'] != alias['alias']):
                    raise ValueError('case and trace alias disagree')
                trace_refs.append({'alias': alias['alias'],
                    'record': _reference(root / 'evidence/694-target-trace-20261117/projection.json',
                                         root, pointer=alias['trace_pointer'])})
        matches.append({'match_basis': 'CASE_ID' if by_case else 'TYPED_TARGET',
                        'matched_targets': roles, 'case': row,
                        'core_record': _reference(core_path, root, line=i+1),
                        'detail_record': _reference(detail_path, root, line=i+1),
                        'detail_fields': 'NOT_EMITTED_PENDING_REVIEW',
                        'nonincluded_markers': markers,
                        'projection_state': state, 'withheld_count': withheld,
                        'neutralized_key_count': neutralized,
                        'survey_record': survey_ref, 'trace_alias_records': trace_refs})
    return matches, {'state': 'AVAILABLE', 'survey_snapshot': survey_state,
                     'trace_snapshot': trace_state,
                     'scope': 'CORE_FIELDS_ONLY_NOT_NEW_EXECUTION_OR_PUBLICATION_APPROVAL'}



_DISCOVERY_INDEX = 'results/evidence-discovery-26-20261117.json'
_DISCOVERY_INDEX_SHA256 = 'e52a311b94f8a0ec18883f163409f2c321ca6bc82c3d5af792340700d349a210'


def additional_evidence_discovery(term, root, kind=None):
    """Provide pinned record links; do not verify executions or originals."""
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    index_path = root / _DISCOVERY_INDEX
    if not index_path.is_file():
        return [], {'index': 'NOT_INSTALLED', 'groups': {}, 'files': {}}
    try:
        if _reference(index_path, root)['path'] != _DISCOVERY_INDEX:
            return [], {'index': 'UNSAFE_REFERENCE', 'groups': {}, 'files': {}}
        raw = index_path.read_bytes()
        # Normalize line endings only for the index so Git checkout settings are portable.
        if hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() != _DISCOVERY_INDEX_SHA256:
            return [], {'index': 'SNAPSHOT_MISMATCH', 'groups': {}, 'files': {}}
        index = json.loads(raw)
        if index.get('schema') != 'evidence-discovery-26-v1':
            return [], {'index': 'INVALID_DATA', 'groups': {}, 'files': {}}
        groups, entries = index['groups'], index['entries']
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return [], {'index': 'INVALID_DATA', 'groups': {}, 'files': {}}
    results, states, issues, references = [], {}, {}, {}
    for name, group in groups.items():
        try:
            refs = [group['records'], *group['readmes']]
            paths = [root / ref['path'] for ref in refs]
            missing = [ref['path'] for path, ref in zip(paths, refs) if not path.is_file()]
            if missing:
                states[name], issues[name] = 'MISSING_FILES', missing
                continue
            unsafe = [ref['path'] for path, ref in zip(paths, refs)
                      if _reference(path, root)['path'] != ref['path']]
            if unsafe:
                states[name], issues[name] = 'UNSAFE_REFERENCE', unsafe
                continue
            contents = [path.read_bytes() for path in paths]
            mismatched = [ref['path'] for raw, ref in zip(contents, refs)
                          if hashlib.sha256(raw).hexdigest() != ref['sha256']]
            if mismatched:
                states[name], issues[name] = 'SNAPSHOT_MISMATCH', mismatched
                continue
            doc = json.loads(contents[0])
            shared_refs = {}
            for label, pointer in group.get('references', {}).items():
                _json_pointer(doc, pointer)
                shared_refs[label] = _reference(paths[0], root, pointer=pointer)
            group_entries = [entry for entry in entries if entry['collection'] == name]
            seen, case_pointers, group_results = set(), set(), []
            for entry in group_entries:
                target = entry['typed_target']
                case = doc if entry['record_pointer'] == '' else _json_pointer(doc, entry['record_pointer'])
                role = _json_pointer(doc, entry['role_pointer'])
                identity = (entry['case_id'], target['kind'], target['name'])
                if (identity in seen or case['case_id'] != entry['case_id'] or role != target or
                        not entry['role_pointer'].startswith(entry['record_pointer'] + '/')):
                    raise ValueError('discovery record identity mismatch')
                seen.add(identity)
                case_pointers.add(entry['record_pointer'])
                details = {key: case[field] for key, field in group['detail_fields'].items()}
                by_case = entry['case_id'].upper() == term
                matched = ((kind is None or target['kind'].upper() == kind) if by_case
                           else _matches(target, term, kind))
                batch_pointer = entry.get('batch_pointer')
                if batch_pointer is not None:
                    batch = _json_pointer(doc, batch_pointer)
                    if not entry['record_pointer'].startswith(batch_pointer + '/cases/'):
                        raise ValueError('discovery batch identity mismatch')
                if matched:
                    item = {
                        'collection': name, 'case_id': entry['case_id'], 'typed_target': target,
                        'match_basis': 'CASE_ID' if by_case else 'TYPED_ROLE',
                        'record': _reference(paths[0], root, pointer=entry['record_pointer']),
                        'readmes': [_reference(path, root) for path in paths[1:]],
                        'scope_limits': group['scope_limits'], 'details': details,
                        'scope': 'DISCOVERY_ONLY_NOT_ORIGINAL_EXECUTION_OR_RIGHTS_VERIFICATION'}
                    if batch_pointer is not None:
                        item['batch_record'] = _reference(paths[0], root, pointer=batch_pointer)
                        item['batch_scope'] = batch['scope']
                        item['batch_group'] = batch['group']
                        item['shared_batch_case_count'] = len(batch['cases'])
                        item['recorded_case_scope'] = {key: case[key] for key in (
                            'public_target_execution_observed', 'public_target_body_executed',
                            'public_stop_phase', 'public_target_values_credited',
                            'recorded_classification', 'public_classification',
                            'recorded_comparison_axes', 'supplemental_fixture_id', 'caseelse_selected',
                            'public_target_body_reached', 'public_target_runtime_value_observed',
                            'public_target_return_observed', 'native_wait_and_return_recorded',
                            'public_logical_input', 'native_repeat_exact', 'native_public_match')
                            if key in case}
                        item['withheld_history_modes'] = [
                            {'mode': mode['mode'], 'reason': asset.get('reason')}
                            for mode in batch['modes'] for asset in mode['assets']
                            if asset.get('role') == 'history' and asset.get('status') == 'withheld']
                    if shared_refs:
                        item['collection_references'] = shared_refs
                    group_results.append(item)
            arrays = group.get('case_array_pointers', ['/cases'])
            expected = ({''} if group.get('root_case') else
                        {base + '/' + str(i) for base in arrays
                         for i in range(len(_json_pointer(doc, base)))})
            if case_pointers != expected:
                raise ValueError('discovery case set mismatch')
            results.extend(group_results)
            states[name] = 'AVAILABLE'
            if shared_refs:
                references[name] = shared_refs
        except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError):
            states[name] = 'INVALID_DATA'
    availability = {'index': 'AVAILABLE', 'groups': states, 'files': issues}
    if references:
        availability['references'] = references
    return results, availability


def parent_restoration_40(term, root, kind=None):
    """Find historic metadata, without treating it as a fresh acceptance."""
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    folder = root / 'evidence/parent-restoration-40-20261117'
    if not folder.exists():
        return [], 'NOT_INSTALLED'
    pins = {
        'targets.jsonl': 'a9f321e1e851d5cc3f92004286023669ce083fc3de4a8edcab1e16142f28e424',
        'README.ja.md': 'a5ed82ee4b268cb357c8cf9f3835ed163946b57acd71ecebb7de0b6d866a3a32',
        'README.md': '93c1eea6ce894a7fff784d8f023f81b408ceb676f734c19bf64ce864f9e960ee',
    }
    raw = {}
    try:
        for name, digest in pins.items():
            path = folder / name
            if not path.is_file():
                return [], 'INCOMPLETE'
            if _reference(path, root)['path'] is None:
                return [], 'UNSAFE_REFERENCE'
            raw[name] = path.read_bytes()
            if hashlib.sha256(raw[name]).hexdigest() != digest:
                return [], 'SNAPSHOT_MISMATCH'
        lines = raw['targets.jsonl'].decode('utf-8').splitlines()
        if len(lines) != 40 or any(not line.strip() for line in lines):
            return [], 'INVALID_DATA'
        rows = [json.loads(line) for line in lines]
        matches = []
        for i, row in enumerate(rows):
            target = row['target']
            restoration = row['restoration_record']
            later = row['later_ledger_snapshot']
            by_case = any(cid.upper() == term for cid in restoration['case_ids_as_recorded'])
            if by_case:
                matched = kind is None or target['kind'].upper() == kind
            else:
                matched = _matches(target, term, kind)
            if not matched:
                continue
            separate_parent = later['historical_source'].get('separate_later_parent')
            matches.append({
                'target': target,
                'match_basis': 'CASE_ID' if by_case else 'TYPED_TARGET',
                'matched_case_id': next((cid for cid in restoration['case_ids_as_recorded']
                                         if cid.upper() == term), None) if by_case else None,
                'case_ids_as_recorded': restoration['case_ids_as_recorded'],
                'historical_restoration_outcome': restoration['comparison_outcome'],
                'later_ledger_outcome': later['comparison_outcome'],
                'separate_later_parent_outcome': separate_parent['outcome'] if separate_parent else None,
                'source_access': restoration['source_access'],
                'limits': row['limits'],
                'record': _reference(folder / 'targets.jsonl', root, line=i+1),
                'readme_ja': _reference(folder / 'README.ja.md', root),
                'readme_en': _reference(folder / 'README.md', root),
            })
        return matches, 'AVAILABLE'
    except (OSError, UnicodeError, ValueError, KeyError, IndexError, TypeError, AttributeError):
        return [], 'INVALID_DATA'


def native_source_static(term, root, kind=None):
    """Return existing static rows; no source-code or routing inference."""
    path = root / 'evidence/native-source-694-static-20261117/targets.jsonl'
    if not path.is_file():
        return [], {'state': 'NOT_INSTALLED'}
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    rows = _rows(path)
    fields = {'target', 'existing_api75', 'historical_a7', 'historical_a8',
              'independent_original_anchors', 'source_location_status', 'v24_audit',
              'v24_same_name_function_dictionary', 'v24_supplemental_commented_candidate'}
    nested_fields = {'kind', 'name', 'end_line', 'file', 'role', 'start_line',
                     'contract_declared_sha256', 'archive_check',
                     'declared_digest_vs_recorded_registration_text', 'v24_source_file_sha256',
                     'initializer_literal_recorded_present', 'scope'}
    def safe_metadata(value):
        if isinstance(value, list):
            return all(safe_metadata(item) for item in value)
        if isinstance(value, dict):
            if not set(value).issubset(nested_fields):
                return False
            if 'file' in value:
                name = value['file']
                if (not isinstance(name, str) or not name or name.startswith('/') or
                        ':' in name or '\\' in name or any(part in ('', '.', '..') for part in name.split('/')) or
                        name.split('/')[0].lower() in ('private', 'evidence', 'requirements') or
                        any(ch in name for ch in ('\n', '\r', '\0'))):
                    return False
            return all(safe_metadata(item) for item in value.values())
        return value is None or isinstance(value, (str, int, bool))
    keys = set()
    matches = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != fields or not isinstance(row['target'], dict):
            raise ValueError('unsupported native static row fields')
        target = row['target']
        if (set(target) != {'kind', 'name'} or not isinstance(target['kind'], str) or
                not isinstance(target['name'], str) or not target['kind'] or not target['name']):
            raise ValueError('invalid native static target')
        key = (target['kind'].upper(), target['name'].upper())
        if key in keys:
            raise ValueError('duplicate native static typed target')
        keys.add(key)
        if _matches(target, term, kind):
            if _has_private_path(row) or not all(safe_metadata(value) for value in row.values()):
                raise ValueError('native static row has unsafe fields or a private path')
            matches.append({'row': row, 'record': _reference(path, root, line=i+1)})
    return matches, {'state': 'AVAILABLE', 'scope': 'STATIC_INDEX_ONLY_NO_ROUTING_OR_RUNTIME_INFERENCE'}


def native_source_operator30(term, root, kind=None):
    """Return supplemental saved source-location rows without runtime inference."""
    path = root / 'evidence/native-source-operator30-20261117/targets.jsonl'
    if not path.is_file():
        return [], {'state': 'NOT_INSTALLED'}
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    fields = {'target', 'anchor_kind', 'source', 'operator_code', 'il_comparison',
              'scope', 'comment_discrepancy', 'supporting_locations'}
    nested = {'kind', 'name', 'archive', 'inner_archive', 'member', 'line',
              'enum_declaration_line', 'numeric_value', 'status', 'ldstr_il_offset',
              'source_build_identity', 'dictionary_spelling', 'enum_comment_spelling',
              'interpretation', 'lines'}
    def safe_metadata(value):
        if isinstance(value, list):
            return all(safe_metadata(item) for item in value)
        if isinstance(value, dict):
            if not set(value).issubset(nested):
                return False
            for field in ('archive', 'inner_archive', 'member'):
                if field in value:
                    name = value[field]
                    if (not isinstance(name, str) or not name or name.startswith('/') or
                            ':' in name or '\\' in name or any(part in ('', '.', '..') for part in name.split('/')) or
                            name.split('/')[0].lower() in ('private', 'evidence', 'requirements') or
                            any(ch in name for ch in ('\n', '\r', '\0'))):
                        return False
            return all(safe_metadata(item) for item in value.values())
        return value is None or isinstance(value, (str, int, bool))
    matches = []
    keys = set()
    for i, row in enumerate(_rows(path)):
        if (not isinstance(row, dict) or not set(row).issubset(fields) or
                not {'target', 'anchor_kind', 'source', 'scope'}.issubset(row) or
                not isinstance(row['target'], dict)):
            raise ValueError('unsupported operator source row fields')
        target = row['target']
        if (set(target) != {'kind', 'name'} or not isinstance(target['kind'], str) or
                not isinstance(target['name'], str) or not target['kind'] or not target['name']):
            raise ValueError('invalid operator source typed target')
        key = (target['kind'].upper(), target['name'].upper())
        if key in keys:
            raise ValueError('duplicate operator source typed target')
        keys.add(key)
        if _matches(target, term, kind):
            if (_has_private_path(row) or not all(safe_metadata(value) for value in row.values()) or
                    not ((target['kind'] == 'operator' and row['anchor_kind'] == 'operator_dictionary_entry') or
                         (target == {'kind': 'command_or_syntax', 'name': 'SET'} and
                          row['anchor_kind'] == 'internal_assignment_identifier'))):
                raise ValueError('unsafe or inconsistent operator source row')
            matches.append({'row': row, 'record': _reference(path, root, line=i+1)})
    return matches, {'state': 'AVAILABLE',
                     'scope': 'STATIC_DICTIONARY_OR_INTERNAL_IDENTIFIER_NO_EXECUTION_OR_BUILD_IDENTITY'}


def native_source_sha_supplement(term, root, kind=None):
    """Return separately recorded reproduction details without changing historical rows."""
    path = root / 'evidence/native-source-sha-supplement-20261117/results.json'
    if not path.is_file():
        return [], {'state': 'NOT_INSTALLED'}
    if not (path.parent / 'README.md').is_file():
        raise ValueError('native SHA supplement README unavailable')
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    doc = json.loads(path.read_text(encoding='utf-8'))
    fields = {'schema', 'kind', 'source_archive_sha256', 'source_archive_root',
              'source_file', 'source_file_sha256', 'retained_generator',
              'retained_generator_sha256', 'scope', 'contract_input', 'display_input', 'targets'}
    target_fields = {'name', 'source_line', 'contract_sha256', 'display_text_utf8_sha256',
                     'contract_input_bytes', 'includes_comment', 'includes_cr', 'includes_lf'}
    if (not isinstance(doc, dict) or set(doc) != fields or
            doc['schema'] != 'native-source-registration-sha-supplement.v1' or
            not isinstance(doc['kind'], str) or not isinstance(doc['targets'], list) or
            _has_private_path(doc)):
        raise ValueError('unsupported native SHA supplement')
    context = {key: value for key, value in doc.items() if key != 'targets'}
    seen = set()
    matches = []
    for i, item in enumerate(doc['targets']):
        if (not isinstance(item, dict) or set(item) != target_fields or
                not isinstance(item['name'], str) or not item['name']):
            raise ValueError('unsupported native SHA supplement target')
        target = {'kind': doc['kind'], 'name': item['name']}
        key = (target['kind'].upper(), target['name'].upper())
        if key in seen:
            raise ValueError('duplicate native SHA supplement target')
        seen.add(key)
        if _matches(target, term, kind):
            matches.append({'target': target, 'supplement_row': item, 'context': context,
                            'record': _reference(path, root, pointer='/targets/'+str(i)),
                            'readme': _reference(path.parent/'README.md', root)})
    return matches, {'state': 'AVAILABLE',
                     'scope': 'SAVED_GENERATOR_REPRODUCTION_NOT_PROOF_OF_HISTORICAL_CODE_AUTHENTICITY'}


def native_source_anchor82(term, root, kind=None):
    """Return v24 locations separately from earlier source records."""
    path = root / 'evidence/native-source-anchor82-20261117/targets.jsonl'
    payload = _pinned_bundle_member(path, _ANCHOR82_MANIFEST_SHA256, 'native-source-anchor82')
    if payload is None:
        return [], {'state': 'NOT_INSTALLED'}
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            raise ValueError('conflicting typed kind')
        kind, term = typed_kind, typed_name
    fields = {'target', 'anchor_kind', 'source_archive', 'locations', 'limitations',
              'original_source_version_and_sha_identity'}
    nested = {'kind', 'name', 'path', 'sha256', 'inner_member', 'inner_sha256',
              'member', 'source_sha256', 'start_line', 'end_line', 'role', 'context_lines'}
    def safe_metadata(value):
        if isinstance(value, list):
            return all(safe_metadata(item) for item in value)
        if isinstance(value, dict):
            if not set(value).issubset(nested):
                return False
            for field in ('path', 'inner_member', 'member'):
                if field in value:
                    name = value[field]
                    if (not isinstance(name, str) or not name or name.startswith('/') or
                            ':' in name or '\\' in name or any(part in ('', '.', '..') for part in name.split('/')) or
                            name.split('/')[0].lower() in ('private', 'evidence', 'requirements') or
                            any(ch in name for ch in ('\n', '\r', '\0'))):
                        return False
            return all(safe_metadata(item) for item in value.values())
        return value is None or isinstance(value, (str, int, bool))
    matches = []
    keys = set()
    lines = payload.decode('utf-8').splitlines()
    if any(not line.strip() for line in lines):
        raise ValueError('blank JSONL line would make record references ambiguous')
    for i, row in enumerate(map(json.loads, lines)):
        if not isinstance(row, dict) or set(row) != fields or not isinstance(row['target'], dict):
            raise ValueError('unsupported anchor82 source row fields')
        target = row['target']
        if (set(target) != {'kind', 'name'} or not isinstance(target['kind'], str) or
                not isinstance(target['name'], str) or not target['kind'] or not target['name']):
            raise ValueError('invalid anchor82 typed target')
        key = (target['kind'].upper(), target['name'].upper())
        if key in keys:
            raise ValueError('duplicate anchor82 typed target')
        keys.add(key)
        if _matches(target, term, kind):
            if _has_private_path(row) or not all(safe_metadata(value) for value in row.values()):
                raise ValueError('anchor82 row has unsafe fields or a private path')
            matches.append({'row': row, 'record': _reference(path, root, line=i+1)})
    return matches, {'state': 'AVAILABLE',
                     'scope': 'V24_STATIC_LOCATIONS_ONLY_NO_OLD_SOURCE_IDENTITY_REGISTRATION_OR_EXECUTION_INFERENCE'}

_CASE_OBSERVATION_RECOVERY_DIRECTORY = 'evidence/case-observation-recovery-20261117'
_CASE_OBSERVATION_RECOVERY_MANIFEST_SHA256 = '2b2cc247c7846e76d7c163bd33cdb790b58f809ff3b89f83db2a5c9e844f103e'


def case_observation_recovery_links(term, root, kind=None):
    """Return candidate-relative record locations only; keep this collection isolated."""
    term = term.upper()
    kind = kind.upper() if kind else None
    if ':' in term:
        typed_kind, typed_name = term.split(':', 1)
        if kind and kind != typed_kind:
            return [], {'state': 'INVALID_QUERY'}
        kind, term = typed_kind, typed_name
    folder = root / _CASE_OBSERVATION_RECOVERY_DIRECTORY
    if not folder.exists() and not folder.is_symlink():
        return [], {'state': 'NOT_INSTALLED'}
    try:
        manifest = folder / 'manifest.json'
        if (not folder.is_dir() or folder.is_symlink() or not manifest.is_file() or manifest.is_symlink()
                or not folder.resolve().is_relative_to(root.resolve())):
            raise ValueError('recovery bundle location')
        if hashlib.sha256(manifest.read_bytes()).hexdigest() != _CASE_OBSERVATION_RECOVERY_MANIFEST_SHA256:
            raise ValueError('recovery bundle manifest pin')
        helper = _normal_verified_tool()
        spec = importlib.util.spec_from_file_location('case_recovery_file_set_manifest', helper)
        verifier = importlib.util.module_from_spec(spec)
        old = sys.dont_write_bytecode
        try:
            sys.dont_write_bytecode = True
            spec.loader.exec_module(verifier)
        finally:
            sys.dont_write_bytecode = old
        verifier.check_path_components(manifest)
        if verifier.verify(manifest, {'public': folder}) != 13:
            raise ValueError('recovery bundle inventory size')
        child = folder / 'marker-recovery'
        child_manifest_path = child / 'manifest.json'
        child_manifest = json.loads(child_manifest_path.read_text(encoding='utf-8'))
        if (not child_manifest_path.is_file() or child_manifest_path.is_symlink()
                or set(child_manifest) != {'algorithm', 'files'} or child_manifest['algorithm'] != 'sha256'):
            raise ValueError('recovery child manifest')
        expected_files = child_manifest['files']
        actual_files = {}
        for path in child.rglob('*'):
            if path.is_symlink():
                raise ValueError('recovery child link')
            if path.is_file() and path != child_manifest_path:
                relative = path.relative_to(child).as_posix()
                raw = path.read_bytes()
                actual_files[relative] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        if expected_files != actual_files or len(actual_files) != 6:
            raise ValueError('recovery child inventory mismatch')
        sources = (
            ('current_correction', 'marker-recovery/current-candidate-corrections.jsonl', 2),
            ('supplement', 'marker-recovery/risk-observations.jsonl', 38),
            ('base_observation', 'observations.jsonl', 486),
        )
        matches = []
        for record_kind, relative, expected_count in sources:
            path = folder / relative
            rows = _rows(path)
            if len(rows) != expected_count:
                raise ValueError('recovery record count mismatch')
            seen = set()
            for index, row in enumerate(rows):
                case_id = row.get('case_id')
                targets = row.get('targets')
                if (not isinstance(case_id, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,96}', case_id)
                        or case_id.upper() in seen or not isinstance(targets, list)
                        or any(not isinstance(target, dict) or not isinstance(target.get('kind'), str)
                               or not isinstance(target.get('name'), str) for target in targets)):
                    raise ValueError('recovery record identity/type')
                seen.add(case_id.upper())
                by_case = case_id.upper() == term
                matched_targets = ([target for target in targets if kind is None or target['kind'].upper() == kind]
                                   if by_case else [target for target in targets if _matches(target, term, kind)])
                if not (matched_targets or (by_case and kind is None)):
                    continue
                matches.append({
                    'record_kind': record_kind,
                    'case_id': case_id,
                    'match_basis': 'CASE_ID' if by_case else 'TYPED_TARGET',
                    'matched_targets': targets if by_case and kind is None else matched_targets,
                    'record': {'path': _CASE_OBSERVATION_RECOVERY_DIRECTORY + '/' + relative,
                               'line_1based': index + 1},
                    'readme_ja': _CASE_OBSERVATION_RECOVERY_DIRECTORY + '/README.ja.md',
                    'readme_en': _CASE_OBSERVATION_RECOVERY_DIRECTORY + '/README.md',
                    'marker_recovery_readme_ja': _CASE_OBSERVATION_RECOVERY_DIRECTORY + '/marker-recovery/README.ja.md',
                    'marker_recovery_readme_en': _CASE_OBSERVATION_RECOVERY_DIRECTORY + '/marker-recovery/README.en.md',
                    'manifest': _CASE_OBSERVATION_RECOVERY_DIRECTORY + '/manifest.json',
                    'scope': 'LOCATION_ONLY_NO_OBSERVATION_PAYLOAD',
                })
        return matches, {'state': 'AVAILABLE', 'manifest_sha256': _CASE_OBSERVATION_RECOVERY_MANIFEST_SHA256,
                         'record_counts': {'base': 486, 'supplement': 38, 'current_correction': 2}}
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, UnicodeError, json.JSONDecodeError):
        return [], {'state': 'INCONSISTENT'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('term', help='Exact typed name or case identifier (case insensitive)')
    parser.add_argument('--kind', help='Optional typed kind filter for typed index and evidence rows')
    parser.add_argument('--printdata-index', help='Explicit saved PRINTDATA index for staging')
    parser.add_argument('--observation-dir', help='Explicit saved observation directory for staging')
    parser.add_argument('--case-projection-dir', help='Explicit case projection directory for staging')
    parser.add_argument('--partial', action='store_true', help='Continue other searches if C196 or supplemental evidence is inconsistent; exit 3 for partial results')
    args = parser.parse_args()
    scoped_helper_path = Path(__file__).with_name('scoped_observations_query.py')
    try:
        scoped_spec = importlib.util.spec_from_file_location('_scoped_observations_query', scoped_helper_path)
        scoped_helper = importlib.util.module_from_spec(scoped_spec)
        scoped_spec.loader.exec_module(scoped_helper)
        if not callable(getattr(scoped_helper, 'lookup', None)):
            raise ValueError('helper lookup is unavailable')
    except (OSError, ImportError, AttributeError, ValueError, SyntaxError):
        parser.exit(2, 'query: required tools/scoped_observations_query.py is missing or cannot be loaded\n')
    legacy226_helper_path = Path(__file__).with_name('legacy226_locator_query.py')
    try:
        legacy226_spec = importlib.util.spec_from_file_location('_legacy226_locator_query', legacy226_helper_path)
        legacy226_helper = importlib.util.module_from_spec(legacy226_spec)
        legacy226_spec.loader.exec_module(legacy226_helper)
        if not callable(getattr(legacy226_helper, 'lookup', None)) or not callable(getattr(legacy226_helper, 'lookup_name', None)):
            raise ValueError('legacy226 lookup is unavailable')
    except (OSError, ImportError, AttributeError, ValueError, SyntaxError):
        parser.exit(2, 'query: required tools/legacy226_locator_query.py is missing or cannot be loaded\n')
    if not _stdout_supports_utf8():
        parser.exit(2, 'query: stdout must support UTF-8 or be a text-only StringIO\n')
    if _has_private_path(args.term) or (args.kind and _has_private_path(args.kind)):
        parser.exit(2, 'query term or kind is invalid\n')
    try:
        supplement_index = ROOT / 'results/evidence-supplement-20261117.json'
        supplement_marker = ROOT / 'results/evidence-supplement-20261117.marker'
        if (supplement_index.exists() or supplement_index.is_symlink()
                or supplement_marker.exists() or supplement_marker.is_symlink()):
            # The helper is shared; validate before any existing collection can import it.
            _normal_verified_tool()
        saved, saved_availability = saved_observations(args.term, ROOT, args.printdata_index, args.observation_dir, args.kind, allow_partial=args.partial)
    except BundleIntegrityError as exc:
        parser.exit(2, str(exc) + '\n')
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'saved observation source is unavailable or inconsistent\n')
    try:
        case_projection, case_projection_availability = case_register_projection(
            args.term, ROOT, args.case_projection_dir, args.kind)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'case projection source is unavailable or inconsistent\n')
    recovery_doc_links, recovery_doc_availability = case_observation_recovery_links(args.term, ROOT, args.kind)
    scoped_observations, scoped_observations_availability = scoped_helper.lookup(
        args.term, ROOT, args.kind, case_projection_override=args.case_projection_dir)
    try:
        native_static, native_static_availability = native_source_static(args.term, ROOT, args.kind)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'native source static index is unavailable or inconsistent\n')
    try:
        operator_static, operator_static_availability = native_source_operator30(args.term, ROOT, args.kind)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'operator source static index is unavailable or inconsistent\n')
    try:
        sha_supplement, sha_supplement_availability = native_source_sha_supplement(args.term, ROOT, args.kind)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'native source SHA supplement is unavailable or inconsistent\n')
    try:
        anchor82, anchor82_availability = native_source_anchor82(args.term, ROOT, args.kind)
    except BundleIntegrityError as exc:
        parser.exit(2, str(exc) + '\n')
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'native source anchor82 index is unavailable or inconsistent\n')
    base_by_target = {(item['row']['target']['kind'], item['row']['target']['name']): item['record']
                      for item in native_static}
    for item in operator_static:
        target = item['row']['target']
        item['base_static_record'] = base_by_target.get((target['kind'], target['name']))
    for item in sha_supplement:
        target = item['target']
        item['base_static_record'] = base_by_target.get((target['kind'], target['name']))
    for item in anchor82:
        target = item['row']['target']
        item['base_static_record'] = base_by_target.get((target['kind'], target['name']))
    restoration, restoration_availability = parent_restoration_40(args.term, ROOT, args.kind)
    discovery, discovery_availability = additional_evidence_discovery(args.term, ROOT, args.kind)
    data = json.loads((ROOT / 'results/survey.json').read_text(encoding='utf-8'))
    term = args.term.upper()
    target_term = term
    kind = args.kind.upper() if args.kind else None
    if ':' in target_term:
        typed_kind, target_term = target_term.split(':', 1)
        if kind and kind != typed_kind:
            parser.exit(2, 'conflicting typed kind\n')
        kind = typed_kind
    targets = [r for r in data['targets'] if _matches(r, target_term, kind)]
    cases = [r for key in ('main_scenarios', 'grammar_cases', 'supplemental_modes')
             for r in data[key] if r['case_id'].upper() == term]
    linked = []
    ids = {case for target in targets for case in target['case_ids']}
    if ids:
        linked = [r for r in data['main_scenarios'] if r['case_id'] in ids]
    representative = json.loads((ROOT / 'differences/representative-20261116/catalog.json').read_text(encoding='utf-8'))
    evidence = [r for r in representative['cases'] if r['id'].upper() == term]
    selected = json.loads((ROOT / 'results/evidence-index.json').read_text(encoding='utf-8'))
    selected_links = [r for r in selected['entries']
                      if (_matches(r['target'], target_term, kind) or
                          ((kind is None or r['target']['kind'].upper() == kind) and
                           term in {r['case_id'].upper(), r.get('neutral_case_id', '').upper(),
                                    *(value.upper() for value in r['historical_case_ids'])}))]
    try:
        supplement_links, supplement_availability = _supplemental_evidence(
            term, target_term, kind, ROOT, allow_partial=args.partial)
    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError, json.JSONDecodeError):
        parser.exit(2, 'supplemental evidence is unavailable or inconsistent\n')
    selected_links.extend(supplement_links)
    native_oracle_rows, native_oracle_availability = _native_oracle_result(
        term, target_term, kind, ROOT)
    extra = json.loads((ROOT / 'results/extra-evidence-index.json').read_text(encoding='utf-8'))
    extra_links = [r for r in extra['entries']
                   if term == r['case_id'].upper() or term in {v.upper() for v in r['parent_ids']}]
    static = json.loads((ROOT / 'evidence/api-gap75-static-20261117/records/targets.json').read_text(encoding='utf-8'))
    static_rows = [r for r in static['targets']
                   if (_matches(r['target'], target_term, kind) or
                       ((kind is None or r['target']['kind'].upper() == kind) and
                        term in {v['case_id'].upper() for v in r['case_roles']}))]
    trace_root = ROOT / 'evidence/694-target-trace-20261117'
    trace = json.loads((trace_root / 'projection.json').read_text(encoding='utf-8'))
    trace_targets = [r for r in trace['targets'] if _matches(r['typed_key'], target_term, kind)]
    trace_cases = [r for r in trace['case_evidence']
                   if (_matches(r['typed_key'], target_term, kind) or
                       ((kind is None or r['typed_key']['kind'].upper() == kind) and
                        term in {r['registered_case_id'].upper(), (r.get('neutral_case_id') or '').upper(),
                                 *(value.upper() for value in r['historical_case_ids'])}))]
    legacy = json.loads((ROOT / 'evidence/legacy-acceptance-269-20261117/layer.json').read_text(encoding='utf-8'))
    legacy_rows = [r for r in legacy['targets'] if _matches(r['typed_key'], target_term, kind)]
    with (trace_root / trace['requirements']['path']).open(encoding='utf-8') as stream:
        requirements = [r for r in map(json.loads, stream)
                        if (_matches(r['typed_key'], target_term, kind) or
                            ((kind is None or r['typed_key']['kind'].upper() == kind) and
                             r['requirement_id'].upper() == term))]
    legacy226_rows = []
    legacy226_availability = {'state': 'NOT_APPLICABLE'}
    if kind or target_term:
        try:
            rows = ([legacy226_helper.lookup(ROOT, kind.lower(), target_term)] if kind
                    else legacy226_helper.lookup_name(ROOT, target_term))
        except ValueError as exc:
            if 'missing or ambiguous' not in str(exc):
                parser.exit(2, 'legacy226 source locator is unavailable or inconsistent\n')
            rows = []
        legacy226_rows = [row for row in rows if row]
        if legacy226_rows:
            legacy226_availability = {'state': 'AVAILABLE', 'records': len(legacy226_rows)}
        else:
            legacy226_availability = {'state': 'NOT_IN_LEGACY226'}
    reasons = []
    if saved_availability.get('normal_observations_196') == 'INCONSISTENT':
        reasons.append('NORMAL_OBSERVATIONS_196_INCONSISTENT')
    if (supplement_availability['index'] == 'INCONSISTENT' or
            'INCONSISTENT' in supplement_availability['collections'].values() or
            'INCONSISTENT' in supplement_availability['readable_documents'].values()):
        reasons.append('SUPPLEMENTAL_EVIDENCE_INCONSISTENT')
    is_partial = args.partial and bool(reasons)
    status = ({'state': 'PARTIAL', 'reason': reasons[0] if len(reasons) == 1 else reasons}
              if is_partial else {'state': 'NO_C196_INCONSISTENCY_DETECTED'})
    print(json.dumps({'query': args.term, **({'search_status': status} if args.partial else {}), 'targets': targets, 'cases': cases,
                      'linked_main_scenarios': linked,
                      'representative_evidence': evidence,
                      'additional_evidence_discovery': discovery,
                      'additional_evidence_discovery_availability': discovery_availability,
                      'parent_restoration_40': restoration,
                      'parent_restoration_40_availability': restoration_availability,
                      'selected_evidence_links': selected_links,
                      'native_oracle_observations': native_oracle_rows,
                      'native_oracle_availability': native_oracle_availability,
                      'supplemental_evidence_availability': supplement_availability,
                      'extra_evidence_links': extra_links,
                      'static_api_evidence': static_rows,
                      'native_source_static': native_static,
                      'native_source_static_availability': native_static_availability,
                      'native_source_operator30': operator_static,
                      'native_source_operator30_availability': operator_static_availability,
                      'native_source_sha_supplement': sha_supplement,
                      'native_source_sha_supplement_availability': sha_supplement_availability,
                      'native_source_anchor82': anchor82,
                      'native_source_anchor82_availability': anchor82_availability,
                      'static_api_evidence_readme': 'evidence/api-gap75-static-20261117/README.md' if static_rows else None,
                      'trace_targets': trace_targets,
                      'verification_requirements': requirements,
                      'trace_case_evidence': trace_cases,
                      'historical_acceptance_references': legacy_rows,
                      'historical_acceptance_readme': 'evidence/legacy-acceptance-269-20261117/README.md' if legacy_rows else None,
                      'case_register_projection': case_projection,
                      'case_register_projection_availability': case_projection_availability,
                      'case_observation_recovery_links': recovery_doc_links,
                      'case_observation_recovery_availability': recovery_doc_availability,
                      'scoped_observations': scoped_observations,
                      'scoped_observations_availability': scoped_observations_availability,
                      'legacy226_source_locator': legacy226_rows,
                      'legacy226_source_locator_availability': legacy226_availability,
                      'saved_observations': saved,
                      'saved_observation_availability': saved_availability,
                      'saved_observation_kind_filter': {'kind': args.kind or (args.term.split(':', 1)[0] if ':' in args.term else None), 'scope': 'SAVED_OBSERVATIONS_ONLY'},
                      'scope': 'Index plus separately selected evidence; original survey records and provenance may be unavailable.'},
                     ensure_ascii=False, indent=2))
    return 3 if is_partial else (0 if targets or cases or evidence or selected_links or extra_links or static_rows or trace_targets or trace_cases or requirements or legacy_rows or saved or case_projection or native_static or operator_static or sha_supplement or anchor82 or restoration or discovery or recovery_doc_links or native_oracle_rows or scoped_observations or legacy226_rows else 1)

if __name__ == '__main__':
    raise SystemExit(main())
