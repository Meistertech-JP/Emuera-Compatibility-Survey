# DELCHARA：保存された3条件の診断

[English](README.md) · [機械可読記録](records.json) · [権利表示](notices/README.ja.md)

本家EmueraとPyEmueraの保存記録です。元case判定は3件とも `matched_scoped` で、選択されたエラー前／引数helper中の状態と停止位置の比較です。診断文・出力経路の違いは別の軸です。エラー後stateと本家の自然終了は未観測です。

| case | 入力と停止行 | 本家の診断要点 | PyEmueraの診断 |
|---|---|---|---|
| `BOUNDARY241_delete_empty_normalized` | 登録キャラクターが0件の状態で `DELCHARA 0`、16行 | `エラー内容：存在しない登録キャラクタ(0)を削除しようとしました` | `E_CHARACTER`、無効または重複の番号 |
| `BOUNDARY241_delete_negative` | `DELCHARA -1`、23行 | `エラー内容：存在しない登録キャラクタ(-1)を削除しようとしました` | `E_CHARACTER`、無効または重複の番号 |
| `BOUNDARY241_delete_duplicate_retry` | `DELCHARA H241A(),H241B()`、23行 | `エラー内容：同一の登録キャラクタ番号(1)が複数回指定されました` | `E_CHARACTER`、無効または重複の番号 |

各caseのSHA・選択checkpoint・共有CSV/configの入力関係は [records.json](records.json) にあります。

- `BOUNDARY241_delete_empty_normalized`: [ERB](assets/fixtures/C01/SEARCHBOUND01.ERB) · [Native-01](assets/raw/C01/native-01/emuera.log) · [Native-02](assets/raw/C01/native-02/emuera.log) · [Py stdout](assets/raw/C01/py/stdout.bin) · [Py stderr](assets/raw/C01/py/stderr.bin)
- `BOUNDARY241_delete_negative`: [ERB](assets/fixtures/C02/SEARCHBOUND01.ERB) · [Native-01](assets/raw/C02/native-01/emuera.log) · [Native-02](assets/raw/C02/native-02/emuera.log) · [Py stdout](assets/raw/C02/py/stdout.bin) · [Py stderr](assets/raw/C02/py/stderr.bin)
- `BOUNDARY241_delete_duplicate_retry`: [ERB](assets/fixtures/C03/SEARCHBOUND01.ERB) · [Native-01](assets/raw/C03/native-01/emuera.log) · [Native-02](assets/raw/C03/native-02/emuera.log) · [Py stdout](assets/raw/C03/py/stdout.bin) · [Py stderr](assets/raw/C03/py/stderr.bin)
共有入力bytesは同一のcase／mode実行を意味しません。各caseはNative-01、Native-02、Pyの3 modeです。エンジンや元receiptは同梱しません。

Emuera NOTICEは別途保全された原ZIP配布単位についての記録で、この資料にそのZIPは含まれません。

fixture・CSV・config・rawの権利主体や再配布許諾、privacyの最終確認は未了です。同伴NOTICEは個別素材の公開許諾を意味しません。

## オフライン検証

次のコマンドは、この資料のディレクトリで実行してください。

verifier、helper、manifest、profileのSHAをこの配布物とは別の信頼経路で取得し、4点すべてを実行前に照合してください。その後、次のコマンドで検証します。`PROFILE_SHA`等は信頼済み値に置換してください。

```text
python -I -B verify.py --manifest-sha256 MANIFEST_SHA --profile-sha256 PROFILE_SHA --helper-sha256 HELPER_SHA
```

この検証は保存bytesと固定されたcase/mode・観測行の整合性であり、過去実行の真正性や権利を証明しません。

信頼済みのmanifest pinは、この資料の全ファイルのbytesとファイル集合の照合に使います。検証器は選択したcheckpoint・診断・停止行・case/modeの結合も確認しますが、任意に変更されたfixtureの実行意味や、README本文とrawの全意味対応を証明しません。fixture、記録または説明を変更して新しいmanifestやprofileに再sealする場合は、元fixture・raw・原記録との対応と説明を別途照合し、新しいpinを独立した信頼経路で確認してください。同梱ファイルから得たpinだけでは、その新しい版の真正性を確立できません。
