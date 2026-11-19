# SPRITESETPOS finite availability and saved observations

[日本語](README.ja.md)

`expression_function:SPRITESETPOS` and `method_as_command:SPRITESETPOS` are different typed keys. Their positions in the shared adapter, parent matrix, two cases each, fixtures, two Native logs, and PyEmuera stdout/stderr remain separate. Both target outcomes are `documented_difference`, not public value parity.

Native registration, signature, and method-form result routing are source-only evidence. Native method form assigns the Int64 return to `RESULT`; expression form returns a value within an expression. This is not a public runtime observation. The saved public expression case reports runtime `E_FUNCTION`; the command-form case reports load-time `E_LOAD`. Native selected states are saved observations, not evidence of successful public execution or value, pixel, or lifecycle equivalence. Native natural exit and GUI pixels were not observed.

The complete original ledgers, receipts, original configuration, engines, sprite BMP/CSV inputs and original source archives are not included in this evidence directory. The surrounding distribution includes a [configuration file](../../harness/fixtures/emuera.config) with the same SHA-256 as the recorded configuration for all 12 modes: `f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc`; it is not bundled here. The hash does not establish historical execution or the meaning of every setting. Full configuration, sprite inputs and run conditions cannot be reconstructed from this evidence directory. Source hashes and pointers cannot be checked against withheld originals without access. This package does not authenticate historical execution or establish redistribution rights or coverage of the other 75-target group.

```sh
sha256sum verify.py
python3 -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
python3 -I -B test_negative.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

The SHA-256 of the included `verify.py` is `631cd4e9043926260f4e717e91c5d66347767aa540ca5186cb131ad9888f3543`. Obtain the manifest and verifier hashes through a trusted independent channel. Replace the angle-bracket placeholders and check the verifier before executing it using `sha256sum` or another trusted tool; on Windows use `Get-FileHash .\verify.py -Algorithm SHA256`. The verifier checks agreement among `manifest.sha256`, the external pin and actual manifest hash, the pinned source-to-copy bindings and byte-copy hashes, and all 16 observations and 160 values reconstructed from wrapped Native logs. A bundled checksum is not a signature; hashes do not authenticate authorship, historical execution or redistribution rights.

The verifier requires the exact unique four-case ID set and its typed-key mappings. It checks the eight recorded observations for the exact nine state keys with integer values excluding booleans and floats, string `RESULTS`, and ordered string IDs: 72 integers and eight result strings. Values were selected from the case register when the records were created; the current verifier reconstructs and compares the retained Native raw observations in both modes.

## Sources and reuse conditions

For Native logs, see the [Emuera original license](LICENSES/Emuera1824-v24-license-original.txt) and [Emuera notice](vendor/emuera/NOTICE.en.md). For PyEmuera diagnostics, see the [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The Emuera notice describes a separate source ZIP, which is not included here. Rights holders and terms for the survey fixtures, records and new code remain unresolved; PyEmuera's MIT license is not automatically applied to all survey materials. Include applicable notices when redistributing these materials separately.

The surrounding distribution also has a [license index](../../LICENSES/README.md) and its [Emuera notice](../../vendor/emuera/NOTICE.en.md).

The saved Native source distinguishes absolute position assignment for SPRITESETPOS from relative offset for SPRITEMOVE; this is static evidence, not an additional runtime test.
