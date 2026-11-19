# Grammar and supplemental observations

[日本語](README.ja.md)

This evidence bundle contains saved observations of 16 COLON grammar cases and 8 supplemental label cases, with three recorded modes per case. These 24 cases are separate from the 694 main targets. It retains the original finite conclusions, diagnostic and stopping conditions, and unobserved states; it is not a new engine execution or a claim of complete compatibility. Probe bodies, original receipts, engines and some parent evidence are not included.

An independent, limited privacy review by an AI separate from the bundle’s preparer examined the 600 evidence materials and found no specific secret, personal-information, developer-instruction or third-party game-story/image issue in its stated scope. This is not a guarantee that every privacy or rights concern has been resolved. The rights holder and permission scope for survey-created fixtures, derived records, documentation and tools remain undetermined; no project-wide permission is inferred. The current candidate is not final publication approval.

The common verifier compares all 24 cases, typed values, field presence, unobserved-state requirements, family/parent identity, mode roles, paths and hashes against a fixed contract derived from the independently reviewed snapshot. A contract change needs a separately reviewed verifier and trusted pin. A checksum or a pin received beside the data does not independently authenticate the source. Identical bytes in different modes cannot establish which execution produced each copy; supplemental receipt files do not themselves contain case/mode fields, so the linkage relies on the retained readback and directory provenance.

With Python 3.9 or later, obtain the manifest, bindings, contract and verifier SHA-256 pins through an authenticated independent channel. Compare the verifier hash before running it; a value received only beside the data is not an independent trust source. From this directory:

```text
python -c "import hashlib,sys; sys.exit(0 if hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()==sys.argv[2] else 1)" verify.py <VERIFIER_SHA256>
python -I -B verify.py --manifest-sha <MANIFEST_SHA256> --bindings-sha <BINDINGS_SHA256> --contract-sha <CONTRACT_SHA256> --verifier-sha <VERIFIER_SHA256>
python -I -B negative_checks.py --manifest-sha <MANIFEST_SHA256> --bindings-sha <BINDINGS_SHA256> --contract-sha <CONTRACT_SHA256> --verifier-sha <VERIFIER_SHA256>
```

Stop if the first command exits nonzero. See the [license index](LICENSES/README.md), [Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera notice](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The unchanged Emuera notice describes a different distribution unit containing a separate original source ZIP. Its statements about packaging that ZIP apply to that other unit, not this evidence bundle; neither that ZIP nor the 7z is included here. The license texts and notices are retained without alteration.
