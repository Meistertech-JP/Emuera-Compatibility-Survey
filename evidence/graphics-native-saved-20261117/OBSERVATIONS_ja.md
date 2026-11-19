# 本家Emueraの保存観測：画像・sprite API

[English entry](README.md) | [日本語入口](README.ja.md)

これは保存済みEmuera1824+v24実行のうち、入力と数値・診断を原ERBとrawでたどれる例を集めた資料です。例は特定のID、寸法、引数、状態に限ります。画像APIの返値、`GGETCOLOR`で採取した画像内の点、GUI画面に描かれた画素はそれぞれ別の観測です。ここでは画面や全ピクセルの一致を主張しません。

各行の「入力」「本家raw」はその行の保存済みfixtureとNative `emuera.log` への直接リンクです。設定、素材画像、Nativeの2回目、SHA-256は[参照一覧](REFERENCES_ja.md)にあります。34 fixtureの原ERB・設定・必要な画像入力・Native 2 raw、計145ファイルを保存時のSHA-256と照合し、各組の2 rawがbyte一致したことを確認しました。2回のbyte一致はその有限入力の記録であり、エンジンの全条件に一般化しません。NativeのDONEやrunner終了は、Nativeの自然終了コードの観測ではありません。

本家の値を先に示します。保存された当時の公開PyEmueraは、対象名の解決または事前の画像準備で停止し、同じ操作に到達しない例があるため、未到達を戻り値の差や一致としません。例えば`GWIDTH`の直接対照は、式で [E_FUNCTION](support/py-expression-missing/stderr.bin)、命令で [E_LOAD](support/py-method-missing/stderr.bin) を記録し、作成済み正例の式は [GCREATEのsetupで停止](support/py-created-setup/stderr.bin) しています。この例のPy側には`GWIDTH`正例の値はありません。この資料はグラフィック38対象全体の完了判定ではなく、原rawとfixtureを確認した選定例です。

## 作成状態・サイズ・色

| API | 入力条件 | 本家の保存値 | 根拠 |
|---|---|---|---|
| `GCREATE` / `GCREATED` | 画像ID 231、`GCREATE 231,3,2` を行い、存在・幅・高さを確認 | 作成の戻り値`1`、状態`1,3,2`。`GCREATED`の値はこの状態列の先頭 | [入力][DISP-E]・[raw][DISP-R] |
| `GWIDTH` / `GHEIGHT` | `GCREATE(230,4,3)` 後に各次元を取得 | 幅`4`、高さ`3` | [入力][Q-E]・[raw][Q-R] |
| `GWIDTH` / `GHEIGHT` | 未作成画像ID 230 | それぞれ`0` | 幅 [入力][QW0-E]・[raw][QW0-R]、高さ [入力][QH0-E]・[raw][QH0-R] |
| `GGETCOLOR` | 4×3画像を `4279312947`（`0xFF112233`）でクリアし、`(0,0)`、`(3,2)`を取得 | 両点とも`4279312947`。`(-1,0)`、`(4,0)`、`(0,3)`は`-1` | [入力][Q-E]・[raw][Q-R] |
| `GGETCOLOR` | 未作成画像ID 230 | `-1` | [入力][QC0-E]・[raw][QC0-R] |
| `SPRITEGETCOLOR` | resourcesに登録した4×3 spriteの左上・右下 | 両点の**返値**は`0`。左外・右外・下外は`-1` | [入力][QSP-E]・[raw][QSP-R] |
| `SPRITEGETCOLOR` | 未登録sprite名 | `-1` | [入力][QSC0-E]・[raw][QSC0-R] |

`SPRITEGETCOLOR`の返値`0`を、そのまま黒画素という意味にはできません。この例の入力BMPと変換の事情は元の [PIXEL_ENCODING.json](support/pixel-encoding.json) に記録されています。`GGETCOLOR`の`0xFF112233`とも同じ形式と決め付けないでください。`GGETCOLOR`の負のy座標は、この表では試していません。

