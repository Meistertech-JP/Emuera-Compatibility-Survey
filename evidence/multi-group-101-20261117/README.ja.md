# 保存済み比較記録：8資料群

[English](README.md)

[index.json](index.json) は8資料群・65 typed targetに関係する101登録case、63 fixture／共有batch、180 mode記録を整理します。複数caseが同じfixtureやmodeを共有するため、case数は独立実行数ではありません。判定と条件は各caseに記した有限範囲の記録であり、対象全体の互換性や新しい受入れを示しません。

各batchの `cases` は対象role・記録判定・選択条件、`modes` は保存素材と派生receiptの要点を示します。同じbytesは `assets/` に一度だけ保存し、役割・case・modeの参照はそれぞれ保持しています。fixture、設定、CSV、履歴、stdout、stderr、OUTPUTLOG、debug consoleは別の役割です。indexの `encoding` を指定して各素材を読めます。履歴のbytes一致、異なる文字コードを含むテキスト比較、画面表示の一致を混同しません。

元receipt・比較票・原台帳は非同梱です。receiptの必要事項は `receipt_projection` に選択しており、Nativeの入力SHA宣言、public receiptに記録された実行前後SHA、実行時の入力SHAが記録されていない場合を区別します。public履歴のうち14素材は保存元で見つからず非同梱です。stdout/stderrの有無とは別に扱います。同梱素材のSHAや派生receiptは実行時の全状態や真正性を証明しません。

各群の主な制約は次のとおりです。

- 234と233の未検証やsetup前停止を成功に変えず、画面・ピクセル全体の一致は主張しません。233群ではgfillrectangle-method-zero-widthのpublic-01について、元の外側invocation 1件が保存元で見つかりません。保存されたinvocationには再試行を含むため、初回実行すべての完全性は確定しません。
- 154は未作成スプライト名に限る観測、230はsetup／load時に停止した条件を含みます。156は限られた有効範囲の数学入力です。
- 214は3 fixtureと条件ごとのCSVを使用します。196は共有fixture内の選択caseを示し、observable content・layout・rawの各比較軸を分けます。
- 108は `NESTEDSELECT01` の補足 `SELECTNEST01` のみ同梱し、元fixtureと元の画面画像は含みません。外側CASE 2・内側CASE 3の経路で、CASEELSEの選択は未観測です。

Nativeの自然終了は元probeが記録する範囲で区別します。多くのmodeは5秒後も生存し、その後のcleanupを自然終了としていません。108の補足2 modeはcleanup前の終了と終了コードが記録されています。製品実行ファイル、原source ZIP、全入力や親票本文は含みません。

別経路で信頼できるmanifestとツールのSHA-256を確認したうえで、Python 3.10以降で、この資料のルートディレクトリから集合を検証できます。

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)を参照してください。NOTICEが記す別配布単位の原ZIPは含みません。調査fixture・派生記録・文書の権利主体と利用条件は別途確認中です。
