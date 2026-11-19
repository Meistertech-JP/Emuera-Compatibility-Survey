# Follow-up: registration contract hashes for three functions

[日本語](README.ja.md)

A later static comparison reproduced the contract hash inputs for GCREATED, GWIDTH and GHEIGHT, which the [694-target static index](../native-source-694-static-20261117/README.md) recorded as unresolved. The scope is the v24 registration of these three expression functions. The index itself is unchanged: its `mismatch_unresolved` records the earlier state, and this supplement explains the three hash differences. This does not establish runtime results, compatibility, the status of other registrations, or approval of the overall publication.

## Reproduced inputs

For each line in `GameData/Function/Creator.cs` in the original ZIP, SHA-256 of the UTF-8 encoding of the original text from the start of the registration through the character before the next LF matches the contract hash. These three source lines use CRLF: the slice excludes the leading indentation, includes the comment and CR, and excludes LF. The displayed registration text is the same range with the comment and CR replaced with spaces; its UTF-8 SHA-256 differs from the contract hash. Trailing spaces in that displayed text are included in its hash.

| Expression function | Line | Contract SHA-256 | Displayed registration text UTF-8 SHA-256 |
| --- | ---: | --- | --- |
| GCREATED | 171 | `63aee4d35c0444cee4e06ee292f691e768246b8673db9919ea0af407e1ccd660` | `e40541b2e9829f720873c61115f638a92d847e8aa8f0324fbe6c0fe12544115d` |
| GWIDTH | 172 | `471ccf05062354021044d22fedbb2ca7d72acc19aa58a2c53aec5acfb6c510eb` | `83ebe1e884c7c4e81c5b8fc1c28353a6093de4195efbe92568171e31747b4d73` |
| GHEIGHT | 173 | `5bfab797a278a3c5065d6c2478c7ce7a2c508014b9d674e33581206b0e6efd6c` | `976c26bf693ad4ede9a2781b5086970bd34de732eabfadefcd62cc47a28f5d6e` |

Machine-readable values are in [results.json](results.json). The source location is relative to `Emuera1824+v24/src1824+v24/src1824/Emuera/` inside the original ZIP. The original ZIP SHA-256 is `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a`; the complete source file SHA-256 is `b2e5f60c5457741208ba99b991cced5106b22834b00347876dea411a3e0dd36a`. See the [Emuera distribution guide](../../vendor/emuera/README.md).

The results were reproduced using the retained generator `reference_contracts.py` (SHA-256 `bdb2837519e499908e48af065ea4f1b8ef43c8d649f239691303361a818b12e4`) and the source above. This supplement does not include the generator, original audit record, or original source. Reproduction with the retained copy does not prove the authenticity of the code actually used at the time or the historical execution.

## Verify file integrity

Use Python 3.9 or later. Obtain trusted SHA-256 values for this supplement's manifest and the shared tool through a separate trusted channel, then verify them from the repository root. Values supplied only within the same distribution are not an independent trust anchor.

```powershell
$expectedManifest = '<trusted-manifest-sha256>'
$expectedTool = '<trusted-tool-sha256>'
$manifest = 'evidence/native-source-sha-supplement-20261117/manifest.json'
$tool = 'tools/file_set_manifest.py'
if ($expectedManifest -notmatch '^[0-9a-fA-F]{64}$' -or $expectedTool -notmatch '^[0-9a-fA-F]{64}$') { throw 'Trusted SHA-256 values are required' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $manifest $expectedManifest
if ($LASTEXITCODE -ne 0) { throw 'Manifest SHA-256 mismatch' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $tool $expectedTool
if ($LASTEXITCODE -ne 0) { throw 'Tool SHA-256 mismatch' }
python -I -B $tool verify --manifest $manifest --root supplement=evidence/native-source-sha-supplement-20261117
if ($LASTEXITCODE -ne 0) { throw 'File-set verification failed' }
```

The manifest checks this supplement's file set, sizes and hashes. External pins help detect changes but do not prove the source material's authenticity, the meaning of its contents, historical execution, or rights. The shared tool, index, rights notices and original ZIP are outside this manifest.

## Rights and notices

See the [original Emuera license](../../LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](../../vendor/emuera/NOTICE.en.md), [PyEmuera license](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt), and [third-party notices](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). These notices concern their respective referenced materials and do not automatically grant rights to all survey outputs including this supplement. The rights holders and distribution terms for the survey materials remain unresolved.
