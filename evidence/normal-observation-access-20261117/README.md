# Saved PRINT SINGLE observations: ten conditions

[日本語](README.ja.md)

[observations.json](observations.json) records input conditions, original case verdicts, and saved history and state for two Emuera modes and one PyEmuera mode for ten selected PRINT SINGLE conditions. The three modes belong to one shared batch containing twenty conditions; these are not ten separate executions. Relative references, SHA-256 values, and half-open byte ranges point to the fixture, configuration and histories in the [eight-group index](../multi-group-101-20261117/index.json) and its [guide](../multi-group-101-20261117/README.md). Line breaks and spaces in the JSON are part of the observations.

For example, C196_13 has `P><T` in the Emuera history, while the PyEmuera history has `P>`, a line containing a space, and `<T`; both state lines contain `A=0 B=0 R=701 S=sentinel`. The original raw, layout, observable-content and state comparison axes remain separate.

Native natural termination and internal argument values were not observed. The original comparison sheet, receipts and acceptance record are not included. These ordinary-condition results do not establish behavior in fault conditions or overall command compatibility, or equality of complete screens and execution environments.

From the distribution root, search with `python -I -B tools/query.py C196_04`, `python -I -B tools/query.py PRINTPLAIN196_C196_04`, or `python -I -B tools/query.py command_or_syntax:PRINTSINGLEV`. The returned case reference leads to each mode's history and byte range.

The two Native modes retain separate probe SHA references recorded in the source index, even when their history bytes match; the Public mode refers to a receipt SHA. Original probe and receipt bodies are not included. To obtain other results when the C196 supplement is inconsistent, use `--partial` and check exit code 3 and the `INCONSISTENT` / `PARTIAL` states. Errors in other collections or the shared verification tool are not isolated by this option.

The other 49 PRINT K/D conditions already have conditions, mode observations and supporting byte ranges in the existing [82-case index](../print-kd-shared-82-20261117/index.json) and [guide](../print-kd-shared-82-20261117/README.md), so they are not duplicated here. That is also a shared batch; GUI color, font, style and Native natural termination remain unobserved. See each guide for its rights notices.

With this material placed under `evidence/normal-observation-access-20261117/`, Python 3.9 or later can check the references. First obtain trusted SHA-256 values for `manifest.json` and `tools/file_set_manifest.py` through an independent channel, and check the tool's SHA. Enter the independently obtained manifest SHA below:

```powershell
$ExpectedManifestSHA256 = Read-Host 'Trusted manifest SHA-256'
if ((Get-FileHash evidence/normal-observation-access-20261117/manifest.json -Algorithm SHA256).Hash -ne $ExpectedManifestSHA256) { throw 'Manifest SHA-256 mismatch' }
python -I -B tools/file_set_manifest.py verify --manifest evidence/normal-observation-access-20261117/manifest.json --root evidence=evidence/normal-observation-access-20261117
if ($LASTEXITCODE -ne 0) { throw 'File-set verification failed' }
python -I -B evidence/normal-observation-access-20261117/verify.py --evidence-root evidence --manifest-sha256 $ExpectedManifestSHA256
```

The check covers the four-file set and compares the projection with the index, fixture, configuration and histories. Privacy and rights remain subject to final review. Integrity checks do not establish execution authenticity or approve publication.
