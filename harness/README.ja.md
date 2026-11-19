# 有限範囲の式比較ハーネス

[English](README.md)

型付き計画から限定された ERB fixture を生成し、Windows 上で固定した Native Emuera と PyEmuera を実行して、値および `RESULT`・`RESULTS` のスナップショットを比較します。エンジンを起動せず、保存ログの比較と証拠封印の検証もできます。式検査・fixture 生成・strict decode・マーカー解析・比較には調査時の v3 runner を再利用し、実行部分は明示的なパスと共有ロックを使うよう移植しています。

付属計画の対象は `ABS`、`STRFIND`、`STRFINDU` です。`different` は観測差異または期待値・sentinel 制約違反を示すため、両側の観測値を確認してください。実行や封印の成功は完全互換性の証明ではありません。先頭ケースを単独で実行し、複数ケースを選んだ場合は全件バッチも実行します。Native の反復は最大3回で、反復間と先頭ケースの単独・バッチ間の観測一致を確認します。

正常な文字列戻り値を確認する別の計画として [`fixtures/string-return-plan.json`](fixtures/string-return-plan.json) もあります。同じ `plan`・`run`・`audit` コマンドにこのファイルを指定すると、`TOSTR` の選定条件を比較できます。

## 必要なもの

* プライベート desktop を作成できる Windows の対話セッション、Windows PowerShell、`Win32_Process` の CIM アクセス、Native 用の .NET Framework 実行環境。Framework の正確な最低バージョンは未確定です。
* Python 3.10 以上。元の観測では 64-bit Python 3.12.10 を記録しています。ハーネスにサードパーティ Python パッケージは不要です。
* `Emuera1824+v24.exe`、SHA-256 `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`。
* 公開 PyEmuera 3.0.0 の pyz、SHA-256 `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35`。公開 runtime ZIP 内の pyz は同じハッシュです。このharnessディレクトリには両エンジンの実行ファイルを直接同梱していません。本家の配布ZIPはリポジトリ内の `vendor/emuera/` にあり、PyEmueraは別途入手します。入手・再配布条件は各表示を確認してください。
* 同梱 config をバイト単位で固定します。入力 ERB は CP932・CRLF で生成し、各側に空の `csv` ディレクトリを用意します。両側の入力とバイナリのハッシュを検査します。

## 操作

このディレクトリで実行します。以下のパスは例なので実際の場所に置き換えてください。コマンドの掲載は実機での成功を意味しません。

```powershell
python -B harness.py plan fixtures/representative-plan.json
python -B -m unittest discover -s tests -v

python -B harness.py run fixtures/representative-plan.json `
  --native <Emuera1824+v24.exeのパス> --pyz <PyEmuera.pyzのパス> `
  --lock-dir <共有ロックディレクトリ> --out <新規出力先> --repeat-native 2

python -B harness.py compare fixtures/representative-plan.json <Nativeログ> <Pyログ>
python -B harness.py validate <attemptディレクトリ>
```

`plan`・`compare`・`run` は `--case CASE_ID` を複数指定できます。選択前に計画全体を検査します。`run` は固定ハッシュを確認し、エンジンをダウンロード・変更しません。`--out` 下に新しい attempt を作ります。原 fixture やエンジンと異なる出力先を指定してください。生成 fixture と config は両側へ個別にコピーされ、原ログ・出力は attempt に残ります。エンジンの出力や例外メッセージにはローカルパスが含まれ得るため、公開前に監査してください。

Windowsでは、階層の深い出力先で本家が早期終了した例があります。原因は特定できていませんが、実行時は短く浅い階層の出力先を使ってください。

並行する Native 実行・計測は、**同じ既存の共有ロックディレクトリ**を使う必要があります。`NATIVE_LOCK.json` を排他的に作成し、既存の Native または `MEASURE_LOCK.json` を拒否し、自分の nonce を再検査して自分のロックだけを削除します。同名 Native プロセスの存在時も起動を拒否します。専用 desktop のプロセスは自分が `CreateProcessW` から取得したハンドルでのみ終了し、その後に残留を確認します。強制終了は自然終了と区別します。ロックを使わない別ツールとの排他は保証できず、中断時にはロックが残り得ます。他の実行者のロックを削除しないでください。

