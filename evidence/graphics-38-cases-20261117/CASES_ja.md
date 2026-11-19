# 38ケース：元の記録と後続観測

[入口](README.ja.md) | [Machine-readable index](cases.json)

元判定はいずれも `unverified`。本家rawの値は保存した条件のみ。後続2試行は元の試行と別に保持します。

| case | 元fixture / 原raw | 後続本家GUI観測 |
|---|---|---|
| `GQUERY230_graphics-expression-created` | [ERB](cases/C01/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C01/original/raw/native-01.bin)・[raw 2](cases/C01/original/raw/native-02.bin) | ― |
| `GQUERY230_graphics-method-created` | [ERB](cases/C02/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C02/original/raw/native-01.bin)・[raw 2](cases/C02/original/raw/native-02.bin) | ― |
| `GMUTATE231_gdispose-expr-positive` | [ERB](cases/C03/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C03/original/raw/native-01.bin)・[raw 2](cases/C03/original/raw/native-02.bin) | ― |
| `GMUTATE231_gdispose-method-positive` | [ERB](cases/C04/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C04/original/raw/native-01.bin)・[raw 2](cases/C04/original/raw/native-02.bin) | ― |
| `GMUTATE231_gclear-expr-positive` | [ERB](cases/C05/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C05/original/raw/native-01.bin)・[raw 2](cases/C05/original/raw/native-02.bin) | ― |
| `GMUTATE231_gclear-method-positive` | [ERB](cases/C06/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C06/original/raw/native-01.bin)・[raw 2](cases/C06/original/raw/native-02.bin) | ― |
| `GMUTATE231_gsetcolor-expr-positive` | [ERB](cases/C07/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C07/original/raw/native-01.bin)・[raw 2](cases/C07/original/raw/native-02.bin) | ― |
| `GMUTATE231_gsetcolor-method-positive` | [ERB](cases/C08/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C08/original/raw/native-01.bin)・[raw 2](cases/C08/original/raw/native-02.bin) | ― |
| `GMUTATE231_gclear-expr-missing-invalid-color` | [ERB](cases/C09/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C09/original/raw/native-01.bin)・[raw 2](cases/C09/original/raw/native-02.bin) | [raw](cases/C09/followup/raw/native.bin)・[crop](cases/C09/followup/crop.png)：4行目 ColorARGB範囲外 |
| `GMUTATE231_gclear-method-missing-invalid-color` | [ERB](cases/C10/original/inputs/ERB/GRAPHICS231.ERB)・[raw 1](cases/C10/original/raw/native-01.bin)・[raw 2](cases/C10/original/raw/native-02.bin) | [raw](cases/C10/followup/raw/native.bin)・[crop](cases/C10/followup/crop.png)：4行目 ColorARGB範囲外 |
| `GRAPHICS232_gsave-expression-positive` | [ERB](cases/C11/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C11/original/raw/native-01.bin)・[raw 2](cases/C11/original/raw/native-02.bin) | ― |
| `GRAPHICS232_gload-expression-positive` | [ERB](cases/C12/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C12/original/raw/native-01.bin)・[raw 2](cases/C12/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gfillrectangle-expr-positive` | [ERB](cases/C13/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C13/original/raw/native-01.bin)・[raw 2](cases/C13/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gfillrectangle-expr-zero-width` | [ERB](cases/C14/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C14/original/raw/native-01.bin)・[raw 2](cases/C14/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gfillrectangle-method-positive` | [ERB](cases/C15/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C15/original/raw/native-01.bin)・[raw 2](cases/C15/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gfillrectangle-method-zero-width` | [ERB](cases/C16/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C16/original/raw/native-01.bin)・[raw 2](cases/C16/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gsetbrush-expr-positive` | [ERB](cases/C17/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C17/original/raw/native-01.bin)・[raw 2](cases/C17/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gsetbrush-method-positive` | [ERB](cases/C18/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C18/original/raw/native-01.bin)・[raw 2](cases/C18/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gsetfont-expr-positive` | [ERB](cases/C19/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C19/original/raw/native-01.bin)・[raw 2](cases/C19/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gsetfont-method-positive` | [ERB](cases/C20/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C20/original/raw/native-01.bin)・[raw 2](cases/C20/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gsetpen-expr-positive` | [ERB](cases/C21/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C21/original/raw/native-01.bin)・[raw 2](cases/C21/original/raw/native-02.bin) | ― |
| `GRAPHICS233_gsetpen-method-positive` | [ERB](cases/C22/original/inputs/ERB/GRAPHICS233.ERB)・[raw 1](cases/C22/original/raw/native-01.bin)・[raw 2](cases/C22/original/raw/native-02.bin) | ― |
| `GRAPHICS234_lifecycle-expression-positive` | [ERB](cases/C23/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C23/original/raw/native-01.bin)・[raw 2](cases/C23/original/raw/native-02.bin) | ― |
| `GRAPHICS234_lifecycle-method-positive` | [ERB](cases/C24/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C24/original/raw/native-01.bin)・[raw 2](cases/C24/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawg-expression-missing-source` | [ERB](cases/C25/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C25/original/raw/native-01.bin)・[raw 2](cases/C25/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawg-expression-positive` | [ERB](cases/C26/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C26/original/raw/native-01.bin)・[raw 2](cases/C26/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawg-method-missing-source` | [ERB](cases/C27/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C27/original/raw/native-01.bin)・[raw 2](cases/C27/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawg-method-positive` | [ERB](cases/C28/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C28/original/raw/native-01.bin)・[raw 2](cases/C28/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawsprite-expression-missing-source` | [ERB](cases/C29/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C29/original/raw/native-01.bin)・[raw 2](cases/C29/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawsprite-expression-positive` | [ERB](cases/C30/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C30/original/raw/native-01.bin)・[raw 2](cases/C30/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawsprite-method-missing-source` | [ERB](cases/C31/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C31/original/raw/native-01.bin)・[raw 2](cases/C31/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawsprite-method-positive` | [ERB](cases/C32/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C32/original/raw/native-01.bin)・[raw 2](cases/C32/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawgwithmask-expression-missing-source` | [ERB](cases/C33/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C33/original/raw/native-01.bin)・[raw 2](cases/C33/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawgwithmask-expression-positive` | [ERB](cases/C34/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C34/original/raw/native-01.bin)・[raw 2](cases/C34/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawgwithmask-method-missing-source` | [ERB](cases/C35/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C35/original/raw/native-01.bin)・[raw 2](cases/C35/original/raw/native-02.bin) | ― |
| `GRAPHICS235_gdrawgwithmask-method-positive` | [ERB](cases/C36/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C36/original/raw/native-01.bin)・[raw 2](cases/C36/original/raw/native-02.bin) | ― |
| `UIQUERY236_lifecycle-expr` | [ERB](cases/C37/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C37/original/raw/native-01.bin)・[raw 2](cases/C37/original/raw/native-02.bin) | ― |
| `UIQUERY236_lifecycle-method` | [ERB](cases/C38/original/inputs/ERB/SEARCHBOUND01.ERB)・[raw 1](cases/C38/original/raw/native-01.bin)・[raw 2](cases/C38/original/raw/native-02.bin) | ― |

## GCLEAR無効色：元記録とrawの食い違い

元の分類／比較文は2ケースのNative診断を未観測と記録します。一方、同じ元ケースの凍結SHAに一致するNative 01／02原rawには、どちらも4行目の `ColorARGB` 値 `0x100000000` に対する診断があります。原記録も原rawも変更しておらず、食い違いの発生原因は不明です。

後続の式・命令それぞれ1試行は、対応する元fixture・設定と同じSHAで、同じ診断を出力し、下記の画面cropにも表示しています。後続rawと元rawは同じbytesですが、**別試行を同一試行とは扱いません**。

自然終了・エラー後の変数値は未観測。後続でPy側の同条件診断比較を実施した記録ではなく、両エンジンの診断一致・不一致も新たに判定しません。

case230のmethod `fill_origin` は、元子比較の `EVAL=1` と物理折返し後の `23` を既存親訂正に従って当該箇所のみ結合した `EVAL=123` を記録。
