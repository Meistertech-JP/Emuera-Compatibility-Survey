# 表示状態の式形式・状態変更命令・文字列長命令（179）

以下は原調査が記録した履歴上の結果です。この資料の検証器は各値の期待値照合を実施しません。

10 getterを13状態で呼び、文字列長4命令の非空/空入力も比較（130+8観測）。本家2回と公開pyzログは原バイト一致。全実行DONE到達。

前景Red=16711680、背景Blue=255、既定前景12632256/背景0/フォーカス16776960、bold=1→italic併用3→regular0、既定フォントＭＳ ゴシック、配置LEFT/RIGHT、REDRAW1/0を確認。LINEISEMPTYは前の行が完了した条件で1。式形式のGETCOLOR等とsetterの相互作用の証拠で、GUIの実際の色・字形一致ではない。

STRLEN/STRLENFORMはAあBを4、U形式は3、空引数は全て0。FORM内の文字列ヘルパーは非空で1回、空で0回。

Thirteen sequential display-state stages under one fixed config; valid Red/Blue names, default-font reuse and complete-line state only. No GUI font/color rendering, unsupported fonts, invalid/transparent colors, alternative config, pending-line buffer, resize, asynchronous redraw, or missing/invalid command args. Length commands only AあB/raw FORM with one string helper and empty argument; not combining marks/surrogates/encoding-error coverage. Native alive5s then cleanup; natural exit unobserved.

