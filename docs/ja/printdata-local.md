# PRINTDATA・STRDATA：文字列状態とログの折り返し

[English](../en/printdata-local.md) · [保存観測61ケース](../../evidence/printdata-61-20261117/README.ja.md)

次の5条件では、命令前に `LOCALS:0` を `PLAN_LOCAL_STRING` に設定し、命令後の状態を出力しています。本家の出力ログでは、各状態行の `LOCAL` 値の途中に物理改行が入ります。表の `\r\n` はログに記録された改行です。本家の2保存modeの該当ログは条件ごとに同一です。

| 条件 | 本家ログのLOCAL部分 | PyEmueraのLOCAL部分 | fixture・ログ |
|---|---|---|---|
| `PD_EMPTY_LIST` | `PL\r\nAN_LOCAL_STRING` | `PLAN_LOCAL_STRING` | [入力](../../evidence/printdata-61-20261117/assets/BATCH020/native-01/inputs/ERB/MAIN.ERB) · [本家1](../../evidence/printdata-61-20261117/assets/BATCH020/native-01/raw.bin) · [本家2](../../evidence/printdata-61-20261117/assets/BATCH020/native-02/raw.bin) · [PyEmuera](../../evidence/printdata-61-20261117/assets/BATCH020/public-01/raw.bin) |
| `PD_EMPTY_FORM` | `PL\r\nAN_LOCAL_STRING` | `PLAN_LOCAL_STRING` | [入力](../../evidence/printdata-61-20261117/assets/BATCH021/native-01/inputs/ERB/MAIN.ERB) · [本家1](../../evidence/printdata-61-20261117/assets/BATCH021/native-01/raw.bin) · [本家2](../../evidence/printdata-61-20261117/assets/BATCH021/native-02/raw.bin) · [PyEmuera](../../evidence/printdata-61-20261117/assets/BATCH021/public-01/raw.bin) |
| `SD_NO_CHOICES` | `P\r\nLAN_LOCAL_STRING` | `PLAN_LOCAL_STRING` | [入力](../../evidence/printdata-61-20261117/assets/BATCH022/native-01/inputs/ERB/MAIN.ERB) · [本家1](../../evidence/printdata-61-20261117/assets/BATCH022/native-01/raw.bin) · [本家2](../../evidence/printdata-61-20261117/assets/BATCH022/native-02/raw.bin) · [PyEmuera](../../evidence/printdata-61-20261117/assets/BATCH022/public-01/raw.bin) |
| `SD_DEFAULT` | `PLAN_LOCAL_ST\r\nRING` | `PLAN_LOCAL_STRING` | [入力](../../evidence/printdata-61-20261117/assets/BATCH026/native-01/inputs/ERB/MAIN.ERB) · [本家1](../../evidence/printdata-61-20261117/assets/BATCH026/native-01/raw.bin) · [本家2](../../evidence/printdata-61-20261117/assets/BATCH026/native-02/raw.bin) · [PyEmuera](../../evidence/printdata-61-20261117/assets/BATCH026/public-01/raw.bin) |
| `SD_INDEX` | `INDEXE\r\nD11` | `INDEXED11` | [入力](../../evidence/printdata-61-20261117/assets/BATCH027/native-01/inputs/ERB/MAIN.ERB) · [本家1](../../evidence/printdata-61-20261117/assets/BATCH027/native-01/raw.bin) · [本家2](../../evidence/printdata-61-20261117/assets/BATCH027/native-02/raw.bin) · [PyEmuera](../../evidence/printdata-61-20261117/assets/BATCH027/public-01/raw.bin) |

本家の実装とfixtureからは、最初の4条件で初期値を保持し、`SD_INDEX` では `INDEXED11` を書き込むと推論できます。本家の処理前の入力markerも、いずれの初期値が `PLAN_LOCAL_STRING` だったことを示します。この推論は、[基準配布物](../../vendor/emuera/README.ja.md)内の `Instraction.Child.cs`、`Process.ScriptProc.cs`、`ArgumentBuilder.cs` と各fixtureの処理経路に基づきます。実行EXEとソースを結ぶビルド記録は確認できていません。

ログだけからは、値の途中に入った改行と表示幅による折り返しを区別できません。本家の `PrintStringBuffer.cs` は表示幅で行を分け、`EmueraConsole.Print.cs` の `OutputLog` は表示行を書き出します。したがって表の本家部分は保存された文字と行境界を示し、改行を除去した値を直接測定したとは扱いません。PyEmueraでの値は別エンジンの実測で、本家の値の直接測定ではありません。原記録にある状態値は、この表示上の限界と併せて読んでください。
