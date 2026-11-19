# 外部保存記録：追加16ケース

4件の式、8件のPRINT関連テキストログ、4件のエンジン診断を示します。原資料は調査凍結の外にあり、記録済みSHAと照合した外部記録です。

表示は取得済みログに限ります。GUI画面の配置・色や、ログにない出力は主張しません。DONEは出力markerであり自然終了を示しません。停止後状態は未観測です。2件のENCODETOUNIはNative probeの当時SHAを確認できず、実行入力のprobe読戻しは現在のものです。Py configも当時の独立pinを確認できていません。

## C001 — `GETBITBASE01`

**入力条件:** `GETBIT(10,3)`

[ERB](fixtures/C001/MAIN.ERB) · [設定](fixtures/C001/emuera.config)

Native側の入力目録には追加入力の記録がなく、PyEmuera側の実行dirにはCSV・ERHが見つかりませんでした。

### 本家Native

自然終了は確認されていません。

[本家実行ログ](raw/C001/native/emuera.log)

```text
Now Loading...
RESULT=1
DONE
```

### PyEmuera

終了コードは0でした。fixtureの範囲を超える入力操作は推測しません。

[PyEmuera出力ログ](raw/C001/public/output.log)

```text
Now Loading...
RESULT=1
DONE
```

対象範囲: 1つの入力条件です。DONEは出力markerで、自然終了の証明ではありません。

## C002 — `INRANGEBASE01`

**入力条件:** `INRANGE(5,2,8)`

[ERB](fixtures/C002/MAIN.ERB) · [設定](fixtures/C002/emuera.config)

Native側の入力目録には追加入力の記録がなく、PyEmuera側の実行dirにはCSV・ERHが見つかりませんでした。

### 本家Native

自然終了は確認されていません。

[本家実行ログ](raw/C002/native/emuera.log)

```text
Now Loading...
RESULT=1
DONE
```

### PyEmuera

終了コードは0でした。fixtureの範囲を超える入力操作は推測しません。

[PyEmuera出力ログ](raw/C002/public/output.log)

```text
Now Loading...
RESULT=1
DONE
```

対象範囲: 1つの入力条件です。DONEは出力markerで、自然終了の証明ではありません。

## C003 — `LIMITBASE01`

**入力条件:** `LIMIT(14,2,11)`

[ERB](fixtures/C003/MAIN.ERB) · [設定](fixtures/C003/emuera.config)

Native側の入力目録には追加入力の記録がなく、PyEmuera側の実行dirにはCSV・ERHが見つかりませんでした。

### 本家Native

自然終了は確認されていません。

[本家実行ログ](raw/C003/native/emuera.log)

```text
Now Loading...
RESULT=11
DONE
```

### PyEmuera

終了コードは0でした。fixtureの範囲を超える入力操作は推測しません。

[PyEmuera出力ログ](raw/C003/public/output.log)

```text
Now Loading...
RESULT=11
DONE
```

対象範囲: 1つの入力条件です。DONEは出力markerで、自然終了の証明ではありません。

## C004 — `SIGNBASE01`

**入力条件:** `SIGN(-9)`

[ERB](fixtures/C004/MAIN.ERB) · [設定](fixtures/C004/emuera.config)

Native側の入力目録には追加入力の記録がなく、PyEmuera側の実行dirにはCSV・ERHが見つかりませんでした。

### 本家Native

自然終了は確認されていません。

[本家実行ログ](raw/C004/native/emuera.log)

```text
Now Loading...
RESULT=-1
DONE
```

### PyEmuera

終了コードは0でした。fixtureの範囲を超える入力操作は推測しません。

[PyEmuera出力ログ](raw/C004/public/output.log)

```text
Now Loading...
RESULT=-1
DONE
```

対象範囲: 1つの入力条件です。DONEは出力markerで、自然終了の証明ではありません。

## C005 — `PRINTCCASE01`

**入力条件:** `PRINTC PRINTC_RIGHT`

[ERB](fixtures/C005/MAIN.ERB) · [設定](fixtures/C005/emuera.config) · [入力tape](fixtures/C005/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C005/native/emuera.log)