## 破棄・クリア・1点への書込み

| API | 入力条件 | 本家の保存値 | 根拠 |
|---|---|---|---|
| `GDISPOSE` | ID 231に3×2を作成後、破棄・再破棄・2×1で再作成 | 破棄`1`後の存在/幅/高さ`0,0,0`、再破棄`0`、再作成`1`後`1,2,1` | [入力][DISP-E]・[raw][DISP-R] |
| `GCLEAR` | 3×2画像を `0xFF112233` でクリアし、次に透明色0でクリア | 両クリアとも`1`。選択3点は不透明色`4279312947`、透明色では`0` | [入力][CLEAR-E]・[raw][CLEAR-R] |
| `GCLEAR` | 未作成IDで有効な色を指定 | `0` | [入力][CLR0-E]・[raw][CLR0-R] |
| `GSETCOLOR` | 3×2画像の `(1,1)` を `0xFF112233`、次に`0xFFFFFFFF`に設定 | どちらも`1`。採取順 `(0,0),(1,1),(2,1)` の結果はそれぞれ `0,4279312947,0` と `0,4294967295,0` | [入力][COLOR-E]・[raw][COLOR-R] |
| `GSETCOLOR` | 同じ画像で `x=-1`、`x=3`、`y=2` | 各戻り値`0`。選択3点は変更前のまま | [入力][COLOR-E]・[raw][COLOR-R] |
| `GSETCOLOR` | 未作成ID、範囲外の色と座標を後続引数に指定 | `0`を返した。これはこの未作成条件の観測で、作成済み画像の範囲エラーを意味しない | [入力][SET0-E]・[raw][SET0-R] |

`GCLEAR`の未作成IDと範囲外色を組み合わせた別条件の本家診断は、このbundleには収録していません。後続のcase別調査では元の保存ログと追加実行の両方に診断を確認しました。エラー後の戻り値や状態は確認していません。

## ファイルを使う画像

いずれもfixture同梱の合成4×3 BMPを使った例です。参照一覧からBMPも開けます。

| API | 入力条件 | 本家の保存値 | 根拠 |
|---|---|---|---|
| `GCREATEFROMFILE` | ID 232に `PIX232.BMP` を読込み | 戻り値`1`、存在`1`、4×3。`(0,0)=4281640448`、`(3,2)=4283891853` | [入力][FILE-E]・[raw][FILE-R] |
| `GCREATEFROMFILE` | 既に作成済みのID 232で別名ファイルを指定 | 戻り値`0`、既存の4×3と上記2点は維持。記録された評価markerは`1` | [入力][FILE-E]・[raw][FILE-R] |
| `GSAVE` | 上記画像ID 232をslot 232に保存 | 戻り値`1`。slot `-1` と `2147483648` は各`0` | [入力][SAVE-E]・[raw][SAVE-R] |
| `GLOAD` | slot 232を空のID 233へ読込み | 戻り値`1`、4×3、上記2点を記録。既存IDへの再読込みは`0`。slot `-1` と `2147483648` は各`0` | [入力][LOAD-E]・[raw][LOAD-R] |

別記録では保存PNGの12ピクセルが検査されていますが、その記録と出力PNGはこのbundleに含まれず、ここだけでは全ピクセルの往復一致を再照合できません。上表で挙げた2点のAPI返値や画面表示とは区別します。負の画像IDなど、ログに後続や診断がない条件を診断確認済みとしません。

## brush・font・矩形・pen

