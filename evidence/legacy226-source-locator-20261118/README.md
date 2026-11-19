# Evidence references for the 226 legacy targets

[日本語](README.ja.md)

The [locator](locator.json) contains 2,476 references for 226 targets whose acceptance records require a legacy-format adapter. The original finite-scope outcomes remain 82 matches, 69 documented differences, and 75 scoped differences. The [browser](../../docs/survey-browser.html) links saved results by case, including for targets without a direct acceptance reference.

| Classification | What can be accessed and verified |
|---|---|
| `PUBLIC_INCLUDED` | Original bytes at a package-relative path or in the listed archive members |
| `PUBLIC_DERIVED` | An observation excerpt with a case ID, JSON pointer, and source SHA-256 |
| `EXTERNAL_FETCHABLE` | A pinned artifact obtainable from its external distributor |
| `PRIVATE_RETAINED` | Index and identity metadata. The original is preserved outside the package |
| `MISSING_OR_UNVERIFIED` | The location or identity of the source artifact remains unverified |
| `REDUNDANT_REFERENCE` | Another public artifact covers the same verification requirement |

The locator's `reference_class_counts` field reports the counts. Paths are relative to the package root. Follow `archive_members` from the outermost archive inward. References retain their individual roles and conditions when they share identical bytes. `candidate_exists` indicates that the original bytes are retrievable from the package.

Copies with different filenames are linked when their size and SHA-256 match the original. This includes empty output files and establishes access to the referenced bytes. Execution and test conditions remain subject to the individual observation records and execution receipts.

Run `python -B tools/verify_saved_evidence.py` from the package root to verify the packaged source artifacts and excerpt links. Independent reproduction of all historical observations for these 226 targets remains unestablished.
