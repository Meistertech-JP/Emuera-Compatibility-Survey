# SPRITEMOVEの有限なAPI提供状況と保存済み観測

[English](README.md)

`expression_function:SPRITEMOVE` と `method_as_command:SPRITEMOVE` は別のtyped keyです。共有ADAPTERの配列位置、親MATRIXの行、各2ケース、各ケース固有のfixture・Native 2回・PyEmuera stdout/stderrを区別します。対象の有限受入はどちらも`documented_difference`で、公開版との値一致を意味しません。

Native側の登録・シグネチャ・命令形の結果代入規則は、保存されたソースに基づく**静的根拠**です。Nativeの命令形はInt64戻り値を`RESULT`へ代入し、関数形は式として値を返します。これは公開版での実行観測ではありません。公開版の関数形は記録された実行時`E_FUNCTION`、命令形は読込時`E_LOAD`です。Nativeの選択状態は保存済みrawによる観測として別に扱い、公開版の正常実行や値・画像・ライフサイクルの一致を推定しません。Native自然終了とGUIピクセルは未観測です。

この資料には元の全台帳、原実行receipt、設定、エンジン、描画用BMP・CSV、元ソースアーカイブは含まれません。このディレクトリ単体では過去の入力・素材と完全な実行条件を復元できません。source SHAとJSON pointerは元資料の位置を示しますが、非公開原票にアクセスできない第三者は、元データとの対応を直接確認できません。歴史上の実機動作、作者・権利、全75対象への適用も証明しません。

```sh
python3 -I -B verify.py --manifest-sha256 "$(cat manifest.sha256)"
python3 -I -B test_negative.py --manifest-sha256 "$(cat manifest.sha256)"
```

manifestのSHAは信頼できる別経路と照合してください。同梱のSHAは署名ではありません。fixtureとログは原バイトを保持し、各原SHAと派生SHAはmanifestにあります。

## 検証と配布上の表示

検証器はNativeログの折り返されたOxx行を復元し、各ケースの保存済み2ログについて、選択状態の全項目とRESULTSを照合します。保存済み形式に限定し、不明・解析不能な値は成功扱いせず検証失敗にします。これは保存記録の整合性であり、過去の実行、GUI画素、公開版との値一致を証明するものではありません。非同梱原資料はハッシュのみでは独立に内容を認証できません。

このprojection単体には原設定、receipt全文、描画用BMP・CSV、エンジンを含みません。リポジトリ内には、この4ケースの記録設定と同一SHAの [harness/fixtures/emuera.config](../../harness/fixtures/emuera.config) がありますが、この証拠ディレクトリの同梱物ではありません。合成BMP・CSVも本projectionにはありません。

Emuera・PyEmueraのライセンスと表示先、配布単位ごとの要件、調査成果の未確定な権利方針は [NOTICE.ja.md](NOTICE.ja.md) を参照してください。参照先のlicense/NOTICE本文は本projectionにはありません。信頼できる別経路のmanifest pinが必要で、検証器は同梱checksumとの整合も確認します。

選択観測は元々ケース台帳から転記して生成されたものです。この版の検証器は、その保存済み値をNative rawと再照合します。ケース記録の元の由来注記は生成当時の方法を示し、現在の検証能力を否定するものではありません。4種類のケースID、正確な項目キー、真偽値や小数を除く整数型も検証します。
