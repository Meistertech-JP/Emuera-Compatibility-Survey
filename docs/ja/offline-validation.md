# オフラインでの検証

[English](../en/offline-validation.md) | [調査データの読み方](results.md)

Python 3.10以上を使用し、展開した候補のルートからコマンドを実行してください。このページの手順は、選択したファイルや記録のオフライン照合に使います。エンジンの起動は不要です。

信頼できる別経路からmanifestや検証スクリプトのSHA-256・署名を入手済みであれば、実行前に照合してください。成功時に確認できる範囲は、資料ごとに下記に示します。当時の実行、来歴、配布条件の確認には別の根拠が必要です。

## 配布物全体と調査台帳

候補のルートから全ファイルの集合、SHA-256、サイズを照合します。manifest自身のSHA-256は配布物の外で確認してください。

```powershell
python -B tools/file_set_manifest.py verify --root repo=. --manifest manifests/public-file-set.json
python -B results/verify.py
python -B results/test_verify.py
python -B tools/verify_environment.py
```

台帳検査の負例は使い捨てコピーを変更して、改変や欠落が拒否されることを確認します。保存比較の照合とエンジンの再実行は別の検証です。

## 選択された7資料のファイル集合

共通の [file-setツール](../../tools/FILE_SET_MANIFEST.ja.md) は、指定されたmanifestに対し対象ディレクトリのファイル集合、サイズ、SHA-256を照合します。検証する資料のコマンドを実行してください。指定する `bundle`、`layer`、`evidence` は各manifestに記録されたルート名です。

```powershell
python -I -B tools/file_set_manifest.py verify --manifest evidence/compound-trailing-comma-20261117/manifest.json --root bundle=evidence/compound-trailing-comma-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/legacy-acceptance-269-20261117/manifest.json --root layer=evidence/legacy-acceptance-269-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/nine-saved-observations-20261117/manifest.json --root evidence=evidence/nine-saved-observations-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/parent-restoration-40-20261117/manifest.json --root evidence=evidence/parent-restoration-40-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/twaitzero-observation-20261117/manifest.json --root bundle=evidence/twaitzero-observation-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/wait-c15-20261117/manifest.json --root evidence=evidence/wait-c15-20261117
python -I -B tools/file_set_manifest.py verify --manifest evidence/wait-release-20261117/manifest.json --root evidence=evidence/wait-release-20261117
```

終了コード0と `verify: OK` は、対象集合がmanifestと一致したことを示します。資料ごとの観測内容と限界は、それぞれのREADMEを参照してください。

- [複合代入の末尾カンマ](../../evidence/compound-trailing-comma-20261117/README_ja.md)・[9件の保存観測](../../evidence/nine-saved-observations-20261117/README.ja.md)
- [旧受入の対応記録](../../evidence/legacy-acceptance-269-20261117/README.ja.md)・[親ケースの復元記録](../../evidence/parent-restoration-40-20261117/README.ja.md)
- [TWAIT 0,1](../../evidence/twaitzero-observation-20261117/README.ja.md)・[WAIT C15](../../evidence/wait-c15-20261117/README.ja.md)・[WAIT解除](../../evidence/wait-release-20261117/README.ja.md)

## 代表例とcase register

[代表的な観測](../../differences/representative-20261116/README.ja.md)は、`differences/representative-20261116` と `evidence/representative-20261116` を一緒に使います。次の検証は4ケースの選択されたファイル、記録された設定や出力の一部などを確認します。エンジンによる再現は行いません。

```powershell
python -I -B differences/representative-20261116/verify.py
```

[case register](../../evidence/case-register-2898-20261117/README.ja.md)は別形式です。検索の例として、次のコマンドを実行できます。

```powershell
python -I -B tools/query.py SEARCH02_STRFINDU_A_NEG1
```

結果の `case_register_projection_availability` と `case_register_projection` を確認してください。関連するsurvey・traceの状態が `NOT_INSTALLED` または `SNAPSHOT_MISMATCH` なら、その資料との照合は行われていません。検索時には投影ファイルのhash・件数と該当行などを検査しますが、詳細欄は検索結果に出力されず、全caseの意味を検証するものではありません。

## 旧形式の参照と保存観測

候補のルートから保存証拠の検証を実行します。

```text
python -B tools/verify_saved_evidence.py
```

検証器は、旧形式索引と保存観測の対応を照合します。同梱バイト列のサイズとハッシュ、派生参照のケースID・ポインター・出典ハッシュを確認し、非公開原本にパスが載っていないことを検査します。出力は展開した候補内の記録の内訳です。[旧形式の証拠参照](results.md#旧形式の証拠参照)も参照してください。

## 確認できる範囲

一部の資料には選択されたraw、fixture、画面またはreceiptが含まれます。一方、旧受入・親ケースの復元記録とcase registerには、対応する原記録や原rawが含まれません。選択rawを含む場合でも、元runの全履歴、入力が消費されたこと、自然終了などは確認できない場合があります。各READMEに示す未観測範囲を確認してください。

[`results/verify.py`](../../results/verify.py) は調査台帳と差異索引を照合します。旧形式索引では、同梱バイト列への相対参照、派生観測への参照、原本を公開しない参照を区別します。候補だけで過去の調査全体を独立に再現できることは確認されていません。[旧形式の証拠参照](results.md#旧形式の証拠参照)を参照してください。
