# PRINTVKW and PRINTVDW: empty input and an error in a later argument

[日本語](README.ja.md) | [Machine-readable observations](observations.json)

Each original fixture waits after printing an empty string. After Enter, the same command evaluates another set of arguments. Native displayed `AFTER_EMPTY`, `BEFORE_FAULT`, and `FIRST_TERM_SIDE_EFFECT` in that order, then reported division by zero in the second argument at line 7. PyEmuera showed the same marker sequence and reported `E_ARITH` at line 7 with exit code 1. Diagnostic formats differ.

| Case | Fixture | Native before Enter | Native after Enter and diagnostic | Py stdout / stderr |
|---|---|---|---|---|
| PRINTVKWC15 | [ERB](PRINTVKWC15/fixture.erb) | [screen](PRINTVKWC15/native-before.bmp) | [screen](PRINTVKWC15/native-after.bmp) | [stdout](PRINTVKWC15/py-stdout.bin) / [stderr](PRINTVKWC15/py-stderr.bin) |
| PRINTVDWC15 | [ERB](PRINTVDWC15/fixture.erb) | [screen](PRINTVDWC15/native-before.bmp) | [screen](PRINTVDWC15/native-after.bmp) | [stdout](PRINTVDWC15/py-stdout.bin) / [stderr](PRINTVDWC15/py-stderr.bin) |

Native received an empty Enter in the owned control on a private desktop; the owned process was terminated after observation and natural exit was not observed. PyEmuera received one empty line via standard input. Post-error variable state, other inputs and arguments, and cross-engine pixel equality were not established. The original survey's historical unverified status is retained; these are separate subsequent observations.

The saved Native histories use UTF-16LE with a BOM: [PRINTVKWC15](PRINTVKWC15/native-history.bin), [PRINTVDWC15](PRINTVDWC15/native-history.bin).

`manifest.json` records the included files' sizes and SHA-256 values. Publication terms for these materials are under review.
