# 数値複合代入の共有記録

[English](README.md)

10種類の数値複合代入 `+= -= *= /= %= <<= >>= |= &= ^=` を含む一つのfixtureについて、Native 2 modeとPyEmuera 2 modeで保存された記録です。[records.json](records.json) は10 typed targetに対応する10登録case、各6条件の計60条件、選択行と4 modeの素材を示します。10 caseは1つの共有batchへの参照であり、10回の独立実行ではありません。

記録された限定判定は10 caseとも `matched_scoped` です。初期値は6・-7・0、右辺は正の2・1で、添字helperの戻り値は常に0です。比較は対象値、対象外の `D:1`、評価回数・順序に限ります。変化する添字、別名参照、文字列代入、桁あふれ、不正な型・添字やゼロ除算時の失敗順序などはこの記録の対象外です。対象全体の互換性を証明するものではありません。

4 modeの保存履歴は元bytesが一致します。PyEmuera stdout/stderrは履歴とは別に保存しています。Nativeの入力SHAはprobeの宣言、2回目のPyEmueraについては原receiptに実行前後SHAの記録がありますが、原receiptとfixture・configの実行前後SHA欄はこの資料に含まれません。初回PyEmueraは保存ファイルのSHAを確認したもので、実行前後の入力SHAは記録されていません。Native自然終了は5秒後に観測されず、後のcleanupとは別です。元receiptは内部pathや管理識別子を含むため非同梱で、同梱receiptは必要な項目を選んだ派生記録です。実行ファイル、全入力、原台帳・原比較票、参照ソース本文は同梱していません。

別経路で信頼できるmanifestとツールのSHA-256を確認したうえで、Python 3.10以降で、この資料のルートディレクトリからファイル集合を検証できます。

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)を参照してください。NOTICEが記す別配布単位の原ZIPは含みません。調査fixture・派生記録・文書の権利主体と利用条件は別途確認中です。
