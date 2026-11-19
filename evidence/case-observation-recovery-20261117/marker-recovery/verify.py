import argparse
import hashlib
import json
import pathlib
import re

SOURCE_SHA = "32f008d1e6ebf6a373a080484b8a493d173bcff6b911249d8b6bf6e894295195"
CANDIDATE_SHA = "53558a68414a8826fdea4450b543b21c41e358bf60b66d3c3cc7394f7b3fbf86"
BASE_SHA = "e11cc635d258949af41d74b30e1157dab02d95b35c9825200066c3ed07a4a515"
IDENT = re.compile(r"^[A-Za-z0-9_]+$")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def enc(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def subset(public, source, key=""):
    if type(public) is not type(source):
        return False
    if isinstance(public, dict):
        return all(child_key in source and subset(value, source[child_key], child_key) for child_key, value in public.items())
    if isinstance(public, list):
        return len(public) == len(source) and all(subset(a, b, key) for a, b in zip(public, source))
    if key == "value_body_execution" and source == "UNOBSERVED; source placement is separate reasoning":
        return public == "UNOBSERVED"
    if key == "diagnostic" and source == "[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.":
        return public == "PyEmuera OUTPUTLOG warning; log destination omitted"
    return public == source


def source_record_spans(raw):
    text = raw.decode("utf-8")
    rows = json.loads(text)["records"]
    decoder = json.JSONDecoder()
    pos = re.search(r'"records"\s*:\s*\[', text).end()
    spans = []
    for row in rows:
        while text[pos] in " \t\r\n,":
            pos += 1
        parsed, end = decoder.raw_decode(text, pos)
        if parsed != row:
            raise ValueError("source span parse mismatch")
        spans.append(text[pos:end].encode("utf-8"))
        pos = end
    return rows, spans


def verify_manifest(root, pinned):
    manifest_path = root / "manifest.json"
    if sha(manifest_path.read_bytes()) != pinned:
        raise ValueError("external manifest pin mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("symlink rejected")
        if path.is_file() and path.name != "manifest.json":
            rel = path.relative_to(root).as_posix()
            actual[rel] = {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
    if manifest != {"algorithm": "sha256", "files": actual}:
        raise ValueError("manifest inventory/hash mismatch")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=pathlib.Path)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--source-register", required=True, type=pathlib.Path)
    parser.add_argument("--candidate-cases", required=True, type=pathlib.Path)
    parser.add_argument("--base-observations", required=True, type=pathlib.Path)
    args = parser.parse_args()
    verify_manifest(args.root, args.manifest_sha256.lower())
    source_raw = args.source_register.read_bytes()
    candidate_raw = args.candidate_cases.read_bytes()
    base_raw = args.base_observations.read_bytes()
    if sha(source_raw) != SOURCE_SHA or sha(candidate_raw) != CANDIDATE_SHA or sha(base_raw) != BASE_SHA:
        raise ValueError("source/candidate/base pin mismatch")
    source, spans = source_record_spans(source_raw)
    candidate = read_jsonl(args.candidate_cases)
    base = read_jsonl(args.base_observations)
    if len(source) != 2898 or len(candidate) != 2898:
        raise ValueError("register length mismatch")
    for a, b in zip(source, candidate):
        if a["case_id"] != b["case_id"] or a.get("targets") != b.get("targets") or a.get("scenario_verdict") != b.get("scenario_verdict"):
            raise ValueError("current candidate case/typed-target/verdict mismatch")
    source_by_id = {row["case_id"]: (i, row, spans[i]) for i, row in enumerate(source)}
    candidate_by_id = {row["case_id"]: row for row in candidate}
    candidate_lines = candidate_raw.splitlines(keepends=True)
    base_by_id = {row["case_id"]: row for row in base}
    published_base = read_jsonl(args.root.parent / "observations.jsonl")
    published_base_by_id = {row["case_id"]: row for row in published_base}
    observations = read_jsonl(args.root / "risk-observations.jsonl")
    expected_ids = {
        "TRYTRANSFER285_TRYCCALL_supplied", "TRYTRANSFER285_TRYCCALL_default",
        "TRYTRANSFER285_TRYCALL_found_callee_fault", "TRYTRANSFER285_TRYJUMP_found_callee_fault",
        "SPRITECREATED_EXISTING_RESOURCE_DIRECT_20261113", "SEARCH02_STRFINDU_A_NEG1",
        "SEARCH02_STRFINDU_A_5", "SEARCH02_STRFINDU_EMPTY_NEG1", "SEARCH02_STRFINDU_EMPTY_5",
        "MINMAX_ERR04_MIN_EMPTY", "MINMAX_ERR04_MIN_WRONG_TYPE", "MINMAX_ERR04_MAX_EMPTY",
        "MINMAX_ERR04_MAX_WRONG_TYPE", "NUMOVER06_TOINT_I64_OVERFLOW", "NUMOVER06_ISNUMERIC_I64_OVERFLOW",
        "OPTYPE07_DIV_MIXED_REACHED_NO", "OPTYPE07_DIV_STRSTR_REACHED_NO", "OPTYPE07_DIV_UNCALLED_BOTH_NO",
        "OPTYPE07_MOD_MIXED_REACHED_NO", "OPTYPE07_MOD_STRSTR_REACHED_NO", "OPTYPE07_MOD_UNCALLED_BOTH_NO",
        "INCDEC08_INC_NONLV_DIAGNOSTIC", "INCDEC08_DEC_NONLV_DIAGNOSTIC",
        "CATCH_REQUIRED_ORPHAN_ENDCATCH_20261115", "CATCH_REQUIRED_MISSING_ENDCATCH_20261115",
        "REND_GOTO_ZERO_NESTED_NORMAL_20261115", "GOTO_MISSING_LOCAL_LABEL_20261115",
        "FIND_BOUNDARY_NORMAL_20261115", "FIND_BOUNDARY_NORMAL_REMAINING_20261115",
        "FIND_BOUNDARY_FINDCHARA_REVERSE_ISOLATED_20261115", "FIND_BOUNDARY_FINDLASTCHARA_REVERSE_ISOLATED_20261115",
        "FIND_BOUNDARY_FINDCHARA_END_OUT_OF_RANGE_20261115", "FIND_BOUNDARY_FINDLASTCHARA_END_OUT_OF_RANGE_20261115",
        "ARRAY_BOUNDARY_NORMAL_CORRECTED_20261115", "LEVEL_BOUNDARY_GETPALAMLV_NEGATIVE_20261115",
        "LEVEL_BOUNDARY_GETPALAMLV_SIZEPLUS1_20261115", "LEVEL_BOUNDARY_GETEXPLV_NEGATIVE_20261115",
        "LEVEL_BOUNDARY_GETEXPLV_SIZEPLUS1_20261115",
    }
    if len(observations) != 38 or {r["case_id"] for r in observations} != expected_ids:
        raise ValueError("risk case set mismatch")
    transfer_count = 0
    for public in observations:
        case_id = public["case_id"]
        i, original, record_bytes = source_by_id[case_id]
        field = original["observation_points_and_comparison"]
        parsed = json.loads(field) if isinstance(field, str) else field
        candidate_row = candidate_by_id[case_id]
        base_row = base_by_id[case_id]
        if public["source_pointer"] != f"/records/{i}/observation_points_and_comparison":
            raise ValueError("source pointer mismatch: " + case_id)
        if public["source_record_bytes_sha256"] != sha(record_bytes) or public["source_field_sha256"] != sha(enc(field)):
            raise ValueError("source hash mismatch: " + case_id)
        if public["selection_status"] == "selected_safe_fields":
            if not public["projection"] or not subset(public["projection"], parsed):
                raise ValueError("projection value/type/mode mismatch: " + case_id)
        elif public["selection_status"] == "no_safe_leaf_selected":
            if public["projection"] is not None or case_id not in {"REND_GOTO_ZERO_NESTED_NORMAL_20261115", "GOTO_MISSING_LOCAL_LABEL_20261115"}:
                raise ValueError("unexpected empty projection: " + case_id)
        else:
            raise ValueError("unknown selection status: " + case_id)
        if public["scenario_verdict"] != candidate_row["scenario_verdict"] or public["targets"] != candidate_row["targets"]:
            raise ValueError("typed target/verdict mismatch: " + case_id)
        if public["base_recovery"].get("limitations") != base_row.get("limitations"):
            raise ValueError("base limitations mismatch: " + case_id)
        if case_id in {"REND_GOTO_ZERO_NESTED_NORMAL_20261115", "GOTO_MISSING_LOCAL_LABEL_20261115"}:
            if "recovered" in public["base_recovery"] or public["base_recovery"].get("inherited_work_mapping_removed") is not True:
                raise ValueError("inherited internal mapping must be removed: " + case_id)
            retained = published_base_by_id[case_id].get("recovered")
            if not isinstance(retained, list) or len(retained) != 1 or not subset(retained[0].get("value"), parsed):
                raise ValueError("retained observation is not a typed source subset: " + case_id)
            def contains_private_work_key(value):
                if isinstance(value, dict):
                    return "current_required_work_mapping" in value or any(contains_private_work_key(v) for v in value.values())
                if isinstance(value, list):
                    return any(contains_private_work_key(v) for v in value)
                return False
            if contains_private_work_key(retained):
                raise ValueError("private work mapping remains in retained observation: " + case_id)
        elif public["base_recovery"].get("recovered") != base_row.get("recovered"):
            raise ValueError("base recovered mismatch: " + case_id)
        if public["base_recovery"]["scenario_verdict"] != base_row["scenario_verdict"] or public["base_recovery"]["targets"] != base_row["targets"]:
            raise ValueError("base typed target/verdict mismatch: " + case_id)
        if case_id.startswith("TRYTRANSFER285_"):
            modes = public["projection"].get("observations")
            if set(modes or {}) != {"native-01", "native-02", "public-01"}:
                raise ValueError("transfer mode set mismatch")
            for mode in ("native-01", "native-02", "public-01"):
                marker = modes[mode].get("markers")
                if not marker or any(not IDENT.fullmatch(key) or type(value) is not int for key, value in marker.items()):
                    raise ValueError("transfer marker key/value type mismatch")
                if marker != parsed["observations"][mode]["markers"]:
                    raise ValueError("transfer marker changed or moved between modes")
                transfer_count += len(marker)
    if transfer_count != 90:
        raise ValueError("transfer marker count mismatch")
    corrections = read_jsonl(args.root / "current-candidate-corrections.jsonl")
    corrected_ids = {"NUM_ASSIGN_STOPPED_STATE_CONTROL_20261116", "NUM_ASSIGN_STOPPED_STATE_BADINDEX_20261116"}
    if len(corrections) != 2 or {row["case_id"] for row in corrections} != corrected_ids:
        raise ValueError("current candidate correction case set mismatch")
    for row in corrections:
        index = row["candidate_line_index_zero_based"]
        current = candidate_by_id[row["case_id"]]
        original = source_by_id[row["case_id"]][1]
        if row["candidate_line_bytes_sha256"] != sha(candidate_lines[index]) or row["candidate_record_sha256"] != sha(enc(current)):
            raise ValueError("current candidate correction hash mismatch: " + row["case_id"])
        if row["candidate_snapshot_sha256"] != CANDIDATE_SHA or row["source_survey_pointer"] != current.get("survey_pointer"):
            raise ValueError("current candidate correction pointer/pin mismatch: " + row["case_id"])
        if row["scenario_verdict"] != current["scenario_verdict"] or row["targets"] != current["targets"]:
            raise ValueError("current candidate correction typed identity mismatch: " + row["case_id"])
        if row["targets"] != original["targets"] or row["scenario_verdict"] != original["scenario_verdict"]:
            raise ValueError("corrected candidate identity differs from source register: " + row["case_id"])
        expected_fields = {key: current["fields"][key] for key in (
            "fixtures_and_initial_state", "observation_points_and_comparison", "limitations")}
        if row["fields"] != expected_fields:
            raise ValueError("candidate correction field overwritten: " + row["case_id"])
    print(json.dumps({"status": "PASS", "records": len(observations), "transfer_integer_markers": transfer_count,
                      "current_candidate_corrections": len(corrections),
                      "source_sha256": SOURCE_SHA, "candidate_sha256": CANDIDATE_SHA,
                      "base_observations_sha256": BASE_SHA, "manifest_sha256": args.manifest_sha256.lower()}, indent=2))


if __name__ == "__main__":
    main()
