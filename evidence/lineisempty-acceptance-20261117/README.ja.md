# LINEISEMPTY ボタン状態：保存観測と受入pin

[English](README.md) | [機械可読record](record.json) | [受入票の派生](parent-acceptance-projection.json)

`method_as_command:LINEISEMPTY` の `LINEBUF20261115_button_method` に関する、保存済みcorrected-02のNative 2 mode・public 1 modeのfixture、config、raw、privacy派生receiptを収録する。元の有限範囲受入は `necessary_comparison_complete`／`matched_in_finite_scope`。この資料は元判定を書き換えず、その受入に含まれる他の2 caseのrawを同梱しない。

各modeで完成済み行の後と未確定の非空PRINTBUTTONの後を比較し、選択行はNative 2／public 1とも `EMPTY=1 R1=702 S=SENTINEL`、`BUTTON=0 R1=702 S=SENTINEL`、`DONE`。Native 2本のhistory bytesは一致するが、2つの記録roleは別。public stdout全体の一致や画面描画は主張しない。Native自然終了は未観測で、5秒後のcleanupが記録されている。

元受入票の個別3 pinは、観測文書・レビュー・manifestの現保存SHAと食い違う。元受入のmanifest専用欄は現manifest SHAを指すが、readbackの全参照一致という値は旧pinと矛盾する。3組の値と状態は [record.json](record.json) に記載。保存された訂正履歴は文書更新後に個別pinが残ったという説明を支持するが、旧bytes未発見のため直前版の完全な同一性は証明できない。旧pinは変更しない。

`PRINT_SPACE 0` のNative 0／public 1は別の `expression_function:LINEISEMPTY`、別caseの記録であり、ここでの命令形式に移さない。このbundleに当該別caseのrawはない。HTML・クリック・不正引数・全出力一致・自然終了も対象外。

原受入票とsession原文は非同梱。親判定の存在は記録済み事実の中立投影であり、このbundle単体では原受入票の全文・旧pin元bytesを外部検証できない。実行体も同梱しないため、保存観測を再読できてもエンジンの独立再実行はできない。candidateの参照pathは記録時点の案であり変更され得る。

## 権利・privacy

この資料は公開候補であり、公開承認されていない。fixtureの作者・権利、Emuera由来configとログの再配布範囲、PyEmuera由来出力、派生receipt、同梱ツールの権利とprivacyを独立確認する。機械的に個人path・PID・時刻等を除去したが、レビュー完了を意味しない。権利資料は[ライセンス案内](LICENSES/README.ja.md)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)を参照。実行体・元受入票・sessionは含まない。

この資料のルートディレクトリで全ファイルを検算: `python -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.`。manifestは整合性記録であって、権利承認や元の実測の保証ではない。