| API | 入力条件 | 本家の保存値・診断 | 根拠 |
|---|---|---|---|
| `GFILLRECTANGLE` | 4×3画像上、初期brushと `0xFF112233` brushで矩形を塗る | 呼出しは各`1`。4つの選択点では、初期brush時 `0,4278190080,4278190080,0`、色指定後 `0,4279312947,4279312947,0` | [入力][FILL-E]・[raw][FILL-R] |
| `GFILLRECTANGLE` | 作成済み画像で幅0 | ERB 21行目、第4引数`0`が不適切と診断。エラー後の状態は未観測 | [入力][FILL0-E]・[raw][FILL0-R] |
| `GSETBRUSH` | ID 233に色を設定し、後続fill、次に白を設定 | 設定`1`の直後は選択4点が`0`のまま。後続fillで色を観測し、白に交換して塗った後は最初の点が`4294967295` | [入力][BRUSH-E]・[raw][BRUSH-R] |
| `GSETFONT` | ID 233、Arial、サイズ12・18・0・-1 | 12と18は各`1`、0と-1は各`0`。選択4点は変化なし | [入力][FONT-E]・[raw][FONT-R] |
| `GSETPEN` | 作成済みIDへの2引数呼出し | ERB 21行目で `System.IndexOutOfRangeException`。設定後のpen状態は未観測 | [入力][PEN2-E]・[raw][PEN2-R] |
| `GSETPEN` | 3引数 `GSETPEN(233,4279312947,1)` | ERB 9行目で引数個数が違うと診断 | [入力][PEN3-E]・[raw][PEN3-R] |

`GSETFONT`の返値は、フォントの実際の字体、代替フォント、GUI表示の正しさを示しません。矩形の表は選択した4点だけです。`GSETPEN`の例外は本家で保存された診断であり、一般に期待される仕様として書き換えません。

## Sprite・アニメーション

| API | 入力条件 | 本家の保存値 | 根拠 |
|---|---|---|---|
| `SPRITECREATE` / `SPRITECREATED` / `SPRITEWIDTH` / `SPRITEHEIGHT` | 4×3の画像ID 234から `SP234` を作成 | 作成`1`、存在`1`、幅`4`、高さ`3`。同名再作成は`0` | [入力][LIFE-E]・[raw][LIFE-R] |
| `SPRITEDISPOSE` | 上記 `SP234` を破棄し、存在確認後に再破棄 | 破棄`1`、存在`0`、再破棄`0` | [入力][LIFE-E]・[raw][LIFE-R] |
| `SPRITECREATE` / サイズ取得 | 座標`(1,1)`から2×2を切り出し再作成 | 作成`1`、幅`2`・高さ`2` | [入力][LIFE-E]・[raw][LIFE-R] |
| `SPRITEANIMECREATE` | `AN234`を4×3で作成し、同名で再作成 | 最初`1`、存在`1`、幅`4`・高さ`3`、再作成`0` | [入力][LIFE-E]・[raw][LIFE-R] |
| `SPRITEANIMEADDFRAME` | 上記animationへ適切な2フレームを追加 | 各`1`。delay `0`、範囲外矩形、未作成graphを指定した各例は`0` | [入力][LIFE-E]・[raw][LIFE-R] |
| `SPRITEANIMEADDFRAME` | 空のanimation名 | `0`。記録markerは第1引数までの`1` | [入力][AN0-E]・[raw][AN0-R] |
| `SPRITEANIMEADDFRAME` | 空でない未登録animation名 | ERB 9行目で `System.NullReferenceException`。エラー後状態は未観測 | [入力][ANERR-E]・[raw][ANERR-R] |
| `SETANIMETIMER` | `0,-2147483648,-1,1,9,10,32767,0` を順に指定 | 記録された各戻り値は`1` | [入力][TIMER-E]・[raw][TIMER-R] |
| `SETANIMETIMER` | `32768` | ERB 9行目、第1引数が不適切と診断 | [入力][TIMERERR-E]・[raw][TIMERERR-R] |

このアニメーション例は作成・追加の返値と寸法を観測したもので、フレーム切替、時間経過、画面やsprite画像のpixelを観測したものではありません。

## 描画コピーとsprite位置

