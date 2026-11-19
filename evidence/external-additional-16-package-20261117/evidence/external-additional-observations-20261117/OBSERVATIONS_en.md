# Historical external records: 16 additional cases

Four expressions, eight PRINT-related text logs and four engine diagnostics. Originals are outside the frozen survey and are identified by recorded historical hashes.

Only retained log content is presented. Screen layout, color and output absent from the logs are not asserted. DONE is an output marker, not proof of natural exit. Post-error state is unobserved. For two ENCODETOUNI cases the historical hash of the Native probe was not found: its input/config readback is current, and the public config is not independently pinned.

## C001 — `GETBITBASE01`

**Input:** `GETBIT(10,3)`

[ERB](fixtures/C001/MAIN.ERB) · [configuration](fixtures/C001/emuera.config)

The Native input inventory records no extra inputs; no CSV or ERH was found in the PyEmuera run directory.

### Native

Natural exit not established.

[Native log](raw/C001/native/emuera.log)

```text
Now Loading...
RESULT=1
DONE
```

### PyEmuera

Return code 0; input actions beyond fixture are not inferred.

[PyEmuera output log](raw/C001/public/output.log)

```text
Now Loading...
RESULT=1
DONE
```

Scope: One input; DONE is an output marker, not a natural-exit proof.

## C002 — `INRANGEBASE01`

**Input:** `INRANGE(5,2,8)`

[ERB](fixtures/C002/MAIN.ERB) · [configuration](fixtures/C002/emuera.config)

The Native input inventory records no extra inputs; no CSV or ERH was found in the PyEmuera run directory.

### Native

Natural exit not established.

[Native log](raw/C002/native/emuera.log)

```text
Now Loading...
RESULT=1
DONE
```

### PyEmuera

Return code 0; input actions beyond fixture are not inferred.

[PyEmuera output log](raw/C002/public/output.log)

```text
Now Loading...
RESULT=1
DONE
```

Scope: One input; DONE is an output marker, not a natural-exit proof.

## C003 — `LIMITBASE01`

**Input:** `LIMIT(14,2,11)`

[ERB](fixtures/C003/MAIN.ERB) · [configuration](fixtures/C003/emuera.config)

The Native input inventory records no extra inputs; no CSV or ERH was found in the PyEmuera run directory.

### Native

Natural exit not established.

[Native log](raw/C003/native/emuera.log)

```text
Now Loading...
RESULT=11
DONE
```

### PyEmuera

Return code 0; input actions beyond fixture are not inferred.

[PyEmuera output log](raw/C003/public/output.log)

```text
Now Loading...
RESULT=11
DONE
```

Scope: One input; DONE is an output marker, not a natural-exit proof.

## C004 — `SIGNBASE01`

**Input:** `SIGN(-9)`

[ERB](fixtures/C004/MAIN.ERB) · [configuration](fixtures/C004/emuera.config)

The Native input inventory records no extra inputs; no CSV or ERH was found in the PyEmuera run directory.

### Native

Natural exit not established.

[Native log](raw/C004/native/emuera.log)

```text
Now Loading...
RESULT=-1
DONE
```

### PyEmuera

Return code 0; input actions beyond fixture are not inferred.

[PyEmuera output log](raw/C004/public/output.log)

```text
Now Loading...
RESULT=-1
DONE
```

Scope: One input; DONE is an output marker, not a natural-exit proof.

## C005 — `PRINTCCASE01`

**Input:** `PRINTC PRINTC_RIGHT`

[ERB](fixtures/C005/MAIN.ERB) · [configuration](fixtures/C005/emuera.config) · [input tape](fixtures/C005/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C005/native/emuera.log)

```text
Now Loading...
             PRINTC_RIGHT_END
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C005/public/output_log.bin)

```text
Now Loading...
             PRINTC_RIGHT_END
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C005/public/stdout.bin)

```text
Now Loading...
             PRINTC_RIGHT_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[standard error](raw/C005/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C006 — `PRINTFORMCASE01`

**Input (consecutive lines excerpted from the fixture):**

```erb
PRINTFORM VALUE={1+2}
PRINTL _END
```

[ERB](fixtures/C006/MAIN.ERB) · [configuration](fixtures/C006/emuera.config) · [input tape](fixtures/C006/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C006/native/emuera.log)

```text
Now Loading...
VALUE=3_END
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C006/public/output_log.bin)

```text
Now Loading...
VALUE=3_END
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C006/public/stdout.bin)

```text
Now Loading...
VALUE=3_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[standard error](raw/C006/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C007 — `PRINTFORMLCASE01`

**Input:** `PRINTFORML VALUE={1+2}`

[ERB](fixtures/C007/MAIN.ERB) · [configuration](fixtures/C007/emuera.config) · [input tape](fixtures/C007/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C007/native/emuera.log)

```text
Now Loading...
VALUE=3
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C007/public/output_log.bin)

```text
Now Loading...
VALUE=3
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C007/public/stdout.bin)

