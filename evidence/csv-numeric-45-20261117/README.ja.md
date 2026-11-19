# CSV数値系45ケース：保存済み記録

[English](README.md)

有限範囲のCSV数値系調査から、45ケース・135保存mode（各Native1、Native2、Public1）、12 typed targetと56 target–case roleを選んだ公開候補です。1ケースに複数roleがあっても独立実行や各roleへの到達を意味しません。

## 記録の読み方

- `index.json` の各caseには条件と期待値、元ケース台帳の判定、保存済み読戻しの分類・選択marker比較・停止位置・未観測を、互いに区別して記録しています。期待値や準備時の予測は実観測ではありません。元ケース台帳の判定はmatched 1、different 40、unverified 4です。
- 未検証4件の後にSP条件を分離した修正版4ケースがありますが、別ケースでありこのセットには含みません。元の記録にある147保存modeは、ここに含む135 modeと修正版の12 modeを合わせた歴史上の数であり、135件の成功を意味しません。
- 実行時の `COMPARISON.json` はraw観測のみ・親判定待ちと記録していました。後のcase台帳判定と異なる時点の記録として保持しており、今回、新たな親の受入判断を作っていません。親review原票・判定根拠全文は同梱していません。
- 各modeのrawはNative `emuera.log` またはPublic `stdout.bin`、入力はそのmodeのERB・CSV・configです。各raw、入力の元SHAと同梱bytesのSHAは一致します。configや入力が別modeと同じ条件であるとはSHAだけから推測しません。
- receiptは原文から必要なfieldだけを派生しています。rawのSHA結合は原receiptの `outputs` 宣言ではなく、case台帳の明示参照、群manifest、保存済みraw読戻しに基づくものです。元receiptのSHAと派生receiptのSHAは異なります。原receipt全文、stderr、元実行物、probe全文、元台帳、親reviewは非同梱です。
- Native 90 modeでは `process_exited_after_5s=false`、`exit_code_observed=false`、`cleanup_terminate_ok=true` が記録されており、自然終了は未観測です。Native runnerのreturncode 0、receiptの `completed` や `integrity_ok` は自然終了や比較成功・受入を示しません。Public側の記録されたreturncodeはそのまま保持します。

`expected-bindings.json` と `manifest.json` は選定したcase・mode・assetの結合とファイル集合の検査に使います。元source→派生の非公開対応表は同梱していません。

## 検証

Python 3.10以上。実行前に、別の信頼できる経路から受け取ったmanifestのSHAを外部のハッシュ手段で照合し、そのmanifestに記載された `verify.py` と `tools/file_set_manifest.py` のSHAも照合してください。manifestとbindingsのSHAを指定します。

```powershell
python -B verify.py --manifest-sha256 <manifestのSHA256> --bindings-sha256 <bindingsのSHA256>
```

検証は既存file-set toolと有限なcase/mode/role結合の確認です。pinを同じ配布物だけから取得しても発行者を認証できず、元観測の真正性、実機の再現、全要件の充足、権利・機密の承認を意味しません。

## ライセンス・非同梱

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照。Emuera NOTICEの元source ZIPはここに含まれません。調査fixture・新規文書・派生データの所有と条件は別途確認が必要であり、これらの表示から全体の許諾は導けません。素材の権利・機密は未承認です。
