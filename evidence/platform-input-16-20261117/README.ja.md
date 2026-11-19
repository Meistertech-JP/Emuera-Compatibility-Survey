# 入力・画面状態の保存済み16ケース

[English](README.md)

6機能の式・命令形式を合わせた12 typed targetについて、16 fixtureをそれぞれNative 2回、PyEmuera 1回で実行した保存記録です。これは48回のcaseとmodeの組であり、12対象全体の互換性判定ではありません。各caseの対象・条件・選択行・記録上の判定・素材は [records.json](records.json) にあります。

元case台帳の判定は限定一致2件、限定的な利用可否の差7件、未検証7件です。比較資料の `unverified_environment` と台帳の `unverified` は分けて表示しています。MOUSESKIPの2件は起動時の選択状態の比較であり、スキップ操作の確認ではありません。`E_PLATFORM` は実行環境の制約を示し、関数値の不一致や到達の成功を意味しません。Nativeで非アクティブ時に引数評価が短絡した条件は、範囲外入力に対する有効時の動作を証明しません。

キー・マウスの送信や物理操作、アクティブ状態でのキー入力・トグル変化、GUIやフォーカスの同等性は観測していません。MOUSEX/Yの値は保存時の環境に依存します。Nativeの自然終了は5秒後の時点で観測されず、後のcleanupと区別します。

`records.json` のmodeから、保存時のERB・設定・Native履歴またはPyEmuera stdout/stderrを読めます。PyEmuera履歴は元記録に存在し結び付けられた11 modeのみ同梱しています。これらは保存bytesのままです。receiptは実行管理識別子や内部パスを除いた派生記録で、case・modeの対応は保存fixture名と参照元pathによります。Native入力SHAはprobeの宣言、PyEmueraのfixture・configの実行前後SHAは元receiptに記録されていますが、その原欄は非同梱のため、この資料だけでは直接確認できません。実行時の完全な状態や真正性を新たに証明するものではありません。元receipt、実行ファイル、全入力素材、元の完全な台帳・比較資料は同梱していません。

ファイル集合を確認するには、別経路で信頼できるmanifestとツールのSHA-256を確認のうえ、Python 3.10以降で、この資料のルートディレクトリから次を実行します。

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)を参照してください。NOTICEが記す別配布単位の元ZIPは含みません。調査fixture・派生記録・文書の権利主体と利用条件は別途確認中です。
