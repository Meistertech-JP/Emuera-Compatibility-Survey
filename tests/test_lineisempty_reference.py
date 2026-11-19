"""Check the published LINEISEMPTY projection reference against its bytes."""
import hashlib
import json
from pathlib import Path
import unittest


class LineIsEmptyReferenceTest(unittest.TestCase):
    def test_parent_projection_reference_resolves_to_candidate_bytes(self):
        root = Path(__file__).resolve().parents[1] / 'evidence' / 'lineisempty-acceptance-20261117'
        record = json.loads((root / 'record.json').read_text(encoding='utf-8'))
        ref = record['original_parent_decision']['acceptance_projection']
        self.assertEqual(ref['path'], 'parent-acceptance-projection.json')
        raw = (root / ref['path']).read_bytes()
        self.assertEqual(ref['size'], len(raw))
        self.assertEqual(ref['sha256'], hashlib.sha256(raw).hexdigest())
        projection = json.loads(raw)
        self.assertIn('record.json#/acceptance_pin_discrepancy', projection['historical_fields_warning'])


if __name__ == '__main__':
    unittest.main()
