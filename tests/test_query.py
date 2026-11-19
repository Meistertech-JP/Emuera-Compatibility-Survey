"""Check that indexed and pilot evidence remain distinguishable in lookup."""
import json
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class QueryTest(unittest.TestCase):
    def query(self, term):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/query.py'), term],
                                capture_output=True, text=True, encoding='utf-8')
        return result.returncode, json.loads(result.stdout)

    def test_saved_printdata_roles_do_not_imply_execution(self):
        code, result = self.query('structural_syntax:PRINTDATA')
        self.assertEqual(code, 0)
        rows = result['saved_observations']
        self.assertEqual(len(rows), 15)
        for row in rows:
            self.assertEqual(row['collection'], 'printdata_saved')
            self.assertEqual(row['matched_parent_roles'],
                             [{'kind': 'structural_syntax', 'name': 'PRINTDATA'}])
            self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')
            self.assertFalse(row['preparation_not_run_is_saved_run_status'])
            self.assertTrue((ROOT / row['record']['path']).is_file())

    def test_saved_observations_preserve_shared_batch(self):
        code, result = self.query('STRCOUNT')
        self.assertEqual(code, 0)
        rows = result['saved_observations']
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(row['collection'], 'observation_saved')
            self.assertEqual(row['shared_batch_case_count'], 3)
            self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')
            self.assertTrue((ROOT / row['record']['path']).is_file())

    def test_csv_numeric_keeps_unverified_and_natural_exit_unknown(self):
        code, result = self.query('CSVBASE')
        self.assertEqual(code, 0)
        rows = [r for r in result['saved_observations'] if r['collection'] == 'csv_numeric_saved']
        self.assertEqual(len(rows), 15)
        self.assertEqual(sum(r['recorded_verdict'] == 'unverified' for r in rows), 2)
        for row in rows:
            self.assertEqual(set(row['native_natural_exit_by_mode'].values()), {'not_observed'})
            self.assertEqual(row['parent_review_artifact'], 'not_included')
            self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')

    def test_unicode_shared_batch_does_not_imply_target_return(self):
        code, result = self.query('UCUNIT_20261116_ACTUAL_GATE_CHARATU_CMD')
        self.assertEqual(code, 0)
        row, = [r for r in result['saved_observations'] if r['collection'] == 'remaining_96_saved']
        self.assertEqual(row['fixture_id'], 'ACTUAL_GATE')
        self.assertEqual(row['shared_batch_case_count'], 6)
        self.assertEqual(row['target_return'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')
        self.assertEqual(set(row['native_natural_exit_by_mode'].values()),
                         {'not_established_from_receipt'})

    def test_selected_cases_keep_mode_specific_config(self):
        data = json.loads((ROOT / 'evidence/selected-51-20261117/index.json').read_text(encoding='utf-8'))
        case = next(c for c in data['cases'] if c['case_id'].endswith('_OFF_GUARD_20261115'))
        code, result = self.query(case['case_id'])
        self.assertEqual(code, 0)
        row, = [r for r in result['saved_observations'] if r['collection'] == 'selected_51_saved']
        self.assertEqual(row['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')
        for mode, inputs in row['inputs_by_mode'].items():
            config, = [item for item in inputs if item['relative_name'] == 'emuera.config']
            self.assertIn('/' + mode + '/inputs/emuera.config', config['record']['path'])
            self.assertTrue((ROOT / config['record']['path']).is_file())

    def test_native_source_index_preserves_static_limits(self):
        code, result = self.query('method_as_command:GETCHARA')
        self.assertEqual(code, 0)
        row, = result['native_source_static']
        self.assertEqual(row['row']['v24_same_name_function_dictionary']['scope'],
                         'same_name_function_dictionary_only_not_command_registration_or_routing')
        code, result = self.query('expression_function:CHKVARDATA')
        self.assertEqual(code, 0)
        row, = result['native_source_static']
        self.assertEqual(row['row']['v24_supplemental_commented_candidate']['scope'],
                         'commented_candidate_not_active_registration')
        code, result = self.query('expression_function:GCREATED')
        self.assertEqual(code, 0)
        row, = result['native_source_static']
        self.assertIn('mismatch_unresolved',
                      [item.get('declared_digest_vs_recorded_registration_text') for item in row['row']['v24_audit']])

    def test_operator_supplement_distinguishes_internal_set(self):
        code, result = self.query('operator:!|')
        self.assertEqual(code, 0)
        row, = result['native_source_operator30']
        self.assertEqual(row['row']['anchor_kind'], 'operator_dictionary_entry')
        self.assertEqual(row['row']['comment_discrepancy']['enum_comment_spelling'], '!^')
        self.assertEqual(row['row']['il_comparison']['source_build_identity'], 'not_established')
        code, result = self.query('command_or_syntax:SET')
        self.assertEqual(code, 0)
        row, = result['native_source_operator30']
        self.assertEqual(row['row']['anchor_kind'], 'internal_assignment_identifier')

    def test_registration_sha_supplement_is_typed_and_historical(self):
        code, result = self.query('expression_function:GCREATED')
        self.assertEqual(code, 0)
        row, = result['native_source_sha_supplement']
        self.assertTrue(row['supplement_row']['includes_comment'])
        self.assertTrue(row['supplement_row']['includes_cr'])
        self.assertFalse(row['supplement_row']['includes_lf'])
        self.assertIn('NOT_PROOF_OF_HISTORICAL_CODE_AUTHENTICITY',
                      result['native_source_sha_supplement_availability']['scope'])
        code, result = self.query('method_as_command:GCREATED')
        self.assertEqual(code, 0)
        self.assertEqual(result['native_source_sha_supplement'], [])

    def test_v24_anchor_supplement_distinguishes_assignment_and_operator(self):
        code, result = self.query('assignment_syntax:=')
        self.assertEqual(code, 0)
        row, = result['native_source_anchor82']
        self.assertEqual(row['row']['anchor_kind'], 'assignment_lexical_branch')
        self.assertIn('NO_OLD_SOURCE_IDENTITY_REGISTRATION_OR_EXECUTION_INFERENCE',
                      result['native_source_anchor82_availability']['scope'])
        code, result = self.query('operator:=')
        self.assertEqual(code, 0)
        self.assertEqual(result['native_source_anchor82'], [])

    def test_grammar_and_representative_evidence(self):
        code, result = self.query('COLON_NORMAL_COMPAT_RAND_YES')
        self.assertEqual(code, 0)
        self.assertEqual(len(result['cases']), 1)
        self.assertEqual(len(result['representative_evidence']), 1)

    def test_pilot_evidence_does_not_become_a_main_case(self):
        code, result = self.query('P38')
        self.assertEqual(code, 0)
        self.assertEqual(result['cases'], [])
        self.assertEqual(len(result['representative_evidence']), 1)

    def test_unknown_is_not_found(self):
        code, result = self.query('NO_SUCH_CASE_998877')
        self.assertEqual(code, 1)
        self.assertEqual(result['representative_evidence'], [])
        self.assertEqual(result['additional_evidence_discovery'], [])
        self.assertEqual(result['additional_evidence_discovery_availability']['index'], 'AVAILABLE')

    def test_legacy_and_current_ids_link_to_same_partial_evidence(self):
        for term in ('STRLEN', 'ARGBOUND246_strlen-control', 'PARENT246_strlen-control'):
            code, result = self.query(term)
            self.assertEqual(code, 0)
            links = [link for link in result['selected_evidence_links']
                     if link['case_id'] == 'ARGBOUND246_strlen-control']
            link, = links
            self.assertEqual(link['case_verdict'], 'matched_scoped')
            self.assertEqual(link['target_outcome'], 'documented_difference')
            self.assertTrue((ROOT / link['manifest']).is_file())

    def test_target_returns_separate_case_evidence(self):
        code, result = self.query('ADDCOPYCHARA')
        self.assertEqual(code, 0)
        links = result['selected_evidence_links']
        self.assertEqual(len(links), 8)
        self.assertEqual(len({link['case_id'] for link in links}), 8)
        for link in links:
            self.assertTrue((ROOT / link['record']).is_file())

    def test_neutral_batch_id_preserves_original_case_and_scope(self):
        code, result = self.query('CASE001')
        self.assertEqual(code, 0)
        link, = result['selected_evidence_links']
        self.assertEqual(link['case_id'], 'AUTO_V2_EXPR_001_ABS')
        self.assertEqual(link['target'], {'kind': 'expression_function', 'name': 'ABS'})

    def test_extra_cases_preserve_domain_and_manifest_relation(self):
        survey = json.loads((ROOT / 'results/survey.json').read_text(encoding='utf-8'))
        extra = json.loads((ROOT / 'results/extra-evidence-index.json').read_text(encoding='utf-8'))
        self.assertEqual(len(extra['entries']), 24)
        for entry in extra['entries']:
            source, = [r for r in survey[entry['domain']] if r['case_id'] == entry['case_id']]
            field = 'verdict' if entry['domain'] == 'grammar_cases' else 'scenario_verdict'
            self.assertEqual(source[field], entry['verdict'])
            manifest = json.loads((ROOT / entry['manifest']).read_text(encoding='utf-8'))
            value = manifest['cases'][int(entry['manifest_pointer'].rsplit('/', 1)[1])]
            self.assertEqual(value['case_id'], entry['case_id'])
            for field in ('readme_ja', 'readme_en'):
                self.assertTrue((ROOT / entry[field]).is_file())
        code, result = self.query('SUP_LABEL_AT_DUPLICATE_NO_20261115')
        self.assertEqual(code, 0)
        self.assertEqual(result['extra_evidence_links'][0]['domain'], 'supplemental_modes')

    def test_static_api_rows_preserve_typed_targets_and_scope(self):
        survey = json.loads((ROOT / 'results/survey.json').read_text(encoding='utf-8'))
        targets = {(r['kind'], r['name']): r for r in survey['targets']}
        static = json.loads((ROOT / 'evidence/api-gap75-static-20261117/records/targets.json').read_text(encoding='utf-8'))
        self.assertEqual(len(static['targets']), 75)
        self.assertEqual(sum(len(r['case_roles']) for r in static['targets']), 167)
        keys = [(r['target']['kind'], r['target']['name']) for r in static['targets']]
        self.assertEqual(len(set(keys)), len(keys))
        self.assertTrue(all(key in targets for key in keys))
        code, result = self.query('SPRITEMOVE')
        self.assertEqual(code, 0)
        self.assertEqual({r['target']['kind'] for r in result['static_api_evidence']},
                         {'expression_function', 'method_as_command'})

    def test_trace_exposes_requirements_and_private_source_limit(self):
        code, result = self.query('SET')
        self.assertEqual(code, 0)
        self.assertTrue(result['verification_requirements'])
        self.assertEqual(result['trace_targets'][0]['acceptance_original'], 'WITHHELD_PRIVATE_SOURCE')
        requirement = result['verification_requirements'][0]
        code, found = self.query(requirement['requirement_id'])
        self.assertEqual(code, 0)
        self.assertIn(requirement, found['verification_requirements'])

    def test_historical_acceptance_is_distinct_and_original_not_provided(self):
        layer = json.loads((ROOT / 'evidence/legacy-acceptance-269-20261117/layer.json').read_text(encoding='utf-8'))
        self.assertEqual(len(layer['targets']), 269)
        identified = [r for r in layer['targets'] if r['historical_classification'] == 'TYPED_SOURCE_IDENTIFIED']
        self.assertEqual(len(identified), 205)
        self.assertTrue(all(r['historical_source_access'] == 'ORIGINAL_NOT_PROVIDED_EXTERNAL_VERIFICATION_UNAVAILABLE'
                            for r in identified))
        code, result = self.query('PRINT')
        self.assertEqual(code, 0)
        self.assertTrue(result['historical_acceptance_references'])

    def test_selected_links_agree_with_survey_and_exist(self):
        index = json.loads((ROOT / 'results/evidence-index.json').read_text(encoding='utf-8'))
        survey = json.loads((ROOT / 'results/survey.json').read_text(encoding='utf-8'))
        targets = {(r['kind'], r['name']): r for r in survey['targets']}
        cases = {r['case_id']: r for r in survey['main_scenarios']}
        self.assertEqual(len(index['entries']), len({(r['case_id'], r['target']['kind'], r['target']['name'])
                                                     for r in index['entries']}))
        for entry in index['entries']:
            key = entry['target']
            target = targets[(key['kind'], key['name'])]
            case = cases[entry['case_id']]
            self.assertEqual(entry.get('acceptance_case_listed', True),
                             entry['case_id'] in target['case_ids'])
            self.assertIn(key, case['targets'])
            self.assertEqual(entry['case_verdict'], case['scenario_verdict'])
            self.assertEqual(entry['target_outcome'], target['comparison_outcome'])
            for field in ('manifest', 'readme_ja', 'readme_en'):
                self.assertTrue((ROOT / entry[field]).is_file(), entry[field])
            if 'manifest_pointer' in entry:
                value = json.loads((ROOT / entry['manifest']).read_text(encoding='utf-8'))
                for part in entry['manifest_pointer'].strip('/').split('/'):
                    value = value[part.replace('~1', '/').replace('~0', '~')]
                self.assertEqual(value['target'], key)
                self.assertEqual(value['case_id'], entry['case_id'])
            if 'record_pointer' in entry:
                values = json.loads((ROOT / entry['record']).read_text(encoding='utf-8'))
                value = values[int(entry['record_pointer'].lstrip('/'))]
                self.assertEqual(value['target'], key)
                self.assertEqual(value['case_id'], entry['case_id'])
                self.assertEqual(value['case_verdict'], entry['case_verdict'])
            if 'batch_record_pointer' in entry:
                value = json.loads((ROOT / entry['batch_record']).read_text(encoding='utf-8'))
                for part in entry['batch_record_pointer'].strip('/').split('/'):
                    value = value[int(part)] if isinstance(value, list) else value[part]
                self.assertEqual(value['typed_key'], key['kind'] + ':' + key['name'])
                self.assertEqual(value['case_id'], entry['neutral_case_id'])
                self.assertEqual(value['status'], entry['case_verdict'])
            if 'typed_record_pointer' in entry:
                values = json.loads((ROOT / entry['typed_record']).read_text(encoding='utf-8'))
                value = values[int(entry['typed_record_pointer'].lstrip('/'))]
                self.assertEqual(value['target'], key)

    def test_shared_physical_case_has_two_typed_roles(self):
        code, result = self.query('PRINTDB15')
        self.assertEqual(code, 0)
        links = result['selected_evidence_links']
        self.assertEqual(len(links), 2)
        self.assertEqual({r['target']['kind'] for r in links}, {'command_or_syntax', 'structural_syntax'})
        self.assertTrue(all(r['shared_physical_case'] for r in links))

    def test_operator_normal_cases_preserve_evidence_and_limits(self):
        folder = ROOT / 'evidence/operator-normal-6-20261117'
        binding = json.loads((folder / 'bindings.json').read_text(encoding='utf-8'))
        for i, case in enumerate(binding['cases']):
            with self.subTest(case=case['case_id']):
                code, result = self.query(case['case_id'])
                self.assertEqual(code, 0)
                self.assertEqual(result['saved_observation_availability']['operator_normal_6'], 'AVAILABLE')
                row, = [r for r in result['saved_observations'] if r['collection'] == 'operator_normal_6_saved']
                self.assertEqual(row['matched_case_roles'], case['typed_targets'])
                self.assertEqual(row['record']['pointer'], '/cases/'+str(i))
                self.assertEqual(row['binding_record']['pointer'], '/cases/'+str(i))
                self.assertEqual(row['source_register']['pointer'], case['case_register_pointer'])
                self.assertEqual(row['source_register']['availability'], 'ORIGINAL_REGISTER_NOT_INCLUDED')
                self.assertEqual(row['public_stdin'], 'INHERITED_CONTENT_NOT_RECORDED')
                self.assertEqual(row['native_input'], 'SEPARATE_GUI_DESKTOP_NO_SYNTHETIC_KEYS_RECORDED')
                self.assertEqual(set(row['native_natural_exit_by_mode'].values()), {'NOT_OBSERVED_CLEANUP_RECORDED'})
                self.assertEqual(row['complete_condition_equivalence'], 'NOT_ESTABLISHED')
                self.assertEqual(row['historical_public_build_identity'], 'NOT_ESTABLISHED')
                self.assertIsNone(row['recorded_verdict'])
                self.assertEqual(row['selected_marker_count'], len(case['selected_normal_markers']))
                self.assertIn('native_natural_exit', row['unobserved'])
                self.assertNotIn(str(ROOT).lower(), json.dumps(row).lower())
                for asset in (row['inputs']['fixture'], row['inputs']['config'],
                              row['outputs_by_mode']['public-refresh']['stdout'],
                              row['outputs_by_mode']['public-refresh']['stderr'],
                              row['outputs_by_mode']['native-01']['raw'],
                              row['outputs_by_mode']['native-02']['raw']):
                    self.assertTrue((ROOT / asset['record']['path']).is_file())

    def test_operator_normal_typed_target_lookup_and_kind_filter(self):
        folder = ROOT / 'evidence/operator-normal-6-20261117'
        binding = json.loads((folder / 'bindings.json').read_text(encoding='utf-8'))
        spec = importlib.util.spec_from_file_location('query_operator_test', ROOT / 'tools/query.py')
        query = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(query)
        for case in binding['cases']:
            for target in case['typed_targets']:
                rows, state = query._operator_normal_6(target['name'].upper(), ROOT, target['kind'].upper())
                self.assertEqual(state, 'AVAILABLE')
                self.assertEqual([r['case_id'] for r in rows], [case['case_id']])
                self.assertEqual(rows[0]['matched_case_roles'], [target])
        code, result = self.query('operator:+')
        self.assertEqual(code, 0)
        self.assertEqual([r['case_id'] for r in result['saved_observations']
                          if r['collection'] == 'operator_normal_6_saved'], ['OPNORMAL273_E143'])
        rows, _ = query._operator_normal_6('+', ROOT, 'ASSIGNMENT_SYNTAX')
        self.assertEqual(rows, [])

    def test_operator_normal_missing_or_forged_bindings_fail_closed(self):
        spec = importlib.util.spec_from_file_location('query_operator_negative', ROOT / 'tools/query.py')
        query = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(query)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(query._operator_normal_6('+', root, 'OPERATOR'), ([], 'NOT_INSTALLED'))
            folder = root / 'evidence/operator-normal-6-20261117'
            folder.parent.mkdir(parents=True)
            shutil.copytree(ROOT / 'evidence/operator-normal-6-20261117', folder)
            index_path = folder / 'index.json'
            original = index_path.read_bytes()
            for attack in ('pointer', 'marker', 'fixture'):
                doc = json.loads(original)
                by_id = {c['case_id']: c for c in doc['cases']}
                a, b = by_id['OPNORMAL273_E143'], by_id['OPNORMAL273_E145']
                if attack == 'pointer':
                    a['case_register_pointer'], b['case_register_pointer'] = b['case_register_pointer'], a['case_register_pointer']
                elif attack == 'marker':
                    markers = a['selected_normal_markers']
                    markers[markers.index('AR21 VALUE=5 COUNT=1 ORDER=1')] = 'AR20 VALUE=15 COUNT=2 ORDER=12'
                else:
                    p, q = folder / a['inputs']['fixture']['path'], folder / b['inputs']['fixture']['path']
                    before_p, before_q = p.read_bytes(), q.read_bytes()
                    p.write_bytes(before_q); q.write_bytes(before_p)
                    for case, raw in ((a, before_q), (b, before_p)):
                        case['inputs']['fixture']['sha256'] = hashlib.sha256(raw).hexdigest()
                        case['inputs']['fixture']['bytes'] = len(raw)
                index_path.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
                with self.subTest(attack=attack), self.assertRaises(ValueError):
                    query._operator_normal_6('+', root, 'OPERATOR')
                if attack == 'fixture':
                    p.write_bytes(before_p); q.write_bytes(before_q)
                index_path.write_bytes(original)
            bindings_path = folder / 'bindings.json'
            bindings_path.write_bytes(bindings_path.read_bytes()+b' ')
            with self.assertRaises(ValueError):
                query._operator_normal_6('+', root, 'OPERATOR')
    def test_method_display_cases_preserve_shared_batch_and_limits(self):
        folder = ROOT / 'evidence/method-display-state-15-20261117'
        index = json.loads((folder / 'index.json').read_text(encoding='utf-8'))
        for i, case in enumerate(index['cases']):
            with self.subTest(case=case['case_id']):
                code, result = self.query(case['case_id'])
                self.assertEqual(code, 0)
                self.assertEqual(result['saved_observation_availability']['method_display_state_15'], 'AVAILABLE')
                row, = [r for r in result['saved_observations'] if r['collection'] == 'method_display_state_15_saved']
                self.assertEqual(row['matched_case_roles'], [case['typed_target']])
                self.assertEqual(row['record']['pointer'], '/cases/'+str(i))
                self.assertEqual(row['condition_markers'], case['condition_markers'])
                for marker, ref in zip(row['condition_markers'], row['condition_records']):
                    self.assertEqual(index['conditions'][int(ref['pointer'].rsplit('/', 1)[1])]['marker'], marker)
                self.assertEqual(row['recorded_verdict'], 'matched_scoped')
                self.assertEqual(row['verdict_scope'], 'HISTORICAL_CASE_SCOPED_NOT_NEW_TARGET_ACCEPTANCE')
                self.assertEqual(row['sharing_scope'], 'ONE_RECORDED_BATCH_NOT_15_INDEPENDENT_CASE_RUNS')
                self.assertEqual(row['public_pyz_sha_scope'], 'COMPARISON_DECLARED_EXECUTION_TIME_BEFORE_AFTER_NOT_ESTABLISHED')
                self.assertEqual(set(row['native_natural_exit_by_mode'].values()), {'NOT_OBSERVED_CLEANUP_RECORDED'})
                self.assertEqual(row['reseal_limit'], 'NEW_MANIFEST_OR_INDEX_PIN_DOES_NOT_PROVE_ORIGINAL_SOURCE_AGREEMENT')
                self.assertEqual(row['source_materials'], 'ORIGINAL_REGISTER_COMPARISON_CONDITIONS_REVIEW_NOT_INCLUDED')
                self.assertIn('gui_rendering', row['target_unobserved'])
                self.assertNotIn(str(ROOT).lower(), json.dumps(row).lower())
                for name, mode in row['mode_references'].items():
                    self.assertEqual(index['modes'][int(mode['mode_record']['pointer'].rsplit('/', 1)[1])]['mode'], name)
                    for field in ('fixture', 'config', 'history'):
                        self.assertTrue((ROOT / mode[field]['record']['path']).is_file())

    def test_method_display_typed_targets_and_kind_filter(self):
        folder = ROOT / 'evidence/method-display-state-15-20261117'
        index = json.loads((folder / 'index.json').read_text(encoding='utf-8'))
        spec = importlib.util.spec_from_file_location('query_method_display_test', ROOT / 'tools/query.py')
        query = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(query)
        for case in index['cases']:
            target = case['typed_target']
            rows, state = query._method_display_state_15(target['name'].upper(), ROOT, target['kind'].upper())
            self.assertEqual(state, 'AVAILABLE')
            self.assertEqual([r['case_id'] for r in rows], [case['case_id']])
            self.assertEqual(rows[0]['matched_case_roles'], [target])
        code, result = self.query('method_as_command:GETCOLOR')
        self.assertEqual(code, 0)
        self.assertEqual([r['case_id'] for r in result['saved_observations']
                          if r['collection'] == 'method_display_state_15_saved'], ['DISPLAYSTATE_GETCOLOR'])
        rows, _ = query._method_display_state_15('GETCOLOR', ROOT, 'EXPRESSION_FUNCTION')
        self.assertEqual(rows, [])

    def test_method_display_missing_and_changed_snapshot_are_rejected(self):
        spec = importlib.util.spec_from_file_location('query_method_display_negative', ROOT / 'tools/query.py')
        query = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(query)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(query._method_display_state_15('GETCOLOR', root, 'METHOD_AS_COMMAND'), ([], 'NOT_INSTALLED'))
            folder = root / 'evidence/method-display-state-15-20261117'
            folder.parent.mkdir(parents=True)
            shutil.copytree(ROOT / 'evidence/method-display-state-15-20261117', folder)
            raw = folder / 'modes/native-01/raw-history.bin'
            original_raw = raw.read_bytes()
            raw.write_bytes(original_raw+b'X')
            with self.assertRaises(ValueError):
                query._method_display_state_15('GETCOLOR', root, 'METHOD_AS_COMMAND')
            raw.write_bytes(original_raw)
            index = folder / 'index.json'
            doc = json.loads(index.read_bytes())
            doc['cases'][0]['recorded_verdict'] = 'unverified'
            index.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            manifest = folder / 'manifest.json'
            manifest.unlink()
            result = subprocess.run([sys.executable, '-I', '-B', str(folder / 'tools/file_set_manifest.py'),
                                     'create', '--manifest', str(manifest), '--root', 'evidence='+str(folder)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            with self.assertRaises(ValueError):
                query._method_display_state_15('GETCOLOR', root, 'METHOD_AS_COMMAND')


if __name__ == '__main__':
    unittest.main()
