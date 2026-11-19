# Saved STRLEN control observation

[日本語](README.ja.md)

This is a projection of one saved case, `ARGBOUND246_strlen-control`, for `command_or_syntax:STRLEN`. Its earlier case ID is `PARENT246_strlen-control`. The local case verdict is `matched_scoped`; the final finite target outcome is `documented_difference` because other conditions differ. This one case does not establish compatibility for the whole target or other targets.

The CP932 fixture runs `STRLEN "abc"` to measure raw text including its quotation marks. Two saved Native outputs and one PyEmuera output contain the selected state `A=919 B=818 R=5 N=1 F=173` and a completion marker. Full log or GUI equivalence is not asserted. Native natural exit and exit code were not observed. PyEmuera stderr is retained separately.

## Verification

With Python 3 standard library, from this directory:

```sh
python3 -I -B verify.py --manifest-sha256 "$(cat manifest.sha256)"
python3 -I -B test_negative.py --manifest-sha256 "$(cat manifest.sha256)"
```

The verifier checks that `manifest.sha256`, the supplied manifest pin, and the actual SHA-256 of `manifest.json` agree. It also checks the file hashes, typed key, case ID, recorded outcomes, fixture, three raw outputs and selected markers, and selected execution metadata. The commands above use the bundled checksum for convenience; for independent identification, supply a pin obtained through a trusted independent channel. A checksum supplied with the files is not a signature or independent proof of authenticity.

## Withheld originals and configuration

The original full ledgers, complete parent review, execution receipts, and original configuration are not included in this evidence directory. The manifest records their source SHA-256 values, JSON pointers, and the selections or transformations used. A third party cannot directly verify selected values against those withheld originals. The derived receipts are selected records, not independently authenticated copies of the full receipts.

The three recorded configuration hashes match the SHA-256 of the separate candidate [configuration file](../../harness/fixtures/emuera.config): `f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc`. The file is elsewhere in the candidate, not in this evidence directory. Matching hashes alone do not establish the historical executions or the effect of every setting. Full engine setup and a runtime rerun procedure are not included.

The earlier parent review is retained as `finite_remaining_proof`, separate from final target acceptance after further observations. Raw evidence for those later conditions is outside this case package, so the target-wide difference cannot be reverified here.

## Sources and reuse conditions

For the referenced engines, see the candidate's [Emuera original license](../../LICENSES/Emuera1824-v24-license-original.txt), [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [PyEmuera third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). Separate redistribution of this evidence needs the applicable notices alongside it. The rights holders and licensing scope of all survey materials remain unresolved; this case does not settle them.
