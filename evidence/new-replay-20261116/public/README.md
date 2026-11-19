# Selected replay evidence, 2026-11-16

[日本語](README.ja.md)

This is provisional evidence from bounded Native Emuera1824+v24 and PyEmuera 3.0.0 runs. It includes byte-identical selected logs, fixtures and crops of the owned window, plus result records projected from the original receipts. Original process receipts and attempt seals are not included.

```text
python -B verify.py
```

The verifier checks the exact file set and SHA-256 values, selected log observations, pinned crop format and hashes, and configuration and license identity. It does not interpret image pixels, run engines, validate the private original seals, or authenticate authorship. The manifest is not a digital signature.

## Included cases

| Group | Evidence and limits |
|---|---|
| [Expressions](expression/successful-rerun/plan.json) | `ABS((-7 + (RESULT:0 - 701)))` yielded 7 on both. `STRFINDU("abc","",(3 + (RESULT:0 - 701)))` and `STRFIND` with the same arguments yielded -1 on Native and 3 on Py. ABS-only and three-case batch use separate fixtures, with two Native runs each. RESULT:0=701, RESULT:1=702 and RESULTS=AUTO_SENT remained unchanged in each observation. |
| [State writes](local/state-write/fixture.ERB) | Before and after `TOINT "42"` and `TOSTR 123`, RESULT:0 changed 701→42 and RESULTS AUTO_SENT→123, in the same order in both logs. |
| [Number input](local/input-number/fixture.ERB) / [string input](local/input-string/fixture.ERB) | P35 receives 42 and P36 receives ABC. Native before/after crops and Py stdout record 42 and `[ABC]`, respectively; images require manual interpretation. |
| [Number with OUTPUTLOG](local/input-number-logged/fixture.ERB) / [string with OUTPUTLOG](local/input-string-logged/fixture.ERB) | Separate fixtures receive 42 / ABC; both logs record `INPUT_RESULT=[42]` / `INPUT_RESULTS=[ABC]`. Before/after crops are included; do not conflate these with the original fixtures. |
| [Missing argument](local/argument/fixture.ERB) | After `BEFORE`, Native reports a line-3 `TOINT` argument-count error; Py reports `E_ARGUMENT` at line 3 after `BEFORE`. Stdout, diagnostics and crop are included. |
| [Syntax and stop position](local/syntax-stop/fixture.ERB) | After load warnings, Native emits `BEFORE` then a missing `ENDIF` error at line 3. Py reports `E_SYNTAX` at load; `BEFORE` is not observed in stdout. Stdout, diagnostics and crop are included. The right edge of the first warning is clipped in the P38 crop. |

Native was forcibly terminated after the recorded observations; natural exit was not observed. GUI observations are manual reviews of lower-left crops of owned windows on an isolated desktop. They do not establish a full-screen match, IME behavior, other inputs or natural Native exits. Execution-time fixture pinning was not established for the error cases; input cases record the fixture-pin check.

## Configuration, attribution, and distribution

[`config/emuera.config`](config/emuera.config) retains the exact CP932 bytes used in the recorded attempts; its SHA-256 is in `configuration.json`. Replay also requires the engines, environment and an appropriate procedure. Engine executables are not included in this evidence package.

The Emuera-derived configuration, screens and diagnostics are accompanied by the [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt). PyEmuera diagnostics are accompanied by the [MIT license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The notices are the unchanged text from the complete PyEmuera 3.0.0 source distribution; they also describe games and other components not included in this evidence package, and their file paths refer to that original distribution. Only window crops are retained; full original screens are not included. Fixtures, logs and crops are associated with their respective attempts; identical bytes from separate attempts are not merged.

Build the distribution from manifest-listed files plus `manifest.json`. Original receipts, seals and internal source mappings remain private and are not included. Images require human interpretation. A final audit of the complete publication candidate remains separate.

## Raw evidence

- Expression batch: [Native 1](expression/successful-rerun/batch/native-01.log), [Native 2](expression/successful-rerun/batch/native-02.log), [Py](expression/successful-rerun/batch/py.log). ABS-only logs are in `single/`.
- State writes: [Native](local/state-write/native.log), [Py](local/state-write/py.log).
- Argument: [Native diagnostic](local/argument/native-diagnostic.log), [Py stdout](local/argument/py-stdout.bin), [Py diagnostic](local/argument/py-stderr.bin).
- Syntax: [Native diagnostic](local/syntax-stop/native-diagnostic.log), [Py stdout](local/syntax-stop/py-stdout.bin), [Py diagnostic](local/syntax-stop/py-stderr.bin).
- Native screen after input: [number](local/input-number/native/crop-after.bmp), [string](local/input-string/native/crop-after.bmp), [number with log](local/input-number-logged/native/crop-after.bmp), [string with log](local/input-string-logged/native/crop-after.bmp).
