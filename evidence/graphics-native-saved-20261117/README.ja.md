# グラフィックAPI：保存された本家観測

[English](README.md) | [英語の観測例](OBSERVATIONS.en.md) | [命令別の観測例](OBSERVATIONS_ja.md) | [入力とraw](REFERENCES_ja.md)

34条件の本家入力と保存rawを収録します。数値・診断は各条件に限り、GUI画面、全画素、自然終了、PyEmueraとの全面互換を示すものではありません。日本語の観測本文が詳しい内容です。入力のresources/CSVは各 `inputs` 内にあり、保存rawはUTF-16 BOM付きです。実行体は同梱しません。

**素材の権利・公開条件とprivacyの判断は未了です**。manifestの一致は公開許可や観測内容の正しさの証明ではありません。

このディレクトリを作業場所として、Python 3.10以上で収録ファイルの集合・SHA-256・サイズを確認できます。

```text
python -I -B file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

独立した真正性の確認には、信頼できる別経路で得たmanifestのSHA-256が必要です。未同梱の元PNG全画素記録は本bundle単体で再照合できません。
