"""Exercise graphics-case discovery without starting either engine."""
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
BUNDLE = ROOT / 'evidence/graphics-38-cases-20261117'
spec = importlib.util.spec_from_file_location('graphics_38_query', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)


class Graphics38QueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='graphics-38-query-')
        cls.root = Path(cls.tmp.name)
        cls.folder = cls.root / 'evidence/graphics-38-cases-20261117'
        cls.folder.parent.mkdir(parents=True)
        shutil.copytree(BUNDLE, cls.folder)
        cls.cases = json.loads((cls.folder / 'cases.json').read_bytes())['cases']

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def lookup(self, term, kind=None):
        rows, availability = query.saved_observations(term, self.root, kind=kind)
        return [r for r in rows if r['collection'] == 'graphics_38_saved'], availability

    def assert_reference(self, ref, expected):
        self.assertEqual(ref['record']['path'], 'evidence/graphics-38-cases-20261117/' + expected['path'])
        p = self.root / ref['record']['path']
        self.assertTrue(p.is_file())
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), expected['sha256'])
        self.assertEqual(ref['sha256'], expected['sha256'])

    def test_all_case_ids_keep_exact_original_and_followup_references(self):
        self.assertEqual(len(self.cases), 38)
        for index, case in enumerate(self.cases):
            with self.subTest(case=case['case_id']):
                rows, availability = self.lookup(case['case_id'].lower())
                row, = rows
                self.assertEqual(availability['graphics_38'], 'AVAILABLE')
                self.assertEqual(row['match_basis'], 'CASE_ID')
                self.assertEqual(row['matched_case_roles'], case['typed_targets'])
                self.assertEqual(row['historical_verdict'], 'unverified')
                self.assertEqual(row['observation_scope'], 'SAVED_NATIVE_SELECTED_OBSERVATIONS_NOT_CROSS_ENGINE_VERDICT')
                self.assertEqual(row['native_natural_exit'], 'NOT_OBSERVED')
                self.assertEqual(row['py_raw'], 'NOT_INCLUDED_TARGET_MAY_BE_UNREACHED')
                self.assertEqual(row['record']['pointer'], f'/cases/{index}')
                doc = json.loads((self.root / row['record']['path']).read_bytes())
                self.assertEqual(doc['cases'][index]['case_id'], case['case_id'])
                for key in ('fixture', 'config'):
                    self.assert_reference(row['original'][key], case['original'][key])
                for actual, expected in zip(row['original']['native_raw'], case['original']['native_raw']):
                    self.assert_reference(actual, expected)
                self.assertEqual(len(row['original']['native_raw']), 2)
                for actual, expected in zip(row['original']['assets'], case['original']['assets']):
                    self.assert_reference(actual, expected)
                self.assertEqual(len(row['original']['assets']), len(case['original']['assets']))
                self.assertTrue((self.root / row['bundle_readme']['path']).is_file())
                self.assertTrue((self.root / row['english_cases']['path']).is_file())
                self.assertEqual(len(row['later_observations']), len(case['later_observations']))
                for j, (later, source) in enumerate(zip(row['later_observations'], case['later_observations'])):
                    self.assertEqual(later['record']['pointer'], f'/cases/{index}/later_observations/{j}')
                    self.assertEqual(later['relationship'], 'SEPARATE_SUBSEQUENT_NATIVE_RUN')
                    self.assertEqual(later['cross_engine_comparison'], 'NOT_ASSESSED')
                    self.assertEqual(later['post_error_state'], 'NOT_OBSERVED')
                    self.assertEqual(later['natural_exit'], 'NOT_OBSERVED')
                    for key in ('fixture', 'config', 'native_raw', 'crop'):
                        self.assert_reference(later[key], source[key])

    def test_all_typed_roles_and_case_id_kind_filter(self):
        expected = {}
        edges = 0
        for case in self.cases:
            for role in case['typed_targets']:
                expected.setdefault((role['kind'], role['name']), set()).add(case['case_id'])
                edges += 1
        self.assertEqual(edges, 64)
        for (kind, name), case_ids in expected.items():
            with self.subTest(kind=kind, name=name):
                rows, _ = self.lookup(kind + ':' + name)
                self.assertEqual({r['case_id'] for r in rows}, case_ids)
                self.assertTrue(all(r['matched_case_roles'] == [{'kind': kind, 'name': name}] for r in rows))
        for case in self.cases:
            wrong = 'operator'
            self.assertEqual(self.lookup(case['case_id'], wrong)[0], [])
        with self.assertRaisesRegex(ValueError, 'conflicting typed kind'):
            self.lookup('expression_function:GWIDTH', 'method_as_command')

    def test_gclear_separate_later_runs_and_original_discrepancy(self):
        for kind, case_id in [('expression_function', 'GMUTATE231_gclear-expr-missing-invalid-color'),
                              ('method_as_command', 'GMUTATE231_gclear-method-missing-invalid-color')]:
            rows, _ = self.lookup(kind + ':GCLEAR')
            row, = [r for r in rows if r['case_id'] == case_id]
            later, = row['later_observations']
            self.assertEqual(later['matching_bytes_scope'], 'DO_NOT_ESTABLISH_SAME_ATTEMPT')
            self.assertEqual(later['crop_scope'], 'DOWNSCALED_CROP_NOT_ORIGINAL_RESOLUTION_PIXEL_PROOF')
            self.assertEqual(later['historical_diagnostic'],
                             'OLD_CLASSIFICATION_UNOBSERVED_BUT_ORIGINAL_RAW_HAS_DIAGNOSTIC_CAUSE_UNKNOWN')
            doc = json.loads((self.root / row['record']['path']).read_bytes())
            record = doc['cases'][int(row['record']['pointer'].rsplit('/', 1)[-1])]
            self.assertEqual(record['original']['recorded_claim_vs_raw']['cause'], 'unknown')
            for ref in row['original']['native_raw'] + [later['native_raw']]:
                raw = (self.root / ref['record']['path']).read_bytes().decode('utf-16')
                self.assertIn('0x100000000', raw)
                self.assertIn('GRAPHICS231.ERBの4行目', raw)

    def test_absent_incomplete_modified_and_resealed_are_distinct(self):
        with tempfile.TemporaryDirectory(prefix='graphics-38-negative-') as tmp:
            root = Path(tmp)
            self.assertEqual(query._graphics_38('GWIDTH', root, None), ([], 'NOT_INSTALLED'))
            folder = root / 'evidence/graphics-38-cases-20261117'
            folder.parent.mkdir(parents=True)
            folder.mkdir()
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                query._graphics_38('GWIDTH', root, None)
            folder.rmdir()
            shutil.copytree(BUNDLE, folder)
            raw = folder / 'cases/C01/original/raw/native-01.bin'
            raw.unlink()
            with self.assertRaisesRegex(ValueError, 'file set, size or SHA-256 mismatch'):
                query._graphics_38('GWIDTH', root, None)
            shutil.copyfile(BUNDLE / 'cases/C01/original/raw/native-01.bin', raw)
            raw.write_bytes(raw.read_bytes() + b'X')
            with self.assertRaisesRegex(ValueError, 'file set, size or SHA-256 mismatch'):
                query._graphics_38('GWIDTH', root, None)
            manifest = folder / 'manifest.json'
            data = json.loads(manifest.read_bytes())
            entry, = [x for x in data['files'] if x['path'] == 'cases/C01/original/raw/native-01.bin']
            entry['size'] = raw.stat().st_size
            entry['sha256'] = hashlib.sha256(raw.read_bytes()).hexdigest()
            manifest.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'manifest snapshot mismatch'):
                query._graphics_38('GWIDTH', root, None)

    def test_cli_keeps_historical_projection_and_new_evidence(self):
        case_id = 'GMUTATE231_gclear-expr-missing-invalid-color'
        for term in (case_id, 'expression_function:GCLEAR'):
            with self.subTest(term=term), patch.object(query, 'ROOT', ROOT), \
                    patch.object(sys, 'argv', ['query.py', term]), contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(query.main(), 0)
                result = json.loads(out.getvalue())
                records = [x for x in result['saved_observations'] if x['collection'] == 'graphics_38_saved']
                row, = [x for x in records if x['case_id'] == case_id]
                self.assertEqual(row['historical_verdict'], 'unverified')
                self.assertEqual(len(row['later_observations']), 1)
                self.assertEqual(result['saved_observation_availability']['graphics_38'], 'AVAILABLE')
                if term == case_id:
                    historical, = [x for x in result['case_register_projection'] if x['case']['case_id'] == case_id]
                    self.assertEqual(historical['case']['scenario_verdict'], 'unverified')


if __name__ == '__main__':
    unittest.main()
