"""Check search of the saved PRINT K/D shared batch and its scope."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = Path('evidence/print-kd-shared-82-20261117')
SELECTED = 'print_kd_shared_82_saved'
EXCLUDED = 'print_kd_shared_82_scope'

spec = importlib.util.spec_from_file_location('candidate_query_print_kd', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)


class PrintKDSharedQueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='query_print_kd_')
        cls.root = Path(cls.temp.name)
        cls.bundle = cls.root / BUNDLE
        cls.bundle.parent.mkdir(parents=True)
        shutil.copytree(ROOT / BUNDLE, cls.bundle)
        cls.index = cls.bundle / 'index.json'
        cls.scope = cls.bundle / 'scope.json'
        cls.original_index = cls.index.read_bytes()
        cls.original_scope = cls.scope.read_bytes()
        cls.doc = json.loads(cls.original_index)
        cls.scope_doc = json.loads(cls.original_scope)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def tearDown(self):
        self.index.write_bytes(self.original_index)
        self.scope.write_bytes(self.original_scope)

    def lookup(self, term, kind=None):
        rows, state = query.saved_observations(term, self.root, kind=kind)
        self.assertEqual(state['print_kd_shared_82'], 'AVAILABLE')
        return rows

    def test_all_case_ids_keep_one_shared_three_mode_batch(self):
        cases = self.doc['cases']
        self.assertEqual(len(cases), 82)
        self.assertEqual(len({case['case_id'] for case in cases}), 82)
        for i, case in enumerate(cases):
            with self.subTest(case=case['case_id']):
                row, = [item for item in self.lookup(case['case_id'])
                        if item['collection'] == SELECTED]
                self.assertEqual(row['match_basis'], 'CASE_ID')
                self.assertEqual(row['recorded_verdict'], case['record']['scenario_verdict'])
                self.assertEqual(row['record']['pointer'], '/cases/' + str(i))
                self.assertEqual(row['case_relationship'], case['relationship']['kind'])
                self.assertEqual(row['shared_batch_case_count'], 82)
                self.assertEqual(row['saved_modes'], ['native-01', 'native-02', 'py'])
                self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_CASE_ROLE_OR_SHARED_BATCH')
                self.assertEqual(row['native_natural_exit'], 'NOT_OBSERVED_CLEANUP_IS_SEPARATE')
                self.assertEqual(set(row['shared_output_references']),
                                 {'native-01_history', 'native-02_history', 'py_history', 'py_stdout'})
                for ref in row['shared_output_references'].values():
                    self.assertEqual(ref['record']['location'], 'CANDIDATE_RELATIVE')
                    self.assertTrue((self.root / ref['record']['path']).is_file())

    def test_typed_roles_find_the_recorded_cases(self):
        keys = {(role['kind'], role['name']) for case in self.doc['cases'] for role in case['roles']}
        self.assertEqual(len(keys), 28)
        for kind, name in keys:
            with self.subTest(kind=kind, name=name):
                expected = {case['case_id'] for case in self.doc['cases']
                            if {'kind': kind, 'name': name} in case['roles']}
                rows = [row for row in self.lookup(kind + ':' + name) if row['collection'] == SELECTED]
                self.assertEqual({row['case_id'] for row in rows}, expected)
                for row in rows:
                    self.assertEqual(row['match_basis'], 'TYPED_ROLE')
                    self.assertEqual(row['matched_parent_roles'], [{'kind': kind, 'name': name}])
                self.assertEqual({row['case_id'] for row in self.lookup(name, kind=kind)
                                  if row['collection'] == SELECTED}, expected)

    def test_seven_excluded_conditions_are_scope_not_case_verdicts(self):
        omitted = self.scope_doc['unselected_conditions']
        self.assertEqual({item['condition_id'] for item in omitted},
                         {*(f'C212_{n}' for n in range(60, 66)), 'C212_86'})
        for item in omitted:
            with self.subTest(case=item['case_id']):
                rows = self.lookup(item['case_id'])
                self.assertFalse([row for row in rows if row['collection'] == SELECTED])
                row, = [row for row in rows if row['collection'] == EXCLUDED]
                self.assertEqual(row['selection_status'],
                                 'OUTSIDE_THIS_82_CASE_SELECTION_NOT_A_CLAIM_OF_NONOBSERVATION')
                self.assertIsNone(row['recorded_verdict'])
                self.assertEqual(row['scope_target'], item['target'])
                self.assertTrue(row['record']['pointer'].startswith('/unselected_conditions/'))
                typed = item['target']['kind'] + ':' + item['target']['name']
                self.assertIn(item['case_id'], [r['case_id'] for r in self.lookup(typed)
                                                if r['collection'] == EXCLUDED])

    def test_ten_empty_single_history_and_stdout_are_distinct(self):
        empty = [case for case in self.doc['cases'] if case['relationship'].get('comparison', {}).get('category')
                 == 'empty_single_serialized_line_lifecycle']
        self.assertEqual({case['relationship']['condition_id'] for case in empty},
                         {f'C212_{n}' for n in range(75, 85)})
        for case in empty:
            with self.subTest(case=case['case_id']):
                row, = [item for item in self.lookup(case['case_id']) if item['collection'] == SELECTED]
                self.assertEqual(row['public_history_stdout_scope'],
                                 'EMPTY_SINGLE_HISTORY_AND_STDOUT_BLANK_LINE_BYTES_DIFFER')
                self.assertIsNotNone(row['byte_references_record'])
                refs = case['relationship']['byte_references']
                self.assertIsNone(refs['public-stdout']['comparison_raw_block_span'])
                history_ref, stdout_ref = refs['public-history'], refs['public-stdout']
                def marker(ref):
                    span = ref['marker_span']
                    data = (self.bundle / ref['asset_path']).read_bytes()
                    return data[span['start_byte_inclusive']:span['end_byte_exclusive']]
                history = marker(history_ref).decode('utf-16-le')
                stdout = marker(stdout_ref).decode('utf-8')
                self.assertIn('\r\n \r\n', history)
                self.assertIn('\r\n\r\n', stdout)
                self.assertNotIn('\r\n \r\n', stdout)
                self.assertNotEqual(row['shared_output_references']['py_history']['sha256'],
                                    row['shared_output_references']['py_stdout']['sha256'])

    def test_aggregate_does_not_infer_setter_failure_or_single_comparison(self):
        case = next(c for c in self.doc['cases']
                    if c['relationship']['kind'] == 'aggregate_interaction_not_setter_identity')
        row, = [item for item in self.lookup(case['case_id']) if item['collection'] == SELECTED]
        self.assertEqual(row['forcekana_setter_failure'], 'NOT_INFERRED_FROM_AGGREGATE_INTERACTION')
        self.assertIsNone(row['condition_id'])
        self.assertIsNone(row['comparison_record'])
        self.assertEqual(row['public_history_stdout_scope'],
                         'DISTINCT_OUTPUTS_NO_SINGLE_COMPARISON_BLOCK_FOR_AGGREGATE')

    def test_missing_scope_or_history_and_bad_batch_are_rejected(self):
        case_id = self.doc['cases'][0]['case_id']
        try:
            self.scope.unlink()
            with self.assertRaises(ValueError):
                self.lookup(case_id)
        finally:
            self.scope.write_bytes(self.original_scope)
        asset = self.bundle / self.doc['batches'][0]['modes'][0]['outputs']['history']['path']
        original = asset.read_bytes()
        try:
            asset.unlink()
            with self.assertRaises(ValueError):
                self.lookup(case_id)
        finally:
            asset.write_bytes(original)
        doc = json.loads(self.original_index)
        doc['batches'][0]['case_ids'][0] = 'WRONG'
        self.index.write_text(json.dumps(doc), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.lookup(case_id)

    def test_duplicate_case_and_uninstalled_bundle(self):
        doc = json.loads(self.original_index)
        doc['cases'][1]['case_id'] = doc['cases'][0]['case_id']
        self.index.write_text(json.dumps(doc), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.lookup(doc['cases'][0]['case_id'])
        with tempfile.TemporaryDirectory(prefix='query_print_kd_empty_') as empty:
            rows, state = query.saved_observations('PRINTVK', Path(empty))
            self.assertEqual(rows, [])
            self.assertEqual(state['print_kd_shared_82'], 'NOT_INSTALLED')

    def test_candidate_cli_selected_excluded_and_typed(self):
        for term, expected in (('PRINTKD212_C212_75', SELECTED),
                               ('PRINTKD212_C212_60', EXCLUDED),
                               ('command_or_syntax:PRINTVK', SELECTED)):
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/query.py'), term],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            doc = json.loads(result.stdout)
            self.assertTrue([row for row in doc['saved_observations'] if row['collection'] == expected])
            self.assertEqual(doc['saved_observation_availability']['print_kd_shared_82'], 'AVAILABLE')


if __name__ == '__main__':
    unittest.main()
