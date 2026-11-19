"""Tests for the standalone projection reader; generated fixtures only."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import case_reader as reader


def bjson(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base_core = {
            "case_id": "Case_A", "targets": [{"kind": "command", "name": "X"}],
            "scenario_verdict": "unverified", "survey_pointer": "/cases/0",
            "trace_aliases": [], "target_positions_outside_694": [],
            "runtime_observation_context": "NO_RUNTIME_OBSERVATION_KEY_FOUND",
        }
        self.row = {**self.base_core, "projection_state": "AUTOMATED_SCREENING_INDEPENDENT_REVIEW_PENDING",
                    "withheld_count": 1, "neutralized_key_count": 0,
                    "fields": {"observation_points_and_comparison": "Native: before; after UNOBSERVED",
                               "fixtures_and_initial_state": "A=17",
                               "invocation": "one Enter",
                               "limitations": ["historical partial only", "natural exit UNOBSERVED"],
                               "evidence": {"$case_projection_withheld": "nonincluded_or_private_field"}}}
        self.schema = "case-register-neutral-screened-draft-v1"
        self.write()

    def write(self, rows=None, cores=None):
        rows = rows if rows is not None else [self.row]
        cores = cores if cores is not None else [self.base_core]
        (self.root / "README.ja.md").write_bytes(b"ja\n")
        (self.root / "README.md").write_bytes(b"en\n")
        (self.root / "cases.jsonl").write_bytes(b"\n".join(map(bjson, rows)) + b"\n")
        (self.root / "core.jsonl").write_bytes(b"\n".join(map(bjson, cores)) + b"\n")
        entries = {}
        for name in sorted(reader.FILES):
            raw = (self.root / name).read_bytes()
            entries[name] = {"size": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        data = bjson({"schema": self.schema, "records": len(rows), "files": entries})
        (self.root / "manifest.json").write_bytes(data)
        self.pin = hashlib.sha256(data).hexdigest()

    def test_case_insensitive_and_original_values(self):
        result = reader.read_projection(self.root, self.pin.upper(), "cASE_a")
        self.assertEqual(result["case_id"], "Case_A")
        self.assertEqual(result["targets"], self.row["targets"])
        self.assertNotIn("related_cases", result)
        self.assertEqual(result["original_scenario_verdict"], "unverified")
        self.assertEqual(result["fields"]["limitations"], self.row["fields"]["limitations"])
        self.assertEqual(result["fields"]["observation_points_and_comparison"],
                         self.row["fields"]["observation_points_and_comparison"])
        self.assertNotIn("evidence", result["fields"])

    def test_v2_historical_partial_preserves_values_no_related_transfer(self):
        self.schema = "case-register-neutral-screened-draft-v2"
        self.row["fields"]["observation_points_and_comparison"] = {"scope": "partial", "value": [1, 2]}
        self.row["related_cases"] = [{"case_id": "Case_B", "result_transfer": "none"}]
        row2, core2 = copy.deepcopy(self.row), copy.deepcopy(self.base_core)
        row2["case_id"] = core2["case_id"] = "Case_B"
        row2["scenario_verdict"] = core2["scenario_verdict"] = "matched_scoped"
        row2["fields"]["observation_points_and_comparison"] = "LATER_VALUE_MUST_NOT_TRANSFER"
        self.write([self.row, row2], [self.base_core, core2])
        out = reader.read_projection(self.root, self.pin, "case_a")
        self.assertEqual(out["fields"]["observation_points_and_comparison"], {"scope": "partial", "value": [1, 2]})
        self.assertEqual(out["fields"]["limitations"], ["historical partial only", "natural exit UNOBSERVED"])
        self.assertEqual(out["original_scenario_verdict"], "unverified")
        self.assertEqual(out["targets"], self.row["targets"])
        self.assertEqual(out["related_cases"], self.row["related_cases"])
        self.assertNotIn("LATER_VALUE_MUST_NOT_TRANSFER", json.dumps(out))

    def test_typed_targets_and_unknown_values_preserved_in_both_versions(self):
        for version in ("v1", "v2"):
            with self.subTest(version=version):
                self.schema = "case-register-neutral-screened-draft-" + version
                targets = [{"kind": "operator", "name": "?"},
                           {"kind": "expression_function", "name": "CLIENTWIDTH"}]
                self.row["targets"] = self.base_core["targets"] = targets
                self.row["scenario_verdict"] = self.base_core["scenario_verdict"] = "unknown"
                self.row["fields"]["observation_points_and_comparison"] = "UNOBSERVED"
                if version == "v2":
                    self.row["related_cases"] = [{"target": targets[1], "case_id": None,
                                                  "relation": "separate_case", "result_transfer": "none"}]
                self.write()
                out = reader.read_projection(self.root, self.pin, "case_a")
                self.assertEqual(out["targets"], targets)
                self.assertEqual(out["original_scenario_verdict"], "unknown")
                self.assertEqual(out["fields"]["observation_points_and_comparison"], "UNOBSERVED")
                if version == "v2":
                    self.assertEqual(out["related_cases"], self.row["related_cases"])

    def test_v2_without_related_cases_omits_key(self):
        self.schema = "case-register-neutral-screened-draft-v2"
        self.write()
        self.assertNotIn("related_cases", reader.read_projection(self.root, self.pin, "case_a"))

    def test_v1_does_not_display_related_cases_even_if_present(self):
        self.row["related_cases"] = [{"case_id": "Case_B"}]
        self.write()
        self.assertNotIn("related_cases", reader.read_projection(self.root, self.pin, "case_a"))

    def test_private_reference_in_related_cases_is_not_displayed(self):
        self.schema = "case-register-neutral-screened-draft-v2"
        self.row["related_cases"] = [{"path": "private/secret.json"}]
        self.write()
        out = reader.read_projection(self.root, self.pin, "case_a")
        self.assertEqual(out["related_cases"], {"$display_omitted": "private_path_or_reference"})

    def test_additional_observations_and_omission_reasons(self):
        self.row["fields"].update({
            "native_corrected_observations": [{"value": 0, "RESULT": 701}],
            "runs": [{"mode": "native-01", "marker_raw_line_map": [{"marker": "VALUE=100"}],
                      "targets": [{"observed": {"value": "100"}}],
                      "raw_path": r"C:\Users\someone\secret.log"}],
            "unselected_field": "NOT_DISPLAYED", "private/secret-key": "SECRET",
        })
        self.write()
        out = reader.read_projection(self.root, self.pin, "case_a")
        extra = out["additional_observations"]
        self.assertEqual(extra["native_corrected_observations"], [{"value": 0, "RESULT": 701}])
        self.assertEqual(extra["runs"][0]["mode"], "native-01")
        self.assertEqual(extra["runs"][0]["marker_raw_line_map"][0]["marker"], "VALUE=100")
        self.assertEqual(extra["runs"][0]["targets"][0]["observed"]["value"], "100")
        self.assertIn({"path": "/fields/runs/0/raw_path", "reason": "not_selected"}, out["omitted_fields"])
        self.assertIn({"path": "/fields/evidence", "reason": "not_selected"}, out["omitted_fields"])
        self.assertIn({"path": "/fields/<redacted-field-name>", "reason": "not_selected"}, out["omitted_fields"])
        self.assertNotIn("secret.log", json.dumps(out))
        self.assertNotIn("private/secret-key", json.dumps(out))
        self.assertNotIn("NOT_DISPLAYED", json.dumps(out))

    def test_nested_private_paths_withhold_only_affected_observation(self):
        self.row["fields"]["runs"] = [
            {"mode": "native-01", "markers": ["VALUE=1", r"C:\Users\x\private\file"],
             "targets": [{"observed": {"value": 1}}]},
            {"mode": "public-01", "markers": ["VALUE=2"]},
        ]
        self.row["fields"]["native_corrected_observations"] = [{"path": "/home/user/file"}]
        self.write()
        out = reader.read_projection(self.root, self.pin, "case_a")
        self.assertEqual(out["additional_observations"]["runs"][0]["markers"],
                         {"$display_omitted": "private_path_or_reference"})
        self.assertEqual(out["additional_observations"]["runs"][0]["targets"][0]["observed"]["value"], 1)
        self.assertEqual(out["additional_observations"]["runs"][1]["markers"], ["VALUE=2"])
        self.assertEqual(out["additional_observations"]["native_corrected_observations"],
                         {"$display_omitted": "private_path_or_reference"})
        self.assertIn({"path": "/fields/runs/0/markers", "reason": "private_path_or_reference"}, out["omitted_fields"])

    def test_unknown_structure_is_reported_and_modes_keep_unknown(self):
        self.row["fields"]["runs"] = {"unexpected": "VALUE=3"}
        self.row["fields"]["new_modes"] = [{"mode": "native-01", "postfatal_state": "UNKNOWN",
                                           "first_diagnostic": "E_INDEX", "receipt": "hidden"}]
        self.write()
        out = reader.read_projection(self.root, self.pin, "case_a")
        self.assertNotIn("runs", out["additional_observations"])
        self.assertIn({"path": "/fields/runs", "reason": "unsupported_runs_structure"}, out["omitted_fields"])
        self.assertEqual(out["additional_observations"]["new_modes"][0]["postfatal_state"], "UNKNOWN")
        self.assertEqual(out["additional_observations"]["new_modes"][0]["first_diagnostic"], "E_INDEX")
        self.assertIn({"path": "/fields/new_modes/0/receipt", "reason": "not_selected"}, out["omitted_fields"])

    def test_mode_channels_select_output_without_raw_reference(self):
        self.row["fields"]["new_modes"] = [{"mode": "native-01", "channels": [
            {"encoding": "utf-16", "text_verbatim": "VALUE=9", "raw": {"path": "private/x"}},
            {"encoding": "utf-8", "text_verbatim": "file C:\\Users\\someone\\secret"}]}]
        self.write()
        out = reader.read_projection(self.root, self.pin, "case_a")
        channels = out["additional_observations"]["new_modes"][0]["channels"]
        self.assertEqual(channels[0], {"encoding": "utf-16", "text_verbatim": "VALUE=9"})
        self.assertEqual(channels[1]["text_verbatim"], {"$display_omitted": "private_path_or_reference"})
        self.assertIn({"path": "/fields/new_modes/0/channels/0/raw", "reason": "not_selected"}, out["omitted_fields"])
        self.assertIn({"path": "/fields/new_modes/0/channels/1/text_verbatim", "reason": "private_path_or_reference"}, out["omitted_fields"])

    def test_reviewed_note_is_selected_by_exact_value_for_any_case(self):
        value = "Only accepted-* runs use the final fixture hash."
        for version, cid in (("v1", "Case_A"), ("v2", "Different_Case")):
            with self.subTest(version=version, cid=cid):
                self.schema = "case-register-neutral-screened-draft-" + version
                self.row["case_id"] = self.base_core["case_id"] = cid
                self.row["fields"]["note"] = value
                self.write()
                out = reader.read_projection(self.root, self.pin, cid.lower())
                self.assertEqual(out["additional_observations"]["note"], value)
                self.assertFalse(any(x["path"] == "/fields/note" for x in out["omitted_fields"]))
                self.assertEqual(out["original_scenario_verdict"], "unverified")

    def test_other_notes_remain_omitted_without_leaking_values(self):
        values = ("independently audited", "Only accepted-* runs use the final fixture hash. ",
                  "Only accepted-* runs use the final fixture hash. private/secret.txt",
                  {"$case_projection_withheld": "nonincluded_locator"},
                  ["Only accepted-* runs use the final fixture hash."])
        for value in values:
            with self.subTest(value=value):
                self.row["fields"]["note"] = value
                self.write()
                out = reader.read_projection(self.root, self.pin, "case_a")
                self.assertNotIn("note", out["additional_observations"])
                self.assertIn({"path": "/fields/note", "reason": "not_selected"}, out["omitted_fields"])
                serialized = json.dumps(out)
                self.assertNotIn("independently audited", serialized)
                self.assertNotIn("private/secret.txt", serialized)
                self.assertNotIn("nonincluded_locator", serialized)

    def test_note_appears_in_human_and_json_outputs_in_both_languages(self):
        value = "Only accepted-* runs use the final fixture hash."
        self.row["fields"]["note"] = value
        self.write()
        args = [sys.executable, "-I", "-B", str(Path(reader.__file__).resolve()), "case_a",
                "--register-dir", str(self.root), "--manifest-sha256", self.pin]
        for lang in ("ja", "en"):
            human = subprocess.run(args + ["--lang", lang], capture_output=True, encoding="utf-8", timeout=20)
            self.assertEqual(human.returncode, 0, human.stderr)
            self.assertIn(value, human.stdout)
            self.assertNotIn("/fields/note :", human.stdout)
            machine = subprocess.run(args + ["--lang", lang, "--json"], capture_output=True, encoding="utf-8", timeout=20)
            self.assertEqual(machine.returncode, 0, machine.stderr)
            data = json.loads(machine.stdout)
            self.assertEqual(data["additional_observations"]["note"], value)
            self.assertFalse(any(x["path"] == "/fields/note" for x in data["omitted_fields"]))

    def test_selected_note_still_checks_private_paths(self):
        value = "Only accepted-* runs; C:\\Users\\someone\\secret.txt"
        self.row["fields"]["note"] = value
        self.write()
        with mock.patch.object(reader, "DISPLAYABLE_NOTE_VALUES", frozenset({value})):
            out = reader.read_projection(self.root, self.pin, "case_a")
        self.assertEqual(out["additional_observations"]["note"],
                         {"$display_omitted": "private_path_or_reference"})
        self.assertIn({"path": "/fields/note", "reason": "private_path_or_reference"}, out["omitted_fields"])
        self.assertNotIn("secret.txt", json.dumps(out))

    def test_omissions_visible_in_both_languages_and_json(self):
        self.row["fields"]["native_corrected_observations"] = [{"value": 0}]
        self.write()
        script = str(Path(reader.__file__).resolve())
        args = [sys.executable, "-I", "-B", script, "case_a",
                "--register-dir", str(self.root), "--manifest-sha256", self.pin]
        for lang, extra, omitted, reason in (
            ("ja", "追加の保存済み観測", "表示しない欄と理由", "表示対象外"),
            ("en", "Additional saved observations", "Omitted fields and reasons", "not selected for display"),
        ):
            p = subprocess.run(args + ["--lang", lang], capture_output=True, encoding="utf-8", timeout=20)
            self.assertEqual(p.returncode, 0, p.stderr)
            for expected in (extra, omitted, reason, '"value": 0', '/fields/evidence'):
                self.assertIn(expected, p.stdout)
            p = subprocess.run(args + ["--lang", lang, "--json"], capture_output=True, encoding="utf-8", timeout=20)
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
            self.assertIn({"path": "/fields/evidence", "reason": "not_selected"}, out["omitted_fields"])
            self.assertEqual(out["additional_observations"]["native_corrected_observations"][0]["value"], 0)

    def test_withheld_and_missing_field_are_distinct(self):
        marker = {"$case_projection_withheld": "nonincluded_locator"}
        self.row["fields"]["observation_points_and_comparison"] = marker
        del self.row["fields"]["invocation"]
        self.write()
        values = reader.read_projection(self.root, self.pin, "case_a")["fields"]
        self.assertEqual(values["observation_points_and_comparison"], marker)
        self.assertEqual(values["invocation"], {"$field": "not_present"})

    def test_private_reference_withholds_entire_affected_field(self):
        self.row["fields"]["limitations"] = ["unchanged", r"C:\Users\someone\private\receipt.json"]
        self.write()
        values = reader.read_projection(self.root, self.pin, "case_a")["fields"]
        self.assertEqual(values["limitations"], {"$display_omitted": "private_path_or_reference"})
        self.assertEqual(values["fixtures_and_initial_state"], "A=17")

    def test_missing_manifest_file(self):
        (self.root / "README.md").unlink()
        with self.assertRaisesRegex(reader.ReaderError, "unavailable"):
            reader.read_projection(self.root, self.pin, "case_a")

    def test_corruption_in_unrequested_file(self):
        (self.root / "core.jsonl").write_bytes(b"bad\n")
        with self.assertRaisesRegex(reader.ReaderError, "mismatch"):
            reader.read_projection(self.root, self.pin, "case_a")

    def test_wrong_pin(self):
        with self.assertRaisesRegex(reader.ReaderError, "manifest SHA-256 mismatch"):
            reader.read_projection(self.root, "0" * 64, "case_a")

    def test_duplicate_id_case_insensitive(self):
        row2, core2 = copy.deepcopy(self.row), copy.deepcopy(self.base_core)
        row2["case_id"] = core2["case_id"] = "CASE_a"
        self.write([self.row, row2], [self.base_core, core2])
        with self.assertRaisesRegex(reader.ReaderError, "duplicate case ID"):
            reader.read_projection(self.root, self.pin, "case_a")

    def test_detail_core_disagreement(self):
        self.row["scenario_verdict"] = "matched_scoped"
        self.write()
        with self.assertRaisesRegex(reader.ReaderError, "core and detail"):
            reader.read_projection(self.root, self.pin, "case_a")

    def test_missing_case_and_invalid_id(self):
        with self.assertRaisesRegex(reader.ReaderError, "not found"):
            reader.read_projection(self.root, self.pin, "other")
        with self.assertRaisesRegex(reader.ReaderError, "invalid case ID"):
            reader.read_projection(self.root, self.pin, "../other")

    def test_unsupported_schema(self):
        self.schema = "future-version"
        self.write()
        with self.assertRaisesRegex(reader.ReaderError, "unsupported"):
            reader.read_projection(self.root, self.pin, "case_a")

    def test_duplicate_json_keys_fail(self):
        with self.assertRaisesRegex(reader.ReaderError, "duplicate key"):
            reader.parse_json(b'{"a":1,"a":2}')

    def test_malformed_resealed_jsonl_and_non_utf8_are_rejected(self):
        for broken in (b'{"case_id":', b'{"case_id":"x","case_id":"y"}\n',
                       '{"case_id":"x"}\n'.encode("utf-16")):
            with self.subTest(broken=broken):
                self.write()
                (self.root / "cases.jsonl").write_bytes(broken)
                manifest = json.loads((self.root / "manifest.json").read_bytes())
                manifest["files"]["cases.jsonl"] = {"size": len(broken),
                    "sha256": hashlib.sha256(broken).hexdigest()}
                data = bjson(manifest)
                (self.root / "manifest.json").write_bytes(data)
                pin = hashlib.sha256(data).hexdigest()
                with self.assertRaises(reader.ReaderError):
                    reader.read_projection(self.root, pin, "case_a")

    def test_cli_unknown_and_corruption_exit_nonzero_without_result(self):
        script = str(Path(reader.__file__).resolve())
        args = [sys.executable, "-I", "-B", script, "missing_case",
                "--register-dir", str(self.root), "--manifest-sha256", self.pin, "--json"]
        proc = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertIn("not found", proc.stderr)
        (self.root / "core.jsonl").write_bytes(b"damaged\n")
        args[4] = "case_a"
        proc = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertIn("mismatch", proc.stderr)

    def test_unhashable_schema_is_reported_as_reader_error(self):
        self.schema = ["invalid"]
        self.write()
        with self.assertRaisesRegex(reader.ReaderError, "unsupported"):
            reader.read_projection(self.root, self.pin, "case_a")

    def test_cli_json_and_human_output(self):
        script = str(Path(reader.__file__).resolve())
        args = [sys.executable, "-I", "-B", script, "case_a",
                "--register-dir", str(self.root), "--manifest-sha256", self.pin]
        p = subprocess.run(args + ["--json"], capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["case_id"], "Case_A")
        json_default = json.loads(p.stdout)
        p = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("元の scenario_verdict: unverified", p.stdout)
        self.assertIn("historical partial only", p.stdout)
        self.assertIn("対象 [targets]:", p.stdout)
        self.assertIn("関連caseの間で結果を転記しません", p.stdout)
        p_en = subprocess.run(args + ["--lang", "en"], capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(p_en.returncode, 0, p_en.stderr)
        self.assertIn("Original scenario_verdict: unverified", p_en.stdout)
        self.assertIn("Targets [targets]:", p_en.stdout)
        self.assertIn("Results are not transferred between related cases.", p_en.stdout)
        json_ja = subprocess.run(args + ["--json", "--lang", "ja"], capture_output=True, encoding="utf-8", timeout=20)
        json_en = subprocess.run(args + ["--json", "--lang", "en"], capture_output=True, encoding="utf-8", timeout=20)
        self.assertEqual(json_ja.returncode, 0, json_ja.stderr)
        self.assertEqual(json_en.returncode, 0, json_en.stderr)
        self.assertEqual(json.loads(json_ja.stdout), json.loads(json_en.stdout))
        self.assertEqual(json.loads(json_ja.stdout), json_default)

    def test_related_cases_shown_in_both_languages(self):
        self.schema = "case-register-neutral-screened-draft-v2"
        self.row["related_cases"] = [{"case_id": "Case_B", "result_transfer": "none"}]
        self.write()
        script = str(Path(reader.__file__).resolve())
        args = [sys.executable, "-I", "-B", script, "case_a",
                "--register-dir", str(self.root), "--manifest-sha256", self.pin]
        for lang, title in (("ja", "関連case [related_cases]:"), ("en", "Related cases [related_cases]:")):
            p = subprocess.run(args + ["--lang", lang], capture_output=True, encoding="utf-8", timeout=20)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(title, p.stdout)
            self.assertIn("Case_B", p.stdout)
            self.assertIn('"result_transfer": "none"', p.stdout)


if __name__ == "__main__":
    unittest.main()
