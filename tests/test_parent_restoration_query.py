"""Tests for historical metadata lookup; does not start an engine."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT
BUNDLE = DATA_ROOT / 'evidence/parent-restoration-40-20261117'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


query = load('restoration_query', ROOT / 'tools/query.py')


class ParentRestorationQueryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='restoration-query-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bundle = self.root / 'evidence/parent-restoration-40-20261117'
        self.bundle.parent.mkdir(parents=True)
        shutil.copytree(BUNDLE, self.bundle)
        self.source = [json.loads(line) for line in (self.bundle / 'targets.jsonl').read_bytes().splitlines()]

    def test_all_40_typed_targets_and_all_218_case_ids(self):
        self.assertEqual(len(self.source), 40)
        expected = collections.defaultdict(set)
        for number, source in enumerate(self.source, 1):
            target = source['target']
            term = target['kind'] + ':' + target['name']
            matches, state = query.parent_restoration_40(term.lower(), self.root)
            row, = matches
            self.assertEqual(state, 'AVAILABLE')
            self.assertEqual(row['target'], target)
            self.assertEqual(row['record']['line_1based'], number)
            self.assertEqual(row['source_access'], 'original_not_included')
            self.assertEqual(row['limits'], source['limits'])
            self.assertEqual(row['historical_restoration_outcome'], source['restoration_record']['comparison_outcome'])
            self.assertEqual(row['later_ledger_outcome'], source['later_ledger_snapshot']['comparison_outcome'])
            self.assertTrue((self.root / row['readme_ja']['path']).is_file())
            self.assertTrue((self.root / row['readme_en']['path']).is_file())
            for cid in source['restoration_record']['case_ids_as_recorded']:
                expected[cid].add((target['kind'], target['name']))
        self.assertEqual(len(expected), 218)
        self.assertEqual(sum(len(v) for v in expected.values()), 232)
        for cid, roles in expected.items():
            with self.subTest(case_id=cid):
                matches, state = query.parent_restoration_40(cid.lower(), self.root)
                self.assertEqual(state, 'AVAILABLE')
                self.assertEqual({(r['target']['kind'], r['target']['name']) for r in matches}, roles)
                self.assertTrue(all(r['match_basis'] == 'CASE_ID' and r['matched_case_id'] == cid for r in matches))

    def test_fontstyle_outcomes_stay_separate_and_originals_are_withheld(self):
        rows, _ = query.parent_restoration_40('command_or_syntax:FONTSTYLE', self.root)
        row, = rows
        self.assertEqual(row['historical_restoration_outcome'], 'documented_difference')
        self.assertEqual(row['later_ledger_outcome'], 'different_scoped')
        self.assertEqual(row['separate_later_parent_outcome'], 'different_scoped')
        self.assertIn('not a fresh acceptance', row['limits'][1])
        self.assertEqual(row['source_access'], 'original_not_included')
        self.assertEqual(query.parent_restoration_40('FONTSTYLE_NEG1', self.root)[0][0]['target'], row['target'])
        self.assertEqual(query.parent_restoration_40('expression_function:FONTSTYLE', self.root)[0], [])
        self.assertEqual(query.parent_restoration_40('FONTSTYLE_NEG1', self.root, kind='expression_function')[0], [])
        self.assertEqual(query.parent_restoration_40('no-such-case', self.root), ([], 'AVAILABLE'))
        with self.assertRaisesRegex(ValueError, 'conflicting typed kind'):
            query.parent_restoration_40('command_or_syntax:FONTSTYLE', self.root, kind='expression_function')

    def test_missing_incomplete_and_changed_snapshots_are_distinct(self):
        empty = self.root / 'empty'
        empty.mkdir()
        self.assertEqual(query.parent_restoration_40('PRINT', empty), ([], 'NOT_INSTALLED'))
        (self.bundle / 'README.md').unlink()
        self.assertEqual(query.parent_restoration_40('PRINT', self.root), ([], 'INCOMPLETE'))
        shutil.copyfile(BUNDLE / 'README.md', self.bundle / 'README.md')
        for name in ('targets.jsonl', 'README.ja.md', 'README.md'):
            path = self.bundle / name
            original = path.read_bytes()
            path.write_bytes(original + b' ')
            self.assertEqual(query.parent_restoration_40('PRINT', self.root), ([], 'SNAPSHOT_MISMATCH'))
            path.write_bytes(original)
        # A newly sealed manifest cannot change the independent query pin.
        path = self.bundle / 'targets.jsonl'
        path.write_bytes(path.read_bytes() + b' ')
        manifest_path = self.bundle / 'manifest.json'
        manifest = json.loads(manifest_path.read_bytes())
        entry = next(item for item in manifest['files'] if item['path'] == 'targets.jsonl')
        entry['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        entry['size'] = path.stat().st_size
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
        self.assertEqual(query.parent_restoration_40('PRINT', self.root), ([], 'SNAPSHOT_MISMATCH'))

    def test_cli_preserves_other_results_and_wires_new_links(self):
        def cli(term):
            process = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/query.py'), term],
                                     capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(process.stderr, '')
            return process.returncode, json.loads(process.stdout)

        target = {'kind': 'command_or_syntax', 'name': 'FONTSTYLE'}
        code, result = cli('command_or_syntax:FONTSTYLE')
        self.assertEqual(code, 0)
        self.assertEqual(result['parent_restoration_40_availability'], 'AVAILABLE')
        row, = result['parent_restoration_40']
        self.assertEqual(row['target'], target)
        self.assertEqual(row['match_basis'], 'TYPED_TARGET')
        self.assertIsNone(row['matched_case_id'])
        self.assertEqual(row['historical_restoration_outcome'], 'documented_difference')
        self.assertEqual(row['later_ledger_outcome'], 'different_scoped')
        self.assertEqual(row['separate_later_parent_outcome'], 'different_scoped')
        self.assertEqual(row['source_access'], 'original_not_included')
        self.assertIn('not a fresh acceptance', row['limits'][1])
        self.assertEqual(row['record']['path'], 'evidence/parent-restoration-40-20261117/targets.jsonl')
        self.assertEqual(row['record']['location'], 'CANDIDATE_RELATIVE')
        record = json.loads((ROOT / row['record']['path']).read_bytes().splitlines()[row['record']['line_1based'] - 1])
        self.assertEqual(record['target'], target)
        self.assertEqual(record['restoration_record']['comparison_outcome'], 'documented_difference')
        for key, name in (('readme_ja', 'README.ja.md'), ('readme_en', 'README.md')):
            ref = row[key]
            self.assertEqual(ref['path'], 'evidence/parent-restoration-40-20261117/' + name)
            self.assertEqual(ref['location'], 'CANDIDATE_RELATIVE')
            self.assertTrue((ROOT / ref['path']).is_file())
        self.assertFalse(query._has_private_path(row))

        # Existing target and saved observation retain their separate, scoped results.
        old_target, = result['targets']
        self.assertEqual((old_target['kind'], old_target['name']), ('command_or_syntax', 'FONTSTYLE'))
        self.assertEqual(old_target['comparison_outcome'], 'different_scoped')
        saved, = [r for r in result['saved_observations']
                  if r['collection'] == 'method_display_state_15_saved']
        self.assertEqual(saved['case_id'], 'DISPLAYSTATE_CMD_FONTSTYLE')
        self.assertEqual(saved['matched_case_roles'], [target])
        self.assertEqual(saved['recorded_verdict'], 'matched_scoped')
        self.assertEqual(saved['sharing_scope'], 'ONE_RECORDED_BATCH_NOT_15_INDEPENDENT_CASE_RUNS')
        self.assertEqual(saved['public_pyz_sha_scope'], 'COMPARISON_DECLARED_EXECUTION_TIME_BEFORE_AFTER_NOT_ESTABLISHED')
        self.assertEqual(set(saved['native_natural_exit_by_mode'].values()), {'NOT_OBSERVED_CLEANUP_RECORDED'})
        self.assertEqual(result['saved_observation_kind_filter']['kind'], 'command_or_syntax')

        code, by_case = cli('FONTSTYLE_NEG1')
        self.assertEqual(code, 0)
        case_row, = by_case['parent_restoration_40']
        self.assertEqual(case_row['target'], target)
        self.assertEqual(case_row['match_basis'], 'CASE_ID')
        self.assertEqual(case_row['matched_case_id'], 'FONTSTYLE_NEG1')
        self.assertEqual(case_row['historical_restoration_outcome'], 'documented_difference')
        self.assertEqual(case_row['later_ledger_outcome'], 'different_scoped')
        self.assertEqual(case_row['record'], row['record'])
        existing_case, = by_case['cases']
        self.assertEqual(existing_case['case_id'], 'FONTSTYLE_NEG1')
        self.assertEqual(existing_case['scenario_verdict'], 'different_scoped')

        code, existing = cli('PRINTDB15')
        self.assertEqual(code, 0)
        self.assertEqual(existing['parent_restoration_40'], [])
        expected_roles = {('command_or_syntax', 'PRINTDATA'), ('structural_syntax', 'PRINTDATA')}
        links = existing['selected_evidence_links']
        self.assertEqual({(x['target']['kind'], x['target']['name']) for x in links}, expected_roles)
        self.assertEqual(len(links), 2)
        self.assertTrue(all(x['case_id'] == 'PRINTDB15' and x['shared_physical_case'] for x in links))
        self.assertEqual({(x['typed_key']['kind'], x['typed_key']['name'])
                          for x in existing['trace_case_evidence']}, expected_roles)
        self.assertTrue(all(x['execution_scope'] == 'TWO_TYPED_ROLES_ONE_PHYSICAL_CASE_THREE_SAVED_MODES'
                            for x in existing['trace_case_evidence']))

        code, alias = cli('PARENT245_dead_hole')
        self.assertEqual(code, 0)
        link, = alias['selected_evidence_links']
        self.assertEqual(link['case_id'], 'ARGBOUND245_dead_hole')
        self.assertIn('PARENT245_dead_hole', link['historical_case_ids'])
        trace, = alias['trace_case_evidence']
        self.assertEqual(trace['registered_case_id'], 'ARGBOUND245_dead_hole')
        self.assertEqual(trace['acceptance_original'], 'WITHHELD_PRIVATE_SOURCE')
        self.assertIs(trace['target_runtime_entered'], False)

        for term in ('expression_function:STRLEN', 'NO_SUCH_CASE_99672'):
            with self.subTest(term=term):
                code, missing = cli(term)
                self.assertEqual(code, 1)
                self.assertEqual(missing['parent_restoration_40_availability'], 'AVAILABLE')
                self.assertEqual(missing['parent_restoration_40'], [])
                self.assertEqual(missing['selected_evidence_links'], [])
                self.assertEqual(missing['saved_observations'], [])


if __name__ == '__main__':
    unittest.main()
