"""Exercise the 28-case saved-evidence query without changing the candidate."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = Path('evidence/target-priority-28-20261117')
COLLECTION = 'target_priority_28_saved'
UNCALLED = {
    'LIST_TRYGOTOLIST_EMPTY_UNCALLED_20261115',
    'LIST_TRYGOTOLIST_MISSING_CLOSE_UNCALLED_20261115',
    'LIST_TRYJUMPLIST_EMPTY_UNCALLED_20261115',
    'LIST_TRYJUMPLIST_MISSING_CLOSE_UNCALLED_20261115',
}

spec = importlib.util.spec_from_file_location('candidate_query_target28', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)


class TargetPriority28QueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='query28_test_')
        cls.root = Path(cls.temp.name)
        cls.bundle = cls.root / BUNDLE
        cls.bundle.parent.mkdir(parents=True)
        shutil.copytree(ROOT / BUNDLE, cls.bundle)
        cls.index = cls.bundle / 'index.json'
        cls.original_index = cls.index.read_bytes()
        cls.doc = json.loads(cls.original_index)
        cls.cases = cls.doc['cases']
        cls.batches = {batch['batch_id']: batch for batch in cls.doc['batches']}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def tearDown(self):
        self.index.write_bytes(self.original_index)

    def lookup(self, term, kind=None):
        rows, availability = query.saved_observations(term, self.root, kind=kind)
        self.assertEqual(availability[COLLECTION], 'AVAILABLE')
        return [row for row in rows if row['collection'] == COLLECTION]

    def test_all_case_ids_keep_modes_and_source_identity(self):
        self.assertEqual(len(self.cases), 28)
        self.assertEqual(len({case['case_id'] for case in self.cases}), 28)
        for case in self.cases:
            with self.subTest(case=case['case_id']):
                row, = self.lookup(case['case_id'])
                self.assertEqual(row['match_basis'], 'CASE_ID')
                self.assertEqual(row['recorded_verdict'], case['record']['scenario_verdict'])
                self.assertEqual(row['matched_parent_roles'], case['parent_and_case_roles'])
                self.assertEqual(row['saved_modes'], ['native-01', 'native-02', 'public-01'])
                self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')
                self.assertEqual(row['target_return'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')
                self.assertEqual(row['post_fatal_state'], 'NOT_INFERRED_SEE_CASE_RECORD')
                self.assertEqual(set(row['native_natural_exit_by_mode'].values()),
                                 {'not_established_from_receipt'})
                expected_identity = ('NOT_DECLARED_BINDING_FROM_CASE_EVIDENCE_AND_SOURCE_PATH'
                                     if case['group'] == 'list-owner-completion'
                                     else 'DECLARED_IN_SOURCE_RECEIPT')
                self.assertEqual(row['source_receipt_case_mode'], expected_identity)
                for mode, refs in row['mode_references'].items():
                    self.assertEqual(refs['raw']['record']['location'], 'CANDIDATE_RELATIVE')
                    self.assertTrue((self.root / refs['raw']['record']['path']).is_file())
                    self.assertTrue((self.root / refs['derived_receipt']['record']['path']).is_file())
                    self.assertEqual(len(refs['inputs']), 2, mode)
                    for ref in refs['inputs'].values():
                        self.assertTrue((self.root / ref['record']['path']).is_file())

    def test_each_typed_role_returns_the_recorded_cases(self):
        targets = json.loads((self.bundle / 'target-priority.json').read_text(encoding='utf-8'))['targets']
        keys = {(target['kind'], target['name']) for target in targets}
        self.assertEqual(len(keys), 19)
        recorded = {(role['kind'], role['name']) for case in self.cases
                    for role in case['parent_and_case_roles']}
        self.assertEqual(keys, recorded)
        for kind, name in keys:
            with self.subTest(kind=kind, name=name):
                expected = {case['case_id'] for case in self.cases
                            if {'kind': kind, 'name': name} in case['parent_and_case_roles']}
                rows = self.lookup(kind + ':' + name)
                self.assertEqual({row['case_id'] for row in rows}, expected)
                for row in rows:
                    self.assertEqual(row['match_basis'], 'TYPED_ROLE')
                    self.assertEqual(row['matched_parent_roles'], [{'kind': kind, 'name': name}])
                self.assertEqual({row['case_id'] for row in self.lookup(name, kind=kind)}, expected)

    def test_uncalled_cases_and_parent_summary_remain_distinct(self):
        found = {case['case_id'] for case in self.cases
                 if case['group'] == 'list-owner-completion' and 'UNCALLED' in case['case_id']}
        self.assertEqual(found, UNCALLED)
        for case in self.cases:
            if case['group'] != 'list-owner-completion':
                continue
            row, = self.lookup(case['case_id'])
            self.assertEqual(row['parent_readback_scope'],
                             'NOT_INCLUDED_SHARED_GROUP_SUMMARY_NOT_CASE_OBSERVATION')
            if case['case_id'] in UNCALLED:
                self.assertEqual(row['recorded_case_scope'], 'UNCALLED_AS_RECORDED')
                observation = case['record']['observation_points_and_comparison']
                self.assertIn('This case is uncalled', observation)
                self.assertIn('not attribute', observation)
            else:
                self.assertEqual(row['recorded_case_scope'], 'SEE_CASE_RECORD')

    def test_invalid_case_mode_and_legacy_receipt_binding_are_rejected(self):
        case = next(case for case in self.cases if case['group'] == 'list-owner-completion')
        for defect in ('case', 'mode', 'legacy_basis'):
            doc = json.loads(self.original_index)
            batch = next(batch for batch in doc['batches'] if batch['batch_id'] == case['batch_id'])
            if defect == 'case':
                batch['case_ids'] = ['WRONG']
            elif defect == 'mode':
                batch['modes'][0]['mode'] = 'public-01'
            else:
                batch['modes'][0]['identity_basis'] = 'case_evidence_source_path_and_receipt_case_mode'
            self.index.write_text(json.dumps(doc), encoding='utf-8')
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                self.lookup(case['case_id'])

    def test_missing_input_or_receipt_is_rejected(self):
        case = self.cases[0]
        mode = self.batches[case['batch_id']]['modes'][0]
        for asset in (mode['inputs'][0], mode['receipt']):
            path = self.bundle / asset['path']
            data = path.read_bytes()
            try:
                path.unlink()
                with self.subTest(asset=asset['path']), self.assertRaises(ValueError):
                    self.lookup(case['case_id'])
            finally:
                path.write_bytes(data)

    def test_duplicate_case_and_uninstalled_bundle(self):
        doc = json.loads(self.original_index)
        doc['cases'].append(doc['cases'][0])
        self.index.write_text(json.dumps(doc), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.lookup(self.cases[0]['case_id'])
        with tempfile.TemporaryDirectory(prefix='query28_empty_') as empty:
            rows, state = query.saved_observations('CALL', Path(empty))
            self.assertEqual(rows, [])
            self.assertEqual(state[COLLECTION], 'NOT_INSTALLED')

    def test_registered_only_role_is_not_promoted(self):
        doc = json.loads(self.original_index)
        doc['cases'][0]['registered_roles'].append({'kind': 'method_as_command', 'name': 'FAKE_ROLE'})
        self.index.write_text(json.dumps(doc), encoding='utf-8')
        row, = self.lookup('method_as_command:FAKE_ROLE')
        self.assertEqual(row['matched_parent_roles'], [])
        self.assertEqual(row['matched_registered_only_roles'],
                         [{'kind': 'method_as_command', 'name': 'FAKE_ROLE'}])
        self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')

    def test_candidate_cli_case_and_typed_role(self):
        for term in ('LIST_TRYGOTOLIST_EMPTY_UNCALLED_20261115',
                     'structural_syntax:TRYGOTOLIST'):
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/query.py'), term],
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            rows = [row for row in data['saved_observations'] if row['collection'] == COLLECTION]
            self.assertTrue(rows)
            self.assertEqual(data['saved_observation_availability'][COLLECTION], 'AVAILABLE')
            self.assertTrue(all(row['target_reach'] == 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH'
                                for row in rows))


if __name__ == '__main__':
    unittest.main()
