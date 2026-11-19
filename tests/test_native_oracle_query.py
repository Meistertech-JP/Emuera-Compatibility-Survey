"""Check native-oracle query results and availability without engine runs."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
RELATIVE_BUNDLE = Path('evidence/native-oracle-20261117')
BUNDLE = ROOT / RELATIVE_BUNDLE
SPEC = importlib.util.spec_from_file_location('native_oracle_query', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(query)


def lookup(term, root=ROOT, kind=None):
    return query._native_oracle_result(term.upper(), term.upper(), kind.upper() if kind else None, root)


def run_cli(term, *args, oracle_root=None):
    output = io.StringIO()
    original = query._native_oracle_result

    def isolated_oracle(query_term, target_term, kind, root):
        return original(query_term, target_term, kind, oracle_root if oracle_root is not None else root)

    with mock.patch.object(sys, 'argv', ['query.py', term, *args]), \
            mock.patch.object(query, 'ROOT', ROOT), \
            mock.patch.object(query, '_native_oracle_result', side_effect=isolated_oracle), \
            contextlib.redirect_stdout(output):
        code = query.main()
    return code, json.loads(output.getvalue())


class NativeOracleQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [json.loads(line) for line in (BUNDLE / 'results/native-oracle-selection.jsonl').read_bytes().splitlines()]

    def test_condition_and_values_for_all_selected_rows(self):
        self.assertEqual(len(self.rows), 113)
        for line, expected in enumerate(self.rows, 1):
            with self.subTest(case=expected['id'], line=line):
                found, status = lookup(expected['id'])
                self.assertEqual(status['state'], 'AVAILABLE')
                matches = [item for item in found if item['selection_index_line_1based'] == line]
                self.assertEqual(len(matches), 1)
                actual = matches[0]
                self.assertEqual(actual['selected_condition'], expected['condition'])
                self.assertEqual(actual['selected_observations'], expected['observations'])
                self.assertEqual(actual['source']['pointer'], expected['source']['pointer'])
                self.assertEqual(actual['selected_fields_scope'], 'SELECTION_INDEX_VALUES_SOURCE_SEMANTIC_EQUIVALENCE_NOT_VERIFIED')
        empty, _ = lookup('SUBSTRINGU_EXPR_HELPER_ERROR_1')
        item = next(x for x in empty if x['case_id'] == 'SUBSTRINGU_EXPR_HELPER_ERROR_1')
        self.assertIsNone(item['selected_condition'])
        self.assertEqual(item['selected_observations'], [])

    def test_corrected_conditions_and_opcont_values(self):
        for case, needles in [
            ('LINEBUF20261115_button_method', ('empty buffer', 'zero-argument LINEISEMPTY', 'nonempty PRINTBUTTON')),
            ('ARGBOUND245_dead_hole', ('0,,0', 'IF 0', 'unexecuted')),
            ('ARGBOUND245_dead_string', ('"0"', 'IF 0', 'unexecuted')),
        ]:
            with self.subTest(case=case):
                found, status = lookup(case)
                self.assertEqual(status['state'], 'AVAILABLE')
                item = next(x for x in found if x['case_id'] == case)
                for needle in needles:
                    self.assertIn(needle, item['selected_condition'])
        code, result = run_cli('OPCONT268_strcmp-ge')
        self.assertEqual(code, 0)
        self.assertEqual(result['native_oracle_availability']['state'], 'AVAILABLE')
        item = next(x for x in result['native_oracle_observations'] if x['case_id'] == 'OPCONT268_strcmp-ge')
        modes = {x['mode']: x for x in item['selected_observations']}
        self.assertIn('C=1', modes['native-01']['selected_values'])
        self.assertIn('C=1', modes['native-02']['selected_values'])
        self.assertIn('C=0', modes['public-01']['selected_values'])
        self.assertFalse(item['observation_scope']['raw_included'])
        self.assertFalse(item['observation_scope']['fixture_included'])
        self.assertFalse(item['observation_scope']['config_included'])
        self.assertTrue(item['observation_scope']['shared_runs'])
        self.assertEqual((item['observation_scope']['native_run_count'], item['observation_scope']['pyemuera_run_count']), (2, 1))

    def test_duplicate_ids_and_typed_target(self):
        for case, count in [('CASE001', 3), ('P38', 2)]:
            rows, status = lookup(case)
            exact = [item for item in rows if item['case_id'] == case]
            self.assertEqual(status['state'], 'AVAILABLE')
            self.assertEqual(len(exact), count)
            self.assertEqual(len({x['selection_index_line_1based'] for x in exact}), count)
        code, result = run_cli('assignment_syntax:*=')
        self.assertEqual(code, 0)
        self.assertTrue(any(x['case_id'] == 'OPCONT268_repeat-str-int-0' for x in result['native_oracle_observations']))

    def test_missing_and_partial_corruption(self):
        with tempfile.TemporaryDirectory(prefix='native-oracle-query-') as directory:
            root = Path(directory)
            self.assertEqual(lookup('OPCONT268_strcmp-ge', root)[1]['state'], 'NOT_PRESENT')
            tree = root / RELATIVE_BUNDLE
            tree.mkdir(parents=True)
            self.assertEqual(lookup('OPCONT268_strcmp-ge', root)[1]['state'], 'INCONSISTENT')
            tree.rmdir()
            shutil.copytree(BUNDLE, tree)
            for name in ['manifest.json', 'results/native-oracle-selection.jsonl', 'evidence/operator-268-20261117/manifest.json', 'evidence/operator-268-20261117/observations.json']:
                with self.subTest(path=name):
                    path = tree / name
                    original = path.read_bytes()
                    try:
                        path.write_bytes(original + b' ')
                        rows, status = lookup('OPCONT268_strcmp-ge', root)
                        self.assertEqual(rows, [])
                        self.assertEqual(status['state'], 'INCONSISTENT')
                    finally:
                        path.write_bytes(original)
            (tree / 'manifest.json').unlink()
            self.assertEqual(lookup('OPCONT268_strcmp-ge', root)[1]['state'], 'INCONSISTENT')
            (tree / 'results/native-oracle-selection.jsonl').unlink()
            self.assertTrue((tree / 'evidence/operator-268-20261117/observations.json').is_file())
            self.assertEqual(lookup('OPCONT268_strcmp-ge', root)[1]['state'], 'INCONSISTENT')

    def test_existing_case_exit_and_availability(self):
        with tempfile.TemporaryDirectory(prefix='native-oracle-query-cli-') as directory:
            root = Path(directory)
            for args in ((), ('--partial',)):
                code, result = run_cli('OPCONT268_strcmp-ge', *args, oracle_root=root)
                self.assertEqual(code, 0)
                self.assertTrue(result['cases'])
                self.assertEqual(result['native_oracle_availability']['state'], 'NOT_PRESENT')
                tree = root / RELATIVE_BUNDLE
                tree.mkdir(parents=True)
                (tree / 'remaining.txt').write_text('partial bundle', encoding='utf8')
                code, result = run_cli('OPCONT268_strcmp-ge', *args, oracle_root=root)
                self.assertEqual(code, 0)
                self.assertTrue(result['cases'])
                self.assertEqual(result['native_oracle_availability']['state'], 'INCONSISTENT')
                self.assertEqual(result['native_oracle_observations'], [])
                (tree / 'remaining.txt').unlink()
                tree.rmdir()


if __name__ == '__main__':
    unittest.main(verbosity=2)
