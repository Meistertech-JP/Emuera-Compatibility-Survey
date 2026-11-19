# 演算子：保存された24条件の出力

各ケースの入力条件と、保存された本家2 mode・PyEmuera 1 modeの出力を示します。既存台帳のケースであり、新しい実行ではありません。

[入力・設定・比較区分の詳細](../../evidence/operator-264-20261117/observations.json)・[資料の使い方と利用条件](../../evidence/operator-264-20261117/README.ja.md)

エラー後の状態、本家の自然終了、未呼出し分岐内の実行は観測されたものとして扱いません。

## OPISOLATED264_ternary-orphan-uncalled

入力条件: `1#2; uncalled`
記録された比較区分: `MATCHED_UNCALLED_CONTINUATION_NO_BODY_CREDIT`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE ternary-orphan-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-orphan-uncalled
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE ternary-orphan-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-orphan-uncalled
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE ternary-orphan-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-orphan-uncalled
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[標準エラー](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/public-01/verified.stderr.bin)

## OPISOLATED264_ternary-strcond-uncalled

入力条件: `"x"?1#2; uncalled`
記録された比較区分: `MATCHED_UNCALLED_CONTINUATION_NO_BODY_CREDIT`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE ternary-strcond-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-strcond-uncalled
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE ternary-strcond-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-strcond-uncalled
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE ternary-strcond-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-strcond-uncalled
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[標準エラー](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/public-01/verified.stderr.bin)

## OPISOLATED264_inc-badindex-pre

入力条件: `F=2 with #DIM D,2; same index guard precedes +/-delta and prefix/postfix correction`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-badindex-pre/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-badindex-pre
EVENT INDEX A=1
REVIEW.ERBの13行目でエラーが発生しました:Emuera1824+v24
C=++ZZREVD:ZZIDX()
エラー内容：配列型変数ZZREVDの第１引数(2)は配列の範囲外です
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-badindex-pre/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-badindex-pre
EVENT INDEX A=1
REVIEW.ERBの13行目でエラーが発生しました:Emuera1824+v24
C=++ZZREVD:ZZIDX()
エラー内容：配列型変数ZZREVDの第１引数(2)は配列の範囲外です
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-badindex-pre/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-badindex-pre
EVENT INDEX A=1
```

記録された診断:

```text
ERB/REVIEW.ERB:13: E_INDEX: 配列型変数ZZREVDの第１引数(2)は配列の範囲外です
```

[標準エラー](../../evidence/operator-264-20261117/assets/inc-badindex-pre/public-01/verified.stderr.bin)

## OPISOLATED264_inc-nonlvalue

入力条件: `C=++(A+1)`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-nonlvalue/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++(A+1)
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-nonlvalue/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++(A+1)
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-nonlvalue/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-nonlvalue
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[標準エラー](../../evidence/operator-264-20261117/assets/inc-nonlvalue/public-01/verified.stderr.bin)

## OPISOLATED264_inc-readonly

入力条件: `C=++ZZCONST`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++ZZCONST
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-readonly/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++ZZCONST
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-readonly
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[標準エラー](../../evidence/operator-264-20261117/assets/inc-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_inc-stmt-readonly

入力条件: `++ZZCONST`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
++ZZCONST
エラー内容：代入文の左辺に変更できない変数を指定することはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
++ZZCONST
エラー内容：代入文の左辺に変更できない変数を指定することはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-readonly
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[標準エラー](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_inc-stmt-tail

入力条件: `++A,1`
記録された比較区分: `OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-stmt-tail/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-tail
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
++A,1
エラー内容：代入文の左辺に余分な','があります
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/inc-stmt-tail/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-tail
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
++A,1
エラー内容：代入文の左辺に余分な','があります
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

通常の出力トレースは記録されていません。

