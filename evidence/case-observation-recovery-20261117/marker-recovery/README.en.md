# Limited recovery of omitted observations

This supplement adds selected values from structured observations in the corresponding source records to existing case IDs. It contains 38 cases and carries each case ID, typed target, verdict, and existing limitations. These are projections of saved records, not new executions or independent reproductions.

For the four TRYTRANSFER285 cases, integer markers remain grouped by native-01, native-02, and public-01. The supplement contains 90 integers in total. Keys are identifier-shaped. Equal values across modes remain separate observations.

Other cases contain only selected observation fields. Field names such as diagnostic, postfatal_values, value_body_execution, after_present, and done_present do not by themselves establish a measurement. Values, null, UNOBSERVED, false, and non-reach are distinguished using the source value and its parent mode/side. Original raw paths/hashes, process data, and long raw diagnostic lines are not included. Unselected and unknown fields are unevaluated; omission does not show that no observation exists.

Of the 49 omitted diagnostic positions, 40 were empty and 9 were OUTPUTLOG warnings. Empty values remain empty; warning text is shown without its destination. Of 54 postfatal_values positions, 48 are UNOBSERVED and 6 are not_a_fatal_observation. Of 36 value_body_execution positions, 30 are UNOBSERVED and 6 are not_called. after_present and done_present each have 18 boolean positions: 6 true and 12 false. These are field-position counts with duplicates, not case counts.

Each row records a source-record pointer, record-byte SHA-256, and field SHA-256. Verdicts and typed targets are checked against the corresponding case register and source records. Two stopped-state corrections recorded after the earlier 486-record snapshot appear separately in `current-candidate-corrections.jsonl`, with their corrected values, limitations, pointers, and line/record hashes. The earlier projection is not presented as the latest record. Existing values and limitations remain under `base_recovery`; consult the corrected records first for those two cases.

## Verification and source limits

The 486 published-observation JSONL is included at the parent bundle root as `observations.jsonl` and is not duplicated in this child directory. The original 486-record source snapshot pinned inside the verifier (SHA-256 `e11cc635d258949af41d74b30e1157dab02d95b35c9825200066c3ed07a4a515`), source register, current case register, original raw files, source receipts, and independent verifier/manifest pins are not distributed, and no retrieval route is provided here. Source-level verification requires that fixed source snapshot separately from the published projection, plus the source and case registers. If an independent pin is supplied separately, compare the SHA-256 of `verify.py` with it before execution and pass the corresponding independently pinned manifest SHA-256 to the verifier. Without an independent pin, verification can establish only consistency with the included manifest and bundle structure, not publisher or source authenticity.

The verifier checks file hashes, all 38 case identities, marker values by mode, carried limitations, source-field hashes, and typed targets/verdicts. It does not independently establish the meaning of measurements or the authenticity of complete raw data, and it cannot confirm absent source receipts. Distribution terms and rights are outside this supplement's scope.

Run these commands from the parent bundle root (the directory containing `query.py`, `verify_bundle.py`, and `manifest.json`):

```powershell
python -B verify_bundle.py
python -B file_set_manifest.py verify --manifest manifest.json --root public=.
python -B query.py --case CASE_ID
```
[Integrated case/typed-target search in the parent bundle](../query.py)
