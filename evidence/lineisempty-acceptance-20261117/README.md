# LINEISEMPTY button state: saved observations and acceptance pins

[日本語](README.ja.md) | [Machine-readable record](record.json) | [Acceptance projection](parent-acceptance-projection.json)

This bundle holds the saved corrected-02 Native two-mode and public one-mode fixtures, configurations, raw outputs and privacy-derived receipts for `LINEBUF20261115_button_method`, typed `method_as_command:LINEISEMPTY`. The original finite parent decision recorded `necessary_comparison_complete` and `matched_in_finite_scope`. The decision is not changed. Raw evidence for the other two cases in that parent decision is not included here.

The selected lines for each mode are `EMPTY=1 R1=702 S=SENTINEL`, `BUTTON=0 R1=702 S=SENTINEL`, and `DONE`. The two Native histories have equal bytes but remain separate recorded roles. Full public stdout equality and visual rendering are not claimed. Native natural exit was not observed; cleanup after five seconds was recorded.

Three individual acceptance pins differ from the retained observation document, review and manifest. The acceptance's separate manifest field matches the retained manifest, while the readback's all-references-match flag conflicts with the three old pins. [record.json](record.json) records the values separately. The saved correction history supports stale individual pins after document changes, but the old bytes were not found, so their exact previous identity is not proven. No original pin is changed.

The Native 0/public 1 `PRINT_SPACE 0` difference is a separate `expression_function:LINEISEMPTY` case and is not transferred to this statement-form comparison. Its raw evidence is not included. HTML, clicks, invalid arguments, full output equality and natural exit remain outside the observed scope.

The original parent acceptance and session are not included. The parent decision is a neutral projection of a saved record; the original acceptance and old bytes cannot be independently verified from this bundle alone. No executable is included, so the bundle supports inspection of saved observations, not independent engine execution. Candidate paths are references observed at preparation time and may change.

## Rights and privacy

This is a publication candidate and has not been approved for publication. Independent rights, provenance and privacy review remains necessary for fixture authorship, Emuera configuration and output, PyEmuera output, receipt projections, notices and the included tool. Mechanical removal of local paths, process IDs, timestamps and host details does not establish review clearance. See [license guidance](LICENSES/README.md) and the [Emuera NOTICE](vendor/emuera/NOTICE.en.md). The executables, original acceptance and session are not included.

From this bundle's root directory, verify the file set with `python -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.`. The manifest records integrity; it is not rights approval or independent proof of the historical execution.
