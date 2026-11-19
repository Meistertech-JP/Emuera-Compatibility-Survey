# PRINTDATA系の有限観測：61ケース

[English](README.md) · [出典・権利表示](LICENSES/README.ja.md)

この証拠セットは公開前のレビュー対象です。`index.json` は61ケース、32 typed target、288 target-case役割と、61組のnative-01・native-02・public-01保存modeを結びます。元のcase判定・条件・比較・未観測範囲を保持しています。登録されたroleは対象の正常到達、成功、独立実行の証明ではありません。uncalled 13ケースのmain継続も、未呼出body内の正常実行を意味しません。

条件内の `runtime_observation: NOT_RUN` は**準備時点の計画属性**です。保存modeの実施有無を示す欄ではありません。保存済みの観測は各modeのreceiptとrawを参照してください。今回新たにエンジンを実行したことを意味しません。fatal後状態、Native自然終了、W系の保存画像がない範囲などは元のcaseとreceiptの限界を維持します。

Native log、public stdout／stderr、fixture、configは保存時のbytesを維持しています。receiptは元の個人ローカルpathを中立表示に置換し、lease tokenを除外した派生JSONです。入力前後と出力のSHA、mode、終了とcleanupの区別は保持しています。183の前receiptは開始時刻、183の後receiptは開始・終了時刻を保持し、後receiptのうち108件はcleanup後のPID関連情報を保持します。時刻とPIDは当時の記録を照合するための値であり、個人の識別や現在のprocessの証明ではありません。公開前に必要性と公開範囲を別途判断してください。

Nativeログと設定はEmuera1824+v24の参照実装に、public出力はPyEmuera 3.0.0に由来します。調査fixtureは条件別probe、receiptは保存記録からの派生です。原親レビューと独立readback本文、原source ZIP、7z、実行物はこのセットに含みません。出典元が非同梱のため、SHAだけで第三者が原文の真正性や過去の実行を確認することはできません。

[ライセンスとNOTICE](LICENSES/README.ja.md)にEmuera原ライセンス・日英NOTICEとPyEmueraライセンス・第三者表示を同伴しています。Emuera NOTICEの同梱説明は原source ZIPを含む**別の配布単位**についてのもので、この証拠セットにはZIPを含みません。調査fixture・新規文書・派生receiptの権利主体と利用条件は別途未確定であり、これらの表示をセット全体への一括許諾と扱いません。

Python 3.9以降でオフライン検証できます。実行前に、信頼できる別経路から取得したmanifestのSHA-256を外部のハッシュ手段で照合し、manifestに記載された `verify.py` と `tools/file_set_manifest.py` の各SHA-256も同じ方法で照合してください。pinもファイルとは別の信頼できる経路から取得してください。

```text
python -B verify.py --manifest-sha256 <manifest SHA256> --bindings-sha256 <bindings SHA256>
```

検証器はファイル集合・SHAとcase／batch／mode／roleの記録上の結合を確認します。外部pinも含めて両方を差し替えられる場合の真正性、過去の実行、権利・privacyの承認は証明しません。
