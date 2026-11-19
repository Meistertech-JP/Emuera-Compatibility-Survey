"""Regression tests against the candidate data and an explicitly chosen query implementation."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ANCESTORS = Path(__file__).resolve().parents
ROOT = next((p if (p / 'results/survey.json').is_file() else p / 'candidate'
             for p in ANCESTORS
             if (p / 'results/survey.json').is_file() or (p / 'candidate/results/survey.json').is_file()))
IMPLEMENTATION = Path(os.environ.get('QUERY_UNDER_TEST',
    str(Path(__file__).resolve().parents[1] / 'tools/query.py')))
spec = importlib.util.spec_from_file_location('query_under_test', IMPLEMENTATION)
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)
query.ROOT = ROOT


def run_query(*args):
    output, error = io.StringIO(), io.StringIO()
    with patch.object(sys, 'argv', ['query.py', *args]), contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
        try:
            code = query.main()
        except SystemExit as exc:
            code = exc.code
    return code, json.loads(output.getvalue()) if output.getvalue() else None


class TypedAcceptanceTests(unittest.TestCase):
    def test_typed_and_kind_filter_agree_for_same_name_distinct_kinds(self):
        code, unfiltered = run_query('GETSTYLE')
        self.assertEqual(code, 0)
        all_rows = unfiltered['historical_acceptance_references']
        self.assertEqual({r['typed_key']['kind'] for r in all_rows},
                         {'expression_function', 'method_as_command'})
        for kind in ('expression_function', 'method_as_command'):
            with self.subTest(kind=kind):
                code1, typed = run_query(f'{kind}:GETSTYLE')
                code2, filtered = run_query('getstyle', '--kind', kind.upper())
                self.assertEqual((code1, code2), (0, 0))
                for field in ('historical_acceptance_references', 'trace_targets', 'verification_requirements', 'trace_case_evidence'):
                    expected = [r for r in unfiltered[field] if r['typed_key']['kind'] == kind]
                    self.assertEqual(typed[field], expected, field)
                    self.assertEqual(filtered[field], expected, field)
                self.assertTrue(typed['historical_acceptance_references'])

    def test_print_typed_search_preserves_original_rows_and_wrong_kind_is_excluded(self):
        _, plain = run_query('PRINT')
        expected = [r for r in plain['historical_acceptance_references']
                    if r['typed_key']['kind'] == 'command_or_syntax']
        self.assertTrue(expected)
        _, typed = run_query('command_or_syntax:PRINT')
        self.assertEqual(typed['historical_acceptance_references'], expected)
        self.assertEqual(typed['trace_targets'], [r for r in plain['trace_targets']
                         if r['typed_key']['kind'] == 'command_or_syntax'])
        _, wrong = run_query('PRINT', '--kind', 'NOT_A_KIND')
        for field in ('historical_acceptance_references', 'trace_targets', 'verification_requirements', 'trace_case_evidence', 'targets', 'selected_evidence_links', 'static_api_evidence'):
            self.assertEqual(wrong[field], [], field)

    def test_identifier_search_and_kind_filter_preserve_scope(self):
        _, original = run_query('GETSTYLE')
        req = next(r for r in original['verification_requirements']
                   if r['typed_key']['kind'] == 'expression_function')
        _, found = run_query(req['requirement_id'], '--kind', 'expression_function')
        self.assertIn(req, found['verification_requirements'])
        _, excluded = run_query(req['requirement_id'], '--kind', 'method_as_command')
        self.assertNotIn(req, excluded['verification_requirements'])
        _, case = run_query('COLON_NORMAL_COMPAT_RAND_YES')
        self.assertEqual(len(case['cases']), 1)

    def test_typed_target_and_case_id_keep_selected_evidence_role(self):
        _, plain = run_query('PRINTDB15')
        self.assertEqual({r['target']['kind'] for r in plain['selected_evidence_links']},
                         {'command_or_syntax', 'structural_syntax'})
        for kind in ('command_or_syntax', 'structural_syntax'):
            expected = [r for r in plain['selected_evidence_links'] if r['target']['kind'] == kind]
            _, typed = run_query(kind + ':PRINTDATA')
            _, filtered = run_query('PRINTDB15', '--kind', kind)
            self.assertEqual([r for r in typed['selected_evidence_links'] if r['case_id'] == 'PRINTDB15'], expected)
            self.assertEqual(filtered['selected_evidence_links'], expected)
            self.assertTrue(all(r['kind'] == kind for r in typed['targets']))

    def test_conflicting_typed_and_kind_is_rejected(self):
        code, result = run_query('expression_function:GETSTYLE', '--kind', 'method_as_command')
        self.assertEqual(code, 2)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
