# Operators: saved output for 24 conditions

Each case lists its input condition and the saved output from two Native modes and one PyEmuera mode. These are existing ledger cases, not new executions.

[Inputs, configuration and comparison details](../../evidence/operator-264-20261117/observations.json) · [Usage and notices](../../evidence/operator-264-20261117/README.md)

Do not infer post-error state, natural Native termination, or execution inside an uncalled branch.

## OPISOLATED264_ternary-orphan-uncalled

Input condition: `1#2; uncalled`
Recorded comparison category: `MATCHED_UNCALLED_CONTINUATION_NO_BODY_CREDIT`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE ternary-orphan-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-orphan-uncalled
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/public-01/verified.stdout.bin)):

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

[Standard error](../../evidence/operator-264-20261117/assets/ternary-orphan-uncalled/public-01/verified.stderr.bin)

## OPISOLATED264_ternary-strcond-uncalled

Input condition: `"x"?1#2; uncalled`
Recorded comparison category: `MATCHED_UNCALLED_CONTINUATION_NO_BODY_CREDIT`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE ternary-strcond-uncalled
REVIEW AFTER C=701
REVIEW STATE A=0 B=0
REVIEW STATE D0=6 D1=99
REVIEW STATE S=[ab]
REVIEW DONE ternary-strcond-uncalled
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/public-01/verified.stdout.bin)):

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

[Standard error](../../evidence/operator-264-20261117/assets/ternary-strcond-uncalled/public-01/verified.stderr.bin)

## OPISOLATED264_inc-badindex-pre

Input condition: `F=2 with #DIM D,2; same index guard precedes +/-delta and prefix/postfix correction`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-badindex-pre/native-01/emuera.log)):

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

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-badindex-pre/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-badindex-pre/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-badindex-pre
EVENT INDEX A=1
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:13: E_INDEX: 配列型変数ZZREVDの第１引数(2)は配列の範囲外です
```

[Standard error](../../evidence/operator-264-20261117/assets/inc-badindex-pre/public-01/verified.stderr.bin)

## OPISOLATED264_inc-nonlvalue

Input condition: `C=++(A+1)`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-nonlvalue/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++(A+1)
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-nonlvalue/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-nonlvalue/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-nonlvalue
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[Standard error](../../evidence/operator-264-20261117/assets/inc-nonlvalue/public-01/verified.stderr.bin)

## OPISOLATED264_inc-readonly

Input condition: `C=++ZZCONST`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++ZZCONST
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-readonly/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-readonly
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[Standard error](../../evidence/operator-264-20261117/assets/inc-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_inc-stmt-readonly

Input condition: `++ZZCONST`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
++ZZCONST
エラー内容：代入文の左辺に変更できない変数を指定することはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-readonly
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[Standard error](../../evidence/operator-264-20261117/assets/inc-stmt-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_inc-stmt-tail

Input condition: `++A,1`
Recorded comparison category: `OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-stmt-tail/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE inc-stmt-tail
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
++A,1
エラー内容：代入文の左辺に余分な','があります
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/inc-stmt-tail/native-02/emuera.log)):

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

A normal output trace was not recorded.

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: Expected EOF, got , at column 4: ++A,1
```

[Standard error](../../evidence/operator-264-20261117/assets/inc-stmt-tail/public-01/verified.stderr.bin)

## OPISOLATED264_dec-nonlvalue

Input condition: `C=--(A+1)`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-nonlvalue/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=--(A+1)
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-nonlvalue/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-nonlvalue/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE dec-nonlvalue
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[Standard error](../../evidence/operator-264-20261117/assets/dec-nonlvalue/public-01/verified.stderr.bin)

## OPISOLATED264_dec-readonly

Input condition: `C=--ZZCONST`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=--ZZCONST
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-readonly/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE dec-readonly
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[Standard error](../../evidence/operator-264-20261117/assets/dec-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_dec-stmt-readonly

Input condition: `--ZZCONST`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
--ZZCONST
エラー内容：代入文の左辺に変更できない変数を指定することはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-readonly
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[Standard error](../../evidence/operator-264-20261117/assets/dec-stmt-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_dec-stmt-tail

Input condition: `--A,1`
Recorded comparison category: `OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-stmt-tail/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE dec-stmt-tail
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
--A,1
エラー内容：代入文の左辺に余分な','があります
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/dec-stmt-tail/native-02/emuera.log)):

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

A normal output trace was not recorded.

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: Expected EOF, got , at column 4: --A,1
```

[Standard error](../../evidence/operator-264-20261117/assets/dec-stmt-tail/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-string-type

Input condition: `Mutable string variable passes VariableTerm/IsConst then fails integer dispatch`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-string-type/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-string-type
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++LOCALS
エラー内容：文字列型に単項演算子'++'は適用できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-string-type/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-string-type/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-string-type
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_TYPE: 式の結果が数値ではありません
```

