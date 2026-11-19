# Saved operator observations: 24 conditions

[日本語](README.ja.md)

[Observation data](observations.json) records 24 bounded conditions, including ternary and increment/decrement expressions, with two Emuera1824+v24 modes and one PyEmuera 3.0.0 mode per condition. Each mode links its ERB, ERH, configuration, saved output, diagnostics, and SHA-256. The CSV directory was empty. Values, events, error lines, and unobserved state are recorded separately.

Continuation through an uncalled branch does not establish execution of its body. Destination state after an error and natural Native termination were not observed. Two modes without a recorded normal trace keep `null`; their saved diagnostics are retained separately. These finite observations do not establish complete operator compatibility.

Native executable SHA-256: `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`. PyEmuera pyz SHA-256: `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35`. Neither engine is included.

Before running, verify `verify.py` itself against its SHA-256 from a separate trusted channel. Supply the manifest and `tools/file_set_manifest.py` SHA-256 values from that channel and use Python 3.10 or newer:

```text
python -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

Verification checks stored files against displayed lines. It does not rerun either engine or prove historical execution or reuse rights. Consult the distribution notices for fixtures, configuration, output and code.

## Inputs and verification scope

To reconstruct a condition in a new working directory, create empty `ERB/` and `csv/` directories; copy the mode's `assets/<unit-id>/<mode>/ERB_REVIEW.ERB` to `ERB/REVIEW.ERB`, `ERB_REVIEW.ERH` to `ERB/REVIEW.ERH`, and `emuera.config` to the root. Keep `csv/` empty. Obtaining and running the engines requires a separate environment and procedure. Engine hashes identify the recorded artifacts; they do not guarantee the same environment or natural termination.

The 24 conditions and 72 mode records (48 Native, 24 Py) correspond to existing registered cases and must not be counted again as new cases. Verification does not start either engine. It checks the file set, trace lines, events and state lines against raw output, and diagnostic reasons. It does not independently re-adjudicate the semantic correctness of verdicts, conditions, targets, post-error state or natural exit; these depend on the pinned manifest and review of the original comparison. Review content separately before trusting a newly resealed manifest.

## Notices and reuse

For the configuration and Native output, see the [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt) and [Emuera notice](vendor/emuera/NOTICE.en.md). For PyEmuera output, see the [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). Reuse rights for the survey ERB/ERH and derived data do not automatically follow from the engine licenses.

`case_id` identifies the registered main-ledger case; `planned_id` is the original condition identifier. Targets, conditions and verdicts were checked against the original ledger.
