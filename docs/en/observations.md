# Examples of observed results

[日本語](../ja/observations.md) | [Reading the survey results](results.md)

These examples compare saved inputs and outputs from Emuera 1.824 +v24 and PyEmuera 3.0.0. These observations are a reference for future PyEmuera compatibility fixes and regression checks, as well as other implementations. Each observation is limited to the stated conditions. Follow the links for the inputs, saved output and unobserved scope.

| Target and condition | Emuera observation | PyEmuera observation |
| --- | --- | --- |
| `RAND`, `CompatiRAND:YES` (`COLON_NORMAL_COMPAT_RAND_YES`) | Returned `0` and continued | Stopped with `RAND:n requires n > 0` |
| `RAND:0`, `CompatiRAND:YES` (`COLON_RAND_ZERO_COMPAT_YES`) | Returned `0` and continued | Stopped with the same `E_ARGUMENT` |
| `IF` with its condition and `ENDIF` omitted (`P38`) | Displayed `BEFORE`, then stopped at the offending line | Stopped with a syntax error before displaying `BEFORE` |
| A lone `=` inside an expression (`GMF_LEX_LONE_EQUALS`) | Stopped after `GM_BEFORE` and diagnosed use of `==` for equality | Stopped after `GM_BEFORE` with `E_SYNTAX` for `=` in the expression |
| Statement-form `LINEISEMPTY`, after a complete line and a pending line following `PRINTBUTTON` (`LINEBUF20261115_button_method`) | Output `EMPTY=1` and `BUTTON=0`, respectively | Output the same selected values |
| Expression `CBGSETG(93236,11,12,1)` (`UIQUERY236_cbgsetg-expr-direct`) | The selected log recorded `V=0` | Function resolution returned `E_FUNCTION`; subsequent statements were not reached |
| Statement-form `LIMIT`, `x=8` or `9`, `min=8`, `max=4` | `RESULT=4` | `RESULT=8` |
| `PRINTC` and `PRINTLC`, configured width 25, with empty, `ABC`, and 25-character ASCII inputs | Recorded the selected output lines and `RESULT=777` / `RESULTS=SENTINEL` | Recorded the same selected output and values |

`RAND` and `RAND:0` were observed with separate inputs. The Native result for the unclosed `IF` comes from a saved display capture. Both engines stopped for the lone `=`, with different diagnostics. The `LINEISEMPTY` values cover the stated pending-line condition after `PRINTBUTTON`; they do not establish click or rendering equivalence. The `CBGSETG` example is limited to that direct-call condition.

The two `PRINTC` and `PRINTLC` cases (`COLUMN_PRINTC_EMPTY_SHORT_EQUAL_20261115` and `COLUMN_PRINTLC_EMPTY_SHORT_EQUAL_20261115`) share one fixture across two native runs and one PyEmuera run. The comparison covers selected serialized output and state, not pixel or font equivalence or natural native exit. The original fixture and logs are not included. The [limited reader](../../tools/LEGACY_EVIDENCE.md) can check the recorded conditions and output when the original materials are available.

- [Conditions and saved output for `RAND`, `RAND:0`, `IF` and lone `=`](../../differences/representative-20261116/README.en.md)
- [Search saved Native observations](../../evidence/native-oracle-20261117/docs/native-oracle.html) (113 selected rows)
- [Saved observations for 33 OPCONT268 conditions](../../evidence/native-oracle-20261117/evidence/operator-268-20261117/README.md)
- [Saved `DO` and `LOOP` observations for BREAK and a false condition](../../evidence/doloop259-20261117/README.md) (two native runs and one PyEmuera run with a shared fixture)
- [Selected observations for eight `PRINTDW`, array, level and `SAVECHARA` cases](../../evidence/eight-scoped-observations-20261117/README.en.md) (original raw files not included)
- [`LINEISEMPTY` condition and saved output](../../evidence/lineisempty-acceptance-20261117/README.md)
- [Background-operation results including `CBGSETG`](../../evidence/console-background-24-20261117/README.md)
- [Examples of saved Native PRINT observations](print-observations.md)
- Additional observations: [`PRINTVKW` and `PRINTVDW` after wait release](../../evidence/wait-release-20261117/README.md), and [empty input followed by division by zero in a later argument](../../evidence/wait-c15-20261117/README.md)
- [Saved Native observations for graphics and sprite APIs](../../evidence/graphics-native-saved-20261117/README.md)
- [Native observations for 38 graphics cases](../../evidence/graphics-38-cases-20261117/README.md)
- [Native GUI observations of images, backgrounds, and buttons](../../evidence/graphics-gui-observations-20261117/README.md)
- [Conditions and saved output for `INRANGE`, `LIMIT` and `PRINTVW`](../../evidence/nine-saved-observations-20261117/README.md) ([separately stored configuration](../../harness/fixtures/emuera.config) with the same recorded SHA)
- [Saved observations for expressions, input, diagnostics and side effects](../../evidence/new-replay-20261116/public/README.md)

