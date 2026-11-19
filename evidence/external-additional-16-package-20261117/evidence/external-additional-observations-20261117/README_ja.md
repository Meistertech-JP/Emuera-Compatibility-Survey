# 外部資料：追加16ケースの保存観測

[16ケースの条件・記録出力](OBSERVATIONS_ja.md) · [機械可読記録](records.json) · [English](README_en.md)

4件の式、8件のPRINT関連テキストログ、4件のエンジン診断を収録しています。原資料は調査凍結の外にあり、当時記録されたSHAと照合した外部記録です。88ケース中、先行29件とは重ならない追加16件で、残る43件は本資料に含みません。非収録は観測が存在しないことを意味しません。

画面の見た目やログにない値は推測していません。Nativeの自然終了・エラー後の状態は確認できた範囲に限ります。2件のENCODETOUNIではNative入力probeの当時SHAが未確認で、probeは現在の読戻しです。PRINT系8件とこの2件のPyEmuera側config等は選択receiptだけでは確定できません。原rawに含まれる診断と未観測の区別を維持しています。

## 権利と再実行の範囲

配布単位のルートにある `notices/README.ja.md` は、同伴するEmuera原license・日英NOTICEとPyEmueraのlicense・第三者表示を案内します。Emuera NOTICEは別に保全された原ZIP配布単位を説明し、この資料にそのZIPが含まれる意味ではありません。PyEmueraの第三者表示とSOURCESも元PyEmuera配布物の説明です。engineは同梱していません。fixture・設定・rawなどの作者と再配布権限、privacyは別途確認が必要であり、同伴表示は公開許諾を意味しません。

保存観測の閲覧とオフライン検証を目的とし、完全な実行環境や元receipt一式は含みません。engineや環境が異なる追試の結果は保証しません。

## オフライン検証

検証コード、helper、両manifestの期待SHAは配布単位とは独立した信頼経路で取得してください。下の4つのplaceholderを独立経路で得た信頼済みSHAに置き換えてください。未設定・hash取得失敗・不一致・Pythonが見つからない／起動不能・いずれかの検証失敗では停止します。外側packageを先に検証します。

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

一致はファイルと記録の整合性を示し、歴史的実行の真正性、権利、機密または公開許諾を証明しません。
