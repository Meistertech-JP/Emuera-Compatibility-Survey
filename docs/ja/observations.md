# 観測結果の例

[English](../en/observations.md) | [調査結果の読み方](results.md)

Emuera 1.824 +v24とPyEmuera 3.0.0について、保存された入力と出力から確認できる結果の例です。これらは今後のPyEmueraの互換性修正・回帰検証、および他の互換実装から参照するための観測です。各行の結論は記載された条件に限ります。リンク先には条件や保存ログ、未観測の範囲があります。

| 対象・条件 | 本家Emueraの観測 | PyEmueraの観測 |
| --- | --- | --- |
| `RAND`、`CompatiRAND:YES`（`COLON_NORMAL_COMPAT_RAND_YES`） | `0`を返し、後続へ進んだ | `RAND:n requires n > 0`で停止 |
| `RAND:0`、`CompatiRAND:YES`（`COLON_RAND_ZERO_COMPAT_YES`） | `0`を返し、後続へ進んだ | 同じ`E_ARGUMENT`で停止 |
| 条件式と`ENDIF`を省いた`IF`（`P38`） | `BEFORE`を表示した後、該当行で停止 | 構文エラーで停止し、`BEFORE`は表示されなかった |
| 式中の単独`=`（`GMF_LEX_LONE_EQUALS`） | `GM_BEFORE`の後に停止し、比較には`==`を使うよう診断 | `GM_BEFORE`の後に停止し、式中の`=`に対する`E_SYNTAX`を表示 |
| 命令形式`LINEISEMPTY`、完成行後と`PRINTBUTTON`文の後の未確定行（`LINEBUF20261115_button_method`） | それぞれ`EMPTY=1`、`BUTTON=0` | 同じ選択値を出力 |
| 式形式`CBGSETG(93236,11,12,1)`（`UIQUERY236_cbgsetg-expr-direct`） | 選択ログに`V=0` | 関数解決で`E_FUNCTION`となり、後続へ到達しなかった |
| 命令形式`LIMIT`、`x=8`または`9`、`min=8`、`max=4` | `RESULT=4` | `RESULT=8` |
| `PRINTC`・`PRINTLC`、設定幅25、空文字・`ABC`・25文字のASCII入力 | 選択した出力行と`RESULT=777`・`RESULTS=SENTINEL`を記録 | 同じ選択出力と値を記録 |

`RAND`と`RAND:0`は別々の入力による観測です。未閉鎖`IF`の本家側は保存画面で確認しました。単独`=`は両側とも停止しますが、診断文が異なります。`LINEISEMPTY`は`PRINTBUTTON`文の後の未確定行に関する限定条件での値で、クリックや画面描画の一致は意味しません。`CBGSETG`は当該の直接呼出し条件に限ります。

`PRINTC`・`PRINTLC`の2ケース（`COLUMN_PRINTC_EMPTY_SHORT_EQUAL_20261115`・`COLUMN_PRINTLC_EMPTY_SHORT_EQUAL_20261115`）は、同じfixtureを用いた本家2回とPyEmuera 1回の保存出力です。選択した文字列と状態の比較であり、画素やフォントの一致、本家の自然終了を意味しません。元のfixture・ログは同梱していません。原資料を用いた[限定リーダー](../../tools/LEGACY_EVIDENCE.ja.md)では、記録された条件と出力を照合できます。

