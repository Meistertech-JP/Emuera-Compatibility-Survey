# 演算子の保存観測：24条件

[English](README.md)

[観測データ](observations.json)は、三項演算や増減演算などの24条件について、本家Emuera1824+v24の2 modeとPyEmuera 3.0.0の1 modeを記録します。各modeのERB・ERH・設定・保存出力、診断とそのSHA-256にたどれます。各条件のCSVフォルダーは空です。値、イベント、エラー行、停止後の未観測は条件ごとに記録されています。

未呼出し分岐の継続は、内部の式が実行された証明ではありません。エラー後の代入先状態は取得していません。本家の自然終了も未観測です。通常出力のtraceが記録されなかった2 modeは `null` のまま、保存された診断を別に保持しています。有限の観測であり、演算子全体の互換性を意味しません。

本家実行体のSHA-256は `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`、PyEmuera pyzは `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35` です。エンジン本体は同梱しません。

実行前に `verify.py` 自体のSHA-256を信頼できる別経路と照合してください。同じ経路で得たmanifestと `tools/file_set_manifest.py` のSHA-256を指定し、Python 3.10以上で整合を確認します。

```text
python -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

検証は保存ファイルと表示する行の対応を調べます。エンジンの再実行や過去の実行の真正性、素材の利用許諾を証明するものではありません。fixture、設定、画面出力やコードの再利用条件は、配布単位の権利表示を確認してください。

## 入力と検証範囲

各条件の入力を新しい作業フォルダーへ組み直す場合は、空の `ERB/` と `csv/` を作り、対象modeの `assets/<unit-id>/<mode>/ERB_REVIEW.ERB` を `ERB/REVIEW.ERB`、`ERB_REVIEW.ERH` を `ERB/REVIEW.ERH`、`emuera.config` を直下へコピーします。`csv/` は空のままにします。エンジンの取得とGUI実行には、別途その環境と手順が必要です。ハッシュは当時の実行記録の識別子で、同一環境や自然終了の再現を保証しません。

24条件・72 mode記録（Native 48、Py 24）は既存のケース台帳に対応し、新規ケースとして重複加算しません。ここでの検証はエンジンを起動しません。検証器はファイル集合、trace行、イベント・状態行がraw中にあること、診断理由を検査します。判定区分、条件、対象、停止後の状態、自然終了などの意味的正しさを独立して再判定するものではなく、それらは固定されたmanifestと原比較のレビューに依存します。再sealした新しいmanifestのpinを信頼する際は内容を別途点検してください。

## 出典と利用条件

設定・本家出力は [Emueraライセンス原文](LICENSES/Emuera1824-v24-license-original.txt) と [Emueraの表示](vendor/emuera/NOTICE.ja.md)、PyEmueraの出力は [PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt) と [第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md) を参照してください。調査用ERB・ERHや派生データの権利と再利用条件は、エンジンのライセンスから自動的に決まりません。

`case_id` は主台帳の登録ID、`planned_id` は元の条件IDです。登録caseのtarget・条件・判定を原台帳と照合しています。
