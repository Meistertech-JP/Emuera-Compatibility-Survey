# 本家Emueraの保存観測

[English](native-oracle.md) · [観測を開く](native-oracle.html)

条件ごとの入力と、本家Emueraの保存された出力・診断を探せます。PyEmueraとの比較は補助情報です。対象名、case ID、ERB内の文字列、出力で検索できます。本家の保存資料、画像、比較で差のある条件、到達未確認の条件を絞り込めます。

元bytesへのリンクとSHA-256があるcaseに加え、元fixtureとrawが非同梱の選択観測投影があります。表示用のテキストは記録された推定文字コードで復号し、CRLF・CRをLFに変換したものです。元ファイルの改行やbyte列を確認するときは元bytesを開いてください。画像は元の保存画像で、解釈は目視による有限観測です。

保存資料があることと、対象命令への到達が確認されていることは別です。未呼出の制御条件や、引数評価中の補助関数で停止した条件にはそれぞれ限定を表示します。共有batchは同じ出力を共有し、個別の独立実行を意味しません。画面、自然終了、エラー後の状態などは記録にある範囲でのみ扱います。

## 代表検索

- `OPCONT268_strcmp-ge`：共有実行の選択値の限定差異。原fixture・rawは非同梱。

- `CASE001`：ABSのbatch・full-batch・singleを別stageで表示。
- `UIQUERY236_lifecycle-expr`：NativeのSTEP記録と、未確認のPy側比較を区別。
- `ARGBOUND245_empty`：対象命令が返した引数不足の診断。
- `P38`：保存画像と本家診断、比較の差。画像による観測も絞り込み可能。
- `LINEBUF20261115_button_method`：case判定、親受入の投影、3 modeの選択行と旧pinの限定。
- `PRINTKD212_C212_0`：共有batch内の選択行。対象到達を共有ログだけで推測しません。

本索引は選定した有限条件だけを収録し、命令全体の網羅率や互換性の認定ではありません。元recordのcandidate相対パス、JSON pointer、SHA-256は各caseの出典欄に記載しています。既存80行の参照する22 recordと、新たな33行の選択観測recordをこのbundle内に含みます。追加33行の原fixture・config・rawは非同梱です。record内に記された別資料のすべてを同梱するものではありません。


実行前に、別の信頼経路からmanifest・`tools/file_set_manifest.py`・`tools/build_native_oracle.py`それぞれの期待SHA-256を取得し、OSの独立したhash手段で3ファイルを照合してください。上の2引数に信頼済みmanifestと検証器のSHAを渡すと、生成器は選定票・生成器・素材を含むファイル集合を先に検証し、生成結果もmanifestのHTML SHAと一致するときだけ保存します。確認前の選定票削除・参照除去・stage変更も拒否します。pin自体を信頼できない場合、同梱物だけで真正性は確認できません。内容を意図して変更するときは、元record・case・stage・mode・roleを別途確認し、別版として生成・検査・再sealし、独立経路で新しいpinを提供してください。旧pinは自動更新しません。

検索欄では「case ID完全一致」を選べます。通常検索は共有fixtureや出力内の文字列にも一致し、それぞれのcaseが独立に到達したことを意味しません。カードのbundle・stageで別資料を区別します。出典リンクはこの独立bundle内の同梱recordを開きます。

このbundleを `evidence/native-oracle-20261117/` に配置すると、manifestの検証rootはそのディレクトリだけです。bundleを単独コピーしても同じ相対リンクを使用できます。ここには既存80行と別の33条件の選択観測投影、計113行を収録し、別の34/38ケースの収録や網羅性を意味しません。素材へのリンクと元recordへのリンクはbundle内で解決します。元recordに書かれた他の資料への言及は同梱の保証ではありません。

## 再生成

Python 3.10以上で、このツリーのルートから実行します。選定票と収録素材だけを読み、各素材のサイズとSHA-256を確認してHTMLを生成します。エンジンやネットワークは使用しません。

```text
python -I -B tools/build_native_oracle.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

`results/native-oracle-selection.jsonl` は選定時のcase・素材対応で、収録されている元bytesは `evidence/` 等にあります。追加33行の元bytesは非同梱です。選定票とHTMLを再生成できることは、過去の実行や著作権の真正性を証明しません。内容を更新する場合は、caseごとの出典・条件・SHAを確認してから選定票を更新してください。

## ライセンス

[ライセンス一覧](../LICENSES/README.ja.md)、[Emuera原ライセンス](../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](../LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。Emuera NOTICEは原ZIPを含む別の配布単位についての説明で、この索引には原ZIPは含まれません。fixture・派生選定票・新規生成器の権利主体と利用条件は別途確認が必要です。
