#!/usr/bin/env python3
"""Search published cases and supplements by exact case ID or exact target."""
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
g=p.add_mutually_exclusive_group(required=True)
g.add_argument('--case',help='exact registered case ID')
g.add_argument('--target',help='exact target name or exact kind:name (case-insensitive)')
a=p.parse_args()
base=[json.loads(x) for x in (ROOT/'observations.jsonl').read_text(encoding='utf-8').splitlines() if x]
child=ROOT/'marker-recovery'
recovery=[json.loads(x) for x in (child/'risk-observations.jsonl').read_text(encoding='utf-8').splitlines() if x]
corrections=[json.loads(x) for x in (child/'current-candidate-corrections.jsonl').read_text(encoding='utf-8').splitlines() if x]
def target_matches(target, query):
    q=query.strip().casefold()
    typed=f"{target['kind']}:{target['name']}".casefold()
    if ':' in q:
        return q == typed
    return q == target['name'].casefold()
def matches(row):
    if a.case is not None:
        return row.get('case_id') == a.case
    return any(target_matches(t,a.target) for t in row.get('targets',[]))
byid={r['case_id']:r for r in corrections}
baseids={r['case_id'] for r in base}
missing=set(byid)-baseids
if missing:
    raise SystemExit('correction lacks base case anchor: '+','.join(sorted(missing)))
out=[]
for row in base:
    if matches(row):
        correction=byid.get(row['case_id'])
        if correction:
            out.append({'record_kind':'current_candidate_correction','priority':'current','case_id':row['case_id'],'record':correction})
        out.append({'record_kind':'base_observation','priority':'historical_base_snapshot' if correction else 'base','case_id':row['case_id'],'record':row})
for row in recovery:
    if matches(row):
        out.append({'record_kind':'field_recovery_supplement','priority':'supplement_only_not_new_case','case_id':row['case_id'],'record':row})
for row in out:
    print(json.dumps(row,ensure_ascii=False,sort_keys=True))
