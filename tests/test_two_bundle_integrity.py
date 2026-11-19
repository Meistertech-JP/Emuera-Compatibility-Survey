"""Portable synthetic tests; no private files or installed candidate are required."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('query_under_test', ROOT / 'tools/query.py')
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)

def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def digest(value):
    return hashlib.sha256(value).hexdigest()

class BundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.anchor = self.root / 'evidence/native-source-anchor82-20261117'
        self.selected = self.root / 'evidence/selected-51-20261117'
        self.anchor.mkdir(parents=True)
        self.selected.mkdir(parents=True)
        self.target = {'kind': 'assignment_syntax', 'name': '='}
        self.anchor_row = {'target': self.target, 'anchor_kind': 'finite',
                           'source_archive': {'path': 'vendor/source.zip', 'sha256': 'a'*64},
                           'locations': [{'member': 'src/x.cs', 'start_line': 1, 'end_line': 1}],
                           'limitations': 'static only', 'original_source_version_and_sha_identity': 'not_established'}
        self.anchor_bytes = dump(self.anchor_row) + b'\n'
        self.case_id = 'CASE_SYNTHETIC'
        role = {'kind': 'method_as_command', 'name': 'MAXARRAY'}
        modes = []
        for mode in ('native-01', 'native-02', 'public-01'):
            inputs = []
            for name in ('ERB/CASE.ERB', 'ERB/ARRAYMSORT176.ERH', 'ERB/ENDPOINT_READBACK.ERH', 'emuera.config'):
                relative = f'assets/B001/{mode}/inputs/{name}'
                path = self.selected / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'synthetic input')
                inputs.append({'relative_name': name, 'path': relative, 'sha256': digest(b'synthetic input')})
            modes.append({'mode': mode, 'inputs': inputs, 'identity_basis': 'fixture',
                          'native_natural_exit': 'not_established'})
        self.selected_doc = {'schema': 'selected-three-group-evidence-1',
            'cases': [{'case_id': self.case_id, 'batch_id': 'B001', 'group': 'array-aggregate-method-endpoints',
                       'parent_and_case_roles': [role], 'registered_roles': [role],
                       'record': {'scenario_verdict': 'different_scoped',
                                  'observation_points_and_comparison': {'id': 'fixture', 'target': role}}}],
            'batches': [{'batch_id': 'B001', 'case_ids': [self.case_id], 'modes': modes}]}
        self.selected_bytes = dump(self.selected_doc)
        (self.selected/'references.json').write_bytes(b'{}')
        (self.selected/'README.md').write_bytes(b'fixture')
        self.anchor_pin = self.seal(self.anchor, 'targets.jsonl', self.anchor_bytes)
        self.selected_pin = self.seal(self.selected, 'index.json', self.selected_bytes)
        self.patches = [patch.object(query, '_ANCHOR82_MANIFEST_SHA256', self.anchor_pin),
                        patch.object(query, '_SELECTED51_MANIFEST_SHA256', self.selected_pin)]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def seal(self, directory, name, payload):
        (directory/name).write_bytes(payload)
        manifest = {'schema':'selected-file-set.v1', 'files':[{'root':'evidence','path':name,
                    'size':len(payload),'sha256':digest(payload)}]}
        value = dump(manifest)
        (directory/'manifest.json').write_bytes(value)
        return digest(value)

    def selected_query(self):
        return query.saved_observations(self.case_id, self.root)

    def anchor_query(self):
        return query.native_source_anchor82('=', self.root, 'assignment_syntax')

    def cli(self, term, *options):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(query, 'ROOT', self.root), patch.object(sys, 'argv', ['query.py',term,*options]), \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = query.main()
            except SystemExit as exc:
                code = exc.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_normal_anchor_and_selected_results(self):
        rows, status = self.anchor_query()
        self.assertEqual(status['state'], 'AVAILABLE')
        self.assertEqual(rows[0]['row'], self.anchor_row)
        self.assertEqual(rows[0]['record']['line_1based'], 1)
        rows, status = self.selected_query()
        selected, = [r for r in rows if r['collection']=='selected_51_saved']
        self.assertEqual(status['selected_51_saved'], 'AVAILABLE')
        self.assertEqual(selected['recorded_verdict'], 'different_scoped')
        self.assertEqual(selected['saved_modes'], ['native-01','native-02','public-01'])
        self.assertEqual(selected['record']['pointer'], '/cases/0')
        self.assertEqual(selected['target_reach'], 'NOT_INFERRED_FROM_REGISTERED_ROLE_OR_BATCH')

    def test_whole_bundle_not_installed(self):
        import shutil
        shutil.rmtree(self.anchor)
        shutil.rmtree(self.selected)
        self.assertEqual(self.anchor_query(), ([], {'state':'NOT_INSTALLED'}))
        self.assertEqual(self.selected_query()[1]['selected_51_saved'], 'NOT_INSTALLED')

    def test_missing_manifest_or_member_and_empty_directory_fail(self):
        for directory, name, lookup in [(self.anchor,'targets.jsonl',self.anchor_query),
                                        (self.selected,'index.json',self.selected_query)]:
            for file in ('manifest.json', name):
                with self.subTest(bundle=directory.name, missing=file):
                    path=directory/file
                    old=path.read_bytes()
                    path.unlink()
                    with self.assertRaises(query.BundleIntegrityError): lookup()
                    path.write_bytes(old)
            import shutil
            for path in list(directory.iterdir()):
                if path.is_dir(): shutil.rmtree(path)
                else: path.unlink()
            with self.assertRaises(query.BundleIntegrityError): lookup()

    def test_changed_member_or_manifest_fails(self):
        for directory, name, lookup in [(self.anchor,'targets.jsonl',self.anchor_query),
                                        (self.selected,'index.json',self.selected_query)]:
            for file in ('manifest.json', name):
                with self.subTest(bundle=directory.name, changed=file):
                    path=directory/file
                    old=path.read_bytes()
                    path.write_bytes(old+b' ')
                    with self.assertRaises(query.BundleIntegrityError): lookup()
                    path.write_bytes(old)

    def test_altered_data_resealed_under_new_manifest_rejected(self):
        altered_anchor = self.anchor_bytes.replace(b'static only', b'changed result')
        altered_selected = self.selected_bytes.replace(b'different_scoped', b'matched_scoped')
        self.assertNotEqual(json.loads(altered_anchor), self.anchor_row)
        self.assertNotEqual(json.loads(altered_selected), self.selected_doc)
        for directory, name, payload, lookup in [(self.anchor,'targets.jsonl',altered_anchor,self.anchor_query),
                                                  (self.selected,'index.json',altered_selected,self.selected_query)]:
            with self.subTest(bundle=directory.name):
                self.seal(directory,name,payload)
                with self.assertRaisesRegex(query.BundleIntegrityError,'manifest pin mismatch'): lookup()

    def test_member_hash_and_size_enforced_even_with_fixture_manifest_pin(self):
        # Pin an intentionally inconsistent synthetic manifest to exercise member binding.
        for directory, name, payload, lookup, const in [
            (self.anchor,'targets.jsonl',self.anchor_bytes,self.anchor_query,'_ANCHOR82_MANIFEST_SHA256'),
            (self.selected,'index.json',self.selected_bytes,self.selected_query,'_SELECTED51_MANIFEST_SHA256')]:
            for field in ('sha256','size'):
                with self.subTest(bundle=directory.name, field=field):
                    pin=self.seal(directory,name,payload)
                    manifest=json.loads((directory/'manifest.json').read_bytes())
                    manifest['files'][0][field]='0'*64 if field=='sha256' else len(payload)+1
                    data=dump(manifest); (directory/'manifest.json').write_bytes(data)
                    with patch.object(query,const,digest(data)):
                        with self.assertRaisesRegex(query.BundleIntegrityError,'member size or hash mismatch'): lookup()

    def test_duplicate_or_absent_manifest_entry_rejected(self):
        for directory, name, payload, lookup, const in [
            (self.anchor,'targets.jsonl',self.anchor_bytes,self.anchor_query,'_ANCHOR82_MANIFEST_SHA256'),
            (self.selected,'index.json',self.selected_bytes,self.selected_query,'_SELECTED51_MANIFEST_SHA256')]:
            for duplicate in (False,True):
                with self.subTest(bundle=directory.name, duplicate=duplicate):
                    self.seal(directory,name,payload)
                    manifest=json.loads((directory/'manifest.json').read_bytes())
                    manifest['files'] = manifest['files']*2 if duplicate else []
                    data=dump(manifest); (directory/'manifest.json').write_bytes(data)
                    with patch.object(query,const,digest(data)):
                        with self.assertRaisesRegex(query.BundleIntegrityError,'missing or duplicated'): lookup()

    def test_cli_integrity_failure_is_specific_even_with_partial(self):
        # Selected is checked first. Remove its member and retain its manifest.
        (self.selected/'index.json').unlink()
        for options in ((),('--partial',)):
            code,out,err=self.cli(self.case_id,*options)
            self.assertEqual(code,2); self.assertEqual(out,''); self.assertIn('selected-51',err)
        (self.selected/'index.json').write_bytes(self.selected_bytes)
        (self.anchor/'targets.jsonl').unlink()
        for options in ((),('--partial',)):
            code,out,err=self.cli('=',*options)
            self.assertEqual(code,2); self.assertEqual(out,''); self.assertIn('native-source-anchor82',err)

    def test_file_symlinks_rejected_when_supported(self):
        for directory,name,lookup in [(self.anchor,'targets.jsonl',self.anchor_query),
                                      (self.selected,'index.json',self.selected_query)]:
            path=directory/name
            other=directory/(name+'.real')
            path.rename(other)
            try:
                path.symlink_to(other.name)
            except (OSError,NotImplementedError):
                other.rename(path)
                self.skipTest('file symlinks unavailable')
            with self.assertRaises(query.BundleIntegrityError): lookup()
            path.unlink(); other.rename(path)

    @unittest.skipUnless(os.name == 'nt', 'Windows junction test')
    def test_windows_junction_bundle_rejected(self):
        other = self.root/'junction-root'/'evidence'
        other.mkdir(parents=True)
        for target in (self.anchor,self.selected):
            junction = other/target.name
            result = subprocess.run(['cmd','/c','mklink','/J',str(junction),str(target)],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if result.returncode:
                self.skipTest('junction creation unavailable')
            try:
                if target==self.anchor:
                    with self.assertRaises(query.BundleIntegrityError):
                        query.native_source_anchor82('=',other.parent,'assignment_syntax')
                else:
                    with self.assertRaises(query.BundleIntegrityError):
                        query.saved_observations(self.case_id,other.parent)
            finally:
                junction.rmdir()

if __name__ == '__main__':
    unittest.main()
