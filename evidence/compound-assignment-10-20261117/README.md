# Shared numeric compound-assignment evidence

[日本語](README.ja.md)

This is the saved evidence for one fixture covering ten numeric compound assignments: `+= -= *= /= %= <<= >>= |= &= ^=`. It has two Native modes and two PyEmuera modes. [records.json](records.json) links ten registered cases and typed targets to six conditions each, 60 conditions in total, selected rows and the four mode materials. The cases refer to one shared batch, not ten independent executions.

All ten case verdicts are recorded as `matched_scoped`. Initial values are 6, -7 and 0, right-hand operands are positive 2 or 1, and the index helper always returns 0. The comparison is limited to the target value, the non-target `D:1`, and evaluation count and order. Changing indices, aliases, string assignment, overflow, invalid types or indices and failure order for division by zero are outside this record. It does not establish target-wide compatibility.

The saved history bytes are identical across all four modes. PyEmuera stdout/stderr are saved separately from history. Native input hashes are probe declarations; the original receipt for the second PyEmuera mode recorded before/after hashes, but that original receipt and its fixture/config before-and-after hash fields are not included here. For the first PyEmuera mode only the saved file hashes were verified; execution-time before/after input hashes were not recorded. Native natural exit was not observed after five seconds and is separate from subsequent cleanup. Original receipts contain internal paths or management identifiers and are excluded; included receipts are derived from selected fields. Executables, complete inputs, the original register and comparison, and referenced source text are not included.

After checking the manifest and tool SHA-256 through a trusted separate channel, verify the file set from this bundle's root directory with Python 3.10 or newer:

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

See the [rights notices](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), and [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt). The source ZIP described in the NOTICE is a separate distribution unit and is not included. Rights holders and terms for the survey fixtures, derived records and documents remain to be confirmed separately.
