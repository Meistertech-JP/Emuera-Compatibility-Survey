"""Verify the portable legacy locator and saved case observation links offline."""
from collections import Counter
from functools import cache
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from file_set_manifest import safe_relative
from legacy226_locator_query import LOCATOR, _pairs

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = 'evidence/saved-case-observations/observations.json'
RESTORED = 'evidence/legacy226-restored/index.json'
LAYOUTS = 'evidence/legacy226-restored/fixture-layouts.json'
CLASSES = {
    'PUBLIC_INCLUDED': 'original_bytes',
    'PUBLIC_DERIVED': 'selected_observations',
    'EXTERNAL_FETCHABLE': 'external_bytes',
    'PRIVATE_RETAINED': 'index_only',
    'MISSING_OR_UNVERIFIED': 'none',
    'REDUNDANT_REFERENCE': 'redundant',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(blob):
    return sha256(blob).hexdigest()


@cache
def data_bytes(path):
    file = ROOT / safe_relative(path)
    require(file.resolve().is_relative_to(ROOT), 'Reference escapes the package')
    return file.read_bytes()


def read_json(path):
    return json.loads(data_bytes(path), object_pairs_hook=_pairs)


@cache
def read_artifact(path, members):
    result = data_bytes(path)
    for name in members:
        with ZipFile(BytesIO(result)) as archive:
            require(archive.namelist().count(safe_relative(name)) == 1, 'Missing or ambiguous ZIP member')
            result = archive.read(name)
    return result


def pin_set(record):
    obs = record.get('observation')
    comparisons = obs.get('case_bound_comparison', []) if isinstance(obs, dict) else []
    return {r['sha256'] for r in [*record['excerpts'], *comparisons] if 'sha256' in r}


def restored_records():
    document = read_json(RESTORED)
    require(document['schema']=='legacy226-restored-evidence.v1','Restored evidence schema')
    records = document['files']
    require(len(records)==document['source_files']==978,'Restored source file count')
    require(len({r['id'] for r in records})==len(records),'Duplicate restored file ID')
    mapping = {}
    for i,row in enumerate(records):
        require(row['decision'] in {'exact','derived','withhold'},'Invalid reviewed decision')
        require(bool(row['reason_ja'].strip()) and bool(row['inspection']) and bool(row['rights_basis']),
                'Missing individual inspection or reason')
        view = row['readable_view']
        require(len(data_bytes(view['path']))==view['size'] and digest(data_bytes(view['path']))==view['sha256'],
                'Readable evidence view pin mismatch')
        if row['decision']=='withhold':
            require('public_file' not in row,'Withheld source has a published payload')
        else:
            file = row['public_file']
            raw = data_bytes(file['path'])
            require(len(raw)==file['size'] and digest(raw)==file['sha256'],'Restored artifact pin mismatch')
            if row['decision']=='exact':
                require(file['sha256']==row['original_sha256'] and file['size']==row['original_size'],
                        'Exact restored source differs from original')
            else:
                require(file['sha256']!=row['original_sha256'] and bool(row['transforms']),
                        'Missing derivative transformation record')
        for ref in row['references']:
            require(ref['id'] not in mapping,'Duplicate reviewed reference')
            mapping[ref['id']] = (i,row,ref)
    require(len(mapping)==document['references']==2020,'Individual reference coverage')
    require(Counter(row['decision'] for row in records)==document['decisions'],'Individual decision totals')
    return mapping


def fixture_layouts():
    doc=read_json(LAYOUTS)
    require(doc['schema']=='restored-fixture-layouts.v1','Fixture layout schema')
    rows=doc['layouts']
    require(len(rows)==172 and len({r['source_file_id'] for r in rows})==doc['source_inputs']==152,
            'Fixture layout population')
    require(len({(r['source_file_id'],r['layout_index']) for r in rows})==len(rows),'Duplicate fixture layout')
    for entry in doc['supplements']:
        view=entry['readable_view'];raw=data_bytes(view['path'])
        require(len(raw)==view['size'] and digest(raw)==view['sha256'],'Supporting input view pin mismatch')
    for row in rows:
        destinations=set()
        for file in row['files']:
            place=safe_relative(file['restore_path']).casefold()
            require(place not in destinations,'Duplicate fixture destination')
            destinations.add(place)
            raw=data_bytes(file['path'])
            require(len(raw)==file['size'] and digest(raw)==file['sha256'],'Fixture dependency pin mismatch')
            basis=file.get('configuration_basis',{})
            if basis.get('public_runner'):
                source=basis['public_runner'];raw=data_bytes(source['path'])
                require(len(raw)==source['size'] and digest(raw)==source['sha256'],
                        'Configuration runner provenance pin mismatch')
    return len(rows)


def verify():
    locator = read_json(LOCATOR)
    observations = read_json(OBSERVATIONS)
    survey = read_json('results/survey.json')
    main_cases = {r['case_id'] for r in survey['main_scenarios']}
    cases = {(r['kind'], r['name']): set(r['case_ids']) for r in survey['targets']}
    require(locator['schema'] in {'legacy226-source-locator.v2','legacy226-source-locator.v3'}, 'Legacy locator schema')
    reviewed = restored_records() if locator['schema']=='legacy226-source-locator.v3' else {}
    layout_count = fixture_layouts() if reviewed else 0
    index_sha = digest(data_bytes(RESTORED)) if reviewed else None
    require(len(locator['records']) == locator['rows'] == 226, 'Legacy target count')
    obs = observations['records']
    obs_ids = {r['id'] for r in obs}
    require(len(obs_ids) == len(obs) and obs_ids <= main_cases, 'Saved observations use duplicate or unknown cases')
    require(all(r['observation'] or r['excerpts'] for r in obs), 'Saved observation has no displayed result')
    obs_sha = digest(data_bytes(OBSERVATIONS))
    counts = Counter(dict.fromkeys(CLASSES, 0))
    typed_keys = set()
    ref_ids = set()
    alias_refs = {}
    for row in locator['records']:
        typed = row['kind'], row['name']
        require(typed in cases and typed not in typed_keys, 'Missing or duplicate typed target')
        typed_keys.add(typed)
        for ref in row['references']:
            ref_id = ref['id']
            require(ref_id not in ref_ids, 'Duplicate reference ID')
            ref_ids.add(ref_id)
            classification = ref['classification']
            if ref.get('original_byte_alias'):
                alias_refs[ref_id]=(typed,ref)
            if ref_id in reviewed:
                i,entry,original_ref = reviewed[ref_id]
                require(tuple(original_ref['target'])==typed and original_ref['role']==ref['role'],
                        'Reviewed source target or role changed')
                require(entry['original_sha256']==ref['original_sha256'] and entry['original_size']==ref['original_size'],
                        'Reviewed source identity changed')
                require(ref['review_file_id']==entry['id'] and ref['selection_reason_ja']==entry['reason_ja']
                        and ref['readable_view']==entry['readable_view']['path'],'Individual decision link mismatch')
                expected = {'exact':'PUBLIC_INCLUDED','derived':'PUBLIC_DERIVED','withhold':'PRIVATE_RETAINED'}[entry['decision']]
                require(classification==expected,'Individual decision classification mismatch')
                if entry['decision']!='withhold':
                    require(all(ref[k]==v for k,v in entry['public_file'].items()),'Reviewed payload link mismatch')
                    require(ref['reviewed_artifact']=={'index':RESTORED,'index_sha256':index_sha,
                            'pointer':f'/files/{i}','source_file_id':entry['id']},'Invalid reviewed artifact pointer')
            require(ref['public_access'] == CLASSES[classification], 'Invalid availability')
            require(ref['candidate_exists'] == (classification == 'PUBLIC_INCLUDED'), 'Invalid byte-availability flag')
            counts[classification] += 1
            if classification == 'PUBLIC_INCLUDED':
                artifact = read_artifact(ref['path'], tuple(ref.get('archive_members', ())))
                require(len(artifact) == ref['size'] == ref['original_size']
                        and digest(artifact) == ref['sha256'] == ref['original_sha256'], 'Original artifact pin mismatch')
            elif classification == 'PUBLIC_DERIVED':
                if ref_id in reviewed:
                    continue
                require(ref['path'] == OBSERVATIONS and ref['sha256'] == obs_sha, 'Derived evidence pin mismatch')
                require(bool(ref['derived']), 'Missing derived observation')
                for link in ref['derived']:
                    number = link['pointer'].removeprefix('/records/')
                    require(number.isdecimal() and int(number) < len(obs), 'Invalid derived pointer')
                    result = obs[int(number)]
                    require(link['case_id'] == result['id'] and result['id'] in cases[typed], 'Wrong observed case')
                    require(ref['original_sha256'] in pin_set(result), 'Derived source pin absent')
            elif classification in {'PRIVATE_RETAINED', 'MISSING_OR_UNVERIFIED'}:
                require('path' not in ref and 'derived' not in ref, 'Unavailable original has a published path')
            else:
                raise ValueError('External fetch or redundancy requires an explicit verifier')
    require(len(ref_ids) == locator['reference_count'] == 2476, 'Legacy reference count')
    if reviewed:
        require(set(reviewed)<=ref_ids and locator['individually_reviewed_references']==len(reviewed)
                and locator['restored_evidence_index']==RESTORED,'Reviewed reference set mismatch')
        restored=read_json(RESTORED)
        aliases=restored.get('original_byte_aliases',{})
        require(set(alias_refs)==set(aliases),'Original-byte alias set mismatch')
        by_id={r['id']:r for r in restored['files']}
        for ref_id,(typed,ref) in alias_refs.items():
            source=by_id[aliases[ref_id]]
            require(source['decision']=='exact' and ref['original_byte_alias']==source['id']
                    and all(ref[k]==v for k,v in source['public_file'].items()),'Invalid original-byte alias')
            prior=ref['retained_selected_observations']
            require(prior['path']==OBSERVATIONS and prior['sha256']==obs_sha,'Retained selected observation pin mismatch')
            for link in prior['derived']:
                prefix='/records/'
                number=link['pointer'].removeprefix(prefix)
                require(number.isdecimal() and int(number)<len(obs),'Invalid retained observation pointer')
                result=obs[int(number)]
                require(link['case_id']==result['id'] and result['id'] in cases[typed]
                        and ref['original_sha256'] in pin_set(result),'Retained observation role mismatch')
    require(counts == locator['reference_class_counts'], 'Legacy classification counts')
    return {'references': dict(counts), 'saved_case_observations': len(obs),
            'individually_reviewed_references':len(reviewed),'recorded_fixture_layouts':layout_count}


if __name__ == '__main__':
    try:
        print(json.dumps(verify(), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        raise SystemExit(f'FAIL: {type(exc).__name__}: {exc}') from None
