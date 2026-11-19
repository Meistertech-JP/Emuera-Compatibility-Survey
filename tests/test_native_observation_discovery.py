"""Exercise direct discovery of saved Native observations."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'evidence' / 'nine-saved-observations-20261117'
SPEC = importlib.util.spec_from_file_location('observation_query', ROOT / 'tools' / 'query.py')
query = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(query)

class NativeObservationDiscoveryTests(unittest.TestCase):
    def test_limit_lookup_exposes_saved_values_and_scope(self):
        rows, state = query.additional_evidence_discovery('method_as_command:LIMIT', ROOT)
        selected = [row for row in rows if row['collection'] == 'nine_saved_observations']
        self.assertEqual(state['groups']['nine_saved_observations'], 'AVAILABLE')
        self.assertEqual(len(selected), 4)
        normal, = [row for row in selected if row['case_id'] == 'METHOD_BOUNDARY_LIMIT_NORMAL_20261115']
        vectors = normal['details']['observation']['vectors_and_results']
        self.assertEqual({(v['x'], v['min'], v['max'], v['native_result'], v['pyemuera_result'])
                          for v in vectors if v['native_result'] != v['pyemuera_result']},
                         {(8, 8, 4, 4, 8), (9, 8, 4, 4, 8)})
        self.assertTrue(any('fixtures' in limit and 'not included' in limit for limit in normal['scope_limits']))
        for mode in normal['details']['modes']:
            for material in mode['materials']:
                self.assertTrue((BUNDLE / material['raw_path']).is_file())
                self.assertTrue((BUNDLE / material['readable_path']).is_file())

    def test_case_lookup_keeps_fault_and_typed_form_distinct(self):
        term = 'METHOD_BOUNDARY_INRANGE_INRANGE_FAULT_1_20261115'
        rows, _ = query.additional_evidence_discovery(term, ROOT, kind='method_as_command')
        row, = [item for item in rows if item['collection'] == 'nine_saved_observations']
        self.assertEqual(row['details']['observation']['condition']['faulting_helper_slot'], 1)
        self.assertFalse(row['details']['observation']['modes'][0]['after_or_done_observed'])
        other, _ = query.additional_evidence_discovery(term, ROOT, kind='expression_function')
        self.assertFalse(any(item['collection'] == 'nine_saved_observations' for item in other))
        records = json.loads((BUNDLE / 'data' / 'records.json').read_text(encoding='utf-8'))['cases']
        with (BUNDLE / 'data' / 'cases.jsonl').open(encoding='utf-8') as stream:
            original = [json.loads(line) for line in stream]
        self.assertEqual(records, original)

    def test_changed_records_are_not_treated_as_the_reviewed_snapshot(self):
        index = json.loads((ROOT / query._DISCOVERY_INDEX).read_text(encoding='utf-8'))
        group = index['groups']['nine_saved_observations']
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in (query._DISCOVERY_INDEX, group['records']['path'],
                             *(item['path'] for item in group['readmes'])):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, target)
            rows, state = query.additional_evidence_discovery('LIMIT', root)
            self.assertEqual(state['groups']['nine_saved_observations'], 'AVAILABLE')
            self.assertTrue(any(row['collection'] == 'nine_saved_observations' for row in rows))
            data = root / group['records']['path']
            data.write_bytes(data.read_bytes() + b' ')
            rows, state = query.additional_evidence_discovery('LIMIT', root)
            self.assertEqual(state['groups']['nine_saved_observations'], 'SNAPSHOT_MISMATCH')
            self.assertFalse(any(row['collection'] == 'nine_saved_observations' for row in rows))

if __name__ == '__main__':
    unittest.main()