| API | 入力条件 | 本家の保存値 | 根拠 |
|---|---|---|---|
| `GDRAWG` | 4×3の送信元・宛先を作成し全体をコピー | 戻り値`1`、宛先の `(0,0)` と `(3,2)` は`4279312947` | [入力][DG-E]・[raw][DG-R] |
| `GDRAWSPRITE` | 4×3送信元から作った `SPR235` を4×3宛先へ描画 | 戻り値`1`、同じ2点は`4279312947` | [入力][DS-E]・[raw][DS-R] |
| `GDRAWGWITHMASK` | 白い4×3マスクを使ってコピー | 戻り値`1`、同じ2点は`4279312947` | [入力][DM-E]・[raw][DM-R] |
| `GDRAWG` | 宛先未作成、または宛先のみ作成して送信元未作成 | 各`0`。記録された引数評価markerはそれぞれ`1`、`12` | 宛先なし [入力][DG0-E]・[raw][DG0-R]、送信元なし [入力][DG1-E]・[raw][DG1-R] |
| `SPRITEMOVE` | resources登録spriteの初期位置`(10,-20)`に `(3,-4)` を2回、`(-16,28)`を1回 | 各戻り値`1`、位置は `(13,-24)` → `(16,-28)` → `(0,0)` | [入力][MOVE-E]・[raw][MOVE-R] |
| `SPRITESETPOS` | 同じ初期位置に同じ3組を指定 | 各戻り値`1`、位置は `(3,-4)` → `(3,-4)` → `(-16,28)` | [入力][SETPOS-E]・[raw][SETPOS-R] |
| `SPRITEMOVE` / `SPRITESETPOS` | 未登録名と範囲外の座標を指定 | 各`0`、記録markerは名前側だけの`1` | MOVE [入力][MOVE0-E]・[raw][MOVE0-R]、SETPOS [入力][SETPOS0-E]・[raw][SETPOS0-R] |

描画の2点取得は画像内の選択点のAPI返値であり、GUI画面・全領域・他のマスクや透明度の検証ではありません。

## 再利用時の注意

本家rawはUTF-16、ERBは各入力のバイトを保持しています。`RESULT`と`RESULTS`、式の返値、helperの評価markerは別項目です。表の例は主に式形式を直接引用し、命令形式まで同じ根拠から推測しません。式の初期`RESULT=701`と、命令形式で結果が`RESULT`に代入される既存比較は、元の各caseの記録を参照してください。

画像やCSVは各fixtureの `inputs` 以下に元の相対配置で収録しています。素材の権利・公開条件は確認中です。

[Q-E]: assets/Q/inputs/ERB/SEARCHBOUND01.ERB
[Q-R]: assets/Q/raw/native-01.bin

[QSP-E]: assets/QSP/inputs/ERB/SEARCHBOUND01.ERB
[QSP-R]: assets/QSP/raw/native-01.bin

[QW0-E]: assets/QW0/inputs/ERB/SEARCHBOUND01.ERB
[QW0-R]: assets/QW0/raw/native-01.bin

[QH0-E]: assets/QH0/inputs/ERB/SEARCHBOUND01.ERB
[QH0-R]: assets/QH0/raw/native-01.bin

[QC0-E]: assets/QC0/inputs/ERB/SEARCHBOUND01.ERB
[QC0-R]: assets/QC0/raw/native-01.bin

[QSC0-E]: assets/QSC0/inputs/ERB/SEARCHBOUND01.ERB
[QSC0-R]: assets/QSC0/raw/native-01.bin

[DISP-E]: assets/DISP/inputs/ERB/GRAPHICS231.ERB
[DISP-R]: assets/DISP/raw/native-01.bin

[CLEAR-E]: assets/CLEAR/inputs/ERB/GRAPHICS231.ERB
[CLEAR-R]: assets/CLEAR/raw/native-01.bin

[COLOR-E]: assets/COLOR/inputs/ERB/GRAPHICS231.ERB
[COLOR-R]: assets/COLOR/raw/native-01.bin

[CLR0-E]: assets/CLR0/inputs/ERB/GRAPHICS231.ERB
[CLR0-R]: assets/CLR0/raw/native-01.bin

