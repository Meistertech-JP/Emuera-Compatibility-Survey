# Display a pinned case projection

[日本語](CASE_READER.ja.md)

`case_reader.py` looks up a case ID in an existing case register and displays typed targets, the original `scenario_verdict`, projection state, observations and comparison, fixture and initial state, input and execution conditions, limitations, and selected additional observations. It requires Python 3.10 or newer and only the standard library. No external engine or network is needed.

From the repository root, specify the register directory and the SHA-256 of **manifest.json itself** obtained through a separate trusted channel:

```powershell
python -I -B tools/case_reader.py PRINTVW_POSTWAIT01 --register-dir evidence/case-register-2898-20261117 --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --lang en
```

For another distribution, supply its directory and manifest SHA. Case IDs are case-insensitive. `--lang ja` is the default; `--lang en` selects English labels. `--json` emits UTF-8 JSON whose contents are the same for either language. Original target and field values are not translated.

`targets` retains its original structure, including `kind` and `name`. For v2, `related_cases` is displayed only when present, preserving original values including `null`; it is not displayed for v1. The reader does not follow related cases to transfer results or convert unknown and unverified observations to success. Exit 0 means lookup and checks succeeded; it does not mean the case passed or establish compatibility. An unknown case ID, invalid input, missing file, or integrity mismatch results in exit 2 and no result on stdout.

When present, additional observations include `native_corrected_observations`, `native_selected_observations`, native and public markers, selected snapshots, comparison axes, stop lines and selected traces. For `runs` and `new_modes`, selected fields such as execution mode, observations, diagnostics, stops and unobserved state are displayed. For example, `runs` retains `marker_raw_line_map` and `targets` per mode, and `new_modes` displays saved channel text and encoding. Unsupported execution-list structures are omitted and reported.

`note` values are not displayed wholesale. Currently, only the reviewed exact string `Only accepted-* runs use the final fixture hash.` is displayed, regardless of case ID. It states a condition in the original projection; it does not mean the CLI independently verified the fixture hash or its association with those runs. Other `note` values are omitted and reported.

**The display does not include every field in the projection.** It omits values of unselected fields such as evidence, review and execution paths, and lists their locations and reasons under `Omitted fields and reasons`. Selected fields withheld because of a possible private path are also listed. JSON uses `additional_observations` and `omitted_fields`, with reason codes `not_selected`, `private_path_or_reference`, and `unsupported_runs_structure`. Locations refer to the original `cases.jsonl` record; a field name that cannot be displayed safely is replaced by `<redacted-field-name>`. Omitted fields can contain observations, so omission does not mean an observation is absent. Consult the case in the specified projection when needed.

Supported schemas are `case-register-neutral-screened-draft-v1` and `case-register-neutral-screened-draft-v2`. The reader checks the manifest SHA, the recorded sizes and hashes of both READMEs, `cases.jsonl` and `core.jsonl`, record counts, duplicate IDs, and core/detail correspondence across all records. It rejects unsupported file sets and corruption detected by those checks. It does not validate every field's meaning or suitability for publication.

A manifest SHA measured from the same distribution does not authenticate its source or the manifest. Obtain the SHA through an independently trusted channel and verify the CLI itself.

Structured values, `$case_projection_withheld`, and `[WITHHELD]` within strings remain unchanged and are distinct from a missing field represented as `{"$field": "not_present"}`. If a displayed field appears to contain a private path, the entire field is replaced with `{"$display_omitted": "private_path_or_reference"}`. This detection is not a comprehensive privacy review.

The reader does not authenticate original raw data, receipts, or source records, or reproduce past executions. Some projection content still needs individual review; being displayable does not imply rights, privacy, or publication approval.
