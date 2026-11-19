# STRFINDU: saved observations for out-of-range start positions

[日本語](../ja/strfindu-boundary.md)

These four conditions summarize saved Emuera 1.824 +v24 and PyEmuera 3.0.0 records. They are readings of existing evidence, not new executions.

For each condition, `RESULT:0=701`, `RESULT:1=702`, and `RESULTS="AUTO_SENT"` were set before evaluating `STRFINDU` on `"AあBA"`. The first argument was `(RESULT:0 == 701 ? "AあBA" # "BAD_SENT")`.

| Case ID | Search string | Start | Recorded Native return | Recorded PyEmuera result |
|---|---|---:|---:|---|
| `SEARCH02_STRFINDU_A_NEG1` | `"A"` | -1 | -1 | Stopped with `E_INDEX` |
| `SEARCH02_STRFINDU_A_5` | `"A"` | 5 | -1 | Stopped with `E_INDEX` |
| `SEARCH02_STRFINDU_EMPTY_NEG1` | `""` | -1 | -1 | Stopped with `E_INDEX` |
| `SEARCH02_STRFINDU_EMPTY_5` | `""` | 5 | -1 | Stopped with `E_INDEX` |

For each condition the selected Native logs contain the return and subsequent marker, with `RESULT:0=701`, `RESULT:1=702`, and `RESULTS="AUTO_SENT"` recorded at that point. PyEmuera recorded `E_INDEX: STRFINDU start outside string` at line 9 of `ERB/SEARCHBOUND01.ERB` and did not record the corresponding subsequent marker. Values after the stop were not observed.

The recorded singleton stage refers to two Native runs and one PyEmuera run per condition. Another batch stage was also retained, but this document does not establish overall singleton/batch consistency. Native was terminated during cleanup; its natural exit and exit code were not observed. These four conditions do not establish compatibility for all STRFINDU inputs or other start positions.

Find the case ID in the [case list](../../evidence/case-register-2898-20261117/cases.jsonl). For example, run `python -B tools/query.py SEARCH02_STRFINDU_A_NEG1` from the repository root to locate the case projection. Some detailed comparison fields are withheld there; the table above is a bounded reading of the retained comparison records and raw output.

For different conditions, see [STRFINDUBASE01](../../evidence/external-scalar-29-package-20261117/evidence/external-scalar-observations-20261117/OBSERVATIONS_en.md#c021--strfindubase01) and the [empty-string/end-position rerun](../../evidence/new-replay-20261116/public/README.md). Their inputs and observation conditions differ from the four cases above.

This record does not include the original fixtures, configuration, executables, receipts, comparison records, or raw outputs for the four conditions above. It is not sufficient to independently reproduce or verify the historical execution.
