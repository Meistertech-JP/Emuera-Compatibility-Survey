# 保存済み比較記録：第2まとめ

[English](README.md)

[index.json](index.json) は6資料群の36 typed target・72登録caseを、36 fixture／共有batchと108 mode記録へ結びます。caseが共有fixtureを参照するため、case数は独立実行数ではありません。保存判定は限定一致28・限定差24・未検証20で、対象全体の互換性や新たな受入れを示しません。ほかの2候補群は、索引の `withheld_groups` に記した理由で非同梱です。

各batchの `cases` にtyped role・記録判定・条件、`modes` にfixture・設定・履歴・stdout・stderr・OUTPUTLOGと派生receiptの要点を記載します。同じbytesは `assets/` に一度だけ保存し、case・mode・役割の参照を分けています。`encoding` は各テキスト素材を読むための記録です。原receipt・原比較票・原台帳は非同梱で、receiptの必要事項だけを `receipt_projection` に選択しました。Native probeによる入力SHAの宣言、public receiptに記録された実行前後SHA、実行時の入力SHAが記録されていない場合は別扱いです。

231と235のpublic履歴19素材は保存元で見つからず非同梱です。stdout／stderrとは別であり、対象到達やエラー原因をそれだけから推測しません。全72 Native modeは保存probe上、自然終了を観測せずcleanupと区別しています。

- 202は1本の共有fixtureを使う表示・履歴の比較です。最後の空行条件はエラー後のstateとDONEが未観測です。画面ピクセルの一致は主張しません。
- 231と235は、直接呼出しの差とsetupで止まった正例を分け、public側の対象本体の未到達や未検証を保持します。選択されたメモリ内画像の観測はGUI全体の証明ではありません。
- 194はBAR／BARLの有限条件と設定snapshotです。一致と整数overflow時の限定差、getterの式形式と命令形式を区別します。136は数値命令形式の有限入力・評価順序です。
- 240は8段階を持つ共有fixtureのうち、選定された6 caseを索引化します。Nativeは各待機で対象windowへReturnを送り、publicは起動時に空行8行を入力した記録です。入力タイミングや画面ピクセルを同一と主張しません。UIイベント原記録は非同梱です。

製品実行体、原source ZIP、全入力、画像、元親票本文は含みません。別経路で信頼できるmanifestとtoolのSHA-256を確認したうえで、Python 3.10以降で、この資料のルートディレクトリからファイル集合を検証できます。

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)を参照してください。NOTICEが記す別配布単位の原ZIPは含みません。調査fixture・派生記録・文書の権利主体と利用条件は別途確認中です。
