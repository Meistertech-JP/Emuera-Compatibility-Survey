# Saved operator records: six cases and 19 typed targets

[日本語](README.ja.md)

This publication candidate associates one refreshed Public run and two retained Native repetitions for each of six cases and 19 typed targets, based on recorded case, configuration and fixture relationships. It does not establish **complete equivalence of conditions**, including environment and input channels, identical builds between historical and refreshed Public runs, compatibility, or acceptance of every target. Six cases are not 19 independent executions.

[`index.json`](index.json) gives each case's typed targets, fixture, configuration and output paths and SHA values, the Public receipt's UTC start and finish, the unknown Native execution times, and input, termination and unobserved limits. Public times are from saved receipts. The Native probe receipts do not state execution times; filesystem modification times are not substituted for execution times.

## Contents and comparison scope

- `assets/<case>/inputs/` contains one fixture and config per case. Their bytes are unchanged and their SHA values matched the recorded Public and both retained Native inputs. Matching these inputs does not establish complete equivalence of execution conditions.
- Each case includes unchanged selected outputs: `public/stdout.bin`, `public/stderr.bin`, and `native-01/emuera.log` and `native-02/emuera.log`. Public stdout uses CP932, stderr UTF-8, and Native logs UTF-16 with a BOM. Public stderr contains a nonfatal OUTPUTLOG notice; diagnostic equivalence with Native is not asserted.
- `selected_normal_markers` contains 108 markers across the six cases. Each appears once in the recorded order in all three selected outputs, followed by one `DONE`. This check does not establish equality of unselected output or all behavior, target reach or success, visual equivalence, or post-exit state.
- Public inherited stdin; its content was not recorded. Native ran as a GUI in a separate desktop; retained probes report no synthetic keyboard events. Complete equivalence of external input or environment is unverified. Native natural exit and exit code were not observed after five seconds, and cleanup was recorded. Public termination cannot be assigned to Native.
- Each case records the before/after SHA of the refreshed Public PYZ and the Native exe SHA from the retained probe. Different engines are not the same build, and missing historical Public build evidence is not filled in from the refresh.

The `case_register_pointer` in each case refers to the original `CASE_SCENARIO_REGISTER.json`, which is not included. Its SHA is identified in `bindings.json`; without access to that original register, a third party cannot directly verify the pointer against it. A separately available case index must be linked by case ID and its own pin, not by assuming it has the same `/records` layout. Full original receipts, personal paths, process information, the private source-to-derived crosswalk, engines, and unselected outputs are not included. The SHA relationship for every selected input and output is retained separately. Final privacy, rights and publication approval remain outstanding.

## Verification

Use Python 3.9 or later. Obtain trusted SHA-256 values for `manifest.json`, `verify.py`, and `bindings.json` through a separate trusted channel, then compare all three with an independent hashing tool. Values supplied only inside the bundle are not an independent trust anchor. From the bundle root:

```text
python -I -B verify.py --manifest-sha256 <trusted manifest SHA256> --verifier-sha256 <trusted verifier SHA256> --bindings-sha256 <trusted bindings SHA256>
```

The verifier checks the shared file-set tool against its pinned SHA before invoking it, then checks the separately pinned case bindings, file set, sizes and hashes and the finite bindings of six cases, 19 typed targets and selected markers in three saved outputs per case. The bindings fix each case's target roles, original pointer, fixture/config SHA, markers, selected output SHA and recorded executable hashes. Without trusted external pins, the manifest, verifier and bindings are not authenticated; if both a binding and its pin are replaced by an untrusted party, the original association is not authenticated. These checks do not prove the authenticity of original receipts or execution, complete condition equivalence, rights, or compatibility. They do not rerun an engine.

## Rights and omitted material

See the [rights notices](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The Emuera NOTICE describes a separate distribution that includes the original ZIP; this bundle contains neither that ZIP nor the 7z. The config is byte-identical to the preserved Emuera-derived configuration. Rights holders and terms for the fixtures, research records and derived data remain separately unresolved; these notices do not grant a blanket license for the bundle.
