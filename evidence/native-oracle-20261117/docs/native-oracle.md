# Saved Native Emuera observations

[日本語](native-oracle.ja.md) · [Open the browser](native-oracle.html)

Find condition-specific inputs and saved Native Emuera output and diagnostics. PyEmuera comparisons are supplementary. Search by target, case ID, text in the ERB, or output. Filters include Native saved material, images, comparison differences, and cases whose target reach is unconfirmed.

Some cases link to original bytes and their SHA-256; the 33 selected-observation projections do not include their original fixture or raw. Display text is decoded using the recorded inferred encoding and converts CRLF and CR to LF. Use the original bytes when exact line endings or bytes matter. Images are retained captures; their interpretation is a finite manual observation.

A saved file and evidence that a target was reached are separate facts. The browser distinguishes uncalled controls and stops inside argument helpers. A shared batch shares output and does not imply separate executions. Display, natural termination, and post-error state are described only to the extent recorded.

## Searches to try

- `OPCONT268_strcmp-ge`: scoped difference from a shared run; original fixture and raw are not included.

- `CASE001`: separate ABS batch, full-batch and single stages.
- `UIQUERY236_lifecycle-expr`: Native STEP observations and an unverified Py comparison.
- `ARGBOUND245_empty`: the target command's missing-argument diagnostic.
- `P38`: saved image and Native diagnostic; image observations can be filtered.
- `LINEBUF20261115_button_method`: case verdict, parent acceptance projection, selected lines in three modes, and the older-pin limitation.
- `PRINTKD212_C212_0`: selected lines in a shared batch, without inferring reach from shared output alone.

This index covers selected finite conditions; it is not a coverage or compatibility certification. The source field records the candidate-relative document, JSON pointer and SHA-256. The existing 80 rows retain their 22 source records; the added 33 rows reference an included selected-observation record. The original fixture, config and raw for the added rows are not included. Other materials mentioned inside those records are not necessarily included.

Before running, obtain the expected SHA-256 values of the manifest, `tools/file_set_manifest.py` and `tools/build_native_oracle.py` through a separately trusted channel, and compare all three with an independent OS hashing tool. Pass the trusted manifest and verifier SHA-256 values below. The generator first verifies the file set including selection, generator and assets; it writes output only if its generated HTML also matches the pinned manifest. A removed row, removed reference or changed stage is rejected before generation. If the pins themselves are untrusted, the bundled files cannot authenticate themselves. For an intentional update, independently review source record, case, stage, mode and role, generate and inspect a new version, reseal it, and distribute new pins through an independent channel. Existing pins are not updated automatically.

The search box offers an exact case-ID option. General search also matches text in shared fixtures and output; a hit does not prove independent case reach. Cards show bundle and stage to distinguish sources. The source link opens the included record within this independent bundle.

When placed at `evidence/native-oracle-20261117/`, only that directory is the manifest verification root. The same relative links work when the bundle is copied independently. It contains 113 rows: the existing 80 and projections of 33 additional conditions; it does not claim to include or cover the separate 34/38 cases. Asset and source-record links resolve inside the bundle; other materials mentioned inside a record are not necessarily included.

## Rebuild

With Python 3.10 or newer, run this from the root of the tree. The builder reads the selection and included assets, checks each asset's size and SHA-256, and generates the HTML. It uses neither an engine nor the network.

```text
python -I -B tools/build_native_oracle.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

`results/native-oracle-selection.jsonl` records selected cases and asset bindings; included original bytes are under `evidence/` and other referenced paths. The original bytes for the added 33 rows are not included. Rebuilding the selection and HTML does not prove historical execution or rights. When updating, check each case's source, conditions and SHA before updating the selection.

## Licenses

See the [license index](../LICENSES/README.md), [original Emuera license](../LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](../vendor/emuera/NOTICE.en.md), [PyEmuera license](../LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [third-party notices](../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The Emuera NOTICE describes a separate distribution containing the original ZIP; this index does not include that ZIP. Authorship and terms for fixtures, the derived selection and the new builder require separate confirmation.
