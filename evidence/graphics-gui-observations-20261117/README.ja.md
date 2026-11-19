# 本家Emuera GUI：保存された有限観測

[English](README.md) · [機械可読一覧](cases.json)

ここにある9条件は、既存38ケースとは異なるfixtureによる本家単独の保存記録です。設定ファイルは共通です。元38件の判定変更、PyEmueraとの一致、全機能の完了を示しません。各条件の入力ERB・設定・UTF-16本家履歴・画像クロップは下表から開けます。エンジンと原ZIPは含みません。

履歴に記録された値と画面の見た目、画像内部の数値を分けています。画像は縮小した画面の一部で、全画素・正確な画面座標の証明ではありません。自然終了はどの条件でも未観測です。取得receiptのない画像は、保存名やファイル更新時刻だけから取得元・phase・時刻・操作順を確定できません。取得記録のある画像も、その記録は過去のOS状態や入力時刻を再認証するものではありません。

| 条件と保存された有限観測 | 入力・履歴・画像 |
|---|---|
| `gui-cbgsetg-01`：64×48画像を生成・単色化しCBGSETGを呼んだ記録。黒い画面下端に細い赤色部分が見えるが、画像だけではその出所や全矩形を確定できない。 | [ERB](cases/gui-cbgsetg-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-cbgsetg-01/emuera.config) · [Native](cases/gui-cbgsetg-01/native-history.bin) · [画像1](cases/gui-cbgsetg-01/images/gui-client-crop.png) |
| `gui-sprite-paint-01`：画像作成・青の塗りつぶし・赤のブラシと矩形描画・sprite作成・背景への配置が各1。クロップには青い領域とその内側の赤い領域が見える。厳密な画面座標や全画素の比較ではない。 | [ERB](cases/gui-sprite-paint-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-sprite-paint-01/emuera.config) · [Native](cases/gui-sprite-paint-01/native-history.bin) · [画像1](cases/gui-sprite-paint-01/images/gui-image-crop.png) |
| `gui-background-clear-01`：履歴に二つの画像の設定、範囲除去、全消去が記録される。保存画像には赤緑、緑のみ、どちらも見えない領域がある。各画像に取得receiptはなく、画像名だけで取得phase・順序・PID・時刻を確定できない。 | [ERB](cases/gui-background-clear-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-background-clear-01/emuera.config) · [Native](cases/gui-background-clear-01/native-history.bin) · [画像1](cases/gui-background-clear-01/images/phase1-crop.png) · [画像2](cases/gui-background-clear-01/images/phase2-crop.png) · [画像3](cases/gui-background-clear-01/images/phase3-crop.png) |
| `gui-button-01`：ボタン素材とmap・ボタン設定の履歴があり、クロップはマゼンタ色の領域を示す。画像に取得receiptやカーソル／入力の記録はなく、名前だけでhover・クリック成立は確定できない。BUTTON_RESULTと後続行は履歴にない。 | [ERB](cases/gui-button-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-button-01/emuera.config) · [Native](cases/gui-button-01/native-history.bin) · [画像1](cases/gui-button-01/images/button-hover-crop.png) |
| `gui-button-mousekey-01`：INPUTMOUSEKEYの保存結果はRESULT:0〜:4が1,1048576,62,-176,7で、後続markerにも到達。マゼンタの画像は取得receiptがなく、操作主体・時刻や画像との同時性は確定しない。通常INPUTの結果とは別。 | [ERB](cases/gui-button-mousekey-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-button-mousekey-01/emuera.config) · [Native](cases/gui-button-mousekey-01/native-history.bin) · [画像1](cases/gui-button-mousekey-01/images/button-click-crop.png) |
| `gui-button-clear-01`：履歴はmap除去とbutton消去の返値1を記録。画像1・2に緑、画像3に緑は見えない。画像2・3にはphase・取得時刻幅・SHAの記録、画像1には個別receiptがない。別のEmuera名プロセスの一時目撃が報告され、由来と時間的重複は未確定。 | [ERB](cases/gui-button-clear-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-button-clear-01/emuera.config) · [Native](cases/gui-button-clear-01/native-history.bin) · [画像1](cases/gui-button-clear-01/images/phase1-crop.png) · [画像2](cases/gui-button-clear-01/images/phase2-crop.png) · [画像3](cases/gui-button-clear-01/images/phase3-crop.png) |
| `gui-sprite-position-01`：sprite初期位置(0,0)の記録と赤い領域。fixture内の後続SPRITEMOVE・再設定は履歴に到達markerがなく、移動後・位置変更後は未観測。 | [ERB](cases/gui-sprite-position-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-sprite-position-01/emuera.config) · [Native](cases/gui-sprite-position-01/native-history.bin) · [画像1](cases/gui-sprite-position-01/images/phase1-crop.png) |
| `gui-draw-copy-mask-01`：GDRAWG、GDRAWSPRITE、白マスクのGDRAWGWITHMASKとGSETCOLORは各1。履歴の4点は画像内部値で、縮小クロップの赤・緑・青領域とは観測軸が別。白い1点、全画素、透明度境界は画面から確定しない。 | [ERB](cases/gui-draw-copy-mask-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-draw-copy-mask-01/emuera.config) · [Native](cases/gui-draw-copy-mask-01/native-history.bin) · [画像1](cases/gui-draw-copy-mask-01/images/draw-crop.png) |
| `gui-animation-01`：アニメ作成・2 frame追加・timer・背景設定の返値は1。保存画像にはシアンと黄色の領域があるが、個別receiptはなく、同一processでの連続性・切替順序・周期・正確な撮影時刻は画像だけでは確定しない。 | [ERB](cases/gui-animation-01/ERB/SEARCHBOUND01.ERB) · [config](cases/gui-animation-01/emuera.config) · [Native](cases/gui-animation-01/native-history.bin) · [画像1](cases/gui-animation-01/images/frame-a-crop.png) · [画像2](cases/gui-animation-01/images/frame-b-crop.png) · [画像3](cases/gui-animation-01/images/frame-c-crop.png) |

`cases.json`の各画像にはcapture記録の有無を明記します。取得記録のある画像は取得前後UTC・phase・SHAを要約し、入力イベント発生時刻とは扱いません。画像のファイル名はその内容や時系列の証明ではありません。

## 保存bytesと検証

`native-history.bin` は元ログの無改変bytesです。UTF-16 BOMとして読んでください。ERBと設定も元bytesのcopyです。実行前後の入力SHAとcopy時SHAを照合しました。取得履歴・画像・hashだけで、第三者環境の再実行や作者の真正性を証明しません。

このディレクトリで次を実行すると、含まれるファイル集合とSHAを検証できます。manifest自体のSHAは信頼する別経路から照合してください。

```text
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root gui=.
```

## 権利と制約

[Emueraに同梱されていたライセンス原文](LICENSES/Emuera1824-v24-license-original.txt)を参照。基準実装から得た表示・履歴の出典を示すもので、調査fixture・文書・新規コード等の著作権者や利用許諾を一括で確定するものではありません。原ZIPや実行体は非同梱であり、原ZIP同伴用NOTICEはこの配布単位の同梱物を説明するものではありません。公開可否は別途確認が必要です。
