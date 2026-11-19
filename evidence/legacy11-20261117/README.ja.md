# 保存済み11ケースの限定資料

[English](README.md)

この資料は、旧IDと登録IDの対応が原台帳に明記された11ケースを扱います。ケースごとにfixture・Native 2回の原ログ・PyEmuera stdout/stderr・選択した比較結果を保存しています。同一ハッシュの別実行も別modeとして保持し、他ケースの証拠を代用していません。元原票のcase ID、typed key、対象の有限受入、各ケースの局所判定と適用範囲は区別しています。

正常継続、診断差、Nativeのみ継続、未到達分岐、別形式の状態比較を別の規則で扱います。特に未到達分岐の一致は対象命令の実行成功を意味しません。Nativeの自然終了は未観測です。

245系列の8ケースの `target_runtime_entered` はfixtureの `dead` 条件から導出された値であり、保存出力と併せて分岐の扱いを示します。エンジン内部メソッドへの進入を独立にトレースした計測値ではありません。

親受入と各ケースの局所判定は別です。ADDCOPYCHARAの `single`・`dead_hole`・`dead_string` は選択した親受入票のcase_idsに含まれず、親の `accepted` はその3件を個別承認した意味ではありません。COPYCHARA controlはcase_ids外で親のaccepted_scopeに記載されています。STRLEN trailingの `finite_remaining_proof` は過去の親レビューで、後続条件を含む対象の最終 `documented_difference` とは別です。各 `requirement_ids` は参照関係であり、単一ケースで要件全体を充足した証明ではありません。

Python 3の標準ライブラリを使い、このディレクトリから実行します。

```powershell
python -I -B .\verify.py --manifest-sha256 (Get-Content .\manifest.sha256 -Raw).Trim()
python -I -B .\test_negative.py --manifest-sha256 (Get-Content .\manifest.sha256 -Raw).Trim()
```

`manifest.json`に原SHA・対象ごとの元JSON pointer・派生SHAを記録しています。原台帳、完全な親レビュー、完全な実行receipt、設定原本、エンジン本体はこの証拠ディレクトリに含まず、第三者は原票を直接照合・再現できません。候補の別の[設定ファイル](../../harness/fixtures/emuera.config)は全33 modeの記録と同じSHA-256 `f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc` を持ちます。SHA一致は当時の実行や設定の意味、全実行条件の同一性の証明ではありません。

verifierは `manifest.sha256` の書式と同梱pin・外部指定pin・manifest実SHAの一致も確認します。上のコマンドは同梱pinによる簡便な整合性検査です。独立した識別には、信頼できる別経路のmanifest SHAを指定してください。同梱SHAは署名ではなく真正性を証明しません。

## 出典と再利用条件

Nativeログ・診断の参照先は[Emueraライセンス原文](../../LICENSES/Emuera1824-v24-license-original.txt)と[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)、PyEmuera出力の参照先は[PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)です。[候補のライセンス案内](../../LICENSES/README.ja.md)も参照してください。この資料だけを再配布する際は必要な表示とリンク先を配布単位に同伴してください。fixture・新規コードを含む調査成果全体の権利主体・利用条件は未確定であり、PyEmueraのMITを全成果に自動適用しません。

この資料は11ケースの保存済み記録の限定検証であり、対象全体や694対象の互換性、歴史上の実機起動の真正性、素材の公開権利を証明しません。
