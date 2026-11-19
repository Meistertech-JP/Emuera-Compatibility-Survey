# PRINTS and PRINTSL: saved observations

[日本語](README.ja.md)

This package records two selected cases, each with distinct Native-01, Native-02 and PyEmuera public-01 roles. It contains fixtures, configuration, saved raw output, selected receipt fields, comparison and acceptance excerpts. It does not contain either executable or a complete proof of the parent acceptances. The historical boundary cases and other source/binary evidence used by those acceptances are separate.

## Selected observations

Both cases record two consecutive spaces in the string, the selected newline behavior and helper order 1→12. Helper 9 was not called during the suppressed section; B remained 71 and the string RESULTS remained `"KEEP"`. RESULT was 0 after `SKIPDISP`, but the intermediate value attributable to the suppressed call alone was not isolated.

[PRINTS Native-01](cases/PRINTS/native-01/observation/raw.bin) · [PRINTS PyEmuera](cases/PRINTS/public-01/observation/raw.bin) · [PRINTSL Native-01](cases/PRINTSL/native-01/observation/raw.bin) · [PRINTSL PyEmuera](cases/PRINTSL/public-01/observation/raw.bin). Native-02, inputs, configuration, stderr and receipts are referenced by mode in `manifest.json`.

The Native logs and configuration relate to Emuera; the public output and diagnostic text relate to PyEmuera. See the [license and notice index](LICENSES/README.md), [Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera notice](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The Emuera notice was written for a separate source ZIP; that ZIP is not included here. The ownership and terms for the survey fixtures, derived data and new tools are still under review: no license listed here is automatically applied to them.

To check the recorded package offline, obtain the manifest and verifier SHA-256 pins from an independent trusted distribution channel, then run in this directory with Python 3.9 or later:

```text
python -B verify.py --manifest-sha <TRUSTED_MANIFEST_SHA256> --verifier-sha <TRUSTED_VERIFIER_SHA256>
python -B negative_checks.py --manifest-sha <TRUSTED_MANIFEST_SHA256> --verifier-sha <TRUSTED_VERIFIER_SHA256>
```

The included `manifest.sha256` must match the externally pinned manifest, but it is not an external trust source. The verifier checks the exact file set, per-case/per-mode role paths and the fixed role-binding record. Its own hash must also be checked independently. If both Native runs have identical bytes, their file bytes cannot independently establish which execution produced each copy; the role assignment follows retained receipts and provenance. Hashes do not authenticate the original operator or publisher.

This is an offline check of retained observations, not a fresh engine run or full compatibility claim. Native natural exit and Native exit code were not observed; a helper return code is not a Native exit code. The historical public runtime identity remains unknown. `SKIPDISP` itself writes `RESULT`; no suppressed-call intermediate numeric state is asserted. Native raw uses UTF-16 and public raw uses CP932. Engine reproduction requires separately obtained authorized executables, a suitable environment and additional instructions.
