# Finite expression comparison harness

[日本語](README.ja.md)

This provisional harness generates a bounded ERB fixture from a typed plan, runs pinned Native Emuera and PyEmuera binaries on Windows, and compares the observed values and `RESULT`/`RESULTS` snapshots. It also compares saved logs and checks an evidence seal without starting either engine. The expression validation, fixture generation, strict decoding, marker parsing and comparison logic are derived from the v3 survey runner; the execution controller has been adapted for explicit paths and a shared lock.

For a normal string-return case, use [`fixtures/string-return-plan.json`](fixtures/string-return-plan.json) with the same `plan`, `run`, and `audit` commands. It compares one selected `TOSTR` condition.

The provided plan covers `ABS`, `STRFIND`, and `STRFINDU`. A `different` result means an observed difference or an unmet expected/sentinel constraint; read both observations. Neither a successful run nor the seal establishes complete compatibility. Each run includes a single representative and, when more cases are selected, a full batch. Native can be repeated up to three times; repeated observations and the first single/batch observations must agree.

## Requirements

* Windows with an interactive session able to create a private desktop, Windows PowerShell and CIM access to `Win32_Process`; Native requires a working .NET Framework environment. The exact minimum Framework version has not yet been established.
* Python 3.10 or later; the original run recorded 64-bit Python 3.12.10. No third-party Python packages are required for the harness.
* `Emuera1824+v24.exe`, SHA-256 `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`.
* Public PyEmuera 3.0.0 pyz, SHA-256 `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35`. The pyz contained in the public runtime ZIP has this hash. The engine binaries are not directly included in this harness directory. The [Native distribution and its notices](../vendor/emuera/README.md) are included in the repository; obtain PyEmuera separately and check the applicable distribution conditions.
* The included config is byte-pinned. Input ERB is generated in CP932 with CRLF; an empty `csv` directory is created on each side. Both engine inputs and binary hashes are checked.

## Commands

Run from this directory. Paths below are examples and must be replaced with local paths. These commands do not imply that a live run has already succeeded.

```powershell
python -B harness.py plan fixtures/representative-plan.json
python -B -m unittest discover -s tests -v

python -B harness.py run fixtures/representative-plan.json `
  --native <path-to-Emuera1824+v24.exe> --pyz <path-to-PyEmuera.pyz> `
  --lock-dir <shared-lock-directory> --out <new-output-directory> --repeat-native 2

python -B harness.py compare fixtures/representative-plan.json <native-log> <py-log>
python -B harness.py validate <attempt-directory>
```

`--case CASE_ID` may be repeated for `plan`, `compare`, and `run`. Plan validation checks the whole plan before selecting cases. `run` checks the pinned hashes; it does not download or change the source binaries. It creates a new attempt under `--out`. Select an output location separate from all original fixtures and engine files. The generated fixture and config are copied independently into each side; raw logs and output remain in the attempt. Treat attempts as potentially private: engine output and exception messages may include local paths.

On Windows, Native has exited early when an output location was deeply nested. The cause has not been established; use a short, shallow output path for reruns.

All cooperating Native and measurement jobs **must use the same existing lock directory**. The program atomically acquires `NATIVE_LOCK.json`, refuses either pre-existing `NATIVE_LOCK.json` or `MEASURE_LOCK.json`, rechecks its nonce, and removes only its own lock. It also refuses to start when a matching Native process exists. The private desktop process is terminated only via the handle returned by its own `CreateProcessW`; its disappearance is checked afterwards. A forced termination is recorded separately from a natural exit. A process-name check cannot coordinate unrelated tools that ignore the lock, and an interrupted process can leave a lock for an operator to investigate. Do not delete a lock that belongs to another run.

## CSVBASE B045 representative rerun

`run_csv_b045.py` reruns one registered CSVBASE condition in two Native and one PyEmuera isolated workdirs. If `--repo-root` is omitted, the parent of the script's `harness` directory is the repository root. The output path and both engine binaries are required explicitly; `run` also requires an existing shared lock directory.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -B harness/run_csv_b045.py dry-run `
  --out-root <output-path-outside-repository> `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz>

python -B harness/run_csv_b045.py run `
  --out-root <new-output-path-outside-repository> `
  --lock-dir <existing-shared-lock-directory> `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz>
