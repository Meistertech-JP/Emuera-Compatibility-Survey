# 参照する構成物の権利表示

[English](README.md)

[MITライセンス](../LICENSE)は、Meistertech-JPが許諾権限を持つ検証コード・補助スクリプト・テスト・fixture・文書と、台帳・索引・差異カタログ・派生データに対する独自の編集部分に適用します。第三者素材とその由来部分は、次の個別条件が適用されます。

- [`Emuera1824-v24-license-original.txt`](Emuera1824-v24-license-original.txt) は、保全したEmueraのソースアーカイブに同梱されていたライセンスの無改変コピーです。基準exe、そこから得た画面・ログ、設定テンプレートは基準配布物に関係します。ソースの対象名と追加表示は[基準配布物のNOTICE](../vendor/emuera/NOTICE.ja.md)を参照してください。`harness/fixtures/emuera.config` は記録済み設定の無改変コピーで、SHA-256を[環境マニフェスト](../manifests/environment.json)に記載しています。
- [`PyEmuera-3.0.0-LICENSE.txt`](PyEmuera-3.0.0-LICENSE.txt) と [`PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md`](PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md) は、公式PyEmuera 3.0.0ソースZIPからの無改変コピーです。第三者表示の中の「この配布物」や同梱内容の説明は、その元のPyEmuera配布物を指し、この調査候補のファイル構成とは異なります。保存した比較出力の一部には同実装の診断文が含まれます。PyEmuera自身の許諾は、同梱の第三者表示に記された別条件を置き換えません。
- 設定のラベル、ソースへの参照、診断、画面やログに含まれるエンジンの表現は、該当するエンジンとその表示に帰属します。JSONへの抽出、文字コード変換、翻訳、画面のクロップ等を施した箇所は、対応する証拠のREADMEに記載しています。エンジンに依存しない独自fixture・収録方法の説明には上記のMITライセンスを適用します。

P38のBMPは調査時に保存されたクロップです。クロップ前の全画面の原バイトは保持していません。表示にはEmuera基準実装による出力が含まれます。

## 命令リファレンス

`reference/entries-*.jsonl`、要件の日本語訳・平易な説明、用語集、表示・生成コードは、権限のある独自の執筆・編集部分に上記MITを適用します。元要件やソース・ログに含まれる第三者の表現は、その由来の条件を保ちます。

`reference/native-source/` は同梱の本家原ZIPのC#を、文字コードを解釈し行番号とHTMLエスケープを付けて閲覧可能にした派生表示です。コード内容は本家ソースに由来し、独自MITで上書きしません。各ページに元member名・SHA-256と、上記の本家ライセンス・第三者NOTICEへのリンクを記載しています。

旧OSDN Wiki、Wayback保存版、Emuera.EM+EE、Era Wikiの資料名・URL・節・取得記録は[文献索引](../reference/SOURCES_ja.md)を参照してください。文献本文のcacheや逐語訳は同梱しません。CC BY-NC 4.0の表示がある派生文書を、このプロジェクトのMITへ変更するものではありません。説明文と使用例は技術的事実を確認して独自に執筆しています。
