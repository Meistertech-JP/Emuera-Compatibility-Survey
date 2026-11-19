# Saved observations: compound assignment with a trailing comma

[日本語](README_ja.md) · [Machine records](records.json) · [Typed-key mapping](mapping.json) · [Environment and engine identities](environment.json)

These are saved observations for two specified inputs. The parent catalog verdict for both cases is `different_scoped`, and the survey marks both typed targets `documented_difference`. The recorded semantic verdict remains `PARENT_ADJUDICATION_REQUIRED`; this supplement does not change it. Associated typed keys describe shared mechanisms, not separate executions. Only the operator actually written on line 12 of each fixture is identified below.

Both fixtures set `A=0 B=0 C=701 E=0 F=0`, `ZZREVD:0=6`, `ZZREVD:1=99`, `LOCALS="ab"`, and `ZZREVS="ab"` before printing `BEFORE`. These are fixture initializations, not separately read-back Py values. See each ERB, ERH, and config for the complete inputs; the CSV input is empty. In the output, `D0` and `D1` denote `ZZREVD:0` and `ZZREVD:1`, and `S` denotes `LOCALS`.

## `assignment_syntax:*=` — C022

Case `OPISOLATED265_compound-trailing-comma`; input line `ZZREVD:0*=7,`. [ERB](fixtures/C022/ERB/REVIEW.ERB) · [ERH](fixtures/C022/ERB/REVIEW.ERH) · [config](fixtures/C022/emuera.config).

Native `native-01` and `native-02` each printed `BEFORE`, `REVIEW AFTER C=701 A=0 B=0 D0=42 D1=99 S=[ab]`, and `DONE` ([01](raw/C022/native-01/emuera.log), [02](raw/C022/native-02/emuera.log)). Natural exit was not observed.

PyEmuera `public-01` recorded `BEFORE` in stdout and `E_SYNTAX: Expected EOF, got , at column 2: 7,` at line 12 in stderr; no AFTER or DONE was recorded. Its exit code was 1 ([stdout](raw/C022/public-01/verified.stdout.bin), [stderr](raw/C022/public-01/verified.stderr.bin)). The separate streams have not been merged into a timeline. Variable state after the error was not observed.

## `assignment_syntax:+=` — C023

Case `OPISOLATED265_compound-string-trailing`; input line `LOCALS+="ab",`. [ERB](fixtures/C023/ERB/REVIEW.ERB) · [ERH](fixtures/C023/ERB/REVIEW.ERH) · [config](fixtures/C023/emuera.config).

Native `native-01` and `native-02` each printed `BEFORE`, `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[abab]`, and `DONE` ([01](raw/C023/native-01/emuera.log), [02](raw/C023/native-02/emuera.log)). Natural exit was not observed.

PyEmuera `public-01` recorded `BEFORE` in stdout and `E_SYNTAX: Expected EOF, got , at column 5: "ab",` at line 12 in stderr; no AFTER or DONE was recorded. Its exit code was 1 ([stdout](raw/C023/public-01/verified.stdout.bin), [stderr](raw/C023/public-01/verified.stderr.bin)). Variable state after the error was not observed.

Native logs are UTF-16; Py raw files retain their saved bytes. The two native logs contain identical data, but they do not establish natural termination, GUI equivalence, or behavior for other inputs. Engine binaries are not included. Authorship and redistribution rights for fixture, config, and raw files remain to be checked before publication. [Emuera license](licenses/Emuera1824-v24-license-original.txt) · [related NOTICE](licenses/NOTICE.en.md) · [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt) · [third-party notices](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The original ZIP described in the NOTICE is not included in this bundle.

File paths in the PyEmuera third-party notices refer to the original PyEmuera distribution; they do not imply that every referenced file is included here.
