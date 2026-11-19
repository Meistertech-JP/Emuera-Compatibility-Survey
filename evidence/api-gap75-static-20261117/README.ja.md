# 75 typed対象の静的API提供状況と参照対応

[English](README.md)

この資料は75 typed対象のprivacy限定派生です。関数形34件・命令形41件で、名前としては41種類です。各行はtyped keyとNative登録情報、実際に読み取ったPyEmueraの関数／命令spec、現行target台帳、共有adapter、親matrix、typed readbackを対応付けます。命令形7件は同名の関数specが存在するため、関数形と命令形の提供状況を一括りにしません。

`native_registration` はNativeの `FunctionMethodCreator.methodList` にある同名の関数メソッド辞書登録と実装signatureを示します。命令形typed keyについて、この辞書登録だけでは命令構文自体の登録やルーティングを証明しません。命令形の経路や実測には別の根拠が必要で、下記case role・拒否phaseは原記録に基づく参照です。

親matrixには対象とcaseの参照が167件あり、typed readbackが選択した参照は110件、未選択は57件です。同じcase IDが複数typed対象に別の役割で現れる場合は対象別の参照を保持します。同じIDだけから物理的に同一の実行だとは断定しません。`reason` は親matrixの選択文脈のみであり、`reason_not_specified` は理由の捏造を避けた値です。拒否phaseはreadback上の記録で、この派生では原rawから再確認していません。

**fixture・実行ログ・receipt・config・GUI画像・エンジンの同梱や再実行はありません。** 全行の `not_reverified_raw_not_included` が示すとおり、親の `documented_difference` は原票の記録であり、75件の実測再現・完了や値一致の主張ではありません。公開版の実行成功、値・画素・ライフサイクルの一致や過去の実行の真正性を証明しません。非公開原票を持たない第三者は、ハッシュやpointerだけからその原票内容を確認できません。登録名・位置・specのキー有無は指定時点の静的事実であり、完全実装や全バージョンの提供状況の証明ではありません。

`records/targets.json` にtyped対象、source IDとJSON pointer、静的登録識別子、関数／命令specのキー有無、case roleを保持します。source IDとSHA-256は`manifest.json`にあり、privateの絶対パスや原receiptは含みません。SPRITEMOVE／SPRITESETPOSの個別証拠は別資料であり、他対象へ流用しません。

Python 3.9以降を使用します。`Path.is_relative_to` を使うための最低要件であり、3.9以降の全環境で動作確認したという意味ではありません。verifier実行前に、信頼できる別経路で得たSHAを独立した手段で照合し、manifestのSHAも別経路で得てから、次の引数を置換してください。

```sh
python3 -I -B verify.py --manifest-sha256 <信頼済みmanifest_SHA256> --verifier-sha256 <信頼済みverifier_SHA256>
python3 -I -B test_negative.py --manifest-sha256 <信頼済みmanifest_SHA256> --verifier-sha256 <信頼済みverifier_SHA256>
```

同梱verifierのSHA-256は `0d70bee333f3c61b03c1b3b76d4cc76482e994770271976a457e219ace9941a7` です。verifierはファイル集合・両pin・checksum・対象とcase roleの件数・基本型を確認し、非公開原票の内容は確認できません。同梱checksumは署名ではありません。

Nativeソースの表示は[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)と[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、PyEmueraソースは[MITライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。無改変のEmuera NOTICEは別の原ソースZIP配布単位に同伴する文書で、その配布物と保全来歴を説明しています。当該ZIPはここには含まず、このディレクトリにZIPがあることを意味しません。調査により作成した記録・文書・検証コードの権利主体と利用条件は別途整理が必要で、PyEmuera MITを調査成果全体に自動適用しません。
