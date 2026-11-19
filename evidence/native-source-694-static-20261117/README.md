# Static Native source-location index for 694 targets

[日本語](README.ja.md)

`targets.jsonl` contains one row per typed target: name and kind together identify each of 694 entries. It records source locations and limited checks against v24. The original integration table, source code text, and execution results are not included. A recorded location does not prove successful execution, matching results, complete implementation, or coverage.

## Counts and scope

| Category | Count | Meaning |
| --- | ---: | --- |
| Location recorded in the original integration table | 661 | 425 targets with structured static records and 236 with independently recorded anchors |
| No location in that table | 33 | Includes the three commented candidates and 30 targets without a source line in this index |
| Commented candidates within those 33 | 3 | CHKVARDATA, CHKGLOBALDATA, and FIND_VARDATA: comment locations from a separate audit checked in the v24 ZIP; not counted as active registrations |
| No source line in this index within those 33 | 30 | 29 operators and SET; IL offsets were not converted into source lines |

A later [source-location supplement](../native-source-operator30-20261117/README.md) separately identifies the v24 operator dictionary and internal assignment path for these 30 targets. This index retains the fact that the original integration table did not record their locations.

For 425 targets, the recorded registration text was found on the specified line in the original v24 ZIP: 385 matched the entire trimmed line and 40 matched a substring. For 361 definition ranges and 61 validator ranges, only the file bounds were checked. Of the 236 independently recorded targets, 154 have a same-name key at the recorded line in the v24 function-method dictionary. The remaining 82 locations are not claimed to have been confirmed against v24 here. The 425, 154, and three commented candidates are disjoint groups.

A later [v24 location supplement](../native-source-anchor82-20261117/README.md) identifies corresponding syntax locations for those 82 targets. The version and SHA of the historical files referenced by the original anchors remain unestablished.

For the 154 command-form targets, a same-name function-method dictionary key does not establish command-form registration, routing, or execution. For the three comments, the separate audit's absence of a literal in the dictionary initializer does not establish absence from every other registration path. The [existing 75 API targets](../api-gap75-static-20261117/README.md) are already included in the 694: 34 in the group of 425 and 41 in the group of 154. They are not additional targets.

`historical_a7` and `historical_a8` label historical audits included on the PyEmuera side; they are not Emuera version names. Historical locations are not assumed identical to v24. Some independent anchors give only a filename, so their version, directory, and role cannot all be assigned to v24. `v24_audit` and `v24_same_name_function_dictionary` express the limited checks above.

`v24_source_file_sha256` is the SHA-256 of an entire source file in the v24 ZIP. `contract_declared_sha256` is a digest recorded in the original audit's contract field and is not necessarily a whole-file digest. For GCREATED, GWIDTH, and GHEIGHT, the UTF-8 SHA of the recorded registration text differed from the contract digest, so this index retains its initial `mismatch_unresolved` status. A [later supplement](../native-source-sha-supplement-20261117/README.md) reproduces all three contract digests from the v24 source and the saved generator, hashing the original text including the comment and CR. This is not a mismatch of the v24 whole-file SHA and does not authenticate the code used at the time.

## Access the original source

The [Emuera distribution](../../vendor/emuera/README.md), `Emuera1824-v24-with-notices.zip`, contains two accompanying notices and the unmodified `Emuera1824+v24.zip`. The original inner ZIP has SHA-256 `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a`. It contains source files directly under `Emuera1824+v24/src1824+v24/src1824/Emuera/`; the v24 `file` values in this index are relative to that directory.

From the repository root, use a fresh working directory called `WORK` to extract the two levels. Verify the inner ZIP against the SHA above using a trusted SHA-256 tool, and keep the notices with the inner ZIP.

```text
python -m zipfile -e vendor/emuera/Emuera1824-v24-with-notices.zip WORK/outer
python -m zipfile -e WORK/outer/Emuera1824+v24.zip WORK/unpacked
```

For example, `GameData/Function/Creator.cs` is at `WORK/unpacked/Emuera1824+v24/src1824+v24/src1824/Emuera/GameData/Function/Creator.cs`. A text viewer and SHA-256 tool can inspect the stated lines and file digests; starting the engine is unnecessary.

## Verify file integrity

Use Python 3.9 or later. First obtain trusted SHA-256 values for this index's `manifest.json` and the shared `tools/file_set_manifest.py` through a **separate trusted channel**. Values supplied only within the same distribution are not an independent trust anchor. Run this PowerShell example from the repository root after replacing both placeholders with those trusted values:

```powershell
$expectedManifest = '<trusted-manifest-sha256>'
$expectedTool = '<trusted-tool-sha256>'
$manifest = 'evidence/native-source-694-static-20261117/manifest.json'
$tool = 'tools/file_set_manifest.py'
if ($expectedManifest -notmatch '^[0-9a-fA-F]{64}$' -or $expectedTool -notmatch '^[0-9a-fA-F]{64}$') { throw 'Trusted SHA-256 values are required' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $manifest $expectedManifest
if ($LASTEXITCODE -ne 0) { throw 'Manifest SHA-256 mismatch' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $tool $expectedTool
if ($LASTEXITCODE -ne 0) { throw 'Tool SHA-256 mismatch' }
python -I -B $tool verify --manifest $manifest --root index=evidence/native-source-694-static-20261117
if ($LASTEXITCODE -ne 0) { throw 'File-set verification failed' }
```

The manifest verifies this directory's file set, sizes, and SHA-256 values. An externally trusted pin detects changes to the pinned files; it does not prove the original table's content, provenance, execution, the meaning of each row, or permission to publish. The omitted original table cannot be verified using this procedure. The shared tool, rights notices, and Emuera ZIP are outside this manifest and require separate verification.

## Rights and distribution status

The [original Emuera license](../../LICENSES/Emuera1824-v24-license-original.txt) and [English NOTICE](../../vendor/emuera/NOTICE.en.md) describe the referenced Emuera distribution. See also the [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). Those notices do not automatically grant rights over the entire research index, original integration table, or explanatory text. The rights holders and distribution terms for the research materials remain unresolved, and publication conditions have not been approved.
