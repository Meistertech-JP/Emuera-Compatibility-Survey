# Main29：旧形式の限定された式観測

[English](README.md)

このリポジトリ内の証拠ディレクトリは、29ケースの全件バッチと、CASE001（ABS）だけの単独・代表バッチを別stageとして保持します。各stageにNative-01、Native-02、Pyの各modeがあります。`matched_scoped` は選択式の値とRESULT／RESULTSの有限観測であり、親対象全体の受入、既知差分の解消、全互換性を意味しません。GUI・入力・fatal/load errorなどの未観測条件は対象外です。

旧形式の実機attemptと別保全のv3 legacy監査から中立IDへ派生したもので、新しいv3実行ではありません。旧rawに `ZZBATCH_DONE` はなく、最終case ENDが当時の観測規則です。Nativeの自然終了と終了コードは未観測で、観測後に所有プロセスを強制終了しました。元Pyのstdout/stderrと元scope全文は同梱していません。Nativeの2 modeが同じbytesの場合、証拠ファイルだけではそれぞれの実行を認証できず、対応は別保全の非公開receiptと来歴に基づきます。

Native raw・configはEmuera1824+v24、PyログはPyEmueraに関係します。リポジトリ共通の[ライセンス一覧](../../LICENSES/README.ja.md)、[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)、[PyEmuera第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)はこのディレクトリの外にあります。リンク先Emuera NOTICEは別のsource ZIPを含む別配布単位の説明です。この証拠ディレクトリにそのZIPはなく、NOTICEの同梱に関する記述は別配布単位のものであって、このディレクトリの構成を示しません。調査fixture・派生データ・文書・新規ツールの権利条件は、リポジトリ共通の[権利表示](../../LICENSES/README.ja.md)の対象範囲と、そこに掲げる第三者表示の個別条件に従います。

オフライン検証では認証された独立経路から `verify.py` と `manifest.json` の信頼するSHA-256を入手し、実行前にverifierを照合します。同じ配布物内の値は独立した信頼源ではありません。Python 3.10以上で、この証拠ディレクトリから実行します。

```text
python -c "import hashlib,sys; sys.exit(0 if hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()==sys.argv[2] else 1)" verify.py <TRUSTED_VERIFIER_SHA256>
python -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

最初のコマンドが非0なら中止してください。verifierは固定29件profile、証拠ファイル集合、fixture、raw観測、終了形態・判定と、リポジトリ共通licenseファイルの固定ハッシュを照合します。エンジンは起動せず、実行者の真正性や過去のlegacy監査の全範囲は証明しません。原票照合には別保全の非公開記録が必要です。このディレクトリ単体は完結した配布物ではなく、必要なリポジトリ共通ライセンス・NOTICEを正しい相対配置で同伴させてください。権利・privacy・公開対象選定と認証されたpin配布には別途レビューが必要です。
