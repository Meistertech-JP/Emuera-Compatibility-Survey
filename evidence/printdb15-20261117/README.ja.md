# PRINTDB15の保存済み有限観測

[English](README.md)

物理ケース `PRINTDB15` は1件で、`command_or_syntax:PRINTDATA` と `structural_syntax:PRINTDATA` の2 typed roleが元票に明記されています。保存modeはNative-01・Native-02・public-01の3件で、typed roleごとに別実行したとは扱いません。

保存された空ブロックなしの条件はindex 99・次のRAND100 43、空DATA itemはindex 0・次のRAND100 5です。対象の表示データなし警告はNativeログ2本にあり、公開側の保存済み3 streamにはありません。公開側stderrには別のOUTPUTLOG警告があり、警告が全くないという主張ではありません。Native自然終了・終了コードとGUI pixelsは未観測です。元case判定は `different_scoped`、親対象の結果はともに `documented_difference` です。

NativeログにはEmuera出力、公開側stderrにはPyEmueraの診断文が含まれます。短いfixtureは調査用のprobe命令とマーカーです。設定原文・エンジン・親票・receipt原文は同梱せず、receiptは必要フィールドの派生です。SHAとprivateの元参照だけでは、非同梱原票の真正性は証明できません。

[ライセンスとNOTICE](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。NOTICEで説明するEmuera source ZIPは同梱しません。これらの文書は調査fixture・独自コード・派生データ全体を自動的に許諾するものではなく、それぞれの権利・機密と最終公開判断は未確定です。

`python -I -B verify.py --manifest-sha256 <信頼済みmanifest SHA> --verifier-sha256 <信頼済みverifier SHA>` で検証します。検証器には確認済み来歴の固定値が含まれます。同梱pinだけでは独立した真正性を保証できません。
