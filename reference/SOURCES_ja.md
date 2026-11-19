# 出典と採用範囲

[English](SOURCES.md) / [機械可読台帳](sources.json)

説明と例は独自執筆です。この台帳は資料の所在と採用範囲を示すもので、取得本文を再配布するものではありません。第三者の文献・コードの権利を本件のMITで上書きしません。確認日は2026年11月18日、取得時刻は台帳でUTC表記です。

## 共通ID

- SRC-NATIVE-V24：同梱vendor ZIPの内包原ZIPにあるEmuera1824+v24ソース。外側・内側archive、member、各SHA-256、1始まりの行番号で特定します。各entryのpathはソースルートsrc1824/Emuera/からの相対パスです。ソース読解は実機観測とは別です。主たる許諾と第三者別条件はvendorのNOTICE類を参照します。
- SRC-SURVEY-3：既存の有限調査・Native/PyEmuera 3.0保存観測。対象、fixture、版、実行モード、結果、証拠locatorの範囲で採用します。この調査で実機を再実行したわけではなく、有限一致は完全互換性を証明しません。
- SRC-NATIVE-README：同梱の本家1.824と私家v24のREADME。配布物の版、ソフトウェア著作者表示、変更履歴を確認する資料です。著作者表示からWikiの各節の執筆者は推定しません。

## 旧OSDNの保存本文

Waybackの本文を実取得し、転送後の実保存日時を記録しました。14桁日時はUTCの保存時点であり、エンジン版・執筆日ではありません。

| ID | 実保存日時 UTC | 取得タイトル |
|---|---|---|
| SRC-OSDN-FRONTPAGE | 20230303163321 | Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXCOM | 20230303163405 | excom - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXMETH | 20230303163405 | exmeth - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXOP | 20230303163446 | exop - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXFUNC | 20230303163353 | exfunc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-USERVARS | 20230303163405 | UserVars - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-RESOURCES | 20230303163405 | resources - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXHTML | 20230303163436 | exhtml - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXTENDED | 20230303163441 | extended - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXETC | 20230303163405 | exetc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |

現在のOSDN FrontPageはTLSエラーでした。Waybackのexvar試行はHTTP 503で、成功した保存本文や保存日時を認定していません。CDX一覧の日時と実本文の取得結果は別々に記録しています。

## 移植・保存・権利の区別

EMEEのChangelogで旧OSDNのEmuera文書をEM+EE Wikiへ移植した旨を確認しました。旧仕様を継ぐEmuera/配下、再編されたReference/、EM+EEの新規追加・変更を区別します。移植の事実からMinorShift本人の各節執筆は認定しません。確定しない個別著者・編集者はnullです。

EMEEトップページのライセンス節にはCC BY-NC 4.0の表示と実リンクがありました。サイト全体の宣言として記録しますが、旧資料の権利者からの再許諾連鎖までは確認していません。取得本文・例の転載、逐語訳は公開候補に収録しません。テーマやアイコンのMIT/CC表示を文書本文の許諾根拠にしません。

旧OSDNと移植先の演算、関数・プリプロセッサ、ユーザー定義変数、リソース、一般記法の5組は実取得本文を比較しました。整形・編集を含む相違があり、バイト同一の保存版とは呼びません。全原改訂履歴、移植時の正確なrevision、各節の執筆者は未確認です。

Era Wikiの一覧、excom、exmeth、ERB/CSV保存ページも取得しました。excomの初回通信失敗は残し、一覧到達後の1回の再試行成功を別記録にしています。英訳・編集された保存版の記述や未確認の許諾条件を旧公式資料と一括しません。

## 版・意味論・観測の限界

旧excomのPRINT族にはver1.736と明記された条件があり、同ページに1.808や1.824の注記もあります。ページ全体を単一版の仕様とは扱いません。eramakerのERB/CSV資料自身にも現行Emueraとの差への注意があるため、古い制限をv24へ直接転用しません。

命令、式中関数、式中関数の命令呼び出しは別のtyped targetです。同名見出しがあっても引数・RESULT/RESULTS・返値・エラー条件が同じとは限りません。見出し索引と対応表は探索補助であり、source claimを自動確定しません。SETは内部代入識別子であり、直接SET呼び出しが可能な命令ではありません。