## CSVBASE B045 代表再実行

`run_csv_b045.py` は登録済みCSVBASE条件1件を Native 2回、PyEmuera 1回の独立workdirで再実行します。`--repo-root` は省略時にこのscriptを置いた `harness` の親をrepository rootとして使います。出力先、Native/PyEmuera実行体は明示が必要です。実行時はさらに既存shared lock directoryを指定します。

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -B harness/run_csv_b045.py dry-run `
  --out-root <repository外の出力先> `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz>

python -B harness/run_csv_b045.py run `
  --out-root <repository外の新規出力先> `
  --lock-dir <既存shared lock directory> `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz>
```

別の配置を確認するときだけ `--repo-root <repository root>` を指定します。実行体は固定SHAを照合します。コマンドは観測不足・診断未検証・画像確認待ちを含む限り非zeroで終了します。作成された `RESULT.json` とsealを確認してください。record schemaは `csv-b045-rerun-dry-run.v1` と `csv-b045-rerun-attempt.v1` です。modeごとに入力/実行体hash、return/強制終了、stdout/log/crop、lock、残留processを記録します。lock所有・解放異常は他の結果より優先してfailureになります。mode開始前・launch前・process終了後・mode終了後にowner nonceとmeasurement lockを確認し、異常時は後続modeを起動しません。

Nativeは既存の所有desktop/process handleによる制御を使います。起動後6秒待ってから最大15秒のwindow cropを試し、そのcallbackの後に既存 `native.py` が最大5秒waitして必要なら自身のprocess handleで終了します。これは以前の起動後5秒probeとは時間条件が異なり、同じ測定として比較しません。実際の待機・capture・process終了の時刻と経過時間をmode記録に残します。両Native crop (`native-01/native-display-crop.bmp`、`native-02/native-display-crop.bmp`) は画像として実見し、window、文字、診断、切れやblankを確認します。読み取れない項目は未観測とします。cropは下部の最大700×320 pixelsで、capture helperが選ぶsurfaceの内容や全表示を保証しません。AIによる画像確認を行えます。人間承認はrunnerの条件にしません。

保存済みB045記録にはNative/Pyの期待診断文が独立pinされた形で揃っていません。Public stdout/stderrは保存されますが、診断の意味は未検証です。markerや終了形が合っても診断一致を示さず、結果は `VISUAL_REVIEW_REQUIRED` または `DIAGNOSTIC_UNVERIFIED` に留まり、scoped differenceの成功扱いにしません。diagnosticを確認できない記録は未確定です。postfatal stateは `UNOBSERVED` です。


## 証拠と限界

`validate` は v3 manifest・seal、ファイル集合とハッシュ、外部参照が空であることを検証します。結果の意味を再判定するものではありません。`compare` は指定した両 raw log を再解析しますが、プロセス receipt は検証しません。過去の v2/v3 attempt の監査には対応しておらず、このハーネスで歴史証拠を再検証済みとは主張できません。元の v3 規約により `VALIDATION.json` は inventory と seal の対象外です。

新しい純粋式実行は要求全体と入力の実行前後記録を保存し、封印後に意味監査を行います。表示される小文字の `SEAL.json SHA-256` を別の信頼できる記録に保管してください。同じ計画・選択・反復回数・エンジン・config・Python・OSバージョン・優先文字コード・プロセス環境全体・ハーネスコードで、エンジンを起動せず試行全体を再検証・再利用できます。

```powershell
python -B harness.py audit <attemptディレクトリ> fixtures/representative-plan.json `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz> --repeat-native 2 --seal-sha256 <別途保管した封印SHA256>
python -B harness.py resume <attemptディレクトリ> fixtures/representative-plan.json `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz> --repeat-native 2 --seal-sha256 <別途保管した封印SHA256>
```

