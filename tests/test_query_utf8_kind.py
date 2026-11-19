"""Regress readable UTF-8 output and effective kind against candidate data."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve()
ROOT = next((p if (p / 'results/survey.json').is_file() else p / 'candidate'
             for p in HERE.parents
             if (p / 'results/survey.json').is_file() or (p / 'candidate/results/survey.json').is_file()))
QUERY = Path(os.environ.get('QUERY_UNDER_TEST', str(HERE.parents[1] / 'tools/query.py')))
spec = importlib.util.spec_from_file_location('query_utf8_kind_test', QUERY)
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)
query.ROOT = ROOT


def run_query(*args, stream=None):
    out, err = stream if stream is not None else io.StringIO(), io.StringIO()
    with patch.object(sys, 'argv', ['query.py', *args]), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = query.main()
        except SystemExit as exc:
            code = exc.code
    return code, out, err.getvalue()


class TerminalBuffer(io.BytesIO):
    def isatty(self):
        return True


class Unconfigurable:
    encoding = 'cp932'
    def __init__(self):
        self.output = ''
    def reconfigure(self, **kwargs):
        raise io.UnsupportedOperation('cannot change encoding')
    def write(self, text):
        self.output += text


class UTF8Only:
    encoding = 'UTF8'
    def __init__(self):
        self.output = ''
    def write(self, text):
        self.output += text


class NoOpReconfigure(Unconfigurable):
    def reconfigure(self, **kwargs):
        pass


class QueryUTF8Tests(unittest.TestCase):
    def test_cp932_redirect_emits_readable_utf8_and_matches_utf8_redirect(self):
        bootstrap = ('import importlib.util,sys; from pathlib import Path; '
                     'spec=importlib.util.spec_from_file_location("query_test",sys.argv[1]); '
                     'q=importlib.util.module_from_spec(spec); spec.loader.exec_module(q); '
                     'q.ROOT=Path(sys.argv[2]); sys.argv=[sys.argv[1],"expression_function:SUBSTRINGU"]; '
                     'print("before="+sys.stdout.encoding,file=sys.stderr); raise SystemExit(q.main())')
        outputs = []
        for encoding in ('cp932', 'utf-8'):
            env = dict(os.environ, PYTHONIOENCODING=encoding, PYTHONUTF8='0')
            p = subprocess.run([sys.executable, '-B', '-c', bootstrap, str(QUERY), str(ROOT)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            with self.subTest(encoding=encoding):
                self.assertEqual(p.returncode, 0, p.stderr.decode('ascii', errors='replace'))
                self.assertIn(('before='+encoding).encode('ascii'), p.stderr.lower())
                text = p.stdout.decode('utf-8')
                self.assertTrue(any(ord(ch) > 127 for ch in text), 'Japanese must remain visible')
                outputs.append(json.loads(text))
        if len(outputs) == 2:
            self.assertEqual(outputs[0], outputs[1])
            self.assertTrue(any(row['collection'] == 'remaining_96_saved' for row in outputs[0]['saved_observations']))

    def test_cp932_terminal_stream_becomes_utf8(self):
        raw = TerminalBuffer()
        terminal = io.TextIOWrapper(raw, encoding='cp932', write_through=True)
        self.assertTrue(terminal.isatty())
        code, _, _ = run_query('expression_function:SUBSTRINGU', stream=terminal)
        self.assertEqual(code, 0)
        self.assertEqual(terminal.encoding.lower().replace('-', ''), 'utf8')
        text = raw.getvalue().decode('utf-8')
        self.assertTrue(any(ord(ch) > 127 for ch in text))
        self.assertTrue(json.loads(text)['saved_observations'])
        terminal.detach()

    def test_stringio_is_text_only_and_preserves_japanese(self):
        out = io.StringIO()
        code, _, _ = run_query('expression_function:SUBSTRINGU', stream=out)
        self.assertEqual(code, 0)
        self.assertTrue(any(ord(ch) > 127 for ch in out.getvalue()))
        self.assertTrue(json.loads(out.getvalue())['saved_observations'])

    def test_unsupported_or_unknown_stream_fails_explicitly_without_output(self):
        for out in (Unconfigurable(), NoOpReconfigure(),
                    type('Unknown', (), {'write': lambda self, text: None})()):
            with self.subTest(stream=type(out).__name__):
                code, _, err = run_query('expression_function:SUBSTRINGU', stream=out)
                self.assertEqual(code, 2)
                self.assertIn('stdout', err.lower())
                if isinstance(out, Unconfigurable):
                    self.assertEqual(out.output, '')

    def test_known_utf8_custom_stream_needs_no_reconfigure(self):
        out = UTF8Only()
        code, _, _ = run_query('expression_function:SUBSTRINGU', stream=out)
        self.assertEqual(code, 0)
        self.assertTrue(any(ord(ch) > 127 for ch in out.output))
        self.assertTrue(json.loads(out.output)['saved_observations'])

    def test_effective_kind_and_existing_semantics(self):
        outputs = []
        for args in (('expression_function:GETSTYLE',), ('GETSTYLE', '--kind', 'expression_function')):
            code, out, _ = run_query(*args)
            self.assertEqual(code, 0)
            outputs.append(json.loads(out.getvalue()))
        a, b = outputs
        self.assertEqual(a['saved_observation_kind_filter']['kind'], 'expression_function')
        self.assertEqual(b['saved_observation_kind_filter']['kind'], 'expression_function')
        for field in ('saved_observations', 'historical_acceptance_references', 'trace_targets'):
            self.assertEqual(a[field], b[field])
        code, _, err = run_query('expression_function:GETSTYLE', '--kind', 'method_as_command')
        self.assertEqual(code, 2)
        self.assertTrue(err)

    def test_query_values_against_candidate_records(self):
        survey = json.loads((ROOT / 'results/survey.json').read_text(encoding='utf-8'))
        trace_root = ROOT / 'evidence/694-target-trace-20261117'
        trace = json.loads((trace_root / 'projection.json').read_text(encoding='utf-8'))
        requirement_rows = [json.loads(line) for line in
                            (trace_root / trace['requirements']['path']).read_text(encoding='utf-8').splitlines()]
        observations = json.loads((ROOT / 'evidence/remaining-96-20261117/index.json').read_text(encoding='utf-8'))
        for name in ('SUBSTRINGU', 'GETSTYLE'):
            with self.subTest(name=name):
                target = {'kind': 'expression_function', 'name': name}
                code, out, err = run_query('expression_function:' + name)
                self.assertEqual(code, 0, err)
                actual = json.loads(out.getvalue())
                self.assertEqual(actual['targets'], [r for r in survey['targets']
                                                     if r['kind'] == target['kind'] and r['name'] == name])
                self.assertEqual(len(actual['targets']), 1)
                self.assertEqual(actual['trace_targets'], [r for r in trace['targets'] if r['typed_key'] == target])
                self.assertEqual(len(actual['trace_targets']), 1)
                self.assertEqual(actual['verification_requirements'],
                                 [r for r in requirement_rows if r['typed_key'] == target])
                self.assertTrue(actual['verification_requirements'])
                ids = set(actual['targets'][0]['case_ids'])
                self.assertEqual(actual['linked_main_scenarios'],
                                 [r for r in survey['main_scenarios'] if r['case_id'] in ids])
                expected = {r['case_id']: r for r in observations['cases']
                            if target in r['parent_and_case_roles'] or target in r['registered_roles']}
                saved = [r for r in actual['saved_observations'] if r['collection'] == 'remaining_96_saved']
                self.assertEqual({r['case_id'] for r in saved}, set(expected))
                self.assertEqual(len(saved), len(expected))
                for row in saved:
                    source = expected[row['case_id']]
                    self.assertEqual(row['recorded_parent_roles'], source['parent_and_case_roles'])
                    self.assertEqual(row['recorded_verdict'], source['record']['scenario_verdict'])
                    self.assertEqual(row['record']['path'], 'evidence/remaining-96-20261117/index.json')
                    pos = int(row['record']['pointer'].removeprefix('/cases/'))
                    self.assertEqual(observations['cases'][pos]['case_id'], row['case_id'])


if __name__ == '__main__':
    unittest.main()
