# Preparing inputs and a bounded rerun

This bundle preserves observations and supports offline validation; it does not include engines or an isolated Native runner for arbitrary fixtures. The original runs used Windows 10 19045, 64-bit CPython 3.12.10, a private Native desktop, an approximately five-second observation and termination of the owned process when it had not exited. Natural exit was not observed. The example below uses an ordinary desktop and does not recreate that private desktop or its lease, so identical behavior is not guaranteed. The exact minimum .NET Framework version is not established.

Check the pinned engine hashes in [environment.json](environment.json) and the [Emuera license](licenses/Emuera1824-v24-license-original.txt), [archive NOTICE](licenses/NOTICE.en.md), [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt), and [third-party notices](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). Obtain the engines separately. Coordinate with other users of a shared environment and operate only on your own processes.

From this bundle, choose C001–C023 and provide paths to the pinned Native EXE and PyEmuera pyz. The commands create fresh separate `native-01`, `native-02`, and `public-01` directories, copy both `ERB/REVIEW.ERB` and `ERB/REVIEW.ERH`, place `emuera.config` at each root, create an empty `csv` directory, and compare every input hash with records.json. They then launch each owned Native process for five seconds and distinguish natural exit from termination. The Python example runs `python -I PYZ --debug .` with a five-second timeout and captures stdout and stderr separately as bytes.

### Prepare inputs

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

### Run the owned Native processes

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

### Capture Py stdout and stderr separately

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

Compare the new Native `emuera.log` and Py stdout/stderr to the separate saved channels, recording any timeout, missing output, different termination, and environment change. Do not infer a GUI match from a text log or combine stdout and stderr into a single timeline. The bundle verifier checks the saved evidence; it does not automatically accept a new rerun.