記録された診断:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: Expected EOF, got , at column 4: ++A,1
```

[標準エラー](../../evidence/operator-264-20261117/assets/inc-stmt-tail/public-01/verified.stderr.bin)

## OPISOLATED264_dec-nonlvalue

入力条件: `C=--(A+1)`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-nonlvalue/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=--(A+1)
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-nonlvalue/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=--(A+1)
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-nonlvalue/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE dec-nonlvalue
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[標準エラー](../../evidence/operator-264-20261117/assets/dec-nonlvalue/public-01/verified.stderr.bin)

## OPISOLATED264_dec-readonly

入力条件: `C=--ZZCONST`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=--ZZCONST
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-readonly/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=--ZZCONST
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE dec-readonly
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[標準エラー](../../evidence/operator-264-20261117/assets/dec-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_dec-stmt-readonly

入力条件: `--ZZCONST`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
--ZZCONST
エラー内容：代入文の左辺に変更できない変数を指定することはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
--ZZCONST
エラー内容：代入文の左辺に変更できない変数を指定することはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-readonly
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[標準エラー](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_dec-stmt-tail

入力条件: `--A,1`
記録された比較区分: `OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-stmt-tail/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-tail
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
--A,1
エラー内容：代入文の左辺に余分な','があります
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/dec-stmt-tail/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-tail
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
--A,1
エラー内容：代入文の左辺に余分な','があります
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

通常の出力トレースは記録されていません。

記録された診断:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: Expected EOF, got , at column 4: --A,1
```

[標準エラー](../../evidence/operator-264-20261117/assets/dec-stmt-tail/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-string-type

入力条件: `Mutable string variable passes VariableTerm/IsConst then fails integer dispatch`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-string-type/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-string-type
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++LOCALS
エラー内容：文字列型に単項演算子'++'は適用できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-string-type/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-string-type
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++LOCALS
エラー内容：文字列型に単項演算子'++'は適用できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-string-type/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-string-type
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_TYPE: 式の結果が数値ではありません
```

