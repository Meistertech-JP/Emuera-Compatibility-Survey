# TWAIT 0,1 の保存観測

[English](README.md)

ケース `TWAITZERO01` は、Emuera1824+v24とPyEmuera 3.0.0で `TWAIT 0,1` を実行した際の限定比較です。登録判定は `different_scoped` です。

[ERB](fixture/ERB/TWAITZERO01.ERB) は `BEFORE_TWAIT_ZERO` を表示した後に `TWAIT 0,1` を呼び、復帰後に `AFTER_TWAIT_ZERO` を表示します。本家では隔離された入力欄に `42` を設定し、Enterのkeydown・keyupをpostしました。PyEmueraには `--debug --wait` と[空の入力テープ](fixture/inputs.txt)を指定しました。[設定](fixture/emuera.config)は保存された実行のものです。

本家では、Enterのpost後、probeの3秒待機を経て取得されたと記録された[画面の切り抜き](raw/native-after-input-crop.png)に `BEFORE_TWAIT_ZERO` が表示され、後続の `AFTER_TWAIT_ZERO` は確認されませんでした。ハーネスはその後、対象プロセスの終了処理を行いました。自然終了と終了コードは観測していません。入力が実際に受理・消費された時点やTWAIT内部のどの段階まで進んだかは、画面だけから確定できません。

PyEmueraは [標準出力](raw/pyemuera-stdout.bin) に `BEFORE_TWAIT_ZERO` を表示し、3行目で `E_UNSUPPORTED` として停止しました。[標準エラー](raw/pyemuera-stderr.bin)には、非正の時間で入力が無効なTWAITは永久に待機する旨の診断が記録され、終了コードは1でした。

このケースは負の待機時間、フラグ0、他の正の待機時間、引数の副作用、GUI全体を検証するものではありません。本家側の画面は文字列を表示した領域の切り抜きであり、これだけで入力の受理時点やプロセス終了を証明しません。保存された原比較票と入力イベント記録はこのbundleに含まず、過去の実行環境・実行者の真正性は同梱hashだけでは検証できません。

本家実行体の記録SHA-256は `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`、PyEmuera 3.0.0 pyzは `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35` です。本家・PyEmueraの実行体は同梱しません。

`manifest.json` には同梱ファイルのサイズとSHA-256を記録しています。これはファイルの整合性確認用であり、過去の実行や配布者の真正性の証明ではありません。

[Emueraの原ライセンス](licenses/Emuera1824-v24-license-original.txt)、[PyEmueraのライセンス](licenses/PyEmuera-3.0.0-LICENSE.txt)、[PyEmueraの第三者表示](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)は元のエンジン配布物に関する表示です。これらだけで画面、ログ、調査用fixtureのすべてに同じ条件が適用されることを意味しません。
