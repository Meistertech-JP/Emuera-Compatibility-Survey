# Saved records: 96 slice, CSV remaining and Unicode cases

[日本語](README.ja.md)

This publication candidate selects 36 string-slice, 32 CSV remaining and 28 Unicode code-unit cases from a finite survey. It retains 114 typed target–case roles, 81 batches, 243 mode records and 288 case–mode references. Shared modes do not imply an independent process for every case or reference.

Each case in `index.json` retains its recorded verdict, conditions, observations, unobserved limits and existing case-specific semantic readback. Check its role and batch separately. Sharing raw data does not establish target reach, a return, success or acceptance for another case. `references.json` distinguishes included derivatives from non-included sources. Original source-declared hashes in a case can differ from a derived receipt hash.

- Slice retains 108 modes, case-specific raw segments, adjacent-line wraps, helpers, values, routing, differences and unobserved state. The execution-stage pending parent review and later recorded case verdict are separate records.
- CSV remaining retains 96 modes and mode-specific ERB, CHARA10, CHARA30 and config. Native natural termination was not observed for 64 modes. Preserve the distinction between SP-off CSV definitions and direct runtime observations; fatal post-state remains UNOBSERVED.
- Unicode has 28 cases and 84 case–mode references sharing 13 fixture groups and 39 receipt/raw paths. Six cases sharing `ACTUAL_GATE` do not imply six independent executions, six target returns or later reach. Preserve separate PAIR0/PAIR1/empty-index, CMD/EXPR, index-helper stops and fatal unobserved state. D800 numeric-unit observation is distinct from Native display and Public escape. A standalone D800/FFFD positive runtime control for the fixed-regex observer was not established.

Raw, fixture, config and CSV bytes in `assets/` are unchanged. Receipts contain selected fields. Unicode raw is tied to the original receipt `outputs`; older slice/CSV receipts do not declare raw in `outputs`, so their binding is explicitly attributed to case references and saved frozen readback. Runner returncodes or cleanup alone do not prove Native natural termination. Stderr, complete original receipts, executables, complete parent records and other outputs are not included.

## Verification

Use Python 3.10 or later. Before running the verifier, use an external hash utility to check the manifest against its SHA-256 obtained through a separate trusted channel, and check `verify.py` and `tools/file_set_manifest.py` against their hashes in that trusted manifest. Specify the manifest and bindings pins:

```powershell
python -B verify.py --manifest-sha256 <manifest-sha256> --bindings-sha256 <bindings-sha256>
```

The existing file-set tool and case/batch/mode/typed-role checks include Unicode shared-fixture condition binding. They do not replay engines or establish past execution, natural termination, target reach, full compatibility, source or publisher authenticity, or rights/confidentiality approval.

## Licenses and notices

See [notices](LICENSES/README.md), the [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The original source ZIP described by the NOTICE is not included. Survey fixtures, derived records and new documents need separate ownership and terms review; no blanket grant is established. Rights and confidentiality remain unapproved.
