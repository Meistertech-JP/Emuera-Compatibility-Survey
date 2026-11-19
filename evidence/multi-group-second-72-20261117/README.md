# Saved comparisons: second collection

[日本語](README.ja.md)

[index.json](index.json) links 72 registered cases for 36 typed targets from six evidence groups to 36 fixture/shared batches and 108 mode records. Cases can share fixtures, so case count is not the number of independent executions. The saved verdicts are 28 scoped matches, 24 scoped differences and 20 unverified cases; they do not establish target-wide compatibility or a new acceptance. Two further candidate groups are excluded for the reasons listed in `withheld_groups`.

Each batch's `cases` records typed roles, verdicts and conditions; `modes` identifies fixtures, configuration, history, stdout, stderr, OUTPUTLOG and selected receipt fields. Identical bytes are stored once in `assets/` with separate case, mode and role references. The index records the text `encoding`. Original receipts, comparison documents and the source register are excluded; selected receipt fields are retained as `receipt_projection`. Native probe input declarations, before/after hashes recorded in public receipts, and modes without recorded execution-time input hashes are distinct.

For groups 231 and 235, 19 public history assets were not present in the saved source and are not included. This is separate from stdout/stderr and does not alone establish target reach or the cause of an error. None of the 72 Native modes records natural exit in its saved probe; cleanup is a separate event.

- Group 202 uses one shared fixture for display and history comparisons. State and DONE after the final empty-line error were not observed. GUI pixel equivalence is not claimed.
- Groups 231 and 235 separate direct availability differences from positive cases stopped during setup; public target-body reach and unverified observations remain distinct. Selected in-memory image values are not proof of full GUI equivalence.
- Group 194 records finite BAR/BARL inputs and one configuration snapshot. Matched and integer-overflow difference cases, and expression and method getter forms, are distinct. Group 136 covers finite numeric method inputs and evaluation order.
- Group 240 indexes six selected cases from an eight-stage shared fixture. Native received Return at each targeted wait; the public run received eight empty lines at startup. This does not equate input timing or GUI pixels. Original UI event records are not included.

Product executables, the original source ZIP, all inputs, images and parent adjudication text are not included. After checking the manifest and tool SHA-256 through a trusted separate channel, verify the file set from this bundle's root directory with Python 3.10 or newer:

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

See the [rights notices](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), and [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt). The source ZIP described in the NOTICE is a separate distribution unit and is not included. Rights holders and terms for the survey fixtures, derived records and documents remain to be confirmed separately.
