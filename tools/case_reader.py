#!/usr/bin/env python3
"""Read selected fields from an explicitly pinned case-register projection."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMAS = {"case-register-neutral-screened-draft-v1",
           "case-register-neutral-screened-draft-v2"}
FILES = {"README.ja.md", "README.md", "cases.jsonl", "core.jsonl"}
CORE = {"case_id", "targets", "scenario_verdict", "survey_pointer",
        "trace_aliases", "target_positions_outside_694", "runtime_observation_context"}
DISPLAY_FIELDS = (
    ("観測・比較", "Observations and comparison", "observation_points_and_comparison"),
    ("fixture・初期状態", "Fixture and initial state", "fixtures_and_initial_state"),
    ("入力・実行条件", "Input and execution conditions", "invocation"),
    ("制限", "Limitations", "limitations"),
)
# Explicitly selected observations, not arbitrary evidence, review, or paths.
ADDITIONAL_FIELDS = frozenset({
    "native_corrected_observations", "native_selected_observations",
    "native_markers", "public_markers", "selected_snapshots",
    "comparison_axes", "stop_lines", "secondary_observation", "actual_traces",
    "actual_invocation_lines", "phase_input_lines", "literal_trigger_body",
    "comparison_class", "comparison_outcome", "comparison_category",
    "difference_category", "strict_output_match", "fatal",
})
# A reviewed fixture-pin applicability condition. Do not generalize this to
# other notes: they can contain private references or unreviewed audit claims.
DISPLAYABLE_NOTE_VALUES = frozenset({"Only accepted-* runs use the final fixture hash."})
RUN_FIELDS = frozenset({"mode", "marker_raw_line_map", "markers", "targets",
                        "diagnostic_text", "stop", "natural_exit_observed",
                        "helper_cleanup_termination"})
MODE_FIELDS = frozenset({"mode", "phase", "AFTER_observed", "before_observed",
                         "cause_literal", "fault_instruction", "first_diagnostic_line",
                         "first_diagnostic", "hidden_postfatal_state", "prefix_marker_lines",
                         "before_invalid", "body_after", "last_valid", "native_natural_exit",
                         "physical_stopline", "postfatal_R0_R1_RS_A", "postfatal_state",
                         "target", "top_after", "helper_zero_not_native_exit",
                         "raw_segments", "stderr_segments"})
CHANNEL_FIELDS = frozenset({"encoding", "text_verbatim"})
SAFE_KEY = re.compile(r"^[A-Za-z0-9_]+$")
ID = re.compile(r"^[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[a-fA-F0-9]{64}$")
PRIVATE_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\[a-z0-9_.-]+\\|"
    r"(?:^|[\s\"'(])/(?:users|home|mnt|tmp|private|workspace)/|"
    r"(?:^|[/\\\s\"'(])(?:private|internal)[/\\])"
)


class ReaderError(Exception):
    pass


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ReaderError("JSON contains a duplicate key")
        obj[key] = value
    return obj


def parse_json(data):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=lambda _: (_ for _ in ()).throw(ReaderError("non-finite JSON value")))
    except (ValueError, UnicodeError) as exc:
        raise ReaderError("invalid UTF-8 JSON") from exc


def load_rows(raw):
    lines = raw.splitlines()
    if not lines or any(not line.strip() for line in lines):
        raise ReaderError("empty or blank JSONL record")
    rows = [parse_json(line) for line in lines]
    if any(not isinstance(row, dict) for row in rows):
        raise ReaderError("JSONL record is not an object")
    return rows


def has_private_reference(value):
    if isinstance(value, str):
        return bool(PRIVATE_PATH.search(value))
    if isinstance(value, list):
        return any(has_private_reference(item) for item in value)
    if isinstance(value, dict):
        return any(has_private_reference(k) or has_private_reference(v)
                   for k, v in value.items())
    return False


def display_value(value):
    # Do not try to repair or reword the public projection. If a private path
    # slips through, withhold the whole field and disclose that omission.
    if has_private_reference(value):
        return {"$display_omitted": "private_path_or_reference"}
    return value


def field_path(prefix, key):
    # Field names are untrusted too; do not echo a private or arbitrary key.
    return prefix + "/" + (key if SAFE_KEY.fullmatch(key) and not has_private_reference(key)
                           else "<redacted-field-name>")


def selected_value(value, path, omissions):
    if has_private_reference(value):
        omissions.append({"path": path, "reason": "private_path_or_reference"})
    return display_value(value)


def select_records(value, prefix, allowed, omissions, nested_channels=False):
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        omissions.append({"path": prefix, "reason": "unsupported_runs_structure"})
        return None
    result = []
    for index, run in enumerate(value):
        current = {}
        for key, item in run.items():
            path = field_path(prefix + "/" + str(index), key)
            if key in allowed:
                current[key] = selected_value(item, path, omissions)
            elif nested_channels and key == "channels":
                channels = select_records(item, path, CHANNEL_FIELDS, omissions)
                if channels is not None:
                    current[key] = channels
            else:
                omissions.append({"path": path, "reason": "not_selected"})
        result.append(current)
    return result


def read_projection(directory, pin, requested):
    if not SHA.fullmatch(pin):
        raise ReaderError("manifest SHA-256 must be 64 hexadecimal characters")
    if not ID.fullmatch(requested):
        raise ReaderError("invalid case ID")
    try:
        raw_manifest = (directory / "manifest.json").read_bytes()
    except OSError as exc:
        raise ReaderError("manifest is unavailable") from exc
    if hashlib.sha256(raw_manifest).hexdigest() != pin.lower():
        raise ReaderError("manifest SHA-256 mismatch")
    manifest = parse_json(raw_manifest)
    if (not isinstance(manifest, dict) or not isinstance(manifest.get("schema"), str)
            or manifest["schema"] not in SCHEMAS):
        raise ReaderError("unsupported manifest schema")
    entries = manifest.get("files")
    if not isinstance(entries, dict) or set(entries) != FILES:
        raise ReaderError("unexpected manifest file set")
    raw_files = {}
    for name in sorted(FILES):
        entry = entries[name]
        if (not isinstance(entry, dict) or type(entry.get("size")) is not int
                or entry["size"] < 0 or not isinstance(entry.get("sha256"), str)
                or not SHA.fullmatch(entry["sha256"])):
            raise ReaderError("invalid file metadata in manifest")
        try:
            raw = (directory / name).read_bytes()
        except OSError as exc:
            raise ReaderError("a manifest file is unavailable: " + name) from exc
        if len(raw) != entry["size"] or hashlib.sha256(raw).hexdigest() != entry["sha256"].lower():
            raise ReaderError("manifest file mismatch: " + name)
        raw_files[name] = raw
    details, cores = load_rows(raw_files["cases.jsonl"]), load_rows(raw_files["core.jsonl"])
    count = manifest.get("records")
    if type(count) is not int or count < 1 or count != len(details) or count != len(cores):
        raise ReaderError("record count mismatch")
    seen = set()
    found = None
    for line, (detail, core) in enumerate(zip(details, cores), 1):
        cid = detail.get("case_id")
        if not isinstance(cid, str) or not ID.fullmatch(cid):
            raise ReaderError("invalid registered case ID")
        norm = cid.casefold()
        if norm in seen:
            raise ReaderError("duplicate case ID, ignoring case")
        seen.add(norm)
        if set(core) != CORE or any(key not in detail or detail[key] != core[key] for key in CORE):
            raise ReaderError("core and detail records disagree")
        if (not isinstance(detail.get("fields"), dict)
                or not isinstance(detail.get("scenario_verdict"), str)
                or not isinstance(detail.get("projection_state"), str)):
            raise ReaderError("invalid detail record")
        if norm == requested.casefold():
            found = (line, detail)
    if found is None:
        raise ReaderError("case ID not found")
    line, row = found
    result = {
        "case_id": row["case_id"],
        "targets": display_value(row["targets"]),
        "original_scenario_verdict": display_value(row["scenario_verdict"]),
        "projection_state": display_value(row["projection_state"]),
        "manifest_schema": manifest["schema"],
        "manifest_sha256": pin.lower(),
        "record": {"file": "cases.jsonl", "line": line},
        "fields": {},
        "additional_observations": {},
        "omitted_fields": [],
    }
    omissions = result["omitted_fields"]
    for key in ("targets", "scenario_verdict", "projection_state"):
        if has_private_reference(row[key]):
            omissions.append({"path": "/" + key, "reason": "private_path_or_reference"})
    if manifest["schema"] == "case-register-neutral-screened-draft-v2" and "related_cases" in row:
        result["related_cases"] = selected_value(row["related_cases"], "/related_cases", omissions)
    for _, _, key in DISPLAY_FIELDS:
        result["fields"][key] = (selected_value(row["fields"][key], "/fields/" + key, omissions)
                                 if key in row["fields"] else {"$field": "not_present"})
    for key, value in row["fields"].items():
        if key in {item[2] for item in DISPLAY_FIELDS}:
            continue
        path = field_path("/fields", key)
        if key in ADDITIONAL_FIELDS:
            result["additional_observations"][key] = selected_value(value, path, omissions)
        elif key == "note" and isinstance(value, str) and value in DISPLAYABLE_NOTE_VALUES:
            result["additional_observations"][key] = selected_value(value, path, omissions)
        elif key in ("runs", "new_modes"):
            runs = select_records(value, path, RUN_FIELDS if key == "runs" else MODE_FIELDS,
                                  omissions, nested_channels=(key == "new_modes"))
            if runs is not None:
                result["additional_observations"][key] = runs
        else:
            omissions.append({"path": path, "reason": "not_selected"})
    shown_top = {"case_id", "targets", "scenario_verdict", "projection_state", "fields"}
    if "related_cases" in result:
        shown_top.add("related_cases")
    for key in row:
        if key not in shown_top:
            omissions.append({"path": field_path("", key), "reason": "not_selected"})
    return result


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Read an existing, pinned case-register projection.")
    parser.add_argument("case_id")
    parser.add_argument("--register-dir", required=True, type=Path)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--lang", choices=("ja", "en"), default="ja")
    args = parser.parse_args(argv)
    try:
        result = read_projection(args.register_dir, args.manifest_sha256, args.case_id)
    except ReaderError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("case ID:", result["case_id"])
        print("元の scenario_verdict:" if args.lang == "ja" else "Original scenario_verdict:",
              result["original_scenario_verdict"])
        print("投影の状態:" if args.lang == "ja" else "Projection state:", result["projection_state"])
        print("参照: cases.jsonl 行" if args.lang == "ja" else "Reference: cases.jsonl line",
              result["record"]["line"])
        print("manifest:", result["manifest_schema"], result["manifest_sha256"])
        print("\n対象 [targets]:" if args.lang == "ja" else "\nTargets [targets]:")
        print(json.dumps(result["targets"], ensure_ascii=False, indent=2))
        if "related_cases" in result:
            print("\n関連case [related_cases]:" if args.lang == "ja" else "\nRelated cases [related_cases]:")
            print(json.dumps(result["related_cases"], ensure_ascii=False, indent=2))
        for label_ja, label_en, key in DISPLAY_FIELDS:
            label = label_ja if args.lang == "ja" else label_en
            print("\n" + label + " [" + key + "]:")
            value = result["fields"][key]
            print(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2))
        if result["additional_observations"]:
            print("\n追加の保存済み観測:" if args.lang == "ja" else "\nAdditional saved observations:")
            print(json.dumps(result["additional_observations"], ensure_ascii=False, indent=2))
        if result["omitted_fields"]:
            reasons = ({"not_selected": "表示対象外", "private_path_or_reference": "非公開パスまたは参照の可能性",
                        "unsupported_runs_structure": "対応していない実行一覧の構造"} if args.lang == "ja" else
                       {"not_selected": "not selected for display", "private_path_or_reference": "possible private path or reference",
                        "unsupported_runs_structure": "unsupported execution list structure"})
            print("\n表示しない欄と理由:" if args.lang == "ja" else "\nOmitted fields and reasons:")
            for item in result["omitted_fields"]:
                print("-", item["path"], ":", reasons[item["reason"]])
        if args.lang == "ja":
            print("\n関連caseの間で結果を転記しません。表示は保存された投影であり、元rawの真正性・再現や追加の観測を証明しません。")
        else:
            print("\nResults are not transferred between related cases. This saved projection does not establish original raw authenticity, reproduction, or additional observations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
