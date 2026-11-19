# 旧復元票の判定：40 typed対象

[English](README.md)

これはメタデータ限定の投影です。41行の復元票から40 typed対象を選び、原票に記録された作成時刻 `2026-11-14T05:05:22.763930+00:00` を示します。この時刻は復元票自体の作成時刻であり、各判定や実行の時刻とは限りません。記録された有限判定は履歴情報で、新規実行、新たな受入れ、完全互換性の証明ではありません。

[`targets.jsonl`](targets.jsonl) は1 typed対象1行です。元復元票はSHA-256で識別しますが同梱しません。`case_ids_as_recorded` は履歴票に列挙されたIDで、別途用意されたsurvey snapshot内の対象roleとの一致を確認しました。ただし独立実行、対象到達、完全な入力や全条件の受入れを示しません。232参照は218 distinct case IDで、互いに重複します。元の有限条件・receipt・raw・親レビューは非同梱です。SHAやIDだけでは、外部の読者が非同梱原票を読んだり真正性を確認したりできません。

各行の後続台帳snapshotと有限判定は、復元票の判定とは別項目です。`ledger_header_generated_utc` は台帳ヘッダーの記載であり、個別判定の確定時刻は未特定です。判定ラベルが同じでも、同じ出典・時点・条件や完全互換を意味しません。`command_or_syntax:FONTSTYLE` は旧復元票が `documented_difference`、別の後続親票と台帳が `different_scoped` です。各出典SHAと判定を分離し、片方で他方を置き換えません。後続親票の個別判定時刻はここでは確定していません。

復元票の14行では、埋め込まれたaccepted-source欄内にtyped targetが明記されています。残る26行はその**欄内**にtyped targetがありません。復元票行自体には40行ともtyped keyがあり、後続のtyped-source対応は別保管の監査対応表に基づきます。共通ファイルやSHAだけから対象roleを推測しません。元資料とprivate対応表はこの投影に含めません。

`candidate_survey` のpathは将来の配布ルート基準で、pointerは記録SHAと一致するsurveyを同一配布単位に用意した場合に限り有効です。この投影にはsurveyを含めていません。元証拠・親票本文や再現性の証明は含まず、出典・派生物・case ID・survey素材のprivacyと権利は別途確認中です。公開承認を意味しません。
