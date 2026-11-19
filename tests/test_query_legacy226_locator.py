import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY = ROOT / "tools" / "query.py"


class Legacy226QueryIntegration(unittest.TestCase):
    def test_query_reports_legacy_locator_without_reproduction(self):
        result = subprocess.run([sys.executable, "-B", str(QUERY), "command_or_syntax:PRINT"],
                                cwd=ROOT, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        data = json.loads(result.stdout.decode("utf-8"))
        rows = data["legacy226_source_locator"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["row_outcome"], "matched_in_finite_scope")
        self.assertEqual(rows[0]["original_present"], rows[0]["reference_count"])
        self.assertEqual(rows[0]["candidate_present"], rows[0]["reference_count"])
        self.assertEqual(rows[0]["reference_class_counts"]["PUBLIC_INCLUDED"],rows[0]["reference_count"])
        self.assertTrue(rows[0]["individually_reviewed_artifacts"])
        self.assertEqual(rows[0]["independent_reproduction"], "not_established_from_candidate_alone")
        self.assertEqual(data["legacy226_source_locator_availability"]["state"], "AVAILABLE")


if __name__ == "__main__":
    unittest.main()