[SET0-E]: assets/SET0/inputs/ERB/GRAPHICS231.ERB
[SET0-R]: assets/SET0/raw/native-01.bin

[FILE-E]: assets/FILE/inputs/ERB/SEARCHBOUND01.ERB
[FILE-R]: assets/FILE/raw/native-01.bin

[SAVE-E]: assets/SAVE/inputs/ERB/SEARCHBOUND01.ERB
[SAVE-R]: assets/SAVE/raw/native-01.bin

[LOAD-E]: assets/LOAD/inputs/ERB/SEARCHBOUND01.ERB
[LOAD-R]: assets/LOAD/raw/native-01.bin

[FILL-E]: assets/FILL/inputs/ERB/GRAPHICS233.ERB
[FILL-R]: assets/FILL/raw/native-01.bin

[BRUSH-E]: assets/BRUSH/inputs/ERB/GRAPHICS233.ERB
[BRUSH-R]: assets/BRUSH/raw/native-01.bin

[FONT-E]: assets/FONT/inputs/ERB/GRAPHICS233.ERB
[FONT-R]: assets/FONT/raw/native-01.bin

[PEN2-E]: assets/PEN2/inputs/ERB/GRAPHICS233.ERB
[PEN2-R]: assets/PEN2/raw/native-01.bin

[PEN3-E]: assets/PEN3/inputs/ERB/GRAPHICS233.ERB
[PEN3-R]: assets/PEN3/raw/native-01.bin

[FILL0-E]: assets/FILL0/inputs/ERB/GRAPHICS233.ERB
[FILL0-R]: assets/FILL0/raw/native-01.bin

[LIFE-E]: assets/LIFE/inputs/ERB/SEARCHBOUND01.ERB
[LIFE-R]: assets/LIFE/raw/native-01.bin

[AN0-E]: assets/AN0/inputs/ERB/SEARCHBOUND01.ERB
[AN0-R]: assets/AN0/raw/native-01.bin

[ANERR-E]: assets/ANERR/inputs/ERB/SEARCHBOUND01.ERB
[ANERR-R]: assets/ANERR/raw/native-01.bin

[TIMER-E]: assets/TIMER/inputs/ERB/SEARCHBOUND01.ERB
[TIMER-R]: assets/TIMER/raw/native-01.bin

[TIMERERR-E]: assets/TIMERERR/inputs/ERB/SEARCHBOUND01.ERB
[TIMERERR-R]: assets/TIMERERR/raw/native-01.bin

[DG-E]: assets/DG/inputs/ERB/SEARCHBOUND01.ERB
[DG-R]: assets/DG/raw/native-01.bin

[DS-E]: assets/DS/inputs/ERB/SEARCHBOUND01.ERB
[DS-R]: assets/DS/raw/native-01.bin

[DM-E]: assets/DM/inputs/ERB/SEARCHBOUND01.ERB
[DM-R]: assets/DM/raw/native-01.bin

[DG0-E]: assets/DG0/inputs/ERB/SEARCHBOUND01.ERB
[DG0-R]: assets/DG0/raw/native-01.bin

[DG1-E]: assets/DG1/inputs/ERB/SEARCHBOUND01.ERB
[DG1-R]: assets/DG1/raw/native-01.bin

[MOVE-E]: assets/MOVE/inputs/ERB/SEARCHBOUND01.ERB
[MOVE-R]: assets/MOVE/raw/native-01.bin

[SETPOS-E]: assets/SETPOS/inputs/ERB/SEARCHBOUND01.ERB
[SETPOS-R]: assets/SETPOS/raw/native-01.bin

[MOVE0-E]: assets/MOVE0/inputs/ERB/SEARCHBOUND01.ERB
[MOVE0-R]: assets/MOVE0/raw/native-01.bin

[SETPOS0-E]: assets/SETPOS0/inputs/ERB/SEARCHBOUND01.ERB
[SETPOS0-R]: assets/SETPOS0/raw/native-01.bin
