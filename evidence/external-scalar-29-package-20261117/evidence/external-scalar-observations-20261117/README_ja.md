# 保存観測の閲覧・検証

[OBSERVATIONS_ja.md](OBSERVATIONS_ja.md)には各ケースの式、Native/PyEmueraのRESULT、追加出力、fixture/config/必要なCSVへのリンクがあります。機械可読記録は同梱の`records.json`です。`raw/Cxxx/native/emuera.log`と`raw/Cxxx/public/emuera.log`はmode別の保存rawです。画面画像は含まれないため、この資料からGUI表示を閲覧・比較できません。

対象は原凍結外の外部比較記録から選ばれた29ケースです。準備時には外部記録との対応やsource hashを確認しましたが、外部原記録、元receipt、対応表、各caseのsource hash一覧はこのbundleに含まれません。したがって第三者はbundle単独でその対応を再検証できず、過去の実行そのものの真正性も確認できません。`records.json`に抽出した値・状態とraw、fixture等の同梱ファイル間の整合は、下記verifierで検査できます。

88件の調査の残る59件は収録していません。非収録は未観測を意味しません。NativeとPyEmueraの記録値の相違を2件含みます。`DONE`はfixture markerであり自然終了を証明しません。receiptのreturncodeも単独では実行全体を証明しません。結果は記録された各入力・CSV・設定等の条件に限られ、未記録条件へ一般化できません。

## 再現限界

fixtureと記録config/CSVは収録していますが、engine binary、完全な実行環境、元receiptファイルは収録していません。record中の抽出項目は元receiptそのものではありません。このため当時の実行を完全再現したり、元receiptと照合したりできません。別途利用条件を確認したengine、適合環境、個別条件による追試は可能ですが、同じ出力を保証しません。

## verifierを実行する前のpin照合

次の手順はPowerShell用です。4つの期待SHAをbundle外から取得し、その提供者と経路を利用者自身が独立に確認してから、placeholderを実値に置き換えてください。この資料はpinの発行元や特定の配布経路を指定・保証しません。placeholder、不正なSHA、ファイル欠落、hash不一致、Pythonの未導入・起動失敗、検証器の非0終了はすべて停止条件です。比較が成功するまでbundle内のPythonコードを実行しません。

```powershell
$ErrorActionPreference = 'Stop'
$bundle = 'PATH_TO_BUNDLE_ROOT'
$evidence = Join-Path $bundle 'evidence/external-scalar-observations-20261117'
$expected = @{
  package_manifest_sha256     = 'REPLACE_WITH_INDEPENDENT_PIN'
  observation_manifest_sha256 = 'REPLACE_WITH_INDEPENDENT_PIN'
  verifier_sha256             = 'REPLACE_WITH_INDEPENDENT_PIN'
  helper_sha256               = 'REPLACE_WITH_INDEPENDENT_PIN'
}

try {
  $python = Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1
} catch {
  throw 'Python is unavailable; no bundle verifier was run.'
}

function Assert-Sha256([string]$Path, [string]$Expected) {
  if ($Expected -notmatch '^[0-9a-fA-F]{64}$') { throw "Invalid or missing expected SHA-256: $Path" }
  $actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256 -ErrorAction Stop).Hash
  if ($actual -ne $Expected) { throw "SHA-256 mismatch: $Path" }
}

$verifier = Join-Path $evidence 'verify.py'
$helper = Join-Path $bundle 'tools/file_set_manifest.py'
Assert-Sha256 (Join-Path $bundle 'package-manifest.json') $expected.package_manifest_sha256
Assert-Sha256 (Join-Path $evidence 'manifest.json') $expected.observation_manifest_sha256
Assert-Sha256 $verifier $expected.verifier_sha256
Assert-Sha256 $helper $expected.helper_sha256

function Invoke-CheckedPython([string[]]$Arguments) {
  try {
    & $python.Source -B @Arguments
    $code = $LASTEXITCODE
  } catch {
    throw "Python failed to start; later checks were not run. $($_.Exception.Message)"
  }
  if ($null -eq $code -or $code -ne 0) { throw "Python check failed with exit code $code; later checks were not run." }
}

Invoke-CheckedPython @($verifier, '--inventory-tool', $helper, '--pin', $expected.observation_manifest_sha256)
Invoke-CheckedPython @($helper, 'verify', '--root', "bundle=$bundle", '--manifest', (Join-Path $bundle 'package-manifest.json'))
```

evidence manifestを検証した後にpackage全体を検証します。各段階が失敗すれば後続コマンドは実行されません。manifest一致は収録ファイルの完全性と内部参照の確認であり、外部原記録との対応、権利、privacy、公開許諾、過去実行の真正性を認定しません。


