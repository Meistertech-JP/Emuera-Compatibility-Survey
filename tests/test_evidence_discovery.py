"""Check additional discovery links without treating them as replay evidence."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('discovery_query', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(query)


class EvidenceDiscoveryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='evidence-discovery-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        index_path = ROOT / query._DISCOVERY_INDEX
        self.index = json.loads(index_path.read_bytes())
        (self.root / query._DISCOVERY_INDEX).parent.mkdir(parents=True)
        shutil.copyfile(index_path, self.root / query._DISCOVERY_INDEX)
        for group in self.index['groups'].values():
            for ref in (group['records'], *group['readmes']):
                path = self.root / ref['path']
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / ref['path'], path)

    def find(self, term, kind=None):
        return query.additional_evidence_discovery(term, self.root, kind)

    def test_all_case_and_typed_role_lookups_and_scopes(self):
        original = [e for e in self.index['entries'] if e['collection'] in ('platform_input_16', 'compound_assignment_10')]
        self.assertEqual(len(original), 26)
        roles = set()
        for entry in original:
            with self.subTest(case=entry['case_id']):
                row, = self.find(entry['case_id'])[0]
                self.assertEqual(row['typed_target'], entry['typed_target'])
                self.assertEqual(row['record']['pointer'], entry['record_pointer'])
                self.assertEqual(row['record']['location'], 'CANDIDATE_RELATIVE')
                self.assertEqual(len(row['readmes']), 2)
                self.assertTrue(all((self.root / r['path']).is_file() for r in row['readmes']))
                self.assertTrue(any('Original receipts are not included.' == x for x in row['scope_limits']))
                self.assertEqual(row['scope'], 'DISCOVERY_ONLY_NOT_ORIGINAL_EXECUTION_OR_RIGHTS_VERIFICATION')
                t = entry['typed_target']
                roles.add((t['kind'], t['name']))
                matches, state = self.find(t['kind'] + ':' + t['name'])
                self.assertTrue(any(r['case_id'] == entry['case_id'] for r in matches))
                self.assertTrue(all(v == 'AVAILABLE' for v in state['groups'].values()))
        self.assertEqual(len(roles), 22)
        platform = [self.find(e['case_id'])[0][0] for e in self.index['entries'] if e['collection'] == 'platform_input_16']
        self.assertEqual(sum(r['details']['scenario_verdict'] == 'unverified' for r in platform), 7)
        self.assertEqual(sum(r['details']['comparison_verdict'] == 'unverified_environment' for r in platform), 7)
        self.assertTrue(all('unverified' in r['details'] for r in platform))
        self.assertTrue(all(any('fixture/config execution-time before/after SHA fields' in x and 'executable hashes are a separate matter' in x for x in r['scope_limits']) for r in platform))
        compound = [self.find(e['case_id'])[0][0] for e in self.index['entries'] if e['collection'] == 'compound_assignment_10']
        self.assertEqual(len(compound), 10)
        for row in compound:
            self.assertEqual(row['details']['execution'], 'shared_batch_not_independent_case_execution')
            self.assertTrue(any('before/after input SHA was not recorded' in x for x in row['scope_limits']))
            self.assertTrue(any('not ten independent' in x for x in row['scope_limits']))
            self.assertTrue(any('original receipt' in x.lower() for x in row['scope_limits']))
            self.assertTrue(any('fixture/config before/after SHA values' in x and 'executable hashes are separate' in x for x in row['scope_limits']))

    def test_kind_and_case_filter_are_not_collapsed(self):
        self.assertEqual(len(self.find('expression_function:GETKEY')[0]), 3)
        self.assertEqual(len(self.find('method_as_command:GETKEY')[0]), 1)
        self.assertEqual(len(self.find('assignment_syntax:+=')[0]), 1)
        self.assertEqual(self.find('operator:+=')[0], [])
        case = 'UIQUERY237_getkey_expr_normal'
        self.assertEqual(len(self.find(case, 'expression_function')[0]), 1)
        self.assertEqual(self.find(case, 'method_as_command')[0], [])
        with self.assertRaisesRegex(ValueError, 'conflicting typed kind'):
            self.find('expression_function:GETKEY', 'method_as_command')

    def test_index_absent_and_bad_pin_are_explicit(self):
        p = self.root / query._DISCOVERY_INDEX
        original = p.read_bytes()
        canonical = original.replace(b'\r\n', b'\n')
        for contents in (canonical, canonical.replace(b'\n', b'\r\n')):
            p.write_bytes(contents)
            self.assertEqual(self.find('GETKEY')[1]['index'], 'AVAILABLE')
        p.unlink()
        self.assertEqual(self.find('GETKEY'), ([], {'index': 'NOT_INSTALLED', 'groups': {}, 'files': {}}))
        p.write_bytes(original + b' ')
        self.assertEqual(self.find('GETKEY')[1]['index'], 'SNAPSHOT_MISMATCH')
        # Updating source and rewriting the index cannot replace the query's external pin.
        changed = json.loads(original)
        changed['groups']['platform_input_16']['scope_limits'] = []
        p.write_text(json.dumps(changed), encoding='utf-8')
        self.assertEqual(self.find('GETKEY')[1]['index'], 'SNAPSHOT_MISMATCH')

    def test_each_required_document_missing_and_changed_are_explicit(self):
        for group_name, group in self.index['groups'].items():
            other = next(name for name in self.index['groups'] if name != group_name)
            for ref in (group['records'], *group['readmes']):
                path = self.root / ref['path']
                original = path.read_bytes()
                with self.subTest(group=group_name, file=ref['path'], failure='missing'):
                    path.unlink()
                    rows, state = self.find('GETKEY')
                    self.assertEqual(state['groups'][group_name], 'MISSING_FILES')
                    self.assertEqual(state['files'][group_name], [ref['path']])
                    self.assertEqual(state['groups'][other], 'AVAILABLE')
                    self.assertFalse(any(r['collection'] == group_name for r in rows))
                    path.write_bytes(original)
                with self.subTest(group=group_name, file=ref['path'], failure='sha'):
                    path.write_bytes(original + b' ')
                    rows, state = self.find('GETKEY')
                    self.assertEqual(state['groups'][group_name], 'SNAPSHOT_MISMATCH')
                    self.assertEqual(state['files'][group_name], [ref['path']])
                    self.assertEqual(state['groups'][other], 'AVAILABLE')
                    self.assertFalse(any(r['collection'] == group_name for r in rows))
                    path.write_bytes(original)

    def test_repin_attempt_and_pointer_mismatch_are_rejected(self):
        index_path = self.root / query._DISCOVERY_INDEX
        original = index_path.read_bytes()
        index = json.loads(original)
        index['entries'][0]['role_pointer'] = '/cases/1/typed_targets/0'
        index_path.write_text(json.dumps(index), encoding='utf-8')
        self.assertEqual(self.find('GETKEY')[1]['index'], 'SNAPSHOT_MISMATCH')
        # Exercise the identity guard independently of the outer pin.
        new_digest = hashlib.sha256(index_path.read_bytes()).hexdigest()
        with patch.object(query, '_DISCOVERY_INDEX_SHA256', new_digest):
            rows, state = self.find('GETKEY')
            self.assertEqual(state['groups']['platform_input_16'], 'INVALID_DATA')
            self.assertEqual(state['groups']['compound_assignment_10'], 'AVAILABLE')
            self.assertEqual(rows, [])

    def test_cli_exposes_discovery_and_preserves_existing_alias_and_limits(self):
        def cli(term):
            run = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/query.py'), term],
                                 capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.stderr, '')
            return run.returncode, json.loads(run.stdout)
        code, result = cli('expression_function:GETKEY')
        self.assertEqual(code, 0)
        self.assertEqual(len(result['additional_evidence_discovery']), 3)
        self.assertTrue(all(r['details']['scenario_verdict'] == 'unverified'
                            for r in result['additional_evidence_discovery']))
        self.assertTrue(all(r['details']['comparison_verdict'] == 'unverified_environment'
                            for r in result['additional_evidence_discovery']))
        code, result = cli('assignment_syntax:+=')
        self.assertEqual(code, 0)
        row, = result['additional_evidence_discovery']
        self.assertEqual(row['details']['execution'], 'shared_batch_not_independent_case_execution')
        self.assertTrue(any('before/after input SHA was not recorded' in x for x in row['scope_limits']))
        code, result = cli('PARENT245_dead_hole')
        self.assertEqual(code, 0)
        self.assertEqual(result['selected_evidence_links'][0]['case_id'], 'ARGBOUND245_dead_hole')
        self.assertEqual(result['trace_case_evidence'][0]['acceptance_original'], 'WITHHELD_PRIVATE_SOURCE')
        code, result = cli('command_or_syntax:FONTSTYLE')
        self.assertEqual(code, 0)
        self.assertEqual(result['parent_restoration_40'][0]['historical_restoration_outcome'], 'documented_difference')
        self.assertEqual(result['parent_restoration_40'][0]['later_ledger_outcome'], 'different_scoped')
        code, result = cli('PRINTNORMAL240_PRINTDW')
        self.assertEqual(code, 0)
        row, = [r for r in result['additional_evidence_discovery'] if r['collection'] == 'multi_group_second_72']
        self.assertIn('eight empty lines supplied at process start', row['recorded_case_scope']['public_logical_input'])
        self.assertEqual(row['collection_references']['withheld_groups']['pointer'], '/withheld_groups')
        code, result = cli('NESTEDSELECT01')
        self.assertEqual(code, 0)
        selected = [r for r in result['additional_evidence_discovery'] if r['collection'] == 'multi_group_101']
        self.assertEqual(len(selected), 8)
        self.assertTrue(all(r['recorded_case_scope']['caseelse_selected'] is False for r in selected))
        self.assertTrue(all('supplemental SELECTNEST01' in r['batch_scope'] for r in selected))
        for term in ('method_as_command:LINEISEMPTY', 'LINEBUF20261115_button_method'):
            code, result = cli(term)
            self.assertEqual(code, 0)
            row, = [r for r in result['additional_evidence_discovery'] if r['collection'] == 'lineisempty_acceptance']
            self.assertEqual(len(row['details']['acceptance_pin_discrepancy']['old_vs_retained']), 3)
            self.assertFalse(row['details']['original_parent_decision']['original_acceptance_included'])


    def test_all_101_cases_and_typed_roles_keep_batch_context(self):
        entries = [e for e in self.index['entries'] if e['collection'] == 'multi_group_101']
        self.assertEqual(len(entries), 126)
        self.assertEqual(len({e['case_id'] for e in entries}), 101)
        self.assertEqual(len({(e['typed_target']['kind'], e['typed_target']['name']) for e in entries}), 65)
        for entry in entries:
            with self.subTest(case=entry['case_id'], role=entry['typed_target']):
                case_hits, state = self.find(entry['case_id'])
                matching = [r for r in case_hits if r['collection'] == 'multi_group_101'
                            and r['typed_target'] == entry['typed_target']]
                row, = matching
                self.assertEqual(row['record']['pointer'], entry['record_pointer'])
                self.assertEqual(row['batch_record']['pointer'], entry['batch_pointer'])
                self.assertIn('batch_scope', row)
                self.assertGreaterEqual(row['shared_batch_case_count'], 1)
                self.assertTrue(any('histories are unavailable' in x and 'stdout' in x for x in row['scope_limits']))
                self.assertTrue(any('Original receipts' in x for x in row['scope_limits']))
                t = entry['typed_target']
                hits, _ = self.find(t['kind'] + ':' + t['name'])
                self.assertTrue(any(r['case_id'] == entry['case_id'] and r['collection'] == 'multi_group_101'
                                    for r in hits))
                self.assertEqual(state['groups']['multi_group_101'], 'AVAILABLE')
        doc = json.loads((self.root / self.index['groups']['multi_group_101']['records']['path']).read_bytes())
        withheld = sum(1 for b in doc['batches'] for m in b['modes'] for a in m['assets']
                       if a.get('role') == 'history' and a.get('status') == 'withheld')
        self.assertEqual(withheld, 14)
        batch = next(b for b in doc['batches'] if any(a.get('role') == 'history' and a.get('status') == 'withheld'
                     for m in b['modes'] for a in m['assets']))
        hit = next(r for r in self.find(batch['cases'][0]['case_id'])[0] if r['collection'] == 'multi_group_101')
        self.assertTrue(hit['withheld_history_modes'])
        self.assertEqual(hit['withheld_history_modes'][0]['reason'], 'not_present_in_saved_source')
        selected = [r for r in self.find('NESTEDSELECT01')[0] if r['collection'] == 'multi_group_101']
        self.assertEqual(len(selected), 8)
        self.assertTrue(all(r['recorded_case_scope']['caseelse_selected'] is False for r in selected))
        self.assertTrue(all('supplemental SELECTNEST01' in r['batch_scope'] and 'CASEELSE was not selected' in r['batch_scope'] for r in selected))
        self.assertTrue(all(any('original fixture' in x and 'screenshot' in x for x in r['scope_limits']) for r in selected))
        stopped = next(r for r in self.find('GRAPHICS233_gfillrectangle-expr-missing')[0] if r['collection'] == 'multi_group_101')
        self.assertIs(stopped['recorded_case_scope']['public_target_body_executed'], False)

    def test_lineisempty_separates_discrepancy_and_expression_form(self):
        rows, state = self.find('method_as_command:LINEISEMPTY')
        row, = [r for r in rows if r['collection'] == 'lineisempty_acceptance']
        self.assertEqual(state['groups']['lineisempty_acceptance'], 'AVAILABLE')
        self.assertEqual(row['case_id'], 'LINEBUF20261115_button_method')
        self.assertEqual(row['record']['pointer'], '')
        self.assertEqual(row['details']['publication_status'], 'PRIVATE_STAGING_REVIEW_REQUIRED')
        self.assertFalse(row['details']['original_parent_decision']['original_acceptance_included'])
        discrepancy = row['details']['acceptance_pin_discrepancy']
        self.assertEqual(len(discrepancy['old_vs_retained']), 3)
        self.assertTrue(all(not pin['bytes_equal'] and pin['old_bytes'] == 'NOT_FOUND_IN_CHECKED_INVENTORIES'
                            for pin in discrepancy['old_vs_retained']))
        self.assertFalse(discrepancy['readback_flag_consistent_with_three_old_pins'])
        self.assertTrue(any('Three individual old acceptance pins disagree' in x for x in row['scope_limits']))
        self.assertTrue(any('Original acceptance and session text are not included' in x for x in row['scope_limits']))
        self.assertTrue(any('Only native-01, native-02 and public-01' in x for x in row['scope_limits']))
        self.assertTrue(any('distinct expression-form' in x for x in row['scope_limits']))
        case_rows, _ = self.find('LINEBUF20261115_button_method')
        self.assertTrue(any(r['collection'] == 'lineisempty_acceptance' for r in case_rows))
        self.assertFalse(any(r['collection'] == 'lineisempty_acceptance' for r in self.find('expression_function:LINEISEMPTY')[0]))
        source = json.loads((self.root / row['record']['path']).read_bytes())
        self.assertEqual([m['mode'] for m in source['modes']], ['native-01', 'native-02', 'public-01'])
        ref = source['original_parent_decision']['acceptance_projection']
        path = (self.root / row['record']['path']).parent / ref['path']
        # This optional file is copied for this targeted readback, not consumed by the locator.
        path.write_bytes((ROOT / row['record']['path']).parent.joinpath(ref['path']).read_bytes())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), ref['sha256'])
        self.assertEqual(path.stat().st_size, ref['size'])

    def test_all_second_72_cases_and_typed_roles_keep_limits(self):
        entries = [e for e in self.index['entries'] if e['collection'] == 'multi_group_second_72']
        self.assertEqual(len(entries), 72)
        self.assertEqual(len({e['case_id'] for e in entries}), 72)
        self.assertEqual(len({(e['typed_target']['kind'], e['typed_target']['name']) for e in entries}), 36)
        hits_by_case = []
        for entry in entries:
            with self.subTest(case=entry['case_id']):
                hits, state = self.find(entry['case_id'])
                row, = [r for r in hits if r['collection'] == 'multi_group_second_72'
                        and r['typed_target'] == entry['typed_target']]
                hits_by_case.append(row)
                self.assertEqual(row['record']['pointer'], entry['record_pointer'])
                self.assertEqual(row['batch_record']['pointer'], entry['batch_pointer'])
                self.assertTrue(any('histories are unavailable' in x and 'stdout' in x for x in row['scope_limits']))
                self.assertTrue(any('Two other candidate groups are withheld' in x for x in row['scope_limits']))
                ref = row['collection_references']['withheld_groups']
                self.assertEqual(ref['pointer'], '/withheld_groups')
                self.assertEqual(state['references']['multi_group_second_72']['withheld_groups'], ref)
                target = entry['typed_target']
                typed, _ = self.find(target['kind'] + ':' + target['name'])
                self.assertTrue(any(r['case_id'] == entry['case_id'] and r['collection'] == 'multi_group_second_72' for r in typed))
        self.assertEqual(sum(r['details']['verdict'] == 'unverified' for r in hits_by_case), 20)
        doc = json.loads((self.root / self.index['groups']['multi_group_second_72']['records']['path']).read_bytes())
        withheld = [(m['mode'], a['reason']) for b in doc['batches'] for m in b['modes'] for a in m['assets']
                    if a.get('role') == 'history' and a.get('status') == 'withheld']
        self.assertEqual(len(withheld), 19)
        self.assertTrue(all(reason == 'not_present_in_saved_source' for _, reason in withheld))
        self.assertEqual(len(doc['withheld_groups']), 2)
        self.assertTrue(all(group['reason'] for group in doc['withheld_groups']))
        wait = next(r for r in self.find('PRINTNORMAL240_PRINTDW')[0] if r['collection'] == 'multi_group_second_72')
        self.assertTrue(wait['recorded_case_scope']['native_wait_and_return_recorded'])
        self.assertIn('eight empty lines supplied at process start', wait['recorded_case_scope']['public_logical_input'])
        self.assertIn('Native targeted Return after each wait', wait['batch_scope'])
        self.assertIn('timing and GUI pixels not compared', wait['batch_scope'])
        self.assertTrue(any('UI event records are not included' in x for x in wait['scope_limits']))
        absent, state = self.find('NO_SUCH_CASE_99672')
        self.assertEqual(absent, [])
        self.assertEqual(state['references']['multi_group_second_72']['withheld_groups']['pointer'], '/withheld_groups')

    def test_bad_batch_pointer_invalidates_only_its_group(self):
        p = self.root / query._DISCOVERY_INDEX
        index = json.loads(p.read_bytes())
        entry = next(e for e in index['entries'] if e['collection'] == 'multi_group_101')
        entry['batch_pointer'] = '/batches/1'
        p.write_text(json.dumps(index), encoding='utf-8')
        self.assertEqual(self.find(entry['case_id'])[1]['index'], 'SNAPSHOT_MISMATCH')
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        with patch.object(query, '_DISCOVERY_INDEX_SHA256', digest):
            rows, state = self.find(entry['case_id'])
            self.assertEqual(state['groups']['multi_group_101'], 'INVALID_DATA')
            self.assertEqual(state['groups']['platform_input_16'], 'AVAILABLE')
            self.assertFalse(any(r['collection'] == 'multi_group_101' for r in rows))


if __name__ == '__main__':
    unittest.main()
