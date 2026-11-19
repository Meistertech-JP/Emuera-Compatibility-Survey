# PRINTVKW・PRINTVDWの待機解除後

[English](README.md) | [機械可読記録](observations.json)

両命令に数値 `42` を渡し、本家 Emuera 1.824 +v24 と PyEmuera 3.0.0 で、空の Enter による待機解除後を観測しました。本家の画面はEnter前には `42` まで、送信後には `AFTER` と後続の状態を示しました。両エンジンで `A=0`、`RESULT=701`、`RESULTS=SENTINEL` を記録し、それぞれの履歴ログは両側でバイト一致しました。

| 命令 | 入力 | 本家のEnter前 | 本家のEnter後 | 保存ログ |
|---|---|---|---|---|
| PRINTVKW | [ERB](PRINTVKW/fixture.erb) | [画面](PRINTVKW/before.bmp) | [画面](PRINTVKW/after.bmp) | [本家](PRINTVKW/native-history.bin) / [Py](PRINTVKW/py-history.bin) |
| PRINTVDW | [ERB](PRINTVDW/fixture.erb) | [画面](PRINTVDW/before.bmp) | [画面](PRINTVDW/after.bmp) | [本家](PRINTVDW/native-history.bin) / [Py](PRINTVDW/py-history.bin) |

本家は専用デスクトップ内の入力欄へEnterを送信し、PyEmueraは開始時に空行を標準入力に与えました。本家の自然終了は観測せず、観測後に対象プロセスを終了しています。PyEmueraの終了コードはいずれも0です。タイミング・画素や他の引数の一致は確認していません。履歴はBOM付きUTF-16LEです。設定、PyEmueraのstdout/stderrと機械可読記録も各ディレクトリにあります。

`manifest.json` は素材のSHA-256とサイズを記録しています。調査fixture・画像・文書の公開条件は確認中です。
