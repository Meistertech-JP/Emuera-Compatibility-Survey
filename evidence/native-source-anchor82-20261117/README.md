# Additional v24 source locations for 82 typed targets

[日本語](README.ja.md)

This independent supplement to the [694-target static source index](../native-source-694-static-20261117/README.md) identifies locations in the bundled v24 source for 82 typed targets. It does not alter that index, a target verdict, or an execution status.

[`targets.jsonl`](targets.jsonl) contains one record per typed target: 49 `FunctionCode` enum declarations, 15 assignment lexical branches, 11 declaration parser switches, and 7 variable declaration modifier switches. Each `locations` entry gives the full nested ZIP source member, its whole-file SHA-256, a one-based inclusive `start_line`–`end_line`, the v24 source role, and `context_lines` used for the role and branch identification. For the 15 assignment targets there are two locations: the lexical branch and a shared assignment-line parser range. The shared range does not prove that every spelling follows that path or establish prefix-form routing. The conditions at the listed context lines distinguish forms sharing an initial-character branch, such as `++` and `+=`.

The source is the separately distributed [v24 source archive](../../vendor/emuera/Emuera1824-v24-with-notices.zip); its outer and inner archive hashes and source-member hashes are recorded in the rows. The source bytes are not included in this layer. The recorded older anchors did not specify their source version, file SHA or role; the original file's version and byte identity with v24 remain unproven. The source roles here describe what can be read at the v24 locations. Enum declarations do not prove command registration, handlers or method routing. Neither these static branches nor their location matches prove execution, compatibility, output, or acceptance. Hashes identify bytes, not their origin or authenticity.

## File set and notices

When placed at `evidence/native-source-anchor82-20261117/` in a repository containing the shared tool, run from the repository root:

```powershell
python -B tools/file_set_manifest.py verify `
  --root evidence=evidence/native-source-anchor82-20261117 `
  --manifest evidence/native-source-anchor82-20261117/manifest.json
python -c "import hashlib; print(hashlib.sha256(open('evidence/native-source-anchor82-20261117/manifest.json','rb').read()).hexdigest())"
```

Compare the manifest hash with a pin obtained through a separate trusted channel. The manifest excludes itself; the tool checks file-set integrity, not authorship, rights, or semantic correctness. The original-record crosswalk and source audit are not distributed in this layer.

See the [common notices](../../LICENSES/README.md), [original Emuera license](../../LICENSES/Emuera1824-v24-license-original.txt), and [Emuera NOTICE](../../vendor/emuera/NOTICE.en.md). Rights for the referenced source and this derived index must be assessed separately; this supplement does not assert publication approval.
