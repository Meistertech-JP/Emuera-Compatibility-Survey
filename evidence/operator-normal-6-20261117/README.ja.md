# 演算子の保存記録：6ケース・19 typed対象

[English](README.md)

この資料は6ケース・19 typed対象について、更新Public各1回と過去Native各2回の保存記録を、case・設定・fixtureの対応に基づきまとめた公開候補です。これは実行環境や入力経路を含む**完全な条件一致**、旧Publicと更新Publicの同一build、互換性、全対象の受入れを示しません。6ケースは19個の独立実行ではありません。

各caseのtyped対象、fixture・config・出力のSHAと場所、Public receiptの実行開始・終了時刻、Nativeの時刻不明、入力・自然終了・未観測の制限は [`index.json`](index.json) にあります。Publicの開始・終了は保存receiptのUTCです。Nativeのprobeには実行時刻がなく、過去の保存実行として扱い、ファイル更新時刻を実行時刻に代用しません。

## 収録内容と比較範囲

- `assets/<case>/inputs/` に、両側でSHAが一致したfixtureとconfigを各caseにつき1組収録します。原バイトは変更していません。Nativeの各2回とPublicの入力が同一ハッシュだったことと、全実行条件の同一性は別です。
- 各caseの `public/stdout.bin`・`stderr.bin` と、`native-01/emuera.log`・`native-02/emuera.log` は保存された選択出力の無改変コピーです。Public stdoutはCP932、stderrはUTF-8、NativeログはBOM付きUTF-16です。stderrにはOUTPUTLOGの非fatal警告があり、Nativeとの診断一致を示しません。
- `selected_normal_markers` は6ケース計108件です。3種類の選択出力で各markerが一度ずつ所定順に現れ、その後に `DONE` が一度現れることを確認しました。選択範囲外の出力や全挙動の一致、全対象の到達・成功、描画や終了後状態を意味しません。
- Publicのstdinは継承で内容未記録です。Nativeは別desktopのGUI実行で、保存probeは合成キー送信なしと記録します。外部入力や完全な環境一致は未確認です。Nativeの5秒後の自然終了・終了コードは観測されずcleanupが行われました。Publicの終了をNativeに転用しません。
- 更新Publicの実行前後PYZ SHAと、Native probeに記録されたexe SHAを各caseに掲載します。別エンジンのSHAを同一buildと扱わず、旧Publicの欠落した実行時build証拠を補完しません。

各caseの `case_register_pointer` は元の `CASE_SCENARIO_REGISTER.json` を基点としますが、この元台帳は非同梱です。台帳SHAは `bindings.json` に記載し、原票にアクセスできない第三者はpointerを直接照合できません。別途公開されたcase索引に結ぶ場合はcase IDとその索引のpinを使い、`/records` の配置が同じと仮定しません。保存された元receipt全文、個人パス・プロセス情報、元と派生のprivate対応表、エンジン、未選択の出力は含めていません。各出力・入力の出典と派生バイトのSHA対応は別に保全されています。機微・権利を含む最終公開承認は未了です。

## 検証

Python 3.9以降。別の信頼できる経路から `manifest.json`・`verify.py`・`bindings.json` のSHA-256を取得し、まず独立したハッシュ手段で3ファイルを照合してください。配布物中だけの値は独立した信頼根拠ではありません。bundleのルートで次を実行します。

```text
python -I -B verify.py --manifest-sha256 <信頼済みmanifest SHA256> --verifier-sha256 <信頼済みverifier SHA256> --bindings-sha256 <信頼済みbindings SHA256>
```

verifierは共通file-set toolのSHAを実行前に固定値と照合してから呼び、別pinのcase binding、集合・サイズ・SHAと6ケース／19 typed対象・3保存出力の選択markerの有限結合を確認します。bindingsはcase別の対象、原pointer、fixture/config SHA、marker、選択出力SHA、記録された実行体hashを固定します。信頼済みpinがない場合、manifest・verifier・bindingsの認証はできません。bindingsとpinの両方を未信頼者が差し替えた場合、元の対応を認証できません。いずれも元receiptや実行の真正性、完全な条件一致、権利、互換性を証明しません。エンジンの再実行は行いません。

## 権利と非同梱資料

[権利表示](LICENSES/README.ja.md)、[Emuera原ライセンス](LICENSES/Emuera1824-v24-license-original.txt)と[Emuera NOTICE](vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。Emuera NOTICEは元ZIPを含む別の配布単位を説明し、このbundleにZIP・7zは含まれません。configは保持されたEmuera由来設定と同じバイトです。fixture・調査資料・派生データの権利主体と利用条件は別途未確定で、これらのNOTICEがbundle全体を一括許諾するものではありません。
