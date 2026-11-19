# PRINTSとPRINTSL：保存済み観測

[English](README.md)

この単位は選択した2ケースを記録し、それぞれNative-01、Native-02、PyEmuera public-01を別の役割として保持します。fixture、設定、保存raw、receiptの選択項目、比較と受入の抜粋を含みます。実行体は含まず、親受入の全根拠でもありません。親受入が使う過去の境界ケースや他のsource/binary証拠は別にあります。

## 選択した観測

両ケースで、文字列中の2個の連続スペースと選択された改行、helperの順序1→12を記録しました。抑制区間ではhelperの9が実行されず、Bは71、文字列RESULTSは `"KEEP"` のままです。`SKIPDISP` 後のRESULTは0ですが、抑制された呼出し単独による中間値は切り分けていません。

[PRINTS 本家Native-01](cases/PRINTS/native-01/observation/raw.bin) · [PRINTS PyEmuera](cases/PRINTS/public-01/observation/raw.bin) · [PRINTSL 本家Native-01](cases/PRINTSL/native-01/observation/raw.bin) · [PRINTSL PyEmuera](cases/PRINTSL/public-01/observation/raw.bin)。各Native-02、入力、設定、stderrとreceiptは `manifest.json` の各modeから参照できます。

Nativeログと設定はEmuera、public出力と診断文はPyEmueraに関係します。[ライセンス・NOTICEの索引](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。Emuera NOTICEは別のソースZIP用に書かれたもので、この単位にそのZIPは含まれません。調査fixture・派生データ・新規ツールの権利主体と利用条件は確認中であり、掲載したライセンスを自動的に一括適用しません。

保存資料をオフライン検証するには、manifestと検証器のSHA-256を独立した信頼できる配布経路から入手し、このディレクトリでPython 3.9以降を使います。

```text
python -B verify.py --manifest-sha <信頼済みmanifestのSHA256> --verifier-sha <信頼済み検証器のSHA256>
python -B negative_checks.py --manifest-sha <信頼済みmanifestのSHA256> --verifier-sha <信頼済み検証器のSHA256>
```

同梱の `manifest.sha256` は外部pinと一致する必要がありますが、それ自体は独立した信頼源ではありません。検証器はファイル集合、ケース・mode別の参照先と固定役割表を照合します。検証器自身のSHAも独立に確認してください。2回のNative出力が同じbytesの場合、bytesだけからどの実行がどちらを生成したかは証明できず、役割の対応は保存receiptと来歴に基づきます。hashは当時の実行者や配布者の本人確認ではありません。

これは保存観測のオフライン検査で、実機再実行や完全互換の主張ではありません。Nativeの自然終了と終了コードは未観測で、helperのreturncodeと同一視できません。過去のpublic実行体の不明な同一性も不明のままです。`SKIPDISP`自身が `RESULT` を変更するため、抑制された呼出しの中間数値状態は断定しません。Native rawはUTF-16、public rawはCP932です。実機再現には別途、適切に入手した実行体、環境および追加手順が必要です。
