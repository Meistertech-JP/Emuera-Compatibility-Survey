# LOADGLOBAL：切り詰められた保存データの比較

[English](README_en.md) · [機械記録](records.json) · [隔離実行入口](runner.py) · [ファイル一覧](manifest.json)

`LOADGLOBAL_CORRUPT_TRUNCATION_20261115` は、各engine自身が作成した形式のglobal保存データを途中で切り詰めた有限条件の記録です。元のcase verdictは `different_scoped`、対象は `command_or_syntax:LOADGLOBAL`。本家とPyEmueraで別形式・別bytesを使っており、同一ファイルの読込み比較や異形式間の互換性試験ではありません。

共通の[ERB](fixture/ERB/SEARCHBOUND01.ERB)・[ERH](fixture/ERB/GLOBAL205.ERH)・[設定](fixture/emuera.config)を用い、CSVは空です。開始時に `GLOBAL:0=900`、`GLOBAL:1=901`、`GLOBALS:0="SENTINEL0"`、`GLOBALS:1="SENTINEL1"`、ユーザー数値配列の先頭3値を `901,902,903`、ユーザー文字列2値を `MUT0,MUT1`、`RESULT=777` に設定します。

本家用の[global.sav](fixture/native/global.sav)は正常保存273 bytesの先頭163 bytes、PyEmuera用の[global.json](fixture/public/global.json)は正常保存557 bytesの先頭441 bytesです。両者はそれぞれ対応engineの保存形式から作成されています。正常な元ファイル自体は含みません。

保存された本家・PyEmuera各1回のログから読める値は次のとおりです。`USER*` は `ZZ205G`、`USERS*` は `ZZ205GS` を表します。

| 出力 | 本家 | PyEmuera |
|---|---|---|
| `RESULT` | 0 | 0 |
| `GLOBAL0`, `GLOBAL1` | 50, -51 | 900, 901 |
| `GLOBALS0`, `GLOBALS1` | BUILTIN0, BUILTIN1 | SENTINEL0, SENTINEL1 |
| `USER0`, `USER1`, `USER2` | 901, 902, 903 | 901, 902, 903 |
| `USERS0`, `USERS1` | MUT0, MUT1 | MUT0, MUT1 |
| `CORRUPT_LOAD_CONTINUED` | 出力あり | 出力あり |

[本家log](observed/native/emuera.log)と[Py log](observed/public/emuera.log)はUTF-16です。Pyの[stdout](observed/public/stdout.bin)と[stderr](observed/public/stderr.bin)も保存しています。stderrには `E_SAVE: Invalid save: Expecting value: line 1 column 442 (char 441)` があり、保存receiptの終了codeは0でした。当時の本家は5秒後も終了せず、後片付けで所有processへの強制終了APIが成功と記録されました。その後のwait結果、本家の自然終了・終了codeとGUI診断は未観測です。OUTPUTLOGや継続markerは自然終了の証明ではありません。両形式それぞれの切り詰め条件に限定され、権限、ゲームID・版の不一致、全保存変数、他の破損位置は対象外です。

## 隔離実行入口

このbundleをリポジトリの `evidence/loadglobal-corrupt-20261117/` に配置し、同じリポジトリの `harness/` を明示して使います。Windowsの対話セッション、Python 3.10以降、.NET Framework実行環境、既存の共有lock directory、別途用意した固定SHAの両engineが必要です。`--out-root` は**既存のリポジトリ外ディレクトリ**を必ず指定します。実ゲームや既存セーブのディレクトリは指定しないでください。

実行前に、独立した信頼経路からmanifestと `runner.py` の期待SHA-256を取得し、OSのhash手段で両方を照合してください。同梱物だけから真正性は確定しません。runnerは指定されたmanifestとbundle全ファイル、リポジトリ内harnessの5 source、および指定されたengineのSHAを検査します。固定対象が変わった場合は利用を中止し、確認された別版のpinを使用します。

### 読取り専用dry-run