[Standard error](../../evidence/operator-264-20261117/assets/incdec-string-type/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-post-nonlvalue

Input condition: `Postfix has separate ReduceUnaryAfterTerm body: (A+1)++`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-nonlvalue
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=(A+1)++
エラー内容：変数以外をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-post-nonlvalue
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[Standard error](../../evidence/operator-264-20261117/assets/incdec-post-nonlvalue/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-post-readonly

Input condition: `Postfix has separate ReduceUnaryAfterTerm body: ZZCONST++`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-readonly/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-readonly
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=ZZCONST++
エラー内容：変更できない変数をインクリメントすることはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-readonly/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-readonly/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-post-readonly
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_READONLY: ZZCONST is read-only
```

[Standard error](../../evidence/operator-264-20261117/assets/incdec-post-readonly/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-post-string-type

Input condition: `Postfix has separate ReduceUnaryAfterTerm body: LOCALS++`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-string-type/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-post-string-type
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=LOCALS++
エラー内容：文字列型に後置単項演算子'++'は適用できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-string-type/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-post-string-type/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-post-string-type
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_TYPE: 式の結果が数値ではありません
```

[Standard error](../../evidence/operator-264-20261117/assets/incdec-post-string-type/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-pre-and-post

Input condition: `++A++; shared TermStack flags before/after guards`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-pre-and-post
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=++A++
エラー内容：インクリメント・デクリメントを前置・後置両方同時に使うことはできません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-pre-and-post
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_REFERENCE: Increment requires an integer variable
```

[Standard error](../../evidence/operator-264-20261117/assets/incdec-pre-and-post/public-01/verified.stderr.bin)

## OPISOLATED264_incdec-double-post

Input condition: `A++++; shared TermStack flags before/after guards`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-double-post/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE incdec-double-post
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
C=A++++
エラー内容：後置の単項演算子が複数存在しています
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-double-post/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/incdec-double-post/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE incdec-double-post
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: Expected EOF, got ++ at column 4: A++++
```

[Standard error](../../evidence/operator-264-20261117/assets/incdec-double-post/public-01/verified.stderr.bin)

## OPISOLATED264_vector-num-1

Input condition: `2-element vector, start=1; RHS helpers evaluated before sequential write`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/vector-num-1/native-01/emuera.log)):

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

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/vector-num-1/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/vector-num-1/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE vector-num-1
EVENT LEFT A=1 B=1
EVENT RIGHT A=2 B=12
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:14: E_INDEX: 配列変数ZZVの要素数を超えて代入しようとしました
```

[Standard error](../../evidence/operator-264-20261117/assets/vector-num-1/public-01/verified.stderr.bin)

## OPISOLATED264_vector-num-rhs-fails

Input condition: `Second RHS fails before any destination setter call`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/native-01/emuera.log)):

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

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE vector-num-rhs-fails
EVENT RIGHT A=1 B=2
EVENT BAD A=2
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:39: E_ARITH: 0による除算が行なわれました
```

[Standard error](../../evidence/operator-264-20261117/assets/vector-num-rhs-fails/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-control

Input condition: `= RHS '7'; ReduceArguments not a universal comma rule`
Recorded comparison category: `MATCHED_REACHED_EMITTED_STATE`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-control/native-01/emuera.log)):

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

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-control/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-control/public-01/verified.stdout.bin)):

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

[Standard error](../../evidence/operator-264-20261117/assets/plain-num-control/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-trailing

Input condition: `= RHS '7,'; ReduceArguments not a universal comma rule`
Recorded comparison category: `OBSERVED_SCOPED_TIMING_OR_BEHAVIOR_DIFFERENCE`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-trailing/native-01/emuera.log)):

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

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-trailing/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-trailing/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-trailing
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: 式が異常です
```

[Standard error](../../evidence/operator-264-20261117/assets/plain-num-trailing/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-hole

Input condition: `= RHS '7,,7'; ReduceArguments not a universal comma rule`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-hole/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-hole
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = 7,,7
エラー内容：代入式の右辺の値は省略できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-hole/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-hole/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-hole
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: 式が異常です
```

[Standard error](../../evidence/operator-264-20261117/assets/plain-num-hole/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-empty

Input condition: `= RHS ''; ReduceArguments not a universal comma rule`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-empty/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-empty
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = 
エラー内容：代入文の右辺の読み取りに失敗しました
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-empty/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-empty/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-empty
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_SYNTAX: 式が異常です
```

[Standard error](../../evidence/operator-264-20261117/assets/plain-num-empty/public-01/verified.stderr.bin)

## OPISOLATED264_plain-num-wrongtype

Input condition: `= RHS '"ab"'; ReduceArguments not a universal comma rule`
Recorded comparison category: `MATCHED_GUARD_LOCATION_EVENT_SCOPE_DIAGNOSTICS_RETAINED`

### Native native-01

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/native-01/emuera.log)):

```text
Now Loading...
REVIEW BEFORE plain-num-wrongtype
REVIEW.ERBの12行目でエラーが発生しました:Emuera1824+v24
ZZV:0 = "ab"
エラー内容：数値型変数に文字列は代入できません
現在の関数：@SYSTEM_TITLE（REVIEW.ERBの1行目）
関数呼び出しスタック：
```

### Native native-02

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/native-02/emuera.log)):

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

Saved output ([Raw bytes](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/public-01/verified.stdout.bin)):

```text
Now Loading...
REVIEW BEFORE plain-num-wrongtype
```

Recorded diagnostic:

```text
ERB/REVIEW.ERB:12: E_TYPE: Invalid assignment type/readonly destination
```

[Standard error](../../evidence/operator-264-20261117/assets/plain-num-wrongtype/public-01/verified.stderr.bin)

