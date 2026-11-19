# Assignment observations: 23 isolated fixtures

Each fixture was recorded in Native 01/02 and PyEmuera public 01. These are 23 fixtures and 69 mode records. The typed keys are associations recorded for a shared mechanism; they do not establish that each named operator was executed. Read the actual ERB and ERH.

Native naturally exiting within the observation window was not observed; owned termination is recorded. For stopped execution, post-error cells and side effects are unobserved. A diagnostic before entry does not show that SYSTEM_TITLE or a deeper guard ran. GUI appearance and full semantic closure are not established. stdout and stderr are separate channels.

The alias-warning case reached AFTER/DONE, but exact load-time alias warnings were not retained. Plain string controls do not print the destination cells: DONE does not prove their values. Source references and archive-member hashes are location aids, not proof that a source build produced the executable.

For C017 and C018, both Native modes and PyEmuera each printed `REVIEW STRCELLS [ab],[abab]`. Native C022 printed an AFTER containing `D0=42`, and C023 printed `S=[abab]`; PyEmuera reported a diagnostic before reaching either AFTER.

| ID / fixture | Associated typed keys | Native 01 | Native 02 | PyEmuera stdout / stderr |
|---|---|---|---|---|
| [C001](fixtures/C001/ERB/REVIEW.ERB) | `=`, `==` | [stop](raw/C001/native-01/emuera.log) | [stop](raw/C001/native-02/emuera.log) | [stop](raw/C001/public-01/verified.stdout.bin) / [stderr](raw/C001/public-01/verified.stderr.bin) |
| [C002](fixtures/C002/ERB/REVIEW.ERB) | `'=` | [stop](raw/C002/native-01/emuera.log) | [stop](raw/C002/native-02/emuera.log) | [stop](raw/C002/public-01/verified.stdout.bin) / [stderr](raw/C002/public-01/verified.stderr.bin) |
| [C003](fixtures/C003/ERB/REVIEW.ERB) | `'=` | [stop](raw/C003/native-01/emuera.log) | [stop](raw/C003/native-02/emuera.log) | [stop](raw/C003/public-01/verified.stdout.bin) / [stderr](raw/C003/public-01/verified.stderr.bin) |
| [C004](fixtures/C004/ERB/REVIEW.ERB) | `'=` | [DONE](raw/C004/native-01/emuera.log) | [DONE](raw/C004/native-02/emuera.log) | [DONE](raw/C004/public-01/verified.stdout.bin) / [stderr](raw/C004/public-01/verified.stderr.bin) |
| [C005](fixtures/C005/ERB/REVIEW.ERB) | `'=` | [DONE](raw/C005/native-01/emuera.log) | [DONE](raw/C005/native-02/emuera.log) | [stop](raw/C005/public-01/verified.stdout.bin) / [stderr](raw/C005/public-01/verified.stderr.bin) |
| [C006](fixtures/C006/ERB/REVIEW.ERB) | `'=` | [stop](raw/C006/native-01/emuera.log) | [stop](raw/C006/native-02/emuera.log) | [stop](raw/C006/public-01/verified.stdout.bin) / [stderr](raw/C006/public-01/verified.stderr.bin) |
| [C007](fixtures/C007/ERB/REVIEW.ERB) | `'=` | [stop](raw/C007/native-01/emuera.log) | [stop](raw/C007/native-02/emuera.log) | [stop](raw/C007/public-01/verified.stdout.bin) / [stderr](raw/C007/public-01/verified.stderr.bin) |
| [C008](fixtures/C008/ERB/REVIEW.ERB) | `'=` | [stop](raw/C008/native-01/emuera.log) | [stop](raw/C008/native-02/emuera.log) | [stop](raw/C008/public-01/verified.stdout.bin) / [stderr](raw/C008/public-01/verified.stderr.bin) |
| [C009](fixtures/C009/ERB/REVIEW.ERB) | `'=` | [stop](raw/C009/native-01/emuera.log) | [stop](raw/C009/native-02/emuera.log) | [stop](raw/C009/public-01/verified.stdout.bin) / [stderr](raw/C009/public-01/verified.stderr.bin) |
| [C010](fixtures/C010/ERB/REVIEW.ERB) | `==` | [DONE](raw/C010/native-01/emuera.log) | [DONE](raw/C010/native-02/emuera.log) | [DONE](raw/C010/public-01/verified.stdout.bin) / [stderr](raw/C010/public-01/verified.stderr.bin) |
| [C011](fixtures/C011/ERB/REVIEW.ERB) | `=`, `'=`, `==`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [stop](raw/C011/native-01/emuera.log) | [stop](raw/C011/native-02/emuera.log) | [stop](raw/C011/public-01/verified.stdout.bin) / [stderr](raw/C011/public-01/verified.stderr.bin) |
| [C012](fixtures/C012/ERB/REVIEW.ERB) | `=`, `'=`, `==`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [pre-entry stop](raw/C012/native-01/emuera.log) | [pre-entry stop](raw/C012/native-02/emuera.log) | [pre-entry stop](raw/C012/public-01/verified.stdout.bin) / [stderr](raw/C012/public-01/verified.stderr.bin) |
| [C013](fixtures/C013/ERB/REVIEW.ERB) | `+=`, `-=`, `*=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [stop](raw/C013/native-01/emuera.log) | [stop](raw/C013/native-02/emuera.log) | [stop](raw/C013/public-01/verified.stdout.bin) / [stderr](raw/C013/public-01/verified.stderr.bin) |
| [C014](fixtures/C014/ERB/REVIEW.ERB) | `/=`, `%=` | [stop](raw/C014/native-01/emuera.log) | [stop](raw/C014/native-02/emuera.log) | [stop](raw/C014/public-01/verified.stdout.bin) / [stderr](raw/C014/public-01/verified.stderr.bin) |
| [C015](fixtures/C015/ERB/REVIEW.ERB) | `+=`, `-=`, `++`, `--` | [stop](raw/C015/native-01/emuera.log) | [stop](raw/C015/native-02/emuera.log) | [stop](raw/C015/public-01/verified.stdout.bin) / [stderr](raw/C015/public-01/verified.stderr.bin) |
| [C016](fixtures/C016/ERB/REVIEW.ERB) | `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [stop](raw/C016/native-01/emuera.log) | [stop](raw/C016/native-02/emuera.log) | [stop](raw/C016/public-01/verified.stdout.bin) / [stderr](raw/C016/public-01/verified.stderr.bin) |
| [C017](fixtures/C017/ERB/REVIEW.ERB) | `+=` | [DONE](raw/C017/native-01/emuera.log) | [DONE](raw/C017/native-02/emuera.log) | [DONE](raw/C017/public-01/verified.stdout.bin) / [stderr](raw/C017/public-01/verified.stderr.bin) |
| [C018](fixtures/C018/ERB/REVIEW.ERB) | `*=` | [DONE](raw/C018/native-01/emuera.log) | [DONE](raw/C018/native-02/emuera.log) | [DONE](raw/C018/public-01/verified.stdout.bin) / [stderr](raw/C018/public-01/verified.stderr.bin) |
| [C019](fixtures/C019/ERB/REVIEW.ERB) | `-=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [stop](raw/C019/native-01/emuera.log) | [stop](raw/C019/native-02/emuera.log) | [stop](raw/C019/public-01/verified.stdout.bin) / [stderr](raw/C019/public-01/verified.stderr.bin) |
| [C020](fixtures/C020/ERB/REVIEW.ERB) | `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [stop](raw/C020/native-01/emuera.log) | [stop](raw/C020/native-02/emuera.log) | [stop](raw/C020/public-01/verified.stdout.bin) / [stderr](raw/C020/public-01/verified.stderr.bin) |
| [C021](fixtures/C021/ERB/REVIEW.ERB) | `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [stop](raw/C021/native-01/emuera.log) | [stop](raw/C021/native-02/emuera.log) | [stop](raw/C021/public-01/verified.stdout.bin) / [stderr](raw/C021/public-01/verified.stderr.bin) |
| [C022](fixtures/C022/ERB/REVIEW.ERB) | `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `\|=`, `&=`, `^=` | [DONE](raw/C022/native-01/emuera.log) | [DONE](raw/C022/native-02/emuera.log) | [stop](raw/C022/public-01/verified.stdout.bin) / [stderr](raw/C022/public-01/verified.stderr.bin) |
| [C023](fixtures/C023/ERB/REVIEW.ERB) | `+=`, `*=` | [DONE](raw/C023/native-01/emuera.log) | [DONE](raw/C023/native-02/emuera.log) | [stop](raw/C023/public-01/verified.stdout.bin) / [stderr](raw/C023/public-01/verified.stderr.bin) |