`python -B tools/query.py METHOD_BOUNDARY_LIMIT_NORMAL_20261115` returns the LIMIT conditions, values from both engines, and saved-output references under `additional_evidence_discovery` / `nine_saved_observations`. Raw and UTF-8 paths in those records are relative to the evidence bundle.

Unverified conditions and cases without a conclusive observation are not classified as successes or differences. These examples are not an exhaustive list of targets or conditions. [Search by target or case ID](../../README.md) for more.

## Character CSV references: CSVFIELDS01

This case reads CSV fields for character ID 1 and index 1. The saved `OUTPUTLOG` files from native Emuera and PyEmuera are byte-identical and record these values:

| Output | Function | Value |
|---|---|---|
| CALL | `CSVCALLNAME` | CALLONE |
| NICK | `CSVNICKNAME` | NICKONE |
| MASTER | `CSVMASTERNAME` | MASTERONE |
| CSTR | `CSVCSTR` | STRVALUE |
| MARK | `CSVMARK` | 13 |
| REL | `CSVRELATION` | 17 |
| TALENT | `CSVTALENT` | 19 |
| FLAG | `CSVCFLAG` | 23 |
| EQUIP | `CSVEQUIP` | 29 |
| JUEL | `CSVJUEL` | 31 |

The comparison covers the output log for one valid character and index. It does not cover invalid, missing or SP conditions, or equality of the entire screen. The log was saved before the subsequent `DONE` output; natural native termination was not observed. The original input files and the two logs are not included in this material.

## SELECTCASE string conditions: SELECT277

These saved records compare four conditions in a shared fixture with state reset for each condition: two native runs and one PyEmuera run. The symbols denote selected observations.

| Case and condition | Native | PyEmuera |
|---|---|---|
| RANGE: `b` falls within `a TO c` | `S=1 LO=1 HI=1 REL=0 T=0 O=123 B=11 A=1` | Same |
| IS: `b`, lower bound `c` does not match, followed by `IS >= b` | `S=1 LO=1 HI=0 REL=1 T=1 O=1245 B=11 A=1` | `S=1 LO=1 HI=0 REL=1 T=0 O=124 B=11 A=1` |
| FALLBACK: `z` matches neither `a` nor `b`, with CASEELSE | `S=1 C1=1 C2=1 O=178 B=33 A=1` | Same |
| NODEFAULT: the same non-matches, without CASEELSE | `S=1 C1=1 C2=1 O=178 B=77 A=1` | Same |

`S` is the selector count; `LO`, `HI`, `REL`, and `T` count condition helpers; `C1` and `C2` count candidate evaluation; `O` records helper order; `B` is the chosen body or retained value; and `A` marks subsequent execution. In IS both record `B=11`, but `T` and `O` differ, so the common body value alone does not show that the same condition was selected. CASEELSE itself is selected only in FALLBACK.

The historical survey ledger records `command_or_syntax:SELECTCASE` as a finite-scope match and `structural_syntax:SELECTCASE` as a documented difference. The four observations above cover selected string conditions from `SELECT277`. The original raw output, fixture and receipts are unavailable in this candidate. Natural Native termination was unobserved. See the [target ledger](../../results/survey.json) for the recorded decisions and case IDs.

## Five MATCH-family cases

The native and PyEmuera saved `OUTPUTLOG` files are byte-identical for each of these cases; the values shown are common to both.

| Case | Inputs, expressions, and results |
|---|---|
| COVMATCH01 | `A=[9,3,9]`, `MATCH(A,9)=2`, `MATCH(A,9,0,2)=1`, `MATCH(A,9,0,3)=2` |
| COVCMATCH01 | Two characters have `CFLAG:0` values 3 and 7. `CMATCH(CFLAG:0,7)=1`; range `[0,1)` gives 0 and `[0,2)` gives 1 |
| COVGROUP01 | `GROUPMATCH(2,2)=1`, `GROUPMATCH(2,1,2,2)=2`, `GROUPMATCH("x","x","y")=1` |
| COVNOSAME01 | `NOSAMES(1,2)=1`, `NOSAMES(1,2,1)=0`, `NOSAMES("x","x")=0` |
| COVALLSAME01 | `ALLSAMES(2,2)=1`, `ALLSAMES(2,2,3)=0`, `ALLSAMES("x","x")=1` |

Each log was saved after the values and before `DONE`. This comparison does not establish equality of the whole screen or stdout, natural termination, empty arrays, invalid arguments, or Japanese collation. The original fixtures and logs are not included in this material.

## Default color getters: GETTER251

In the saved expression-form and command-form fixtures, native default foreground, background, and focus colors were configured as RGB `(17,34,51)`, `(4,5,6)`, and `(7,8,9)` respectively. Each fixture first changed the current foreground and background to different values. Each shared fixture was run twice on native Emuera and once on PyEmuera.

| Target | Native value | PyEmuera value |
|---|---:|---:|
| `GETDEFCOLOR` | 1122867 | 12632256 |
| `GETDEFBGCOLOR` | 263430 | 0 |
| `GETFOCUSCOLOR` | 460809 | 16776960 |

