import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parent.parent

class EnvironmentChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for rel in ('tools/verify_environment.py', 'manifests/environment.json',
                    'harness/fixtures/emuera.config',
                    'vendor/emuera/Emuera1824-v24-with-notices.zip',
                    'vendor/emuera/NOTICE.ja.md', 'vendor/emuera/NOTICE.en.md'):
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / rel, target)

    def tearDown(self):
        self.temp.cleanup()

    def run_checker(self):
        return subprocess.run([sys.executable, '-I', '-B', str(self.root / 'tools/verify_environment.py')],
                              capture_output=True, text=True)

    def test_isolated_copy(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'PASS')

    def test_modified_bundle_rejected(self):
        bundle = self.root / 'vendor/emuera/Emuera1824-v24-with-notices.zip'
        data = bytearray(bundle.read_bytes())
        data[len(data) // 2] ^= 1
        bundle.write_bytes(data)
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SHA-256 mismatch', result.stderr)

    def test_missing_notice_rejected(self):
        (self.root / 'vendor/emuera/NOTICE.ja.md').unlink()
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