実行時に指定した `--case` と `--config` も同じにします。環境変数は平文ではなく全体のハッシュで固定するため、無関係な変数の変更でも再利用できません。ハッシュは機密性の保証ではないため、試行記録とともに保護してください。`resume` は再導出した結果を返し、エンジンの起動や失敗時の自動再実行はしません。監査は封印・計画由来の fixture・入力とプロセスの記録・生ログ・反復と単独／バッチの一致を確認し、比較と判定を再導出します。記録不足、失敗試行、異なる入力、封印対象外の `VALIDATION.json` は拒否し、試行内容は変更しません。別途保管したハッシュが信頼できる場合に限り対象バイトの改変を検出できます。ハッシュや意味整合だけでは、信頼できない作成者がエンジンを実際に実行したことは証明できません。旧 portable v1 は必要な記録が不足し再開できず、過去の v2/v3 attempt もこのハーネスの対象外です。固定入力が変わった場合は新規実行が必要です。ケース単位の途中再開には対応せず、インストール済みFrameworkなど環境の全状態を記録するものではありません。

runの直後に別processでauditするときは、同じPowerShell sessionを開いたまま、runが表示したattempt pathと別途保存したseal SHAを指定してください。run時と同じplan、選択case、反復回数、実行体、config、Pythonを使います。コマンドごとに新しい実行環境を注入するlauncherでは、利用者が設定を変更しなくても環境hashが変わり拒否されることがあります。その場合、hash検査を省略・差替えせず、固定された元の環境が保たれているsessionで監査してください。hashだけから元の環境は復元できません。環境変数の名前や値を公開記録へ出力する必要はありません。

意味を再解析するのは主に両側のOUTPUTLOGに記録された選択観測です。PyEmueraのstdout・stderrは封印されたバイト列の整合性を確認しますが、その診断内容と終了コードの意味上の整合までは判定しません。

純粋式 runner は GUI・エラー・任意 ERB・旧 scope 参照の再生に対応しません。比較時の PyEmuera は `--debug` で起動し、この条件を記録対象とします。付属単体試験は合成ログと模擬プロセスを使用し、実エンジンや Native desktop を起動しません。

`fixtures/manual/` の P35（数値入力）、P36（文字列入力）、P38（閉じていない IF）は `local_cases.py` が扱います。固定ケース `ARGUMENT`、`RESULT_WRITE` と入力後ログ追加版 `P35_OBS`・`P36_OBS` も同 runner の対象です。`harness.py run` はこれらを扱いません。

```powershell
python -B local_cases.py --case P35 --native <Emuera1824+v24.exeのパス> `
  --pyz <PyEmuera.pyzのパス> --lock-dir <共有ロックディレクトリ> --out <新規出力先>
```

固定入力は P35=`42`、P36=`ABC`。Native は隔離 desktop の所有 PID・入力欄を照合して入力し、表示面の下部の 700×320 以下をクロップします。キャプチャ成功は可読性や結果の一致を意味せず、画像の実見と Py 側 stdout/stderr の確認が必要です。`RESULT_WRITE` は両側の OUTPUTLOG から前後値を検査します。出力先は機密監査前の記録を保護できる場所にしてください。GUI 比較は固定された１画面・入力条件に限定され、IME や他の画面、任意の fixture に一般化できません。

元コードと固定入力の対応は [PROVENANCE.md](PROVENANCE.md)、再利用条件は[権利表示](../LICENSES/README.ja.md)を参照してください。比較用のpyzは[PyEmuera 3.0.0のRelease](https://github.com/Meistertech-JP/PyEmuera/releases/tag/v3.0.0)から入手し、候補のルートで `python -B tools/verify_environment.py --native <exe> --pyz <pyz>` を実行して照合してください。

PRINTVKWの[通常の待機解除](../evidence/wait-release-20261117/README.ja.md)、[待機後の評価順と診断](../evidence/wait-c15-20261117/README.ja.md)、[スプライト表示](../evidence/graphics-gui-observations-20261117/README.ja.md)については、各資料に記録したfixture・設定・出力を参照してください。これらは上記の純粋式・固定ケース用コマンドの対象外です。待機や描画の確認は、観測位置と入力を固定した別個の実行として扱います。
