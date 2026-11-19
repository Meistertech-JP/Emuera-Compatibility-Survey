# DELCHARA: diagnostics from three saved conditions

[日本語](README.ja.md) · [Machine-readable records](records.json) · [Notices](notices/README.en.md)

These are saved Emuera and PyEmuera records. All three original case verdicts are `matched_scoped`, covering selected pre-error or argument-helper checkpoints and the stop location. Differences in diagnostics and output channels are a separate axis. The post-error state and Native natural exit were not observed.

| Case | Input and stop line | Native diagnostic | PyEmuera diagnostic |
|---|---|---|---|
| `BOUNDARY241_delete_empty_normalized` | `DELCHARA 0` with zero registered characters, line 16 | `エラー内容：存在しない登録キャラクタ(0)を削除しようとしました` (character 0 does not exist) | `E_CHARACTER`, invalid or duplicate index |
| `BOUNDARY241_delete_negative` | `DELCHARA -1`, line 23 | `エラー内容：存在しない登録キャラクタ(-1)を削除しようとしました` (character −1 does not exist) | `E_CHARACTER`, invalid or duplicate index |
| `BOUNDARY241_delete_duplicate_retry` | `DELCHARA H241A(),H241B()`, line 23 | `エラー内容：同一の登録キャラクタ番号(1)が複数回指定されました` (character 1 was specified more than once) | `E_CHARACTER`, invalid or duplicate index |

The input relationships, shared CSV/config, hashes, and selected checkpoints are listed in [records.json](records.json).

- `BOUNDARY241_delete_empty_normalized`: [ERB](assets/fixtures/C01/SEARCHBOUND01.ERB) · [Native-01](assets/raw/C01/native-01/emuera.log) · [Native-02](assets/raw/C01/native-02/emuera.log) · [Py stdout](assets/raw/C01/py/stdout.bin) · [Py stderr](assets/raw/C01/py/stderr.bin)
- `BOUNDARY241_delete_negative`: [ERB](assets/fixtures/C02/SEARCHBOUND01.ERB) · [Native-01](assets/raw/C02/native-01/emuera.log) · [Native-02](assets/raw/C02/native-02/emuera.log) · [Py stdout](assets/raw/C02/py/stdout.bin) · [Py stderr](assets/raw/C02/py/stderr.bin)
- `BOUNDARY241_delete_duplicate_retry`: [ERB](assets/fixtures/C03/SEARCHBOUND01.ERB) · [Native-01](assets/raw/C03/native-01/emuera.log) · [Native-02](assets/raw/C03/native-02/emuera.log) · [Py stdout](assets/raw/C03/py/stdout.bin) · [Py stderr](assets/raw/C03/py/stderr.bin)
 Shared input bytes do not imply shared case/mode executions. Each case has Native-01, Native-02, and Py mode. Engines and original receipts are not included.

The Emuera NOTICE describes a separately retained original ZIP distribution; that ZIP is not included in this bundle.

Authorship, redistribution permissions, and final privacy review of fixture, CSV, configuration, and raw output remain unresolved. Notices do not grant permission for every individual asset.

## Offline verification

Run the following command from this document directory.

Obtain the verifier, helper, manifest and profile SHA values through a trusted channel independent of this bundle and compare all four before execution. Replace the placeholders with those trusted values:

```text
python -I -B verify.py --manifest-sha256 MANIFEST_SHA --profile-sha256 PROFILE_SHA --helper-sha256 HELPER_SHA
```

This checks saved bytes and fixed case/mode/checkpoint bindings; it does not prove historical execution authenticity or rights.

The trusted manifest pin identifies this complete set of files and their bytes. The verifier also checks selected checkpoints, diagnostics, stop lines, and case/mode bindings; it does not prove the execution semantics of arbitrarily modified fixtures or the full semantic agreement of README prose with raw output. If fixtures, records, or explanations are changed and a new manifest or profile is sealed, separately compare their inputs, outputs, and descriptions with the original fixtures, raw data, and source records, and obtain the new pins through an independent trusted channel. Pins taken only from the bundle do not establish the authenticity of the new version.
