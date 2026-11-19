# SPRITEMOVE finite availability and saved observations

[日本語](README.ja.md)

`expression_function:SPRITEMOVE` and `method_as_command:SPRITEMOVE` are different typed keys. Their positions in the shared adapter, parent matrix, two cases each, fixtures, two Native logs, and PyEmuera stdout/stderr remain separate. Both target outcomes are `documented_difference`, not public value parity.

Native registration, signature, and method-form result routing are source-only evidence. Native method form assigns the Int64 return to `RESULT`; expression form returns a value within an expression. This is not a public runtime observation. The saved public expression case reports runtime `E_FUNCTION`; the command-form case reports load-time `E_LOAD`. Native selected states are saved observations, not evidence of successful public execution or value, pixel, or lifecycle equivalence. Native natural exit and GUI pixels were not observed.

The complete original ledgers, receipts, configuration, engines, sprite BMP/CSV inputs and original source archives are withheld. Their hashes and pointers identify source material but cannot be checked against the original contents without access to those private records. The complete historical inputs and run conditions cannot be reconstructed from this evidence directory alone. This package does not authenticate historical execution or establish redistribution rights or coverage of the other 75-target group.

```sh
python3 -I -B verify.py --manifest-sha256 "$(cat manifest.sha256)"
python3 -I -B test_negative.py --manifest-sha256 "$(cat manifest.sha256)"
```

Obtain the manifest hash from a trusted independent channel; a bundled checksum is not a signature. Fixtures and logs retain their original bytes; the manifest records original and derivative hashes.

## Verification and distribution notices

The verifier reconstructs Oxx records from wrapped Native log fragments and compares every selected state field and RESULTS in both saved logs per case. It accepts only the saved record grammar and fails closed for unknown or unparseable values. This verifies consistency of the saved records, not historical execution, GUI pixels or public value parity. Source bytes for withheld material cannot be independently authenticated from their hashes alone.

This projection alone excludes original configuration, complete receipts, BMP/CSV drawing inputs and engines; its hashes do not reconstruct them. The repository separately contains [harness/fixtures/emuera.config](../../harness/fixtures/emuera.config), which has the same recorded configuration SHA; it is not contained in this evidence directory. The synthetic BMP and CSV are also not contained here.

See [NOTICE.en.md](NOTICE.en.md) for Emuera and PyEmuera license and attribution paths, distribution-unit requirements, and the unresolved license status of survey artifacts. Those license/NOTICE documents are not bundled in this projection. An independently trusted manifest pin is required; the verifier also checks that the bundled checksum agrees with it.

The selected observation fields were originally transcribed from the case register. This verifier independently compares those retained fields with the saved Native logs; the original provenance statement describes how the fields were generated, not a limit on the current comparison. The verifier also enforces the four distinct case IDs, exact field keys, and integer types excluding JSON booleans and floats.
