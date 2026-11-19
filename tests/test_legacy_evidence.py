"""Synthetic, anonymous fixtures for explicitly supported evidence layouts."""
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
TOOL = HERE.parent/'tools/legacy_evidence.py'
spec = importlib.util.spec_from_file_location('legacy_evidence', TOOL)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def h(data):
    return hashlib.sha256(data).hexdigest()


class SyntheticLayouts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='legacy-adapter-',dir=HERE)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = {'kind':'command_or_syntax','name':'CASE_X'}

    def write(self, path, value):
        file = self.root/path
        file.parent.mkdir(parents=True,exist_ok=True)
        data = value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False)+'\n').encode('utf8')
        file.write_bytes(data)
        return h(data)

    def audit(self, acceptance_path, acceptance_sha, schema, readbacks, gaps=None, outcome='matched_in_finite_scope'):
        row = {'target':self.target,'row_outcome':outcome,'gaps':gaps if gaps is not None else [{'code':'LEGACY_ADAPTER_REQUIRED'}],
               'errors':[],'acceptance':{'path':acceptance_path,'sha256':acceptance_sha,
                        'record_pointer':'','schema':schema},
               'readbacks':readbacks,'case_role_links':[{'case_id':'ANON_1','registered_typed_target_matches':True}]}
        audit={'schema':adapter.AUDIT_SCHEMA,'rows':[row]}
        pin=self.write('audit.json',audit)
        return audit,pin

    def inspect_evidence(self, pin):
        return adapter.adapt(self.root,'audit.json',pin,'command_or_syntax','CASE_X')

    def print_layout(self):
        fixture_sha=self.write('fixtures/case.erb',b'@SYSTEM_TITLE\r\n')
        config_sha=h(b'synthetic config')
        runs={}
        for mode in ['native-final-01','native-final-02','public-receipted-01','public-receipted-02']:
            logname='emuera.log' if mode.startswith('native') else 'outputlog.bin'
            data=('synthetic output '+mode).encode()
            self.write(f'comparison/{mode}/{logname}',data)
            self.write(f'comparison/{mode}/emuera.config',b'synthetic config')
            runs[mode]={'receipt':mode+'/receipt.json','fixture_sha256_before_after':fixture_sha,
                        'outputlog_sha256':h(data),
                        ('config_sha256' if mode.startswith('native') else 'config_sha256_before_after'):config_sha}
        comp={'schema':'native-public-command-comparison-1','target':self.target,'case_ids':['ANON_1'],
              'scoped_outcome':'matched_in_finite_scope','fixture':{'path':'fixtures/case.erb',
              'sha256':fixture_sha,'config_sha256':config_sha},'runs':runs}
        comp_sha=self.write('comparison/COMPARISON.json',comp)
        acc={'schema':'parent-target-finite-scope-adjudication-1','target':self.target,
             'decision':'necessary_comparison_complete','comparison_outcome':'matched_in_finite_scope',
             'comparison_path':'comparison/COMPARISON.json','comparison_sha256':comp_sha}
        acc_sha=self.write('acceptance.json',acc)
        return self.audit('acceptance.json',acc_sha,acc['schema'],[])

    def phase2_layout(self, readback_kind):
        acc={'schema':'phase2-target-parent-acceptance/v1','target':self.target,'accepted':True,'case_ids':['ANON_1']}
        apin=self.write('record/acceptance.json',acc)
        if readback_kind=='explicit':
            rb={'schema':'parent-acceptance-readback-1','target':self.target,'case_ids':['ANON_1'],
                'acceptance_sha256':apin,'comparison_outcome':'different_scoped'}
            outcome='different_scoped'
        else:
            rb={'valid':True,'acceptance_sha256':apin,'case_ids_registered_for_exact_target':['ANON_1'],
                'native_replicates':2,'public_replicates':2}
            outcome='matched_in_finite_scope'
        pin=self.write('record/readback.json',rb)
        return self.audit('record\\acceptance.json',apin,acc['schema'],
                          [{'path':'record\\readback.json','sha256':pin}],outcome=outcome)

    def current_layout(self):
        run=[]
        for mode in ['native-01','native-02','public-01']:
            entry={'mode':mode}
            for role in ['raw','stderr','receipt','probe']:
                if role=='probe' and mode.startswith('public'):
                    entry[role]=None
                    continue
                path=f'artifacts/{mode}/{role}.bin'
                entry[role]={'path':path,'sha256':self.write(path,(mode+role).encode())}
            run.append(entry)
        rb={'observations':[{'case_id':'ANON_1','targets':['CASE_X'],'runs':run}]}
        rsha=self.write('readback.json',rb)
        ref={'path':'readback.json','sha256':rsha}
        acc={'schema':'original-return-three-parent-acceptance-1','target':self.target,
             'decision':'necessary_comparison_complete','comparison_outcome':'matched_in_finite_scope',
             'case_ids':['ANON_1'],'readback':ref}
        apin=self.write('acceptance.json',acc)
        return self.audit('acceptance.json',apin,acc['schema'],[ref],gaps=[])

    def test_comparison_layout_hashes_modes_but_receipts_remain_unpinned(self):
        _,pin=self.print_layout(); result=self.inspect_evidence(pin)
        self.assertEqual(result['status'],'PARTIAL')
        self.assertEqual(len(result['modes']),4)
        self.assertTrue(all(m['receipt']=='unpinned' for m in result['modes']))
        self.assertEqual(result['gaps'][0]['code'],'LEGACY_ADAPTER_REQUIRED')

    def test_phase2_schema_and_untyped_backlink(self):
        _,pin=self.phase2_layout('hash'); result=self.inspect_evidence(pin)
        self.assertEqual(result['status'],'PARTIAL')
        self.assertIsNone(result['declared_outcome'])
        self.assertEqual([x['recorded_replicates'] for x in result['modes']],[2,2])
        self.assertTrue(all(x['individual_raw_pins']=='not provided here' for x in result['modes']))

    def test_phase2_explicit_target_and_outcome(self):
        _,pin=self.phase2_layout('explicit'); result=self.inspect_evidence(pin)
        self.assertEqual(result['status'],'PARTIAL')
        self.assertEqual(result['source_outcome'],'different_scoped')
        self.assertEqual(result['declared_outcome'],'different_scoped')
        self.assertEqual(result['modes'],[])

    def test_current_normalized_layout_reads_declared_mode_files(self):
        _,pin=self.current_layout(); result=self.inspect_evidence(pin)
        self.assertEqual(result['status'],'PARTIAL')
        self.assertEqual([x['name'] for x in result['modes']],['native-01','native-02','public-01'])
        self.assertEqual(len(result['checked']),14)

    def test_wrong_and_missing_hash_or_missing_file_rejected(self):
        _,pin=self.print_layout()
        with self.assertRaisesRegex(adapter.EvidenceError,'hash mismatch'):
            self.inspect_evidence('0'*64)
        f=self.root/'comparison/native-final-01/emuera.log'; f.write_bytes(b'changed')
        with self.assertRaisesRegex(adapter.EvidenceError,'hash mismatch'):
            self.inspect_evidence(pin)
        f.unlink()
        with self.assertRaises(OSError):
            self.inspect_evidence(pin)

    def test_missing_declared_pin_is_not_backfilled(self):
        audit,pin=self.phase2_layout('explicit'); audit['rows'][0]['readbacks'][0].pop('sha256')
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'missing or invalid declared SHA'):
            self.inspect_evidence(pin)

    def test_same_name_other_kind_rejected(self):
        audit,pin=self.phase2_layout('explicit'); audit['rows'][0]['target']['kind']='method_as_command'
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'target missing'):
            self.inspect_evidence(pin)

    def test_reference_escape_and_absolute_paths_rejected(self):
        audit,pin=self.phase2_layout('explicit')
        for value in ['../outside.json','X:\\outside\\artifact.json','/outside','x//a','x/./b']:
            audit['rows'][0]['acceptance']['path']=value
            pin=self.write('audit.json',audit)
            with self.subTest(value=value),self.assertRaises(adapter.EvidenceError):
                self.inspect_evidence(pin)

    def test_wrong_backlink_does_not_accept_even_if_readback_rehashed(self):
        audit,pin=self.phase2_layout('explicit'); rb=json.loads((self.root/'record/readback.json').read_text())
        rb['acceptance_sha256']='0'*64
        audit['rows'][0]['readbacks'][0]['sha256']=self.write('record/readback.json',rb)
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'backlink mismatch'):
            self.inspect_evidence(pin)

    def test_outcome_mismatch_and_missing_case_binding_rejected(self):
        audit,pin=self.phase2_layout('explicit')
        audit['rows'][0]['row_outcome']='matched_in_finite_scope'; pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'outcome differs'):
            self.inspect_evidence(pin)
        audit['rows'][0]['row_outcome']='different_scoped'
        audit['rows'][0]['case_role_links'][0]['registered_typed_target_matches']=False
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'case target binding'):
            self.inspect_evidence(pin)

    def test_unknown_layout_and_missing_acceptance_are_not_pass(self):
        audit,pin=self.phase2_layout('explicit');audit['rows'][0]['acceptance']['schema']='unknown-format'
        pin=self.write('audit.json',audit); self.assertEqual(self.inspect_evidence(pin)['status'],'UNSUPPORTED')
        audit['rows'][0]['acceptance']=None;pin=self.write('audit.json',audit)
        self.assertEqual(self.inspect_evidence(pin)['status'],'UNSUPPORTED')

    def test_duplicate_mode_and_mode_artifact_missing_rejected(self):
        audit,pin=self.current_layout(); acc=json.loads((self.root/'acceptance.json').read_text());rb=json.loads((self.root/'readback.json').read_text())
        rb['observations'][0]['runs'].append(dict(rb['observations'][0]['runs'][0]))
        rsha=self.write('readback.json',rb); acc['readback']['sha256']=rsha; audit['rows'][0]['readbacks'][0]['sha256']=rsha
        audit['rows'][0]['acceptance']['sha256']=self.write('acceptance.json',acc);pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'duplicate current mode'):
            self.inspect_evidence(pin)
        rb['observations'][0]['runs'].pop()
        del rb['observations'][0]['runs'][0]['receipt']
        rsha=self.write('readback.json',rb); acc['readback']['sha256']=rsha; audit['rows'][0]['readbacks'][0]['sha256']=rsha
        audit['rows'][0]['acceptance']['sha256']=self.write('acceptance.json',acc);pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'mode artifact missing'):
            self.inspect_evidence(pin)

    def test_duplicate_target_row_is_not_resolved_arbitrarily(self):
        audit,pin=self.phase2_layout('explicit');audit['rows'].append(dict(audit['rows'][0]))
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'ambiguous'):
            self.inspect_evidence(pin)

    def test_invalid_recorded_replicate_does_not_become_a_mode(self):
        audit,pin=self.phase2_layout('hash');rb=json.loads((self.root/'record/readback.json').read_text())
        rb['native_replicates']=True
        audit['rows'][0]['readbacks'][0]['sha256']=self.write('record/readback.json',rb)
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'invalid recorded replicate'):
            self.inspect_evidence(pin)

    def test_duplicate_keys_and_invalid_utf8_rejected(self):
        _,pin=self.print_layout()
        audit=self.root/'audit.json';audit.write_bytes(b'{"schema":"x","schema":"y"}')
        with self.assertRaisesRegex(adapter.EvidenceError,'duplicate JSON'):
            self.inspect_evidence(h(audit.read_bytes()))
        audit.write_bytes(b'\xff')
        with self.assertRaises(UnicodeError):
            self.inspect_evidence(h(audit.read_bytes()))

    def test_nonfinite_json_and_unknown_pointer_rejected(self):
        _,pin=self.print_layout()
        audit=self.root/'audit.json'
        audit.write_bytes(b'{"extra":1e999}')
        with self.assertRaisesRegex(adapter.EvidenceError,'nonfinite JSON'):
            self.inspect_evidence(h(audit.read_bytes()))
        doc,pin=self.phase2_layout('explicit')
        doc['rows'][0]['acceptance']['record_pointer']='/rows/0'
        pin=self.write('audit.json',doc)
        with self.assertRaisesRegex(adapter.EvidenceError,'unsupported acceptance pointer'):
            self.inspect_evidence(pin)

    def test_duplicate_pinned_artifact_path_is_rejected(self):
        audit,pin=self.current_layout()
        acc=json.loads((self.root/'acceptance.json').read_text())
        rb=json.loads((self.root/'readback.json').read_text())
        first=rb['observations'][0]['runs'][0]
        first['stderr']=dict(first['raw'])
        rsha=self.write('readback.json',rb); acc['readback']['sha256']=rsha
        audit['rows'][0]['readbacks'][0]['sha256']=rsha
        audit['rows'][0]['acceptance']['sha256']=self.write('acceptance.json',acc)
        pin=self.write('audit.json',audit)
        with self.assertRaisesRegex(adapter.EvidenceError,'duplicate referenced path'):
            self.inspect_evidence(pin)

    def test_reparse_attribute_is_rejected_before_read(self):
        _,pin=self.phase2_layout('explicit')
        real = Path.lstat
        flagged = self.root/'record/readback.json'
        def observed(path):
            if path == flagged:
                return SimpleNamespace(st_mode=stat.S_IFREG,st_file_attributes=adapter.REPARSE)
            return real(path)
        with mock.patch.object(Path,'lstat',observed):
            with self.assertRaisesRegex(adapter.EvidenceError,'reparse point rejected'):
                self.inspect_evidence(pin)

    def test_cli_partial_is_not_success_exit(self):
        _,pin=self.phase2_layout('explicit')
        p=subprocess.run([sys.executable,'-I','-B',str(TOOL),'--root',str(self.root),'--audit','audit.json',
                          '--audit-sha256',pin,'--kind','command_or_syntax','--name','CASE_X'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2)
        self.assertEqual(json.loads(p.stdout)['status'],'PARTIAL')


if __name__=='__main__':
    unittest.main()
