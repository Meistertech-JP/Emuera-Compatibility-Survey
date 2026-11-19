# Recorded observations for 183 finite-scope cases

[日本語](README.ja.md)

This proposed distribution selects records for 183 cases from a finite Emuera1824+v24 and PyEmuera 3.0.0 survey. It contains 184 typed target–case roles, 126 shared batches, 377 mode records, and 548 case–mode references. Original case verdicts, individual observations, unobserved states, and limits are retained. It does not establish complete observations for all 694 targets, full compatibility, target-role reach, or a separate process execution for each case.

## Reading the records

- [`data/cases.jsonl`](data/cases.jsonl) contains case IDs, typed roles, batch and mode references, and the recorded conditions, verdicts, observations, and unobserved limits. Each `observation_pointer` is relative to that case's `record`.
- [`data/batches.jsonl`](data/batches.jsonl) groups the shared Native1/Public1 receipt pairs and related cases. Cases in one shared batch do not imply separate process launches. A selected Native2 is also associated with the batch.
- [`data/modes.jsonl`](data/modes.jsonl) lists each mode's fixture, inputs including configuration, selected raw output, derived receipt, and SHA-256 references. The selected Native raw is `emuera.log`; the selected Public raw is stdout. Stderr files, complete original receipts, other outputs, images, original registers, and supporting documents are generally not included. Case records may nevertheless include excerpts of stderr diagnostics.
- [`data/references.json`](data/references.json) resolves the `ref:R...` identifiers in case records. Of 1,499 references, 820 point to included derivatives and **679 are not included**. Non-inclusion does not establish that an original was missing, that execution did not occur, or that a result was unobserved. A document named in an original case is not necessarily included here.
- Native2 for `STRING_METHOD_NEXT_20261116_ISNUMERIC_I64_OVERFLOW` refers to a different recovery-receipt format and is outside the standard modes selected here. Do not infer that Native2 was not run or not observed.

A helper exit code of zero alone does not establish natural termination of Native. The original caveat is retained in the four relevant Native receipts. Where termination or reach is unknown, preserve the unknown or unobserved status recorded by the case.

## SHA and verification limits

The included raw, fixture, and configuration bytes are identical to their selected sources and retain corresponding SHA-256 values. Receipts are derivatives containing selected fields, so source receipt and derived receipt SHA values may differ. Distinguish source-declared SHA values in case records from the hashes of included files in `references.json` and `modes.jsonl`. Original source files and the private provenance mapping are not distributed here.

[`data/manifest.json`](data/manifest.json) records hashes within the original projection. The selected directory can additionally be checked with [`file-set-manifest.json`](file-set-manifest.json). The following is a proposed command from the repository root **if** this distribution is placed at `evidence/observation-adapter-183-20261117/` and the shared tool is included.

```powershell
python -B tools/file_set_manifest.py verify `
  --root evidence=evidence/observation-adapter-183-20261117 `
  --manifest evidence/observation-adapter-183-20261117/file-set-manifest.json
```

The inventory excludes the manifest itself. Obtain and compare the manifest's own SHA-256 through a separate trusted channel. Matching the inventory establishes consistency of the selected files; it does not authenticate the original execution or publisher, establish semantic sufficiency, or grant publication rights.

## Licenses and notices

These links target common documents in the proposed repository placement. Check their targets and each material's rights and confidentiality before distribution.

- [Common notices](../../LICENSES/README.md), [original Emuera license](../../LICENSES/Emuera1824-v24-license-original.txt), and [Emuera NOTICE](../../vendor/emuera/NOTICE.en.md)
- [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [PyEmuera third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)

These notices identify related third-party material; they do not grant a blanket license for survey fixtures, original documentation, derived records, or every other item. Ownership, terms of use, and confidentiality require material-specific review.
