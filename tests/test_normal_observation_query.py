"""C196 access paths use bounded, verified shared observations."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    # Keep sealed evidence trees byte-identical: importing must not add __pycache__.
    bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = bytecode
    return mod
query = module('normal_query', ROOT / 'tools/query.py')

class NormalObservationQueryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'evidence/normal-observation-access-20261117/observations.json').read_text(encoding='utf8'))

    def lookup(self, term, kind=None):
        rows, states = query.saved_observations(term, ROOT, kind=kind)
        return [r for r in rows if r['collection'] == 'normal_observations_196'], states

    def test_all_ten_ids_and_roles_have_verified_mode_references(self):
        for case in self.data['cases']:
            cond = case['condition']['id']; cid = case['case_id']; role = case['target'][0]
            for term, basis in ((cond.lower(), 'CONDITION_ID'), (cid, 'CASE_ID'),
                                (role['kind'] + ':' + role['name'], 'TYPED_ROLE')):
                with self.subTest(term=term, case=cid):
                    rows, states = self.lookup(term)
                    row = next(r for r in rows if r['case_id'] == cid)
                    self.assertEqual(row['match_basis'], basis)
                    self.assertEqual(row['condition_id'], cond)
                    self.assertEqual(row['matched_case_roles'], [role])
                    self.assertEqual(row['sharing_scope'], 'ONE_SHARED_BATCH_NOT_TEN_INDEPENDENT_EXECUTIONS')
                    self.assertEqual(row['native_natural_exit'], 'NOT_OBSERVED')
                    self.assertEqual(states['normal_observations_196'], 'AVAILABLE')
                    self.assertEqual([x['mode'] for x in row['modes']], ['native-01','native-02','public-01'])
                    self.assertNotIn('raw_block', json.dumps(row))
                    for i, mode in enumerate(row['modes']):
                        for k in ('history','fixture','config'):
                            ref = mode[k]; self.assertEqual(ref['location'], 'CANDIDATE_RELATIVE')
                            self.assertTrue((ROOT / ref['path']).is_file())
                        self.assertEqual(mode['observation']['pointer'], row['record']['pointer'] + '/observations/' + str(i))
                        raw=(ROOT / mode['history']['path']).read_bytes(); a,b=mode['byte_span']
                        self.assertEqual(hashlib.sha256(raw).hexdigest(), mode['history_sha256'])
                        self.assertEqual(raw[a:b].decode('utf-16-le'), case['observations'][i]['raw_block'])

    def test_kind_filter_and_unknown_condition(self):
        for term in ('C196_04','PRINTPLAIN196_C196_04','PRINTSINGLEV'):
            self.assertEqual(self.lookup(term, 'expression_function')[0], [])
            self.assertTrue(self.lookup(term, 'command_or_syntax')[0])
        self.assertEqual(self.lookup('expression_function:PRINTSINGLEV')[0], [])
        self.assertEqual(self.lookup('C196_99')[0], [])
        with self.assertRaisesRegex(ValueError, 'conflicting typed kind'):
            self.lookup('command_or_syntax:PRINTSINGLEV', 'expression_function')

    def test_empty_condition_layout_difference_is_preserved(self):
        row, = self.lookup('C196_13')[0]
        case = self.data['cases'][int(row['record']['pointer'].split('/')[-1])]
        self.assertFalse(case['recorded_comparison_axes']['raw_equal'])
        self.assertFalse(case['recorded_comparison_axes']['layout_equal'])
        self.assertTrue(case['recorded_comparison_axes']['observable_content_equal'])
        self.assertIn('P><T\r\n', case['observations'][0]['raw_block'])
        self.assertIn('P>\r\n \r\n<T\r\n', case['observations'][2]['raw_block'])

    def test_missing_modified_resealed_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory(prefix='negative-query-') as tmp:
            root=Path(tmp); ev=root/'evidence'; ev.mkdir()
            for name in ('normal-observation-access-20261117','multi-group-101-20261117'):
                shutil.copytree(ROOT/'evidence'/name, ev/name)
            def check(): return query._normal_observations_196('C196_04',root,None)
            self.assertEqual(len(check()[0]),1)
            bundle=ev/'normal-observation-access-20261117'; spare=ev/'removed'
            bundle.rename(spare); self.assertEqual(check(),([], 'NOT_INSTALLED')); spare.rename(bundle)
            record=bundle/'observations.json'; original=record.read_bytes(); record.unlink()
            with self.assertRaisesRegex(ValueError, 'incomplete'): check()
            record.write_bytes(original+b' ')
            with self.assertRaises(ValueError): check()
            manifest=bundle/'manifest.json'; original_manifest=manifest.read_bytes(); doc=json.loads(original_manifest)
            item=next(x for x in doc['files'] if x['path']=='observations.json')
            item['sha256']=hashlib.sha256(record.read_bytes()).hexdigest(); item['size']=record.stat().st_size
            manifest.write_text(json.dumps(doc),encoding='utf8')
            with self.assertRaisesRegex(ValueError,'manifest snapshot mismatch'): check()
            manifest.write_bytes(original_manifest); record.write_bytes(original)
            source=ev/'multi-group-101-20261117'; raw=source/'assets/bbdfcba295b75e9aeb4106422889f6615054e7d8f7198a24ac9ce7855856725b.bin'; old=raw.read_bytes()
            raw.write_bytes(old+b'X')
            with self.assertRaises(ValueError): check()
            raw.write_bytes(old); raw.unlink()
            with self.assertRaises(ValueError): check()
            raw.write_bytes(old)
            s_manifest=source/'manifest.json'; s_original=s_manifest.read_bytes(); s_manifest.write_bytes(s_original+b' ')
            with self.assertRaisesRegex(ValueError,'dependency manifest snapshot mismatch'): check()
            s_manifest.write_bytes(s_original)
            source.rename(ev/'source-preserved')
            with self.assertRaises(ValueError): check()
            (ev/'source-preserved').rename(source)
            self.assertEqual(len(check()[0]),1)

    def test_bundle_symlink_rejected_when_supported(self):
        with tempfile.TemporaryDirectory(prefix='link-query-') as tmp:
            root=Path(tmp); ev=root/'evidence'; ev.mkdir()
            target=ev/'preserved'; target.mkdir()
            bundle=ev/'normal-observation-access-20261117'
            try: bundle.symlink_to(target,target_is_directory=True)
            except OSError: self.skipTest('directory symlink creation unavailable on this host')
            with self.assertRaises(ValueError): query._normal_observations_196('C196_04',root,None)

    @unittest.skipUnless(sys.platform == 'win32','Windows junction test')
    def test_windows_junction_rejected(self):
        with tempfile.TemporaryDirectory(prefix='junction-query-') as tmp:
            root=Path(tmp); ev=root/'evidence'; ev.mkdir()
            target=ev/'preserved'
            shutil.copytree(ROOT/'evidence/normal-observation-access-20261117',target)
            shutil.copytree(ROOT/'evidence/multi-group-101-20261117',ev/'multi-group-101-20261117')
            bundle=ev/'normal-observation-access-20261117'
            proc=subprocess.run(['cmd','/c','mklink','/J',str(bundle),str(target)],capture_output=True)
            if proc.returncode: self.skipTest('junction creation unavailable on this host')
            try:
                with self.assertRaises(ValueError): query._normal_observations_196('C196_04',root,None)
            finally: os.rmdir(bundle)

    def test_cli_modified_data_is_generic_and_leaks_no_path(self):
        with tempfile.TemporaryDirectory(prefix='cli-negative-') as tmp:
            root=Path(tmp); ev=root/'evidence'; ev.mkdir()
            for name in ('normal-observation-access-20261117','multi-group-101-20261117'):
                shutil.copytree(ROOT/'evidence'/name, ev/name)
            record=ev/'normal-observation-access-20261117/observations.json'
            record.write_bytes(record.read_bytes()+b'X')
            with patch.object(query,'ROOT',root), patch.object(sys,'argv',['query.py','C196_04']), contextlib.redirect_stderr(io.StringIO()) as err:
                with self.assertRaises(SystemExit) as exc: query.main()
            self.assertEqual(exc.exception.code,2)
            self.assertEqual(err.getvalue(),'saved observation source is unavailable or inconsistent\n')
            self.assertNotIn(str(root),err.getvalue())

    def test_external_manifest_pin_and_semantic_contract(self):
        with tempfile.TemporaryDirectory(prefix='seal-query-') as tmp:
            root=Path(tmp); ev=root/'evidence'; ev.mkdir(); (root/'tools').mkdir()
            shutil.copyfile(ROOT/'tools/file_set_manifest.py',root/'tools/file_set_manifest.py')
            for name in ('normal-observation-access-20261117','multi-group-101-20261117'):
                shutil.copytree(ROOT/'evidence'/name, ev/name)
            bundle=ev/'normal-observation-access-20261117'; record=bundle/'observations.json'; manifest=bundle/'manifest.json'
            old_record=record.read_bytes(); old_manifest=manifest.read_bytes()
            def pin(): return hashlib.sha256(manifest.read_bytes()).hexdigest()
            def standalone(expected):
                return subprocess.run([sys.executable,'-I','-B',str(bundle/'verify.py'),'--evidence-root',str(ev),
                                       '--manifest-sha256',expected],capture_output=True,text=True,encoding='utf8')
            def reseal(name):
                doc=json.loads(old_manifest); item=next(x for x in doc['files'] if x['path']==name)
                b=(bundle/name).read_bytes(); item.update(size=len(b),sha256=hashlib.sha256(b).hexdigest())
                manifest.write_text(json.dumps(doc),encoding='utf8')
            original_pin=pin(); self.assertEqual(standalone(original_pin).returncode,0)
            self.assertNotEqual(standalone('0'*64).returncode,0)
            for mutation in ('scope','limitations'):
                doc=json.loads(old_record)
                if mutation=='scope': doc['scope']='Every case was separately executed and completed.'
                else: doc['limitations']=[]
                record.write_text(json.dumps(doc),encoding='utf8'); reseal('observations.json')
                self.assertNotEqual(standalone(original_pin).returncode,0)
                proc=standalone(pin())
                self.assertNotEqual(proc.returncode,0)
                self.assertEqual(proc.stderr,'FAIL: evidence or verification tool is unavailable or inconsistent\n')
                verifier=module('standalone_semantics',bundle/'verify.py')
                with self.assertRaisesRegex(ValueError,'scope or limitations'): verifier.run(record,ev)
                with self.assertRaisesRegex(ValueError,'manifest snapshot mismatch'):
                    query._normal_observations_196('C196_04',root,None)
                record.write_bytes(old_record); manifest.write_bytes(old_manifest)
            readme=bundle/'README.md'; old_readme=readme.read_bytes(); readme.write_bytes(old_readme+b' altered')
            self.assertNotEqual(standalone(original_pin).returncode,0)
            reseal('README.md')
            self.assertNotEqual(standalone(original_pin).returncode,0)
            with self.assertRaisesRegex(ValueError,'manifest snapshot mismatch'):
                query._normal_observations_196('C196_04',root,None)

    def test_cli_preserves_existing_results_and_exposes_new_condition(self):
        def cli(term,disable_new=False):
            feature = patch.object(query,'_normal_observations_196',return_value=([], 'NOT_INSTALLED')) if disable_new else contextlib.nullcontext()
            with feature,patch.object(query,'ROOT',ROOT),patch.object(sys,'argv',['query.py',term]),contextlib.redirect_stdout(io.StringIO()) as out:
                code=query.main(); return code,json.loads(out.getvalue())
        for term in ('command_or_syntax:PRINTSINGLEV','PRINTPLAIN196_C196_04','C196_04','FONTSTYLE_NEG1','WAIT'):
            with self.subTest(term=term):
                old_code,old=cli(term,True); new_code,new=cli(term)
                rows=[x for x in new['saved_observations'] if x['collection']=='normal_observations_196']
                new['saved_observations']=[x for x in new['saved_observations'] if x['collection']!='normal_observations_196']
                new['saved_observation_availability'].pop('normal_observations_196')
                old['saved_observation_availability'].pop('normal_observations_196')
                self.assertEqual(new,old)
                if term=='C196_04': self.assertEqual((old_code,new_code,len(rows)),(1,0,1))
                else: self.assertEqual(new_code,old_code)

if __name__ == '__main__': unittest.main()
