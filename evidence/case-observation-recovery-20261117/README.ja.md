# 観測ケース集

486件のケース記録と、既存caseへの38行の観測補足を収録します。486件のうち95件は `recovered` 欄に保存観測の記述があり、残り391件は同欄が空です。他の欄には条件や比較範囲などを記録しています。同欄が空であることは、元の調査で観測がなかったことを意味しません。補足は新しいcaseやrunを追加しません。停止後stateの修正後記録2件は検索時に先に表示し、486件の従来記録も過去snapshotとして併記します。

以下のコマンドは配布bundle root（このREADME、`query.py`、`verify_bundle.py`、`manifest.json` があるディレクトリ）で実行します。

```powershell
python -B query.py --case CASE_ID
python -B query.py --target 'kind:name'
python -B verify_bundle.py
python -B file_set_manifest.py verify --manifest manifest.json --root public=.
```

typed target検索はkindとnameの完全一致（大文字小文字は区別しない）です。name単体も完全一致で検索します。`verify_bundle.py` は収録数・ID関係・補正記録の検索優先規則などを確認し、最後のコマンドは統合manifestのfile inventoryとhashを照合します。

486件の観測JSONLは `observations.jsonl` としてこのbundleに含まれます。元source register、source receipts、raw filesは含まれず、これらを取得する経路も案内しません。配布物単独で確認できるのは同梱manifestとの整合性などに限られ、manifest/hashは署名や発行者認証ではありません。

- [日本語 marker recovery案内](marker-recovery/README.ja.md)
- [English marker recovery guide](marker-recovery/README.en.md)
- [統合manifest](manifest.json)