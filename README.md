# Emuera compatibility survey

[日本語](README.ja.md)

For offline browsing, open [`index.html`](index.html) in the extracted folder to reach the reference through clickable links.

This project is an independent, evidence-based compatibility survey for Emuera-compatible engines. Its initial dataset records a finite comparison between Emuera 1.824 +v24 and PyEmuera 3.0.0. Emuera runs variants written in ERB with CSV data; this project examines selected language and command behavior rather than distributing variants. The saved Emuera observations provide a reference for future PyEmuera compatibility fixes and regression checks, as well as for other compatible implementations.

The historical ledger records 694 typed targets, 2,898 main scenarios, 16 supplemental items and 114 separate grammar cases. The survey recorded its source census as complete within the declared scope. The ledger retains scoped matches, differences, unsupported behavior and unresolved observations. Registered modes describe case configurations. A shared run can supply records for several cases.

The candidate contains a neutral index, saved observations, and a harness for selected comparisons. Independent reproduction of the survey's full historical execution and acceptance records has yet to be established. The [legacy evidence guide](docs/en/results.md#legacy-references) explains original-byte and derivative availability, including transformation reasons, for 2,476 references across 226 typed targets. Read the [978 additionally selected comparison records, logs and fixtures in HTML](evidence/legacy226-restored/index.html).

