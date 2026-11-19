# LOADGLOBAL: comparison with truncated save data

[日本語](README_ja.md) · [Machine record](records.json) · [Isolated runner](runner.py) · [File inventory](manifest.json)

`LOADGLOBAL_CORRUPT_TRUNCATION_20261115` records a bounded comparison using truncated global save files in each engine's own format. The original case verdict is `different_scoped`; the target is `command_or_syntax:LOADGLOBAL`. Native and PyEmuera use different formats and bytes. This is not a comparison of the same file or a cross-format compatibility test.

Both use the same [ERB](fixture/ERB/SEARCHBOUND01.ERB), [ERH](fixture/ERB/GLOBAL205.ERH), and [configuration](fixture/emuera.config), with empty CSV input. Before `LOADGLOBAL`, the fixture sets `GLOBAL:0=900`, `GLOBAL:1=901`, `GLOBALS:0="SENTINEL0"`, `GLOBALS:1="SENTINEL1"`, the first three user numeric values to `901,902,903`, the two user strings to `MUT0,MUT1`, and `RESULT=777`.

Native [global.sav](fixture/native/global.sav) is the first 163 bytes of a 273-byte valid save; PyEmuera [global.json](fixture/public/global.json) is the first 441 bytes of its 557-byte valid save. Each comes from its corresponding engine's format. The complete valid seed files are not included.

The retained logs contain one recorded run per engine. `USER*` denotes `ZZ205G`; `USERS*` denotes `ZZ205GS`.

| Output | Native | PyEmuera |
|---|---|---|
| `RESULT` | 0 | 0 |
| `GLOBAL0`, `GLOBAL1` | 50, -51 | 900, 901 |
| `GLOBALS0`, `GLOBALS1` | BUILTIN0, BUILTIN1 | SENTINEL0, SENTINEL1 |
| `USER0`, `USER1`, `USER2` | 901, 902, 903 | 901, 902, 903 |
| `USERS0`, `USERS1` | MUT0, MUT1 | MUT0, MUT1 |
| `CORRUPT_LOAD_CONTINUED` | present | present |

The [Native log](observed/native/emuera.log) and [Py log](observed/public/emuera.log) are UTF-16. Py [stdout](observed/public/stdout.bin) and [stderr](observed/public/stderr.bin) are also retained. Stderr contains `E_SAVE: Invalid save: Expecting value: line 1 column 442 (char 441)`; the saved receipt recorded exit code 0. The historical Native process had not exited after five seconds, and the cleanup call to terminate the owned process was recorded as successful. The subsequent wait result, Native natural exit, exit code, and GUI diagnostics were not observed. OUTPUTLOG or the continuation marker does not prove natural termination. The comparison covers only these two corruptions, not permissions, game identity or version mismatch, all saved variables, or other truncation positions.

## Isolated runner

Install this bundle at `evidence/loadglobal-corrupt-20261117/` within the repository and explicitly provide that repository's `harness/` directory. A Windows interactive session, Python 3.10 or later, a .NET Framework runtime, an existing shared lock directory, and the two separately supplied pinned engines are required. `--out-root` is mandatory and must be an **existing directory outside the repository**. Do not select a game or existing saves directory.

Before execution, obtain trusted expected SHA-256 values for the manifest and `runner.py` through an independent channel and check both with an OS hash utility. The included files alone do not establish authenticity. The runner checks the specified manifest and complete bundle, the five repository harness sources, and the specified engine hashes. If a pinned file changes, stop and use pins for a separately reviewed version.

### Read-only dry-run

From the bundle directory in PowerShell, replace the placeholders with real paths and a trusted SHA. `$OutputRoot` must already exist and must be neither inside nor an ancestor of the repository.

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

The dry-run creates or changes no files and starts no engine, process lookup, or lock acquisition. It checks the bundle, harness, engines, output location, and input-placement plan. It does not test write access to the output directory. If `--lock-dir` is supplied it only reads lock presence; that does not guarantee acquisition at run time.

### Rerun on the engines

For `--lock-dir`, specify an existing shared lock directory that is neither inside nor an ancestor of the repository, and use the same lock as other cooperating users. Choose a new attempt name. The runner copies separate inputs into a new attempt under the output root and observes Native for up to five seconds on an isolated desktop. If its process remains, it terminates that owned handle only. Other processes with the same name are never terminated: they block startup, and if detected afterward they prevent the Py run.

```powershell
$SharedLock = (Resolve-Path -LiteralPath '<EXISTING_SHARED_LOCK_DIRECTORY>').Path
python -I -B runner.py --run --repository-root $Repo --harness-dir $HarnessDir `
  --out-root $OutputRoot --manifest-sha256 $ManifestPin --native $NativeExe --pyz $PyZ `
  --lock-dir $SharedLock --attempt-name 'loadglobal-truncation-01'
if ($LASTEXITCODE -ne 0) { throw "Run incomplete or failed (exit $LASTEXITCODE); inspect retained output" }
```

The lock does not coordinate tools that do not use it. Existing attempts are never overwritten. `<out-root>/<attempt-name>/` retains each engine's work, save bytes in `snapshots/before/` and `snapshots/after/`, Native log, Py log/stdout/stderr, `RESULT.json`, and the file inventory taken before that result file. This runner does not sign or seal results. Created output is retained where possible on error or timeout. It may contain local information and needs review before sharing.

`CAPTURED` means the selected markers appeared in both logs; it is not final acceptance or full compatibility. Native natural exit and forced termination, and Py nonzero and timeout, are distinguished. Py nonzero is returned when possible; timeout exits 124. Native GUI diagnostics are not captured. Actual engine execution has not been confirmed by this dry-run.

Pinned engine SHA-256: Native `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`; PyEmuera 3.0.0 pyz `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35`. See `HARNESS_PINS` in `runner.py` for the five fixed harness source hashes. Hashes identify bytes; they do not establish execution or publisher authenticity.

## Notices

[Original Emuera license](licenses/Emuera1824-v24-license-original.txt) · [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt) · [third-party notices](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). These notices concern the original engine distributions; they do not by themselves establish authorship or redistribution permission for all fixture, corrupt-save and log material. Rights and privacy for each item require review before publication.
