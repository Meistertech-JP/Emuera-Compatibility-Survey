# 構文・補助の保存観測

[English](README.md)

この証拠bundleはCOLON構文16ケースと補助ラベル8ケースの保存観測を、各3 modeで保持します。24ケースは主694対象とは別の分母です。元の有限判定、診断・停止条件、未観測状態を保持し、新たなエンジン実行や完全互換性を主張しません。probe本文、元receipt、エンジンおよび一部の親証拠は含みません。

600証拠資材について、構築担当とは別のAIによる独立した限定privacyレビューが行われ、その範囲では具体的な秘密・個人情報・開発者宛て指示や第三者ゲーム文章・画像の問題は見つかりませんでした。これはすべてのprivacy・権利問題が解消した保証ではありません。調査側fixture・派生記録・文書・ツールの権利主体と許諾範囲は未確定で、成果全体への一括許諾を推定しません。現在のcandidateは最終公開承認ではありません。

共通verifierは独立確認済みsnapshotから導いた固定contractに照らし、24ケースの型・値・存在／不在、未観測状態、family・親、mode・役割、パスとSHAを検査します。contract変更時はverifierと信頼pinの別途レビューが必要です。データと同封されたchecksumやpinは独立した真正性の証明ではありません。同一bytesだけでは各modeの歴史的実行帰属を決められず、補助側receiptにはcase／mode欄がないため、保存readbackとディレクトリの来歴に依存します。

Python 3.9以上で、manifest・bindings・contract・verifierのSHA-256を認証された独立経路から入手し、実行前にverifierを照合します。このディレクトリで実行します。

```text
python -c "import hashlib,sys; sys.exit(0 if hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()==sys.argv[2] else 1)" verify.py <VERIFIER_SHA256>
python -I -B verify.py --manifest-sha <MANIFEST_SHA256> --bindings-sha <BINDINGS_SHA256> --contract-sha <CONTRACT_SHA256> --verifier-sha <VERIFIER_SHA256>
python -I -B negative_checks.py --manifest-sha <MANIFEST_SHA256> --bindings-sha <BINDINGS_SHA256> --contract-sha <CONTRACT_SHA256> --verifier-sha <VERIFIER_SHA256>
```

最初のコマンドが非0なら中止してください。[ライセンス一覧](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。無改変のEmuera NOTICEは別の原source ZIPを含む別配布単位を説明しています。ZIPの同梱に関する記述はその別単位についてのもので、この証拠bundleにはZIPも7zも含まれません。原ライセンスとNOTICEの本文は変更していません。