```

Use `--repo-root <repository-root>` only for a nonstandard placement. Binary hashes are fixed. The command exits nonzero when results are incomplete, diagnostics are unverified, or visual review remains.Inspect `RESULT.json` and its seal. Record schemas are `csv-b045-rerun-dry-run.v1` and `csv-b045-rerun-attempt.v1`. Each mode records input/executable hashes, return/forced termination, stdout/log/crop, lock state, and residual processes. Lock ownership/release failures take precedence over all other results. The nonce and measurement lock are checked before each mode and launch, after process cleanup, and after each mode; a failure stops later launches.

Native uses the existing owned desktop/process-handle control. It waits 6 seconds after launch, attempts a window crop for up to 15 seconds, then the existing `native.py` waits up to 5 seconds and terminates only its own process handle if needed. This differs from the earlier 5-second-after-launch probe and must not be treated as the same timing condition. Per-mode timestamps and elapsed durations distinguish wait, capture, and process completion. Visually inspect both Native crops (`native-01/native-display-crop.bmp`, `native-02/native-display-crop.bmp`) for the correct window, readable text/diagnostic, clipping, or blank capture. Mark unreadable items unobserved. Crops are limited to at most 700×320 pixels at the lower display area; the helper does not guarantee which surface content is visible or that all text fits. AI image review may be used; no human approval is encoded as a runner gate.

The saved B045 records do not provide independently pinned expected diagnostic text for both Native and Py. Public stdout/stderr are retained, but diagnostic meaning remains unverified. Matching markers or termination alone do not establish diagnostic agreement, so results remain `VISUAL_REVIEW_REQUIRED` or `DIAGNOSTIC_UNVERIFIED`; they are not accepted as a successful scoped difference. A record without diagnostic verification remains inconclusive. Postfatal state remains `UNOBSERVED`.


## Evidence and limits

`validate` checks the v3 manifest and seal, exact listed file hashes and no external references. It is an integrity check, not a replay of the results or a proof that the observations are correct. `compare` independently parses the two supplied raw logs but does not verify process receipts. Old v2/v3 historical attempts are not supported by this portable controller; it must not be used to assert that historical evidence was revalidated. `VALIDATION.json` is excluded by the inherited v3 inventory convention and is not covered by the seal.

New expression runs record the whole request and input receipts and perform a semantic audit after sealing. Save the printed lowercase `SEAL.json SHA-256` in a separate trusted record. To audit or reuse a whole attempt without starting either engine, supply that hash and the same plan, selection, repeat count, binaries, config, Python runtime, OS version, preferred encoding, complete process environment and harness code:

```powershell
python -B harness.py audit <attempt-directory> fixtures/representative-plan.json `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz> --repeat-native 2 --seal-sha256 <trusted-seal-sha256>
python -B harness.py resume <attempt-directory> fixtures/representative-plan.json `
  --native <Emuera1824+v24.exe> --pyz <PyEmuera.pyz> --repeat-native 2 --seal-sha256 <trusted-seal-sha256>
```

Supply the same `--case` options and `--config` if used for the run. The environment is pinned by a digest, not stored as plaintext; even an unrelated environment-variable change prevents reuse. Protect the attempt and digest because a digest is not a privacy guarantee. `resume` returns rederived results; it neither starts an engine nor starts a replacement run on failure. The audit checks the sealed inventory, plan-derived fixtures, input and process receipts, raw logs, stage/repeat and single/batch consistency, and rederives comparisons and verdicts. It refuses missing receipts, failures, mismatched inputs and unsealed `VALIDATION.json`, without changing the attempt. A separately trusted hash anchors the supplied bytes; neither it nor semantic consistency proves an untrusted producer actually ran an engine. Old portable v1 attempts lack required receipts and cannot be resumed. Changes to pinned inputs require a new run. There is no per-case checkpoint reuse; other ambient state such as installed frameworks is not fully captured.

To audit in a separate process immediately after a run, keep the same PowerShell session open and use the attempt path and separately saved seal SHA printed by the run. Use the same plan, selected cases, repeat count, executables, config, and Python. A launcher that injects a new process environment for each command can change the environment hash even if you did not change your settings. If it fails, do not bypass or replace the hash check; audit in the session that retains the original pinned environment. The original environment cannot be reconstructed from its hash alone. There is no need to publish environment variable names or values.

Semantic reanalysis principally covers selected observations in the two OUTPUTLOG files. PyEmuera stdout and stderr are checked for sealed byte integrity; the audit does not establish semantic consistency between their diagnostics and the exit code.

The pure-expression controller does not implement GUI, errors, arbitrary ERB or historical scope-reference replay. `--debug` is used for the PyEmuera comparison path; it is part of this test condition. The included unit tests use synthetic logs and mocked process execution, not real engines or a native desktop.

`local_cases.py` runs the original P35 (numeric input), P36 (string input), and P38 (unclosed IF), plus fixed `ARGUMENT` and `RESULT_WRITE` fixtures. The additional `P35_OBS` and `P36_OBS` fixtures add output logging after input. `harness.py run` does not execute these local cases.

```powershell
python -B local_cases.py --case P35 --native <path-to-Emuera1824+v24.exe> `
  --pyz <path-to-PyEmuera.pyz> --lock-dir <shared-lock-directory> --out <new-output-directory>
```

The fixed inputs are P35=`42` and P36=`ABC`. Native input is sent only to the owned PID's input control on its private desktop. At most 700×320 pixels from the bottom of the display surface are saved as a crop. Capture success alone does not establish readable content or a match: inspect the image and Py stdout/stderr. `RESULT_WRITE` checks pre/post values in both OUTPUTLOG files. Save run data in a location protected until privacy review. GUI observations apply only to the selected display and inputs, not IME or arbitrary fixtures.

See [PROVENANCE.md](PROVENANCE.md) for source lineage and fixed inputs, and the [component notices](../LICENSES/README.md) for reuse terms. Download the comparison pyz from the [PyEmuera 3.0.0 release](https://github.com/Meistertech-JP/PyEmuera/releases/tag/v3.0.0), then run `python -B tools/verify_environment.py --native <exe> --pyz <pyz>` from the package root to check both engines.

See the evidence for [PRINTVKW wait release](../evidence/wait-release-20261117/README.md), [evaluation order and diagnostics after a wait](../evidence/wait-c15-20261117/README.md), and [sprite display](../evidence/graphics-gui-observations-20261117/README.md) for their fixtures, settings, and outputs. These conditions are outside the expression and fixed-case commands above. Observe the wait and GUI cases separately with their recorded input and checkpoints.
