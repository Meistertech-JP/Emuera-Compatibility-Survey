# Limited legacy evidence adapter

[日本語](LEGACY_EVIDENCE.ja.md)

`legacy_evidence.py` selects **one typed target** from a pinned audit snapshot and checks declared SHA-256 references and selected identity, case-ID and outcome fields for three observed layouts and a narrowly scoped PRINTC/PRINTLC layout. It is read-only; it does not anonymize data, change historical decisions, update a ledger or launch an engine. All test fixtures are newly generated synthetic data; no private source evidence is copied into the tests.

| Layout | Checked | Limitation |
|---|---|---|
| `parent-target-finite-scope-adjudication-1` | Typed acceptance, declared comparison, fixture and logs/config for supported mode names | Receipt locators are unpinned; the comparison is not promoted to an independent readback; output semantics are not replayed |
| `phase2-target-parent-acceptance/v1` | Typed acceptance, audit-declared readback hash, acceptance backlink and case IDs; typed target/outcome when present | No outcome is invented for an outcome-less readback; hash-only or unlocated raw references and recorded counts are not verified |
| `original-return-three-parent-acceptance-1` | Typed acceptance, pinned readback, selected case's mode raw/stderr/receipt and optional probe pins | Other observations are not checked; a target-name list is not independent typed-target evidence |
| `target-finite-comparison-adjudication-1`, restricted to PRINTC/PRINTLC column-boundary | Pinned case register, acceptance and manifest; three mode inputs, config, output logs and receipts; Native probes and executables; fixture conditions, serialized columns and sentinels | Other targets using this schema are unsupported; the Py pyz bytes are not verified. No full requirements or Native natural-exit proof |

The output keeps the original audit `row_outcome`, available `declared_outcome`, checked references and original `gaps` distinct. `PARTIAL` means bounded checks were possible, not that the target or compatibility is complete. `UNSUPPORTED` means the acceptance or layout is not recognized; missing/unpinned, changed, contradictory or unsafe inputs are `INVALID`. No hash, readback or natural exit is backfilled.

## Usage

Requires Python 3.10 or later. Supply an evidence root, an audit JSON path relative to that root, and its **independently trusted SHA-256**. This is only a syntax example and does not assert that any evidence file is publicly available.

```powershell
python -B tools/legacy_evidence.py --root <evidence-root> `
  --audit <root-relative-audit.json> --audit-sha256 <audit-sha256> `
  --kind command_or_syntax --name <target-name>
```

The supported audit schema is `read-only-uniform-acceptance-chain-audit-1` with `rows`. References are root-relative; legacy Windows separators are normalized. Absolute paths, parent traversal, symlinks/reparse points, duplicate references, missing files and absent or incorrect pins are rejected. An anonymized derivative has different hashes: keep original pins intact and provide a separately auditable derivative mapping.

Exit code `1` means `INVALID`; `2` means `PARTIAL` or `UNSUPPORTED`. The adapter deliberately has no full-validation success exit. Output may contain relative paths, case IDs and gaps from the input and must itself be reviewed before sharing. A hash supplied alongside an untrusted input is not authentication. Concurrent modifications are not an atomic snapshot.

For the original three layouts case-role links are read from the pinned audit snapshot without rechecking the case register. For the restricted PRINTC/PRINTLC layout, the audit-pinned case-register snapshot, typed target and case pointer are also checked. Semantic sufficiency of requirements, all raw modes, application to all 226 historical targets, public relocation of private references, and rights/privacy review remain outside this adapter.

```powershell
python -B -m unittest discover -s tests -p 'test_legacy*.py' -v
```

## PRINTC / PRINTLC scope

The pinned parent record binds `native-01`, `native-02` and `public-01` separately. The check covers empty text, three ASCII characters and 25-character text, their serialized output, `RESULT=777` and `RESULTS=SENTINEL`. Three modes share one fixture; the two cases and six conditions are not separate launches. Native natural exit is not established. The Py executable is identified from receipt hashes only; its bytes are not checked. Actual paths and management fields inside receipts are not printed; relative paths, case IDs and gaps appear in the output.

The source audit, acceptance, fixture, config, raw, receipts and engines are not included in this tool. This material alone does not establish that the historical execution can be reproduced or rechecked. Rights and publication conditions for the source fixtures and output need separate confirmation. Swapping byte-identical raw files cannot be detected from those bytes; the separately pinned mode receipts and their recorded content are checked.
