# PRINTVKW・PRINTVDW：空文字と後続項のエラー

[English](README.md) | [機械可読記録](observations.json)

各原fixtureで、空文字を出力する待機命令をEnterで解除し、次の同じ命令の引数を評価します。本家は解除後に `AFTER_EMPTY`、`BEFORE_FAULT`、`FIRST_TERM_SIDE_EFFECT` の順に表示し、7行目の第2項でゼロ除算を診断しました。PyEmueraも同じマーカー順で進み、7行目に `E_ARITH` を出して終了コード1でした。診断形式は異なります。

| case | fixture | 本家Enter前 | 本家Enter後・診断 | Py stdout / stderr |
|---|---|---|---|---|
| PRINTVKWC15 | [ERB](PRINTVKWC15/fixture.erb) | [画面](PRINTVKWC15/native-before.bmp) | [画面](PRINTVKWC15/native-after.bmp) | [stdout](PRINTVKWC15/py-stdout.bin) / [stderr](PRINTVKWC15/py-stderr.bin) |
| PRINTVDWC15 | [ERB](PRINTVDWC15/fixture.erb) | [画面](PRINTVDWC15/native-before.bmp) | [画面](PRINTVDWC15/native-after.bmp) | [stdout](PRINTVDWC15/py-stdout.bin) / [stderr](PRINTVDWC15/py-stderr.bin) |

本家は隔離デスクトップの所有入力欄へ空Enterを送信し、観測後に所有プロセスを終了しました。自然終了は未観測です。PyEmueraには空行を標準入力へ与えました。停止後の変数値、他の入力・引数、画素のエンジン間一致は未確認です。原調査時の未検証判定は当時の記録として維持し、この追加実行を別観測として扱います。

本家の実行履歴はBOM付きUTF-16LEの保存bytesです：[PRINTVKWC15](PRINTVKWC15/native-history.bin)、[PRINTVDWC15](PRINTVDWC15/native-history.bin)。

`manifest.json` は同梱素材のSHA-256とサイズを記録します。素材の公開条件は確認中です。
