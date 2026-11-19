"""Regression checks for restoring the actual published fixture dependencies."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import restore_fixture


class RestoredFixtureTests(unittest.TestCase):
    def test_all_recorded_layouts_restore_exactly(self):
        doc=json.loads((ROOT/restore_fixture.INDEX).read_bytes())
        self.assertEqual(len(doc['layouts']),172)
        with tempfile.TemporaryDirectory() as temporary:
            for row in doc['layouts']:
                target=Path(temporary)/(row['source_file_id']+'-'+str(row['layout_index']))
                with self.subTest(source=row['source_file_id'],layout=row['layout_index']):
                    result=restore_fixture.restore(row['source_file_id'],row['layout_index'],target)
                    self.assertEqual(result['configuration_status'],row['configuration_status'])
                    paths={p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}
                    self.assertEqual(paths,{item['restore_path'] for item in row['files']})
                    for item in row['files']:
                        raw=(target/item['restore_path']).read_bytes()
                        self.assertEqual(len(raw),item['size'])
                        self.assertEqual(sha256(raw).hexdigest(),item['sha256'])
                    if row['csv_directory_required']:
                        self.assertTrue(any(p.is_dir() and p.name.casefold()=='csv' for p in target.iterdir()))

    def test_changed_dependency_is_rejected_before_creating_output(self):
        source=json.loads((ROOT/restore_fixture.INDEX).read_bytes())['layouts'][0]
        layout=json.loads(json.dumps(source))
        with tempfile.TemporaryDirectory() as temporary:
            base=Path(temporary)
            for number,row in enumerate(layout['files']):
                original=(ROOT/row['path']).read_bytes()
                row['path']=f'assets/{number}.bin'
                file=base/row['path'];file.parent.mkdir(exist_ok=True)
                file.write_bytes(original)
            index=base/restore_fixture.INDEX;index.parent.mkdir(parents=True)
            index.write_text(json.dumps({'layouts':[layout]}),encoding='utf-8')
            first=base/layout['files'][0]['path']
            first.write_bytes(first.read_bytes()+bytes([0]))
            with mock.patch.object(restore_fixture,'ROOT',base):
                with self.assertRaisesRegex(ValueError,'Recorded fixture content changed'):
                    restore_fixture.restore(layout['source_file_id'],layout['layout_index'],base/'output')
            self.assertFalse((base/'output').exists())

    def test_existing_output_is_preserved(self):
        source=json.loads((ROOT/restore_fixture.INDEX).read_bytes())['layouts'][0]
        with tempfile.TemporaryDirectory() as temporary:
            target=Path(temporary)/'existing';target.mkdir()
            sentinel=target/'keep.txt';sentinel.write_bytes(b'original')
            with self.assertRaises(FileExistsError):
                restore_fixture.restore(source['source_file_id'],source['layout_index'],target)
            self.assertEqual(sentinel.read_bytes(),b'original')
            self.assertEqual(list(target.iterdir()),[sentinel])


if __name__=='__main__':
    unittest.main()
