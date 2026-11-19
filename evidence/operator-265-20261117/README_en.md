# Assignment evidence

[23 observations](OBSERVATIONS_en.md) · [Machine-readable records](records.json) · [日本語](README_ja.md)

Original raw channels, ERB, ERH and config are byte-preserved. These records do not close every associated typed target. No engine is included. Material authorship and redistribution rights require review; this is not publication approval.

The verifier and `tools/file_set_manifest.py` are executable code. Before executing either, compare their SHA-256 values with independently distributed trusted values. Obtain the code hashes, manifest pin and separate source-profile pin from a trusted location outside this bundle. Then run `python -B verify.py --inventory-tool PATH_TO_tools/file_set_manifest.py --pin EXTERNAL_MANIFEST_SHA256 --profile-pin EXTERNAL_PROFILE_SHA256`.

The [source profile](source-profile.json) fixes the typed keys and 71 source ranges for 23 cases as recorded in the frozen original, plus identities for 27 source members. The verifier checks metadata against the independently pinned profile. Source bytes are not included: without archives the tool explicitly reports source-byte and line-content checks as `NOT RUN`. Add `--native-source-zip PATH` and/or `--py-source-pyz PATH` to check each supplied archive SHA, member bytes and selected line hashes read-only. This does not establish that each line semantically supports a claim or that the executable was built from that source. Pins taken only from the same untrusted bundle do not establish authenticity.

[Registered case IDs and traces](CASE_INDEX_en.md) · [Input preparation and bounded rerun](REPRODUCE_en.md) · [Engine identification](environment.json)

[Emuera license](licenses/Emuera1824-v24-license-original.txt) · [Emuera NOTICE](licenses/NOTICE.en.md) · [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt) · [PyEmuera third-party notices](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)

The Emuera NOTICE describes a separately retained original ZIP distribution; that ZIP is not included in this evidence bundle. Distribution references in the PyEmuera third-party notices likewise refer to the original PyEmuera distribution. Rights and permission for these fixtures/config/raw require separate review.
