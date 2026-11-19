# SPRITESETPOSの有限なAPI提供状況と保存済み観測

[English](README.md)

`expression_function:SPRITESETPOS` と `method_as_command:SPRITESETPOS` は別のtyped keyです。共有ADAPTERの配列位置、親MATRIXの行、各2ケース、各ケース固有のfixture・Native 2回・PyEmuera stdout/stderrを区別します。対象の有限受入はどちらも`documented_difference`で、公開版との値一致を意味しません。

Native側の登録・シグネチャ・命令形の結果代入規則は、保存されたソースに基づく**静的根拠**です。Nativeの命令形はInt64戻り値を`RESULT`へ代入し、関数形は式として値を返します。これは公開版での実行観測ではありません。公開版の関数形は記録された実行時`E_FUNCTION`、命令形は読込時`E_LOAD`です。Nativeの選択状態は保存済みrawによる観測として別に扱い、公開版の正常実行や値・画像・ライフサイクルの一致を推定しません。Native自然終了とGUIピクセルは未観測です。

この証拠ディレクトリには元の全台帳、原実行receipt、設定原本、エンジン、描画用BMP・CSV、元ソースアーカイブは含まれません。配布物内の別の[設定ファイル](../../harness/fixtures/emuera.config)は記録された12モードすべてと同じSHA-256 `f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc` ですが、この資料には同梱していません。SHAの一致は当時の実行・設定の意味全体を証明しません。設定・描画素材を含む完全な実行条件はこの資料から復元できません。source SHAとJSON pointerは元資料の位置を示しますが、非公開原票にアクセスできない第三者は元データとの対応を直接確認できません。歴史上の実機動作、作者・権利、全75対象への適用も証明しません。

```sh
sha256sum verify.py
python3 -I -B verify.py --manifest-sha256 <信頼済みmanifest_SHA256> --verifier-sha256 <信頼済みverifier_SHA256>
python3 -I -B test_negative.py --manifest-sha256 <信頼済みmanifest_SHA256> --verifier-sha256 <信頼済みverifier_SHA256>
```

同梱 `verify.py` のSHA-256は `631cd4e9043926260f4e717e91c5d66347767aa540ca5186cb131ad9888f3543` です。manifestとverifierのSHAは信頼できる別経路から取得し、実行前に `sha256sum` 等の独立した手段でverifierを照合してください。上の山括弧を含む部分は値に置き換えます。Windowsでは `Get-FileHash .\verify.py -Algorithm SHA256` を使用できます。verifierは同梱 `manifest.sha256` と外部pinとmanifest実SHAの一致、固定されたsource対応とコピーbytesのSHA一致、Nativeの折返しを復元した16観測・160値を確認します。同梱SHAは署名ではなく、hashは作者・実行の真正性や権利を証明しません。

4ケースのIDは一意な期待集合とtyped key別の対応を検査します。ケース記録の8観測はそれぞれ9項目を真偽値・小数を除く整数、`RESULTS` を文字列、IDを順番どおりの文字列として検査し、計72整数と8文字列を確認します。記録値は生成時にcase registerから選択され、現在のverifierは保存済みNative rawを折返し復元して両モード分を比較します。

## 出典と再利用条件

Nativeログについて[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)と[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、PyEmuera診断について[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。NOTICEは別の原ソースZIPを説明しており、この資料にそのZIPは含まれません。調査fixture・記録・新規コードの権利主体と条件は未確定で、PyEmuera MITを調査成果全体に自動適用しません。別の配布単位へ切り出す場合は必要な表示を同伴してください。

配布物内の[ライセンス一覧](../../LICENSES/README.ja.md)と[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)も参照できます。

保存されたNativeソースではSPRITESETPOSは位置を絶対設定します。相対移動するSPRITEMOVEとは区別します。これは静的根拠です。
