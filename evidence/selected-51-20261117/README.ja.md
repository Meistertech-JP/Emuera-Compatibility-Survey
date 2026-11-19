# CSV string／flag・CARRAY・array aggregate：51ケースの保存記録

[English](README.md)

有限範囲の保存記録をまとめた公開候補です。CSV string／flag 26、CARRAY 13、array aggregate 12の計51ケース、70 typed target–case role、51 batch、153 modeを保持します。caseの元判定・条件・観測・未観測と限定事項を `index.json` に保存しています。登録roleや保存modeだけから到達・成功・一般的互換性を推測しません。

## 資料と制約

- `assets/` の選択raw・fixture・config・CSV・ERHは、各modeで記録された元bytesのままです。各raw、入力、派生receiptのpath・SHAは `index.json` にあります。Nativeは `emuera.log`、Publicは `stdout.bin` を選択しています。
- CSV string／flagのguard-off 8ケースは専用の元manifestに属し、同群の別manifestに混ぜていません。2種類のconfigを各modeの宣言どおりに保持します。CARRAYのconfigも各mode固有の参照を保持します。
- array aggregateの各modeは `CASE.ERB`、`ARRAYMSORT176.ERH`、`ENDPOINT_READBACK.ERH`、configの4入力を保持し、ERHを別条件のファイルに置換しません。原receipt内の条件ID・modeと各case観測を結合しています。
- CSV／CARRAYの古いreceiptにはcase IDやmode欄がありません。結合はcaseの明示的な原参照・mode別path・該当manifestと保存済みSHA照合に基づき、その根拠を派生receiptに表示します。いずれの原receiptにも存在しないraw `outputs` 宣言を捏造しません。
- helper／runnerのreturncodeやcleanupからNativeの自然終了を推測しません。各caseのfatal後state・到達・親判断の制限をそのまま参照してください。原receipt全文、stderr、原実行物、parent review全文や他の出力は非同梱です。
- `references.json` は元case記録中の中立参照を同梱派生と非同梱に分けます。元source宣言SHAと同梱派生receiptのSHAは異なり得ます。原pathと元／派生の対応表はprivateに保管し、このbundleには含めません。

## 検証

Python 3.10以上。実行前に、別の信頼できる経路から受け取ったmanifestのSHAを外部のハッシュ手段で照合し、そのmanifestに記載された `verify.py` と `tools/file_set_manifest.py` のSHAも照合してください。manifestとbindingsのSHAを指定します。

```powershell
python -B verify.py --manifest-sha256 <manifest SHA256> --bindings-sha256 <bindings SHA256>
```

共通file-set toolとcase・role・mode・入力・raw・receiptの有限結合を確認します。整合性は元実行・自然終了・発行者・互換性・権利を証明しません。

[権利表示](LICENSES/README.ja.md)、[Emueraライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照。NOTICEの元source ZIPは非同梱で、調査fixture・派生物の所有と条件は別途未確定です。機密・権利は未承認です。
