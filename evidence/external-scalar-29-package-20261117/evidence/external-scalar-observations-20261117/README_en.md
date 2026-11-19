# Viewing and verifying the saved observations

[OBSERVATIONS_en.md](OBSERVATIONS_en.md) lists each expression, Native/PyEmuera RESULT, additional recorded output, and links to its fixture, config, and any required CSV. The machine-readable records are in `records.json`. Mode-specific raw logs are under `raw/Cxxx/native/emuera.log` and `raw/Cxxx/public/emuera.log`. No screenshots are included, so GUI output cannot be viewed or compared here.

The 29 cases were selected from external comparison records. Their source association and hashes were checked during preparation, but the original external records, original receipts, case-binding table, and per-case source-hash list are not included in this bundle. A third party therefore cannot independently recheck that mapping or authenticate the historical executions from this bundle alone. The verifier can check consistency among the extracted fields in `records.json`, included raw logs, fixtures, and other bundled files.

The other 59 cases in the 88-case review are not included; omission does not mean they were never observed. Two cases have different recorded values between Native and PyEmuera. `DONE` is a fixture marker, not proof of natural termination. A receipt return code alone does not establish the complete execution. Results are limited to each recorded input, CSV, configuration, and other condition; they do not generalize to unrecorded cases.

## Reproduction limits

Fixtures and recorded config/CSV files are included, but engine binaries, the complete execution environment, and original receipt files are not. Extracted fields in `records.json` are not the original receipts. The historical runs therefore cannot be fully replayed or checked against their original receipts from this bundle. Follow-up runs may be possible with engines whose use is separately cleared, a compatible environment, and case-specific conditions; matching output is not guaranteed.

## Compare pins before running the verifier

Use the following PowerShell procedure. Obtain the four expected hashes outside this bundle, and independently authenticate the provider and channel before replacing the placeholders with those values. This document does not identify or guarantee a pin issuer or distribution channel. Placeholders, malformed hashes, missing files, mismatches, missing Python, Python startup failures, and nonzero verification exits all stop the procedure. No bundled Python code runs until every hash comparison succeeds.

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

The evidence manifest is checked first, followed by the complete package. If either step fails, the later command is not run. Manifest agreement checks file integrity and internal references. It does not establish the source mapping to external records, rights, privacy clearance, publication permission, or historical execution authenticity.


