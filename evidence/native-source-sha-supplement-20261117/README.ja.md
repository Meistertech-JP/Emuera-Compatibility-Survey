# 3件の登録契約SHAの後続照合

[English](README.md)

[694対象の静的索引](../native-source-694-static-20261117/README.ja.md)が未解決として記録したGCREATED・GWIDTH・GHEIGHTについて、後続の静的照合で契約SHAの算出条件を再現しました。対象は3件の式関数のv24登録で、索引自体は変更していません。索引の `mismatch_unresolved` は当時の記録であり、この追補が3件のSHA差の説明を追加します。実行結果、機能互換性、他の登録や公開全体を判定するものではありません。

## 再現された条件

原ZIPの `GameData/Function/Creator.cs` の各行で、登録部分の開始から次のLFの直前までを、コメントを含む元テキストから切り出してUTF-8でSHA-256化すると契約SHAと一致します。この3行はCRLFで、切り出しは行頭のインデントを含まず、コメントとCRを含み、LFを含みません。表示用の登録テキストは、同範囲のコメントとCRを空白化した文字列であり、そのUTF-8 SHA-256は契約SHAと異なります。表示用文字列の末尾の空白もハッシュ対象です。

| 式関数 | 行 | 契約SHA-256 | 表示用登録テキストのUTF-8 SHA-256 |
| --- | ---: | --- | --- |
| GCREATED | 171 | `63aee4d35c0444cee4e06ee292f691e768246b8673db9919ea0af407e1ccd660` | `e40541b2e9829f720873c61115f638a92d847e8aa8f0324fbe6c0fe12544115d` |
| GWIDTH | 172 | `471ccf05062354021044d22fedbb2ca7d72acc19aa58a2c53aec5acfb6c510eb` | `83ebe1e884c7c4e81c5b8fc1c28353a6093de4195efbe92568171e31747b4d73` |
| GHEIGHT | 173 | `5bfab797a278a3c5065d6c2478c7ce7a2c508014b9d674e33581206b0e6efd6c` | `976c26bf693ad4ede9a2781b5086970bd34de732eabfadefcd62cc47a28f5d6e` |

機械可読の値は [results.json](results.json) にあります。ソース位置は原ZIP内の `Emuera1824+v24/src1824+v24/src1824/Emuera/` からの相対位置です。原ZIPのSHA-256は `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a`、対象ソースファイル全体は `b2e5f60c5457741208ba99b991cced5106b22834b00347876dea411a3e0dd36a` です。[Emuera配布物の案内](../../vendor/emuera/README.ja.md)も参照してください。

この結果は、保存版の生成コード `reference_contracts.py`（SHA-256 `bdb2837519e499908e48af065ea4f1b8ef43c8d649f239691303361a818b12e4`）と上記ソースから再現したものです。この追補には生成コード、元監査票、原ソースは同梱していません。保存版での再現は、当時実際に使われたコードの真正性や実行履歴の証明ではありません。

## ファイル整合性

Python 3.9以降を使用します。別の信頼できる経路から、この追補のmanifestと共通ツールそれぞれの期待SHA-256を取得し、リポジトリのルートで照合してください。同じ配布物内だけの値は独立した信頼根拠になりません。

```powershell
$expectedManifest = '<trusted-manifest-sha256>'
$expectedTool = '<trusted-tool-sha256>'
$manifest = 'evidence/native-source-sha-supplement-20261117/manifest.json'
$tool = 'tools/file_set_manifest.py'
if ($expectedManifest -notmatch '^[0-9a-fA-F]{64}$' -or $expectedTool -notmatch '^[0-9a-fA-F]{64}$') { throw 'Trusted SHA-256 values are required' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $manifest $expectedManifest
if ($LASTEXITCODE -ne 0) { throw 'Manifest SHA-256 mismatch' }
python -c "import hashlib,sys;sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest().lower()!=sys.argv[2].lower())" $tool $expectedTool
if ($LASTEXITCODE -ne 0) { throw 'Tool SHA-256 mismatch' }
python -I -B $tool verify --manifest $manifest --root supplement=evidence/native-source-sha-supplement-20261117
if ($LASTEXITCODE -ne 0) { throw 'File-set verification failed' }
```

manifestはこの追補のファイル集合・サイズ・SHAを検査します。外部pinの照合は変更の検出に役立ちますが、元資料の真正性、記載の意味、当時の実行、権利を証明しません。共通ツール、索引、ライセンス表示、原ZIPはこのmanifestの対象外です。

## 権利と表示

[Emuera原ライセンス](../../LICENSES/Emuera1824-v24-license-original.txt)、[Emuera NOTICE](../../vendor/emuera/NOTICE.ja.md)、[PyEmueraライセンス](../../LICENSES/PyEmuera-3.0.0-LICENSE.txt)および[第三者表示](../../LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。各表示は該当する参照素材に関するもので、この追補を含む調査成果のすべてへの許諾を自動的に示すものではありません。調査資料の権利主体と配布条件は未確定です。
