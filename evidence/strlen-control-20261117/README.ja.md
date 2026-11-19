# STRLEN control の保存済み観測

[English](README.md)

この資料は、`command_or_syntax:STRLEN` の1ケース `ARGBOUND246_strlen-control` の保存済み観測を確認するための派生物です。旧ケースIDは `PARENT246_strlen-control` です。このケースの局所結果は `matched_scoped`、対象全体の有限受入は別条件の差異を含む `documented_difference` です。単一ケースは対象全体や他の対象の互換性を証明しません。

CP932のfixtureは `STRLEN "abc"` を実行し、引用符を含むraw textの長さを調べます。Native 2回とPyEmuera 1回の保存出力には、選択した状態 `A=919 B=818 R=5 N=1 F=173` と終了マーカーがあります。ログ本文やGUI表示の完全一致は主張しません。Nativeの自然終了と終了コードは未観測です。PyEmuera標準エラーは別ファイルとして保持しています。

## 照合

Python 3の標準ライブラリを使用し、このディレクトリから実行します。

```powershell
python -I -B .\verify.py --manifest-sha256 (Get-Content .\manifest.sha256 -Raw).Trim()
python -I -B .\test_negative.py --manifest-sha256 (Get-Content .\manifest.sha256 -Raw).Trim()
```

macOS / Linuxでは次のように実行します。

```sh
python3 -I -B verify.py --manifest-sha256 "$(cat manifest.sha256)"
python3 -I -B test_negative.py --manifest-sha256 "$(cat manifest.sha256)"
```

外部pin、同梱 `manifest.sha256` の書式・内容、`manifest.json` のSHAがすべて一致することに加え、各ファイルのハッシュ、typed key・ケースID・受入区分、fixture、3出力の選択状態、派生receiptの設定ハッシュなどを確認します。上記のコマンドは同梱pinを使う簡便な整合性検査です。真正性の確認には別経路で得た信頼できるmanifest SHAを `--manifest-sha256` に指定してください。同梱のSHAだけではmanifestの真正性を証明できません。

## 原票と設定の非公開範囲

原票の台帳、親レビュー全文、実行receipt、設定原本はこの証拠ディレクトリに含まれていません。manifestには、それらの原SHA、原JSON上のpointer、派生への選択・変換を記録しています。原票が非公開のため、第三者はそれらの元SHA・pointerから選択値を直接照合できません。派生receiptの数値は原票から選択した記録であり、原receiptの完全性の独立証明ではありません。

3モードの設定SHAは同じです。候補全体の別の場所にある[設定ファイル](../../harness/fixtures/emuera.config)は同じSHA-256 `f08f478f133fa2b1b0887d3a48934138860f3b13be623ecbba453ed85e9a11cc` を持ち、内容を確認できます。この証拠ディレクトリ自体には同梱していません。実行環境・エンジン・fixture配置の完全な再実行手順は含まれていません。SHAの一致だけでは、当時の実行や設定全体の意味上の同一性を証明できません。

以前の親レビューは `finite_remaining_proof` として保持し、後続の追加条件を含む対象の最終受入と区別しています。追加条件のrawは本資料に含まれず、対象全体の差異は再検証できません。

## 出典と再利用条件

Nativeのログ・表示は[Emueraのライセンス原文](../../LICENSES/Emuera1824-v24-license-original.txt)、PyEmueraの出力は[PyEmuera 3.0.0のMITライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。調査fixture・検証コードを含むプロジェクト全体の権利主体と利用条件は別途整理中です。候補の他の部分を含めずこの証拠ディレクトリだけで配布する場合は、必要な表示とリンク先をその配布単位に別途同伴してください。
