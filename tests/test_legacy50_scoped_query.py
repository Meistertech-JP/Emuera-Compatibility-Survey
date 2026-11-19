"""Real-bundle regression tests; copy into candidate/tests, no private paths."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('scoped_query_for_legacy50_test', ROOT / 'tools/scoped_observations_query.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
BUNDLE = ROOT / helper.LEGACY50


def resolve(doc, pointer):
    node = doc
    if not pointer:
        return node
    for part in pointer[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Legacy50Query(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(BUNDLE, self.root / helper.LEGACY50)
        self.bundle = self.root / helper.LEGACY50
        self.doc = json.loads((self.bundle / 'selected-observations.json').read_bytes())

    def lookup(self, term, kind=None, override=None):
        matches, states = helper.lookup(term, self.root, kind, override)
        return [x for x in matches if x['bundle'] == 'legacy50_selected'], states['legacy50_selected']

    def test_real_selection_all_ids_targets_and_pointers(self):
        cases = self.doc['getter']['cases'] + self.doc['operator_normal']['cases']
        target_set = {(r['target']['kind'], r['target']['name']) for r in self.doc['getter']['cases']}
        target_set.update((m['target']['kind'], m['target']['name']) for r in self.doc['operator_normal']['cases'] for m in r['marker_observations'])
        self.assertEqual(len(target_set), 27)
        self.assertEqual(sum(len(c['marker_observations']) for c in self.doc['operator_normal']['cases']), 71)
        for case in cases:
            with self.subTest(case=case['case_id']):
                hits, state = self.lookup(case['case_id'].swapcase())
                self.assertEqual(state['state'], 'AVAILABLE')
                self.assertEqual(len(hits), 1)
                hit = hits[0]
                self.assertEqual(resolve(self.doc, hit['record']['pointer']), case)
                for selection in hit['selected']:
                    self.assertEqual(resolve(self.doc, selection['pointer']), selection['value'])
                self.assertIn('not included', hit['raw_scope'])
                self.assertIn('unobserved', hit['execution_scope'])
                self.assertIn('unidentified', hit['historical_acceptance_scope'])
        for kind, name in target_set:
            with self.subTest(kind=kind, name=name):
                hits, state = self.lookup(kind + ':' + name)
                self.assertEqual(state['state'], 'AVAILABLE')
                self.assertTrue(hits)
                for hit in hits:
                    self.assertEqual(hit['matched_targets'], [{'kind': kind, 'name': name}])
                    for item in hit['selected']:
                        self.assertEqual(resolve(self.doc, item['pointer']), item['value'])
                        if '/marker_observations/' in item['pointer']:
                            self.assertEqual(item['value']['target'], {'kind': kind, 'name': name})

    def test_getter_type_condition_and_selected_values(self):
        hits, _ = self.lookup('expression_function:GETDEFCOLOR')
        self.assertEqual([h['case_id'] for h in hits], ['GETTER251_expression_0'])
        selections = {x['pointer'].rsplit('/', 1)[-1]: x['value'] for x in hits[0]['selected']}
        self.assertEqual(selections['condition']['value_type'], 'integer')
        self.assertEqual([o['state']['value'] for o in selections['observations']], ['1122867', '1122867', '12632256'])
        command, _ = self.lookup('method_as_command:GETDEFCOLOR')
        self.assertEqual([h['case_id'] for h in command], ['GETTER251_method_0'])
        self.assertEqual(self.lookup('operator:GETDEFCOLOR')[0], [])

    def test_operator_case_target_filter_and_shared_runs(self):
        hits, _ = self.lookup('operator:&&')
        self.assertEqual(len(hits), 1)
        hit = hits[0]
        markers = [s['value'] for s in hit['selected'] if '/marker_observations/' in s['pointer']]
        self.assertEqual(len(markers), 5)
        short = next(m for m in markers if m['marker'] == 'LOG20')
        self.assertTrue(any('0&&ZZ_BAD()' in s for s in short['condition_statements']))
        self.assertTrue(all('VALUE=0 BADCOUNT=0' in o['observed_marker'] for o in short['observations']))
        run_pointers = [s for s in hit['selected'] if s['pointer'].startswith('/runs/')]
        self.assertEqual(len(run_pointers), 3)
        self.assertEqual(sum(r['value']['engine'] == 'Native' for r in run_pointers), 2)
        case, _ = self.lookup('OPNORMAL273_E140')
        case_markers = [x for x in case[0]['selected'] if '/marker_observations/' in x['pointer']]
        self.assertEqual(len(case_markers), 14)
        self.assertEqual({m['value']['target']['name'] for m in case_markers}, {'&&', '^^', '!&'})
        filtered, _ = self.lookup('OPNORMAL273_E140', 'expression_function')
        self.assertEqual(filtered, [])
        override, state = self.lookup('operator:&&', override='some-other-register')
        self.assertEqual(override, [])
        self.assertEqual(state, {'state': 'REGISTER_OVERRIDE_NOT_CHECKED', 'bundle_integrity': 'AVAILABLE',
                                 'register_scope': 'EXPLICIT_CASE_PROJECTION_OVERRIDE'})

    def test_missing_and_corrupt_are_distinct(self):
        shutil.rmtree(self.bundle)
        self.assertEqual(self.lookup('operator:&&')[1]['state'], 'NOT_INSTALLED')
        shutil.copytree(BUNDLE, self.bundle)
        (self.bundle / 'selected-observations.json').unlink()
        hits, state = self.lookup('operator:&&')
        self.assertEqual((hits, state['state']), ([], 'MISSING_FILES'))
        shutil.copy2(BUNDLE / 'selected-observations.json', self.bundle / 'selected-observations.json')
        with (self.bundle / 'selected-observations.json').open('ab') as f:
            f.write(b' ')
        self.assertEqual(self.lookup('operator:&&'), ([], {'state': 'INCONSISTENT'}))
        self.assertEqual(self.lookup('operator:&&', override='other-register'), ([], {'state': 'INCONSISTENT'}))
        shutil.copy2(BUNDLE / 'selected-observations.json', self.bundle / 'selected-observations.json')
        with (self.bundle / 'file-set-manifest.json').open('ab') as f:
            f.write(b' ')
        self.assertEqual(self.lookup('operator:&&'), ([], {'state': 'INCONSISTENT'}))
        shutil.copy2(BUNDLE / 'file-set-manifest.json', self.bundle / 'file-set-manifest.json')
        (self.bundle / 'unexpected').write_bytes(b'x')
        self.assertEqual(self.lookup('operator:&&'), ([], {'state': 'INCONSISTENT'}))

    def test_duplicate_case_and_marker_rejected_even_if_rebound(self):
        original = self.doc
        for mutation in ('case', 'marker', 'run'):
            with self.subTest(mutation=mutation):
                doc = json.loads(json.dumps(original))
                if mutation == 'case':
                    doc['getter']['cases'][1]['case_id'] = doc['getter']['cases'][0]['case_id']
                elif mutation == 'marker':
                    ms = doc['operator_normal']['cases'][0]['marker_observations']
                    ms[1]['marker'] = ms[0]['marker']
                else:
                    doc['operator_normal']['cases'][0]['marker_observations'][0]['observations'][0]['run_id'] = 'E138-retained-native-1'
                raw = json.dumps(doc, ensure_ascii=False).encode('utf-8')
                (self.bundle / 'selected-observations.json').write_bytes(raw)
                m = json.loads((BUNDLE / 'file-set-manifest.json').read_bytes())
                entry = next(x for x in m['files'] if x['path'] == 'selected-observations.json')
                entry.update(size=len(raw), sha256=digest(raw))
                manifest = json.dumps(m).encode('utf-8')
                (self.bundle / 'file-set-manifest.json').write_bytes(manifest)
                pin = (helper.LEGACY50_PIN[0], digest(manifest), *helper.LEGACY50_PIN[2:])
                with patch.object(helper, 'LEGACY50_PIN', pin):
                    self.assertEqual(self.lookup('operator:&&'), ([], {'state': 'INCONSISTENT'}))

    def test_actual_query_cli(self):
        def query(term, *extra):
            env = dict(os.environ, PYTHONUTF8='1')
            p = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'tools/query.py'), term, *extra],
                               cwd=ROOT, env=env, capture_output=True, timeout=60)
            return p.returncode, json.loads(p.stdout.decode('utf-8'))
        code, out = query('operator:&&')
        self.assertEqual(code, 0)
        self.assertEqual(out['scoped_observations_availability']['legacy50_selected']['state'], 'AVAILABLE')
        hit = next(x for x in out['scoped_observations'] if x['bundle'] == 'legacy50_selected')
        self.assertEqual(hit['case_id'], 'OPNORMAL273_E140')
        self.assertTrue(all(x['value']['target']['name'] == '&&' for x in hit['selected'] if '/marker_observations/' in x['pointer']))
        code, out = query('GETTER251_expression_0')
        self.assertEqual(code, 0)
        self.assertTrue(any(x['case_id'] == 'GETTER251_expression_0' for x in out['scoped_observations']))
        code, out = query('ZZZ_NONEXISTENT_LEGACY50_92817')
        self.assertEqual(code, 1)
        self.assertEqual(out['scoped_observations_availability']['legacy50_selected']['state'], 'AVAILABLE')

        # Construct a valid, different explicit register with the same case ID
        # and a conflicting verdict, without changing the real register.
        register = ROOT / 'evidence/case-register-2898-20261117'
        cores = [json.loads(x) for x in (register / 'core.jsonl').read_bytes().splitlines()]
        details = [json.loads(x) for x in (register / 'cases.jsonl').read_bytes().splitlines()]
        idx = next(i for i, r in enumerate(cores) if r['case_id'] == 'GETTER251_expression_0')
        self.assertEqual(cores[idx]['scenario_verdict'], 'different_scoped')
        cores[idx]['scenario_verdict'] = details[idx]['scenario_verdict'] = 'matched_scoped'
        override = self.root / 'alternate-register'
        override.mkdir()
        manifest = json.loads((register / 'manifest.json').read_bytes())
        for name, row in (('core.jsonl', cores[idx]), ('cases.jsonl', details[idx])):
            raw = (json.dumps(row, ensure_ascii=False) + '\n').encode('utf-8')
            (override / name).write_bytes(raw)
            manifest['files'][name]['size'] = len(raw)
            manifest['files'][name]['sha256'] = digest(raw)
        manifest['records'] = 1
        manifest['candidate_survey_sha256'] = '0' * 64
        manifest['candidate_trace_sha256'] = '0' * 64
        (override / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        code, out = query('GETTER251_expression_0', '--case-projection-dir', str(override))
        self.assertEqual(code, 0)
        self.assertEqual(out['case_register_projection'][0]['case']['scenario_verdict'], 'matched_scoped')
        self.assertFalse(any(x['bundle'] == 'legacy50_selected' for x in out['scoped_observations']))
        self.assertEqual(out['scoped_observations_availability']['legacy50_selected'],
                         {'state': 'REGISTER_OVERRIDE_NOT_CHECKED', 'bundle_integrity': 'AVAILABLE',
                          'register_scope': 'EXPLICIT_CASE_PROJECTION_OVERRIDE'})


if __name__ == '__main__':
    unittest.main()