```text
Now Loading...
             PRINTC_RIGHT_END
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C005/public/output_log.bin)

```text
Now Loading...
             PRINTC_RIGHT_END
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C005/public/stdout.bin)

```text
Now Loading...
             PRINTC_RIGHT_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[標準エラー](raw/C005/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C006 — `PRINTFORMCASE01`

**入力条件（fixtureの連続する行の抜粋）:**

```erb
PRINTFORM VALUE={1+2}
PRINTL _END
```

[ERB](fixtures/C006/MAIN.ERB) · [設定](fixtures/C006/emuera.config) · [入力tape](fixtures/C006/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C006/native/emuera.log)

```text
Now Loading...
VALUE=3_END
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C006/public/output_log.bin)

```text
Now Loading...
VALUE=3_END
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C006/public/stdout.bin)

```text
Now Loading...
VALUE=3_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[標準エラー](raw/C006/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C007 — `PRINTFORMLCASE01`

**入力条件:** `PRINTFORML VALUE={1+2}`

[ERB](fixtures/C007/MAIN.ERB) · [設定](fixtures/C007/emuera.config) · [入力tape](fixtures/C007/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C007/native/emuera.log)

```text
Now Loading...
VALUE=3
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C007/public/output_log.bin)

```text
Now Loading...
VALUE=3
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C007/public/stdout.bin)

```text
Now Loading...
VALUE=3
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[標準エラー](raw/C007/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C008 — `PRINTFORMSCASE01`

**入力条件:** `PRINTFORMS "PRINTFORMS_STRING"`

[ERB](fixtures/C008/MAIN.ERB) · [設定](fixtures/C008/emuera.config) · [入力tape](fixtures/C008/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C008/native/emuera.log)

```text
Now Loading...
PRINTFORMS_STRING_END
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C008/public/output_log.bin)

```text
Now Loading...
PRINTFORMS_STRING_END
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C008/public/stdout.bin)

```text
Now Loading...
PRINTFORMS_STRING_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[標準エラー](raw/C008/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C009 — `PRINTFORMSWCASE01`

**入力条件（fixtureの連続する行の抜粋）:**

```erb
PRINTFORMSW "FORM_VALUE={1+2}"
PRINTL AFTER_WAIT
```

[ERB](fixtures/C009/MAIN.ERB) · [設定](fixtures/C009/emuera.config) · [入力tape](fixtures/C009/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C009/native/emuera.log)

```text
Now Loading...
FORM_VALUE=3
0
AFTER_WAIT
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C009/public/output_log.bin)

```text
Now Loading...
FORM_VALUE=3
AFTER_WAIT
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C009/public/stdout.bin)

```text
Now Loading...
FORM_VALUE=3
AFTER_WAIT
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[標準エラー](raw/C009/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C010 — `PRINTFORMWCASE01`

**入力条件（fixtureの連続する行の抜粋）:**

```erb
PRINTFORMW WAIT_LINE={1+2}
PRINTL AFTER_WAIT
OUTPUTLOG
QUIT
```

[ERB](fixtures/C010/MAIN.ERB) · [設定](fixtures/C010/emuera.config) · [入力tape](fixtures/C010/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C010/native/emuera.log)

```text
Now Loading...
WAIT_LINE=3
0
AFTER_WAIT
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C010/public/output_log.bin)

```text
Now Loading...
WAIT_LINE=3
AFTER_WAIT
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C010/public/stdout.bin)

```text
Now Loading...
WAIT_LINE=3
AFTER_WAIT
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[標準エラー](raw/C010/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C011 — `PRINTLCASE01`

**入力条件:** `PRINTL PRINTL_CASE_BETA`

[ERB](fixtures/C011/MAIN.ERB) · [設定](fixtures/C011/emuera.config) · [入力tape](fixtures/C011/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C011/native/emuera.log)

```text
Now Loading...
PRINTL_CASE_BETA
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C011/public/output_log.bin)

```text
Now Loading...
PRINTL_CASE_BETA
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C011/public/stdout.bin)

