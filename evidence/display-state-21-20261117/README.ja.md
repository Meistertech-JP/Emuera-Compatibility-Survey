# 表示状態と文字列長：21対象・3共有modeの記録

[English](README.md)

既存21ケース・21 typed targetを、共通のNative-01、Native-02、公開PyEmuera-01の記録に結びます。元の `matched_scoped` は**履歴上の判定**であり、今回新たに成立を確認した結果ではありません。元群は22ケースで、`DISPLAYCOMMAND179_STRLEN` は今回の21ケースから除外していますが、その2条件は共有fixtureに残ります。roleやmarkerから対象到達や21回の独立実行を推測しません。

`cases.jsonl` は記録条件と制約を保持し、`bindings.json` はcase ID・typed target・対応方法・marker一覧および選定外caseを固定します。138 markerは13段階×10 getterと4種類の文字列長命令×2条件です。ケースとmarkerの参照216件は重複を含み、実行回数ではありません。

オフライン検証器は別pinのbindings、ファイル集合、markerの順序・ラベル、fixture構造と共有modeの記録を確認します。**138個の観測値と期待値の独立照合は行いません。** [source-review.ja.md](source-review.ja.md)には元調査が記録した期待値・結果の一部がありますが、検証器がその成立を確認するものではありません。対象到達、完全互換性、権利も証明しません。3 modeの値を同じように変えて新manifestを信頼すると構造検証は通り得ます。信頼済みの元pinはbundle bytesの変更を検出します。

fixture・config・選択rawはmodeごとに保持します。元receipt全文と元review全文は非同梱です。Native 2 modeは5秒後生存、その後の終了処理成功が記録され、自然終了と終了コードは未観測です。`DONE`はログmarkerで、自然終了の証明ではありません。公開側wrapperのreturncode 0もNative終了を意味しません。GUIの実際の色・字形、無効色、別設定、resize、非同期redrawなどは元記録の対象外です。

## オフライン検証

3種類のSHA-256 pinは別の信頼経路から入手してください。同じbundle内のmanifestやbindingsだけを信頼の根拠にはできません。このディレクトリで実行します。

```powershell
python -B verify.py --manifest-sha256 <信頼済みmanifest SHA> --bindings-sha256 <信頼済みbindings SHA> --tool-sha256 <信頼済みtool SHA>
```

検証器は同梱した共通 `tools/file_set_manifest.py` のpinと別pinの `bindings.json` を確認します。真正性のためには検証器自体も別途信頼する必要があります。bindingsとそのpinの両方を第三者が差し替えた場合、この検査だけで元対応の真正性は分かりません。

## 権利表示

[ライセンス索引](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[PyEmuera第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。Emuera NOTICEは別配布のsource ZIPを説明しており、そのZIPはこの資料に含みません。fixture、config、raw観測、条件票、比較票、元review、派生物それぞれの権利・機密・配布条件は別途確認中で、公開承認されていません。
