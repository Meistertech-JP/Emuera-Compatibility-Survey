# Saved background-operation evidence: 24 cases

[日本語](README.ja.md)

This set contains 24 saved cases for expression and command forms of eight CBG operations: 16 direct, six short-circuit and two lifecycle cases. [records.json](records.json) connects each case, typed role, condition and scoped verdict to its own Native-01, Native-02 and public-01 materials. These are 24 fixtures, not one shared execution; equal hashes alone do not prove independent execution or target reach.

The recorded case verdicts are 22 `different_scoped` and two `unverified`. The public side of the two lifecycle cases stopped during setup or loading, so comparison of the CBG body is not established. Saved Native selected rows and public error codes remain case-specific. GUI pixels, clicks, mouse events, the complete background list and actual button selection were not observed. A return value does not establish rendering or interaction.

For example, `UIQUERY236_cbgsetg-expr-direct` records `OBS236 V=0 R=701 A=0` and a continuation in the selected Native log, and `E_FUNCTION` in public stderr. This is a scoped observation for that case, not an overall compatibility verdict.

## Reading the evidence

Each case's `modes` / `evidence` entries in `records.json` reference its mode-specific ERB, configuration, raw output and derived receipt. Native `native-history.bin` is a saved UTF-16 log with BOM. Public `public-stdout.bin` and `public-stderr.bin` are separate saved outputs, readable as CP932. ERB is UTF-8 and `emuera.config` is CP932. From this directory, the following prints the first case's Native log:

```powershell
python -c "from pathlib import Path; print(Path('assets/C001/native-01/native-history.bin').read_text(encoding='utf-16'))"
```

The example [fixture](assets/C001/native-01/inputs/ERB/SEARCHBOUND01.ERB), public [stdout](assets/C001/public-01/public-stdout.bin) and [stderr](assets/C001/public-01/public-stderr.bin) are included. Raw files, fixtures and configuration retain their saved bytes. Original receipts contain personal paths and process-management details and are not included; `receipt.json` retains selected fields. The derived case/mode identity comes from the saved case, fixture and original path, not a case or mode declaration by the original receipt. Native input hashes are probe declarations; public input hashes are receipt-recorded before/after values. Native before/after equality is not inferred.

Native natural exit was not observed and is separate from cleanup. Public stdout and stderr are distinct from the ordinary log and runner streams. Source code, executables, full original receipts, complete parent records and other outputs are not included. Equal hashes do not prove compatibility for all conditions, another execution or publisher authenticity.

## Integrity and rights

Use Python 3.10 or later. Verify the SHA-256 of the manifest and bundled `tools/file_set_manifest.py` through a separate trusted channel, then run from this directory:

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

The manifest checks file sets, sizes and hashes; it does not prove execution, publisher authenticity, rights or publication approval. See the [rights index](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The original ZIP described in the NOTICE is not included in this set. Rights holders and terms for survey fixtures and derived records remain to be confirmed separately.
