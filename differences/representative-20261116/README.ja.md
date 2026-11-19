# 代表差異：有限条件での保存済み観測

[English](README.en.md) | [機械可読カタログ](catalog.json) | [証拠ファイル一覧](../../evidence/representative-20261116/manifest.json)

以下は当時の保存済み観測です。fixtureと生出力・画面を収録していますが、完全な当時の設定、起動ハーネス、エンジン配布物は含みません。独立環境での再実行は行っておらず、**再現可能とは判定していません**。Nativeの自然終了や未印字のエラー後状態も、観測されていない限り不明です。登録モード数は起動回数ではありません。

## `RAND`：`COLON_NORMAL_COMPAT_RAND_YES`

条件は `CompatiRAND:YES`。実際の[入力ERB](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/fixture/ERB/MAIN.ERB)は先に `RAND`、続いて `RAND:0` を評価します。[入力CSV](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/fixture/csv/)と、[設定から抽出した一項目](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/fixture/config-observed.json)も保存しています。設定全体の代用にはなりません。

本家の[1回目](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/native-01-emuera.log)・[2回目](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/native-02-emuera.log)は `OBS_RAND_BARE=0`、`OBS_RAND_ZERO=0` と後続の `AFTER`・`DONE` を出力しました。公開版の[標準出力](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/public-stdout.bin)は `BEFORE` までで、[標準エラー](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/public-stderr.bin)には22行目 `E_ARGUMENT: RAND:n requires n > 0` が記録されています。このケースの受入理由は、裸の `RAND` に対する本家の返値0と公開版の拒否です。

公開版は先の `RAND` で停止し、同じ実行の後続 `RAND:0` には到達していません。本家が両方を出力した事実を、公開版で後続が実行された証拠にしません。

## `RAND:0`：`COLON_RAND_ZERO_COMPAT_YES`

[独立した入力ERB](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/fixture/ERB/MAIN.ERB)で `CompatiRAND:YES` の `RAND:0` を直接評価します。[入力CSV](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/fixture/csv/)も保存しています。

本家の[1回目](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/native-01-emuera.log)・[2回目](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/native-02-emuera.log)は `OBS_RAND_ZERO=0` と `AFTER`・`DONE` を出力しました。公開版の[標準出力](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/public-stdout.bin)は `BEFORE` まで、[標準エラー](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/public-stderr.bin)は22行目の同じ `E_ARGUMENT` です。これは先のケースの続きではなく、別fixtureの実測に基づく差異判定です。

## `P38`：未閉鎖IFの停止時点

[実際の入力ERB](../../evidence/representative-20261116/P38/fixture/ERB/P38.ERB)は3行目の `IF` で条件と `ENDIF` の両方を省きます。本家の[保存画面](../../evidence/representative-20261116/P38/raw/native-display.bmp)には読込み時警告、`BEFORE`、3行目の未対応 `ENDIF` エラーが表示されています。これは画面証拠であり、Nativeのテキスト原ログではありません。

公開版の[標準出力](../../evidence/representative-20261116/P38/raw/public-stdout.txt)には `Now Loading...` のみ、[標準エラー](../../evidence/representative-20261116/P38/raw/public-stderr.txt)には `ERB/P38.ERB:3: E_SYNTAX: Unclosed IF` があり、`BEFORE` はありません。先行表示と停止時点の差が `mismatch` 判定の根拠です。本家が問題を読込み時に警告することと、該当行に到達して停止することは分けて扱います。

元のパイロット証拠目録には公開版stdoutの当時のSHAが記録されていますが、stderrはその目録の固定対象に含まれていません。収録stderrは現存ファイルと今回使用した凍結台帳の一致を確認したもので、過去実行時の独立したSHA固定を遡って主張しません。条件の省略を除外したP38Bは別ケースです。

## `GMF_LEX_LONE_EQUALS`：不正な単独 `=`

[実際の入力ERB](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/fixture/ERB/MAIN.ERB)の4行目は `A=1=2` です。本家の[1回目](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/native-01-actual-final-log.bin)・[2回目](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/native-02-actual-final-log.bin)は `GM_BEFORE` の後に4行目で停止し、予期しない代入演算子 `=` と、等価比較への `==` 使用を示す診断を出しました。

公開版も[標準出力](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/public-stdout.bin)に `GM_BEFORE` を出した後、[標準エラー](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/public-stderr.bin)で `E_SYNTAX: Unexpected expression character '=' at column 2: 1=2` を報告しました。両側とも `GM_AFTER` は出ていません。差異判定は主診断の違いに限定され、診断全体のバイト一致やエラー後の変数状態は主張しません。ソース上で推定された分岐は直接計測していません。

## 証拠の取扱い

NativeログはUTF-16、公開版の生出力はファイル一覧のencodingを参照してください。元の生ログ・fixtureは本文を改変せずコピーし、SHA-256を一覧に記載しています。原receiptからはパスや識別子等を除き、入力ハッシュなどを選択した派生JSONを収録しました。元ファイル・変換後ファイルの対応と方法は非公開プロベナンスに保持しています。P38の画像は調査時に保持したクロップの原バイトであり、フル画面の原バイトは保持されていません。

設定やCSVを含む入力の一部が揃っていても、完全な設定・依存物・実行手順の検証を経ていないため、これらは再現性の証明ではありません。エンジン本体や第三者コードは収録していません。公開に際しては権利と機密性の最終監査が必要です。