命令・式中関数・演算子・代入・宣言・制御・PRINT・INPUT・SAVE/LOAD・CSV/ERB・GUI/spriteの各領域で資料を発見しました。これは資料の存在確認であり、694対象すべての仕様を文献で網羅したという意味ではありません。GUI/spriteは本家GUIの条件付き機能として説明し、CLIだけを理由に除きません。

## 登録資料

元URL、保存先URL、節、版、確認時刻、取得結果、採用範囲・制限はsources.jsonに記録しています。本文キャッシュ、応答ヘッダー、完全索引、typed target対応表は所有者監査記録に限定しています。

| ID | 区分 | タイトル | Wayback UTC | ライセンス表示・状態 |
|---|---|---|---|---|
| SRC-NATIVE-V24 | SOURCE_CONFIRMED | Emuera1824+v24 bundled C# source | — | individual / unverified |
| SRC-SURVEY-3 | SOURCE_CONFIRMED | PyEmuera 3.0 saved finite survey and native/PyEmuera observations | — | MIT |
| SRC-NATIVE-README | DOCUMENTED_ORIGINAL | Bundled Emuera 1.824 and private Emuera1824+v24 readmes | — | individual / unverified |
| SRC-OSDN-FRONTPAGE | DOCUMENTED_ORIGINAL | Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163321 | individual / unverified |
| SRC-EMEE-EMUERA | MIRROR | Index - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-ERAGAMES-EXCOM | MIRROR | Emuera/excom - Era Wiki | — | individual / unverified |
| SRC-OSDN-EXCOM | DOCUMENTED_ORIGINAL | excom - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXMETH | DOCUMENTED_ORIGINAL | exmeth - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXOP | DOCUMENTED_ORIGINAL | exop - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163446 | individual / unverified |
| SRC-OSDN-EXFUNC | DOCUMENTED_ORIGINAL | exfunc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163353 | individual / unverified |
| SRC-OSDN-USERVARS | DOCUMENTED_ORIGINAL | UserVars - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-RESOURCES | DOCUMENTED_ORIGINAL | resources - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXHTML | DOCUMENTED_ORIGINAL | exhtml - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163436 | individual / unverified |
| SRC-EMEE-CHANGELOG-INDEX | DERIVATIVE | 変更ログ - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-REFERENCE-INDEX | DERIVATIVE | Index - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-OPERAND | MIRROR | 演算 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-EXPRESSION | MIRROR | Emueraで追加された記法 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-USER-DEFINED-VARIABLES | MIRROR | ユーザー定義の変数 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-FUNCTION | MIRROR | 関数・プリプロセッサ - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-IN-EXPRESSION-FUNCTION | MIRROR | 式中で使える関数 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-RESOURCES | MIRROR | リソースファイル - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-ERAMAKER-ERB-FORMAT | DERIVATIVE | eramakerのERB書式 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-ERAMAKER-CSV-FORMAT | DERIVATIVE | eramakerのCSV書式 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-INDEX | DERIVATIVE | Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-REPO-README-MD | DERIVATIVE | README.md | — | individual / unverified |
| SRC-ERAGAMES-INDEX | MIRROR | Emuera - Era Wiki | — | individual / unverified |
| SRC-OSDN-EXTENDED | DOCUMENTED_ORIGINAL | extended - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163441 | individual / unverified |
| SRC-OSDN-EXETC | DOCUMENTED_ORIGINAL | exetc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXVAR | DOCUMENTED_ORIGINAL | Internet Archive: Temporarily Offline | — | individual / unverified |
| SRC-ERAGAMES-EXMETH | MIRROR | Emuera/exmeth - Era Wiki | — | individual / unverified |
| SRC-ERAGAMES-ERAMAERB | MIRROR | Emuera/eramaerb - Era Wiki | — | individual / unverified |
| SRC-ERAGAMES-ERAMACSV | MIRROR | Emuera/eramacsv - Era Wiki | — | individual / unverified |
| SRC-EMEE-REFERENCE-IF | DERIVATIVE | (S)IF - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
