# CSV numeric: 45 saved cases

[日本語](README.ja.md)

This publication candidate selects 45 cases, 135 saved modes (Native1, Native2 and Public1 per case), 12 typed targets and 56 target–case roles from a finite CSV numeric survey. Multiple roles in one case do not establish separate launches or reach of every role.

## Reading the records

- Each `index.json` case retains conditions and expected values, its recorded case-register verdict, and the saved readback classification, selected marker comparisons, stop location and unobserved limits separately. Expected values and preparation predictions are not observations. The case register records 1 matched, 40 different and 4 unverified cases.
- Four later cases separate the SP conditions affecting those unverified cases; they are distinct cases and are not included here. The 147 saved modes mentioned in the original record comprise this set's 135 modes and 12 modes from those later cases; they do not mean 135 successes.
- The execution-time `COMPARISON.json` records raw observations only and parent adjudication pending. It is retained as a statement at that stage, separately from the later case-register verdict. This bundle does not create a new parent acceptance decision; the parent review and its full rationale are not included.
- Each mode includes the selected Native `emuera.log` or Public `stdout.bin` and that mode's ERB, CSV and configuration inputs. Their source and included byte hashes match. Do not infer identical conditions across modes merely from hashes.
- Receipts contain selected fields derived from the originals. The raw hash binding comes from explicit case-register references, the group manifest and the saved raw readback, not an `outputs` declaration in the original receipt. Original and derived receipt hashes can differ. Complete original receipts, stderr, executables, full probes, original registers and the parent review are not included.
- In all 90 Native modes the record has `process_exited_after_5s=false`, `exit_code_observed=false` and `cleanup_terminate_ok=true`; natural termination was not observed. Native runner returncode 0, `completed` and `integrity_ok` do not establish natural termination, a successful comparison, or acceptance. Recorded Public returncodes are preserved.

`expected-bindings.json` and `manifest.json` support checks of the selected case/mode/assets and file set. The private source-to-derived mapping is not distributed here.

## Verification

Python 3.10 or later. Before running the verifier, use an external hash utility to check the manifest against its SHA-256 obtained through a separate trusted channel, and check `verify.py` and `tools/file_set_manifest.py` against their hashes in that trusted manifest. Specify the manifest and bindings SHA-256 values:

```powershell
python -B verify.py --manifest-sha256 <manifest-sha256> --bindings-sha256 <bindings-sha256>
```

Verification uses the existing file-set tool and checks the finite case/mode/role bindings. Pins obtained only from the same distribution do not authenticate the publisher. Verification does not prove the original observation, replay the engines, establish every requirement, or approve rights and confidentiality.

## Licenses and exclusions

See [notices](LICENSES/README.md), the [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The original source ZIP described by the Emuera NOTICE is not included. Survey fixtures, new documentation and derived data require separate ownership and terms review; these notices do not grant blanket rights over the bundle. Rights and confidentiality remain unapproved.
