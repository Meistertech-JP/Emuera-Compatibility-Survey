# 外部scalar観測

この資料は、記録された条件下でのEmueraとPyEmueraのscalar観測29件を収録します。各条件・値・範囲は[日本語観測一覧](evidence/external-scalar-observations-20261117/OBSERVATIONS_ja.md)と[機械可読記録](evidence/external-scalar-observations-20261117/records.json)を参照してください。

- [English observations](evidence/external-scalar-observations-20261117/OBSERVATIONS_en.md)
- [NOTICEとライセンス](notices/README.md)
- [閲覧・検証・再現上の制約](evidence/external-scalar-observations-20261117/README_ja.md) ([English](evidence/external-scalar-observations-20261117/README_en.md))

## 範囲と解釈

対象は記録された29ケースと各ケースの入力・設定条件に限られます。88件の調査の残る59件はここに収録していません。非収録は未観測を意味しません。NativeとPyEmueraの記録値が異なるケースを2件含みます。`DONE`はfixtureが出力するmarkerで、アプリケーションの自然終了を示すものではありません。一般的な互換性、未記録条件での動作、完全なGUI動作を主張しません。

C005の値は空文字・index 0の記録条件に限ります。C012はNative/PyEmueraの集約結果の差を記録しています。「値9が数えられた」という説明は保存値と集約結果に基づく推論で、個別要素の直接観測ではありません。個々の条件と限界はcase記録を参照してください。

## 再現と権利

fixture、設定、CSV、保存rawを収録しています。engine実行ファイル、完全な実行環境、元receipt、外部原記録は含まれないため、過去の実行の真正性や外部記録との対応をこの資料だけで第三者が再検証することはできず、当時の実行を完全再現できません。画面画像も含まれないためGUI表示を比較できません。追試が同じ結果になる保証はありません。

同梱NOTICE・ライセンスは記載された範囲に適用されます。同梱だけで資料全体の公開・再配布権が確定するものではなく、一部素材の条件は未確認です。[NOTICEとライセンスの案内](notices/README.md)を参照してください。

[English](README.md)
