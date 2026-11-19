# 82 typed対象のv24ソース位置補足

[English](README.md)

この独立した補足は、[694対象の静的ソース索引](../native-source-694-static-20261117/README.ja.md)に対し、82 typed対象の同梱v24ソース上の位置を示します。既存索引や対象の判定・実行状況は変更しません。

[`targets.jsonl`](targets.jsonl) は1対象1行で、`FunctionCode` enum宣言49件、代入字句分岐15件、宣言パーサのswitch 11件、変数宣言修飾子のswitch 7件です。各 `locations` は入れ子ZIP内の完全なsource member名、そのファイル全体のSHA-256、1始まりの両端を含む `start_line`–`end_line`、v24上の役割と、識別に用いた `context_lines` を示します。代入の15件には字句分岐と共通の代入行パーサ範囲の2位置があります。共通範囲は、全表記がそこを通ることや前置形式の経路を証明しません。`++` と `+=` のように同じ先頭文字の分岐を使う表記は、補助行の条件で区別します。

対象ソースは別途配布する[v24ソースアーカイブ](../../vendor/emuera/Emuera1824-v24-with-notices.zip)にあります。各行には外側・内側ZIPとsource memberのSHAを記載し、ソース本文はこのレイヤーに含めません。旧アンカーの記録には元ソースの版・ファイルSHA・役割の指定がなく、元ファイルとv24の版およびbytesの同一性は未証明です。ここでの役割はv24の該当箇所から読めたものです。enum宣言は命令登録、handler、method routingを証明しません。これらの静的分岐と位置照合は実行、互換性、出力、受入も証明しません。SHAはbytesを識別するもので、由来や真正性の証明ではありません。

## ファイル集合と権利表示

このディレクトリを `evidence/native-source-anchor82-20261117/` に配置し、共通toolを含む構成で、リポジトリルートから実行する例です。

```powershell
python -B tools/file_set_manifest.py verify `
  --root evidence=evidence/native-source-anchor82-20261117 `
  --manifest evidence/native-source-anchor82-20261117/manifest.json
python -c "import hashlib; print(hashlib.sha256(open('evidence/native-source-anchor82-20261117/manifest.json','rb').read()).hexdigest())"
```

manifestのSHAは別の信頼経路から得たpinと比較してください。manifest自身は集合から除外されます。toolが確認するのはファイル集合の整合性であり、作成者、権利、意味の正しさではありません。原票との対応表とソース調査記録はこのレイヤーには同梱しません。

[共通の権利表示](../../LICENSES/README.ja.md)、[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)を参照してください。参照ソースとこの派生索引の権利は別々に確認する必要があり、この補足自体は公開承認を意味しません。
