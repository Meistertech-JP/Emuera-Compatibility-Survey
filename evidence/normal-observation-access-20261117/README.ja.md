# PRINT SINGLEの保存観測：10条件

[English](README.md)

[observations.json](observations.json) は、PRINT SINGLE系の選択10条件について入力条件、元のcase判定、2つのEmuera modeと1つのPyEmuera modeの履歴・状態を示します。3 modeは20条件を含む1共有batchの保存結果で、10件の別々の実行ではありません。元の [8群のindex](../multi-group-101-20261117/index.json) と [説明](../multi-group-101-20261117/README.ja.md) にあるfixture、設定、履歴への相対参照・SHA-256と、各履歴の半開byte範囲を保持します。JSONの改行・空白は観測そのものです。

例えばC196_13では、Emuera履歴の `P><T` とPyEmuera履歴の `P>`、半角スペース1文字の行、`<T` は異なり、両者の状態行は `A=0 B=0 R=701 S=sentinel` です。元indexのraw・layoutと、observable content・stateという比較軸は別々に保たれています。

Nativeの自然終了、内部引数値は未観測です。比較票・原receipt・原受入票は同梱していません。ここにある通常条件の結果は異常条件の挙動や命令全般の互換性を証明しません。表示画面や実行環境の全体一致も主張しません。

配布物のルートから `python -I -B tools/query.py C196_04`、`python -I -B tools/query.py PRINTPLAIN196_C196_04`、または `python -I -B tools/query.py command_or_syntax:PRINTSINGLEV` で検索できます。検索結果のcase参照から各modeの履歴とbyte範囲へ進めます。

履歴bytesが一致するNative 2 modeも、元indexに記録されたmode別probeのSHAを別々に参照します。Public modeはreceiptのSHAを参照します。原probe・receipt本文は含みません。C196追補の不整合時に他の検索結果を得るには `--partial` を指定し、終了コード3と `INCONSISTENT`／`PARTIAL` を確認してください。他の資料や共通検証toolのエラーは分離されません。

別に保存されたPRINT K/Dの49条件は、既存の [82 case index](../print-kd-shared-82-20261117/index.json) と [説明](../print-kd-shared-82-20261117/README.ja.md) に条件・mode別結果・根拠byte範囲があるため重複掲載していません。こちらも共有batchで、GUI色・font・styleおよびNative自然終了は未観測です。両資料の権利表示はそれぞれのREADMEをご覧ください。

この資料を `evidence/normal-observation-access-20261117/` に置いた構成では、Python 3.9以降で参照先の整合を確認できます。先に信頼できる別経路から `manifest.json` と `tools/file_set_manifest.py` のSHA-256を入手し、ツールのSHAを照合してください。次の例では、その別経路で得たmanifestのSHAを入力します。

```powershell
$ExpectedManifestSHA256 = Read-Host 'Trusted manifest SHA-256'
if ((Get-FileHash evidence/normal-observation-access-20261117/manifest.json -Algorithm SHA256).Hash -ne $ExpectedManifestSHA256) { throw 'Manifest SHA-256 mismatch' }
python -I -B tools/file_set_manifest.py verify --manifest evidence/normal-observation-access-20261117/manifest.json --root evidence=evidence/normal-observation-access-20261117
if ($LASTEXITCODE -ne 0) { throw 'File-set verification failed' }
python -I -B evidence/normal-observation-access-20261117/verify.py --evidence-root evidence --manifest-sha256 $ExpectedManifestSHA256
```

検証は4ファイルの集合とindex・fixture・設定・履歴との整合を確認します。privacyと権利は最終確認前です。実行の真正性や公開承認を示すものではありません。
