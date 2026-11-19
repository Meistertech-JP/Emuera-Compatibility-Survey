# Emuera互換性調査

[English](README.md)

オフラインでは、展開したフォルダーの [`index.html`](index.html) をブラウザで開くと、クリックできる入口からリファレンスへ進めます。

歴代Emueraの配布アーカイブ208件の保全目録と案内は、[preservation/](preservation/README.ja.md)にあります。

Emuera互換エンジンを対象とする、証拠に基づく独立した互換性調査です。初回データはEmuera 1.824 +v24とPyEmuera 3.0.0を有限範囲で比較した記録です。EmueraはERBとCSVで作成されたバリアントを実行します。このプロジェクトは言語や命令の選択した挙動を調べます。本家の観測を、今後のPyEmueraの互換性修正・回帰検証と、他の互換実装の開発に役立つ参照資料として残します。

当時の台帳には型付きの主対象694件、主シナリオ2,898件、補助16項目、別枠の構文114ケースが記録されています。ソース調査の完了は、調査時に定めた範囲に限ります。台帳には有限範囲の一致・差異、未対応の挙動、未確定の観測を残しています。登録モードはケースの実行条件を表し、同じ実行記録に複数のケースが対応する場合があります。

この候補では、中立索引、保存観測、選択した比較を行うハーネスを参照できます。調査全体の過去の実行と対象判定を独立に再現できることは確認されていません。[旧形式の証拠参照](docs/ja/results.md#旧形式の証拠参照)では、226対象の2,476参照について、原バイトと派生物の区別、加工の理由と対応を確認できます。追加選定した比較票・原ログ・fixture等の[978資料を全文HTMLで閲覧](evidence/legacy226-restored/index.html)できます。

- [命令リファレンスと保存観測を検索](docs/survey-browser.html)。694対象を機能ジャンル・対象種別・比較判定・検索で組み合わせて絞り込み、機能・構文・使用例・期待効果を日英で読めます。保存画面は「画像を固定」で画面内に表示したまま、本家とPyEmueraの比較、3,359件の検証要件の日本語訳、同梱された出力・診断を読み進められます。
- [リファレンスの使い方と再生成](reference/README.ja.md)・[用語集](reference/glossary.html)・[旧OSDN公式Wikiと保存資料の調査](reference/SOURCES_ja.md)
- [調査結果の読み方](docs/ja/results.md)・[選択資料のオフライン検証](docs/ja/offline-validation.md)
- [本家とPyEmueraの観測結果の例](docs/ja/observations.md)
- [本家の保存観測を検索](evidence/native-oracle-20261117/docs/native-oracle.html)（[使い方と制限](evidence/native-oracle-20261117/docs/native-oracle.ja.md)）
- [PRINTVKW・PRINTVDWの待機解除後の観測](evidence/wait-release-20261117/README.ja.md)
- [PRINTVKW・PRINTVDW：空文字の待機と後続項のエラー](evidence/wait-c15-20261117/README.ja.md)
- [グラフィック・スプライトAPIの本家保存観測](evidence/graphics-native-saved-20261117/README.ja.md)
- [画像系38ケースの本家観測](evidence/graphics-38-cases-20261117/README.ja.md)
- [本家GUIの画像・背景・ボタンの観測](evidence/graphics-gui-observations-20261117/README.ja.md)
- [再実行で観測された式・入力・診断](evidence/new-replay-20261116/public/README.ja.md)
- [データと検証方法](results/README.md#日本語)
- [694対象・要件と選定証拠の追跡](evidence/694-target-trace-20261117/README.ja.md)
- [694対象の本家ソース位置に関する静的索引](evidence/native-source-694-static-20261117/README.ja.md)
- [登録2,898ケースの記録と保留](evidence/case-register-2898-20261117/README.ja.md)
- [486ケースの保存観測を検索](evidence/case-observation-recovery-20261117/README.ja.md)
- [ハーネスの使い方](harness/README.ja.md)
- [代表的な差異](differences/representative-20261116/README.ja.md)
- [記録された差異のケース索引](differences/catalog.json)
- [129対象の保存観測の限定検索](differences/saved-observation-lookup-20261117/README.md#日本語)
- [TWAIT 0,1の保存観測](evidence/twaitzero-observation-20261117/README.ja.md)
- [外部保存記録：数値・文字列の29ケース](evidence/external-scalar-29-package-20261117/README.ja.md)
- [外部保存記録：式・PRINT・診断16ケース](evidence/external-additional-16-package-20261117/README.ja.md)
- [代入・演算子23ケースの保存観測](evidence/operator-265-20261117/README_ja.md)
- [FINDELEMENT・FINDLASTELEMENT：文字列配列64条件](evidence/find-element-string-64-20261117/README_ja.md)
- [PRINTDATA系61ケースの保存観測](evidence/printdata-61-20261117/README.ja.md)
- [保存観測183ケースの索引](evidence/observation-adapter-183-20261117/README.ja.md)
- [CSV数値系45ケースの保存観測](evidence/csv-numeric-45-20261117/README.ja.md)
- [文字列・CSV・Unicodeの96ケースの保存観測](evidence/remaining-96-20261117/README.ja.md)
- [CSV文字列・配列の51ケースの保存観測](evidence/selected-51-20261117/README.ja.md)
- [CALL・JUMP・表示・LISTの28ケースの保存観測](evidence/target-priority-28-20261117/README.ja.md)
- [PRINT系82ケースの共有記録](evidence/print-kd-shared-82-20261117/README.ja.md)
- [PRINT SINGLEの保存観測：10条件](evidence/normal-observation-access-20261117/README.ja.md)
- [表示状態21ケースの共有記録](evidence/display-state-21-20261117/README.ja.md)
- [演算子6ケースの保存記録](evidence/operator-normal-6-20261117/README.ja.md)
- [表示状態の命令形式15ケース](evidence/method-display-state-15-20261117/README.ja.md)
- [背景操作24ケースの保存記録](evidence/console-background-24-20261117/README.ja.md)
- [入力・画面状態16ケースの保存記録](evidence/platform-input-16-20261117/README.ja.md)
- [数値複合代入10ケースの共有記録](evidence/compound-assignment-10-20261117/README.ja.md)
- [8資料群・101ケースの保存記録](evidence/multi-group-101-20261117/README.ja.md)
- [6資料群・72ケースの保存記録](evidence/multi-group-second-72-20261117/README.ja.md)
- [LINEISEMPTYの受入記録と旧ハッシュ不一致](evidence/lineisempty-acceptance-20261117/README.ja.md)
- [旧受入復元票40対象の索引](evidence/parent-restoration-40-20261117/README.ja.md)
- [調査方法・範囲・環境](docs/ja/method.md)
- [固定環境と依存物](manifests/environment.json)
- [基準アーカイブと同伴NOTICE](vendor/emuera/README.ja.md)
- [構成物の権利表示と出典](LICENSES/README.ja.md)
- [選定済みファイル集合の検証](tools/FILE_SET_MANIFEST.ja.md)
- [旧形式証拠の限定的な読取り](tools/LEGACY_EVIDENCE.ja.md)

`python -B tools/query.py SET` で対象名またはケースIDを検索できます。保存観測の対象種別を指定する場合は、例えば `python -B tools/query.py structural_syntax:PRINTDATA` を使います。一部のケースでは別途収録した証拠も表示します。共有batchと未到達の区別は検索結果に残り、検索結果自体は実行ログの独立検証を意味しません。

ケースの条件や選択観測を直接読むには、[case readerの使い方](tools/CASE_READER.ja.md)を参照してください。元の判定と未表示欄も確認できます。

486ケースの保存観測に該当する場合、`case_observation_recovery_links` は同梱記録のファイルと行へのリンクを返します。元のrawやsource記録はその資料に含まれません。

`--kind` はtyped対象や一部の証拠欄を絞りますが、case IDで一致する `cases` 欄は絞りません。終了コード0だけで指定kindの一致を判断せず、各欄の対象と件数を確認してください。例えば `FONTSTYLE_NEG1 --kind expression_function` では旧復元欄が空でも `cases` に命令のcaseが残ります。

C196追補と補助索引の整合性エラーでは、通常の検索は終了コード2を返します。`--partial` の対象となるエラーでは、該当結果を除き、`INCONSISTENT` と `PARTIAL` を表示して残りの結果を返します。終了コードは3です。各資料の状態は個別のavailability欄で確認してください。[調査結果の読み方](docs/ja/results.md)に本家の保存観測索引の例があります。

`parent_restoration_40` のcase ID検索は旧復元票に記載されたcaseが対象です。例えばFONTSTYLEの後続票caseは通常の `cases` 欄で検索し、旧復元欄の情報は `command_or_syntax:FONTSTYLE` のようにtyped対象から辿ってください。旧票と後続票の判定は別々に記載されています。

`query.py` はUTF-8のJSONを出力します。Windows PowerShell 5.1とPowerShell 7でパイプから受け取る場合、受信側もUTF-8にします。リポジトリのルートで次を実行すると、設定は処理後に元へ戻ります。

```powershell
$previousEncoding = [Console]::OutputEncoding
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $json = (python -B tools/query.py expression_function:SUBSTRINGU) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw "query.py failed ($LASTEXITCODE)" }
    $data = $json | ConvertFrom-Json
} finally {
    [Console]::OutputEncoding = $previousEncoding
}
$data
```

`$data` はJSONから変換したオブジェクトです。出力を他のプログラムで受け取る場合もUTF-8として読み取ってください。


主シナリオには、当初の区分が未検証の99件と、中断・証拠不備等の17件が残っています。後続調査では、この116件と型付き対象の有限範囲の要件との関係を整理しました。対象単位の判定と当初のケース単位の区分は、[調査結果の読み方](docs/ja/results.md)でそれぞれの内訳と根拠を確認できます。

この調査はPyEmueraとは独立し、[環境記録](manifests/environment.json)に示した版を比較対象とします。独自の検証資産と編集部分には[MITライセンス](LICENSE)を適用します。第三者素材の出典と再利用条件は[構成物の権利表示](LICENSES/README.ja.md)に記載しています。

## 証拠補助索引

固定された補助索引は `selected_evidence_links` から、[演算子24ケース](evidence/operator-264-20261117/README.ja.md)、[文字列配列検索64条件](evidence/find-element-string-64-20261117/README_ja.md)、[代入・演算子23ケース](evidence/operator-265-20261117/README_ja.md)、[外部保存16ケース](evidence/external-additional-16-package-20261117/README.ja.md)、[外部保存29ケース](evidence/external-scalar-29-package-20261117/README.ja.md)の記録へ案内します。登録case IDやtyped targetで検索できます。短い別名は複数の資料群で重なることがあるため、完全な登録case IDやcollectionを確認してください。条件や対象役割が同じ実行記録を共有する場合もあるため、リンク数を起動回数として数えないでください。

`TWAITZERO01` または `command_or_syntax:TWAIT` の検索からも、[TWAIT 0,1の保存観測](evidence/twaitzero-observation-20261117/README.ja.md)へ辿れます。

`supplemental_evidence_availability` は索引・各資料群・索引が対応する日英の読み物の状態を分けて示します。operator264の読み物は両方が記録SHAと一致した場合に各ケース結果から該当節へ辿れます。対応する読み物を索引で提供しない資料群では `NOT_PROVIDED` となり、各資料群のREADMEは上記リンクから参照できます。索引と導入markerの両方がない場合は `NOT_INSTALLED`、索引だけの欠落は不整合です。両方が失われた場合は未導入との区別がつきません。破損・一部欠落は通常検索を失敗させます。`--partial` は独立して検証できた他結果を保持し、終了3を返します。共通helperはimport前にpin照合し、不整合なら終了2です。受入行へのcase掲載は対象完了や命令本体到達を意味しません。各資料の元記録や未同梱部分は、リンク先の制限を参照してください。

