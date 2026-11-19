"""Check search of the 24 saved background-operation cases."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = Path('evidence/console-background-24-20261117')
COLLECTION = 'console_background_24_saved'

spec = importlib.util.spec_from_file_location('candidate_query_console24', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)


class ConsoleBackgroundQueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='query_console24_')
        cls.root = Path(cls.temp.name)
        cls.bundle = cls.root / BUNDLE
        cls.bundle.parent.mkdir(parents=True)
        shutil.copytree(ROOT / BUNDLE, cls.bundle)
        cls.path = cls.bundle / 'records.json'
        cls.original = cls.path.read_bytes()
        cls.cases = json.loads(cls.original)['cases']

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def tearDown(self):
        self.path.write_bytes(self.original)

    def lookup(self, term, kind=None):
        rows, availability = query.saved_observations(term, self.root, kind=kind)
        self.assertEqual(availability['console_background_24'], 'AVAILABLE')
        return [row for row in rows if row['collection'] == COLLECTION]

    def test_all_cases_preserve_mode_references_and_derived_receipts(self):
        self.assertEqual(len(self.cases), 24)
        self.assertEqual(len({case['case_id'] for case in self.cases}), 24)
        self.assertEqual(sum(len(case['modes']) for case in self.cases), 72)
        for i, case in enumerate(self.cases):
            with self.subTest(case=case['case_id']):
                row, = self.lookup(case['case_id'])
                self.assertEqual(row['match_basis'], 'CASE_ID')
                self.assertEqual(row['record']['pointer'], '/cases/' + str(i))
                self.assertEqual(row['recorded_verdict'], case['recorded_verdict'])
                self.assertEqual(row['matched_parent_roles'], case['roles'])
                self.assertEqual(row['collection_case_mode_references'], 72)
                self.assertEqual(row['saved_modes'], ['native-01', 'native-02', 'public-01'])
                self.assertEqual(row['native_natural_exit'], 'NOT_OBSERVED_CLEANUP_SEPARATE')
                self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_CASE_ROLE_OR_RECEIPT')
                self.assertEqual(row['public_target_reach'], case['public_target_reach'])
                self.assertEqual(row['public_error_recorded'], case['public_error_recorded'])
                self.assertIn('GUI pixels', row['unobserved'])
                self.assertIn('click/mouse events', row['unobserved'])
                self.assertIn('entire background state', row['unobserved'])
                self.assertEqual(row['actual_button_selection'], 'NOT_OBSERVED_SEE_BUNDLE_README')
                for mode in case['modes']:
                    name = mode['mode']
                    refs = row['mode_references'][name]
                    self.assertEqual(refs['source_receipt'],
                                     'NOT_INCLUDED_SELECTED_FIELDS_IN_DERIVED_RECEIPT')
                    self.assertEqual(refs['case_mode_identity'],
                                     'DERIVED_FROM_CASE_PLAN_COMPARISON_AND_SOURCE_PATH')
                    self.assertEqual(refs['input_identity_basis'], mode['input_identity_basis'])
                    for label in ('fixture', 'config', 'raw', 'derived_receipt'):
                        self.assertTrue((self.root / refs[label]['record']['path']).is_file())
                    self.assertEqual('stderr' in refs, name == 'public-01')
                    receipt = json.loads((self.root / refs['derived_receipt']['record']['path']).read_bytes())
                    self.assertEqual(receipt['case_id'], case['case_id'])
                    self.assertEqual(receipt['mode'], name)
                    self.assertEqual(receipt['source_receipt_sha256'], mode['receipt_sha256'])
                    if name.startswith('native-'):
                        self.assertEqual(receipt['input_before_after'], 'NOT_CAPTURED_BY_THIS_PROBE')
                        self.assertEqual(receipt['native_natural_exit'], 'NOT_OBSERVED_CLEANUP_SEPARATE')
                    else:
                        self.assertEqual(receipt['inputs_before'], receipt['inputs_after'])

    def test_each_typed_target_returns_recorded_cases(self):
        keys = {(role['kind'], role['name']) for case in self.cases for role in case['roles']}
        self.assertEqual(len(keys), 16)
        for kind, name in keys:
            with self.subTest(kind=kind, name=name):
                expected = {case['case_id'] for case in self.cases
                            if {'kind': kind, 'name': name} in case['roles']}
                rows = self.lookup(kind + ':' + name)
                self.assertEqual({row['case_id'] for row in rows}, expected)
                for row in rows:
                    self.assertEqual(row['match_basis'], 'TYPED_ROLE')
                    self.assertEqual(row['matched_parent_roles'], [{'kind': kind, 'name': name}])
                self.assertEqual({row['case_id'] for row in self.lookup(name, kind=kind)}, expected)

    def test_two_lifecycle_cases_remain_unverified(self):
        cases = [case for case in self.cases if case['recorded_verdict'] == 'unverified']
        self.assertEqual({case['case_id'] for case in cases},
                         {'UIQUERY236_lifecycle-expr', 'UIQUERY236_lifecycle-method'})
        for case in cases:
            row, = self.lookup(case['case_id'])
            self.assertEqual(row['case_kind'], 'setup')
            self.assertEqual(row['recorded_verdict'], 'unverified')
            self.assertEqual(row['public_target_reach'], 'not_established_setup_or_load_stopped')

    def test_invalid_mode_receipt_sha_and_setup_scope_are_rejected(self):
        first_id = self.cases[0]['case_id']
        for defect in ('mode', 'receipt', 'sha', 'setup'):
            doc = json.loads(self.original)
            case = doc['cases'][0]
            if defect == 'mode':
                case['modes'][0]['mode'] = 'public-01'
            elif defect == 'receipt':
                case['modes'][0]['source_receipt_included'] = True
            elif defect == 'sha':
                case['modes'][0]['evidence']['raw']['sha256'] = '0' * 64
            else:
                case = next(item for item in doc['cases'] if item['recorded_verdict'] == 'unverified')
                case['public_target_reach'] = 'reached'
            self.path.write_text(json.dumps(doc), encoding='utf-8')
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                self.lookup(case['case_id'])
        self.assertEqual(self.cases[0]['case_id'], first_id)

    def test_missing_fixture_and_derived_receipt_are_rejected(self):
        case = self.cases[0]
        mode = case['modes'][0]
        for label in ('fixture', 'derived_receipt'):
            asset = self.bundle / mode['evidence'][label]['path']
            original = asset.read_bytes()
            try:
                asset.unlink()
                with self.subTest(asset=label), self.assertRaises(ValueError):
                    self.lookup(case['case_id'])
            finally:
                asset.write_bytes(original)

    def test_duplicate_case_and_uninstalled_bundle(self):
        doc = json.loads(self.original)
        doc['cases'][1]['case_id'] = doc['cases'][0]['case_id']
        self.path.write_text(json.dumps(doc), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.lookup(doc['cases'][0]['case_id'])
        with tempfile.TemporaryDirectory(prefix='query_console_empty_') as empty:
            rows, state = query.saved_observations('CBGSETG', Path(empty))
            self.assertEqual(rows, [])
            self.assertEqual(state['console_background_24'], 'NOT_INSTALLED')

    def test_candidate_cli_case_and_typed_target(self):
        for term in ('UIQUERY236_lifecycle-expr', 'expression_function:CBGSETG'):
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/query.py'), term],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            doc = json.loads(result.stdout)
            rows = [row for row in doc['saved_observations'] if row['collection'] == COLLECTION]
            self.assertTrue(rows)
            self.assertEqual(doc['saved_observation_availability']['console_background_24'], 'AVAILABLE')


if __name__ == '__main__':
    unittest.main()
