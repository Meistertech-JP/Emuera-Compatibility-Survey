#!/usr/bin/env python3
"""Verify this candidate offline; no original survey files or network needed."""
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

def fail(message): raise ValueError(message)
def unique(values, label):
    if len(values) != len(set(values)): fail('duplicate ' + label)
def counts(rows, field): return dict(collections.Counter(x[field] for x in rows))
def check(value, message):
    if not value: fail(message)
def exact(row, fields, label): check(set(row) == set(fields.split()), 'unexpected fields: ' + label)
def strict_json(path):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d: fail('duplicate JSON key')
            d[k] = v
        return d
    def bad_constant(x): fail('non-finite JSON number: ' + x)
    return json.loads(path.read_bytes(), object_pairs_hook=pairs, parse_constant=bad_constant)

def main():
    lock = strict_json(ROOT / 'results/manifest.json')
    check(set(lock) == {'schema', 'files'} and lock['schema'] == 'survey-neutral-manifest-v1', 'manifest schema')
    check(set(lock['files']) == {'results/survey.json', 'differences/catalog.json'}, 'manifest file set')
    for path, expected in lock['files'].items():
        p = ROOT / path
        check(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == expected['sha256'] and p.stat().st_size == expected['bytes'], 'file hash/size: ' + path)
    d = strict_json(ROOT / 'results/survey.json'); diff = strict_json(ROOT / 'differences/catalog.json')
    exact(d, 'schema scope evidence_availability targets main_scenarios supplemental_items supplemental_modes grammar_cases', 'survey root')
    exact(diff, 'schema evidence_availability main_scenarios grammar_cases supplemental_modes', 'differences root')
    check(d['schema'] == 'survey-neutral-results-v1' and diff['schema'] == 'survey-neutral-differences-v1', 'schema')
    check(d['scope'] == {'native_grammar_census_complete': True, 'whole_grammar_complete': False, 'full_compatibility': False, 'mode_counts_are_process_launches': False}, 'finite scope')
    resolution = {'native_observation': 'unresolved_not_in_candidate', 'pyemuera_observation': 'unresolved_not_in_candidate', 'evidence_links': 'unresolved_not_in_candidate', 'reproducibility': 'not_established'}
    check(d['evidence_availability'] == resolution and diff['evidence_availability'] == resolution, 'evidence availability')
    targets = d['targets']; cases = d['main_scenarios']; supp = d['supplemental_items']; modes = d['supplemental_modes']; grammar = d['grammar_cases']
    for x in targets: exact(x, 'kind name status necessary_comparison_complete comparison_outcome case_ids', 'target')
    for x in cases:
        exact(x, 'case_id targets scenario_verdict', 'main scenario')
        for t in x['targets']: exact(t, 'kind name', 'typed key')
    for x in supp: exact(x, 'id work_type status comparison_outcome', 'supplemental item')
    for x in modes: exact(x, 'case_id work_item_ids phase scenario_verdict', 'supplemental mode')
    for x in grammar: exact(x, 'case_id grammar_family_ids phase case_mode_count finite_observations_accepted verdict', 'grammar case')
    unique([(x['kind'], x['name']) for x in targets], 'typed key')
    for rows, field in [(cases, 'case_id'), (supp, 'id'), (modes, 'case_id'), (grammar, 'case_id')]: unique([x[field] for x in rows], field)
    check(len(targets) == 694 and all(x['status'] == 'necessary_comparison_complete' and x['necessary_comparison_complete'] is True for x in targets), 'target completion')
    check(counts(targets, 'kind') == {'command_or_syntax':266,'expression_function':163,'method_as_command':154,'operator':29,'assignment_syntax':15,'structural_syntax':49,'declaration':11,'declaration_modifier':7}, 'typed population')
    check(counts(targets, 'comparison_outcome') == {'matched_in_finite_scope':201,'documented_difference':294,'different_scoped':199}, 'target outcomes')
    check(len(cases) == 2898 and counts(cases, 'scenario_verdict') == {'matched_scoped':1711,'different_scoped':1071,'unverified':99,'blocked':17}, 'main scenario outcomes')
    check(len(supp) == 16 and all(x['status'] == 'necessary_comparison_complete' for x in supp), 'supplemental items')
    check(counts(supp, 'comparison_outcome') == {'different_scoped':10,'matched_in_finite_scope':3,None:2,'documented_difference':1}, 'supplemental outcomes')
    check(len(modes) == 83 and counts(modes, 'scenario_verdict') == {'different_scoped':48,'matched_scoped':35}, 'supplemental modes')
    check(len(grammar) == 114 and sum(x['case_mode_count'] for x in grammar) == 342 and counts(grammar, 'verdict') == {'different_scoped':65,'matched_scoped':36,None:13}, 'grammar cases')
    check(all(x['finite_observations_accepted'] is True for x in grammar), 'grammar finite acceptance')
    caseids = {x['case_id'] for x in cases}; workids = {x['id'] for x in supp}; keys = {(x['kind'], x['name']) for x in targets}
    check(all(cid in caseids for x in targets for cid in x['case_ids']), 'target case link')
    check(all(x['work_item_ids'] and all(i in workids for i in x['work_item_ids']) for x in modes), 'supplemental item link')
    external = [(x['case_id'], t['kind'], t['name']) for x in cases for t in x['targets'] if (t['kind'],t['name']) not in keys]
    check(external == [('RENAMEEDGE01','parser_preprocessing','_Rename.csv duplicate key last wins')], 'non-main target exceptions')
    m = {x['case_id']:x for x in cases}; g = {x['case_id']:x for x in grammar}; s = {x['case_id']:x for x in modes}
    for x in diff['main_scenarios']:
        exact(x, 'case_id targets verdict', 'main difference')
        check(x['case_id'] in m and x['targets'] == m[x['case_id']]['targets'] and x['verdict'] == m[x['case_id']]['scenario_verdict'] == 'different_scoped', 'main difference link')
    for x in diff['grammar_cases']:
        exact(x, 'case_id grammar_family_ids verdict', 'grammar difference')
        check(x['case_id'] in g and x['grammar_family_ids'] == g[x['case_id']]['grammar_family_ids'] and x['verdict'] == g[x['case_id']]['verdict'] == 'different_scoped', 'grammar difference link')
    for x in diff['supplemental_modes']:
        exact(x, 'case_id work_item_ids verdict', 'supplemental difference')
        check(x['case_id'] in s and x['work_item_ids'] == s[x['case_id']]['work_item_ids'] and x['verdict'] == s[x['case_id']]['scenario_verdict'] == 'different_scoped', 'supplemental difference link')
    for label, arr, original, verdict in [('main_scenarios',diff['main_scenarios'],cases,'scenario_verdict'),('grammar_cases',diff['grammar_cases'],grammar,'verdict'),('supplemental_modes',diff['supplemental_modes'],modes,'scenario_verdict')]:
        unique([x['case_id'] for x in arr], label + ' difference')
        check({x['case_id'] for x in arr} == {x['case_id'] for x in original if x[verdict] == 'different_scoped'}, label + ' difference coverage')
    # Only controlled field names and compact identifiers are published. This is a
    # structural screen, not a blanket privacy/security audit of other artifacts.
    forbidden = re.compile(r'(?i)([a-z]:[\\/]|\\\\|https?://|/users/|/home/|password|secret|api[_-]?key|bearer\s|subagent|agent|ユーザー|依頼者|ご指示|本セッション)')
    def walk(x):
        if isinstance(x, dict):
            for k,v in x.items():
                check(not forbidden.search(k), 'unsafe key'); walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
        elif isinstance(x,str):
            check(len(x) <= 200 and not forbidden.search(x) and '\\' not in x and '\n' not in x, 'unsafe text value')
    walk(d); walk(diff)
    print(json.dumps({'status':'PASS','typed_targets':694,'main_scenarios':2898,'supplemental_items':16,'supplemental_modes':83,'grammar_cases':114,'grammar_modes':342,'difference_main':len(diff['main_scenarios']),'difference_grammar':len(diff['grammar_cases']),'difference_supplemental_modes':len(diff['supplemental_modes']),'non_main_target_edges':len(external),'evidence_reproducibility':'not_established'}, indent=2))

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr); sys.exit(1)
