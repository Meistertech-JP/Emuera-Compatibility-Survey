# 外部保存記録：式・関数の29ケース

各行は元case IDを持つ保存比較票、case固有のfixtureとNative / PyEmuera原ログ、および実行記録を結んだものです。元資料は調査凍結123,679件の外側にあり、当時の記録SHAと現物を照合した外部原票です。凍結対象と偽って扱いません。

表は実ログに出力されたRESULTを示します。下の詳細は実際に記録された他の状態行も含みます。fixture・config・必要なCSVにリンクします。各caseは記録された単一条件であり、引数全域、自然終了、全GUI表示、仕様全体の一致は示しません。DONEはfixtureの出力markerです。入力操作や環境の完全な再現は保証しません。

| ID | 公開case ID | 式 | 本家Native raw | PyEmuera raw | 入力 |
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
- 範囲: 0を終端値として含む数値配列・文字列配列各4要素の1条件。キー同値、文字列sort key、多次元配列、終端値なし、失敗時の戻り値は未確認。

### C002 — `CBRTBASE01`

[ERB](fixtures/C002/MAIN.ERB) · [config](fixtures/C002/emuera.config)

- Native: `RESULT=2`; `DONE`
- PyEmuera: `RESULT=2`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C003 — `COLORNAMEBASE01`

[ERB](fixtures/C003/MAIN.ERB) · [config](fixtures/C003/emuera.config)

- Native: `RESULT=16711680`; `DONE`
- PyEmuera: `RESULT=16711680`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C004 — `ENCODETOUNIASCII01`

[ERB](fixtures/C004/MAIN.ERB) · [config](fixtures/C004/emuera.config)

- Native: `RESULT=65`; `DONE`
- PyEmuera: `RESULT=65`; `DONE`
- 範囲: index 0にあるASCIIのBMP文字1文字のみ。

### C005 — `ENCODETOUNIEMPTY01`

[ERB](fixtures/C005/MAIN.ERB) · [config](fixtures/C005/emuera.config)

- Native: `RESULT=-1`; `DONE`
- PyEmuera: `RESULT=-1`; `DONE`
- 範囲: 空文字・index 0の1条件で、保存rawは両modeともRESULT=-1。これはこの入力で観測した値であり、関数一般の定義済みsentinelとは主張しない。

### C006 — `ENCODETOUNIKANA01`

[ERB](fixtures/C006/MAIN.ERB) · [config](fixtures/C006/emuera.config)

- Native: `RESULT=12354`; `DONE`
- PyEmuera: `RESULT=12354`; `DONE`
- 範囲: ASCIIとかなを含む文字列のindex 1にある日本語BMP文字1文字のみ。

### C007 — `EXPONENTBASE01`

[ERB](fixtures/C007/MAIN.ERB) · [config](fixtures/C007/emuera.config)

- Native: `RESULT=20`; `DONE`
- PyEmuera: `RESULT=20`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C008 — `GETCONFIGNUM01`

