# String-array search observations

[64 conditions and outputs](OBSERVATIONS_en.md) · [Machine-readable data](conditions.json) · [Registered case bindings](case-bindings.json) · [日本語](README_ja.md)

These records cover 64 conditions across expression and command forms of FINDELEMENT and FINDLASTELEMENT. They use 61 fixtures and 183 recorded runs; 192 condition/mode references do not represent 192 separate launches. Four GATE conditions share one fixture and three modes. A registered-case link does not change its recorded verdict or establish a new acceptance.

`condition_marker_observed` records a BEFORE marker; it does not prove all arguments or the function body were reached. Native natural termination and post-error RESULT, RESULTS, local and array state are unobserved. These are string-array observations: numeric size4 `[1,2,1,0]` was not executed or checked here. A separate numeric size6 record does not complete that condition or the parent acceptance. No engine is included.

C016 requires fixture and three mode histories from the [existing observation bundle](../observation-adapter-183-20261117/README.md) in the same distribution layout; its PyEmuera stderr is included here. Final privacy and rights decisions for these materials remain separate.

See the [rights guide](../../LICENSES/README.md), [original Emuera license](../../LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](../../vendor/emuera/NOTICE.en.md), and [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt). These notices do not grant a blanket license for survey fixtures and derived records.

## Verification

Run from the distribution root with this material and the peer as siblings under `evidence/`. First obtain trusted SHA-256 values for this manifest, the peer manifest, and `tools/file_set_manifest.py` through an independent channel. The following checks all three before executing the shared tool, verifies both file sets, then executes this bundle's verifier. Python 3.9 or later is required.

```powershell
$BundlePath = 'evidence/find-element-string-64-20261117'
$PeerPath = 'evidence/observation-adapter-183-20261117'
$ToolPath = 'tools/file_set_manifest.py'
$ExpectedBundleSHA = Read-Host 'Trusted bundle manifest SHA-256'
$ExpectedPeerSHA = Read-Host 'Trusted peer manifest SHA-256'
$ExpectedToolSHA = Read-Host 'Trusted file-set tool SHA-256'
$ExpectedBundleSHA = $ExpectedBundleSHA.ToLowerInvariant()
$ExpectedPeerSHA = $ExpectedPeerSHA.ToLowerInvariant()
$ExpectedToolSHA = $ExpectedToolSHA.ToLowerInvariant()
if (($ExpectedBundleSHA -notmatch '^[0-9a-f]{64}$') -or ($ExpectedPeerSHA -notmatch '^[0-9a-f]{64}$') -or ($ExpectedToolSHA -notmatch '^[0-9a-f]{64}$')) { throw 'Invalid SHA-256' }
function Get-CheckedSHA256([string]$InputPath) {
    try {
        $AbsoluteInputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($InputPath)
        $InputStream = [System.IO.File]::OpenRead($AbsoluteInputPath)
        try {
            $HashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
            try { return [BitConverter]::ToString($HashAlgorithm.ComputeHash($InputStream)).Replace('-', '').ToLowerInvariant() }
            finally { $HashAlgorithm.Dispose() }
        } finally { $InputStream.Dispose() }
    } catch { throw 'Required SHA-256 could not be computed' }
}
if ((Get-CheckedSHA256 "$BundlePath/manifest.json") -cne $ExpectedBundleSHA) { throw 'Bundle manifest mismatch' }
if ((Get-CheckedSHA256 "$PeerPath/file-set-manifest.json") -cne $ExpectedPeerSHA) { throw 'Peer manifest mismatch' }
if ((Get-CheckedSHA256 $ToolPath) -cne $ExpectedToolSHA) { throw 'Tool mismatch' }
# Resolve an application without executing it; missing Python must terminate the script.
try { $PythonPath = (Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source }
catch { throw 'Python executable unavailable' }
if ([string]::IsNullOrWhiteSpace($PythonPath)) { throw 'Python executable unavailable' }
function Invoke-CheckedPython([string[]]$PythonArgs) {
    # A failed process launch must not reuse the previous native exit code.
    $global:LASTEXITCODE = $null
    try {
        & $PythonPath @PythonArgs
        if ($null -eq $LASTEXITCODE -or $LASTEXITCODE -ne 0) { throw 'Python verification failed' }
    } catch { throw 'Python verification failed or could not be started' }
}
Invoke-CheckedPython -PythonArgs @('-I', '-B', $ToolPath, 'verify', '--manifest', "$BundlePath/manifest.json", '--root', "bundle=$BundlePath")
Invoke-CheckedPython -PythonArgs @('-I', '-B', $ToolPath, 'verify', '--manifest', "$PeerPath/file-set-manifest.json", '--root', "evidence=$PeerPath")
Invoke-CheckedPython -PythonArgs @('-I', '-B', "$BundlePath/verify.py", '--peer', $PeerPath, '--inventory-tool', $ToolPath, '--pin', $ExpectedBundleSHA, '--peer-pin', $ExpectedPeerSHA, '--tool-pin', $ExpectedToolSHA)
```

The fixed bindings and manifests check consistency; they do not authenticate the past execution, publisher, rights or publication approval. Updating a trusted pin requires independent comparison with the original materials.
