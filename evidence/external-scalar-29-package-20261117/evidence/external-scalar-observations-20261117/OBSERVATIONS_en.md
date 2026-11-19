# Historical external records: 29 expression cases

Each row binds a case-specific historical comparison record to its fixture, Native / PyEmuera raw logs and execution records. The originals are outside the 123,679-file frozen survey: their bytes match the SHA recorded at the time and are not represented as frozen survey files.

The table shows the RESULT actually printed in each raw log. Details include the other recorded state lines. ERB, config and applicable CSV are linked. Each case covers one recorded condition, not all arguments, natural process exit, full GUI presentation, or general conformance. DONE is a fixture marker. Complete reproduction of input actions or environment is not established.

| ID | Registered case ID | Expression | Native raw | PyEmuera raw | Input |
|---|---|---|---|---|---|
| C001 | ARRAYMSORTBASE01 | `ARRAYMSORT(SORTKEY,SORTNAME)` | [RESULT=1](raw/C001/native/emuera.log) | [RESULT=1](raw/C001/public/emuera.log) | [ERB](fixtures/C001/MAIN.ERB) |
| C002 | CBRTBASE01 | `CBRT(26)` | [RESULT=2](raw/C002/native/emuera.log) | [RESULT=2](raw/C002/public/emuera.log) | [ERB](fixtures/C002/MAIN.ERB) |
| C003 | COLORNAMEBASE01 | `COLOR_FROMNAME("Red")` | [RESULT=16711680](raw/C003/native/emuera.log) | [RESULT=16711680](raw/C003/public/emuera.log) | [ERB](fixtures/C003/MAIN.ERB) |
| C004 | ENCODETOUNIASCII01 | `ENCODETOUNI("A",0)` | [RESULT=65](raw/C004/native/emuera.log) | [RESULT=65](raw/C004/public/emuera.log) | [ERB](fixtures/C004/MAIN.ERB) |
| C005 | ENCODETOUNIEMPTY01 | `ENCODETOUNI("",0)` | [RESULT=-1](raw/C005/native/emuera.log) | [RESULT=-1](raw/C005/public/emuera.log) | [ERB](fixtures/C005/MAIN.ERB) |
| C006 | ENCODETOUNIKANA01 | `ENCODETOUNI("Aあ",1)` | [RESULT=12354](raw/C006/native/emuera.log) | [RESULT=12354](raw/C006/public/emuera.log) | [ERB](fixtures/C006/MAIN.ERB) |
| C007 | EXPONENTBASE01 | `EXPONENT(3)` | [RESULT=20](raw/C007/native/emuera.log) | [RESULT=20](raw/C007/public/emuera.log) | [ERB](fixtures/C007/MAIN.ERB) |
| C008 | GETCONFIGNUM01 | `GETCONFIG("PRINTCを並べる数")` | [RESULT=3](raw/C008/native/emuera.log) | [RESULT=3](raw/C008/public/emuera.log) | [ERB](fixtures/C008/MAIN.ERB) |
| C009 | GETCONFIGSTR01 | `GETCONFIGS("フォント名")` | [RESULT=ＭＳ ゴシック](raw/C009/native/emuera.log) | [RESULT=ＭＳ ゴシック](raw/C009/public/emuera.log) | [ERB](fixtures/C009/MAIN.ERB) |
| C010 | GETNUMBASE01 | `GETNUM(TALENT,"Alpha")` | [RESULT=0](raw/C010/native/emuera.log) | [RESULT=0](raw/C010/public/emuera.log) | [ERB](fixtures/C010/MAIN.ERB) |
| C011 | GETNUMCASE01 | `GETNUM(TALENT,"alpha")` | [RESULT=1](raw/C011/native/emuera.log) | [RESULT=0](raw/C011/public/emuera.log) | [ERB](fixtures/C011/MAIN.ERB) |
| C012 | INRANGEARRAYBASE01 | `INRANGEARRAY(LOCAL,2,9,0,4)` | [RESULT=3](raw/C012/native/emuera.log) | [RESULT=4](raw/C012/public/emuera.log) | [ERB](fixtures/C012/MAIN.ERB) |
| C013 | LOG10BASE01 | `LOG10(1000)` | [RESULT=3](raw/C013/native/emuera.log) | [RESULT=3](raw/C013/public/emuera.log) | [ERB](fixtures/C013/MAIN.ERB) |
| C014 | LOGBASE01 | `LOG(20)` | [RESULT=2](raw/C014/native/emuera.log) | [RESULT=2](raw/C014/public/emuera.log) | [ERB](fixtures/C014/MAIN.ERB) |
| C015 | MAXBASE01 | `MAX(-3,0,7)` | [RESULT=7](raw/C015/native/emuera.log) | [RESULT=7](raw/C015/public/emuera.log) | [ERB](fixtures/C015/MAIN.ERB) |
| C016 | MINBASE01 | `MIN(-3,0,7)` | [RESULT=-3](raw/C016/native/emuera.log) | [RESULT=-3](raw/C016/public/emuera.log) | [ERB](fixtures/C016/MAIN.ERB) |
| C017 | POWERBASE01 | `POWER(2,3)` | [RESULT=8](raw/C017/native/emuera.log) | [RESULT=8](raw/C017/public/emuera.log) | [ERB](fixtures/C017/MAIN.ERB) |
| C018 | SAVENOSBASE01 | `SAVENOS()` | [RESULT=20](raw/C018/native/emuera.log) | [RESULT=20](raw/C018/public/emuera.log) | [ERB](fixtures/C018/MAIN.ERB) |
| C019 | SQRTBASE01 | `SQRT(15)` | [RESULT=3](raw/C019/native/emuera.log) | [RESULT=3](raw/C019/public/emuera.log) | [ERB](fixtures/C019/MAIN.ERB) |
| C020 | STRFINDBASE01 | `STRFIND("ABABCDE","CD",1)` | [RESULT=4](raw/C020/native/emuera.log) | [RESULT=4](raw/C020/public/emuera.log) | [ERB](fixtures/C020/MAIN.ERB) |
| C021 | STRFINDUBASE01 | `STRFINDU("ABABCDE","CD",1)` | [RESULT=4](raw/C021/native/emuera.log) | [RESULT=4](raw/C021/public/emuera.log) | [ERB](fixtures/C021/MAIN.ERB) |
| C022 | STRLENSUBASE01 | `STRLENSU("AあB")` | [RESULT=3](raw/C022/native/emuera.log) | [RESULT=3](raw/C022/public/emuera.log) | [ERB](fixtures/C022/MAIN.ERB) |
| C023 | SUBSTRINGBASE01 | `SUBSTRING("ABCDE",1,2)` | [RESULT=[BC]](raw/C023/native/emuera.log) | [RESULT=[BC]](raw/C023/public/emuera.log) | [ERB](fixtures/C023/MAIN.ERB) |
| C024 | SUBSTRINGUBASE01 | `SUBSTRINGU("ABCDE",1,2)` | [RESULT=[BC]](raw/C024/native/emuera.log) | [RESULT=[BC]](raw/C024/public/emuera.log) | [ERB](fixtures/C024/MAIN.ERB) |
| C025 | TOHALFBASE01 | `TOHALF("ＡＢＣ１２３")` | [RESULT=[ABC123]](raw/C025/native/emuera.log) | [RESULT=[ABC123]](raw/C025/public/emuera.log) | [ERB](fixtures/C025/MAIN.ERB) |
| C026 | TOINTBASE01 | `TOINT("-123")` | [RESULT=-123](raw/C026/native/emuera.log) | [RESULT=-123](raw/C026/public/emuera.log) | [ERB](fixtures/C026/MAIN.ERB) |
| C027 | TOLOWERBASE01 | `TOLOWER("AbC")` | [RESULT=[abc]](raw/C027/native/emuera.log) | [RESULT=[abc]](raw/C027/public/emuera.log) | [ERB](fixtures/C027/MAIN.ERB) |
| C028 | TOSTRBASE01 | `TOSTR(12345)` | [RESULT=[12345]](raw/C028/native/emuera.log) | [RESULT=[12345]](raw/C028/public/emuera.log) | [ERB](fixtures/C028/MAIN.ERB) |
| C029 | TOUPPERBASE01 | `TOUPPER("AbC")` | [RESULT=[ABC]](raw/C029/native/emuera.log) | [RESULT=[ABC]](raw/C029/public/emuera.log) | [ERB](fixtures/C029/MAIN.ERB) |

