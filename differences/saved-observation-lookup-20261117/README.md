# Saved observation lookup

## English

This package lets you search a **bounded set of saved observations** in the research repository. It covers 129 typed items and 1,842 recorded fields. It reads the recorded values from the repository files; it does not rerun either engine or claim complete coverage.

### 1. Prepare the files

Keep this folder and a finalized, read-only copy of the research repository available locally. Open PowerShell in this folder and set `$ROOT` to that repository copy. Use Python 3.9 or later.

### 2. Check the saved files

The checker confirms that the pinned files and recorded field pointers still match. The hashes below identify the exact lookup data and checker used by this package.

```powershell
$ROOT = '<path to the finalized read-only research repository>'
python -I -B verify_v4.py --repository-root $ROOT --index-sha256 6ff1f5f7a153a7bf6e489e0ea41a83cb9f527321f33ec48732f29e112493beab --profile-sha256 6d1e9e9bdf6c0f10bc53887bd661a36abc2d8c7870a819fe6936b95759086566 --dependencies-sha256 c6ba2d7e9632fcb8b2e61bc441ccf7f846131eb5112500c9c9a9da6f8600629b
```

### 3. Search a saved observation

Search by a saved record name or typed item. For example, this case lookup returns six recorded fields:

```powershell
python -I -B query_v4.py UIQUERY236_cbgsetg-expr-direct --repository-root $ROOT --index-sha256 6ff1f5f7a153a7bf6e489e0ea41a83cb9f527321f33ec48732f29e112493beab --profile-sha256 6d1e9e9bdf6c0f10bc53887bd661a36abc2d8c7870a819fe6936b95759086566 --dependencies-sha256 c6ba2d7e9632fcb8b2e61bc441ccf7f846131eb5112500c9c9a9da6f8600629b --verifier-sha256 6c7fe09daa41b310a772e1d769167897d184554db32677ff2c934a1a3f8b9468
```

Each result shows the saved value, case name, relative file path, and JSON Pointer. For example, the recorded value `OBS236 V=0 R=701 A=0` is in `evidence/console-background-24-20261117/records.json` at `/cases/0/native_01_selected_rows`. You can read that field directly from the same repository copy:

```powershell
$record = Get-Content (Join-Path $ROOT 'evidence/console-background-24-20261117/records.json') -Raw | ConvertFrom-Json
$record.cases[0].native_01_selected_rows
```

The recorded case scope is `saved_case_not_target_acceptance`. GUI pixels, click or mouse events, and the entire background state were not observed. The result reports the saved record; it does not independently establish how the original run occurred.

### 4. Understand a result with no case-specific link

Some items have shared-batch references but no case-specific field in this lookup. For example, `SPRITEWIDTH` returns zero linked fields. The result does not provide a case or raw-record link, and does not imply that other evidence is absent.

### Fixed lookup data

- Search index SHA-256: `6ff1f5f7a153a7bf6e489e0ea41a83cb9f527321f33ec48732f29e112493beab`
- Observation profile SHA-256: `6d1e9e9bdf6c0f10bc53887bd661a36abc2d8c7870a819fe6936b95759086566`
- Required-file list SHA-256: `c6ba2d7e9632fcb8b2e61bc441ccf7f846131eb5112500c9c9a9da6f8600629b`
- Checker SHA-256: `6c7fe09daa41b310a772e1d769167897d184554db32677ff2c934a1a3f8b9468`
- Search program SHA-256: `91dd08a2581653f8b565af3744aec2dffdac6cb077eb720e643c869a14a39c9c`

---

## 日本語

このパッケージは、調査リポジトリに保存された**限定範囲の観測記録**を検索します。型付き項目129件、保存記録のfield 1,842件を対象にします。値はリポジトリ内の記録から読み出します。Emuera/PyEmueraの再実行や、全範囲の網羅を主張しません。

### 1. ファイルを用意する

このフォルダーと、固定後の調査リポジトリのread-only copyを手元に置きます。このフォルダーを開いたPowerShellで `$ROOT` にそのcopyの場所を設定します。Python 3.9以降が必要です。

### 2. 保存ファイルを検証する

検証器は、固定されたファイルと記録fieldへのpointerが一致することを確認します。下記のSHAは、このパッケージが使う検索データと検証器を特定します。

```powershell
$ROOT = '<固定後のread-only調査リポジトリの場所>'
python -I -B verify_v4.py --repository-root $ROOT --index-sha256 6ff1f5f7a153a7bf6e489e0ea41a83cb9f527321f33ec48732f29e112493beab --profile-sha256 6d1e9e9bdf6c0f10bc53887bd661a36abc2d8c7870a819fe6936b95759086566 --dependencies-sha256 c6ba2d7e9632fcb8b2e61bc441ccf7f846131eb5112500c9c9a9da6f8600629b
```

### 3. 保存観測を検索する

保存記録名または型付き項目名で検索できます。次のcase検索は記録fieldを6件返します。

```powershell
python -I -B query_v4.py UIQUERY236_cbgsetg-expr-direct --repository-root $ROOT --index-sha256 6ff1f5f7a153a7bf6e489e0ea41a83cb9f527321f33ec48732f29e112493beab --profile-sha256 6d1e9e9bdf6c0f10bc53887bd661a36abc2d8c7870a819fe6936b95759086566 --dependencies-sha256 c6ba2d7e9632fcb8b2e61bc441ccf7f846131eb5112500c9c9a9da6f8600629b --verifier-sha256 6c7fe09daa41b310a772e1d769167897d184554db32677ff2c934a1a3f8b9468
```

各結果には保存値、case名、リポジトリ相対path、JSON Pointerが表示されます。例えば `OBS236 V=0 R=701 A=0` は `evidence/console-background-24-20261117/records.json` の `/cases/0/native_01_selected_rows` に記録されています。同じリポジトリcopyから直接読み出す場合は次の通りです。

```powershell
$record = Get-Content (Join-Path $ROOT 'evidence/console-background-24-20261117/records.json') -Raw | ConvertFrom-Json
$record.cases[0].native_01_selected_rows
```

このcaseの判定範囲は `saved_case_not_target_acceptance` です。GUI pixel、click/mouse event、background全体のstateは未観測です。検索結果は保存recordを示し、過去の実行過程を独立に証明しません。

### 4. case別linkのない結果を読む

共有batchへの参照があっても、この検索にcase別fieldがない項目があります。例として `SPRITEWIDTH` はlink 0件です。結果にcase/raw-recordへのlinkはなく、他の証拠が存在しないという意味でもありません。

### 固定された検索データ

- 検索index SHA-256: `6ff1f5f7a153a7bf6e489e0ea41a83cb9f527321f33ec48732f29e112493beab`
- 観測profile SHA-256: `6d1e9e9bdf6c0f10bc53887bd661a36abc2d8c7870a819fe6936b95759086566`
- 必須ファイル一覧 SHA-256: `c6ba2d7e9632fcb8b2e61bc441ccf7f846131eb5112500c9c9a9da6f8600629b`
- 検証器 SHA-256: `6c7fe09daa41b310a772e1d769167897d184554db32677ff2c934a1a3f8b9468`
- 検索プログラム SHA-256: `91dd08a2581653f8b565af3744aec2dffdac6cb077eb720e643c869a14a39c9c`

