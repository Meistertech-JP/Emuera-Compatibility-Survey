# Reading the survey data

[日本語](../ja/results.md) | [Overview](../../README.md)

The [offline validation guide](offline-validation.md) provides commands and scope for checking selected bundles.

[Examples of observed results](observations.md) show the conditions and saved output from both engines.

The [bounded saved-observation lookup](../../differences/saved-observation-lookup-20261117/README.md#english) searches recorded values, cases, and references for 129 selected typed items, including the status of items without a case-specific field.

The [records for 486 cases](../../evidence/case-observation-recovery-20261117/README.md) can be searched by case ID or target. Of these, 95 have saved observation descriptions in the `recovered` field; that field is empty for the remaining 391. The original raw files and source records are not included, so the included records alone support only limited independent verification of the historical executions.

The [four saved STRFINDU boundary observations](strfindu-boundary.md) describe the selected inputs and saved results. The original fixtures and raw output are not included.

The [recorded `TWAIT 0,1` observation](../../evidence/twaitzero-observation-20261117/README.md) shows the Native screen and PyEmuera diagnostic with their respective conditions and observation limits.

The [recorded compound-assignment trailing-comma cases](../../evidence/compound-trailing-comma-20261117/README_en.md) show Native output and PyEmuera syntax diagnostics for two inputs.

The [three recorded `DELCHARA` conditions](../../evidence/delchara-diagnostics-20261117/README.md) show the Native diagnostics, PyEmuera diagnostics, selected state, and stopping positions.

The [recorded `LOADGLOBAL` observations with truncated save data](../../evidence/loadglobal-corrupt-20261117/README_en.md) show the selected loading results for inputs created in the two engines' different formats.

The [saved stopped-state records](../../evidence/stopped-state-observations-20261117/README_en.md) distinguish values read directly in Native from values inferred from PyEmuera's recorded storage and implementation. The original observation raw files are not included.

[PRINTDATA and STRDATA string state and log wrapping](printdata-local.md) distinguishes the saved native and PyEmuera output from source-derived inference.

[Saved output for 24 operator conditions](operator-264-observations.md) presents the Native and PyEmuera output and diagnostics for each registered case. These cases are already in the ledger and are not counted again.

The shared machine-readable data is in [`results/survey.json`](../../results/survey.json). Its `targets` use a typed key (`kind`, `name`). Each target lists related case IDs and its scoped decision. `main_scenarios` retains the original classification for each of the 2,898 registered scenarios. `supplemental_items`, `supplemental_modes`, and `grammar_cases` are separate populations. A mode count is not a count of processes or independent bugs.

The [target and requirement trace](../../evidence/694-target-trace-20261117/README.md) connects 3,359 requirements for the 694 targets to selected evidence available in this material. It marks original acceptance records that remain private; a listed requirement does not by itself make the original observation independently verifiable.

Use `python -B tools/query.py <name-or-case-id>` from the project root to look up an exact name or ID. `python -B results/verify.py` validates the neutral index and its file hashes. These tools do not infer source evidence from a name or certify that every linked scenario exercised the target; consult the individual case's evidence and scope.

Examples for reading search results (run commands from the repository root):

- `python -B tools/query.py 'assignment_syntax:*='` returns the typed target and related cases. An associated role does not establish separate execution: for example, inspect the fixtures and mode-specific output for [the two trailing-comma cases](../../evidence/compound-trailing-comma-20261117/README_en.md).
- `python -B tools/query.py TWAITZERO01` returns `cases`, `case_register_projection`, and a link in `selected_evidence_links` to the [saved TWAIT 0,1 observation](../../evidence/twaitzero-observation-20261117/README.md). `NO_RUNTIME_OBSERVATION_KEY_FOUND` in `runtime_observation_context` concerns keys in the case projection; it does not mean that no observation exists in another bundle.
- For `python -B tools/query.py E143E`, `detail_record` in `case_register_projection` identifies the case line in [cases.jsonl](../../evidence/case-register-2898-20261117/cases.jsonl). Included fields describe the setup and comparison scope, but the query does not emit the detail fields, and the original evidence and review are withheld. Checking those originals requires source records not included here; this does not establish that no other saved evidence exists.
- To read a case's conditions, selected observations and limitations directly, provide its ID and a trusted manifest SHA to the [case reader](../../tools/CASE_READER.md). The displayed projection does not authenticate or reproduce the original raw data.
- Searching the grammar case `COLON_NORMAL_COMPAT_RAND_YES` returns `representative_evidence` and `extra_evidence_links`. For the supplemental case `SUP_LABEL_DOLLAR_DUPLICATE_NO_20261115`, follow `manifest` and `manifest_pointer` in `extra_evidence_links` to the case in the [saved observation bundle](../../evidence/syntax-supplemental-20261117/README.md). The selected bundle omits the probe text, original receipts and other materials; not every grammar or supplemental case has the same route.

The historical scenario register records 1,711 scoped matches, 1,071 scoped differences, 99 unverified cases and 17 blocked or evidence-deficient cases. A target may have observations in multiple categories. The recorded target decisions cover a separate population of 201 scoped matches, 294 documented differences and 199 scoped differences. These counts describe the ledger's categories and can include several observations of the same underlying difference.

The 116 originally unverified or blocked records were organized as 68 retained historical failures or unobserved attempts, 42 observations outside the finite comparison scope, and six initially unresolved mappings. Later work mapped those six to the finite acceptance scope; that mapping does not mean the measurements succeeded. Where later cases support finite acceptance, they remain separate executions and do not rewrite the original case verdicts.

For 38 graphics cases among the 42, [original native records and limited observations](../../evidence/graphics-38-cases-20261117/README.md) are available. Two GCLEAR cases also have separate later native GUI trials. These observations do not change the original finite-comparison classification or establish agreement between both engines across all conditions.

[`differences/catalog.json`](../../differences/catalog.json) is an index of recorded differences, not a diagnosis of their root causes. Four entries currently have [representative observations](../../differences/representative-20261116/README.en.md). The full chain from each typed target through conditions, both raw observations and adjudication is not available in this material; do not interpret an index entry as independent reproduction of the original result.

The root `evidence_availability` in `catalog.json` and `survey.json` describes the original survey projection; it is not a current inventory of evidence added later. `python -B tools/query.py OPCONT268_strcmp-ge` returns a source and JSON pointer in `native_oracle_observations` for [33 selected conditions](../../evidence/native-oracle-20261117/evidence/operator-268-20261117/README.md), along with `selected_condition` and `selected_observations` copied from the pinned selection index. These are index values; semantic equivalence to the source has not been verified. They are projections from two Native and one PyEmuera shared runs; the original fixture, config and raw output are not included. `native_oracle_availability` describes only this 113-row index: no match does not mean that evidence is absent from other collections. A missing collection directory is `NOT_PRESENT`; an empty directory or missing or inconsistent required files is `INCONSISTENT`. A query can exit 0 when an existing case is found even if this collection is inconsistent. `--partial` does not reflect this collection's inconsistency in the exit code either, so check `native_oracle_availability.state`.

For `STRLEN`, historical ID `PARENT246_strlen-control` and registered ID `ARGBOUND246_strlen-control` link to [selected retained evidence](../../evidence/strlen-control-20261117/README.md). The scoped match for this case is distinct from the target-wide documented difference. `results/evidence-index.json` links selected cases and is not exhaustive.

The [29-case batch evidence](../../evidence/main29-20261117/README.md) can be queried by the original registered ID or the neutral ID. Twelve of those cases are associated with their targets in the scenario register but are not listed in the final target-acceptance row. The index distinguishes them with `acceptance_case_listed`; do not infer that those cases formed part of the acceptance basis.

The [selected evidence](../../evidence/syntax-supplemental-20261117/README.md) for 16 grammar and eight supplemental cases is indexed separately in `results/extra-evidence-index.json`. Those populations are distinct from the 694 main targets.

For 75 API-related targets, [shared static evidence and parent case references](../../evidence/api-gap75-static-20261117/README.md) can be queried by target or case ID. This does not establish access to each case's raw observations or prove command-form routing from that registration line alone.

The [retained `PRINTDB15` evidence](../../evidence/printdb15-20261117/README.md) represents one physical case associated with two typed roles: `command_or_syntax:PRINTDATA` and `structural_syntax:PRINTDATA`. It is not counted as two separate executions.

The finite `INPUT` survey added two cases for default selection on empty input and echo, which had been outside the earlier acceptance scope. Echo was observed separately for each engine; equivalence across all GUI and CLI display channels and natural Native exit were not verified. Historical records pinning the ledger before those additions should not be confused with the final ledger.

`python -B tools/query.py PRINTDWEMPTY01` and `python -B tools/query.py structural_syntax:LOOP` show selected saved values in `scoped_observations`. The selection covers eight cases including array, level, and save commands, plus one DO/LOOP case. Check `scoped_observations_availability` for each collection. Original raw records are not included, so lookup does not reproduce the runs. Multiple targets can reference the same shared run and are not separate executions. When `--case-projection-dir` is explicitly supplied, these observations are suppressed to avoid mixing register snapshots.

For `native_source_anchor82` and `selected_51_saved`, lookup checks each collection's pinned manifest and the index file used by the search. A missing or altered manifest or index in an installed collection causes an error; an entirely absent collection is reported as `NOT_INSTALLED`. This checks index integrity; it does not verify every input file in the collection or authenticate the historical run.

## Legacy references

The historical evidence-chain audit recorded 468 of 694 typed targets as traceable without another adapter and identified 226 targets that required a legacy or layout adapter. The recorded outcomes for those 226 targets were 82 finite-scope matches, 69 documented differences, and 75 scoped differences. These are historical decisions. The adapter requirement describes how the evidence was recorded.

The revised [legacy reference index](../../evidence/legacy226-source-locator-20261118/locator.json) retains **226 typed targets and 2,476 reference entries**. A file or shared execution can appear in multiple entries. Read each entry by its `classification`:

| Classification | What the candidate provides |
| --- | --- |
| `PUBLIC_INCLUDED` | A candidate-relative path to included bytes that match the recorded source. Archive entries also identify the members to open. |
| `PUBLIC_DERIVED` | A candidate-relative path and a case ID with a JSON pointer to a selected observation. The cited data are an excerpt or projection of a source record. |
| `PRIVATE_RETAINED` | An index entry for an original held privately. The reference does not expose its private location or provide the original bytes. |
| `MISSING_OR_UNVERIFIED` | An entry whose original was unavailable or whose bytes could not be verified against the frozen inventory and applicable prior hashes. |

The classification labels describe what can be inspected in the candidate. Reproduction of a historical run or confirmation of a target decision requires its inputs, execution evidence and acceptance records. The candidate has yet to establish independent reproduction of the entire historical survey. Distribution follows the [component license index](../../LICENSES/README.md) and the [reference distribution guide](../../vendor/emuera/README.md).

The [adapter coverage record](../../evidence/legacy226-adapter-index-20261118/README.md) reports 35 partial reads, 169 unsupported inputs, and 18 invalid inputs for the limited legacy reader. Those reported results account for 222 of the 226 targets. The record supplies no per-status result for the remaining four. The [reader guide](../../tools/LEGACY_EVIDENCE.md) describes the supported formats and checks.

The [historical acceptance mapping](../../evidence/legacy-acceptance-269-20261117/README.md) uses a different selection criterion. For 269 targets with no `current_acceptance` field in the final ledger it identifies historical references for 205 and leaves 64 unidentified. The [selected default-color, display-state and operator observations](../../evidence/legacy50-selected-observations-20261117/README.md) provide later conditions and values for 27 targets. The original acceptance records for those targets remain unavailable in this selection.

For current availability, consult the legacy locator and [individual evidence review](../../evidence/legacy226-restored/README.md). Non-inclusion fields in older projections describe that projection date. The 978 added records include acceptance and comparison records, Native/PyEmuera logs, and inputs with their dependencies. Original verdicts and current publication availability remain separate attributes.
