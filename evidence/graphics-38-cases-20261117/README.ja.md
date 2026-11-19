# 画像系38ケースとGCLEAR後続観測

[English](README.md) | [日本語case一覧](CASES_ja.md) | [English case observations](CASES_en.md) | [機械可読記録](cases.json)

元分類の38ケースについて、入力・設定・本家の保存raw 2本とNativeの観測を参照できます。GCLEAR無効色2ケースには、元と同じSHAのfixture・設定を用いた後続Native GUI試行を別記録として示します。元判定はすべて `unverified` のままで、後続の本家診断をPyEmueraとの一致や新たな総合判定へ昇格していません。Pyのrawと元登録簿の全文は含みません。機械記録の元登録簿文は全文の原文引用ではなく、中立的な投影です。

元分類文の診断未観測という記述と、凍結原rawに診断が存在する事実は異なります。原因は不明です。GUI画像は保存された画面を縮小してからcropしたもので、元解像度のpixel証明ではありません。元試行と後続試行の自然終了、および後続のエラー後状態は未観測です。ケースによってはPyEmuera側が準備・読込で停止して対象状態に到達しておらず、範囲は各機械記録を参照してください。選択した座標の値は画面表示や全画素の確認を意味しません。

素材の権利・privacy・公開条件は未確定です。エンジンやPy側の比較証拠は同梱していません。

このディレクトリから、Python 3.10以上で収録ファイルを照合できます。

```text
python -I -B file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

manifestの一致は真正性・公開許可・意味監査ではありません。別の信頼経路によるmanifest SHAが必要です。
