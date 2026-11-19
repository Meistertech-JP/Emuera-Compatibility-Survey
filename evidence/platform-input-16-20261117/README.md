# Saved input and display state: 16 cases

[日本語](README.ja.md)

These saved records cover 16 fixtures for 12 typed targets, the expression and method forms of six functions. Each fixture has two Native modes and one PyEmuera mode: 48 case-mode records, not a target-wide compatibility judgment. See [records.json](records.json) for the targets, conditions, selected rows, recorded verdicts and materials.

The source case register records two scoped matches, seven scoped availability differences and seven unverified cases. The comparison's `unverified_environment` and the register's `unverified` are shown separately. The two MOUSESKIP cases compare selected startup state; skip activation was not tested. `E_PLATFORM` reflects an environment constraint and is not proof of a value mismatch or successful target execution. Native short-circuiting in an inactive condition does not establish the active-state behavior of out-of-range input.

Key or mouse events and physical input were not sent or manipulated. Active-window key and toggle transitions, and GUI or focus equivalence, were not observed. MOUSEX/Y values depend on the recorded environment. Native natural exit was not observed after five seconds and is distinct from subsequent cleanup.

Each mode in `records.json` links to the saved ERB and configuration and to Native history or PyEmuera stdout/stderr. PyEmuera history is included only for the 11 modes where it was present and linked in the saved evidence. These materials retain their saved bytes. Receipts are derived records omitting internal paths and execution-management identifiers; their case/mode links come from saved fixture IDs and source paths. Native input hashes are probe declarations; The original PyEmuera receipts recorded fixture and config hashes before and after execution, but those original fields are not included and cannot be directly checked from this material alone. This does not establish the full execution state or the authenticity of the run. Complete source receipts, executables, all inputs and the full source register and comparison are not included.

After checking the manifest and tool SHA-256 through a trusted separate channel, verify the file set from this bundle's root directory with Python 3.10 or newer:

```powershell
python -I -B tools/file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

See the [rights notices](LICENSES/README.md), [original Emuera license](LICENSES/Emuera1824-v24-license-original.txt), [Emuera NOTICE](vendor/emuera/NOTICE.en.md), and [PyEmuera license](LICENSES/PyEmuera-3.0.0-LICENSE.txt). The source ZIP described in the NOTICE belongs to a separate distribution unit and is not included. Rights holders and terms for the survey fixtures, derived records and documents remain to be confirmed separately.
