# Saved comparisons: eight evidence groups

[日本語](README.ja.md)

[index.json](index.json) organizes eight evidence groups, 101 registered cases linked to 65 typed targets, 63 fixture/shared batches and 180 mode records. Several cases share a fixture or mode, so the number of cases is not the number of independent executions. Each recorded verdict and condition has a finite scope; it is not a new acceptance or a target-wide compatibility judgment.

Each batch's `cases` identifies typed roles, recorded verdicts and selected conditions; `modes` identifies saved materials and selected receipt fields. Identical bytes are stored once in `assets/`, while separate case, mode and material-role references are preserved. Fixtures, configuration, CSV, history, stdout, stderr, OUTPUTLOG and debug console are distinct roles. Each material's `encoding` is recorded in the index. Byte-identical history, text comparison across different encodings, and visual equivalence are distinct claims.

Original receipts, comparison documents and the source register are not included. Selected fields are retained under `receipt_projection`, distinguishing Native probe input declarations, before/after hashes recorded in public receipts, and modes without recorded execution-time input hashes. Fourteen public history assets were not present in the saved source and are not included; stdout and stderr availability is recorded separately. Hashes and derived receipts do not establish the complete execution state or the authenticity of a run.

The group-specific limits include:

- For groups 234 and 233, unverified or setup-stopped cases remain distinct from success, and complete GUI or pixel equivalence is not claimed. One original outer invocation for gfillrectangle-method-zero-width, public-01, was not found in the saved source. Retained invocations include retries and do not establish completeness of all original first runs.
- Group 154 covers absent-sprite names; group 230 includes setup/load stops. Group 156 covers selected valid-domain math inputs.
- Group 214 has three fixtures and condition-specific CSV inputs. Group 196 indexes selected cases in a shared fixture and separates observable content, layout and raw comparison axes.
- Group 108 includes only supplemental `SELECTNEST01` for registered case `NESTEDSELECT01`; the original fixture and original screen image are not included. The included numeric path selects outer CASE 2 and inner CASE 3; CASEELSE selection was not observed.

Native natural exit is reported only to the extent recorded in each probe. Many modes were still running after five seconds; subsequent cleanup is not natural exit. The two supplemental 108 modes record exit and its code before cleanup. Product executables, the original source ZIP, all inputs and parent adjudication text are not included.

After checking the manifest and tool SHA-256 through a trusted separate channel, verify the file set from this bundle's root directory with Python 3.10 or newer:

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

See the [rights notices](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), and [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt). The source ZIP described in the NOTICE is a separate distribution unit and is not included. Rights holders and terms for the survey fixtures, derived records and documents remain to be confirmed separately.
