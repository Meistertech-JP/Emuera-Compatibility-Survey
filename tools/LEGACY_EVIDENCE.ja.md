# 旧証拠を読む限定 adapter

[English](LEGACY_EVIDENCE.md)

`legacy_evidence.py` は、指定した audit snapshot から **１つの型付き対象**を選び、実在する３種類の構造とPRINTC/PRINTLCの限定形式について、宣言済み SHA-256 と一部の参照・case ID・対象種別・記録済み outcome を読み取り専用で確認します。データの匿名化、元の判定の変更、台帳への書戻し、エンジン起動はしません。テストで使用するデータはすべて作成した架空の fixture で、非公開原証拠のコピーは含みません。

| 形式 | 確認する範囲 | 残る制約 |
|---|---|---|
| `parent-target-finite-scope-adjudication-1` | 型付き受入、declared comparison、比較票の fixture と指定された形式の mode 名に合うログ・config pin | receipt は path だけで pin がないため未固定。比較票を独立 readback として昇格しない。観測内容の意味は再判定しない |
| `phase2-target-parent-acceptance/v1` | 型付き受入、audit 指定 readback の SHA、受入への backlink と case ID。該当形式では typed target と記録 outcome も確認 | outcome のない readback に outcome を補わない。個別 raw に解決できないハッシュのみの参照・登録回数は未検証 |
| `original-return-three-parent-acceptance-1` | 型付き受入から pin 付き readback、受入 case に該当する mode ごとの raw/stderr/receipt と存在する probe の pin | readback の他ケースは未確認。target 名一覧は独立した typed target の証明ではない |
| `target-finite-comparison-adjudication-1` のPRINTC/PRINTLC column-boundary限定 | 親受入、固定case register、親manifest、3 modeの入力・config・outputlog・receipt、Native probe・exe、対象のfixture条件・整形文字列・sentinel | 他の同schema対象は非対応。Py pyz本体は検査外。原要件の意味的充足や自然終了を証明しない |

共通結果は、元 audit の `row_outcome`、取得できた `declared_outcome`、照合した参照と、元の `gaps` を区別します。`PARTIAL` は限定された検査ができた意味であり、対象完了・互換性・raw の意味的な正しさを示しません。未対応形式・受入票なしは `UNSUPPORTED`、存在しない／pin 不明・不正・対象違い・矛盾は `INVALID` です。後付けの pin や readback、自然終了を推定しません。

## 実行

Python 3.10 以上。データを読み取るルート、ルート相対の audit JSON、および**別途信頼した audit の SHA-256** を明示します。以下は形式例で、対象ファイルの公開・入手可能性を示しません。ツールは元の audit とその宣言先を変更しません。

```powershell
python -B tools/legacy_evidence.py --root <証拠ルート> `
  --audit <ルート相対のaudit.json> --audit-sha256 <監査票のSHA256> `
  --kind command_or_syntax --name <対象名>
```

サポートする snapshot schema は `read-only-uniform-acceptance-chain-audit-1` の `rows` です。参照はルート相対とし、旧 Windows 区切りは正規化します。絶対パス・親ディレクトリ・symlink/reparse point、重複参照、改変・欠落・pin 未指定は拒否します。元ファイルの公開用変換により SHA が変わる場合、元 pin を書き換えず、別の検証可能な派生データと対応関係を整備する必要があります。

終了コードは `1` が `INVALID`、`2` が `PARTIAL` または `UNSUPPORTED` です。この限定 adapter に全面検証成功の終了コード0はありません。結果には入力データ中の相対パスや case ID、audit gap が含まれ得るため、公開前に別途確認してください。指定した SHA は外部で信頼・固定した値である必要があり、入力と SHA を同時に書き換えられる場合の真正性は保証できません。読み取り中の競合を完全なスナップショットとして扱わないでください。

従来３形式のcase-role結合はpin済みaudit snapshotを参照し、元case register自体は再検査しません。PRINTC/PRINTLC限定形式では、auditでpinされたcase register snapshotと型付き対象・case pointerを追加照合します。原要件と case・readback の意味論的な十分性、原証拠の全実行モード・旧226対象への適用範囲、非公開参照の公開移植、権利・機密監査は対象外です。

```powershell
python -B -m unittest discover -s tests -p 'test_legacy*.py' -v
```

## PRINTC / PRINTLCの範囲

固定親票から `native-01`、`native-02`、`public-01` を別々に検査します。空文字・ASCII 3文字・幅25文字の条件と出力行、`RESULT=777`、`RESULTS=SENTINEL` に限定します。共有fixtureの３modeを、２caseや６条件の独立起動として数えません。Nativeの自然終了は記録から確認できず、Pyの実行体はreceiptのSHAを記録するだけで元bytesを検査しません。receipt内の実pathや管理値は結果に写さず、参照パス・case ID・gapは出力に含まれます。

元audit・親票・fixture・config・raw・receipt・engineはこのツールに同梱していません。この資料だけで元の実行を再現・再検証できるとは限りません。元fixtureや出力の権利・公開条件は別途確認が必要です。byteが同じ２modeのrawを入れ替えたこと自体は、そのbytesから区別できません。mode別receiptの固定と記録内容を照合します。
