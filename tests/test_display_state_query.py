"""Exercise the 21-case shared display-state query without starting engines."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = Path(os.environ.get('DISPLAY_STATE_QUERY_DATA_ROOT', str(ROOT))).resolve()
BUNDLE = DATA_ROOT / 'evidence/display-state-21-20261117'
SPEC = importlib.util.spec_from_file_location('display_state_staged_query', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(query)


class DisplayStateQueryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='display-state-query-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        if not self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()):
            raise ValueError('temporary test root is outside the temporary directory')
        self.bundle = self.root / 'evidence/display-state-21-20261117'
        self.bundle.parent.mkdir(parents=True)
        shutil.copytree(BUNDLE, self.bundle)

    def display(self, term, kind=None):
        rows, availability = query.saved_observations(term, self.root, kind=kind)
        return [r for r in rows if r['collection'].startswith('display_state_21_')], availability

    def test_all_21_case_and_typed_lookups_preserve_scope(self):
        cases = [json.loads(s) for s in (self.bundle / 'cases.jsonl').read_bytes().splitlines()]
        self.assertEqual(len(cases), 21)
        for c in cases:
            with self.subTest(case=c['case_id']):
                for term, basis in ((c['case_id'], 'CASE_ID'),
                                    (c['target']['kind'] + ':' + c['target']['name'], 'TYPED_ROLE')):
                    rows, availability = self.display(term)
                    row, = rows
                    self.assertEqual(availability['display_state_21'], 'AVAILABLE')
                    self.assertEqual(row['case_id'], c['case_id'])
                    self.assertEqual(row['match_basis'], basis)
                    self.assertEqual(row['matched_parent_roles'], [c['target']])
                    self.assertEqual(row['condition_markers'], c['condition_markers'])
                    self.assertEqual(row['recorded_verdict'], 'matched_scoped')
                    self.assertEqual(row['verdict_scope'], 'HISTORICAL_CASE_NOT_INDEPENDENT_EXPECTED_VALUE_VALIDATION')
                    self.assertEqual(row['saved_modes'], ['native-01', 'native-02', 'public-01'])
                    self.assertEqual(row['shared_batch_case_count'], 21)
                    self.assertEqual(row['expected_values'], '138_VALUES_NOT_INDEPENDENTLY_CHECKED')
                    self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_ROLE_MARKER_OR_SHARED_BATCH')
                    self.assertEqual(row['gui_rendering'], 'NOT_OBSERVED')
                    self.assertEqual(set(row['native_natural_exit_by_mode'].values()),
                                     {'NOT_OBSERVED_CLEANUP_RECORDED'})
                    case_file = self.root / row['record']['path']
                    binding_file = self.root / row['binding_record']['path']
                    self.assertEqual(json.loads(case_file.read_bytes().splitlines()[row['record']['line_1based'] - 1]), c)
                    binding_index = int(row['binding_record']['pointer'].rsplit('/', 1)[-1])
                    binding = json.loads(binding_file.read_bytes())['cases'][binding_index]
                    self.assertEqual(binding['case_id'], c['case_id'])
                    self.assertEqual(binding['target'], c['target'])
                    for mode in row['mode_references'].values():
                        for asset in mode.values():
                            p = self.root / asset['record']['path']
                            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), asset['sha256'])

    def test_unselected_strlen_is_scope_not_a_selected_result(self):
        for term in ('command_or_syntax:STRLEN', 'DISPLAYCOMMAND179_STRLEN', 'STRLEN'):
            row, = self.display(term)[0]
            self.assertEqual(row['collection'], 'display_state_21_scope')
            self.assertEqual(row['selection_status'], 'OUTSIDE_21_NOT_A_CLAIM_OF_NONOBSERVATION')
            self.assertEqual(row['condition_markers'], ['STATE130', 'STATE131'])
            self.assertEqual(row['matched_parent_roles'], [])
            self.assertIsNone(row['recorded_verdict'])
        self.assertEqual(self.display('expression_function:STRLEN')[0], [])
        self.assertEqual(self.display('DISPLAYCOMMAND179_STRLEN', kind='expression_function')[0], [])
        self.assertEqual(self.display('command_or_syntax:STRLENFORM')[0][0]['collection'], 'display_state_21_saved')

    def test_absent_and_incomplete_are_distinct(self):
        empty = self.root / 'empty'
        empty.mkdir()
        rows, availability = query.saved_observations('GETCOLOR', empty)
        self.assertEqual(rows, [])
        self.assertEqual(availability['display_state_21'], 'NOT_INSTALLED')
        (empty / 'evidence/display-state-21-20261117').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            query.saved_observations('GETCOLOR', empty)

    def test_untrusted_binding_and_case_swap_are_rejected(self):
        binding_path = self.bundle / 'bindings.json'
        original = binding_path.read_bytes()
        binding_path.write_bytes(original + b' ')
        with self.assertRaisesRegex(ValueError, 'bindings snapshot mismatch'):
            self.display('GETCOLOR')
        binding_path.write_bytes(original)
        path = self.bundle / 'cases.jsonl'
        cases = [json.loads(x) for x in path.read_bytes().splitlines()]
        c = next(c for c in cases if c['target']['name'] == 'STRLENU')
        c['target']['name'] = 'STRLEN'
        c['condition_markers'] = ['STATE130', 'STATE131']
        path.write_text(''.join(json.dumps(c, ensure_ascii=False, separators=(',', ':')) + '\n' for c in cases),
                        encoding='utf-8')
        with self.assertRaises(ValueError):
            self.display('STRLEN')

    def test_mode_corruption_or_false_native_exit_is_rejected(self):
        path = self.bundle / 'modes/native-01/raw.log'
        path.write_bytes(path.read_bytes() + b'X')
        with self.assertRaisesRegex(ValueError, 'mode file mismatch'):
            self.display('GETCOLOR')
        shutil.copyfile(BUNDLE / 'modes/native-01/raw.log', path)
        mp = self.bundle / 'modes.json'
        modes = json.loads(mp.read_bytes())
        modes['mode_records'][0]['recorded_process']['natural_exit_observed'] = True
        mp.write_text(json.dumps(modes), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'mode observation mismatch'):
            self.display('GETCOLOR')

    def test_excluded_condition_cannot_be_redefined(self):
        cp = self.bundle / 'conditions.json'
        cmp = self.bundle / 'comparison.json'
        conditions = json.loads(cp.read_bytes())
        conditions[130]['command'] = 'STRLENU'
        comparison = json.loads(cmp.read_bytes())
        comparison['conditions'] = conditions
        cp.write_text(json.dumps(conditions), encoding='utf-8')
        cmp.write_text(json.dumps(comparison), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'excluded condition mismatch'):
            self.display('STRLEN')

    def test_rehashed_single_mode_difference_is_rejected(self):
        path = self.bundle / 'modes/native-01/raw.log'
        path.write_bytes(path.read_bytes() + b'X')
        mp = self.bundle / 'modes.json'
        modes = json.loads(mp.read_bytes())
        modes['mode_records'][0]['raw_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        mp.write_text(json.dumps(modes), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'shared mode bytes mismatch'):
            self.display('GETCOLOR')

    def test_equal_false_values_do_not_become_new_validation(self):
        mp = self.bundle / 'modes.json'
        modes = json.loads(mp.read_bytes())
        for mode in modes['mode_records']:
            path = self.bundle / mode['raw']
            text = path.read_bytes().decode('utf-16')
            self.assertEqual(text.count('STATE0 GETCOLOR=12632256'), 1)
            path.write_bytes(text.replace('STATE0 GETCOLOR=12632256', 'STATE0 GETCOLOR=0').encode('utf-16'))
            mode['raw_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        mp.write_text(json.dumps(modes), encoding='utf-8')
        row, = self.display('expression_function:GETCOLOR')[0]
        self.assertEqual(row['recorded_verdict'], 'matched_scoped')
        self.assertEqual(row['verdict_scope'], 'HISTORICAL_CASE_NOT_INDEPENDENT_EXPECTED_VALUE_VALIDATION')
        self.assertEqual(row['expected_values'], '138_VALUES_NOT_INDEPENDENTLY_CHECKED')

    def test_conflicting_typed_filter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'conflicting typed kind'):
            query.saved_observations('expression_function:GETCOLOR', self.root, kind='command_or_syntax')

    def test_real_cli_wires_saved_results_without_promoting_scope(self):
        for term, collection in (('expression_function:GETCOLOR', 'display_state_21_saved'),
                                 ('DISPLAYCOMMAND179_STRLEN', 'display_state_21_scope')):
            with self.subTest(term=term), patch.object(query, 'ROOT', DATA_ROOT), \
                    patch.object(sys, 'argv', ['query.py', term]), contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(query.main(), 0)
                result = json.loads(out.getvalue())
                rows = [r for r in result['saved_observations'] if r['collection'].startswith('display_state_21_')]
                self.assertEqual([r['collection'] for r in rows], [collection])
                self.assertEqual(result['saved_observation_availability']['display_state_21'], 'AVAILABLE')
                self.assertEqual(rows[0]['expected_values'], '138_VALUES_NOT_INDEPENDENTLY_CHECKED')


if __name__ == '__main__':
    unittest.main()
