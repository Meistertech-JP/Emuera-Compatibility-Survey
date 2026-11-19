# Main29: limited legacy expression observations

[日本語](README.ja.md)

This repository evidence directory contains 29 cases in one full batch and separate single and representative batch stages for CASE001 (ABS) only. Each stage retains Native-01, Native-02 and Py roles. `matched_scoped` records the selected expression value and RESULT/RESULTS snapshots; it does not establish acceptance of a parent target, resolve known differences, or establish full compatibility. GUI, input, fatal/load-error conditions and other unobserved conditions are outside this evidence.

This neutral-ID derivation comes from an old-format real-engine attempt and a separately retained v3 legacy audit; it is not a new v3 run. Old logs have no `ZZBATCH_DONE`; the last case END is the historical rule. Native natural exit and exit code were not observed: owned processes were forcibly terminated after observation. Py's original stdout/stderr and full original scope records are not included. When Native roles have identical bytes, the evidence files alone cannot authenticate which execution produced each copy; role binding follows separately retained private receipts and provenance.

Native raw/config are associated with Emuera1824+v24 and the Py log with PyEmuera. The repository's [license index](../../LICENSES/README.md), [Emuera original license](../../LICENSES/Emuera1824-v24-license-original.txt), [Emuera notice](../../vendor/emuera/NOTICE.en.md), [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [PyEmuera third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md) are outside this directory. The linked Emuera notice describes a different distribution unit containing a separate source ZIP; this evidence directory contains no such ZIP. Its packaging statements concern that separate unit, not this directory. Survey fixtures, derived data, documentation and new tools follow the repository's [component license index](../../LICENSES/README.md); third-party notices retain their separate terms as listed there.

For offline verification obtain trusted SHA-256 pins for `verify.py` and `manifest.json` through an authenticated independent channel. Compare the verifier before executing it; files or values delivered together are not an independent trust source. Python 3.10 or later, from this evidence directory:

```text
python -c "import hashlib,sys; sys.exit(0 if hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()==sys.argv[2] else 1)" verify.py <TRUSTED_VERIFIER_SHA256>
python -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

Stop if the first command exits nonzero. The verifier checks the fixed 29-case profile, evidence file set, fixture, raw observations, outcomes and verdicts, and the fixed hashes of the shared repository license files. It starts no engine and does not authenticate the historical producer or replay the entire legacy audit. Original-source verification requires separately retained private records. The directory alone is not a complete standalone distribution: provide the linked repository license and notice files with the appropriate relative layout. Rights, privacy, release selection and authenticated pin distribution require separate review.
