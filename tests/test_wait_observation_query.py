"""Search the two later wait observations without running either engine."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('wait_query', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)


class WaitObservationQueryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='wait-query-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ('wait-release-20261117', 'wait-c15-20261117'):
            destination = self.root / 'evidence' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(ROOT / 'evidence' / name, destination)

    def lookup(self, term, kind=None):
        rows, states = query.saved_observations(term, self.root, kind=kind)
        return [r for r in rows if r['collection'].startswith('wait_')], states

    def test_command_and_case_lookups_resolve_distinct_records(self):
        for command, case in (('PRINTVKW', 'PRINTVKWC15'), ('PRINTVDW', 'PRINTVDWC15')):
            for term in (command.lower(), 'command_or_syntax:' + command, case):
                with self.subTest(term=term):
                    rows, states = self.lookup(term)
                    self.assertEqual(states['wait_release'], 'AVAILABLE')
                    self.assertEqual(states['wait_c15'], 'AVAILABLE')
                    self.assertEqual(len(rows), 2)
                    for row in rows:
                        self.assertEqual(row['case_id'], case)
                        self.assertEqual(row['matched_case_roles'],
                                         [{'kind': 'command_or_syntax', 'name': command}])
                        self.assertEqual(row['historical_verdict'], 'unverified')
                        self.assertEqual(row['historical_verdict_scope'], 'ORIGINAL_SURVEY_UNCHANGED')
                        self.assertIn('NOT_OBSERVED', row['native_natural_exit'])
                        for key in ('record', 'manifest', 'bundle_readme', 'native_history'):
                            self.assertTrue((self.root / row[key]['path']).is_file())
                        doc = json.loads((self.root / row['record']['path']).read_bytes())
                        index = int(row['record']['pointer'].rsplit('/', 1)[-1])
                        record = doc['records'][index]
                        if row['collection'] == 'wait_release_subsequent_observation':
                            self.assertEqual(record['command'], command)
                            self.assertEqual(record['argument'], 42)
                            self.assertEqual(row['relationship'],
                                             'RELATED_COMMAND_DIFFERENT_FIXTURE_NOT_C15_REPLAY')
                            self.assertEqual(record['py']['returncode'], 0)
                        else:
                            self.assertEqual(record['case_id'], case)
                            self.assertEqual(row['relationship'], 'SUBSEQUENT_OBSERVATION_USING_C15_FIXTURE')
                            self.assertEqual(record['py_returncode'], 1)
                            self.assertIn('post_fault_state', row['unobserved'])

    def test_kind_filter_applies_to_names_and_case_ids(self):
        for term in ('PRINTVKW', 'PRINTVKWC15', 'expression_function:PRINTVDW'):
            self.assertEqual(self.lookup(term, None if ':' in term else 'expression_function')[0], [])
        with self.assertRaisesRegex(ValueError, 'conflicting typed kind'):
            self.lookup('command_or_syntax:PRINTVKW', 'expression_function')
        self.assertEqual(self.lookup('PRINTVDWC15', 'command_or_syntax')[0][1]['case_id'], 'PRINTVDWC15')

    def test_missing_and_incomplete_bundles_are_distinct(self):
        shutil.rmtree(self.root / 'evidence/wait-c15-20261117')
        rows, states = self.lookup('PRINTVKW')
        self.assertEqual(len(rows), 1)
        self.assertEqual(states['wait_c15'], 'NOT_INSTALLED')
        (self.root / 'evidence/wait-c15-20261117').mkdir()
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            self.lookup('PRINTVKW')

    def test_modified_or_resealed_material_cannot_be_accepted(self):
        bundle = self.root / 'evidence/wait-c15-20261117'
        history = bundle / 'PRINTVKWC15/native-history.bin'
        original = history.read_bytes()
        history.write_bytes(original + b'X')
        with self.assertRaisesRegex(ValueError, 'file set, size or SHA-256 mismatch'):
            self.lookup('PRINTVKW')
        manifest = bundle / 'manifest.json'
        doc = json.loads(manifest.read_bytes())
        item, = [f for f in doc['files'] if f['path'] == 'PRINTVKWC15/native-history.bin']
        item['size'] = history.stat().st_size
        item['sha256'] = hashlib.sha256(history.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(doc), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'manifest snapshot mismatch'):
            self.lookup('PRINTVKW')

    def test_cli_preserves_historical_verdict_and_adds_both_bundles(self):
        for command, case in (('PRINTVKW', 'PRINTVKWC15'), ('PRINTVDW', 'PRINTVDWC15')):
            for term in ('command_or_syntax:' + command, case):
                with self.subTest(term=term), patch.object(query, 'ROOT', ROOT), \
                        patch.object(sys, 'argv', ['query.py', term]), contextlib.redirect_stdout(io.StringIO()) as out:
                    self.assertEqual(query.main(), 0)
                    result = json.loads(out.getvalue())
                    rows = [r for r in result['saved_observations'] if r['collection'].startswith('wait_')]
                    self.assertEqual({r['collection'] for r in rows},
                                     {'wait_release_subsequent_observation', 'wait_c15_subsequent_observation'})
                    self.assertTrue(all(r['case_id'] == case for r in rows))
                    if term == case:
                        old, = [r for r in result['case_register_projection'] if r['case']['case_id'] == case]
                        self.assertEqual(old['case']['scenario_verdict'], 'unverified')


if __name__ == '__main__':
    unittest.main()