- [Browse the command reference and saved observations](docs/survey-browser.html). Combine the genre, target-kind, verdict, and search filters to narrow the 694 targets, then read bilingual descriptions, syntax, examples, and expected effects. Pin a saved capture to keep it on screen while you read Native/PyEmuera comparisons, 3,359 requirements, and the bundled output and diagnostics.
- [Reference usage and regeneration](reference/README.md), [glossary](reference/glossary.html), and [original OSDN Wiki and preserved-source research](reference/SOURCES.md)
- [How to read the results](docs/en/results.md) and [check selected files offline](docs/en/offline-validation.md)
- [Examples of observed results](docs/en/observations.md)
- [Search saved Native observations](evidence/native-oracle-20261117/docs/native-oracle.html) ([usage and limits](evidence/native-oracle-20261117/docs/native-oracle.md))
- [PRINTVKW and PRINTVDW after wait release](evidence/wait-release-20261117/README.md)
- [PRINTVKW and PRINTVDW: empty wait and a later argument error](evidence/wait-c15-20261117/README.md)
- [Saved Native observations for graphics and sprite APIs](evidence/graphics-native-saved-20261117/README.md)
- [Native observations for 38 graphics cases](evidence/graphics-38-cases-20261117/README.md)
- [Native GUI observations of images, backgrounds, and buttons](evidence/graphics-gui-observations-20261117/README.md)
- [Saved expression, input and diagnostic observations](evidence/new-replay-20261116/public/README.md)
- [Dataset and verification](results/README.md)
- [Trace 694 targets, requirements and selected evidence](evidence/694-target-trace-20261117/README.md)
- [Static source-location index for 694 targets](evidence/native-source-694-static-20261117/README.md)
- [Records and withheld fields for 2,898 registered cases](evidence/case-register-2898-20261117/README.md)
- [Search saved observations for 486 cases](evidence/case-observation-recovery-20261117/README.md)
- [Harness instructions](harness/README.md)
- [Representative differences](differences/representative-20261116/README.en.md)
- [Index of recorded difference cases](differences/catalog.json)
- [Search selected saved observations for 129 targets](differences/saved-observation-lookup-20261117/README.md#english)
- [Recorded observation: TWAIT 0,1](evidence/twaitzero-observation-20261117/README.md)
- [Saved external observations: 29 numeric and string cases](evidence/external-scalar-29-package-20261117/README.md)
- [Saved external observations: 16 expression, PRINT and diagnostic cases](evidence/external-additional-16-package-20261117/README.md)
- [Saved assignment and operator observations: 23 cases](evidence/operator-265-20261117/README_en.md)
- [FINDELEMENT and FINDLASTELEMENT: 64 string-array conditions](evidence/find-element-string-64-20261117/README_en.md)
- [Saved observations for 61 PRINTDATA-family cases](evidence/printdata-61-20261117/README.md)
- [Index of 183 saved observation cases](evidence/observation-adapter-183-20261117/README.md)
- [Saved observations for 45 CSV numeric cases](evidence/csv-numeric-45-20261117/README.md)
- [Saved observations for 96 string, CSV and Unicode cases](evidence/remaining-96-20261117/README.md)
- [Saved observations for 51 CSV string and array cases](evidence/selected-51-20261117/README.md)
- [Saved observations for 28 CALL, JUMP, display and LIST cases](evidence/target-priority-28-20261117/README.md)
- [PRINT: shared records for 82 cases](evidence/print-kd-shared-82-20261117/README.md)
- [PRINT SINGLE: saved observations for ten conditions](evidence/normal-observation-access-20261117/README.md)
- [Display state: shared records for 21 cases](evidence/display-state-21-20261117/README.md)
- [Operators: saved records for six cases](evidence/operator-normal-6-20261117/README.md)
- [Display-state command forms: 15 cases](evidence/method-display-state-15-20261117/README.md)
- [Background operations: 24 saved cases](evidence/console-background-24-20261117/README.md)
- [Input and screen state: 16 saved cases](evidence/platform-input-16-20261117/README.md)
- [Numeric compound assignment: 10 saved cases](evidence/compound-assignment-10-20261117/README.md)
- [Eight groups: 101 saved cases](evidence/multi-group-101-20261117/README.md)
- [Six groups: 72 saved cases](evidence/multi-group-second-72-20261117/README.md)
- [LINEISEMPTY acceptance and historical hash discrepancies](evidence/lineisempty-acceptance-20261117/README.md)
- [Historical acceptance records: 40 targets](evidence/parent-restoration-40-20261117/README.md)
- [Methods, scope and environment](docs/en/method.md)
- [Pinned environment and dependencies](manifests/environment.json)
- [Reference archive and its accompanying notices](vendor/emuera/README.md)
- [Component notices and attribution](LICENSES/README.md)
- [Verify a selected file set](tools/FILE_SET_MANIFEST.md)
- [Partial reader for older evidence](tools/LEGACY_EVIDENCE.md)

Browse an exact target name or case identifier with `python -B tools/query.py SET`. To restrict saved observations by target kind, use for example `python -B tools/query.py structural_syntax:PRINTDATA`. Where available, the lookup also returns separately retained evidence, preserving shared-batch and uncalled distinctions. An index entry alone is not an independently verified execution log.

To read a case's conditions and selected observations directly, see the [case reader instructions](tools/CASE_READER.md). They also show the original verdict and identify omitted fields.

For matches in the 486-case saved-observation collection, `case_observation_recovery_links` points to the included record files and lines. That collection does not include the original raw files or source records.

`--kind` filters typed targets and some evidence fields, but does not filter the `cases` field matched by case ID. Do not infer a match for the requested kind from exit code 0 alone; check the target and count in each field. For example, `FONTSTYLE_NEG1 --kind expression_function` leaves the command case in `cases` even though the historical restoration field is empty.

For the C196 supplement and the supplemental evidence index, an integrity error stops strict lookup with exit code 2. With `--partial`, eligible errors suppress the affected results, report `INCONSISTENT` and `PARTIAL`, and return the remaining results with exit code 3. Inspect each collection's availability field for its own rules. See [how to read the results](docs/en/results.md) for a Native observation example.

Case ID lookup in `parent_restoration_40` covers cases recorded in the historical restoration document. For example, find FONTSTYLE’s later cases in the ordinary `cases` field, and follow the historical restoration information by typed target, such as `command_or_syntax:FONTSTYLE`. Historical and later decisions are reported separately.

`query.py` writes UTF-8 JSON. In Windows PowerShell 5.1 or PowerShell 7, set the receiving side to UTF-8 when using a pipeline. Run this from the repository root; it restores the previous setting afterward.

```powershell
$previousEncoding = [Console]::OutputEncoding
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $json = (python -B tools/query.py expression_function:SUBSTRINGU) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw "query.py failed ($LASTEXITCODE)" }
    $data = $json | ConvertFrom-Json
} finally {
    [Console]::OutputEncoding = $previousEncoding
}
$data
```

`$data` is the object converted from JSON. Other programs receiving the output should also decode it as UTF-8.


The ledger retains 99 main scenarios originally marked unverified and 17 marked blocked or evidence-deficient. Later finite-scope work recorded how these 116 cases relate to the typed targets. The recorded target decisions and the original case verdicts describe different levels of the survey. See [how to read the results](docs/en/results.md) for the breakdown and evidence limits.

The survey is separate from PyEmuera and covers the engine versions identified in the [environment record](manifests/environment.json). The [MIT License](LICENSE) applies to original verification materials and editorial contributions. The [component notices](LICENSES/README.md) identify third-party sources and their reuse terms.

## Supplemental evidence index

The pinned supplemental index adds links in `selected_evidence_links` to [24 operator cases](evidence/operator-264-20261117/README.md), [64 string-array search conditions](evidence/find-element-string-64-20261117/README_en.md), [23 assignment and operator cases](evidence/operator-265-20261117/README_en.md), [16 externally preserved cases](evidence/external-additional-16-package-20261117/README.md), and [29 externally preserved cases](evidence/external-scalar-29-package-20261117/README.md). Search by registered case ID or typed target. Short aliases can occur in more than one collection, so check the full registered case ID or collection. Some conditions or target roles share an execution record; the number of links is not a count of process launches.

Searching `TWAITZERO01` or `command_or_syntax:TWAIT` also links to the [recorded TWAIT 0,1 observation](evidence/twaitzero-observation-20261117/README.md).

`supplemental_evidence_availability` reports the index, each collection, and index-linked Japanese and English readable documents separately. For operator264, matching document hashes allow each case result to link to the corresponding sections. Collections without index-linked documents report `NOT_PROVIDED`; their READMEs are available through the links above. When both the index and its installation marker are absent, the index reports `NOT_INSTALLED`; an absent index alone is inconsistent. If both files are removed, that state cannot be distinguished from non-installation. A damaged or partly missing collection fails strict searches; `--partial` retains independently verified results and exits 3. The shared verifier helper must pass its pin before import; if inconsistent the search exits 2. Case listing in an acceptance row does not imply target closure or body execution. See each collection for its source-record and non-inclusion limits.

