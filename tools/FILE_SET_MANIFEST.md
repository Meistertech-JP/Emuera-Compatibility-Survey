# SHA-256 inventory for selected distribution files

[日本語](FILE_SET_MANIFEST.ja.md)

`file_set_manifest.py` records and verifies the relative path, size and SHA-256 of every regular file in each **separately staged, selected directory**. Named roots distinguish ordinary repository files from Release assets. Identical relative names in different roots identify different files. Each root is scanned in full; there are no automatic exclusions or automatic publication decisions. Empty directories are not files and are not recorded.

Neither this tool nor an inventory grants publication, licensing, privacy, or compatibility approval. The current candidate remains under review. After selection and audit, stage the intended files in dedicated directories and freeze them before creating an inventory. Do not assume `.git`, internal documents, or old failures are automatically excluded.

## Usage

Requires Python 3.10 or later. The paths below are examples of selected staging directories. Creation requires a new manifest path and will not overwrite an existing file. These examples do not assert that a final freeze has occurred.

```powershell
python -B tools/file_set_manifest.py create `
  --root repo=<selected-repository-directory> `
  --root release=<selected-release-assets-directory> `
  --manifest <new-manifest.json>

python -B tools/file_set_manifest.py verify `
  --root repo=<same-repository-directory> `
  --root release=<same-release-assets-directory> `
  --manifest <manifest.json>
```

Root names start with an ASCII lowercase letter and contain lowercase letters, digits, `_` or `-`. Duplicate names, overlapping or aliased roots are refused. Absolute root paths are not embedded, so a tree can be relocated if its root name and manifest location are preserved. Quote the entire `NAME=PATH` argument when a path contains spaces.

If a manifest is inside a root, its exact location is recorded and **only that manifest file** is excluded to avoid circular hashing. Other manifests and checksum files remain ordinary files. The manifest's parent directory must already exist. A manifest outside the roots is also supported. Record its hash or signature separately in a trusted place if authenticity is needed.

For Windows normal and extended-length (`\\?\`) paths, case variants and short-name aliases, the tool uses the operating system's file identity and ancestor relationships. Overlapping roots are rejected even when spelled differently, and the same manifest is excluded using its actual location. An older recorded spelling is accepted only when the OS confirms it is the same file; differently cased but distinct files are not assumed identical. An older manifest that incorrectly recorded an inside-root location as outside (`null`) is rejected rather than silently repaired; create a new inventory.

Verification rejects missing, extra, resized or altered files. It rejects unsafe relative paths, Windows device names including `CONIN$` and `CONOUT$` with extensions, alternate streams, duplicate JSON keys and entries, case/Unicode NFC name collisions, file/directory conflicts, symlinks and Windows reparse points including junctions. Non-regular files are refused. Success exits 0 and failure exits 1.

The device-name rule is applied on every OS. Each component is NFKC-normalized, then its stem before the first dot is checked after removing trailing spaces, so names such as `CON .txt` and `LPT9 . .txt` are refused. This is a conservative Windows-portability rule: it also rejects names that may be valid regular files on POSIX and names that become reserved under NFKC normalization. Stems that are not reserved, such as `CONSOLE .txt` and `COM10 .txt`, are not rejected by this rule. Trailing spaces or dots at the end of any component are rejected separately.

An inventory proves consistency with the manifest; it is not a signature. Someone able to alter both files and manifest can recompute hashes. Use a separately trusted hash or signature. File identity, size and timestamps are checked before and after reading, but this is not an atomic snapshot and cannot rule out all concurrent changes. Stop writers and use frozen staging directories. Link-creation privileges and OS reparse behavior vary by environment.

Run the targeted tests from the candidate directory:

```powershell
python -B -m unittest discover -s tests -p test_file_set_manifest.py -v
```