- [`RAND`・`RAND:0`・`IF`・単独`=`の条件と保存出力](../../differences/representative-20261116/README.ja.md)
- [本家の保存観測を検索](../../evidence/native-oracle-20261117/docs/native-oracle.html)（113行の選定資料）
- [OPCONT268の33条件の保存観測](../../evidence/native-oracle-20261117/evidence/operator-268-20261117/README.ja.md)
- [`DO`・`LOOP`でのBREAKと偽条件の保存観測](../../evidence/doloop259-20261117/README.ja.md)（共有fixtureによる本家2回・PyEmuera 1回）
- [`PRINTDW`・配列・レベル取得・`SAVECHARA`の8ケースの選択観測](../../evidence/eight-scoped-observations-20261117/README.ja.md)（元rawは非同梱）
- [`LINEISEMPTY`の条件と保存出力](../../evidence/lineisempty-acceptance-20261117/README.ja.md)
- [`CBGSETG`を含む背景操作の保存結果](../../evidence/console-background-24-20261117/README.ja.md)
- [PRINT系の本家保存観測の例](print-observations.md)
- [`PRINTVKW`・`PRINTVDW`の待機解除後](../../evidence/wait-release-20261117/README.ja.md)と[空文字・後続項のゼロ除算](../../evidence/wait-c15-20261117/README.ja.md)の追加観測
- [画像・スプライトAPIの本家保存観測](../../evidence/graphics-native-saved-20261117/README.ja.md)
- [画像系38ケースの本家観測](../../evidence/graphics-38-cases-20261117/README.ja.md)
- [本家GUIの画像・背景・ボタンの観測](../../evidence/graphics-gui-observations-20261117/README.ja.md)
- [`INRANGE`・`LIMIT`・`PRINTVW`の条件と保存出力](../../evidence/nine-saved-observations-20261117/README.ja.md)（記録された設定と同じSHAの[別置き設定](../../harness/fixtures/emuera.config)）
- [式・入力・診断・副作用の保存観測](../../evidence/new-replay-20261116/public/README.ja.md)

`python -B tools/query.py METHOD_BOUNDARY_LIMIT_NORMAL_20261115` は、`additional_evidence_discovery` の `nine_saved_observations` に上記LIMITの条件、両側の値、保存出力の参照を返します。出力中のraw／UTF-8パスは該当資料フォルダーからの相対パスです。

未検証の条件や、観測結果を確定できなかったケースは、成功や差異として扱いません。これらは例であり、全対象・全条件の一覧ではありません。[対象名やケースIDから検索](../../README.ja.md)できます。

## キャラクターCSVの参照：CSVFIELDS01

キャラクターID 1と添字1のCSV項目を参照したケースです。本家とPyEmueraの保存された `OUTPUTLOG` はバイト一致し、次の値が記録されています。

| 出力 | 関数 | 値 |
|---|---|---|
| CALL | `CSVCALLNAME` | CALLONE |
| NICK | `CSVNICKNAME` | NICKONE |
| MASTER | `CSVMASTERNAME` | MASTERONE |
| CSTR | `CSVCSTR` | STRVALUE |
| MARK | `CSVMARK` | 13 |
| REL | `CSVRELATION` | 17 |
| TALENT | `CSVTALENT` | 19 |
| FLAG | `CSVCFLAG` | 23 |
| EQUIP | `CSVEQUIP` | 29 |
| JUEL | `CSVJUEL` | 31 |

対象は有効なキャラクターと添字を各1条件で試した出力ログです。無効・未定義・SP条件や画面全体の一致は含みません。ログは後続の `DONE` を出力する前に保存されており、本家の自然終了も未観測です。元の入力ファイルと2つのログはこの資料に含まれません。

## SELECTCASEの文字列条件：SELECT277

同じfixtureの4条件を、状態を初期化して比較した保存記録です。本家2回、PyEmuera 1回の共有実行です。各記号の値は選択された観測項目です。

| ケース・条件 | 本家 | PyEmuera |
|---|---|---|
| RANGE：`b` が `a TO c` に入る | `S=1 LO=1 HI=1 REL=0 T=0 O=123 B=11 A=1` | 同じ |
| IS：`b`、範囲下限 `c` の不一致後に `IS >= b` | `S=1 LO=1 HI=0 REL=1 T=1 O=1245 B=11 A=1` | `S=1 LO=1 HI=0 REL=1 T=0 O=124 B=11 A=1` |
| FALLBACK：`z` が `a,b` と不一致、CASEELSEあり | `S=1 C1=1 C2=1 O=178 B=33 A=1` | 同じ |
| NODEFAULT：同じ不一致、CASEELSEなし | `S=1 C1=1 C2=1 O=178 B=77 A=1` | 同じ |

`S` はselector、`LO`・`HI`・`REL`・`T` は条件評価helperの回数、`C1`・`C2` は候補評価回数、`O` はhelper順序、`B` は選択bodyまたは保持値、`A` は後続到達です。ISでは両方とも `B=11` ですが、`T` と `O` に差があり、同じbodyの値だけで同じ条件が選択されたとは言えません。CASEELSEが実際に選択されたのはFALLBACKのみです。

