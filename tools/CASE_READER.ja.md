# 固定された case 投影の表示

[English](CASE_READER.md)

`case_reader.py` は既存の case register を case ID で検索し、typed targets、元の `scenario_verdict`、投影状態、観測・比較、fixture・初期状態、入力・実行条件、制限と、選択した追加観測を表示します。Python 3.10 以上と標準ライブラリが必要です。外部エンジンやネットワークは不要です。

リポジトリのルートから、対象 register と、信頼できる別経路で得た **manifest.json 自体**の SHA-256 を指定します。

```powershell
python -I -B tools/case_reader.py PRINTVW_POSTWAIT01 --register-dir evidence/case-register-2898-20261117 --manifest-sha256 <TRUSTED_MANIFEST_SHA256>
```

別の配布物では対象に合わせてパスと SHA を変更してください。ID は大小文字を区別しません。`--lang ja` が既定、`--lang en` は英語ラベルです。`--json` は UTF-8 JSON を出力し、`--lang` によって JSON の内容は変わりません。対象や欄の元値は翻訳しません。

`targets` は `kind` と `name` を含む元の構造を表示します。v2 の `related_cases` は欄が存在するときだけ表示し、`null` を含め元値を保ちます。v1 では表示しません。関連先を追跡して結果を転記せず、未観測・未検証を成功に変換しません。終了 0 は検索と検査が成功したことを示し、case の実測成功や互換性を示しません。未知の case ID、入力不正、欠落、整合性不一致などは終了 2 で、結果を出力しません。

追加観測では、存在する `native_corrected_observations`、`native_selected_observations`、本家・publicのmarkers、選択snapshot、比較軸、停止行、選択traceなどを元の値で示します。`runs` と `new_modes` は実行モード、観測、診断、停止・未観測などの選択欄を表示します。たとえば `runs` の `marker_raw_line_map` や `targets` はモードごとに残し、`new_modes` の `channels` では保存済みテキストとencodingを表示します。実行一覧の対応しない構造は表示せず通知します。

`note` は一括表示しません。現在は、最終fixture hashが適用されるrunを限定する `Only accepted-* runs use the final fixture hash.` という確認済みの文字列だけを、case IDに関係なく完全一致で表示します。これは元投影の条件を示すものであり、CLIがそのhashやrunの対応を独立検証したことを意味しません。その他の `note` は値を出さず、省略を通知します。

**表示は投影の全欄ではありません。** 未選択の evidence・review・実行path等の値は表示せず、`表示しない欄と理由` にフィールド位置と理由を示します。非公開pathと判定した表示対象欄もそこに列挙します。JSONでは `additional_observations` と `omitted_fields` を使い、理由コードは `not_selected`、`private_path_or_reference`、`unsupported_runs_structure` です。位置は元の `cases.jsonl` に対するパスで、安全に表示できない欄名は `<redacted-field-name>` とします。表示対象外の欄にも観測が含まれる可能性があり、省略は観測が存在しないことを意味しません。必要に応じ、指定した投影の該当caseを確認してください。

対応 schema は `case-register-neutral-screened-draft-v1` と `case-register-neutral-screened-draft-v2` です。manifest の SHA を照合し、記載された両 README と `cases.jsonl`・`core.jsonl` のサイズと SHA、レコード数、ID の重複、全行の core/detail 対応などを検査します。非対応のファイル構成や、検査で発見された破損は拒否します。全フィールドの意味や公開適否を検証するものではありません。

同じ配布物から測った manifest SHA は、配布元や manifest の真正性を証明しません。信頼できる別経路で取得した SHA と実行する CLI 自身を照合してください。

構造化値や `$case_projection_withheld`、文字列中の `[WITHHELD]` は元のまま表示し、欠落欄の `{"$field": "not_present"}` と区別します。非公開 path と思われる参照を含む表示対象欄は、欄全体を `{"$display_omitted": "private_path_or_reference"}` に置き換えます。この検出は網羅的な privacy 審査ではありません。

元 raw・receipt・原票の真正性検証や過去実行の再現は行いません。投影には個別確認が必要な部分があり、表示可能なことは権利・privacy や公開の承認を意味しません。
