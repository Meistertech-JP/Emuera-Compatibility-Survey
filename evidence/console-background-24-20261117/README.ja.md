# 背景操作：保存済み24ケース

[English](README.md)

CBG系8対象の式形・命令形について、保存済みの直接16、短絡6、ライフサイクル2の計24ケースを収録しています。[records.json](records.json) にcase・typed role・条件・限定判定と、各fixtureに対応するNative-01・Native-02・public-01の素材への参照を記載しています。24ケースを一つの共有実行と扱わず、同一SHAだけから独立実行や到達を推測しません。

元記録の判定は `different_scoped` が22件、`unverified` が2件です。ライフサイクル2件はpublic側がsetupまたはロードで停止し、CBG本体の比較は成立していません。Nativeの選択行とpublic側のerror codeはケースごとに区別しています。GUI画素、クリック・マウス、背景リスト全体、実際のボタン選択は未観測です。返値だけで表示や操作の成功を示しません。

例えば `UIQUERY236_cbgsetg-expr-direct` は、Nativeの選択ログに `OBS236 V=0 R=701 A=0` と後続行があり、public側stderrには `E_FUNCTION` が記録されています。これはそのケースの限定的な記録であり、CBG全体の互換性判定ではありません。

## 収録物を読む

`records.json` の各 `modes` / `evidence` から、mode固有のERB、設定、rawと派生receiptをたどれます。Nativeの `native-history.bin` はUTF-16（BOM付き）の保存ログ、publicの `public-stdout.bin` と `public-stderr.bin` はそれぞれ別の保存出力です。public出力はCP932で読めます。ERBはUTF-8、`emuera.config` はCP932です。例えば次は最初のcaseのNativeログを表示します。

```powershell
python -c "from pathlib import Path; print(Path('assets/C001/native-01/native-history.bin').read_text(encoding='utf-16'))"
```

例のfixtureは [ERB](assets/C001/native-01/inputs/ERB/SEARCHBOUND01.ERB)、public側は [stdout](assets/C001/public-01/public-stdout.bin) と [stderr](assets/C001/public-01/public-stderr.bin) です。raw・fixture・設定は保存bytesを維持しています。元receiptは個人path・プロセス管理情報等を含むため非同梱で、必要項目のみ選んだ `receipt.json` を同梱しています。派生receiptのcase・modeは保存case／fixtureと元pathの結合であり、原receipt自身のcase IDやmode宣言としません。Native入力SHAはprobeの宣言、public入力SHAはreceiptに記録された前後値です。Nativeのbefore/after一致を推測しません。

Native自然終了は未観測でcleanupとは別です。public stdout・stderrは通常ログやrunnerのstdout/stderrと別素材です。ソースコード、実行体、元receipt全文、完全な親票、その他出力は非同梱です。素材の同一SHAは全条件の互換性、別の実行、発行元の真正性を証明しません。

## 整合性と権利

Python 3.10以上を使用します。信頼できる別経路でmanifestと同梱 `tools/file_set_manifest.py` のSHA-256を確認した後、このディレクトリで実行します。

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

manifestはファイル集合・サイズ・SHAを検査します。実行や発行者の真正性、権利・公開承認は証明しません。[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。NOTICEが説明する原ZIPはこの資料に含みません。調査fixtureや派生記録の権利主体・利用条件は別途確認中です。