当時の調査台帳では、`command_or_syntax:SELECTCASE` に有限範囲の一致、`structural_syntax:SELECTCASE` に記録済み差異が付いています。表は `SELECT277` の文字列4条件の保存観測です。元の出力・入力ファイル・実行記録は非同梱で、本家の自然終了は未観測です。対象ごとの判定とケースIDは[対象台帳](../../results/survey.json)で確認できます。

## MATCH系の5ケース

次の式は、それぞれ本家とPyEmueraの保存 `OUTPUTLOG` がバイト一致した条件です。数値は両者で共通です。

| ケース | 入力・式と結果 |
|---|---|
| COVMATCH01 | `A=[9,3,9]`、`MATCH(A,9)=2`、`MATCH(A,9,0,2)=1`、`MATCH(A,9,0,3)=2` |
| COVCMATCH01 | キャラクター2人の `CFLAG:0` が3と7。`CMATCH(CFLAG:0,7)=1`、範囲 `[0,1)` は0、`[0,2)` は1 |
| COVGROUP01 | `GROUPMATCH(2,2)=1`、`GROUPMATCH(2,1,2,2)=2`、`GROUPMATCH("x","x","y")=1` |
| COVNOSAME01 | `NOSAMES(1,2)=1`、`NOSAMES(1,2,1)=0`、`NOSAMES("x","x")=0` |
| COVALLSAME01 | `ALLSAMES(2,2)=1`、`ALLSAMES(2,2,3)=0`、`ALLSAMES("x","x")=1` |

各ケースのログは結果出力後、`DONE` より前に保存されています。全画面や標準出力の一致、自然終了、空配列・不正引数・日本語照合などはこのログ比較の対象外です。元fixtureとログはこの資料には含まれません。

## 既定色の取得：GETTER251

保存された式形式と命令形式の各fixtureで、本家の既定前景・背景・フォーカス色をそれぞれRGB `(17,34,51)`・`(4,5,6)`・`(7,8,9)` に設定した条件です。両fixtureとも先に現在の前景・背景色を別の値へ変更しています。各fixtureの共有実行は本家2回、PyEmuera 1回です。

| 対象 | 本家の値 | PyEmueraの値 |
|---|---:|---:|
| `GETDEFCOLOR` | 1122867 | 12632256 |
| `GETDEFBGCOLOR` | 263430 | 0 |
| `GETFOCUSCOLOR` | 460809 | 16776960 |

式形式では、記録された `RESULT:0`・`RESULT:1`・`RESULTS` の初期値が保持されました。命令形式では各値が `RESULT:0` に書き込まれ、記録された `RESULT:1`・`RESULTS` は保持されました。これはこの設定と実行履歴での値であり、他の設定や画面全体の一致を示しません。元raw・fixtureは非同梱で、本家の自然終了は未観測です。

## 論理演算子の短絡：OPNORMAL273_E140

`A=0`、`B=0` のもとで、呼び出されると `A` を増やし `1/(B-B)` を評価する関数 `ZZ_BAD()` を右辺に置きました。保存済み本家2回と後続PyEmuera 1回では、次の値が記録されています。

| 式 | 結果 | `ZZ_BAD()` の呼出し回数 |
|---|---:|---:|
| `0&&ZZ_BAD()` | 0 | 0 |
| `0!&ZZ_BAD()` | 1 | 0 |

両条件の選択マーカーは3実行で一致し、右辺の関数は呼び出されていません。この2条件に限った観測であり、他のguardや異常終了後の状態、全演算子条件を証明するものではありません。旧Py実行のreceiptを復元したものではなく、元raw・fixtureは非同梱です。本家の自然終了も未観測です。

## GROUPMATCHの命令形式：GROUPMATCH266

先に保存された本家2回と、同じfixtureによる後続PyEmuera 1回の記録です。次の4条件の `OUTPUTLOG` は3本とも同一bytesで、表は共通の観測値です。