```text
Now Loading...
VALUE=3
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[standard error](raw/C007/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C008 — `PRINTFORMSCASE01`

**Input:** `PRINTFORMS "PRINTFORMS_STRING"`

[ERB](fixtures/C008/MAIN.ERB) · [configuration](fixtures/C008/emuera.config) · [input tape](fixtures/C008/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C008/native/emuera.log)

```text
Now Loading...
PRINTFORMS_STRING_END
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C008/public/output_log.bin)

```text
Now Loading...
PRINTFORMS_STRING_END
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C008/public/stdout.bin)

```text
Now Loading...
PRINTFORMS_STRING_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[standard error](raw/C008/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C009 — `PRINTFORMSWCASE01`

**Input (consecutive lines excerpted from the fixture):**

```erb
PRINTFORMSW "FORM_VALUE={1+2}"
PRINTL AFTER_WAIT
```

[ERB](fixtures/C009/MAIN.ERB) · [configuration](fixtures/C009/emuera.config) · [input tape](fixtures/C009/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C009/native/emuera.log)

```text
Now Loading...
FORM_VALUE=3
0
AFTER_WAIT
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C009/public/output_log.bin)

```text
Now Loading...
FORM_VALUE=3
AFTER_WAIT
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C009/public/stdout.bin)

```text
Now Loading...
FORM_VALUE=3
AFTER_WAIT
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[standard error](raw/C009/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C010 — `PRINTFORMWCASE01`

**Input (consecutive lines excerpted from the fixture):**

```erb
PRINTFORMW WAIT_LINE={1+2}
PRINTL AFTER_WAIT
OUTPUTLOG
QUIT
```

[ERB](fixtures/C010/MAIN.ERB) · [configuration](fixtures/C010/emuera.config) · [input tape](fixtures/C010/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C010/native/emuera.log)

```text
Now Loading...
WAIT_LINE=3
0
AFTER_WAIT
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C010/public/output_log.bin)

```text
Now Loading...
WAIT_LINE=3
AFTER_WAIT
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C010/public/stdout.bin)

```text
Now Loading...
WAIT_LINE=3
AFTER_WAIT
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
```

[standard error](raw/C010/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C011 — `PRINTLCASE01`

**Input:** `PRINTL PRINTL_CASE_BETA`

[ERB](fixtures/C011/MAIN.ERB) · [configuration](fixtures/C011/emuera.config) · [input tape](fixtures/C011/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C011/native/emuera.log)

```text
Now Loading...
PRINTL_CASE_BETA
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C011/public/output_log.bin)