In expression form, the recorded initial values of `RESULT:0`, `RESULT:1`, and `RESULTS` were retained. In command form, the value was written to `RESULT:0`, while the recorded `RESULT:1` and `RESULTS` values were retained. These values apply to the recorded configuration and execution history; they do not establish behavior under other settings or equality of the complete screen. Original raw records and fixtures are not included, and native natural termination was not observed.

## Logical short circuit: OPNORMAL273_E140

With `A=0` and `B=0`, the right operand is `ZZ_BAD()`. Invoking it would increment `A` and evaluate `1/(B-B)`. Two saved Native runs and one later PyEmuera run record the following values.

| Expression | Result | Calls to `ZZ_BAD()` |
|---|---:|---:|
| `0&&ZZ_BAD()` | 0 | 0 |
| `0!&ZZ_BAD()` | 1 | 0 |

The selected markers agree across these three runs, and the right-hand function was not called in either condition. This does not establish other guards, state after a fatal error, or all operator conditions. The earlier Py receipt was not restored; original raw data and the fixture are not included. Native natural termination was not observed.

## GROUPMATCH command form: GROUPMATCH266

These records compare two previously saved native runs with one later PyEmuera run using the same fixture. All three saved `OUTPUTLOG` files are byte-identical for the following four conditions; the table shows their common observations.

| Case | Arguments | `RESULT` | Helper calls / order | `RESULTS` |
|---|---|---:|---|---|
| `GROUPMATCH266_GR0` | `1,1,2,1` | 2 | `4 / 1234` | `SENTINEL` |
| `GROUPMATCH266_GR1` | `1,2,3` | 0 | `3 / 123` | `SENTINEL` |
| `GROUPMATCH266_GR2` | `"a","a","b","a"` | 2 | `4 / 1234` | `SENTINEL` |
| `GROUPMATCH266_GR3` | `"a","b","c"` | 0 | `3 / 123` | `SENTINEL` |

This is a bounded comparison of the command form; it does not establish equality for other inputs, the complete stdout, or the GUI. The later Py receipt does not restore the older Py execution receipt, and native natural termination was not observed. Original logs, fixture, and receipts are not included.

## ELSEIF and ENDIF branching: IFCHAIN269

In saved records from two native runs and one PyEmuera run of the same fixture, the following selected values agree. `C1`–`C3` count condition-helper calls, `ORDER` records their order, and `AFTER` marks continuation.

| Case | Condition | DEST | C1 / C2 / C3 | ORDER | AFTER |
|---|---|---:|---|---:|---:|
| `IFCHAIN269_P1` | First condition false, next ELSEIF true | 22 | 1 / 1 / 0 | 12 | 1 |
| `IFCHAIN269_P2` | All conditions false, no ELSE | 79 | 1 / 1 / 1 | 123 | 1 |

ELSEIF is treated as an evaluated condition and ENDIF as the paired structure and continuation. The unselected ELSE in P1 was not observed executing. Native natural termination and QUIT completion were not observed; original raw data and fixture are not included.

## Unregistered function names

In the absence cases for `CHKVARDATA`, `CHKGLOBALDATA`, and `FIND_VARDATA`, both native Emuera and PyEmuera failed name resolution on line 4 and did not reach `OBS225` or `DONE225`. PyEmuera emitted `E_FUNCTION: Unknown function` and exited with code 1. Native natural termination was not observed. The original `matched_scoped` verdict means a bounded match in name-resolution failure, not a successful call.

In separate controls using user functions with the same names, the recorded return values and helper counts agree, while the name-collision warnings differ. Unexecuted portions of the commented-out native handlers and hypothetical argument contracts were not tested. Original raw data and fixtures are not included.

## Graphics API availability: RECEIPT252

These saved records invoke each target in a separate fixture with no image resources in the initial inventory. Native Emuera produced the values below for both expression and command forms, then reached `AFTER` and `DONE`.

| Target | Condition | Native value in both forms |
|---|---|---:|
| `SPRITEWIDTH` | Missing `ZZ_MISSING` | 0 |
| `SPRITEHEIGHT` | Missing `ZZ_MISSING` | 0 |
| `SPRITEPOSX` | Missing `ZZ_MISSING` | 0 |
| `SPRITEPOSY` | Missing `ZZ_MISSING` | 0 |
| `GCREATED` | Graphics ID 0 | 0 |
| `GCREATE` | Graphics ID 0, width and height 16 | 1 |

`GCREATED` and `GCREATE` use separate fixtures and do not show a before-and-after change within one run. Expression and command forms are separate typed targets. Sixteen saved native witnesses were used; no new native run was made for the later comparison.

All 12 later PyEmuera runs stopped before returning a target value. Expression forms produced `E_FUNCTION`; command forms were rejected at load with `E_LOAD`. Neither `AFTER` nor `DONE` appeared. This is not a numeric comparison of PyEmuera values with the native 0 or 1. Case IDs follow `RECEIPT252_expression_function_<target>` or `RECEIPT252_method_as_command_<target>`.

Behavior with existing image resources, pixel or complete GUI equivalence, and native natural termination are outside the observations. Original logs, fixtures, and receipts for this section are not included. The [38 graphics cases](../../evidence/graphics-38-cases-20261117/README.md) cover separate conditions.
