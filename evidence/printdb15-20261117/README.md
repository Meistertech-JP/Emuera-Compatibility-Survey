# PRINTDB15: saved finite observations

[日本語](README.ja.md)

One physical case, PRINTDB15, has two explicitly registered roles: `command_or_syntax:PRINTDATA` and `structural_syntax:PRINTDATA`. The evidence contains three saved modes, Native-01, Native-02 and public-01; it does not claim separate execution per typed role.

The saved absent-block observation is index 99 and next RAND100 43; an empty DATA item gives index 0 and next RAND100 5. The specific Native no-display warning appears in both Native logs and not in the three saved public streams. Public stderr contains a different OUTPUTLOG warning; absence of all warnings is not claimed. Native natural exit, its exit code and GUI pixels were not observed. The original case verdict is `different_scoped`; both parent outcomes are `documented_difference`.

The Native logs contain Emuera output; public stderr contains PyEmuera diagnostic text. The short fixture consists of survey-generated probe commands and markers. Original configuration, engines, parent documents and full receipts are not included; receipt files are allowlist derivatives. Hashes and private source references do not by themselves authenticate withheld originals.

See [licenses and notices](LICENSES/README.md), [Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera notice](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The Emuera source ZIP described by its notice is not included. These texts do not automatically license survey fixtures, new code or derived data; their rights and final privacy/publication decisions remain unresolved.

Run `python -I -B verify.py --manifest-sha256 <trusted-manifest-sha> --verifier-sha256 <trusted-verifier-sha>`. The verifier embeds the reviewed lineage commitments. A pin received alongside the files is not independently authenticated.