```text
Now Loading...
PRINTL_CASE_BETA
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C011/public/stdout.bin)

```text
Now Loading...
PRINTL_CASE_BETA
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[standard error](raw/C011/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C012 — `PRINTVLCASE01`

**Input:** `PRINTVL 17,"-",29`

[ERB](fixtures/C012/MAIN.ERB) · [configuration](fixtures/C012/emuera.config) · [input tape](fixtures/C012/input.txt)

The Native input inventory records only the ERB. The selected receipt does not establish the PyEmuera ERH, CSV or configuration.

Requested Native input recorded by the probe (hex): `30`. Its timing relative to the target is not inferred.

### Native

Text log only; crop not included; natural exit not established.

[Native log](raw/C012/native/emuera.log)

```text
Now Loading...
17-29
_END
```

### PyEmuera

OUTPUTLOG and stdout/stderr are distinct; public config not established by selected receipt.

[PyEmuera output log](raw/C012/public/output_log.bin)

```text
Now Loading...
17-29
_END
※※※ログファイルをemuera.logに出力しました※※※

```

[standard output](raw/C012/public/stdout.bin)

```text
Now Loading...
17-29
_END
※ ※ ※ ログファイルをemuera.logに出力しました※ ※ ※ 
0
```

[standard error](raw/C012/public/stderr.bin)

```text
[PyEmuera warning] OUTPUTLOG writes the bounded text history under .pyemuera/logs; review it before sharing.
```

Scope: One fixed input. Screen appearance, full-screen layout, Unicode and other input/argument forms not established.

## C013 — `ENCODETOUNINEGATIVE01`

**Input:** `ENCODETOUNI("A",-1)`

[ERB](fixtures/C013/MAIN.ERB) · [configuration](fixtures/C013/emuera.config)

The current Native probe lists only the ERB. The selected receipt does not establish the PyEmuera configuration, CSV or ERH.

### Native

Error screen and natural exit not observed; exact input/config before/after probe is current readback, historically unpinned.

[Native log](raw/C013/native/emuera.log)

```text
Now Loading...
ENCODETOUNINEGATIVE01.ERBの2行目でエラーが発生しました:Emuera1824+v24
PRINTFORML RESULT={ENCODETOUNI("A",-1)}
エラー内容：ENCOIDETOUNI関数の第２引数(-1)が負の値です
現在の関数：@SYSTEM_TITLE（ENCODETOUNINEGATIVE01.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera

Error return recorded; post-error state unobserved; public config not independently pinned.

[standard output](raw/C013/public/stdout.bin)

```text
Now Loading...
```

[standard error](raw/C013/public/stderr.bin)

```text
ERB/ENCODETOUNINEGATIVE01.ERB:2: E_INDEX: UTF-16 index outside string
  at @SYSTEM_TITLE ERB/ENCODETOUNINEGATIVE01.ERB:2
```

Scope: Only these fixed invalid positions; exact error wording differs; post-error state and Native error screen are unobserved.

## C014 — `ENCODETOUNIRANGE01`

**Input:** `ENCODETOUNI("A",1)`

[ERB](fixtures/C014/MAIN.ERB) · [configuration](fixtures/C014/emuera.config)

The current Native probe lists only the ERB. The selected receipt does not establish the PyEmuera configuration, CSV or ERH.

### Native

Error screen and natural exit not observed; exact input/config before/after probe is current readback, historically unpinned.

[Native log](raw/C014/native/emuera.log)

```text
Now Loading...
ENCODETOUNIRANGE01.ERBの2行目でエラーが発生しました:Emuera1824+v24
PRINTFORML RESULT={ENCODETOUNI("A",1)}
エラー内容：ENCOIDETOUNI関数の第２引数(1)が第１引数の文字列(A)の文字数を超えています
現在の関数：@SYSTEM_TITLE（ENCODETOUNIRANGE01.ERBの1行目）
関数呼び出しスタック：
```

### PyEmuera

Error return recorded; post-error state unobserved; public config not independently pinned.

[standard output](raw/C014/public/stdout.bin)

```text
Now Loading...
```

[standard error](raw/C014/public/stderr.bin)

```text
ERB/ENCODETOUNIRANGE01.ERB:2: E_INDEX: UTF-16 index outside string
  at @SYSTEM_TITLE ERB/ENCODETOUNIRANGE01.ERB:2
```

Scope: Only these fixed invalid positions; exact error wording differs; post-error state and Native error screen are unobserved.

## C015 — `COLORNEGFAULT01`

**Input:** `COLOR_FROMRGB(-1,ZZ_FAULT(),0)`

[ERB](fixtures/C015/MAIN.ERB) · [configuration](fixtures/C015/emuera.config)

The specified input records list no CSV or ERH; PyEmuera standard input was DEVNULL.

### Native 01

Natural exit and post-error state not observed.

[Native log](raw/C015/native-01/emuera.log)

```text
Now Loading...
BEFORE
MAIN.ERBの6行目でエラーが発生しました:Emuera1824+v24
A=COLOR_FROMRGB(-1,ZZ_FAULT(),0)
エラー内容：第１引数が0から255の範囲外です
現在の関数：@SYSTEM_TITLE（MAIN.ERBの1行目）
関数呼び出しスタック：
```

### Native 02

Natural exit and post-error state not observed.

[Native log](raw/C015/native-02/emuera.log)

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

Selected public run only; post-error state not observed.

[standard output](raw/C015/public/stdout.bin)

```text
Now Loading...
BEFORE
FAULT_HELPER_EVAL
```

[standard error](raw/C015/public/stderr.bin)

```text
ERB/MAIN.ERB:13: E_ARITH: 0による除算が行なわれました
  at @SYSTEM_TITLE ERB/MAIN.ERB:6
  at @ZZ_FAULT ERB/MAIN.ERB:13
```

Scope: Only recorded error precedence and markers; no natural exit, post-error state or general closure.

## C016 — `SQRTNEGFAULT01`

**Input:** `SQRT(ZZ_NEG())`

[ERB](fixtures/C016/MAIN.ERB) · [configuration](fixtures/C016/emuera.config)

The specified input records list no CSV or ERH; PyEmuera standard input was DEVNULL.

### Native 01

Natural exit and post-error state not observed.

[Native log](raw/C016/native-01/emuera.log)

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

### Native 02

Natural exit and post-error state not observed.

[Native log](raw/C016/native-02/emuera.log)

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

Selected public run only; post-error state not observed.

[standard output](raw/C016/public/stdout.bin)

```text
Now Loading...
BEFORE_SQRT
SQRT_HELPER_EVAL
```

[standard error](raw/C016/public/stderr.bin)

```text
ERB/MAIN.ERB:6: E_ARITH: Math domain/overflow
  at @SYSTEM_TITLE ERB/MAIN.ERB:6
```

Scope: Only recorded error precedence and markers; no natural exit, post-error state or general closure.