## Recorded markers and output

<a id="c001"></a>
### C001 — `plain-num-badindex`

ERB: [REVIEW.ERB](fixtures/C001/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C001/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C001/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c002"></a>
### C002 — `vector-str-1`

ERB: [REVIEW.ERB](fixtures/C002/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C002/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C002/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT STRRIGHT A=2 B=12`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT STRRIGHT A=2 B=12`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT STRRIGHT A=2 B=12`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c003"></a>
### C003 — `vector-str-rhs-fails`

ERB: [REVIEW.ERB](fixtures/C003/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C003/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C003/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT BAD A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT BAD A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT BAD A=2`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c004"></a>
### C004 — `plain-str-control`

ERB: [REVIEW.ERB](fixtures/C004/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C004/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C004/emuera.config).

- `native-01`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[ab]`.
- `native-02`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[ab]`.
- `public-01`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[ab]`.

<a id="c005"></a>
### C005 — `plain-str-trailing`

ERB: [REVIEW.ERB](fixtures/C005/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C005/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C005/emuera.config).

- `native-01`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[ab]`.
- `native-02`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[ab]`.
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c006"></a>
### C006 — `plain-str-hole`

ERB: [REVIEW.ERB](fixtures/C006/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C006/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C006/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c007"></a>
### C007 — `plain-str-empty`

ERB: [REVIEW.ERB](fixtures/C007/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C007/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C007/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c008"></a>
### C008 — `plain-str-wrongtype`

ERB: [REVIEW.ERB](fixtures/C008/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C008/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C008/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c009"></a>
### C009 — `plain-str-badindex`

ERB: [REVIEW.ERB](fixtures/C009/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C009/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C009/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT STRLEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c010"></a>
### C010 — `assignment-alias-warning`

ERB: [REVIEW.ERB](fixtures/C010/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C010/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C010/emuera.config).

- `native-01`: `REACHED_DONE`; `REVIEW AFTER C=7 A=0 B=0 D0=7 D1=99 S=[alias]`.
- `native-02`: `REACHED_DONE`; `REVIEW AFTER C=7 A=0 B=0 D0=7 D1=99 S=[alias]`.
- `public-01`: `REACHED_DONE`; `REVIEW AFTER C=7 A=0 B=0 D0=7 D1=99 S=[alias]`.

<a id="c011"></a>
### C011 — `assignment-common-const`

ERB: [REVIEW.ERB](fixtures/C011/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C011/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C011/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c012"></a>
### C012 — `assignment-common-nonvar`

ERB: [REVIEW.ERB](fixtures/C012/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C012/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C012/emuera.config).

- `native-01`: `PREENTRY_OR_UNREACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `PREENTRY_OR_UNREACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `PREENTRY_OR_UNREACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c013"></a>
### C013 — `compound-badindex-mul`

ERB: [REVIEW.ERB](fixtures/C013/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C013/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C013/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT INDEX A=1`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT INDEX A=1`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT INDEX A=1`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c014"></a>
### C014 — `compound-badindex-div`

ERB: [REVIEW.ERB](fixtures/C014/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C014/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C014/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT LEFT A=1 B=1`; `EVENT INDEX A=2`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c015"></a>
### C015 — `compound-addconst-badindex`

ERB: [REVIEW.ERB](fixtures/C015/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C015/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C015/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT INDEX A=1`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT INDEX A=1`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT INDEX A=1`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c016"></a>
### C016 — `compound-write-index-fails`

ERB: [REVIEW.ERB](fixtures/C016/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C016/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C016/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT WRITEINDEX A=1`; `EVENT RIGHT A=2 B=2`; `EVENT WRITEINDEX A=3`. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT WRITEINDEX A=1`; `EVENT RIGHT A=2 B=2`; `EVENT WRITEINDEX A=3`. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; `EVENT WRITEINDEX A=1`; `EVENT RIGHT A=2 B=2`; `EVENT WRITEINDEX A=3`. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c017"></a>
### C017 — `compound-string-index-add`

ERB: [REVIEW.ERB](fixtures/C017/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C017/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C017/emuera.config).

- `native-01`: `REACHED_DONE`; `EVENT STRINDEX COUNT=1`; `EVENT STRRIGHT A=1 B=2`; `EVENT STRINDEX COUNT=2`; `REVIEW STRCELLS [ab],[abab]`; `REVIEW AFTER C=701 A=1 B=2 D0=6 D1=99 S=[ab]`.
- `native-02`: `REACHED_DONE`; `EVENT STRINDEX COUNT=1`; `EVENT STRRIGHT A=1 B=2`; `EVENT STRINDEX COUNT=2`; `REVIEW STRCELLS [ab],[abab]`; `REVIEW AFTER C=701 A=1 B=2 D0=6 D1=99 S=[ab]`.
- `public-01`: `REACHED_DONE`; `EVENT STRINDEX COUNT=1`; `EVENT STRRIGHT A=1 B=2`; `EVENT STRINDEX COUNT=2`; `REVIEW STRCELLS [ab],[abab]`; `REVIEW AFTER C=701 A=1 B=2 D0=6 D1=99 S=[ab]`.

<a id="c018"></a>
### C018 — `compound-string-index-mul`

ERB: [REVIEW.ERB](fixtures/C018/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C018/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C018/emuera.config).

- `native-01`: `REACHED_DONE`; `EVENT STRINDEX COUNT=1`; `EVENT RIGHT A=1 B=2`; `EVENT STRINDEX COUNT=2`; `REVIEW STRCELLS [ab],[abab]`; `REVIEW AFTER C=701 A=1 B=2 D0=6 D1=99 S=[ab]`.
- `native-02`: `REACHED_DONE`; `EVENT STRINDEX COUNT=1`; `EVENT RIGHT A=1 B=2`; `EVENT STRINDEX COUNT=2`; `REVIEW STRCELLS [ab],[abab]`; `REVIEW AFTER C=701 A=1 B=2 D0=6 D1=99 S=[ab]`.
- `public-01`: `REACHED_DONE`; `EVENT STRINDEX COUNT=1`; `EVENT RIGHT A=1 B=2`; `EVENT STRINDEX COUNT=2`; `REVIEW STRCELLS [ab],[abab]`; `REVIEW AFTER C=701 A=1 B=2 D0=6 D1=99 S=[ab]`.

<a id="c019"></a>
### C019 — `compound-string-reject`

ERB: [REVIEW.ERB](fixtures/C019/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C019/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C019/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c020"></a>
### C020 — `compound-extra-rhs`

ERB: [REVIEW.ERB](fixtures/C020/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C020/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C020/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c021"></a>
### C021 — `compound-wrong-rhs`

ERB: [REVIEW.ERB](fixtures/C021/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C021/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C021/emuera.config).

- `native-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `native-02`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c022"></a>
### C022 — `compound-trailing-comma`

ERB: [REVIEW.ERB](fixtures/C022/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C022/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C022/emuera.config).

- `native-01`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=42 D1=99 S=[ab]`.
- `native-02`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=42 D1=99 S=[ab]`.
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).

<a id="c023"></a>
### C023 — `compound-string-trailing`

ERB: [REVIEW.ERB](fixtures/C023/ERB/REVIEW.ERB); ERH: [REVIEW.ERH](fixtures/C023/ERB/REVIEW.ERH); config: [emuera.config](fixtures/C023/emuera.config).

- `native-01`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[abab]`.
- `native-02`: `REACHED_DONE`; `REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[abab]`.
- `public-01`: `REACHED_STOP_WITH_DIAGNOSTIC`; no event/AFTER marker. Diagnostic and source line: see raw and [records.json](records.json).
