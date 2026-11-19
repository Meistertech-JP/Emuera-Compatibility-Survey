# 表示状態の命令形式：15対象と1共有batch

[English](README.md)

この資料は15 typed対象・15登録caseを、case150の**1共有batch**に記録されたNative 2 modeとPublic 1 modeに対応付けた公開候補です。各caseで独立に起動したという意味ではありません。`index.json` は10個の命令形式getterについて設定前後の20条件、5つの設定命令について各getterを通じた1回の状態遷移を保持します。`matched_scoped` は元台帳の限定判定です。

各modeのfixture、config、保存historyは `modes/` に無改変で保持しています。3つのhistoryは同じSHAで、元比較票に記載された20の観測行と `DONE` をそれぞれ含みます。Public stdoutはこのhistory比較の代わりに用いていません。Native probeが記録したfixture・config SHAは保持物と一致しますが、原receiptには入力の独立した実行前後SHAがありません。Public側も保持ファイルと元比較票の宣言であり、実行時の入力前後SHAを記録したreceiptは確認できません。

Native 2 modeは別desktopのGUI実行で、5秒後に生存しcleanupされたことが記録されています。自然終了と終了コードは未観測です。Publicはコマンドライン実行でstdin継承、その内容は未記録です。Public invocationに記録されたreturncode 0はNative終了の証拠ではありません。元比較票のPYZ SHAは記録値として保持していますが、Publicの当時の実行前後ハッシュが独立に保存されたことや、他のPublic実行と同一buildであることは示しません。

観測は特定設定における取得値・状態変化・RESULT／RESULTSの振り分けに限られます。実際のGUIの色やフォント描画、入力配置、別設定や互換性全体は確認していません。LINEISEMPTYは先行出力行の完了後に限られます。先行case149の記録は、この観測には含みません。元receipt・個人path・原実行物・元と派生のprivate対応表は同梱しません。 元ケース台帳・比較票・条件票・原reviewも非同梱のため、このbundleだけでは第三者が元資料と直接照合できません。

## 検証と権利

検証にはPython 3.9以降を使用します。別の信頼できる経路で取得したmanifestとverifierのSHA-256を、それぞれ独立したハッシュ手段で照合してから、このディレクトリで実行してください。

```text
python -I -B verify.py --manifest-sha256 <信頼済みmanifest SHA256> --verifier-sha256 <信頼済みverifier SHA256>
```

verifierは共通file-set toolの固定SHAを実行前に照合し、集合・15 case／typed targetの結合・3履歴のSHAと、20観測行それぞれの先頭が対応する条件markerであることを確認します。期待値の独立導出、元実行・発行者の真正性、自然終了、画面描画や権利を証明せず、エンジンは再実行しません。信頼済みpinはbundle外で別途提供される必要があります。 新たなpinで再封緘されたmanifestは、それだけでは元資料との一致を自動的に保証しません。

[ライセンス索引](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照。NOTICEが説明する原source ZIPは別配布単位で、この資料には含めていません。fixture・派生記録の権利主体や利用条件は未確定であり、機密・権利・公開は未承認です。
