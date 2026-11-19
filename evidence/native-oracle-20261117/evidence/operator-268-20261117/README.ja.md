# 演算子：33条件の有限観測

[English](README.md) · [機械可読の条件・mode別記録](observations.json)

本家Emueraの保存観測とPyEmueraの比較です。１つの共有fixtureに35条件を順次含み、ここでは登録済み33条件を表示します。他の２条件は先行controlであり33には加えません。本家２回、PyEmuera１回の共有実行であり、33×３の個別実行ではありません。同じ本家ログSHAでも別々の実行として記録されています。

各行の入力と選択値・helperの順序に限る判定は31件が限定一致、２件が限定差異です。全ログ・全出力・文字列全体・全入力領域の一致ではありません。長さ19998の文字列は長さと先頭・末尾のみの観測です。本家２回の自然終了は未観測で、取得後にcleanup終了しています。PyEmueraは終了コード0と記録されています。Pyのstderrには、OUTPUTLOGが有限の履歴を `.pyemuera/logs` に保存するという警告があります。GUI画像は含みません。

各条件の開始時はA=B=0、C=701、整数配列の先頭２要素=6,99、文字列値=abです。左右の値helperはAを増やし、左はB=B×10+1、右はB=B×10+2で順序を記録します。添字helperはAのみを増やします。`measurements` は選択した出力で、`EQ` は最初の比較、`RETURN` は式の戻り値とその時点の配列値、`VECTOR` は配列の記録です。イベント順序とmode別値はJSONを参照してください。typed keyには共有関連先も含むため、直接実行を示す `observed_own_roles` と区別してください。

**元のERB・ERH・configとNative/Py rawは同梱していません。** 素材の作者・配布権限と出力の取り扱いは確認中です。以下は保存記録と元rawから抽出した選択値で、原bytesの再照合や完全な再実行はこの資料だけではできません。元資料の条件を超える結果は推定しません。

使用されたと記録された実行物はEmuera1824+v24とPyEmuera 3.0.0で、SHA-256はJSON内にあります。原ライセンスとPyEmueraのNOTICEは[LICENSES](LICENSES/)に収録しています。PyEmueraのNOTICE中の配布物・同梱構成は元のPyEmuera配布物を指し、この資料が同じ内容を含むという意味ではありません。調査の入力・投影資料への許諾は別途確認が必要です。

case IDまたはtyped keyは [observations.json](observations.json) の `case_id` / `typed_keys` を検索してください。現行の共通queryはcase registerへ案内しますが、この資料へのリンクは統合後に追加する必要があります。

## 条件と選択結果