## Details / 詳細

### C001 — `ARRAYMSORTBASE01`

[ERB](fixtures/C001/MAIN.ERB) · [config](fixtures/C001/emuera.config)

- Native: `RESULT=1`; `KEYS=1,2,3,0`; `NAMES=a,b,c,z`; `DONE`
- PyEmuera: `RESULT=1`; `KEYS=1,2,3,0`; `NAMES=a,b,c,z`; `DONE`
- Scope: One 4-element numeric and string array pair with zero sentinel; ties, string sort keys, multidimensional arrays, missing sentinel, and failure return paths not covered.

### C002 — `CBRTBASE01`

[ERB](fixtures/C002/MAIN.ERB) · [config](fixtures/C002/emuera.config)

- Native: `RESULT=2`; `DONE`
- PyEmuera: `RESULT=2`; `DONE`
- Scope: Single recorded input.

### C003 — `COLORNAMEBASE01`

[ERB](fixtures/C003/MAIN.ERB) · [config](fixtures/C003/emuera.config)

- Native: `RESULT=16711680`; `DONE`
- PyEmuera: `RESULT=16711680`; `DONE`
- Scope: Single recorded input.

### C004 — `ENCODETOUNIASCII01`

[ERB](fixtures/C004/MAIN.ERB) · [config](fixtures/C004/emuera.config)