[ERB](fixtures/C008/MAIN.ERB) · [config](fixtures/C008/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- 範囲: configで設定した整数値の項目1件のみ。

### C009 — `GETCONFIGSTR01`

[ERB](fixtures/C009/MAIN.ERB) · [config](fixtures/C009/emuera.config)

- Native: `RESULT=ＭＳ ゴシック`; `DONE`
- PyEmuera: `RESULT=ＭＳ ゴシック`; `DONE`
- 範囲: configで設定した文字列値の項目1件のみ。

### C010 — `GETNUMBASE01`

[ERB](fixtures/C010/MAIN.ERB) · [config](fixtures/C010/emuera.config) · [CSV](fixtures/C010/csv/TALENT.CSV)

- Native: `BEFORE=77`; `RESULT=0`; `AFTER=77`; `DONE`
- PyEmuera: `BEFORE=77`; `RESULT=0`; `AFTER=77`; `DONE`
- 範囲: 大文字小文字を一致させた登録済みTALENT key 1件のみ。未登録keyや大小文字を変えた検索は未確認。

### C011 — `GETNUMCASE01`

[ERB](fixtures/C011/MAIN.ERB) · [config](fixtures/C011/emuera.config) · [CSV](fixtures/C011/csv/TALENT.CSV)

- Native: `BEFORE=77`; `RESULT=1`; `AFTER=77`; `DONE`
- PyEmuera: `BEFORE=77`; `RESULT=0`; `AFTER=77`; `DONE`
- 範囲: 大小文字だけが異なるTALENT名2件を登録し、小文字queryだけを比較。ほかの変数familyや、大小文字を無視した場合の重複衝突は未確認。

### C012 — `INRANGEARRAYBASE01`

[ERB](fixtures/C012/MAIN.ERB) · [config](fixtures/C012/emuera.config)

- Native: `RESULT=3`; `VALUES=2,5,8,9`; `DONE`
- PyEmuera: `RESULT=4`; `VALUES=2,5,8,9`; `DONE`
- 範囲: 1次元数値配列[2,5,8,9]、添字範囲[0,4)、値境界2・9の1条件。保存rawはNative RESULT=3、PyEmuera RESULT=4を記録する。原比較資料が引用するNative実装根拠（`Creator.Method.cs:1871-1945`、`VariableEvaluator.cs:489-501`）の解釈は2以上9未満。保存rawは要素値列と合計結果を示すが、要素ごとの判定・加算は出力しない。「PyEmueraで値9が数えられた」はこの結果からの推論であり、独立に観測された内訳ではない。一般的な境界規則は確立しない。エラー、省略境界、空・逆範囲、他の配列型は未確認。

### C013 — `LOG10BASE01`

[ERB](fixtures/C013/MAIN.ERB) · [config](fixtures/C013/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C014 — `LOGBASE01`

[ERB](fixtures/C014/MAIN.ERB) · [config](fixtures/C014/emuera.config)

- Native: `RESULT=2`; `DONE`
- PyEmuera: `RESULT=2`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C015 — `MAXBASE01`

[ERB](fixtures/C015/MAIN.ERB) · [config](fixtures/C015/emuera.config)

- Native: `RESULT=7`; `DONE`
- PyEmuera: `RESULT=7`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C016 — `MINBASE01`

[ERB](fixtures/C016/MAIN.ERB) · [config](fixtures/C016/emuera.config)

- Native: `RESULT=-3`; `DONE`
- PyEmuera: `RESULT=-3`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C017 — `POWERBASE01`

[ERB](fixtures/C017/MAIN.ERB) · [config](fixtures/C017/emuera.config)

- Native: `RESULT=8`; `DONE`
- PyEmuera: `RESULT=8`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C018 — `SAVENOSBASE01`

[ERB](fixtures/C018/MAIN.ERB) · [config](fixtures/C018/emuera.config)

- Native: `RESULT=20`; `DONE`
- PyEmuera: `RESULT=20`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C019 — `SQRTBASE01`

[ERB](fixtures/C019/MAIN.ERB) · [config](fixtures/C019/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C020 — `STRFINDBASE01`

[ERB](fixtures/C020/MAIN.ERB) · [config](fixtures/C020/emuera.config)

- Native: `RESULT=4`; `DONE`
- PyEmuera: `RESULT=4`; `DONE`
- 範囲: 固定日本語config下でのASCII入力1件のみ。言語別文字幅やほかのoffsetは未確認。

### C021 — `STRFINDUBASE01`

[ERB](fixtures/C021/MAIN.ERB) · [config](fixtures/C021/emuera.config)

- Native: `RESULT=4`; `DONE`
- PyEmuera: `RESULT=4`; `DONE`
- 範囲: 開始位置が0以外のASCII入力1件のみ。空needleや範囲外needleは未確認。

### C022 — `STRLENSUBASE01`

[ERB](fixtures/C022/MAIN.ERB) · [config](fixtures/C022/emuera.config)

- Native: `RESULT=3`; `DONE`
- PyEmuera: `RESULT=3`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C023 — `SUBSTRINGBASE01`

[ERB](fixtures/C023/MAIN.ERB) · [config](fixtures/C023/emuera.config)

- Native: `RESULT=[BC]`; `DONE`
- PyEmuera: `RESULT=[BC]`; `DONE`
- 範囲: 固定日本語config下でのASCII入力1件のみ。非ASCIIのbyte幅や境界条件は未確認。

### C024 — `SUBSTRINGUBASE01`

[ERB](fixtures/C024/MAIN.ERB) · [config](fixtures/C024/emuera.config)

- Native: `RESULT=[BC]`; `DONE`
- PyEmuera: `RESULT=[BC]`; `DONE`
- 範囲: ASCII入力1件のみ。空文字、範囲外、補助Unicode文字の条件は未確認。

### C025 — `TOHALFBASE01`

[ERB](fixtures/C025/MAIN.ERB) · [config](fixtures/C025/emuera.config)

- Native: `RESULT=[ABC123]`; `DONE`
- PyEmuera: `RESULT=[ABC123]`; `DONE`
- 範囲: 日本語config下で全角の英数字1入力のみ。

### C026 — `TOINTBASE01`

[ERB](fixtures/C026/MAIN.ERB) · [config](fixtures/C026/emuera.config)

- Native: `RESULT=-123`; `DONE`
- PyEmuera: `RESULT=-123`; `DONE`
- 範囲: 記録された1入力のみを対象とし、他の入力条件は未確認。

### C027 — `TOLOWERBASE01`

[ERB](fixtures/C027/MAIN.ERB) · [config](fixtures/C027/emuera.config)

- Native: `RESULT=[abc]`; `DONE`
- PyEmuera: `RESULT=[abc]`; `DONE`
- 範囲: ASCII入力のみ。culture依存の文字は対象外。

### C028 — `TOSTRBASE01`

[ERB](fixtures/C028/MAIN.ERB) · [config](fixtures/C028/emuera.config)

- Native: `RESULT=[12345]`; `DONE`
- PyEmuera: `RESULT=[12345]`; `DONE`
- 範囲: 既定の整数format 1件のみ。format stringやculture依存の条件は対象外。

### C029 — `TOUPPERBASE01`

[ERB](fixtures/C029/MAIN.ERB) · [config](fixtures/C029/emuera.config)

- Native: `RESULT=[ABC]`; `DONE`
- PyEmuera: `RESULT=[ABC]`; `DONE`
- 範囲: ASCII入力のみ。culture依存の文字は対象外。