| case ID | 条件 | Native | PyEmuera |
| --- | --- | --- | --- |
| `OPCONT268_repeat-str-int-0` | 文字列 ab を0回繰り返す。回数はhelperから取得。 | C=0; A=2 B=12; D0=6; D1=99; S=[] | 選択値・helper順が一致 |
| `OPCONT268_repeat-str-int-2` | 文字列 ab を2回繰り返す。回数はhelperから取得。 | C=4; A=2 B=12; D0=6; D1=99; S=[abab] | 選択値・helper順が一致 |
| `OPCONT268_repeat-str-int-9999` | 文字列 ab を9999回繰り返し、長さ・先頭・末尾を記録。 | C=19998; A=2 B=12; D0=6; D1=99; SLEN=19998; HEAD=[ab]; TAIL=[ab] | 選択値・helper順が一致 |
| `OPCONT268_strcmp-eq` | 文字列 ab 同士、続いて空文字と ab の == 比較。 | EQ C=1 A=2 B=12; C=0; A=3 B=121; D0=6; D1=99; S=[] | 選択値・helper順が一致 |
| `OPCONT268_strcmp-ne` | 文字列 ab 同士、続いて空文字と ab の != 比較。 | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | 選択値・helper順が一致 |
| `OPCONT268_strcmp-gt` | 文字列 ab 同士、続いて空文字と ab の > 比較。 | EQ C=0 A=2 B=12; C=0; A=3 B=121; D0=6; D1=99; S=[] | 選択値・helper順が一致 |
| `OPCONT268_strcmp-lt` | 文字列 ab 同士、続いて空文字と ab の < 比較。 | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | 選択値・helper順が一致 |
| `OPCONT268_strcmp-ge` | 文字列 ab 同士、続いて空文字と ab の >= 比較。 | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | EQ C=1 A=2 B=12; C=0; A=3 B=121; D0=6; D1=99; S=[] — 選択値に差 |
| `OPCONT268_strcmp-le` | 文字列 ab 同士、続いて空文字と ab の <= 比較。 | EQ C=0 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] | EQ C=1 A=2 B=12; C=1; A=3 B=121; D0=6; D1=99; S=[] — 選択値に差 |
| `OPCONT268_unary-effect-not` | helperから -1 を受け取り論理否定 ! を評価。 | C=0; A=1 B=1; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_unary-effect-complement` | helperから -1 を受け取りビット反転 ~ を評価。 | C=0; A=1 B=1; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_shift-narrow-left` | 1 を 2147483648 だけ左シフト。 | C=1; A=0 B=0; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_shift-narrow-right` | 1 を 2147483648 だけ右シフト。 | C=1; A=0 B=0; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_ternary-nested` | 外側が0、内側が1の入れ子条件式。選択branchは7を返すhelper。 | C=7; A=1 B=2; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_inc-edge-pre` | 配列0番に最大64bit整数を置き、前置++の式値と単独実行後を別に記録。 | RETURN C=-9223372036854775808 D0=-9223372036854775808; C=-9223372036854775808; A=1 B=0; D0=-9223372036854775808; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_inc-edge-post` | 配列0番に最大64bit整数を置き、後置++の式値と単独実行後を別に記録。 | RETURN C=9223372036854775807 D0=-9223372036854775808; C=9223372036854775807; A=1 B=0; D0=-9223372036854775808; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_dec-edge-pre` | 配列0番に最小64bit整数を置き、前置--の式値と単独実行後を別に記録。 | RETURN C=9223372036854775807 D0=9223372036854775807; C=9223372036854775807; A=1 B=0; D0=9223372036854775807; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_dec-edge-post` | 配列0番に最小64bit整数を置き、後置--の式値と単独実行後を別に記録。 | RETURN C=-9223372036854775808 D0=9223372036854775807; C=-9223372036854775808; A=1 B=0; D0=9223372036854775807; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_vector-num-0` | ２要素数値配列にhelperが返す11と22を代入。 | VECTOR 11,22; C=701; A=2 B=12; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_vector-num-constant` | ２要素数値配列に定数7と7を代入。 | VECTOR 7,7; C=701; A=0 B=0; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_vector-str-0` | ２要素文字列配列に２つのhelperが返す ab を代入。 | VECTOR [ab],[ab]; C=701; A=2 B=12; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_vector-str-constant` | ２要素文字列配列に定数 ab と ab を代入。 | VECTOR [ab],[ab]; C=701; A=0 B=0; D0=6; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_raw-form-comma` | 文字列へ FORM の ab, を代入し長さを記録。 | C=3; A=0 B=0; D0=6; D1=99; S=[ab,] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-add` | 配列0番の最大64bit整数に += 1。 | C=-9223372036854775808; A=0 B=0; D0=-9223372036854775808; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-sub` | 配列0番の最小64bit整数に -= 1。 | C=9223372036854775807; A=0 B=0; D0=9223372036854775807; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-mul` | 配列0番の最大64bit整数に *= 2。 | C=-2; A=0 B=0; D0=-2; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-shl` | 配列0番の1に <<= 64。 | C=1; A=0 B=0; D0=1; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-shr` | 配列0番の -8 に >>= 64。 | C=-8; A=0 B=0; D0=-8; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-or` | 配列0番の -1 に \|= 1。 | C=-1; A=0 B=0; D0=-1; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-and` | 配列0番の -1 に &= 1。 | C=1; A=0 B=0; D0=1; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-edge-xor` | 配列0番の -1 に ^= 1。 | C=-2; A=0 B=0; D0=-2; D1=99; S=[ab] | 選択値・helper順が一致 |
| `OPCONT268_compound-string-add` | 文字列 ab にhelperが返す ab を +=。 | C=4; A=1 B=2; D0=6; D1=99; S=[abab] | 選択値・helper順が一致 |
| `OPCONT268_compound-string-mul` | 文字列 ab にhelperが返す2を *=。 | C=4; A=1 B=2; D0=6; D1=99; S=[abab] | 選択値・helper順が一致 |

## ファイルの検査

このディレクトリで `python -B verify.py` を実行します。ファイル集合・ハッシュとmode間の整合を現在のmanifestに照合します。manifest自体の真正性や、非同梱の原rawへの意味的な一致はこのコマンドだけでは証明しません。
