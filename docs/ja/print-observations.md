# 本家EmueraのPRINT系：保存観測の例

[English](../en/print-observations.md)

以下は、同じfixtureを使った共有batch `PRINTKD212_SHARED` の保存履歴から選んだ条件例です。条件ごとに独立実行した結果ではありません。Native 01・02の保存履歴は同じSHA-256で、各例の該当byte範囲を両方で照合しています。

出力中の `P>` と `<T` はfixtureが対象命令の前後に印字する目印です。以下の `\r\n` は保存履歴の改行を示します。[入力ERB][fixture]（CP932）、[設定][config]、[Native 01履歴][n1]、[Native 02履歴][n2]、[条件とbyte範囲の索引][index]を参照できます。履歴はUTF-16 LEのBOM付きで、byte範囲は先頭からの位置・終端を含まない値です。

## 1. FORCEKANAとPRINTVK

入力 `PRINTVK ZZ212N(1),"/",ZZ212S(2)` の条件で、各 `FORCEKANA` 値に対応する保存履歴は次のとおりです。`ZZ212S(2)` は `あアｱ` を返すfixture内の関数です。

| 条件 | fixtureの命令行 | 目印を含む出力行 | 履歴のbyte範囲 |
|---|---:|---|---:|
| `C212_0`: 0 | 10 | `P>1/あアｱ<T` | `[62, 168)` |
| `C212_1`: 1 | 22 | `P>1/アアｱ<T` | `[220, 326)` |
| `C212_2`: 2 | 34 | `P>1/ああｱ<T` | `[378, 484)` |
| `C212_3`: 3 | 46 | `P>１／あああ<T` | `[536, 642)` |

各範囲には続く状態行も含まれ、いずれも `A=2 B=12 R=701 S=[sentinel]` です。この例では入力文字と数字・記号の保存文字列が条件により変わっています。全ての文字種についての一般則を示すものではありません。

## 2. 文字列のままと書式展開

`FORCEKANA 0` で、`ZZ212T(1)` は `あアｱ{ZZ212N(2)}` を返します。対象命令と保存履歴の違いは次のとおりです。

| 条件・fixture行 | 対象命令 | 目印を含む出力行 | 状態の記録 | byte範囲 |
|---|---|---|---|---:|
| `C212_4`・58行 | `PRINTSK ZZ212T(1)` | `P>あアｱ{ZZ212N(2)}<T` | `A=1 B=1` | `[694, 816)` |
| `C212_12`・154行 | `PRINTFORMSK ZZ212T(1)` | `P>あアｱ2<T` | `A=2 B=12` | `[2116, 2222)` |

このfixtureでは `A` と `B` が補助関数の呼出し回数と順序を記録します。二つの履歴は、文字列中の `{ZZ212N(2)}` がそのまま出た条件と、`2` になった条件を示します。

## 3. 空でないSINGLEと空のSINGLE

`FORCEKANA 0` の `PRINTSINGLEK` について、引数がある条件と空の条件を比較します。以下は目印を含む保存履歴の行です。

| 条件・fixture行 | 対象命令 | 保存された目印間の行 | byte範囲 |
|---|---|---|---:|
| `C212_36`・442行 | `PRINTSINGLEK あアｱ{ZZ212N(1)}` | `P>\r\nあアｱ{ZZ212N(1)}\r\n<T\r\n` | `[6566, 6698)` |
| `C212_75`・910行 | `PRINTSINGLEK` | `P><T\r\n` | `[13504, 13600)` |

前者では対象文字列が目印とは別の行に保存されています。後者の本家**履歴**では目印の間に空行はありません。この記述は他の出力媒体における空行の有無を主張しません。

## 4. 表示抑止中の条件

`C212_85` では、fixtureの1030〜1032行で `SKIPDISP 1`、`PRINTFORMSK ZZ212T(1)`、`SKIPDISP 0` を順に置きます。`FORCEKANA` は3です。保存された本家履歴は `P><T\r\n` に続いて `C212_85_STATE A=0 B=0 R=0 S=[sentinel]` と記録されています。byte範囲は `[15024, 15116)` です。この条件で観測された出力と状態の例であり、全ての表示抑止条件の一般化ではありません。

GUI画面での実際の文字表示・レンダリング、色・フォント・styleやNativeの自然終了は、この保存履歴から確認していません。共有素材には、この82件の選定外である7条件も残っていますが、上記の例には使っていません。

[fixture]: ../../evidence/print-kd-shared-82-20261117/assets/native-01/inputs/ERB/SEARCHBOUND01.ERB
[config]: ../../evidence/print-kd-shared-82-20261117/assets/native-01/inputs/emuera.config
[n1]: ../../evidence/print-kd-shared-82-20261117/assets/native-01/raw-history.bin
[n2]: ../../evidence/print-kd-shared-82-20261117/assets/native-02/raw-history.bin
[index]: ../../evidence/print-kd-shared-82-20261117/index.json
