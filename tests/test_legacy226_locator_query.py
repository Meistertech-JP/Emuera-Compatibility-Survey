import tempfile
import unittest
from pathlib import Path
import shutil
import tools.legacy226_locator_query as query

ROOT = Path(__file__).resolve().parents[1]
LOCATOR = ROOT / 'evidence' / 'legacy226-source-locator-20261118'


class Legacy226LocatorQuery(unittest.TestCase):
    def test_known_target_reports_originals_without_claiming_reproduction(self):
        row = query.lookup(ROOT, 'command_or_syntax', 'PRINT')
        self.assertEqual(row['row_outcome'], 'matched_in_finite_scope')
        self.assertEqual(row['original_present'], row['reference_count'])
        self.assertEqual(row['candidate_present'], row['reference_count'])
        self.assertEqual(row['reference_class_counts']['PUBLIC_INCLUDED'],row['reference_count'])
        self.assertTrue(row['individually_reviewed_artifacts'])
        self.assertEqual(row['recorded_sha_checked'], row['recorded_sha_matched'])
        self.assertEqual(row['independent_reproduction'], 'not_established_from_candidate_alone')

    def test_absent_locator_is_distinct_from_unknown_target(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(query.lookup(temp, 'command_or_syntax', 'PRINT'))
            partial = Path(temp) / 'evidence' / 'legacy226-source-locator-20261118'
            partial.mkdir(parents=True)
            shutil.copy(LOCATOR / 'locator.json', partial / 'locator.json')
            with self.assertRaises(ValueError):
                query.lookup(temp, 'command_or_syntax', 'PRINT')

    def test_unknown_target_is_rejected(self):
        with self.assertRaises(ValueError):
            query.lookup(ROOT, 'command_or_syntax', 'NOT_A_LEGACY_TARGET')


if __name__ == '__main__':
    unittest.main()
