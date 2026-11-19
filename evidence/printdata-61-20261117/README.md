# PRINTDATA-family finite observations: 61 cases

[日本語](README.ja.md) · [Sources and rights](LICENSES/README.md)

This evidence set requires review before publication. `index.json` links 61 cases, 32 typed targets and 288 target-case roles to 61 sets of saved native-01, native-02 and public-01 mode records. Original case verdicts, conditions, comparisons and unobserved limits are retained. A recorded role does not prove target reach, success, or a separate execution. Continuation of the main script in the 13 uncalled cases does not establish normal execution inside an uncalled body.

`runtime_observation: NOT_RUN` within a condition is a **pre-execution preparation attribute**. It is not the status of the saved mode observations. Consult the saved receipts and raw for those records; this package does not claim a new engine run. Original limits concerning fatal-after state, native natural exit, and missing saved W-mode images remain in force.

Native logs, public stdout/stderr, fixtures and configurations retain their saved bytes. Receipts are derived JSON with personal local paths replaced and lease tokens omitted. Input-before/after and output hashes, mode, and exit/cleanup distinctions remain. All 183 before receipts retain start times; all 183 after receipts retain start and end times, and 108 after receipts retain PID-related cleanup fields. Times and PIDs help correlate historical records; they do not establish personal identity or the identity of a current process. Review their necessity and disclosure scope before publication.

Native logs and configuration relate to the Emuera1824+v24 reference implementation; public output comes from PyEmuera 3.0.0. Survey fixtures are condition-specific probes, and receipts derive from saved records. The original parent review, independent readback text, source ZIP, 7z and executables are not included. Hashes alone cannot let a third party authenticate the withheld originals or historical runs.

[Licenses and notices](LICENSES/README.md) includes the original Emuera license and bilingual notice, plus the PyEmuera license and third-party notices. The Emuera notice's packaging language concerns a **separate distribution unit** containing the original source ZIP; this evidence set does not include that ZIP. Ownership and reuse terms for survey fixtures, new documentation and derived receipts remain separate and undetermined; those notices do not grant a blanket license for this entire set.

Verify offline with Python 3.9 or newer. Before running the verifier, use an external hash utility to check the manifest against its SHA-256 obtained through a separate trusted channel, and check `verify.py` and `tools/file_set_manifest.py` against their SHA-256 values in that trusted manifest. Obtain the pins through a trusted channel separate from the files:

```text
python -B verify.py --manifest-sha256 <manifest SHA256> --bindings-sha256 <bindings SHA256>
```

The verifier checks the file set, hashes, and recorded case/batch/mode/role relationships. It does not authenticate a publisher when the external pins can also be replaced, establish historical execution, or grant rights or privacy approval.
