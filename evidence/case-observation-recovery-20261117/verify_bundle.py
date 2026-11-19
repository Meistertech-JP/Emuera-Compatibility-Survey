#!/usr/bin/env python3
"""Always-on bundle-only structural and query checks."""
import json, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]

def query(target):
    result=subprocess.run([sys.executable,str(R/'query.py'),'--target',target],capture_output=True,text=True,encoding='utf-8')
    require(result.returncode==0,'query failed for '+target+': '+result.stderr)
    return [json.loads(line) for line in result.stdout.splitlines() if line]

def verify():
    base=load_jsonl(R/'observations.jsonl')
    child=R/'marker-recovery'
    recovery=load_jsonl(child/'risk-observations.jsonl')
    corrections=load_jsonl(child/'current-candidate-corrections.jsonl')
    base_ids={row.get('case_id') for row in base}
    recovery_ids={row.get('case_id') for row in recovery}
    correction_ids={row.get('case_id') for row in corrections}
    require(len(base)==486 and len(base_ids)==486,'base must contain 486 distinct cases')
    require(len(recovery)==38 and len(recovery_ids)==38,'supplement must contain 38 distinct rows')
    require(recovery_ids<=base_ids,'supplements must point to base case IDs')
    expected_correction_ids={'NUM_ASSIGN_STOPPED_STATE_CONTROL_20261116','NUM_ASSIGN_STOPPED_STATE_BADINDEX_20261116'}
    require(len(corrections)==2 and len(correction_ids)==2 and correction_ids==expected_correction_ids,'corrections must contain exactly the two distinct expected current case IDs')
    require(correction_ids<=base_ids,'two corrections must point to base case IDs')
    require(len(base_ids|recovery_ids|correction_ids)==486,'combined distinct case count changed')
    for row in recovery:
        require(row.get('selection_status') in {'selected_safe_fields','no_safe_leaf_selected'},'invalid selection status')
        if row['selection_status']=='no_safe_leaf_selected':
            require(row.get('projection') is None,'no-safe-leaf row must retain null projection')
    no_safe={'REND_GOTO_ZERO_NESTED_NORMAL_20261115','GOTO_MISSING_LOCAL_LABEL_20261115'}
    for row in base:
        if row.get('case_id') in no_safe:
            retained=row.get('recovered')
            require(isinstance(retained,list) and len(retained)==1,'retained finite observation missing')
            def has_work(value):
                if isinstance(value,dict):
                    return 'current_required_work_mapping' in value or any(has_work(v) for v in value.values())
                if isinstance(value,list):
                    return any(has_work(v) for v in value)
                return False
            require(not has_work(retained),'private work mapping appears in public observation')
    public_text='\n'.join(path.read_text(encoding='utf-8') for path in [R/'observations.jsonl',child/'risk-observations.jsonl',child/'current-candidate-corrections.jsonl',R/'README.ja.md',R/'README.md',child/'README.ja.md',child/'README.en.md'])
    for forbidden in ('current_required_work_mapping','new reached normal markers','historical receipts remain unknown','evidence actually executes this target'):
        require(forbidden not in public_text,'private mapping phrase leaked: '+forbidden)
    for cid in correction_ids:
        out=subprocess.run([sys.executable,str(R/'query.py'),'--case',cid],capture_output=True,text=True,encoding='utf-8')
        require(out.returncode==0,'case query failed: '+cid)
        rows=[json.loads(line) for line in out.stdout.splitlines() if line]
        require(len(rows)>=2 and rows[0].get('record_kind')=='current_candidate_correction' and rows[0].get('priority')=='current','current correction is not first: '+cid)
        require(any(row.get('priority')=='historical_base_snapshot' for row in rows),'historical base snapshot missing: '+cid)
    exact=query('command_or_syntax:GOTO')
    require(len(exact)==4 and {row['case_id'] for row in exact}==no_safe,'exact GOTO query mismatch')
    require(query('command_or_syntax:GOT')==[],'typed prefix must not match')
    require(query('GOT')==[],'bare-name prefix must not match')
    require(query('expression_function:GOTO')==[],'wrong typed kind must not match')
    similar=query('command_or_syntax:TRYGOTOLIST')
    require({row['case_id'] for row in similar}=={
        'LIST_TRYGOTOLIST_EMPTY_REACHED_20261115','LIST_TRYGOTOLIST_MISSING_CLOSE_REACHED_20261115',
        'LIST_TRYGOTOLIST_EMPTY_UNCALLED_20261115','LIST_TRYGOTOLIST_MISSING_CLOSE_UNCALLED_20261115'},'similar-name exact target mismatch')
    require(query('Command_Or_Syntax:goto')==exact,'case-insensitive exact typed query mismatch')
    print('bundle-only structural/query checks: PASS; cases=486; supplement_rows=38; corrections=2; distinct_cases=486')

def main():
    try:
        verify()
        return 0
    except Exception as exc:
        print('bundle-only structural/query checks: FAIL: '+str(exc),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
