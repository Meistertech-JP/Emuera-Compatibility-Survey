#!/usr/bin/env python3
"""Project frozen survey JSON to a neutral index; never modify source files.

Requires a local source tree and its private freeze ledger. For independent
verification of an already built candidate use verify.py, which needs neither.
"""
import argparse
import hashlib
import json
from pathlib import Path


def digest(b):
    return hashlib.sha256(b).hexdigest()


def encode(v):
    return (json.dumps(v, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True, type=Path)
    ap.add_argument('--freeze', required=True, type=Path, help='freeze-files.jsonl')
    ap.add_argument('--freeze-summary', required=True, type=Path)
    ap.add_argument('--candidate', required=True, type=Path)
    ap.add_argument('--private-provenance', required=True, type=Path)
    args = ap.parse_args()
    source, candidate = args.source.resolve(), args.candidate.resolve()
    private = args.private_provenance.resolve()
    tool_repository = Path(__file__).resolve().parent.parent
    if private == candidate or private.is_relative_to(candidate) or private == tool_repository or private.is_relative_to(tool_repository):
        ap.error('private provenance must be outside the candidate and tool repository')
    if candidate == source or candidate.is_relative_to(source) or source.is_relative_to(candidate):
        ap.error('candidate and frozen source must be separate, non-nested directories')
    summary = json.loads(args.freeze_summary.read_bytes())
    freeze_bytes = args.freeze.read_bytes()
    if not summary.get('complete') or digest(freeze_bytes) != summary['inventory_sha256']:
        raise ValueError('freeze inventory is incomplete or SHA mismatch')
    pins = {}
    for line in freeze_bytes.splitlines():
        entry = json.loads(line)
        if entry['path'] in pins:
            raise ValueError('duplicate frozen path')
        pins[entry['path']] = entry
    sources = {}
    def read(relative):
        rel = Path(relative)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('unsafe source path')
        rel = rel.as_posix()
        if rel not in pins:
            raise ValueError('source absent from freeze: ' + rel)
        path = (source / rel).resolve()
        if not path.is_relative_to(source):
            raise ValueError('source outside root')
        b = path.read_bytes()
        if digest(b) != pins[rel]['sha256'] or len(b) != pins[rel]['size']:
            raise ValueError('source changed since freeze: ' + rel)
        sources[rel] = {'sha256': digest(b), 'size': len(b)}
        return json.loads(b)
    target = read('TARGET_COMPARISON_REVIEW_CURRENT.json')
    ledger = read('MASTER_LEDGER.json')
    cases = read('CASE_SCENARIO_REGISTER.json')
    supp = read('SUPPLEMENTAL_SURVEY_QUEUE_CURRENT.json')
    supval = read('SUPPLEMENTAL_EVIDENCE_VALIDATION_CURRENT.json')
    grammar = read('NATIVE_GRAMMAR_FOLLOWUP_INDEX_CURRENT.json')
    diffpath = 'evidence/final-finite-survey-readback-20261116/NEXT_VERSION_DIFFERENCE_INDEX.json'
    diff = read(diffpath)
    targets = target['rows']; records = cases['records']; items = supp['work_items']; grows = grammar['cases']
    key = lambda x: (x['kind'], x['name'])
    master = ledger.get('rows', ledger.get('targets'))
    if len(targets) != 694 or {key(x) for x in targets} != {key(x) for x in master} or len(master) != 694:
        raise ValueError('typed target population mismatch')
    if len(records) != 2898 or len({x['case_id'] for x in records}) != 2898:
        raise ValueError('case population mismatch')
    trows = [{'kind': x['kind'], 'name': x['name'], 'status': x['status'],
              'necessary_comparison_complete': x['necessary_comparison_complete'],
              'comparison_outcome': x['comparison_outcome'], 'case_ids': x['case_ids']}
             for x in targets]
    crows = [{'case_id': x['case_id'], 'targets': [{'kind': z['kind'], 'name': z['name']} for z in x['targets']],
              'scenario_verdict': x['scenario_verdict']} for x in records]
    srows = [{'id': x['id'], 'work_type': x['work_type'], 'status': x['status'],
              'comparison_outcome': x.get('comparison_outcome')} for x in items]
    grows_out = [{'case_id': x['case_id'], 'grammar_family_ids': x['grammar_family_ids'],
                  'phase': x['phase'], 'case_mode_count': x['case_mode_count'],
                  'finite_observations_accepted': x['finite_observations_accepted'],
                  'verdict': x.get('verdict')} for x in grows]
    modes, mode_sources = [], []
    for reg in supval['registers']:
        rel = reg['path']; data = read(rel)
        if sources[rel]['sha256'] != reg['sha256'] or len(data['records']) != reg['case_modes']:
            raise ValueError('supplemental register pin/count mismatch')
        for i, x in enumerate(data['records']):
            ids = x.get('supplemental_work_item_ids') or [x['work_item_id']]
            modes.append({'case_id': x['case_id'], 'work_item_ids': ids,
                          'phase': x.get('phase'), 'scenario_verdict': x['scenario_verdict']})
            mode_sources.append({'source': rel, 'pointer': '/records/' + str(i)})
    if len(items) != 16 or len(grows) != 114 or len(modes) != 83:
        raise ValueError('supplemental or grammar population mismatch')
    main_diff = diff['main_difference_scenarios']; grammar_diff = diff['grammar_declared_difference_cases']
    if len(main_diff) != 1071 or len(grammar_diff) != 65:
        raise ValueError('difference index population mismatch')
    for x in main_diff:
        idx = int(x['register_pointer'].removeprefix('/records/'))
        if records[idx]['case_id'] != x['case_id'] or records[idx]['scenario_verdict'] != 'different_scoped' or records[idx]['targets'] != x['targets']:
            raise ValueError('main difference pointer mismatch')
    for x in grammar_diff:
        idx = int(x['index_pointer'].removeprefix('/cases/'))
        if grows[idx]['case_id'] != x['case_id'] or grows[idx].get('verdict') != 'different_scoped' or grows[idx]['grammar_family_ids'] != x['families']:
            raise ValueError('grammar difference pointer mismatch')
    if {x['case_id'] for x in main_diff} != {x['case_id'] for x in records if x['scenario_verdict'] == 'different_scoped'}:
        raise ValueError('main difference set mismatch')
    if {x['case_id'] for x in grammar_diff} != {x['case_id'] for x in grows if x.get('verdict') == 'different_scoped'}:
        raise ValueError('grammar difference set mismatch')
    resolution = {'native_observation': 'unresolved_not_in_candidate',
                  'pyemuera_observation': 'unresolved_not_in_candidate',
                  'evidence_links': 'unresolved_not_in_candidate',
                  'reproducibility': 'not_established'}
    results = {'schema': 'survey-neutral-results-v1',
               'scope': {'native_grammar_census_complete': grammar['native_grammar_census_complete'],
                         'whole_grammar_complete': grammar['whole_grammar_complete'],
                         'full_compatibility': grammar['full_compatibility'],
                         'mode_counts_are_process_launches': False},
               'evidence_availability': resolution,
               'targets': trows, 'main_scenarios': crows, 'supplemental_items': srows,
               'supplemental_modes': modes, 'grammar_cases': grows_out}
    differences = {'schema': 'survey-neutral-differences-v1', 'evidence_availability': resolution,
                   'main_scenarios': [{'case_id': x['case_id'], 'targets': x['targets'], 'verdict': 'different_scoped'} for x in main_diff],
                   'grammar_cases': [{'case_id': x['case_id'], 'grammar_family_ids': x['families'], 'verdict': 'different_scoped'} for x in grammar_diff],
                   'supplemental_modes': [{'case_id': x['case_id'], 'work_item_ids': x['work_item_ids'], 'verdict': x['scenario_verdict']} for x in modes if x['scenario_verdict'] == 'different_scoped']}
    outputs = {'results/survey.json': encode(results), 'differences/catalog.json': encode(differences)}
    # Per-record mapping remains private; absolute paths do not enter public data.
    mappings = []
    def maps(output, field, src, ptr, n):
        for i in range(n):
            mappings.append({'output': output, 'pointer': '/' + field + '/' + str(i),
                             'sources': [{'source': src, 'pointer': ptr + str(i)}]})
    maps('results/survey.json', 'targets', 'TARGET_COMPARISON_REVIEW_CURRENT.json', '/rows/', len(trows))
    maps('results/survey.json', 'main_scenarios', 'CASE_SCENARIO_REGISTER.json', '/records/', len(crows))
    maps('results/survey.json', 'supplemental_items', 'SUPPLEMENTAL_SURVEY_QUEUE_CURRENT.json', '/work_items/', len(srows))
    maps('results/survey.json', 'grammar_cases', 'NATIVE_GRAMMAR_FOLLOWUP_INDEX_CURRENT.json', '/cases/', len(grows_out))
    for i, ref in enumerate(mode_sources):
        mappings.append({'output': 'results/survey.json', 'pointer': '/supplemental_modes/' + str(i), 'sources': [ref]})
    for i, x in enumerate(main_diff):
        mappings.append({'output': 'differences/catalog.json', 'pointer': '/main_scenarios/' + str(i),
                         'sources': [{'source': diffpath, 'pointer': '/main_difference_scenarios/' + str(i)},
                                     {'source': 'CASE_SCENARIO_REGISTER.json', 'pointer': x['register_pointer']}]})
    for i, x in enumerate(grammar_diff):
        mappings.append({'output': 'differences/catalog.json', 'pointer': '/grammar_cases/' + str(i),
                         'sources': [{'source': diffpath, 'pointer': '/grammar_declared_difference_cases/' + str(i)},
                                     {'source': 'NATIVE_GRAMMAR_FOLLOWUP_INDEX_CURRENT.json', 'pointer': x['index_pointer']}]})
    i = 0
    for n, x in enumerate(modes):
        if x['scenario_verdict'] == 'different_scoped':
            mappings.append({'output': 'differences/catalog.json', 'pointer': '/supplemental_modes/' + str(i), 'sources': [mode_sources[n]]})
            i += 1
    provenance = {'schema': 'survey-private-provenance-v1', 'source_root': str(source),
                  'freeze_inventory_sha256': digest(freeze_bytes), 'sources': sources,
                  'outputs': {k: {'sha256': digest(v), 'size': len(v)} for k, v in outputs.items()},
                  'mappings': mappings}
    # Refuse overwriting pre-existing unrelated or changed output.
    for rel, b in outputs.items():
        dest = candidate / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and dest.read_bytes() != b:
            raise FileExistsError('output exists with different bytes: ' + str(dest))
    if private.exists() and private.read_bytes() != encode(provenance):
        raise FileExistsError('private provenance already exists with different bytes')
    for rel, b in outputs.items():
        dest = candidate / rel
        if not dest.exists(): dest.write_bytes(b)
    if not private.exists(): private.write_bytes(encode(provenance))
    print(json.dumps({'outputs': {k: digest(v) for k, v in outputs.items()}, 'source_files': len(sources), 'record_mappings': len(mappings)}, indent=2))

if __name__ == '__main__':
    main()
