# DO and LOOP: saved observations for BREAK and a false exit condition

[日本語](README.ja.md) · [Selected observations JSON](observation.json) · [Source SHA-256 digests](source-digests.json)

This is the finite case `DOLOOP259_BREAK_SUPPRESSION`. The source register associates this single case with `command_or_syntax:DO`, `command_or_syntax:LOOP`, `structural_syntax:DO`, and `structural_syntax:LOOP`, with verdict **matched_scoped**. These four roles are not four separate executions or a claim of complete compatibility.

## Conditions and results

The saved record uses empty CSV and the same ERB, ERH and configuration fixture for two runs of Emuera 1.824 +v24 (Native) and one run of PyEmuera 3.0.0 (Py). The first DO breaks on its second body entry; a separate DO evaluates a false LOOP condition after its body. A guard returns false and prevents calls to a function that would divide if invoked. Initial values are `RESULT=701` and `RESULTS=sentinel259`.

The table gives values common to all three saved histories. B/F are body-entry counters, BC/FC are the first/second condition-helper counters, G is the guard counter, and X is the fault-helper counter.

| Observation | Native, both runs | Py, one run |
|---|---|---|
| First DO body | `B=1 BC=0 X=0` → `B=2 BC=1 X=0` | Same |
| Before BREAK → after exit | `B=2 BC=1 G=2 X=0` → `B=2 BC=1 G=2 X=0` | Same |
| False-condition DO body → after condition | `F=1 FC=0 X=0` → `F=1 FC=1 G=3 X=0` | Same |
| Final values | `O=12113 TMP=0 X=0` | Same |
| Result sentinels | `RESULT=701`, `RESULTS=sentinel259` at begin, after BREAK, after the false condition, and final | Same |

`O` accumulates helper-call order. The first LOOP condition is evaluated once on the first iteration and skipped on the BREAK iteration. The second DO enters its body once, evaluates its false condition once, and exits. The guard is evaluated three times and the fault helper is not called. The skipped LOOP instance is not counted as a normal execution. Each history reaches the last retained checkpoint `C259_DONE`; all three history byte streams match.

The source verdict `matched_scoped` is retained. The comparison records `MATCHED_FINITE` after classifying the Py OUTPUTLOG notification within its stated scope. Py returned exit code 0 without timeout. Both Native processes were still alive after five seconds and were subsequently terminated by the execution controller, so **natural exit was not observed**. `C259_DONE` is not an instruction-level trace of QUIT.

## Scope and exclusions

This is a selected projection of saved observations, not a new run. It does not establish an actual divide-by-zero positive control, malformed syntax, all-input behavior, screen or timing parity, or completion of the structural targets. Original logs, fixture, configuration, receipts, comparison documents and executables are excluded because their rights and absence of confidential information have not been established here. Readers cannot independently check the original bytes or reproduce the run from this document alone. The selected observations JSON records the SHA-256 of each history, but hashes alone cannot verify the original log contents or authenticity.

From this directory, the following command checks the included file set and hashes. A matching manifest does not authenticate the publisher or the original execution.

```text
python -I -B ../../tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```
