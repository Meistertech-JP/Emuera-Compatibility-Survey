# STRFINDU：開始位置の範囲外での保存観測

[English](../en/strfindu-boundary.md)

Emuera 1.824 +v24とPyEmuera 3.0.0の保存記録から、`STRFINDU` の4条件を示します。これは既存記録の読取りであり、新たな実行結果ではありません。

各条件で `RESULT:0=701`、`RESULT:1=702`、`RESULTS="AUTO_SENT"` を設定し、文字列`"AあBA"`に対して次の式を評価しました。最初の引数は `(RESULT:0 == 701 ? "AあBA" # "BAD_SENT")` です。

| case ID | 検索文字列 | 開始位置 | Nativeで記録された戻り値 | PyEmueraで記録された結果 |
|---|---|---:|---:|---|
| `SEARCH02_STRFINDU_A_NEG1` | `"A"` | -1 | -1 | `E_INDEX`で停止 |
| `SEARCH02_STRFINDU_A_5` | `"A"` | 5 | -1 | `E_INDEX`で停止 |
| `SEARCH02_STRFINDU_EMPTY_NEG1` | `""` | -1 | -1 | `E_INDEX`で停止 |
| `SEARCH02_STRFINDU_EMPTY_5` | `""` | 5 | -1 | `E_INDEX`で停止 |

各条件のNativeの選択ログには、戻り値と後続markerがあり、その時点の`RESULT:0=701`、`RESULT:1=702`、`RESULTS="AUTO_SENT"`が記録されています。PyEmueraは `ERB/SEARCHBOUND01.ERB` の9行目で `E_INDEX: STRFINDU start outside string` を記録し、対応する後続markerはありません。停止後の値は未観測です。

記録された単独stageではNativeの2回分とPyEmueraの1回分を参照しています。別のbatch stageの保存記録もありますが、この資料は単独stageとbatch全体の整合性を確立するものではありません。Nativeはcleanupで終了され、自然終了・終了コードは未観測です。これら4条件からSTRFINDU全体の互換性や他の文字列・開始位置を推定しません。

[ケース一覧](../../evidence/case-register-2898-20261117/cases.jsonl)で該当case IDを参照できます。リポジトリのルートから `python -B tools/query.py SEARCH02_STRFINDU_A_NEG1` のように検索すると、そのcaseの投影位置に辿れます。投影では具体的な比較欄の一部が非掲載であり、この文書の表は保存比較票とrawの限定読取りに基づきます。

異なる条件の既存資料として、[STRFINDUBASE01](../../evidence/external-scalar-29-package-20261117/evidence/external-scalar-observations-20261117/OBSERVATIONS_ja.md#c021--strfindubase01)と[空文字・末尾位置の再実行](../../evidence/new-replay-20261116/public/README.ja.md)があります。それぞれ入力と観測時の条件が異なり、上の4ケースの代替ではありません。

この記録には、上記4条件の元fixture、設定、実行ファイル、receipt、比較票、raw出力を同梱していません。これだけで当時の実行を独立に再現・検証することはできません。