- Native: `RESULT=65`; `DONE`
- PyEmuera: `RESULT=65`; `DONE`
- Scope: One ASCII BMP code point at index 0.

### C005 — `ENCODETOUNIEMPTY01`

[ERB](fixtures/C005/MAIN.ERB) · [config](fixtures/C005/emuera.config)

- Native: `RESULT=-1`; `DONE`
- PyEmuera: `RESULT=-1`; `DONE`
- Scope: For the empty string at index 0, both saved mode logs record RESULT=-1. This is the observed value for this input; it does not establish a generally defined sentinel.

### C006 — `ENCODETOUNIKANA01`

[ERB](fixtures/C006/MAIN.ERB) · [config](fixtures/C006/emuera.config)

- Native: `RESULT=12354`; `DONE`
- PyEmuera: `RESULT=12354`; `DONE`
- Scope: One Japanese BMP code point at index 1 in an ASCII-plus-kana string.

### C007 — `EXPONENTBASE01`

[ERB](fixtures/C007/MAIN.ERB) · [config](fixtures/C007/emuera.config)

- Native: `RESULT=20`; `DONE`
- PyEmuera: `RESULT=20`; `DONE`
- Scope: Single recorded input.

### C008 — `GETCONFIGNUM01`

[ERB](fixtures/C008/MAIN.ERB) · [config](fixtures/C008/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- Scope: One configured integer-valued setting.

### C009 — `GETCONFIGSTR01`

[ERB](fixtures/C009/MAIN.ERB) · [config](fixtures/C009/emuera.config)

- Native: `RESULT=ＭＳ ゴシック`; `DONE`
- PyEmuera: `RESULT=ＭＳ ゴシック`; `DONE`
- Scope: One configured string-valued setting.

### C010 — `GETNUMBASE01`

[ERB](fixtures/C010/MAIN.ERB) · [config](fixtures/C010/emuera.config) · [CSV](fixtures/C010/csv/TALENT.CSV)

- Native: `BEFORE=77`; `RESULT=0`; `AFTER=77`; `DONE`
- PyEmuera: `BEFORE=77`; `RESULT=0`; `AFTER=77`; `DONE`
- Scope: One registered TALENT keyword with exact case; does not cover missing or case-folded keys.

### C011 — `GETNUMCASE01`

[ERB](fixtures/C011/MAIN.ERB) · [config](fixtures/C011/emuera.config) · [CSV](fixtures/C011/csv/TALENT.CSV)

- Native: `BEFORE=77`; `RESULT=1`; `AFTER=77`; `DONE`
- PyEmuera: `BEFORE=77`; `RESULT=0`; `AFTER=77`; `DONE`
- Scope: Two case-distinct TALENT names; only lowercase query is compared. Other variable families and duplicate case-folding collisions are not covered.

### C012 — `INRANGEARRAYBASE01`

[ERB](fixtures/C012/MAIN.ERB) · [config](fixtures/C012/emuera.config)

- Native: `RESULT=3`; `VALUES=2,5,8,9`; `DONE`
- PyEmuera: `RESULT=4`; `VALUES=2,5,8,9`; `DONE`
- Scope: One case with a 1D numeric array [2,5,8,9], index range [0,4), and value bounds 2 and 9. The saved raw records Native RESULT=3 and PyEmuera RESULT=4. The interpretation of the Native implementation cited by the original comparison (`Creator.Method.cs:1871-1945`; `VariableEvaluator.cs:489-501`) is to count values >=2 and <9. The saved raw shows the element list and aggregate result, but does not emit per-element inclusion decisions. Saying that PyEmuera counted value 9 is an inference from that result, not a separately observed breakdown. No general boundary rule is established. Errors, omitted bounds, empty or reversed ranges, and other array types are untested.

### C013 — `LOG10BASE01`

[ERB](fixtures/C013/MAIN.ERB) · [config](fixtures/C013/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- Scope: Single recorded input.

### C014 — `LOGBASE01`

[ERB](fixtures/C014/MAIN.ERB) · [config](fixtures/C014/emuera.config)

- Native: `RESULT=2`; `DONE`
- PyEmuera: `RESULT=2`; `DONE`
- Scope: Single recorded input.

### C015 — `MAXBASE01`

[ERB](fixtures/C015/MAIN.ERB) · [config](fixtures/C015/emuera.config)

- Native: `RESULT=7`; `DONE`
- PyEmuera: `RESULT=7`; `DONE`
- Scope: Single recorded input.

### C016 — `MINBASE01`

[ERB](fixtures/C016/MAIN.ERB) · [config](fixtures/C016/emuera.config)

- Native: `RESULT=-3`; `DONE`
- PyEmuera: `RESULT=-3`; `DONE`
- Scope: Single recorded input.

### C017 — `POWERBASE01`

[ERB](fixtures/C017/MAIN.ERB) · [config](fixtures/C017/emuera.config)

- Native: `RESULT=8`; `DONE`
- PyEmuera: `RESULT=8`; `DONE`
- Scope: Single recorded input.

### C018 — `SAVENOSBASE01`

[ERB](fixtures/C018/MAIN.ERB) · [config](fixtures/C018/emuera.config)

- Native: `RESULT=20`; `DONE`
- PyEmuera: `RESULT=20`; `DONE`
- Scope: Single recorded input.

### C019 — `SQRTBASE01`

[ERB](fixtures/C019/MAIN.ERB) · [config](fixtures/C019/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- Scope: Single recorded input.

### C020 — `STRFINDBASE01`

[ERB](fixtures/C020/MAIN.ERB) · [config](fixtures/C020/emuera.config)

- Native: `RESULT=4`; `DONE`
- PyEmuera: `RESULT=4`; `DONE`
- Scope: Single ASCII input under the pinned Japanese config. Language-width and other offset cases not covered.

### C021 — `STRFINDUBASE01`

[ERB](fixtures/C021/MAIN.ERB) · [config](fixtures/C021/emuera.config)

- Native: `RESULT=4`; `DONE`
- PyEmuera: `RESULT=4`; `DONE`
- Scope: One ASCII input with nonzero start; empty and out-of-range needles not covered.

### C022 — `STRLENSUBASE01`

[ERB](fixtures/C022/MAIN.ERB) · [config](fixtures/C022/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- Scope: Single recorded input.

### C023 — `SUBSTRINGBASE01`

[ERB](fixtures/C023/MAIN.ERB) · [config](fixtures/C023/emuera.config)

- Native: `RESULT=[BC]`; `DONE`
- PyEmuera: `RESULT=[BC]`; `DONE`
- Scope: Single ASCII input under the pinned Japanese config. Non-ASCII byte-width and boundary cases not covered.

### C024 — `SUBSTRINGUBASE01`

[ERB](fixtures/C024/MAIN.ERB) · [config](fixtures/C024/emuera.config)

- Native: `RESULT=[BC]`; `DONE`
- PyEmuera: `RESULT=[BC]`; `DONE`
- Scope: One ASCII input; empty/out-of-range and supplementary Unicode cases not covered.

### C025 — `TOHALFBASE01`

[ERB](fixtures/C025/MAIN.ERB) · [config](fixtures/C025/emuera.config)

- Native: `RESULT=[ABC123]`; `DONE`
- PyEmuera: `RESULT=[ABC123]`; `DONE`
- Scope: One full-width ASCII alphanumeric input under Japanese config only.

### C026 — `TOINTBASE01`

[ERB](fixtures/C026/MAIN.ERB) · [config](fixtures/C026/emuera.config)

- Native: `RESULT=-123`; `DONE`
- PyEmuera: `RESULT=-123`; `DONE`
- Scope: Single recorded input.

### C027 — `TOLOWERBASE01`

[ERB](fixtures/C027/MAIN.ERB) · [config](fixtures/C027/emuera.config)

- Native: `RESULT=[abc]`; `DONE`
- PyEmuera: `RESULT=[abc]`; `DONE`
- Scope: ASCII only, avoiding culture-dependent letters.

### C028 — `TOSTRBASE01`

[ERB](fixtures/C028/MAIN.ERB) · [config](fixtures/C028/emuera.config)

- Native: `RESULT=[12345]`; `DONE`
- PyEmuera: `RESULT=[12345]`; `DONE`
- Scope: Default integer formatting only; format strings and culture-sensitive cases are outside scope.

### C029 — `TOUPPERBASE01`

[ERB](fixtures/C029/MAIN.ERB) · [config](fixtures/C029/emuera.config)

- Native: `RESULT=[ABC]`; `DONE`
- PyEmuera: `RESULT=[ABC]`; `DONE`
- Scope: ASCII only, avoiding culture-dependent letters.
