# 保存された有限比較の証拠（2026-11-16）

[English](README.md)

Native Emuera1824+v24とPyEmuera 3.0.0の、有限範囲の実行から選んだ暫定証拠です。原ログ・fixture・所有ウィンドウのcropを無改変で収録し、結果記録は原票から必要な項目を選んだ派生物です。原process receipt・attempt封印は含みません。

```text
python -B verify.py
```

ファイル集合とSHA-256、選択したログの観測値、cropのファイル形式と固定ハッシュ、設定・ライセンスの同一性を検査します。画像の文字の意味を自動判定したり、エンジンを起動したり、非公開原本の封印や著作者を検証したりするものではありません。manifestは署名ではありません。

## 含まれるケース

| 対象 | 記録と制限 |
|---|---|
| [式比較](expression/successful-rerun/plan.json) | `ABS((-7 + (RESULT:0 - 701)))` は双方7。`STRFINDU("abc","",(3 + (RESULT:0 - 701)))` と同引数の `STRFIND` はNative -1・Py 3。ABS単独と3件batchは別fixtureで、各Native 2回。RESULT:0=701、RESULT:1=702、RESULTS=AUTO_SENTは各観測で維持。 |
| [状態書換](local/state-write/fixture.ERB) | `TOINT "42"`、`TOSTR 123` の前後で、RESULT:0は701→42、RESULTSはAUTO_SENT→123。両側のログに同じ順序で記録。 |
| [数値入力](local/input-number/fixture.ERB) / [文字列入力](local/input-string/fixture.ERB) | P35は42、P36はABCを入力。Native入力前後cropとPy stdoutにそれぞれ42、`[ABC]` を記録。画像の読取は手動。 |
| [数値＋OUTPUTLOG](local/input-number-logged/fixture.ERB) / [文字列＋OUTPUTLOG](local/input-string-logged/fixture.ERB) | 別fixtureで42／ABCを入力し、両ログに `INPUT_RESULT=[42]`／`INPUT_RESULTS=[ABC]` を記録。前後cropも同梱。元fixtureとは区別する。 |
| [引数省略](local/argument/fixture.ERB) | Nativeは `BEFORE` の後、3行目の `TOINT` 引数個数エラー。Pyは `BEFORE` の後、3行目で `E_ARGUMENT`。stdout・診断・cropを同梱。 |
| [構文と停止位置](local/syntax-stop/fixture.ERB) | Nativeは読み込み警告の後 `BEFORE`、3行目で対応する `ENDIF` がないエラー。Pyは読み込み時 `E_SYNTAX`、`BEFORE` はstdoutで未観測。stdout・診断・cropを同梱。P38 cropは先頭警告の右側が一部切れている。 |

記録された観測後にNativeは強制終了しており、自然終了は未観測です。GUIは隔離デスクトップの所有ウィンドウの左下cropを人が確認した観測です。画面全体、IME、他の入力条件やNativeの自然終了は確認していません。エラーケースでは実行時のfixture固定検査は確認されていません。入力ケースでは実行時のfixture固定検査が記録されています。

## 設定・出典・公開範囲

[`config/emuera.config`](config/emuera.config) は元試行と同一のCP932原バイトで、SHA-256は `configuration.json` にあります。実機再現には別途エンジン、環境、実行手順が必要です。エンジン実行ファイルはこの証拠パッケージには含みません。

Emuera由来の設定・画面・診断は[Emueraライセンス原文](LICENSES/Emuera1824-v24-license-original.txt)、PyEmueraの診断は[MITライセンス](LICENSES/PyEmuera-3.0.0-LICENSE.txt)および[第三者表示](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md)を参照してください。第三者表示はPyEmuera 3.0.0ソース配布物の原文であり、記載されたゲームなど、この証拠パッケージに含まれないものも説明しています。原文中のファイルパスは元の配布物を指します。画面はウィンドウのクロップのみを保持したもので、元のフル画面ではありません。fixture、ログ、cropは各ケースの実行に紐付け、同じバイトの別試行を統合していません。

配布物はmanifest列挙ファイルと `manifest.json` から作成します。原receipt・元封印・内部変換対応表は別途非公開で保管し、含めません。画像を含む証拠は手動の読み取りが必要です。候補全体の最終公開監査は別途必要です。

## 生記録への入口

- 式batch：[本家1回目](expression/successful-rerun/batch/native-01.log)、[本家2回目](expression/successful-rerun/batch/native-02.log)、[Py](expression/successful-rerun/batch/py.log)。ABS単独は `single/`。
- 状態書換：[本家](local/state-write/native.log)、[Py](local/state-write/py.log)。
- 引数：[本家診断](local/argument/native-diagnostic.log)、[Py stdout](local/argument/py-stdout.bin)、[Py診断](local/argument/py-stderr.bin)。
- 構文：[本家診断](local/syntax-stop/native-diagnostic.log)、[Py stdout](local/syntax-stop/py-stdout.bin)、[Py診断](local/syntax-stop/py-stderr.bin)。
- 入力後の本家画面：[数値](local/input-number/native/crop-after.bmp)、[文字列](local/input-string/native/crop-after.bmp)、[数値＋ログ](local/input-number-logged/native/crop-after.bmp)、[文字列＋ログ](local/input-string-logged/native/crop-after.bmp)。
