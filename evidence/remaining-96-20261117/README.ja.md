# 文字列slice・CSV remaining・Unicode：96ケースの保存記録

[English](README.md)

有限範囲の調査から、文字列slice 36、CSV remaining 32、Unicode code-unit 28の計96ケースを選んだ公開候補です。114 typed target–case role、81 batch、243 mode実体、288 case–mode参照を保持します。共有modeがあるため、case数・参照数を独立プロセス数に換算しません。

`index.json` の各caseには元台帳の判定・条件・観測・未観測と、既存のcase別semantic readbackを保持しています。caseごとのroleとbatchの対応を確認し、共有rawを参照したことだけで対象到達、返値、成功、受入を推測しないでください。`references.json` は中立参照の同梱／非同梱を区別します。case記録内の元source宣言SHAと同梱派生receiptのSHAは異なり得ます。

- 文字列sliceの36ケースは108 mode。case別のraw線分、隣接行折返し、helper、値、routing、差異・未観測を区別します。元実行時の親裁定待ちと後続case台帳の判定は別時点の記録です。
- CSV remainingの32ケースは96 mode。各modeのERB、CHARA10、CHARA30、configを個別に保持。Native自然終了は64 modeで未観測。SP offのSP30に関するCSV定義と実runtime観測、fatal後値のUNOBSERVEDを区別します。
- Unicodeの28ケースは84 case–mode参照ですが、13 fixture組・39 receipt／rawを共有します。`ACTUAL_GATE` を共有する6ケースを、6回の独立実行や6対象の返値・後続到達として扱いません。PAIR0／PAIR1／empty-index、CMD／EXPR、index-helper停止、fatal後未観測を各caseのまま保持。D800の数値観測とNative表示・Public escapeは別です。固定regex observerのD800／FFFD単独positive runtime controlは未確認です。

`assets/` のraw・fixture・config・CSVは元bytesを維持。receiptは必要なfieldの派生です。Unicode receiptでは原 `outputs` とrawを照合し、旧slice／CSV receiptに存在しないraw `outputs` は捏造せず、case明示参照と保存済み凍結読戻しによる結合と記録します。Native runnerのreturncodeやcleanupだけでは自然終了を証明しません。stderr、元receipt全文、元実行物、完全な親原票・レビュー、その他出力は非同梱です。

## 検証

Python 3.10以上で実行します。実行前に、別の信頼できる経路から受け取ったmanifestのSHAを外部のハッシュ手段で照合し、そのmanifestに記載された `verify.py` と `tools/file_set_manifest.py` のSHAも照合してください。manifestとbindingsのpinを指定します。

```powershell
python -B verify.py --manifest-sha256 <manifest SHA256> --bindings-sha256 <bindings SHA256>
```

既存のfile-set toolとcase・batch・mode・typed roleの結合を検査します。Unicode共有fixtureのcase条件とroleも照合します。検証は過去の実機実行、自然終了、対象到達、全互換性、元sourceや発行者の真正性、権利・機密の承認を証明しません。

## 権利と表示

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照。NOTICEが説明する元source ZIPは含みません。調査fixture・派生記録・新規文書の所有と利用条件は別途確認が必要であり、全素材への許諾は未確定です。機密・権利は未承認です。
