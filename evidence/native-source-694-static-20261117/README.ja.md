# Nativeソース位置の静的索引（694対象）

[English](README.md)

`targets.jsonl` は694件のtyped対象を1行ずつ記録する静的索引です。対象名と種別を組にして区別し、ソースの記録位置と限定的なv24照合を示します。元統合票、ソースコード本文、実行結果は同梱していません。ここに記載された位置は、実行の成功、結果の一致、完全実装や網羅性の証明ではありません。

## 対象と照合範囲

| 分類 | 件数 | 内容 |
| --- | ---: | --- |
| 元統合票に位置あり | 661 | 構造化された静的記録425対象と、独立記載の位置236対象 |
| 元統合票に位置なし | 33 | 次のコメント候補3対象と、行位置未特定30対象 |
| うちコメント候補 | 3 | CHKVARDATA、CHKGLOBALDATA、FIND_VARDATA。別監査のコメント位置をv24 ZIP上で確認。アクティブ登録として数えない |
| うち本索引では行位置未特定 | 30 | 演算子29対象とSET。ILオフセットをソース行に置き換えていない |

この30対象については、後続の[ソース位置の追補](../native-source-operator30-20261117/README.ja.md)で、v24の演算子辞書とSETの内部代入経路を別途確認しています。本索引の元統合票に位置がなかったという記録はそのまま保持します。

425対象は、v24の記録された登録テキストが原ZIP内の指定行にあることを確認しました。385行は記録文字列と前後の空白を除いた行全体が一致し、40行は部分文字列として一致します。定義361件とvalidator 61件は記載範囲がファイル内に収まることまでの確認です。独立記載236対象のうち154対象は、v24の関数メソッド辞書の記載行に同名キーがあることを別途確認し、残り82対象の位置は今回v24で確認済みとしていません。425・154・コメント3は別集合です。

この82対象についても、後続の[v24位置追補](../native-source-anchor82-20261117/README.ja.md)で対応する構文位置を確認しています。元アンカーが参照した旧ファイルの版やSHAは引き続き未確立です。

154対象の関数メソッド辞書の同名キーは、命令形式の登録・ルーティング・実行を証明しません。コメント候補について、別監査が報告した辞書初期化子のリテラル不在は、他の登録経路全体の不在を証明しません。[既存の75 API対象](../api-gap75-static-20261117/README.ja.md)は694件に含まれ、425側34件と154側41件です。別に加算しません。

`historical_a7` / `historical_a8` はPyEmuera側の歴史的監査の版ラベルであり、Emueraの版名ではありません。旧記録の行をv24と同一視できません。独立記載の一部はファイル名だけで、版・ディレクトリ・役割を一律にv24へ結び付けられません。`v24_audit` と `v24_same_name_function_dictionary` は上記の限定照合です。

`v24_source_file_sha256` はv24 ZIP内ソースファイル全体のSHA-256です。`contract_declared_sha256` は元監査の契約欄に記録されたSHAで、ファイル全体のSHAとは限りません。GCREATED、GWIDTH、GHEIGHTの3件では、元監査の登録テキストのUTF-8 SHAと契約欄のSHAが一致しなかったため、本索引の当初の状態は `mismatch_unresolved` のまま保持しています。[後続の追補](../native-source-sha-supplement-20261117/README.ja.md)では、保存版の生成手順とv24ソースから、コメントとCRを含む元文字列のハッシュとして3件の契約SHAを再現しました。これはv24ファイル全体のSHA不一致ではなく、当時使用されたコードの真正性を証明するものでもありません。

## 原ソースを参照する

[Emuera配布物](../../vendor/emuera/README.ja.md)の `Emuera1824-v24-with-notices.zip` には、NOTICE 2通と無改変の `Emuera1824+v24.zip` が入っています。原ZIPのSHA-256は `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a` です。原ZIP内の `Emuera1824+v24/src1824+v24/src1824/Emuera/` 以下にソースファイルが展開された形で入っています。索引中のv24の `file` はこのディレクトリからの相対パスです。

リポジトリのルートから、既存ファイルと重ならない作業ディレクトリを `WORK` として、次のように2段階で展開できます。原ZIPを取得した後、信頼できる方法で上記SHAを照合し、内側ZIPとNOTICEを同伴させてください。

```text
python -m zipfile -e vendor/emuera/Emuera1824-v24-with-notices.zip WORK/outer
python -m zipfile -e WORK/outer/Emuera1824+v24.zip WORK/unpacked
```

例えば `GameData/Function/Creator.cs` は `WORK/unpacked/Emuera1824+v24/src1824+v24/src1824/Emuera/GameData/Function/Creator.cs` です。記載行とファイルSHAを確認するにはテキストビューアとSHA-256ツールを使えます。エンジンの起動は不要です。

## ファイル整合性の確認

Python 3.9以降を使用します。まず**信頼できる別経路**から、この索引の `manifest.json` と共通 `tools/file_set_manifest.py` それぞれの期待SHA-256を取得してください。同じ配布物内の値だけでは独立した信頼の根拠になりません。次はリポジトリのルートで実行するPowerShellの例です。2つのプレースホルダーを取得した値に置き換えてください。

```powershell
$expectedManifest = '<trusted-manifest-sha256>'
$expectedTool = '<trusted-tool-sha256>'
$manifest = 'evidence/native-source-694-static-20261117/manifest.json'
$tool = 'tools/file_set_manifest.py'
if ($expectedManifest -notmatch '^[0-9a-fA-F]{64}$' -or $expectedTool -notmatch '^[0-9a-fA-F]{64}$') { throw 'Trusted SHA-256 values are required' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $manifest $expectedManifest
if ($LASTEXITCODE -ne 0) { throw 'Manifest SHA-256 mismatch' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $tool $expectedTool
if ($LASTEXITCODE -ne 0) { throw 'Tool SHA-256 mismatch' }
python -I -B $tool verify --manifest $manifest --root index=evidence/native-source-694-static-20261117
if ($LASTEXITCODE -ne 0) { throw 'File-set verification failed' }
```

manifestはこのディレクトリのファイル集合・サイズ・SHAの整合性を確認するものです。外部pinによって固定されたファイルへの変更を検出できますが、元票の内容、由来、実行、各行の意味や公開許諾の真正性は証明しません。非同梱の元票をこの手順から検証することもできません。共通ツールと権利表示・Emuera ZIPはこのmanifestの対象外であり、それぞれ別途確認してください。

## 権利と配布状況

[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)と[日本語NOTICE](../../vendor/emuera/NOTICE.ja.md)は参照するEmuera配布物に適用される表示です。[PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)と[第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)も参照してください。これらは調査索引・元統合票・説明文の全体に自動的に適用される許諾ではありません。調査資料の権利主体と配布条件は未確定であり、公開条件は未承認です。
