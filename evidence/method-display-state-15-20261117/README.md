# Display-state command forms: 15 targets and one shared batch

[日本語](README.ja.md)

This publication candidate connects 15 typed targets and 15 registered cases to **one shared case150 batch** with two Native modes and one Public mode. It does not represent a separate execution per case. `index.json` retains 20 before/after conditions for ten command-form getters and one transition for each of five setting commands, observed through the respective getters. `matched_scoped` is the original ledger's limited verdict.

Each mode's fixture, configuration and saved history are preserved unchanged under `modes/`. The three histories have the same SHA and each contains the 20 observation lines recorded in the original comparison and `DONE`. Public stdout is not substituted for this history comparison. Native probe-declared fixture and config hashes match retained files, but the original receipts do not independently record input hashes both before and after execution. Public inputs are retained files and source-comparison declarations; no receipt independently recording their pre/post hashes was found.

The two Native modes ran as GUI processes on separate desktops; the probes record survival after five seconds and subsequent cleanup. Natural exit and exit codes were not observed. Public ran through a command line with inherited stdin, whose content was not recorded. The Public invocation's return code 0 does not establish Native termination. The source comparison's Public PYZ SHA is retained as a recorded value, not proof of independently captured before/after hashes or identical builds across other Public executions.

The observations cover getter values, state changes and RESULT/RESULTS routing for the recorded settings. They do not establish actual GUI color or font rendering, input layout, other settings, or general compatibility. LINEISEMPTY was observed only after preceding output lines. The earlier case149 record is not included in these observations. Full original receipts, personal paths, executables and the private source-to-derived crosswalk are not included. The original CASE register, comparison, conditions and original review are also not included; a third party cannot directly compare this bundle with those original records using this bundle alone.

## Verification and rights

Use Python 3.9 or later. Obtain the SHA-256 values of the manifest and verifier through a separate trusted channel and check both with an independent hashing tool, then run from this directory:

```text
python -I -B verify.py --manifest-sha256 <trusted manifest SHA256> --verifier-sha256 <trusted verifier SHA256>
```

Before running the shared file-set tool, the verifier checks its fixed SHA. It checks the file set, the 15 case/typed-target bindings, three saved-history hashes, and that each of the 20 observation lines starts with its condition marker. It does not independently derive expected values or authenticate the original execution or publisher, natural exit, rendering, or rights. It does not launch an engine. Trusted pins must be provided separately from the bundle. A resealed manifest with a newly accepted pin does not by itself establish agreement with the original materials.

See the [license index](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The original source ZIP described by the NOTICE is a separate distribution and is not included here. Rights holders and terms for fixtures and derived records remain unresolved; privacy, rights and publication are not approved.
