# Eleven selected saved evidence cases

[日本語](README.ja.md)

This material contains eleven cases whose old and registered IDs are explicitly mapped in the original ledger. Each case retains its own fixture, two Native logs, PyEmuera stdout and stderr, comparison outcome, and finite target outcome. Equal hashes do not merge different modes or cases.

Normal continuation, diagnostic difference, Native-only continuation, a skipped branch, and the separately structured state comparison are checked under distinct rules. A match in a skipped branch is not proof of executing the target command. Native natural exit was not observed.

For the eight cases in the 245 series, `target_runtime_entered` is derived from the fixture's `dead` condition and interpreted alongside the saved output. It is not an independently measured trace of entry into an engine method.

Parent acceptance and each local case verdict are distinct. ADDCOPYCHARA `single`, `dead_hole`, and `dead_string` are absent from the selected parent review's case_ids; its `accepted` decision is not individual approval of those three cases. COPYCHARA control is outside case_ids but named in the parent's accepted_scope. STRLEN trailing's `finite_remaining_proof` is a historical parent review, separate from the final target outcome `documented_difference` after later observations. Each `requirement_ids` entry is a reference, not proof that a single case satisfies the whole requirement.

From this directory with Python 3:

```sh
python3 -I -B verify.py --manifest-sha256 "$(cat manifest.sha256)"
python3 -I -B test_negative.py --manifest-sha256 "$(cat manifest.sha256)"
```

The manifest records original hashes, source JSON pointers and derivative hashes. Original full ledgers, parent reviews, execution receipts, original configuration and engine binaries are absent from this evidence directory; a third party cannot directly inspect the original records or reconstruct a full execution. A separate candidate [configuration file](../../harness/fixtures/emuera.config) has the same SHA-256 as the records for all 33 modes: `f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc`. Matching hashes do not establish historical execution or semantic equivalence of every runtime condition.

The verifier checks the format of `manifest.sha256` and agreement between its bundled pin, the supplied external pin, and the actual manifest SHA. The commands above use the bundled pin for convenience. For independent identification supply a pin obtained through a trusted separate channel; the bundled checksum is not a signature or proof of authenticity.

## Sources and reuse conditions

For Native logs and diagnostics, see the [Emuera original license](../../LICENSES/Emuera1824-v24-license-original.txt) and [Emuera notice](../../vendor/emuera/NOTICE.en.md). For PyEmuera output, see the [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). See also the candidate's [license guide](../../LICENSES/README.md). If redistributing this directory separately, accompany it with the applicable notices and linked materials. Rights holders and reuse conditions for the survey as a whole, including fixtures and new code, remain unresolved; the PyEmuera MIT license is not automatically applied to all survey materials.

This verifies selected saved evidence, not historical execution authenticity, licensing, target-wide behavior, or compatibility across all 694 targets.
