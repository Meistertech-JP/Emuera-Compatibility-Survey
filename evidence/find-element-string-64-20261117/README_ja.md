# 文字列配列検索の観測

[64条件と出力](OBSERVATIONS_ja.md) · [機械可読データ](conditions.json) · [登録caseとの対応](case-bindings.json) · [English](README_en.md)

FINDELEMENT / FINDLASTELEMENTの式・命令の4役割について、64条件の保存記録を示します。61 fixture・183記録実行で、192条件別mode参照は192回の独立起動ではありません。GATEの4条件は1 fixtureと3 modeを共有します。登録caseとの対応は元判定の変更や新しい受入を意味しません。

`condition_marker_observed` はBEFORE markerの観測であり、引数すべてや関数本体の到達を証明しません。Nativeの自然終了とエラー後のRESULT・RESULTS・local・配列は未観測です。文字列配列に限る観測で、数値size4 `[1,2,1,0]` は今回実行・照合していません。別の数値size6の記録はこの条件や親受入の代替完了を示しません。エンジン本体は含みません。

C016のfixtureと3 mode rawには、同じ配布構成内の[既存観測資料](../observation-adapter-183-20261117/README.ja.md)が必要です。PyEmuera stderrは本資料に含みます。参照先を含めて権利・privacyの最終判断は別途必要です。

[権利表示](../../LICENSES/README.ja.md)、[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)を参照してください。これらの表示は調査fixture・派生記録全体への一括許諾ではありません。

## 検証

この資料とpeerを `evidence/` の同じ階層に置いた配布ルートで実行します。先に、信頼できる別経路から本資料manifest、peer manifest、共通 `tools/file_set_manifest.py` のSHA-256を取得してください。次の手順は、その3値を比較してから共通toolを実行し、本資料のverifierを検証してから実行します。Python 3.9以降が必要です。

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

固定対応表とmanifestは整合性検査であり、過去の実行の真正性・発行者・権利・公開承認を証明しません。信頼pinの更新時には原資料との独立照合が必要です。
