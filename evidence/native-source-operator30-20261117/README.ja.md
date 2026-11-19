# v24ソース位置の補足：演算子29とSET

[English](README.md)

このレイヤーは、[694対象の静的ソース索引](../native-source-694-static-20261117/README.ja.md)で位置が未記録だった30 typed targetに、同梱v24ソース上の限定的な位置を補足します。既存694索引を書き換えず、対象の判定・実行状況・互換性を変更するものではありません。

[`targets.jsonl`](targets.jsonl) は1対象1行、演算子29行と `command_or_syntax:SET` 1行です。`source.archive` はリポジトリルートからの相対path、`inner_archive` と `member` はその中のZIPとソースメンバー、`line` は当該ソースの1始まりの行番号です。対象は共通の[v24ソース配布アーカイブ](../../vendor/emuera/Emuera1824-v24-with-notices.zip)内にあります。

## 演算子とIL対照

29行の位置は `OperatorManager` の記号→`OperatorCode` 辞書登録です。登録箇所であり、その演算の実行分岐や結果を証明しません。既存IL記録にある記号と数値定数を、ソースのenum値と照合した結果を併記しています。`ldstr_il_offset` は**IL内のoffset**であり、C#ソース行ではありません。IL記録はここに同梱しておらず、対照は記号・数値に限ります。IL側バイナリが同梱ソースからbuildされたこと、build同一性、実行・結果一致はいずれも証明しません。

`!|` は辞書では `Nor` に結び付き、IL記録の数値は `Nor` のenum値と一致します。一方、enum宣言のコメントには `!^` とあります。コメントから `!^` が登録済みとは推測しません。

## SET

`SET` の主位置は `FunctionIdentifier.cs` の内部代入識別子の生成行です。補助位置としてenum宣言、`SET_Instruction`、代入構文が内部識別子へ渡されるparser箇所を記録します。これはスクリプトでリテラルの `SET` 命令を呼び出せることや実行結果を示すものではありません。

## ファイル集合と権利表示

このディレクトリを `evidence/native-source-operator30-20261117/` に配置し、共通toolを含む構成でのコマンド例です。

```powershell
python -B tools/file_set_manifest.py verify `
  --root evidence=evidence/native-source-operator30-20261117 `
  --manifest evidence/native-source-operator30-20261117/manifest.json
```

manifest自身は集合から除外されるため、そのSHA-256は別の信頼経路で取得・比較してください。集合SHAはファイルの一致を示しますが、元ソース・IL・発行者の真正性や実行、権利を証明しません。原調査の来歴対応表は配布していません。

[共通の権利表示](../../LICENSES/README.ja.md)、[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)を参照してください。参照ソースの表示と、この補足索引の権利主体・利用条件は別であり、一括許諾や公開承認を意味しません。
