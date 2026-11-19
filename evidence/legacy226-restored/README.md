# Individually selected comparisons, logs and fixtures

[日本語](README.ja.md) · [Read every record in HTML](index.html) · [Survey browser](../../docs/survey-browser.html)

The additional selection covers 2,020 references to 978 source files for the legacy targets. Each file was inspected. The package includes 682 files as original bytes and 296 as derivatives with private runtime paths or internal coordination wording neutralized. No whole file was withheld. References with different targets or roles retain their individual IDs.

[index.json](index.json) records each file's reason, inspection, original SHA-256, published SHA-256, transformations, targets and reference IDs. The HTML pages display the complete published records and link their stored bytes. JSON is formatted for display. Use the artifact itself for byte comparison. Any original execution receipt, manifest hash or seal inside a record continues to describe that original execution.

## Restore fixture inputs

The [fixture layout index](fixture-layouts.json) records 172 retained layouts for 152 ERB/CSV inputs. Their same-case ERH, CSV and configuration dependencies were checked. Three additional inputs were copied unchanged from the same cases, ARRAY180.ERH, ZZ269.ERH and CHARA1.CSV. Required empty csv directories are restored as well.

Run from the candidate root and choose a new destination.

    python -B tools/restore_fixture.py U0157 --layout 0 --out C:/Temp/array180-input

This restores input bytes without launching an engine. An existing destination or mismatched source hash is refused. The configuration for U0975 could not be identified in the retained same-case material. That limitation appears in the index and restoration result. Another case's configuration is not substituted.

## Verification and notices

    python -B tools/verify_saved_evidence.py

The verifier checks the 978 individually reviewed files and 2,020 references, stored artifacts, HTML views, derivative mappings and fixture dependencies. The original verdicts for 694 targets and 2,898 scenarios are preserved. Checking retained observations and executing new observations are distinct operations.

Notice paths in the index are relative to the repository root. The [MIT License](../../LICENSE) covers original contributions the owner has authority to license. A reference to LICENSE.txt within a retained document denotes the same MIT text. Engine diagnostics, screens and source material retain their [component attribution and conditions](../../LICENSES/README.md). Distribute the applicable notices with those materials.
