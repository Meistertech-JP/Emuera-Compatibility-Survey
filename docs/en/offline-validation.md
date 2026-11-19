# Offline validation

[日本語](../ja/offline-validation.md) | [Reading the survey data](results.md)

Use Python 3.10 or later and run the commands from the root of the extracted candidate. The checks in this guide read selected files and records offline. They require neither engine.

Use any independently trusted SHA-256 values or signatures you have to identify the manifests and verifier scripts before running these commands. Success establishes the checks described for the selected bundle. The original execution, provenance and distribution rights require separate evidence.

## Package inventory and survey ledger

From the package root, verify the complete file set, SHA-256 hashes, and sizes. Verify the manifest's own SHA-256 using a separate trusted record.

```powershell
python -B tools/file_set_manifest.py verify --root repo=. --manifest manifests/public-file-set.json
python -B results/verify.py
python -B results/test_verify.py
python -B tools/verify_environment.py
```

The ledger negative controls alter disposable copies to confirm that missing or changed data is rejected. Checking saved comparisons and running the engines are separate procedures.

## File sets for seven selected bundles

The shared [file-set tool](../../tools/FILE_SET_MANIFEST.md) checks the file set, sizes and SHA-256 values of a directory against its manifest. Run the command for the bundle you want to check. The names `bundle`, `layer` and `evidence` are the root names recorded in the respective manifests.

```powershell
python -I -B tools/file_set_manifest.py verify --manifest evidence/compound-trailing-comma-20261117/manifest.json --root bundle=evidence/compound-trailing-comma-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/legacy-acceptance-269-20261117/manifest.json --root layer=evidence/legacy-acceptance-269-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/nine-saved-observations-20261117/manifest.json --root evidence=evidence/nine-saved-observations-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/parent-restoration-40-20261117/manifest.json --root evidence=evidence/parent-restoration-40-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/twaitzero-observation-20261117/manifest.json --root bundle=evidence/twaitzero-observation-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/wait-c15-20261117/manifest.json --root evidence=evidence/wait-c15-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/wait-release-20261117/manifest.json --root evidence=evidence/wait-release-20261117
```

Exit code 0 and `verify: OK` mean the selected file set matches its manifest. See each README for the observations and their limits:

- [Compound-assignment trailing comma](../../evidence/compound-trailing-comma-20261117/README_en.md) and [nine saved observations](../../evidence/nine-saved-observations-20261117/README.md)
- [Historical acceptance references](../../evidence/legacy-acceptance-269-20261117/README.md) and [parent-case restoration records](../../evidence/parent-restoration-40-20261117/README.md)
- [TWAIT 0,1](../../evidence/twaitzero-observation-20261117/README.md), [WAIT C15](../../evidence/wait-c15-20261117/README.md), and [WAIT release](../../evidence/wait-release-20261117/README.md)

## Representative examples and case register

The [representative observations](../../differences/representative-20261116/README.en.md) use `differences/representative-20261116` and `evidence/representative-20261116` together. This check covers selected files, recorded settings and some output markers for four cases; it does not reproduce them with an engine.

```powershell
python -I -B differences/representative-20261116/verify.py
```

The [case register](../../evidence/case-register-2898-20261117/README.md) uses a different format. For example, run:

```powershell
python -I -B tools/query.py SEARCH02_STRFINDU_A_NEG1
```

Inspect `case_register_projection_availability` and `case_register_projection` in the output. If the survey or trace state is `NOT_INSTALLED` or `SNAPSHOT_MISMATCH`, the corresponding comparison was not performed. The query checks projection hashes, counts and the matching row, among other things; it does not emit the detailed fields or validate the meaning of every case.

## Legacy references and saved observations

Run the saved-evidence verifier from the candidate root.

```text
python -B tools/verify_saved_evidence.py
```

The verifier checks the locator and saved-observation records. It checks the sizes and hashes of included bytes, the case IDs, pointers and source hashes for derived references, and the absence of paths for private originals. Its output summarizes the records present in the extracted candidate. See the [legacy reference guide](results.md#legacy-references).

## Limits

Some bundles include selected raw files, fixtures, screenshots or receipts. The historical acceptance records, parent-case restoration records and case register do not include the corresponding original records or raw observations. Even where selected raw files are included, the full history of the original run, whether input was consumed, or natural process exit may remain unverified. Consult each README for its unobserved scope.

[`results/verify.py`](../../results/verify.py) checks the survey and differences index. For older records, the lookup distinguishes relative references to included bytes from derived observations and references whose originals are withheld. The candidate has yet to establish independent reproduction of the complete historical survey. See the [legacy reference guide](results.md#legacy-references).
