# 複合代入・末尾カンマの保存観測

[English](README_en.md) · [機械記録](records.json) · [typed key対応](mapping.json) · [環境とengine識別](environment.json)

以下は指定された2入力での保存結果です。親catalogの両case verdictは `different_scoped`、両typed targetのsurvey判定は `documented_difference` です。記録の意味判定は `PARENT_ADJUDICATION_REQUIRED` のままで、この補足はそれを変更しません。関連typed key一覧は共有機構の関連付けであり、各演算子を実行した証明ではありません。以下では各fixtureの12行目に実際に書かれた演算子だけを示します。

両fixtureは `A=0 B=0 C=701 E=0 F=0`、`ZZREVD:0=6`、`ZZREVD:1=99`、`LOCALS="ab"`、`ZZREVS="ab"` を設定してから `BEFORE` を出力します。これらはfixture上の初期設定であり、Py側で別途読み戻した値ではありません。完全な条件は各ERB・ERH・configと空のCSV入力を参照してください。`D0` と `D1` は出力上の `ZZREVD:0` と `ZZREVD:1`、`S` は `LOCALS` です。

## `assignment_syntax:*=` — C022

case `OPISOLATED265_compound-trailing-comma`、入力行 `ZZREVD:0*=7,`。[ERB](fixtures/C022/ERB/REVIEW.ERB) · [ERH](fixtures/C022/ERB/REVIEW.ERH) · [config](fixtures/C022/emuera.config)。

本家 `native-01`・`native-02` はともに `BEFORE`、`REVIEW AFTER C=701 A=0 B=0 D0=42 D1=99 S=[ab]`、`DONE` を出力しました（[01](raw/C022/native-01/emuera.log)・[02](raw/C022/native-02/emuera.log)）。自然終了は未観測です。

PyEmuera `public-01` のstdoutには `BEFORE`、stderrには12行目の `E_SYNTAX: Expected EOF, got , at column 2: 7,` が記録され、AFTER・DONEは記録されませんでした。終了コードは1です（[stdout](raw/C022/public-01/verified.stdout.bin)・[stderr](raw/C022/public-01/verified.stderr.bin)）。別々の出力streamの時系列は結合していません。エラー後の変数状態は未観測です。

## `assignment_syntax:+=` — C023

case `OPISOLATED265_compound-string-trailing`、入力行 `LOCALS+="ab",`。[ERB](fixtures/C023/ERB/REVIEW.ERB) · [ERH](fixtures/C023/ERB/REVIEW.ERH) · [config](fixtures/C023/emuera.config)。

本家 `native-01`・`native-02` はともに `BEFORE`、`REVIEW AFTER C=701 A=0 B=0 D0=6 D1=99 S=[abab]`、`DONE` を出力しました（[01](raw/C023/native-01/emuera.log)・[02](raw/C023/native-02/emuera.log)）。自然終了は未観測です。

PyEmuera `public-01` のstdoutには `BEFORE`、stderrには12行目の `E_SYNTAX: Expected EOF, got , at column 5: "ab",` が記録され、AFTER・DONEは記録されませんでした。終了コードは1です（[stdout](raw/C023/public-01/verified.stdout.bin)・[stderr](raw/C023/public-01/verified.stderr.bin)）。エラー後の変数状態は未観測です。

本家ログはUTF-16、Pyのrawは保存bytesです。2回の本家ログは同一内容ですが、自然終了・GUI表示の一致や他の入力への一般化を示しません。両engine本体は含みません。fixture・config・rawの作者と再配布権限は未確認であり、公開前に確認が必要です。[Emuera原license](licenses/Emuera1824-v24-license-original.txt) · [関連NOTICE](licenses/NOTICE.ja.md) · [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt) · [第三者表示](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)。NOTICEにある原ZIPはこのbundleに含まれません。

PyEmuera第三者表示の中のファイルパスは、元のPyEmuera配布物を指します。この資料にそれらがすべて同梱されていることを意味しません。
