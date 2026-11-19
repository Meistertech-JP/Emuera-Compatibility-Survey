# 調査データの読み方

[English](../en/results.md) | [概要](../../README.ja.md)

[オフライン検証の手順](offline-validation.md)では、選択された資料の検証コマンドと確認範囲を案内します。

[本家とPyEmueraが返した結果の例](observations.md)から、条件と保存出力を確認できます。

[保存観測の限定検索](../../differences/saved-observation-lookup-20261117/README.md#日本語)では、選定された129対象について、同梱記録の値・case・参照位置を検索できます。個別fieldが未収録の対象も状態を表示します。

[486ケースの記録](../../evidence/case-observation-recovery-20261117/README.ja.md)は、ケースIDまたは対象名で検索できます。うち95ケースの `recovered` 欄に保存観測の記述があり、残り391ケースでは同欄が空です。元のrawやsource記録は含まれないため、同梱記録から当時の実行を独立に検証できる範囲には限りがあります。

[STRFINDUの開始位置4条件の保存観測](strfindu-boundary.md)では、選択した入力と保存結果を確認できます。元fixtureとrawは含まれません。

[`TWAIT 0,1` の保存観測](../../evidence/twaitzero-observation-20261117/README.ja.md)では、本家の画面とPyEmueraの診断を、それぞれの実行条件と未観測範囲とともに確認できます。

[複合代入の末尾カンマに関する保存観測](../../evidence/compound-trailing-comma-20261117/README_ja.md)では、2ケースの本家出力とPyEmueraの構文診断を確認できます。

[`DELCHARA` の3条件の保存観測](../../evidence/delchara-diagnostics-20261117/README.ja.md)では、本家の診断原文とPyEmueraの診断、比較した状態・停止位置を確認できます。

[`LOADGLOBAL` の切り詰め保存データの観測](../../evidence/loadglobal-corrupt-20261117/README_ja.md)では、各エンジンの異なる形式で作った入力と選定した読み込み結果を確認できます。

[停止後の状態に関する保存記録](../../evidence/stopped-state-observations-20261117/README_ja.md)では、本家で直接読み取った値と、PyEmueraの保存状態・実装から推論した値を区別しています。元の観測rawは同梱されません。

[PRINTDATA・STRDATAの文字列状態とログの折り返し](printdata-local.md)では、本家ログ・PyEmuera出力とソースからの推論を分けて説明します。

[演算子24条件の保存出力](operator-264-observations.md)では、登録ケースごとに本家とPyEmueraの出力・診断を読めます。これらは既存台帳のケースであり、新規件数として加算しません。

共通の機械可読データは [`results/survey.json`](../../results/survey.json) です。`targets` は `kind` と `name` の組で対象を区別し、関係ケースIDと有限範囲の判定を記録します。`main_scenarios` は主登録2,898件の元の区分を保持します。`supplemental_items`、`supplemental_modes`、`grammar_cases` は別の母集団です。登録モード数はプロセス起動数でも固有の不具合数でもありません。

[対象・要件の追跡索引](../../evidence/694-target-trace-20261117/README.ja.md)は、694対象の3,359要件と、同梱資料で利用できる選定証拠を結びます。元の受入票が非公開の箇所はその状態を示し、要件が掲載されているだけで原観測を独立検証できるとは扱いません。

プロジェクト直下から `python -B tools/query.py <対象名またはケースID>` で完全一致検索できます。`python -B results/verify.py` は中立データとファイルハッシュを検証します。名前の一致だけで原証拠や対象到達を推定するものではないため、各ケースの証拠と範囲を確認してください。

検索結果を読む例（コマンドはリポジトリのルートで実行）:

- `python -B tools/query.py 'assignment_syntax:*='` はtyped対象と関連caseを返します。関連roleをそれぞれの実行到達とせず、例として[末尾カンマの2ケース](../../evidence/compound-trailing-comma-20261117/README_ja.md)のfixtureとmode別観測を確認できます。
- `python -B tools/query.py TWAITZERO01` は `cases`、`case_register_projection` と、`selected_evidence_links` 内の[TWAIT 0,1の保存観測](../../evidence/twaitzero-observation-20261117/README.ja.md)へのリンクを返します。`runtime_observation_context` の `NO_RUNTIME_OBSERVATION_KEY_FOUND` はcase投影内のキーに関する表示で、他のbundleに観測がないことを意味しません。
- `python -B tools/query.py E143E` の `case_register_projection` にある `detail_record` は、[cases.jsonl](../../evidence/case-register-2898-20261117/cases.jsonl)のcase行を示します。同梱欄には条件と比較範囲がありますが、この検索結果では詳細欄を出力せず、元evidence・reviewは保留されています。原資料を確認するには非同梱の原票が必要です。これは他の保存証拠の不存在を意味しません。
- ケースの条件・選択観測・未確認範囲を直接読むには、[case reader](../../tools/CASE_READER.ja.md)にケースIDと信頼済みmanifest SHAを指定します。表示は保存された投影であり、原rawの真正性や再実行を証明しません。
- 構文の `COLON_NORMAL_COMPAT_RAND_YES` を検索すると `representative_evidence` と `extra_evidence_links` が得られます。補助の `SUP_LABEL_DOLLAR_DUPLICATE_NO_20261115` では `extra_evidence_links` の `manifest` と `manifest_pointer` から[保存観測](../../evidence/syntax-supplemental-20261117/README.ja.md)のcaseへ進めます。選定bundleにはprobe本文と元receiptなどの非同梱部分があり、全構文・補助ケースが同様に辿れるわけではありません。

当時のシナリオ台帳には、局所一致1,711件、局所差異1,071件、未検証99件、中断・証拠不備等17件が記録されています。同じ対象に複数の区分のケースがあり得ます。対象単位の判定は別集計で、有限範囲の一致201件、記録済み差異294件、範囲を限定した差異199件です。同じ原因による差異を複数含む場合があります。

元の未検証・中断等116件は、過去の失敗・未観測を保持した68件、有限比較の範囲外として未観測を保持した42件、当初の対応関係が不明だった6件に整理されました。最後の6件は後続調査で有限受入範囲との対応付けを完了しています。この対応付けは実測成功を意味しません。後続ケースに基づいて有限受入を行った場合も、元ケースの結果を書き換えず、別の実行として扱います。

42件のうち画像系38件については、[元の本家保存記録と限定的な観測](../../evidence/graphics-38-cases-20261117/README.ja.md)があります。そのうちGCLEARの2件には、別の後続本家GUI試行も記録されています。これらは元の有限比較上の区分を変更するものでも、全条件や両エンジンの一致を示すものでもありません。

[`differences/catalog.json`](../../differences/catalog.json) は記録された差異の索引であり、根本原因の診断ではありません。現在、4件について[代表的な観測](../../differences/representative-20261116/README.ja.md)を添付しています。各typed keyから条件、両側の原観測、受入までの全経路は、この資料には揃っていません。索引の存在だけを、元結果の第三者再現と扱わないでください。

`catalog.json` と `survey.json` のルートにある `evidence_availability` は元のsurvey投影の状態で、後から同梱した資料の現況一覧ではありません。`python -B tools/query.py OPCONT268_strcmp-ge` の `native_oracle_observations` は[33条件の選択観測](../../evidence/native-oracle-20261117/evidence/operator-268-20261117/README.ja.md)への出典とJSON pointerに加え、固定pinを照合した選定索引にある `selected_condition` と `selected_observations` をそのまま返します。これらは選定索引内の値であり、元sourceとの意味一致を検証したものではありません。これは2回のNativeと1回のPyEmueraの共有実行から選んだ投影で、元fixture・config・rawは非同梱です。検索結果の `native_oracle_availability` はこの113行の索引だけの状態であり、該当なしは他の資料全体に証拠がないことを意味しません。collectionディレクトリがない場合は `NOT_PRESENT`、空ディレクトリや必要なファイルの欠落・不整合は `INCONSISTENT` です。既存caseが見つかると終了コードが0でもcollectionは不整合になり得ます。`--partial` もこのcollectionの不整合を終了コードに反映しないため、必ず `native_oracle_availability.state` を確認してください。

`STRLEN`の旧ID `PARENT246_strlen-control` と登録ID `ARGBOUND246_strlen-control` は、[保存済みの選定証拠](../../evidence/strlen-control-20261117/README.ja.md)へつながります。局所ケースの一致と対象全体の差異は別の判定です。`results/evidence-index.json` はこのような選定済みケースの参照であり、全ケースを網羅しません。

[29ケース一括実行の派生証拠](../../evidence/main29-20261117/README.ja.md)は、元の登録IDと公開用IDの両方から検索できます。そのうち12ケースは、ケース台帳では対象に関連付いている一方、最終の対象受入行のケース一覧には掲載されていません。索引の `acceptance_case_listed` で区別し、受入根拠だったと推定しないでください。

構文16ケースと補助8ケースの[選定済み証拠](../../evidence/syntax-supplemental-20261117/README.ja.md)は `results/extra-evidence-index.json` から参照できます。構文と補助は主694対象と別の集計です。

API関連75対象については、[共有された静的根拠と親ケース参照](../../evidence/api-gap75-static-20261117/README.ja.md)を対象名やケースIDから検索できます。これは各ケースの実測rawを確認できることや、命令形式のルーティングをその登録行だけで証明したことを意味しません。

[`PRINTDB15`の保存証拠](../../evidence/printdb15-20261117/README.ja.md)は1つの物理ケースで、`command_or_syntax:PRINTDATA` と `structural_syntax:PRINTDATA` の2つのtyped roleに関連します。2回の別実行としては数えません。

`INPUT`の有限調査では、以前の受入で対象外だった空入力時の既定値選択とechoについて、追加の2ケースを評価しました。echoは両エンジンでそれぞれ観測していますが、GUI・CLIの全表示チャネルの一致やNativeの自然終了は検証していません。追加評価前の台帳SHAを記録する旧資料と、最終台帳を混同しないでください。

`python -B tools/query.py PRINTDWEMPTY01` と `python -B tools/query.py structural_syntax:LOOP` は、それぞれ保存された限定観測を `scoped_observations` に表示します。配列・レベル・保存命令など8ケースとDO/LOOPの1ケースが対象です。`scoped_observations_availability` で各資料の状態を確認してください。原rawは含まれず、この検索によって実行を再現できるわけではありません。複数の対象に同じ共有実行が関連する場合も、別々の実行として数えません。`--case-projection-dir` を明示した検索では別の台帳と混同しないよう、この観測を返しません。

`native_source_anchor82` と `selected_51_saved` の検索では、各資料の固定manifestと検索対象の索引ファイルを照合します。導入済み資料のmanifestや索引に欠落・改変があれば検索はエラーになります。資料全体が未導入の場合は `NOT_INSTALLED` と表示します。これは索引の整合性の検査であり、資料内のすべての入力ファイルや元実行の真正性を検証するものではありません。

## 旧形式の証拠参照

当時の証拠経路監査では、型付きの694対象のうち468対象を追加の変換なしで追跡し、226対象に旧形式・配置の読み替えが必要と記録しました。226対象の当時の判定は、有限範囲の一致82件、記録済み差異69件、範囲を限定した差異75件です。読み替えの要否は証拠の形式や配置に関する区分です。

更新した[旧形式の参照索引](../../evidence/legacy226-source-locator-20261118/locator.json)では、**226対象・2,476参照**を維持しています。同じファイルや共有実行を複数の項目が参照する場合があります。参照先は各項目の `classification` で確認できます。

| 区分 | 候補から確認できるもの |
| --- | --- |
| `PUBLIC_INCLUDED` | 記録された原本と同じバイト列への候補ルート相対パス。アーカイブ内の場合は内部のメンバー名も記載します。 |
| `PUBLIC_DERIVED` | 保存観測への候補ルート相対パスとケースID、JSONポインター。確認できるのは元記録から抜粋・投影した範囲です。 |
| `PRIVATE_RETAINED` | 原本を非公開で保全した参照項目。原本の保管場所やバイト列は参照から取得できません。 |
| `MISSING_OR_UNVERIFIED` | 原本を参照できないか、凍結時の一覧と既存のハッシュでバイト列の一致を確認できなかった参照項目。 |

これらの区分は、候補から確認できる資料の範囲を示します。当時の実行の再現や対象判定の確認には、入力、実行証拠、判定根拠が必要です。候補だけで過去の調査全体を独立に再現できることは確認されていません。配布物の権利条件は[権利表示](../../LICENSES/README.ja.md)と[基準配布物の案内](../../vendor/emuera/README.ja.md)に従います。

[旧形式のリーダー対応記録](../../evidence/legacy226-adapter-index-20261118/README.ja.md)には、部分確認35件、未対応169件、入力不整合18件とあります。この内訳で確認できるのは226対象のうち222件です。残り4件の区分は記録から確定できません。対応する形式と確認範囲は[限定リーダーの説明](../../tools/LEGACY_EVIDENCE.ja.md)を参照してください。

[旧受入資料の対応索引](../../evidence/legacy-acceptance-269-20261117/README.ja.md)は別の基準で抽出しています。最終台帳に `current_acceptance` 欄がない269対象のうち、205対象で旧資料への参照を識別し、64対象は未特定と記録しています。[既定色・表示状態と演算子の選択観測](../../evidence/legacy50-selected-observations-20261117/README.ja.md)では、27対象の後続の条件と観測値を確認できます。これらの対象の旧受入原票は非同梱です。

現在の可用性は旧形式索引の分類と[個別審査資料](../../evidence/legacy226-restored/README.ja.md)を参照してください。過去の投影に残る非同梱の表記は投影時点の状態です。今回追加した978資料には、受入票・比較票・本家とPyEmueraの原ログ・入力と依存物が含まれます。原判定と新しい公開可用性は別の属性として保持しています。
