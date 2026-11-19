# Native Emuera PRINT examples from saved observations

[日本語](../ja/print-observations.md)

These examples come from selected conditions in the shared batch `PRINTKD212_SHARED`, using one fixture. They are not separate executions per condition. The saved Native 01 and Native 02 histories have the same SHA-256; the byte ranges below were checked against both.

`P>` and `<T` are markers printed by the fixture before and after the command. `\r\n` denotes a recorded line break. See the [input ERB][fixture] (CP932), [configuration][config], [Native 01 history][n1], [Native 02 history][n2], and [condition and byte-range index][index]. Each history is UTF-16 LE with a BOM; byte offsets are measured from the start of the file and the end offset is exclusive.

## 1. FORCEKANA with PRINTVK

With `PRINTVK ZZ212N(1),"/",ZZ212S(2)`, the histories contain the following lines for each `FORCEKANA` value. The fixture function `ZZ212S(2)` returns `あアｱ`.

| Condition | Fixture command line | Output including markers | History byte range |
|---|---:|---|---:|
| `C212_0`: 0 | 10 | `P>1/あアｱ<T` | `[62, 168)` |
| `C212_1`: 1 | 22 | `P>1/アアｱ<T` | `[220, 326)` |
| `C212_2`: 2 | 34 | `P>1/ああｱ<T` | `[378, 484)` |
| `C212_3`: 3 | 46 | `P>１／あああ<T` | `[536, 642)` |

Each range also contains the following state line: `A=2 B=12 R=701 S=[sentinel]`. The saved characters, digits and punctuation differ across these conditions. This example does not establish a rule for every character.

## 2. Literal string and formatted string

With `FORCEKANA 0`, `ZZ212T(1)` returns `あアｱ{ZZ212N(2)}`. The commands and saved histories differ as follows.

| Condition and fixture line | Command | Output including markers | Recorded state | Byte range |
|---|---|---|---|---:|
| `C212_4`, line 58 | `PRINTSK ZZ212T(1)` | `P>あアｱ{ZZ212N(2)}<T` | `A=1 B=1` | `[694, 816)` |
| `C212_12`, line 154 | `PRINTFORMSK ZZ212T(1)` | `P>あアｱ2<T` | `A=2 B=12` | `[2116, 2222)` |

In this fixture, `A` and `B` record helper-call count and order. One saved condition retains `{ZZ212N(2)}` as text; the other records `2` in its place.

## 3. Nonempty and empty SINGLE

For `PRINTSINGLEK` with `FORCEKANA 0`, compare the nonempty and empty conditions. The lines recorded in the saved history include the markers.

| Condition and fixture line | Command | Saved lines between markers | Byte range |
|---|---|---|---:|
| `C212_36`, line 442 | `PRINTSINGLEK あアｱ{ZZ212N(1)}` | `P>\r\nあアｱ{ZZ212N(1)}\r\n<T\r\n` | `[6566, 6698)` |
| `C212_75`, line 910 | `PRINTSINGLEK` | `P><T\r\n` | `[13504, 13600)` |

The nonempty text is saved on a line separate from the markers. In the empty condition, the Native **history** contains no blank line between them. This does not assert whether another output stream contains a blank line.

## 4. Display-suppressed condition

For `C212_85`, fixture lines 1030–1032 place `SKIPDISP 1`, `PRINTFORMSK ZZ212T(1)`, and `SKIPDISP 0` in sequence, with `FORCEKANA` set to 3. The saved Native history contains `P><T\r\n`, followed by `C212_85_STATE A=0 B=0 R=0 S=[sentinel]`. The byte range is `[15024, 15116)`. This is an example of the output and state recorded under that condition, not a generalization to every display-suppressed condition.

Actual text display and rendering on the GUI screen, GUI color, font and style, and Native natural termination are not established by these saved histories. The shared assets also retain seven conditions outside this 82-case selection; none is used in the examples above.

[fixture]: ../../evidence/print-kd-shared-82-20261117/assets/native-01/inputs/ERB/SEARCHBOUND01.ERB
[config]: ../../evidence/print-kd-shared-82-20261117/assets/native-01/inputs/emuera.config
[n1]: ../../evidence/print-kd-shared-82-20261117/assets/native-01/raw-history.bin
[n2]: ../../evidence/print-kd-shared-82-20261117/assets/native-02/raw-history.bin
[index]: ../../evidence/print-kd-shared-82-20261117/index.json
