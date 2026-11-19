# Saved CSV string/flag, CARRAY and array-aggregate records: 51 cases

[日本語](README.ja.md)

This publication candidate combines 26 CSV string/flag, 13 CARRAY and 12 array-aggregate cases: 51 cases, 70 typed target–case roles, 51 batches and 153 modes. `index.json` retains recorded case verdicts, conditions, observations, unobserved states and limits. Registered roles and saved modes do not by themselves establish target reach, success or general compatibility.

## Materials and limits

- Selected raw, fixtures, configurations, CSV and ERH files in `assets/` retain their original mode-specific bytes. `index.json` lists each asset and derived receipt with its SHA. Native raw is `emuera.log`; Public raw is `stdout.bin`.
- Eight guard-off CSV cases belong to a separate source manifest; they are not treated as members of the other group manifest. Both recorded config variants remain bound to their own modes. CARRAY configuration references are also retained per mode.
- Each array-aggregate mode retains `CASE.ERB`, `ARRAYMSORT176.ERH`, `ENDPOINT_READBACK.ERH` and its config. ERH files are not substituted across conditions. Original receipt condition ID and mode are joined to the case observation.
- Older CSV/CARRAY receipts contain no case ID or mode field. Their binding is attributed to explicit case evidence, mode-specific source paths, the appropriate group manifest and saved SHA readback. A raw `outputs` declaration absent from the original receipts is not invented.
- Do not infer Native natural termination from helper or runner returncodes or cleanup. Preserve each case's fatal post-state, reach and parent-review limits. Complete original receipts, stderr, executables, full parent reviews and other outputs are not included.
- `references.json` distinguishes included derivatives from non-included references in original case records. A source-declared SHA can differ from a derived receipt SHA. Original paths and source-to-derived mappings remain private and are not included.

## Verification

Use Python 3.10 or later. Before running the verifier, use an external hash utility to check the manifest against its SHA-256 obtained through a separate trusted channel, and check `verify.py` and `tools/file_set_manifest.py` against their hashes in that trusted manifest. Specify the manifest and bindings pins:

```powershell
python -B verify.py --manifest-sha256 <manifest-sha256> --bindings-sha256 <bindings-sha256>
```

The shared file-set tool and finite case/role/mode/input/raw/receipt checks establish selected-file consistency, not original execution, natural termination, publisher authentication, compatibility or permission.

See [notices](LICENSES/README.md), [Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The source ZIP described by the NOTICE is not included. Ownership and terms for survey fixtures and derivatives remain unresolved; rights and confidentiality are not approved.
