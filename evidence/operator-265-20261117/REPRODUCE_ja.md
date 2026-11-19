# 入力の準備と限定的な再実行

この資料は保存観測の閲覧とオフライン検証を目的とし、engine・任意fixture用のNative隔離runnerは含みません。以下は同じ入力を別の作業領域で準備する具体例です。記録当時はWindows 10 19045、CPython 3.12.10 64-bit、専用desktop上のNativeを約5秒観測し、自然終了しない所有processを終了しました。以下の通常desktopでの実行は当時の専用desktop・leaseを再現せず、同じ結果や画面を保証しません。.NET Frameworkの正確な最低版は未確定です。

事前に [environment.json](environment.json) の2 engine SHAと[権利表示](licenses/Emuera1824-v24-license-original.txt)・[NOTICE](licenses/NOTICE.ja.md)・[PyEmuera権利表示](licenses/PyEmuera-3.0.0-LICENSE.txt)・[第三者表示](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を確認してください。両engineは別途用意します。共有環境では同時実行者と調整し、他人のprocessやlockを操作しないでください。

PowerShellでこのbundleをcurrent directoryとし、engine pathを指定します。C017以外もC001〜C023から選べます。毎回一時領域に3つの別入力を作ります。`ERB/REVIEW.ERB` と `ERB/REVIEW.ERH` を両方配置し、configをrootに置き、`csv` は空のdirectoryにします。各入力hashは元recordに照合します。

```powershell
$bundle = (Get-Location).Path
$case = 'C017'
$nativeExe = 'PATH_TO_Emuera1824+v24.exe'
$pyz = 'PATH_TO_PyEmuera-3.0.0.pyz'
if ((Get-FileHash -Algorithm SHA256 $nativeExe).Hash.ToLowerInvariant() -ne '14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964') { throw 'Native SHA mismatch' }
if ((Get-FileHash -Algorithm SHA256 $pyz).Hash.ToLowerInvariant() -ne '8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35') { throw 'PyEmuera SHA mismatch' }
$pyz = (Resolve-Path $pyz).Path
$record = (Get-Content -Raw -Encoding UTF8 "$bundle/records.json" | ConvertFrom-Json).records | Where-Object id -eq $case
if (@($record).Count -ne 1) { throw 'Unknown case' }
$work = Join-Path ([IO.Path]::GetTempPath()) ('operator265-' + [guid]::NewGuid().ToString('N'))
foreach ($mode in @('native-01','native-02','public-01')) {
  $dir = Join-Path $work $mode
  New-Item -ItemType Directory -Path "$dir/ERB", "$dir/csv" -ErrorAction Stop | Out-Null
  foreach ($rel in @('ERB/REVIEW.ERB','ERB/REVIEW.ERH','emuera.config')) {
    $ref = $record.input.files.$rel
    Copy-Item -LiteralPath (Join-Path $bundle $ref.path) -Destination (Join-Path $dir $rel)
    if ((Get-FileHash -Algorithm SHA256 (Join-Path $dir $rel)).Hash.ToLowerInvariant() -ne $ref.sha256) { throw 'Input SHA mismatch' }
  }
  if (@(Get-ChildItem -LiteralPath "$dir/csv" -File -Recurse).Count -ne 0) { throw 'CSV is not empty' }
}
Write-Output $work
```

通常desktopでのNative試行例。各processの所有ハンドルだけを使い、5秒前に終了した場合と強制終了を区別します。障害・ダイアログ・未取得を成功と判断しないでください。

```powershell
foreach ($mode in @('native-01','native-02')) {
  $dir = Join-Path $work $mode
  Copy-Item -LiteralPath $nativeExe -Destination "$dir/Emuera1824+v24.exe"
  $p = Start-Process -FilePath "$dir/Emuera1824+v24.exe" -WorkingDirectory $dir -PassThru
  Start-Sleep -Seconds 5
  $p.Refresh()
  if ($p.HasExited) { "${mode}: natural exit code $($p.ExitCode)" }
  else { $p.Kill(); $p.WaitForExit(); "${mode}: terminated after observation" }
}
```

Py側は5秒上限で記録どおり `--debug .` を実行し、stdout/stderrを別々の生bytesとして保存する例です。

```powershell
$pyDir = Join-Path $work 'public-01'
$runner = @'
import pathlib, subprocess, sys
pyz, run = sys.argv[1:]
try:
    p = subprocess.run([sys.executable, '-I', pyz, '--debug', '.'], cwd=run, capture_output=True, timeout=5)
    pathlib.Path(run, 'stdout.bin').write_bytes(p.stdout)
    pathlib.Path(run, 'stderr.bin').write_bytes(p.stderr)
    print('returncode:', p.returncode)
except subprocess.TimeoutExpired as e:
    pathlib.Path(run, 'stdout.bin').write_bytes(e.stdout or b'')
    pathlib.Path(run, 'stderr.bin').write_bytes(e.stderr or b'')
    print('timeout; partial output only')
'@
python -I -c $runner $pyz $pyDir
```

Nativeの `emuera.log` とPyの `stdout.bin` / `stderr.bin` を各modeの保存rawと比較します。stdoutとstderrの時系列は合成しません。表示を実見していない場合、GUIの一致は未確認です。入力条件・終了形態・環境差を記録し、ログがない場合は未取得としてください。このbundleのverifierは保存済み原記録を調べるもので、新規試行を自動承認しません。
