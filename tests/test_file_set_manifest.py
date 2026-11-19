"""Behavior and rejection tests for the named-root file inventory."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
TOOL = HERE.parent/'tools'/'file_set_manifest.py'
spec = importlib.util.spec_from_file_location('file_set_manifest', TOOL)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class FileSetManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='file-set-test-', dir=HERE)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root/'repository'
        self.assets = self.root/'release'
        self.repo.mkdir()
        self.assets.mkdir()
        (self.repo/'data').mkdir()
        (self.repo/'data'/'a.txt').write_bytes(b'alpha')
        (self.assets/'bundle.zip').write_bytes(b'example')
        self.roots = {'repo':self.repo, 'release':self.assets}
        self.manifest = self.root/'inventory.json'

    def create(self):
        self.assertEqual(tool.create(self.manifest, self.roots), 2)

    def rewrite(self, modify):
        data = json.loads(self.manifest.read_text(encoding='utf-8'))
        modify(data)
        self.manifest.write_text(json.dumps(data), encoding='utf-8')

    def test_separate_roots_can_use_same_relative_name(self):
        (self.repo/'bundle.zip').write_bytes(b'different')
        self.assertEqual(tool.create(self.manifest, self.roots), 3)
        self.assertEqual(tool.verify(self.manifest, self.roots), 3)

    def test_manifest_inside_root_is_exactly_excluded(self):
        path = self.repo/'manifest.json'
        self.assertEqual(tool.create(path, self.roots), 2)
        self.assertEqual(tool.verify(path, self.roots), 2)
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['manifest_location'], {'root':'repo', 'path':'manifest.json'})
        self.assertNotIn('manifest.json', [r['path'] for r in data['files']])
        with self.assertRaisesRegex(tool.InventoryError, 'already exists'):
            tool.create(path, self.roots)

    def test_missing_extra_and_same_size_tamper_rejected(self):
        self.create()
        file = self.repo/'data'/'a.txt'
        file.write_bytes(b'omega')
        with self.assertRaisesRegex(tool.InventoryError, 'mismatch'):
            tool.verify(self.manifest, self.roots)
        file.write_bytes(b'alpha')
        file.unlink()
        with self.assertRaisesRegex(tool.InventoryError, 'mismatch'):
            tool.verify(self.manifest, self.roots)
        file.write_bytes(b'alpha')
        extra = self.assets/'extra.txt'
        extra.write_bytes(b'x')
        with self.assertRaisesRegex(tool.InventoryError, 'mismatch'):
            tool.verify(self.manifest, self.roots)
        extra.unlink()
        self.assertEqual(tool.verify(self.manifest, self.roots), 2)

    def test_unsafe_paths_rejected(self):
        for name in ('../secret', '/absolute', 'C:/file', 'foo\\bar', 'a//b', 'a/./b',
                     'a/../b', 'x:stream', 'a.', 'a ', 'CON', 'nul.txt', 'COM¹.txt',
                     'CONIN$', 'conin$.txt', 'CONOUT$', 'conout$.log', 'x?y', 'a\x00b'):
            with self.subTest(name=name), self.assertRaises(tool.InventoryError):
                tool.safe_relative(name)

    def test_reserved_stems_at_extension_boundary_and_nearby_names(self):
        reserved = ('CON .txt', 'NUL .txt', 'CONIN$ .txt', 'CONOUT$ .txt', 'COM1 .txt',
                    'con  .txt', 'lpt9 . .txt', 'PRN...log', 'AUX .',
                    'COM\u00b9 .txt', '\uff23\uff2f\uff2e\uff0etxt', 'folder/nuL .log')
        for name in reserved:
            with self.subTest(name=name), self.assertRaises(tool.InventoryError):
                tool.safe_relative(name)
        allowed = ('CONSOLE .txt', 'NULX .txt', 'CONIN$X .txt', 'COM10 .txt',
                   'COM1x .txt', 'LPT0 .txt', 'name .txt', 'folder/.hidden')
        for name in allowed:
            with self.subTest(name=name):
                self.assertEqual(tool.safe_relative(name), name)

    def test_reserved_spaced_stem_in_manifest_is_rejected(self):
        self.create()
        original = self.manifest.read_text(encoding='utf-8')
        for name in ('CON .txt', 'NUL .txt', 'CONIN$ .txt', 'CONOUT$ .txt',
                     'COM1 .txt', 'folder/lPt9  . .txt'):
            self.manifest.write_text(original, encoding='utf-8')
            self.rewrite(lambda d: d['files'][0].update(path=name))
            with self.subTest(name=name), self.assertRaisesRegex(tool.InventoryError, 'reserved Windows device'):
                tool.verify(self.manifest, self.roots)

    def test_windows_reserved_spaced_stems_on_disk(self):
        if sys.platform != 'win32':
            self.skipTest('Windows extended paths')
        names = ('CON .txt', 'NUL .txt', 'CONIN$ .txt', 'CONOUT$ .txt',
                 'COM1 .txt', 'con  .txt', 'LPT9 . .txt', 'COM\u00b9 .txt')
        for name in names:
            path = '\\\\?\\' + str(self.repo/name)
            fd = None
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_BINARY', 0), 0o600)
                self.assertTrue(stat.S_ISREG(os.fstat(fd).st_mode))
                os.write(fd, b'isolated test bytes')
                os.close(fd)
                fd = None
                with self.subTest(name=name), self.assertRaisesRegex(tool.InventoryError, 'reserved Windows device'):
                    tool.create(self.manifest, {'repo':'\\\\?\\'+str(self.repo)})
                self.assertFalse(self.manifest.exists())
            finally:
                if fd is not None:
                    os.close(fd)
                if os.path.lexists(path):
                    os.unlink(path)

    def test_nearby_nonreserved_filename_can_be_inventoried(self):
        (self.repo/'CONSOLE .txt').write_bytes(b'ordinary name')
        (self.repo/'COM10 .txt').write_bytes(b'ordinary name')
        self.assertEqual(tool.create(self.manifest, self.roots), 4)
        self.assertEqual(tool.verify(self.manifest, self.roots), 4)

    def test_manifest_path_injection_rejected(self):
        self.create()
        for value in ('../outside', 'C:/private', 'x\\y', 'NUL.txt'):
            data = json.loads(self.manifest.read_text(encoding='utf-8'))
            data['files'][0]['path'] = value
            self.manifest.write_text(json.dumps(data), encoding='utf-8')
            with self.subTest(value=value), self.assertRaises(tool.InventoryError):
                tool.verify(self.manifest, self.roots)

    def test_duplicate_entries_and_case_unicode_collisions(self):
        self.create()
        original = self.manifest.read_text(encoding='utf-8')
        for path in ('DATA/a.txt', 'data/a.txt'):
            self.manifest.write_text(original, encoding='utf-8')
            def add(data):
                row = next(dict(row) for row in data['files'] if row['root']=='repo')
                row['path'] = path
                data['files'].append(row)
            self.rewrite(add)
            with self.subTest(path=path), self.assertRaisesRegex(tool.InventoryError, 'duplicate or colliding'):
                tool.verify(self.manifest, self.roots)
        self.assertEqual(tool.collision_key('e\u0301.txt'), tool.collision_key('\u00e9.txt'))
        data = json.loads(original)
        data['files'] = [{'root':'repo','path':p,'size':0,'sha256':'0'*64}
                         for p in ('e\u0301.txt', '\u00e9.txt')]
        self.manifest.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(tool.InventoryError, 'colliding'):
            tool.verify(self.manifest, self.roots)

    def test_component_and_file_directory_collisions(self):
        self.create()
        original = json.loads(self.manifest.read_text(encoding='utf-8'))
        for pair in [('A/file','a/other'), ('folder','folder/child'), ('folder/child','folder')]:
            data = dict(original)
            data['files'] = [{'root':'repo','path':p,'size':0,'sha256':'0'*64} for p in pair]
            self.manifest.write_text(json.dumps(data), encoding='utf-8')
            with self.subTest(pair=pair), self.assertRaises(tool.InventoryError):
                tool.verify(self.manifest, self.roots)

    def test_duplicate_json_key_and_invalid_numbers(self):
        self.create()
        self.manifest.write_text('{"schema":"x","schema":"y"}', encoding='utf-8')
        with self.assertRaisesRegex(tool.InventoryError, 'duplicate JSON'):
            tool.verify(self.manifest, self.roots)
        self.manifest.write_text('{"value":NaN}', encoding='utf-8')
        with self.assertRaises(tool.InventoryError):
            tool.verify(self.manifest, self.roots)

    def test_reject_overlapping_or_aliased_roots(self):
        with self.assertRaisesRegex(tool.InventoryError, 'overlap'):
            tool.create(self.manifest, {'one':self.repo,'two':self.repo/'data'})
        with self.assertRaisesRegex(tool.InventoryError, 'overlap'):
            tool.create(self.manifest, {'one':self.repo,'two':self.repo})

    def test_windows_extended_root_overlap_in_both_directions(self):
        if sys.platform != 'win32':
            self.skipTest('Windows extended paths')
        extended = lambda path: '\\\\?\\' + str(path)
        cases = [({'parent':self.repo, 'child':extended(self.repo/'data')}),
                 ({'parent':extended(self.repo), 'child':self.repo/'data'}),
                 ({'parent':extended(self.repo), 'child':self.repo})]
        for roots in cases:
            with self.subTest(roots=roots), self.assertRaisesRegex(tool.InventoryError,'overlap'):
                tool.create(self.manifest, roots)
            self.assertFalse(self.manifest.exists())

    def test_windows_manifest_aliases_inside_root(self):
        if sys.platform != 'win32':
            self.skipTest('Windows path spelling aliases')
        extended = lambda path: '\\\\?\\' + str(path)
        original = self.repo/'data'/'manifest.json'
        parent_case = self.repo/'DATA'/'manifest.json'
        leaf_case = self.repo/'data'/'MANIFEST.JSON'
        self.assertEqual(tool.create(parent_case, {'repo':self.repo}), 1)
        data = json.loads(original.read_text(encoding='utf-8'))
        self.assertEqual(data['manifest_location'], {'root':'repo','path':'data/manifest.json'})
        for root, manifest in [(self.repo, parent_case), (self.repo, original), (self.repo, leaf_case),
                               (self.repo, extended(original)), (extended(self.repo), original),
                               (extended(self.repo), extended(leaf_case))]:
            with self.subTest(root=root, manifest=manifest):
                self.assertEqual(tool.verify(manifest, {'repo':root}), 1)
        # A previous version could record a differently cased parent.
        # It is acceptable only when the OS confirms the same manifest file.
        data['manifest_location']['path'] = 'DATA/manifest.json'
        original.write_text(json.dumps(data),encoding='utf-8')
        self.assertEqual(tool.verify(original, {'repo':self.repo}),1)

    def test_windows_extended_creation_with_normal_verification(self):
        if sys.platform != 'win32':
            self.skipTest('Windows extended paths')
        extended = lambda path: '\\\\?\\' + str(path)
        path = self.repo/'manifest.json'
        self.assertEqual(tool.create(extended(path), {'repo':self.repo}), 1)
        self.assertEqual(tool.verify(path, {'repo':extended(self.repo)}), 1)
        with self.assertRaisesRegex(tool.InventoryError,'already exists'):
            tool.create(extended(self.repo/'MANIFEST.JSON'), {'repo':self.repo})

    def test_windows_short_path_alias_if_available(self):
        if sys.platform != 'win32':
            self.skipTest('Windows short path aliases')
        import ctypes
        folder = self.repo/'Long fixture directory for short path'
        folder.mkdir()
        kernel = ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetShortPathNameW.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_ulong]
        kernel.GetShortPathNameW.restype = ctypes.c_ulong
        buf = ctypes.create_unicode_buffer(32768)
        length = kernel.GetShortPathNameW(str(folder),buf,len(buf))
        if not length or buf.value.casefold()==str(folder).casefold():
            self.skipTest('filesystem did not provide a distinct short path')
        short = Path(buf.value)
        manifest = folder/'manifest.json'
        self.assertEqual(tool.create(short/'manifest.json',{'repo':self.repo}),1)
        self.assertEqual(tool.verify(manifest,{'repo':self.repo}),1)
        with self.assertRaisesRegex(tool.InventoryError,'overlap'):
            tool.canonical_roots({'parent':self.repo,'child':short})

    def test_windows_reserved_names_on_disk_with_extended_path(self):
        if sys.platform != 'win32':
            self.skipTest('Windows extended paths')
        for name in ('CONIN$', 'CONIN$.txt', 'CONOUT$', 'CONOUT$.log'):
            path = '\\\\?\\' + str(self.repo/name)
            fd = None
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os,'O_BINARY',0), 0o600)
                self.assertTrue(stat.S_ISREG(os.fstat(fd).st_mode))
                os.write(fd,b'isolated test bytes')
                os.close(fd)
                fd = None
                with self.subTest(name=name), self.assertRaisesRegex(tool.InventoryError,'reserved Windows device'):
                    tool.create(self.manifest, {'repo':'\\\\?\\'+str(self.repo)})
                self.assertFalse(self.manifest.exists())
            finally:
                if fd is not None:
                    os.close(fd)
                if os.path.lexists(path):
                    os.unlink(path)

    def test_reserved_device_names_in_manifest_are_rejected(self):
        self.create()
        original = self.manifest.read_text(encoding='utf-8')
        for name in ('CONIN$', 'conin$.txt', 'CONOUT$', 'conout$.log'):
            self.manifest.write_text(original,encoding='utf-8')
            self.rewrite(lambda d: d['files'][0].update(path=name))
            with self.subTest(name=name), self.assertRaisesRegex(tool.InventoryError,'reserved Windows device'):
                tool.verify(self.manifest,self.roots)

    def test_case_sensitive_distinct_manifest_names_are_not_merged(self):
        if sys.platform == 'win32':
            proc = subprocess.run(['fsutil.exe','file','setCaseSensitiveInfo',str(self.repo),'enable'],
                                  capture_output=True)
            if proc.returncode:
                self.skipTest('case-sensitive directory cannot be enabled')
        upper = self.repo/'MANIFEST.JSON'
        lower = self.repo/'manifest.json'
        upper.write_bytes(b'protected data')
        if lower.exists():
            self.skipTest('filesystem is not case-sensitive')
        with self.assertRaisesRegex(tool.InventoryError,'manifest path collides'):
            tool.create(lower,{'repo':self.repo})
        self.assertFalse(lower.exists())
        self.assertEqual(upper.read_bytes(),b'protected data')
        upper.unlink()
        tool.create(lower,{'repo':self.repo})
        upper.write_bytes(b'distinct file')
        data = json.loads(lower.read_text(encoding='utf-8'))
        data['manifest_location']['path'] = 'MANIFEST.JSON'
        lower.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaisesRegex(tool.InventoryError,'manifest location differs'):
            tool.verify(lower,{'repo':self.repo})
        self.assertEqual(upper.read_bytes(),b'distinct file')

    def test_case_sensitive_sibling_roots_are_not_merged(self):
        if sys.platform == 'win32':
            self.skipTest('case-sensitive sibling names tested on POSIX')
        a,b=self.root/'Name',self.root/'name'
        a.mkdir(); b.mkdir()
        (a/'one').write_bytes(b'a'); (b/'two').write_bytes(b'b')
        self.assertEqual(tool.create(self.manifest,{'first':a,'second':b}),2)
        self.assertEqual(tool.verify(self.manifest,{'first':a,'second':b}),2)

    def test_manifest_root_location_and_unknown_root(self):
        self.create()
        with self.assertRaises(tool.InventoryError):
            tool.verify(self.manifest, {'repo':self.repo})
        self.rewrite(lambda d: d.update(manifest_location={'root':'repo','path':'wrong.json'}))
        with self.assertRaisesRegex(tool.InventoryError, 'location'):
            tool.verify(self.manifest, self.roots)

    def test_inside_manifest_recorded_as_external_is_not_silently_repaired(self):
        path=self.repo/'manifest.json'
        tool.create(path,{'repo':self.repo})
        data=json.loads(path.read_text(encoding='utf-8'))
        data['manifest_location']=None
        path.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaisesRegex(tool.InventoryError,'manifest location differs'):
            tool.verify(path,{'repo':self.repo})

    def test_relative_parent_components_keep_normal_use(self):
        relative = Path(os.path.relpath(self.repo/'data',Path.cwd()))/'..'
        self.assertEqual(tool.create(self.manifest,{'repo':relative}),1)
        self.assertEqual(tool.verify(self.manifest,{'repo':self.repo}),1)

    def test_link_inside_root_is_rejected(self):
        link = self.repo/'link'
        try:
            os.symlink(self.assets/'bundle.zip', link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest('file symlinks unavailable: '+str(exc))
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(self.manifest, self.roots)

    def test_directory_junction_is_rejected_on_windows(self):
        if sys.platform != 'win32':
            self.skipTest('Windows junction test')
        junction = self.repo/'junction'
        proc = subprocess.run(['cmd.exe','/c','mklink','/J',str(junction),str(self.assets)],
                              capture_output=True, text=True)
        if proc.returncode:
            self.skipTest('junction creation unavailable')
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(self.manifest, self.roots)
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(self.manifest, {'junction':junction})
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(junction/'manifest.json', {'repo':self.repo})
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(self.manifest, {'repo':junction/'..'})
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(junction/'..'/'manifest.json', {'repo':self.repo})

    def test_root_or_manifest_path_link_is_rejected(self):
        link = self.root/'linked-root'
        try:
            os.symlink(self.repo, link, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest('directory symlinks unavailable: '+str(exc))
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(self.manifest, {'repo':link})
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(link/'new.json', {'repo':self.repo})
        with self.assertRaisesRegex(tool.InventoryError, 'link or reparse'):
            tool.create(self.manifest, {'repo':link/'..'})

    def test_reparse_detection_even_without_symlink_privileges(self):
        fake = mock.Mock(st_mode=0, st_file_attributes=tool.REPARSE)
        self.assertTrue(tool.is_link(fake))
        symbolic = mock.Mock(st_mode=stat.S_IFLNK, st_file_attributes=0)
        self.assertTrue(tool.is_link(symbolic))

    def test_manifest_cannot_be_added_as_its_own_entry(self):
        path = self.repo/'manifest.json'
        tool.create(path, self.roots)
        data = json.loads(path.read_text(encoding='utf-8'))
        data['files'].append({'root':'repo','path':'manifest.json','size':0,'sha256':'0'*64})
        path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(tool.InventoryError, 'cannot inventory itself'):
            tool.verify(path, self.roots)

    def test_cli_create_verify_and_no_overwrite(self):
        args = ['--manifest',str(self.manifest),'--root',f'repo={self.repo}', '--root',f'release={self.assets}']
        def call(action, extra=()):
            return subprocess.run([sys.executable,'-I','-B',str(TOOL),action,*args,*extra],capture_output=True,text=True)
        self.assertEqual(call('create').returncode, 0)
        self.assertEqual(call('verify').returncode, 0)
        before = self.manifest.read_bytes()
        self.assertNotEqual(call('create').returncode, 0)
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertNotEqual(call('verify',['--root',f'repo={self.repo}']).returncode, 0)


if __name__ == '__main__':
    unittest.main()