| ケース | 引数 | `RESULT` | helper回数／順序 | `RESULTS` |
|---|---|---:|---|---|
| `GROUPMATCH266_GR0` | `1,1,2,1` | 2 | `4 / 1234` | `SENTINEL` |
| `GROUPMATCH266_GR1` | `1,2,3` | 0 | `3 / 123` | `SENTINEL` |
| `GROUPMATCH266_GR2` | `"a","a","b","a"` | 2 | `4 / 1234` | `SENTINEL` |
| `GROUPMATCH266_GR3` | `"a","b","c"` | 0 | `3 / 123` | `SENTINEL` |

これは命令形式の限定比較で、他の入力・標準出力全体・GUIの一致を示しません。後続Pyのreceiptは旧Py実行のreceiptを復元するものではなく、本家の自然終了は未観測です。元ログ・fixture・receiptは非同梱です。

## ELSEIF・ENDIFの条件分岐：IFCHAIN269

同じfixtureを本家2回、PyEmuera 1回実行した保存記録では、次の選択値が一致しました。`C1`〜`C3` は条件helperの呼出し回数、`ORDER` は呼出し順、`AFTER` は後続到達です。

| ケース | 条件 | DEST | C1 / C2 / C3 | ORDER | AFTER |
|---|---|---:|---|---:|---:|
| `IFCHAIN269_P1` | 初回条件が偽、次のELSEIFが真 | 22 | 1 / 1 / 0 | 12 | 1 |
| `IFCHAIN269_P2` | すべての条件が偽、ELSEなし | 79 | 1 / 1 / 1 | 123 | 1 |

ELSEIFは評価された条件、ENDIFは対応する構造と後続到達として扱います。P1で未選択のELSEの実行は確認していません。本家自然終了とQUIT完了は未観測で、元raw・fixtureは非同梱です。

## 未登録関数名の比較

`CHKVARDATA`・`CHKGLOBALDATA`・`FIND_VARDATA` の不在ケースでは、本家とPyEmueraの双方が4行目で名前解決に失敗し、後続の `OBS225`・`DONE225` に到達しませんでした。PyEmueraは `E_FUNCTION: Unknown function` を出し、終了コード1でした。本家の自然終了は未観測です。元caseの `matched_scoped` は、この名前解決失敗の限定的な一致であり、呼出しの成功を意味しません。

同名ユーザー関数を使った別のcontrolでは、戻り値とhelper回数は一致し、名前衝突警告が異なると記録されています。コメントアウトされた本家handlerの未実行部分や、仮定した引数仕様は検証していません。元raw・fixtureは非同梱です。

## 画像関連APIの利用可否：RECEIPT252

画像resourceを置かない初期状態で、各対象を別々のfixtureで呼び出した保存記録です。本家では式形式と命令形式のどちらも、下表の値を出力して後続の `AFTER`・`DONE` に到達しました。

| 対象 | 条件 | 本家の式・命令形式の値 |
|---|---|---:|
| `SPRITEWIDTH` | 存在しない `ZZ_MISSING` | 0 |
| `SPRITEHEIGHT` | 存在しない `ZZ_MISSING` | 0 |
| `SPRITEPOSX` | 存在しない `ZZ_MISSING` | 0 |
| `SPRITEPOSY` | 存在しない `ZZ_MISSING` | 0 |
| `GCREATED` | graphics ID 0 | 0 |
| `GCREATE` | graphics ID 0、幅・高さ16 | 1 |

`GCREATED` と `GCREATE` は別fixtureであり、同一実行での生成前後の変化を示すものではありません。式形式と命令形式は別々のtyped対象です。保存済み本家witnessは計16本で、後続の比較時に新たな本家実行はありません。

後続PyEmuera実行は12形式すべてで対象の値を返す前に停止しました。式形式は `E_FUNCTION`、命令形式は読込時の `E_LOAD` で、`AFTER`・`DONE` は出ていません。PyEmueraの戻り値を本家の0・1と比較した結果ではありません。各case IDは `RECEIPT252_expression_function_対象名` または `RECEIPT252_method_as_command_対象名` です。

画像が存在する場合の動作や画素・GUI全体の一致は対象外で、本家の自然終了も未観測です。この節の原ログ・fixture・receiptは非同梱です。別条件の[画像系38ケース](../../evidence/graphics-38-cases-20261117/README.ja.md)も参照できます。