```text
Now Loading...
PRINTL_CASE_BETA
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[標準エラー](raw/C011/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C012 — `PRINTVLCASE01`

**入力条件:** `PRINTVL 17,"-",29`

[ERB](fixtures/C012/MAIN.ERB) · [設定](fixtures/C012/emuera.config) · [入力tape](fixtures/C012/input.txt)

Native側の入力目録にはERBのみ記録されています。PyEmuera側のERH・CSV・設定は、選択されたreceiptでは確認できません。

probeに記録されたNative側の要求入力（16進）: `30`。対象処理との前後関係は推測しません。

### 本家Native

テキストログのみです。画面cropは含まれず、自然終了は確認されていません。

[本家実行ログ](raw/C012/native/emuera.log)

```text
Now Loading...
17-29
_END
```

### PyEmuera

OUTPUTLOGと標準出力・標準エラーは別々です。PyEmuera側の設定は選択されたreceiptでは確認できません。

[PyEmuera出力ログ](raw/C012/public/output_log.bin)

```text
Now Loading...
17-29
_END
※※※ログファイルをemuera.logに出力しました※※※

```

[標準出力](raw/C012/public/stdout.bin)

```text
Now Loading...
17-29
_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[標準エラー](raw/C012/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

対象範囲: 1つの固定入力です。画面の見た目・全画面配置・Unicode・他の入力や引数形式は確認していません。

## C013 — `ENCODETOUNINEGATIVE01`

**入力条件:** `ENCODETOUNI("A",-1)`

[ERB](fixtures/C013/MAIN.ERB) · [設定](fixtures/C013/emuera.config)

現在のNative probeにはERBのみ記載されています。PyEmuera側の設定・CSV・ERHは、選択されたreceiptでは確認できません。

### 本家Native

エラー画面と自然終了は未観測です。入力・設定の実行前後に関するprobeは現在の読戻しで、当時のSHAは固定されていません。

[本家実行ログ](raw/C013/native/emuera.log)

```text
Now Loading...
ENCODETOUNINEGATIVE01.ERBの2行目でエラーが発生しました:Emuera1824+v24
PRINTFORML RESULT={ENCODETOUNI("A",-1)}
エラー内容：ENCOIDETOUNI関数の第２引数(-1)が負の値です
現在の関数：@SYSTEM_TITLE（ENCODETOUNINEGATIVE01.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera

エラー終了が記録され、エラー後の状態は未観測です。PyEmuera側の設定は独立したpinで固定されていません。

[標準出力](raw/C013/public/stdout.bin)

```text
Now Loading...
```

[標準エラー](raw/C013/public/stderr.bin)

```text
ERB/ENCODETOUNINEGATIVE01.ERB:2: E_INDEX: UTF-16 index outside string
  at @SYSTEM_TITLE ERB/ENCODETOUNINEGATIVE01.ERB:2
```

対象範囲: 指定された不正位置のみです。診断文は異なり、エラー後の状態とNativeのエラー画面は未観測です。

## C014 — `ENCODETOUNIRANGE01`

**入力条件:** `ENCODETOUNI("A",1)`

[ERB](fixtures/C014/MAIN.ERB) · [設定](fixtures/C014/emuera.config)

現在のNative probeにはERBのみ記載されています。PyEmuera側の設定・CSV・ERHは、選択されたreceiptでは確認できません。

### 本家Native

エラー画面と自然終了は未観測です。入力・設定の実行前後に関するprobeは現在の読戻しで、当時のSHAは固定されていません。

[本家実行ログ](raw/C014/native/emuera.log)

```text
Now Loading...
ENCODETOUNIRANGE01.ERBの2行目でエラーが発生しました:Emuera1824+v24
PRINTFORML RESULT={ENCODETOUNI("A",1)}
エラー内容：ENCOIDETOUNI関数の第２引数(1)が第１引数の文字列(A)の文字数を超えています
現在の関数：@SYSTEM_TITLE（ENCODETOUNIRANGE01.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera

エラー終了が記録され、エラー後の状態は未観測です。PyEmuera側の設定は独立したpinで固定されていません。

[標準出力](raw/C014/public/stdout.bin)

```text
Now Loading...
```

[標準エラー](raw/C014/public/stderr.bin)

```text
ERB/ENCODETOUNIRANGE01.ERB:2: E_INDEX: UTF-16 index outside string
  at @SYSTEM_TITLE ERB/ENCODETOUNIRANGE01.ERB:2
```

対象範囲: 指定された不正位置のみです。診断文は異なり、エラー後の状態とNativeのエラー画面は未観測です。

## C015 — `COLORNEGFAULT01`

**入力条件:** `COLOR_FROMRGB(-1,ZZ_FAULT(),0)`

[ERB](fixtures/C015/MAIN.ERB) · [設定](fixtures/C015/emuera.config)

指定された入力記録にCSV・ERHはなく、PyEmuera側の標準入力はDEVNULLです。

### 本家Native 01

自然終了とエラー後の状態は未観測です。

[本家実行ログ](raw/C015/native-01/emuera.log)

```text
Now Loading...
BEFORE
MAIN.ERBの6行目でエラーが発生しました:Emuera1824+v24
A=COLOR_FROMRGB(-1,ZZ_FAULT(),0)
エラー内容：第１引数が0から255の範囲外です
現在の関数：@SYSTEM_TITLE（MAIN.ERBの1行目）
関数呼び出しスタック：
```

### 本家Native 02

自然終了とエラー後の状態は未観測です。

[本家実行ログ](raw/C015/native-02/emuera.log)

```text
Now Loading...
BEFORE
MAIN.ERBの6行目でエラーが発生しました:Emuera1824+v24
A=COLOR_FROMRGB(-1,ZZ_FAULT(),0)
エラー内容：第１引数が0から255の範囲外です
現在の関数：@SYSTEM_TITLE（MAIN.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera

選択されたPyEmuera実行の記録のみです。エラー後の状態は未観測です。

[標準出力](raw/C015/public/stdout.bin)

```text
Now Loading...
BEFORE
FAULT_HELPER_EVAL
```

[標準エラー](raw/C015/public/stderr.bin)

```text
ERB/MAIN.ERB:13: E_ARITH: 0による除算が行なわれました
  at @SYSTEM_TITLE ERB/MAIN.ERB:6
  at @ZZ_FAULT ERB/MAIN.ERB:13
```

対象範囲: 記録されたエラーの優先順とmarkerのみです。自然終了・エラー後状態・一般的な意味での完了は確認していません。

## C016 — `SQRTNEGFAULT01`

**入力条件:** `SQRT(ZZ_NEG())`

[ERB](fixtures/C016/MAIN.ERB) · [設定](fixtures/C016/emuera.config)

指定された入力記録にCSV・ERHはなく、PyEmuera側の標準入力はDEVNULLです。

### 本家Native 01

自然終了とエラー後の状態は未観測です。

[本家実行ログ](raw/C016/native-01/emuera.log)

```text
Now Loading...
BEFORE_SQRT
SQRT_HELPER_EVAL
MAIN.ERBの6行目でエラーが発生しました:Emuera1824+v24
A=SQRT(ZZ_NEG())
エラー内容：SQRT関数の引数に負の値が指定されました
現在の関数：@SYSTEM_TITLE（MAIN.ERBの1行目）
関数呼び出しスタック：
```

### 本家Native 02

自然終了とエラー後の状態は未観測です。

[本家実行ログ](raw/C016/native-02/emuera.log)

```text
Now Loading...
BEFORE_SQRT
SQRT_HELPER_EVAL
MAIN.ERBの6行目でエラーが発生しました:Emuera1824+v24
A=SQRT(ZZ_NEG())
エラー内容：SQRT関数の引数に負の値が指定されました
現在の関数：@SYSTEM_TITLE（MAIN.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera

選択されたPyEmuera実行の記録のみです。エラー後の状態は未観測です。

[標準出力](raw/C016/public/stdout.bin)

```text
Now Loading...
BEFORE_SQRT
SQRT_HELPER_EVAL
```

[標準エラー](raw/C016/public/stderr.bin)

```text
ERB/MAIN.ERB:6: E_ARITH: Math domain/overflow
  at @SYSTEM_TITLE ERB/MAIN.ERB:6
```

対象範囲: 記録されたエラーの優先順とmarkerのみです。自然終了・エラー後状態・一般的な意味での完了は確認していません。
