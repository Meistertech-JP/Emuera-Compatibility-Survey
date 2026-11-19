# Additional v24 source locations: 29 operators and SET

[日本語](README.ja.md)

This layer adds limited locations in the bundled v24 source for 30 typed targets whose positions were not recorded in the [694-target static source index](../native-source-694-static-20261117/README.md). It does not rewrite that index or change any target verdict, execution status or compatibility claim.

[`targets.jsonl`](targets.jsonl) has one line per target: 29 operators and `command_or_syntax:SET`. `source.archive` is relative to the repository root; `inner_archive` and `member` identify the nested ZIP and source member, and `line` is a one-based source line. The referenced member is in the shared [v24 source archive](../../vendor/emuera/Emuera1824-v24-with-notices.zip).

## Operators and the IL comparison

The 29 locations are `OperatorManager` dictionary entries mapping a token spelling to an `OperatorCode`. Registration does not establish the execution branch or result. The existing IL record's spelling and numeric constant were compared with the source enum value. `ldstr_il_offset` is an **IL offset**, not a C# source line. The IL record itself is not distributed here, and the comparison covers only spelling and number. It does not establish that the IL-side binary was built from the bundled source, build identity, execution, or result equivalence.

For `!|`, the dictionary maps the spelling to `Nor`, and the numeric value in the IL record matches the `Nor` enum value. The enum declaration's comment instead says `!^`. The comment is not evidence that `!^` is registered.

## SET

The main `SET` location is construction of an internal assignment identifier in `FunctionIdentifier.cs`. Supporting locations identify the enum declaration, `SET_Instruction`, and parser handoffs for assignment syntax. This does not establish a callable literal `SET` script command or its runtime outcome.

## File set and notices

If this directory is placed at `evidence/native-source-operator30-20261117/` in a repository containing the shared tool, verify from its root:

```powershell
python -B tools/file_set_manifest.py verify `
  --root evidence=evidence/native-source-operator30-20261117 `
  --manifest evidence/native-source-operator30-20261117/manifest.json
```

The manifest excludes itself. Obtain and compare its SHA-256 via a separate trusted channel. A matching file set establishes consistency, not source, IL or publisher authenticity, execution, or rights. The source-to-projection crosswalk is not distributed here.

See the [common notices](../../LICENSES/README.md), [original Emuera license](../../LICENSES/Emuera1824-v24-license-original.txt) and [Emuera NOTICE](../../vendor/emuera/NOTICE.en.md). Notices for referenced source and ownership or terms for this derived index are separate matters; no blanket license or publication approval is implied.
