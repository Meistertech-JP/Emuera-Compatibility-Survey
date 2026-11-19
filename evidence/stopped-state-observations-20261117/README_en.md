# Limited stopped-state observations

[日本語](README_ja.md)

This record summarizes selected global and cell observations from four saved SWAP and numeric-assignment conditions. It adds no engine run or GUI action.

## Observations and diagnostics

- **SWAP normal control:** Native built-in Debug console literal reads observed D:0/D:1 changing from 11,22 to 22,11. PyEmuera's before values come from an execution output marker; after values come from explicit entries in a PDB storage-map snapshot.
- **SWAP second-index error:** Execution stopped at line 5. Native Debug console reported D index 1,000,000 outside the 1,000-element array range. PyEmuera recorded `E_INDEX` at line 5 for D index 1,000,000 outside dimension `(1000,)`. Native directly read the two cells twice in the same stopped process. PyEmuera captured its storage map twice in the same stopped VM, with explicit entries `(0,):11` and `(1,):22`; no per-cell get command is recorded.
- **Numeric assignment control:** Native literal reads observed 31,47 then 7,9. PyEmuera observed explicit `(0,):7` and `(1,):9` entries in its PDB map. These are map observations, not individual cell gets.
- **Numeric bad-index stop:** Execution stopped at line 14. Native Debug console reported ZZV index 2 outside the two-element array and directly read ZZV:0/1 twice in the same stopped process, observing 0,0. PyEmuera recorded `E_INDEX` at line 14 for ZZV index 2 outside dimension `(2,)`. Its PDB displayed shape `[2]`, sparse map `{}`, and default `0` twice in the same stopped VM. No per-cell get is saved. The pinned `pyemuera/data.py` uses `values.get(tuple(key), default)` for valid keys, so the effective ZZV:0/1 values 0,0 are inferred from source. This is distinct from Native's direct cell readback.

Diagnostic summaries in the record point to source pin IDs and SHA-256 values for the Native UIA and Py error records. Engine wording and observation methods are kept distinct; the record does not claim identical error representations or exit outcomes. Each pair of reads is repeated within one stopped process/VM, not two independent executions.

## Source ID and observed scope

The numeric bad-index condition cites source case ID `OPISOLATED265_plain-num-badindex`, which is associated in the comparison register with both `=` and `==`. This stopped-state fixture uses `ZZV:ZZIDX() = ZZL()`; the only target role actually executed and observed here is `=`. The `==` role is not executed or observed by this condition. Do not read the register association as the observation scope of this fixture. The machine-readable `source_scope_binding` records the same distinction.

## Scope and limits

[`observations.json`](observations.json) records case IDs, typed keys, input and engine hashes, observation methods, diagnostic summaries and source pins, inference, values, and unobserved limits. It makes no claim about full state, natural exit, LOCAL/REF, every array, or absence of transient setters.

Original raw bytes, Native UIA records, Py PDB records, and fixtures are not included. The SHA values link each summary to preserved bytes, but a reader cannot independently recheck the diagnostics or state from this bundle alone without those bytes.

## Verification

Set the bundle root as the working directory. Before starting Python, compare both `verify.py` and `manifest.json` SHA-256 values with expected values obtained through an independent trusted channel outside this bundle. Values copied from this README, the manifest, records, or another file distributed in the same bundle are not independent checks. No independent pin issuer or channel is designated here. If either expected value is unavailable, pre-execution authenticity remains unconfirmed.

PowerShell example (replace both placeholders with values obtained independently before running):

```powershell
Set-Location -LiteralPath '<unpacked bundle root>'
$expectedVerifier = '<SHA-256 of verify.py from an independent trusted channel>'
$expectedManifest = '<SHA-256 of manifest.json from the same independent trusted channel>'
$actualVerifier = (Get-FileHash -LiteralPath .\verify.py -Algorithm SHA256).Hash.ToLowerInvariant()
$actualManifest = (Get-FileHash -LiteralPath .\manifest.json -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualVerifier -ne $expectedVerifier.Trim().ToLowerInvariant()) { throw 'verify.py SHA-256 mismatch; do not run Python' }
if ($actualManifest -ne $expectedManifest.Trim().ToLowerInvariant()) { throw 'manifest.json SHA-256 mismatch; do not run Python' }
python -B .\verify.py
```

This fixed verifier checks the observations hash, file hashes and sizes listed in the manifest, relative links, and selected constraints on case and typed-key bindings, diagnostic pins, and unobserved fields. It does not independently prove every record value, the semantic correctness of observation methods or repeats, source-register associations, or correspondence to excluded raw bytes. Original raw files, Native UIA records, Py PDB records, and fixture bytes are not included, so this bundle alone cannot trace measurements or diagnostics back to those originals. A hash-check PASS does not prove that every observation claim is true. If records or sources change, compare them separately with the original register and raw evidence, and independently pin the new `verify.py` before running it.
