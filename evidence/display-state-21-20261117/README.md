# Display state and string lengths: 21 targets in three shared modes

[日本語](README.ja.md)

This evidence set links 21 registered cases and 21 typed targets to the same Native-01, Native-02 and public PyEmuera-01 recordings. The original `matched_scoped` verdict is a **historical record**, not a newly established result. The source group contains 22 cases; `DISPLAYCOMMAND179_STRLEN` is excluded from this 21-case selection, while its two conditions remain in the shared fixture. Roles and markers do not establish target reach or 21 independent runs.

`cases.jsonl` records conditions and limitations. `bindings.json` fixes the selected case ID, typed target, association and marker list; it also records the excluded case and target. There are 138 distinct markers: 13 stages of 10 getters and four length commands under two conditions. The 216 case-to-marker references overlap and are not execution counts.

The offline verifier checks the separately pinned bindings, file set, marker sequence and labels, fixture structure and shared-mode metadata. **It does not independently compare the 138 recorded values to expected values.** The historical report [source-review.ja.md](source-review.ja.md) states selected historical expectations and results; the verifier does not establish that those expectations were met. It does not establish target reach, full compatibility, or rights. Changed values across all three modes can pass the structure check if a new manifest is trusted; the original trusted pin detects changed bundle bytes.

Fixture, config and selected raw bytes are retained per mode. The original detailed receipts and complete original review are not included. The two Native records report process alive at five seconds, no observed natural exit or exit code, and successful cleanup. `DONE` is a log marker, not proof of natural exit. The public wrapper reports returncode 0; that is not a claim about Native exit. The recorded scope excludes actual GUI color/font rendering, invalid colors, other configurations, resize, asynchronous redraw, and the other conditions described in the historical record.

## Offline verification

Obtain all three SHA-256 pins independently through a trusted channel; the manifest and bindings in the same bundle are not their own trust anchors. From this directory:

```powershell
python -B verify.py --manifest-sha256 <trusted-manifest-sha256> --bindings-sha256 <trusted-bindings-sha256> --tool-sha256 <trusted-tool-sha256>
```

The verifier uses the included copy of the common `tools/file_set_manifest.py`, verifies its supplied pin, and checks the separately pinned `bindings.json`. A separately trusted verifier is also required for authenticity. If both a binding and its pin are replaced by an untrusted party, this check does not authenticate the original mapping.

## Rights and notices

See the [license index](LICENSES/README.md), [Emuera original license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [PyEmuera third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The Emuera NOTICE describes a separately distributed source ZIP; this set does not include that ZIP. Rights, privacy and distribution conditions for each fixture, config, raw observation, conditions, comparison, source review and derivative remain under separate review. This set is not approved for publication.
