# 停止後stateの限定観測

[English](README_en.md)

この記録は、保存済み4条件におけるSWAPと数値代入の選択global/cellの観測をまとめます。新しいengine実行やGUI操作は含みません。

## 観測と診断

- **SWAP正常対照**：Native内蔵Debug consoleのliteral readsでD:0/D:1を11,22から22,11と観測。PyEmueraのbefore値は実行出力marker、after値は明示entryを含むPDB storage-map snapshotです。
- **SWAP第2添字エラー**：5行目で停止。Native Debug consoleはDのindex 1,000,000が1,000要素配列の範囲外と表示。PyEmueraは`E_INDEX`、5行目、D index 1,000,000、dimension `(1000,)`を記録。Nativeの2セルは同一停止process内の直接読み。Pyは同一停止VM内のstorage mapを2回観測し、明示entry `(0,):11`, `(1,):22` を確認しました。個別cell getを実行した記録ではありません。
- **数値代入正常対照**：Nativeは31,47から7,9をliteral readsで観測。PyEmueraはPDB mapの明示entry `(0,):7`, `(1,):9` を観測しました。これは個別cell getではありません。
- **数値代入bad-index停止**：14行目で停止。Native Debug consoleはZZV index 2が2要素配列の範囲外と表示し、ZZV:0/1を同一停止process内で直接2回読み0,0。PyEmueraは`E_INDEX`、14行目、ZZV index 2、dimension `(2,)`を記録。Py PDBはshape `[2]`、sparse map `{}`、default `0` を同一停止VM内で2回表示しました。個別cell getは保存されていません。固定pyzの`pyemuera/data.py`にある`values.get(tuple(key), default)`に基づき、有効なZZV:0/1の値0,0を推論します。これはNative直接readbackとは異なる種類の根拠です。

record内の診断要約は各Native UIA/Py error recordのsource pin IDとSHAに対応します。エンジンごとの文言・観測方法は別々に記録し、同一のエラー表現や終了結果とは主張しません。各「2回」は一つの停止process/VM内での反復であり、独立した2実行ではありません。

## source IDと実際の観測範囲

数値代入bad-index停止のsource case ID `OPISOLATED265_plain-num-badindex` は、比較台帳で `=` と `==` の両方に関連付けられています。一方、この停止後fixtureの式は `ZZV:ZZIDX() = ZZL()` で、実際に実行・観測したtarget roleは `=` のみです。`==` はこの条件では実行も観測もしていません。台帳上の関連付けを、このfixtureでの観測範囲として読まないでください。機械recordの `source_scope_binding` にも同じ区別を記録しています。

## 記録範囲

[`observations.json`](observations.json)にはcase ID、typed key、入力・engine SHA、観測方式、診断要約とsource pin、推論、値、未観測範囲を記録します。全state、Natural exit、LOCAL/REF、全配列、途中setterの不存在は主張しません。

元raw、Native UIA、Py PDB、fixtureのbytesは付属しません。記録中のSHAは保存bytesとの対応を示しますが、bytesがない第三者はこのbundleだけから診断や状態を独立再検証できません。

## 検証

このbundleのルートディレクトリを作業ディレクトリにし、Pythonを起動する前に `verify.py` と `manifest.json` のSHA-256を両方とも照合してください。各期待値はbundle外の独立した信頼経路から取得します。bundle内README、manifest、record、その他同梱値から得た期待値は独立照合になりません。この配布物について独立pinを発行する主体・経路は指定していません。両方の期待値を別途取得できない場合、実行前の真正性確認は未確定です。

Windows PowerShellの例（両placeholderを独立に取得した値に置き換えてから実行）：

```powershell
Set-Location -LiteralPath '<unpacked bundle root>'
$expectedVerifier = '<SHA-256 of verify.py from an independent trusted channel>'
$expectedManifest = '<SHA-256 of manifest.json from the same independent trusted channel>'
$actualVerifier = (Get-FileHash -LiteralPath .\verify.py -Algorithm SHA256).Hash.ToLowerInvariant()
$actualManifest = (Get-FileHash -LiteralPath .\manifest.json -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualVerifier -ne $expectedVerifier.Trim().ToLowerInvariant()) { throw 'verify.py SHA-256 mismatch; do not run Python' }
if ($actualManifest -ne $expectedManifest.Trim().ToLowerInvariant()) { throw 'manifest.json SHA-256 mismatch; do not run Python' }
python -B .\verify.py
```

検証器はこの固定版のobservations SHA、manifestの記載file SHA/size、相対link、および一部のcase・typed key・診断pin・未観測フィールドの制約を確認します。全recordの各値、観測方式やrepeatの意味的正しさ、source registerとの関連、非同梱rawとの対応を独立に証明するものではありません。特に元raw、Native UIA、Py PDB、fixture bytesは同梱されず、このbundleだけでは実測や診断を原記録に遡って再照合できません。hash検査のPASSは、すべての観測主張が真であることの証明ではありません。recordまたはsourceが変わる場合は元の比較台帳とrawを別途照合し、新しい版のverify.pyも実行前に独立pin照合してください。
