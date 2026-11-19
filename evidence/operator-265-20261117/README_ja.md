# 代入の保存観測

[23件の観測](OBSERVATIONS_ja.md) · [機械可読record](records.json) · [English](README_en.md)

原raw、ERB・ERH・configはbyteを維持しています。関連typed keyすべての個別到達や親判定の完了を示すものではありません。engine本体は含みません。素材の作者・再配布権限は要確認であり、公開承認を意味しません。

`verify.py` と `tools/file_set_manifest.py` は実行コードです。どちらも実行する前に、両者のSHA-256をbundle外の信頼できる値と比較してください。期待hash、manifest pin、別のsource profile pinはいずれもbundle外の信頼できる場所から取得します。一致後 `python -B verify.py --inventory-tool PATH_TO_tools/file_set_manifest.py --pin 外部manifest_SHA256 --profile-pin 外部profile_SHA256` を実行します。

[source profile](source-profile.json) は、凍結原recordに記された23 caseのtyped keyと71 source行範囲、27 memberの識別情報を固定します。verifierはrecordのmetadataが独立pin済みprofileと一致するか検査します。source自体は同梱しないため、archiveを指定しない場合はsource bytes・行内容の検査を `NOT RUN` と表示します。`--native-source-zip PATH` と `--py-source-pyz PATH` をそれぞれ追加すると、指定したarchiveのSHA、member bytesおよび記録行のhashを読み取り専用で照合します。これは各行が主張を意味的に裏付けることや、sourceから実行EXEがbuildされたことの証明ではありません。profileを含む全pinを同じ未信頼の配布物から取得しただけでは真正性を保証できません。

[登録case IDとmode別の観測](CASE_INDEX_ja.md) · [入力準備・限定的再実行](REPRODUCE_ja.md) · [engine識別](environment.json)

[Emuera原license](licenses/Emuera1824-v24-license-original.txt) · [Emuera NOTICE](licenses/NOTICE.ja.md) · [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt) · [PyEmuera第三者表示](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)

Emuera NOTICEは別途保全した原ZIP配布単位の説明であり、この証拠bundleに原ZIPが同梱されている意味ではありません。PyEmuera第三者表示の配布物表現も元PyEmuera配布物を指します。fixture/config/raw自体の権利・許諾は別確認が必要です。
