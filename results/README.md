# Finite survey: neutral data index

[日本語](#日本語)

This index records the reported classifications from the finite Emuera1824+v24 / PyEmuera 3.0.0 survey. It is a projection of the source registers, not a collection of original evidence or proof of full compatibility. The entries in `survey.json` retain the original projection's `unresolved_not_in_candidate` and `not_established` markers; these markers do not describe evidence added later. Separate indexes and [representative evidence](../differences/representative-20261116/README.en.md) link selected cases to saved material. [The PRINTDATA-family set](../evidence/printdata-61-20261117/README.md) also contains 61 saved cases. These collections do not establish the remaining entries.

## Files

- `survey.json`: typed targets, main scenarios, supplemental work items, supplemental registered modes, and grammar cases. A `null` verdict or phase means that the source index did not supply that field; it is not an inferred pass or failure.
- `../differences/catalog.json`: the 1,071 main and 65 grammar differences in the original difference index, plus the 48 `different_scoped` supplemental modes derived separately from the six supplemental registers. These populations overlap in meaning and must not be added to infer a unique bug count.
- [`../evidence/case-register-2898-20261117/`](../evidence/case-register-2898-20261117/README.md): recorded conditions and limits for the main cases, with non-included or withheld fields marked. Search a catalog case ID using `python -B tools/query.py CASE_ID`; the returned references do not make withheld originals available.
- `evidence-index.json`: links selected cases and their historical IDs to separately retained evidence; it does not imply that other cases are covered. The evidence directory has its own manifest and verification instructions.
- `manifest.json`: SHA-256 and size of the two data files. The manifest detects accidental changes relative to its recorded hashes; it is not a digital signature or an independent assertion of origin.
- `verify.py`: checks data structure, classification counts, links, declared hashes and a bounded sensitive-text screen without the source survey or network.
- `test_verify.py`: isolated positive and negative controls for the verifier. Uses disposable files under this directory.
- `build_from_frozen.py`: projects a separately supplied source tree and private freeze ledger into these files and writes a source-pointer mapping to an explicitly specified private path. The provenance output must be outside both the candidate and the tool repository; the candidate and source must be separate, non-nested directories. It does not ship or fetch that source tree or private mapping. Read `--help` before use.

Run from any working directory with Python 3.9 or later:

```text
python -B results/verify.py
python -B results/test_verify.py
```

The command paths above assume the current directory is the candidate root; alternatively use the full path to each script. Verification checks the dataset as distributed, not original runtime observations, full semantic sufficiency, the authenticity of the manifest, or every possible secret. A case can refer to more than one typed target. The registered preprocessing target for `RENAMEEDGE01` is outside the 694-target population and is explicitly retained.

## 日本語

この索引は有限範囲の調査台帳から判定と識別子を抽出したものです。`survey.json` の `unresolved_not_in_candidate` と `not_established` は投影当時の記録で、後から追加された証拠の有無を示すものではありません。別の索引や[代表的な一部の証拠](../differences/representative-20261116/README.ja.md)から、選定したケースの保存資料を参照できます。[PRINTDATA系の証拠](../evidence/printdata-61-20261117/README.ja.md)には61ケースを収録しています。これらは残りの項目を検証できることを意味しません。

`survey.json` は主対象694、主シナリオ2,898、補助16項目と83登録モード、別枠の構文114ケース・342登録モードを格納します。`null` は元の索引に該当フィールドがないことを示し、成功や失敗ではありません。登録モード数はプロセス起動回数ではありません。

`../differences/catalog.json` は元の差異索引にある主1,071・構文65件と、補助登録簿から別途抽出した差異48モードを収録します。これらの合計は固有バグ数ではありません。694対象の必要比較完了も完全互換性を意味しません。

[2,898ケースの記録](../evidence/case-register-2898-20261117/README.ja.md)には、主ケースの条件と制限を記載し、非同梱または保留した欄を明示しています。差異索引のケースIDは `python -B tools/query.py CASE_ID` で検索できますが、参照があることは非公開の原票を読めることを意味しません。

`build_from_frozen.py` の非公開来歴出力先には、候補およびツールのリポジトリ外を指定します。候補と凍結済み原本も互いに入れ子にしません。

候補ルートから `python -B results/verify.py` で元ディレクトリ不要の検証を実行できます。`python -B results/test_verify.py` は候補内に一時コピーを作って改変等の負例を試し、終了時に削除します。検証は件数、分類、参照、データの整合性を対象とし、元の実測・意味論・公開可否を証明するものではありません。原本のSHAと各JSONポインターの対応表は候補に含まれていません。
