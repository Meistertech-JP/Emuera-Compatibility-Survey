# Historical external observations: 16 additional cases

[Conditions and recorded output](OBSERVATIONS_en.md) · [Machine-readable records](records.json) · [日本語](README_ja.md)

These are four expressions, eight PRINT-related text logs and four engine diagnostics. The originals lie outside the frozen survey and were checked against historically recorded SHA values. The 16 are distinct from the earlier 29 among the 88 cases; the other 43 are not included here. Exclusion does not mean that no observations exist.

Screen appearance and values absent from the logs are not inferred. Natural exit and post-error state remain limited to what was recorded. For two ENCODETOUNI cases the historical SHA of the Native input probe was not found; the probe is a current readback. The selected receipts do not establish the PyEmuera configuration and related inputs for the eight PRINT cases and those two error cases. The original diagnostics and unobserved states are retained.

## Rights and rerun scope

At the distribution root, `notices/README.en.md` describes the accompanying Emuera license and bilingual NOTICE and the PyEmuera license and third-party notices. The Emuera NOTICE describes a separately retained original ZIP distribution; that ZIP is not included here. The PyEmuera notices and SOURCES describe the original PyEmuera distribution. No engine is included. Authorship, redistribution permissions and privacy for the fixtures, configurations and raw output require separate review; accompanying notices do not constitute publication approval.

This material supports reading saved observations and offline verification. It does not contain the complete execution environment or all original receipts and does not guarantee the same result in a later rerun.

## Offline verification

Obtain trusted expected hashes for the verifier, helper and both manifests through a channel independent of the bundle. Replace the four placeholders below with independently obtained trusted SHA values. Missing pins, hash errors, mismatches, missing or unlaunchable Python, or either verification failure stop the block. The outer package is verified first:

```powershell
& {
    $ErrorActionPreference = 'Stop'
    $bundle = 'PATH_TO_BUNDLE_ROOT'
    # Replace each placeholder with its separately obtained trusted SHA-256.
    $expectedPackage = 'INDEPENDENT_PACKAGE_MANIFEST_SHA256'
    $expectedObservation = 'INDEPENDENT_OBSERVATION_MANIFEST_SHA256'
    $expectedVerifier = 'INDEPENDENT_VERIFIER_SHA256'
    $expectedHelper = 'INDEPENDENT_HELPER_SHA256'
    $evidence = Join-Path $bundle 'evidence/external-additional-observations-20261117'
    $helper = Join-Path $bundle 'tools/file_set_manifest.py'
    $verifier = Join-Path $evidence 'verify.py'
    $packageManifest = Join-Path $bundle 'package-manifest.json'
    $observationManifest = Join-Path $evidence 'manifest.json'
    $checks = @(
        @{ Path = $packageManifest; Expected = $expectedPackage },
        @{ Path = $observationManifest; Expected = $expectedObservation },
        @{ Path = $verifier; Expected = $expectedVerifier },
        @{ Path = $helper; Expected = $expectedHelper }
    )
    foreach ($check in $checks) {
        if ($check.Expected -notmatch '^[0-9a-fA-F]{64}$') { throw 'A trusted SHA-256 is missing or invalid.' }
        $actual = (Get-FileHash -LiteralPath $check.Path -Algorithm SHA256 -ErrorAction Stop).Hash
        if ($actual -ine $check.Expected) { throw "SHA-256 mismatch: $($check.Path)" }
    }
    $python = (Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    if (-not $python) { throw 'Python executable not found.' }
    $global:LASTEXITCODE = -1
    & $python -I -B $helper verify --root "package=$bundle" --manifest $packageManifest
    if ($LASTEXITCODE -ne 0) { throw 'Outer package verification failed or did not start.' }
    $global:LASTEXITCODE = -1
    & $python -I -B $verifier --inventory-tool $helper --pin $expectedObservation.ToLowerInvariant()
    if ($LASTEXITCODE -ne 0) { throw 'Observation verification failed or did not start.' }
    Write-Output 'Both verifications passed.'
}
```

Matching inventories establish file and record integrity; they do not prove historical execution authenticity, rights, privacy or publication permission.
