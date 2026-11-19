# 183ケースの有限範囲の観測記録

[English](README.md)

この配布案は、Emuera1824+v24とPyEmuera 3.0.0の有限範囲の調査から、183ケースの記録を選んだものです。184のtyped target–case role、126の共有batch、377のmode記録と548のcase–mode参照を含みます。case記録にある元判定、個別の観測、未観測と制約を維持しています。全694対象の網羅的な実測、完全互換性、対象roleの到達や個別ケースごとの独立実行を証明するものではありません。

## 記録の読み方

- [`data/cases.jsonl`](data/cases.jsonl) はcase ID、typed role、batchとmodeへの参照、および条件・元判定・観測・未観測を含む記録です。mode中の `observation_pointer` は当該caseの `record` 内を指します。
- [`data/batches.jsonl`](data/batches.jsonl) は共有されたNative1／Public1のreceipt組と関連caseを示します。共有batch内の各caseは別々のプロセス起動を意味しません。Native2が選択されている場合も同じbatchに記録されます。
- [`data/modes.jsonl`](data/modes.jsonl) はmode別のfixture、設定を含む入力、選択rawおよび派生receiptへのパスとSHA-256です。Nativeの選択rawは `emuera.log`、Publicの選択rawはstdoutです。stderrファイル、原receipt全文、その他出力、画像、原票や補助資料は一般に同梱していません。ただしcase記録にはstderr診断の抜粋が含まれる場合があります。
- [`data/references.json`](data/references.json) はcase中の `ref:R...` を解決します。1,499参照のうち820は同梱された派生物を指し、**679は非同梱**です。非同梱は原資料が存在しない、実行されなかった、観測されなかった、のいずれも意味しません。元case中に名前だけ残る資料も、ここに収録済みとは限りません。
- `STRING_METHOD_NEXT_20261116_ISNUMERIC_I64_OVERFLOW` のNative2は別形式のrecovery receiptを参照するため、ここで選択した標準modeには含まれません。Native2自体が未実行・未観測だったと推測しないでください。

helperの終了コード0だけからNativeの自然終了を推定することはできません。該当する4 Native receiptにはその旨の元注記を保持しています。自然終了や到達が不明な場合は、case記録に示された不明・未観測のまま扱ってください。

## SHAと検証の範囲

同梱のraw・fixture・configは元の選択素材と同一bytesで、対応するSHAを記録しています。receiptは必要な項目へ派生した記録で、元receiptのSHAと派生receiptのSHAは異なり得ます。case記録中の元資料の宣言SHAと、`references.json`・`modes.jsonl` の同梱ファイルSHAは、それぞれが指すものを区別してください。元資料・privateの来歴対応表は同梱していません。

[`data/manifest.json`](data/manifest.json) は元の投影内ファイルのSHAを記録します。さらに選定済みのこのディレクトリ全体は [`file-set-manifest.json`](file-set-manifest.json) で検査できます。次は、この配布案をリポジトリの `evidence/observation-adapter-183-20261117/` に配置し、共通ツールを含めた場合の、リポジトリルートからのコマンド案です。

```powershell
python -B tools/file_set_manifest.py verify `
  --root evidence=evidence/observation-adapter-183-20261117 `
  --manifest evidence/observation-adapter-183-20261117/file-set-manifest.json
```

台帳は自分自身を集合から除外します。台帳自体のSHA-256は別の信頼できる経路から取得して比較してください。集合とSHAの一致は選定されたファイルの整合性を示すもので、元実行の真正性、発行者の認証、意味上の十分性や公開許諾を証明しません。

## ライセンスと表示

この案を上記の位置へ配置する場合の共通文書へのリンクです。配布前にリンク先と素材ごとの権利・機密を確認してください。

- [共通の権利表示](../../LICENSES/README.ja.md)、[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)
- [PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[PyEmuera第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)

これらは関連する第三者素材の表示であり、調査fixture、独自文書、派生記録を含む全素材に一括して許諾を与えるものではありません。各素材の所有・利用条件と機密性の確認が必要です。