[標準エラー](../../evidence/operator-264-20261117/assets/incdec-string-type/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-post-nonlvalue

入力条件: `Postfix has separate ReduceUnaryAfterTerm body: (A+1)++`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=(A+1)++
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=(A+1)++
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-post-nonlvalue
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[標準エラー](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-post-readonly

入力条件: `Postfix has separate ReduceUnaryAfterTerm body: ZZCONST++`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=ZZCONST++
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-readonly/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=ZZCONST++
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-post-readonly
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[標準エラー](../../evidence/operator-264-20261117/assets/incdec-post-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-post-string-type

入力条件: `Postfix has separate ReduceUnaryAfterTerm body: LOCALS++`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-string-type/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-string-type
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=LOCALS++
エラー内容：文字列型に後置単項演算子'++'は適用できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-string-type/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-string-type
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=LOCALS++
エラー内容：文字列型に後置単項演算子'++'は適用できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-post-string-type/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-post-string-type
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_TYPE: 式の結果が数値ではありません
```

[標準エラー](../../evidence/operator-264-20261117/assets/incdec-post-string-type/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-pre-and-post

入力条件: `++A++; shared TermStack flags before/after guards`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-pre-and-post
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++A++
エラー内容：インクリメント・デクリメントを前置・後置両方同時に使うことはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-pre-and-post
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++A++
エラー内容：インクリメント・デクリメントを前置・後置両方同時に使うことはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-pre-and-post
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[標準エラー](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-double-post

入力条件: `A++++; shared TermStack flags before/after guards`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-double-post/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-double-post
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=A++++
エラー内容：後置の単項演算子が複数存在しています
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-double-post/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-double-post
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=A++++
エラー内容：後置の単項演算子が複数存在しています
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/incdec-double-post/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-double-post
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: Expected EOF, got ++ at column 4: A++++
```

[標準エラー](../../evidence/operator-264-20261117/assets/incdec-double-post/public-01/verified.stderr.bin)

## OPISOLATED264_vector-num-1

入力条件: `2-element vector, start=1; RHS helpers evaluated before sequential write`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/vector-num-1/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE vector-num-1
EVENT LEFT A=1 B=1
EVENT RIGHT A=2 B=12
REVIEW.ERBの14行目でエラーが発生しました:Emuera1824+v24
ZZV:1 = ZZL(),ZZR()
エラー内容：配列変数ZZVの要素数を超えて代入しようとしました
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/vector-num-1/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE vector-num-1
EVENT LEFT A=1 B=1
EVENT RIGHT A=2 B=12
REVIEW.ERBの14行目でエラーが発生しました:Emuera1824+v24
ZZV:1 = ZZL(),ZZR()
エラー内容：配列変数ZZVの要素数を超えて代入しようとしました
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/vector-num-1/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE vector-num-1
EVENT LEFT A=1 B=1
EVENT RIGHT A=2 B=12
```

記録された診断:

```text
ERB/REVIEW.ERB:14: E_INDEX: 配列変数ZZVの要素数を超えて代入しようとしました
```

[標準エラー](../../evidence/operator-264-20261117/assets/vector-num-1/public-01/verified.stderr.bin)

## OPISOLATED264_vector-num-rhs-fails

入力条件: `Second RHS fails before any destination setter call`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE vector-num-rhs-fails
EVENT RIGHT A=1 B=2
EVENT BAD A=2
REVIEW.ERBの39行目でエラーが発生しました:Emuera1824+v24
RETURNF 1/E
エラー内容：0による除算が行なわれました
現在の関数：@ZZBAD（REVIEW.ERBの35行目）
関数呼び出しスタック：
↑REVIEW.ERBの14行目（関数@SYSTEM_TITLE内）
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE vector-num-rhs-fails
EVENT RIGHT A=1 B=2
EVENT BAD A=2
REVIEW.ERBの39行目でエラーが発生しました:Emuera1824+v24
RETURNF 1/E
エラー内容：0による除算が行なわれました
現在の関数：@ZZBAD（REVIEW.ERBの35行目）
関数呼び出しスタック：
↑REVIEW.ERBの14行目（関数@SYSTEM_TITLE内）
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE vector-num-rhs-fails
EVENT RIGHT A=1 B=2
EVENT BAD A=2
```

記録された診断:

```text
ERB/REVIEW.ERB:39: E_ARITH: 0による除算が行なわれました
```

[標準エラー](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-control

入力条件: `= RHS '7'; ReduceArguments not a universal comma rule`
記録された比較区分: `MATCHED_REACHED_EMITTED_STATE`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-control/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-control
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW VECTOR V0=7 V1=0
REVIEW DONE plain-num-control
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-control/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-control
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW VECTOR V0=7 V1=0
REVIEW DONE plain-num-control
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-control/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-control
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW VECTOR V0=7 V1=0
REVIEW DONE plain-num-control
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[標準エラー](../../evidence/operator-264-20261117/assets/plain-num-control/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-trailing

入力条件: `= RHS '7,'; ReduceArguments not a universal comma rule`
記録された比較区分: `OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-trailing/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-trailing
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW VECTOR V0=7 V1=0
REVIEW DONE plain-num-trailing
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-trailing/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-trailing
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW VECTOR V0=7 V1=0
REVIEW DONE plain-num-trailing
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-trailing/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-trailing
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: 式が異常です
```

[標準エラー](../../evidence/operator-264-20261117/assets/plain-num-trailing/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-hole

入力条件: `= RHS '7,,7'; ReduceArguments not a universal comma rule`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-hole/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-hole
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = 7,,7
エラー内容：代入式の右辺の値は省略できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-hole/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-hole
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = 7,,7
エラー内容：代入式の右辺の値は省略できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-hole/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-hole
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: 式が異常です
```

[標準エラー](../../evidence/operator-264-20261117/assets/plain-num-hole/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-empty

入力条件: `= RHS ''; ReduceArguments not a universal comma rule`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-empty/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-empty
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = 
エラー内容：代入文の右辺の読み取りに失敗しました
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-empty/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-empty
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = 
エラー内容：代入文の右辺の読み取りに失敗しました
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-empty/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-empty
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: 式が異常です
```

[標準エラー](../../evidence/operator-264-20261117/assets/plain-num-empty/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-wrongtype

入力条件: `= RHS '"ab"'; ReduceArguments not a universal comma rule`
記録された比較区分: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### 本家 native-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-wrongtype
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = "ab"
エラー内容：数値型変数に文字列は代入できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### 本家 native-02

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/native-02/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-wrongtype
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = "ab"
エラー内容：数値型変数に文字列は代入できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera public-01

保存された出力 ([原バイト](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-wrongtype
```

記録された診断:

```text
ERB/REVIEW.ERB:12: E_TYPE: Invalid assignment type/readonly destination
```

[標準エラー](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/public-01/verified.stderr.bin)