bundle directoryからPowerShellで実行します。下記のplaceholderは実際のpathと信頼済みSHAへ置き換えてください。`$OutputRoot` は作成済みで、リポジトリの内側でもその親でもないディレクトリです。

```powershell
$Repo = (Resolve-Path -LiteralPath '<REPOSITORY_ROOT>').Path
$HarnessDir = Join-Path $Repo 'harness'
$OutputRoot = (Resolve-Path -LiteralPath '<EXISTING_OUTPUT_DIRECTORY_OUTSIDE_REPOSITORY>').Path
$NativeExe = (Resolve-Path -LiteralPath '<PATH_TO_Emuera1824+v24.exe>').Path
$PyZ = (Resolve-Path -LiteralPath '<PATH_TO_PyEmuera-3.0.0.pyz>').Path
$ManifestPin = '<TRUSTED_MANIFEST_SHA256>'
python -I -B runner.py --dry-run --repository-root $Repo --harness-dir $HarnessDir `
  --out-root $OutputRoot --manifest-sha256 $ManifestPin --native $NativeExe --pyz $PyZ
if ($LASTEXITCODE -ne 0) { throw 'Dry-run failed' }
```

dry-runはファイルを作成・変更せず、engine・process検索・lock取得を行いません。bundle、harness、両engine、出力先と入力配置計画を検査します。出力先への書込み権限は検査しません。`--lock-dir` を追加した場合もlockの存在を読むだけで、実行時の取得成功は保証しません。

### 実機の再実行

`--lock-dir` には、リポジトリ内でもその祖先でもない既存のshared lock directoryを指定し、他の実行者と同一のlockを使います。未使用のattempt名を指定します。実行時は入力を出力先の新規attemptに別々にcopyし、Nativeは隔離desktopで最大5秒観測します。所有processが残れば、そのhandleだけで強制終了します。同名の他processは終了せず、起動前に拒否し、終了後に検出された場合はPyを起動しません。

```powershell
$SharedLock = (Resolve-Path -LiteralPath '<EXISTING_SHARED_LOCK_DIRECTORY>').Path
python -I -B runner.py --run --repository-root $Repo --harness-dir $HarnessDir `
  --out-root $OutputRoot --manifest-sha256 $ManifestPin --native $NativeExe --pyz $PyZ `
  --lock-dir $SharedLock --attempt-name 'loadglobal-truncation-01'
if ($LASTEXITCODE -ne 0) { throw "Run incomplete or failed (exit $LASTEXITCODE); inspect retained output" }
```

ロックに参加しないツールとの排他は保証しません。既存attemptは上書きしません。`<out-root>/<attempt-name>/` に各engineの作業内容、`snapshots/before/` と `snapshots/after/` のsave、Native log、Py log・stdout・stderr、`RESULT.json` とその作成前のファイルinventoryを保持します。この入口は結果を署名・sealしません。エラーやtimeout時も作成済み出力は可能な範囲で残ります。出力にローカル情報が含まれることがあり、共有前に確認が必要です。

`CAPTURED` は選択markerが両logに揃ったことを意味し、正式受入や完全互換性を示しません。Nativeの自然終了と強制終了、Py非0とtimeoutは区別します。Py非0は可能な範囲でexit codeを返し、timeoutは124です。Native GUI診断は採取しません。実機runの成功はこの案のdry-runでは確認していません。

固定engine SHA-256: Native `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`、PyEmuera 3.0.0 pyz `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35`。固定harness sourceのhashは `runner.py` 内の `HARNESS_PINS` を参照してください。hashはbytesの識別であり、実行や配布者の真正性を保証しません。

## 権利表示

[Emuera原ライセンス](licenses/Emuera1824-v24-license-original.txt) · [PyEmueraライセンス](licenses/PyEmuera-3.0.0-LICENSE.txt) · [第三者表示](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)。各表示は元engine配布物についてのもので、fixture・破損save・log全体の作者や再配布許諾を一括して確定しません。素材ごとの権利とprivacyは公開前に確認が必要です。
