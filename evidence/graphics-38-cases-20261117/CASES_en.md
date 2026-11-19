# Native observations for 38 historical graphics cases

[English entry](README.md) | [Japanese case index](CASES_ja.md) | [Machine-readable records](cases.json)

These are selected readbacks from the existing case records, for the specific inputs linked below. They summarize recorded fields and may combine raw lines or omit fields, so they are not verbatim quotations from the raw files. They are not an exhaustive API specification or proof of rendered screen pixels. `VALUE`, `RET`, `V`, `RESULT`, `R`, `EVAL`, `E`, `P00`, and other labels retain their recorded meanings and are not interchangeable; consult each fixture for the exact calls, setup, and sampled positions. The two original Native logs are distinct saved files; equal bytes do not establish that they are the same attempt. The case 230 method `fill_origin` value `EVAL=123` follows the existing parent correction of a physical line wrap in the original raw; the original raw is unchanged.

All 38 historical verdicts remain `unverified`. Natural exit of the historical Native runs was not observed. PyEmuera's historical setup or loading stopped before the selected target state in some cases; refer to the individual machine record for scope. Py raw and the full historical registry are not included, so this bundle cannot establish their contents independently. A Native value alone does not establish a cross-engine match. Pixel values below are reported reads at selected coordinates, not a visual or whole-image check.

## Case observations

### `GQUERY230_graphics-expression-created`

[Original fixture](cases/C01/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C01/original/inputs/emuera.config) · [Native raw 01](cases/C01/original/raw/native-01.bin) · [Native raw 02](cases/C01/original/raw/native-02.bin)

Selected Native readbacks: `OBS230 1 width_created VALUE=4 RESULT=701 EVAL=1`; `OBS230 2 height_created VALUE=3 RESULT=701 EVAL=1`; `OBS230 3 fill_origin VALUE=4279312947 RESULT=701 EVAL=123`; `OBS230 5 x_negative VALUE=-1 RESULT=701 EVAL=123`; `OBS230 6 x_equal_width VALUE=-1 RESULT=701 EVAL=123`.

### `GQUERY230_graphics-method-created`

[Original fixture](cases/C02/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C02/original/inputs/emuera.config) · [Native raw 01](cases/C02/original/raw/native-01.bin) · [Native raw 02](cases/C02/original/raw/native-02.bin)

Selected Native readbacks: `OBS230 1 width_created VALUE=4 RESULT=4 EVAL=1`; `OBS230 2 height_created VALUE=3 RESULT=3 EVAL=1`; `OBS230 3 fill_origin VALUE=4279312947 RESULT=4279312947 EVAL=123`; `OBS230 5 x_negative VALUE=-1 RESULT=-1 EVAL=123`; `OBS230 6 x_equal_width VALUE=-1 RESULT=-1 EVAL=123`.

### `GMUTATE231_gdispose-expr-positive`

[Original fixture](cases/C03/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C03/original/inputs/emuera.config) · [Native raw 01](cases/C03/original/raw/native-01.bin) · [Native raw 02](cases/C03/original/raw/native-02.bin)

Selected Native readbacks: `CREATE=1`; `DISPOSE=1`; `AFTER_DISPOSE_STATE=0,0,0`; `REPEAT=0`; `RECREATE=1`.

### `GMUTATE231_gdispose-method-positive`

[Original fixture](cases/C04/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C04/original/inputs/emuera.config) · [Native raw 01](cases/C04/original/raw/native-01.bin) · [Native raw 02](cases/C04/original/raw/native-02.bin)

Selected Native readbacks: `CREATE=1`; `DISPOSE=1`; `AFTER_DISPOSE_STATE=0,0,0`; `REPEAT=0`; `RECREATE=1`.

### `GMUTATE231_gclear-expr-positive`

[Original fixture](cases/C05/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C05/original/inputs/emuera.config) · [Native raw 01](cases/C05/original/raw/native-01.bin) · [Native raw 02](cases/C05/original/raw/native-02.bin)

Selected Native readbacks: `CLEAR_OPAQUE=1`; `OPAQUE_PIXELS=4279312947,4279312947,4279312947`; `CLEAR_TRANSPARENT=1`; `TRANSPARENT_PIXELS=0,0,0`.

### `GMUTATE231_gclear-method-positive`

[Original fixture](cases/C06/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C06/original/inputs/emuera.config) · [Native raw 01](cases/C06/original/raw/native-01.bin) · [Native raw 02](cases/C06/original/raw/native-02.bin)

Selected Native readbacks: `CLEAR_OPAQUE=1`; `OPAQUE_PIXELS=4279312947,4279312947,4279312947`; `CLEAR_TRANSPARENT=1`; `TRANSPARENT_PIXELS=0,0,0`.

### `GMUTATE231_gsetcolor-expr-positive`

[Original fixture](cases/C07/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C07/original/inputs/emuera.config) · [Native raw 01](cases/C07/original/raw/native-01.bin) · [Native raw 02](cases/C07/original/raw/native-02.bin)

Selected Native readbacks: `SET=1`; `SET_PIXELS=0,4279312947,0`; `X_NEG=0`; `X_WIDTH=0`; `Y_HEIGHT=0`.

### `GMUTATE231_gsetcolor-method-positive`

[Original fixture](cases/C08/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C08/original/inputs/emuera.config) · [Native raw 01](cases/C08/original/raw/native-01.bin) · [Native raw 02](cases/C08/original/raw/native-02.bin)

Selected Native readbacks: `SET=1`; `SET_PIXELS=0,4279312947,0`; `X_NEG=0`; `X_WIDTH=0`; `Y_HEIGHT=0`.

### `GMUTATE231_gclear-expr-missing-invalid-color`

[Original fixture](cases/C09/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C09/original/inputs/emuera.config) · [Native raw 01](cases/C09/original/raw/native-01.bin) · [Native raw 02](cases/C09/original/raw/native-02.bin)

The original Native raw records a line 4 GCLEAR diagnostic for an out-of-range `ColorARGB` value `0x100000000`. The old classification says this Native diagnostic was unobserved; the reason for this discrepancy is unknown. The original verdict remains `unverified`.

A **separate subsequent GUI run**, with fixture and config matching the original by SHA-256, recorded the same diagnostic: [fixture](cases/C09/followup/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C09/followup/inputs/emuera.config) · [Native raw](cases/C09/followup/raw/native.bin) · [screen crop](cases/C09/followup/crop.png). Matching bytes do not make it the same attempt. Natural exit and post-error state were not observed; no same-condition Py diagnostic comparison is established by this follow-up.

### `GMUTATE231_gclear-method-missing-invalid-color`

[Original fixture](cases/C10/original/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C10/original/inputs/emuera.config) · [Native raw 01](cases/C10/original/raw/native-01.bin) · [Native raw 02](cases/C10/original/raw/native-02.bin)

The original Native raw records a line 4 GCLEAR diagnostic for an out-of-range `ColorARGB` value `0x100000000`. The old classification says this Native diagnostic was unobserved; the reason for this discrepancy is unknown. The original verdict remains `unverified`.

A **separate subsequent GUI run**, with fixture and config matching the original by SHA-256, recorded the same diagnostic: [fixture](cases/C10/followup/inputs/ERB/GRAPHICS231.ERB) · [config](cases/C10/followup/inputs/emuera.config) · [Native raw](cases/C10/followup/raw/native.bin) · [screen crop](cases/C10/followup/crop.png). Matching bytes do not make it the same attempt. Natural exit and post-error state were not observed; no same-condition Py diagnostic comparison is established by this follow-up.

### `GRAPHICS232_gsave-expression-positive`

[Original fixture](cases/C11/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C11/original/inputs/emuera.config) · [Native raw 01](cases/C11/original/raw/native-01.bin) · [Native raw 02](cases/C11/original/raw/native-02.bin) · [image input](cases/C11/original/inputs/resources/PIX232.BMP)

Selected Native readbacks: `SAVE RET=1, R=701, RS=sentinel232, EVAL=12, EXISTS=1, W=4, H=3, P00=4281640448, P32=4283891853`; `NEGATIVE_SLOT RET=0, R=701, RS=sentinel232, EVAL=12, EXISTS=1, W=4, H=3, P00=4281640448, P32=4283891853`; `OVER_SLOT RET=0, R=701, RS=sentinel232, EVAL=12, EXISTS=1, W=4, H=3, P00=4281640448, P32=4283891853`.

### `GRAPHICS232_gload-expression-positive`

[Original fixture](cases/C12/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C12/original/inputs/emuera.config) · [Native raw 01](cases/C12/original/raw/native-01.bin) · [Native raw 02](cases/C12/original/raw/native-02.bin) · [image input](cases/C12/original/inputs/resources/PIX232.BMP)

Selected Native readbacks: `LOAD RET=1, R=701, RS=sentinel232, EVAL=12, EXISTS=1, W=4, H=3, P00=4281640448, P32=4283891853`; `EXISTING RET=0, R=701, RS=sentinel232, EVAL=1, EXISTS=1, W=4, H=3, P00=4281640448, P32=4283891853`; `NEGATIVE_SLOT RET=0, R=701, RS=sentinel232, EVAL=12, EXISTS=0, W=0, H=0, P00=-1, P32=-1`; `OVER_SLOT RET=0, R=701, RS=sentinel232, EVAL=12, EXISTS=0, W=0, H=0, P00=-1, P32=-1`.

### `GRAPHICS233_gfillrectangle-expr-positive`

[Original fixture](cases/C13/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C13/original/inputs/emuera.config) · [Native raw 01](cases/C13/original/raw/native-01.bin) · [Native raw 02](cases/C13/original/raw/native-02.bin)

Selected Native readbacks: `OBS_FILL_DEFAULT=1|701|"sentinel233"|12345`; `OBS_PIX_DEFAULT=0,4278190080,4278190080,0`; `OBS_FILL=1|701|"sentinel233"|12345`; `OBS_PIX_FILL=0,4279312947,4279312947,0`; `OBS_CLIP_NEG_X=1|701|"sentinel233"|0`.

### `GRAPHICS233_gfillrectangle-expr-zero-width`

[Original fixture](cases/C14/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C14/original/inputs/emuera.config) · [Native raw 01](cases/C14/original/raw/native-01.bin) · [Native raw 02](cases/C14/original/raw/native-02.bin)

Native reports a `GFILLRECTANGLE` error at line 21 for the fourth argument value `0`; the later state is not established by this diagnostic.

### `GRAPHICS233_gfillrectangle-method-positive`

[Original fixture](cases/C15/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C15/original/inputs/emuera.config) · [Native raw 01](cases/C15/original/raw/native-01.bin) · [Native raw 02](cases/C15/original/raw/native-02.bin)

Selected Native readbacks: `OBS_FILL_DEFAULT=1|1|"sentinel233"|12345`; `OBS_PIX_DEFAULT=0,4278190080,4278190080,0`; `OBS_FILL=1|1|"sentinel233"|12345`; `OBS_PIX_FILL=0,4279312947,4279312947,0`; `OBS_CLIP_NEG_X=1|1|"sentinel233"|0`.

### `GRAPHICS233_gfillrectangle-method-zero-width`

[Original fixture](cases/C16/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C16/original/inputs/emuera.config) · [Native raw 01](cases/C16/original/raw/native-01.bin) · [Native raw 02](cases/C16/original/raw/native-02.bin)

Native reports a `GFILLRECTANGLE` error at line 21 for the fourth argument value `0`; the later state is not established by this diagnostic.

### `GRAPHICS233_gsetbrush-expr-positive`

[Original fixture](cases/C17/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C17/original/inputs/emuera.config) · [Native raw 01](cases/C17/original/raw/native-01.bin) · [Native raw 02](cases/C17/original/raw/native-02.bin)

Selected Native readbacks: `OBS_SET_BRUSH=1|701|"sentinel233"|12`; `OBS_PIX_AFTER_SET=0,0,0,0`; `OBS_PIX_FILL=0,4279312947,4279312947,0`; `OBS_REPLACE_BRUSH=1|701|"sentinel233"|12`; `OBS_PIX_REPLACED=4294967295,4279312947,4279312947,0`.

### `GRAPHICS233_gsetbrush-method-positive`

[Original fixture](cases/C18/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C18/original/inputs/emuera.config) · [Native raw 01](cases/C18/original/raw/native-01.bin) · [Native raw 02](cases/C18/original/raw/native-02.bin)

Selected Native readbacks: `OBS_SET_BRUSH=1|1|"sentinel233"|12`; `OBS_PIX_AFTER_SET=0,0,0,0`; `OBS_PIX_FILL=0,4279312947,4279312947,0`; `OBS_REPLACE_BRUSH=1|1|"sentinel233"|12`; `OBS_PIX_REPLACED=4294967295,4279312947,4279312947,0`.

### `GRAPHICS233_gsetfont-expr-positive`

[Original fixture](cases/C19/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C19/original/inputs/emuera.config) · [Native raw 01](cases/C19/original/raw/native-01.bin) · [Native raw 02](cases/C19/original/raw/native-02.bin)

Selected Native readbacks: `OBS_SET_FONT=1|701|"sentinel233"|12`; `OBS_PIX_AFTER_FONT=0,0,0,0`; `OBS_SIZE_ZERO=0|701|"sentinel233"|0`; `OBS_SIZE_NEG=0|701|"sentinel233"|0`.

### `GRAPHICS233_gsetfont-method-positive`

[Original fixture](cases/C20/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C20/original/inputs/emuera.config) · [Native raw 01](cases/C20/original/raw/native-01.bin) · [Native raw 02](cases/C20/original/raw/native-02.bin)

Selected Native readbacks: `OBS_SET_FONT=1|1|"sentinel233"|12`; `OBS_PIX_AFTER_FONT=0,0,0,0`; `OBS_SIZE_ZERO=0|0|"sentinel233"|0`; `OBS_SIZE_NEG=0|0|"sentinel233"|0`.

### `GRAPHICS233_gsetpen-expr-positive`

[Original fixture](cases/C21/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C21/original/inputs/emuera.config) · [Native raw 01](cases/C21/original/raw/native-01.bin) · [Native raw 02](cases/C21/original/raw/native-02.bin)

Native reports an unexpected `System.IndexOutOfRangeException` at line 21; later state is not established.

### `GRAPHICS233_gsetpen-method-positive`

[Original fixture](cases/C22/original/inputs/ERB/GRAPHICS233.ERB) · [config](cases/C22/original/inputs/emuera.config) · [Native raw 01](cases/C22/original/raw/native-01.bin) · [Native raw 02](cases/C22/original/raw/native-02.bin)

Native reports an unexpected `System.IndexOutOfRangeException` at line 21; later state is not established.

### `GRAPHICS234_lifecycle-expression-positive`

[Original fixture](cases/C23/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C23/original/inputs/emuera.config) · [Native raw 01](cases/C23/original/raw/native-01.bin) · [Native raw 02](cases/C23/original/raw/native-02.bin)

Selected Native readbacks: `1 SPRITECREATE create_full V=1 R=701 E=12`; `3 SPRITEWIDTH spritewidth V=4 R=701 E=1`; `4 SPRITEHEIGHT spriteheight V=3 R=701 E=1`; `6 SPRITEDISPOSE dispose V=1 R=701 E=1`; `7 SPRITECREATED after_dispose V=0 R=701 E=1`; `20 SPRITEANIMEADDFRAME delay_zero V=0 R=701 E=123456789`; `23 SPRITECREATED post_frames_spritecreated V=1 R=701 E=1`.

### `GRAPHICS234_lifecycle-method-positive`

[Original fixture](cases/C24/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C24/original/inputs/emuera.config) · [Native raw 01](cases/C24/original/raw/native-01.bin) · [Native raw 02](cases/C24/original/raw/native-02.bin)

Selected Native readbacks: `1 SPRITECREATE create_full V=1 R=1 E=12`; `3 SPRITEWIDTH spritewidth V=4 R=4 E=1`; `4 SPRITEHEIGHT spriteheight V=3 R=3 E=1`; `6 SPRITEDISPOSE dispose V=1 R=1 E=1`; `7 SPRITECREATED after_dispose V=0 R=0 E=1`; `20 SPRITEANIMEADDFRAME delay_zero V=0 R=0 E=123456789`; `23 SPRITECREATED post_frames_spritecreated V=1 R=1 E=1`.

### `GRAPHICS235_gdrawg-expression-missing-source`

[Original fixture](cases/C25/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C25/original/inputs/emuera.config) · [Native raw 01](cases/C25/original/raw/native-01.bin) · [Native raw 02](cases/C25/original/raw/native-02.bin)

Selected Native readbacks: `RET=0`; `RESULT=701`; `EVAL=12`; `P00=4278190080`; `P32=4278190080`.

### `GRAPHICS235_gdrawg-expression-positive`

[Original fixture](cases/C26/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C26/original/inputs/emuera.config) · [Native raw 01](cases/C26/original/raw/native-01.bin) · [Native raw 02](cases/C26/original/raw/native-02.bin)

Selected Native readbacks: `RET=1`; `RESULT=701`; `EVAL=12`; `P00=4279312947`; `P32=4279312947`.

### `GRAPHICS235_gdrawg-method-missing-source`

[Original fixture](cases/C27/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C27/original/inputs/emuera.config) · [Native raw 01](cases/C27/original/raw/native-01.bin) · [Native raw 02](cases/C27/original/raw/native-02.bin)

Selected Native readbacks: `RET=0`; `RESULT=0`; `EVAL=12`; `P00=4278190080`; `P32=4278190080`.

### `GRAPHICS235_gdrawg-method-positive`

[Original fixture](cases/C28/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C28/original/inputs/emuera.config) · [Native raw 01](cases/C28/original/raw/native-01.bin) · [Native raw 02](cases/C28/original/raw/native-02.bin)

Selected Native readbacks: `RET=1`; `RESULT=1`; `EVAL=12`; `P00=4279312947`; `P32=4279312947`.

### `GRAPHICS235_gdrawsprite-expression-missing-source`

[Original fixture](cases/C29/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C29/original/inputs/emuera.config) · [Native raw 01](cases/C29/original/raw/native-01.bin) · [Native raw 02](cases/C29/original/raw/native-02.bin)

Selected Native readbacks: `RET=0`; `RESULT=701`; `EVAL=12`; `P00=4278190080`; `P32=4278190080`.

### `GRAPHICS235_gdrawsprite-expression-positive`

[Original fixture](cases/C30/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C30/original/inputs/emuera.config) · [Native raw 01](cases/C30/original/raw/native-01.bin) · [Native raw 02](cases/C30/original/raw/native-02.bin)

Selected Native readbacks: `RET=1`; `RESULT=701`; `EVAL=124`; `P00=4279312947`; `P32=4279312947`.

### `GRAPHICS235_gdrawsprite-method-missing-source`

[Original fixture](cases/C31/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C31/original/inputs/emuera.config) · [Native raw 01](cases/C31/original/raw/native-01.bin) · [Native raw 02](cases/C31/original/raw/native-02.bin)

Selected Native readbacks: `RET=0`; `RESULT=0`; `EVAL=12`; `P00=4278190080`; `P32=4278190080`.

### `GRAPHICS235_gdrawsprite-method-positive`

[Original fixture](cases/C32/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C32/original/inputs/emuera.config) · [Native raw 01](cases/C32/original/raw/native-01.bin) · [Native raw 02](cases/C32/original/raw/native-02.bin)

Selected Native readbacks: `RET=1`; `RESULT=1`; `EVAL=124`; `P00=4279312947`; `P32=4279312947`.

### `GRAPHICS235_gdrawgwithmask-expression-missing-source`

[Original fixture](cases/C33/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C33/original/inputs/emuera.config) · [Native raw 01](cases/C33/original/raw/native-01.bin) · [Native raw 02](cases/C33/original/raw/native-02.bin)

Selected Native readbacks: `RET=0`; `RESULT=701`; `EVAL=12`; `P00=4278190080`; `P32=4278190080`.

### `GRAPHICS235_gdrawgwithmask-expression-positive`

[Original fixture](cases/C34/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C34/original/inputs/emuera.config) · [Native raw 01](cases/C34/original/raw/native-01.bin) · [Native raw 02](cases/C34/original/raw/native-02.bin)

Selected Native readbacks: `RET=1`; `RESULT=701`; `EVAL=1234`; `P00=4279312947`; `P32=4279312947`.

### `GRAPHICS235_gdrawgwithmask-method-missing-source`

[Original fixture](cases/C35/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C35/original/inputs/emuera.config) · [Native raw 01](cases/C35/original/raw/native-01.bin) · [Native raw 02](cases/C35/original/raw/native-02.bin)

Selected Native readbacks: `RET=0`; `RESULT=0`; `EVAL=12`; `P00=4278190080`; `P32=4278190080`.

### `GRAPHICS235_gdrawgwithmask-method-positive`

[Original fixture](cases/C36/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C36/original/inputs/emuera.config) · [Native raw 01](cases/C36/original/raw/native-01.bin) · [Native raw 02](cases/C36/original/raw/native-02.bin)

Selected Native readbacks: `RET=1`; `RESULT=1`; `EVAL=1234`; `P00=4279312947`; `P32=4279312947`.

### `UIQUERY236_lifecycle-expr`

[Original fixture](cases/C37/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C37/original/inputs/emuera.config) · [Native raw 01](cases/C37/original/raw/native-01.bin) · [Native raw 02](cases/C37/original/raw/native-02.bin)

Selected Native readbacks: `STEP236 CBGSETG V=1 R=701`; `STEP236 CBGSETSPRITE V=1 R=701`; `STEP236 CBGSETBMAPG V=1 R=701`; `STEP236 CBGSETBUTTONSPRITE V=1 R=701`; `OBS236 V=1 R=701 A=0`.

### `UIQUERY236_lifecycle-method`

[Original fixture](cases/C38/original/inputs/ERB/SEARCHBOUND01.ERB) · [config](cases/C38/original/inputs/emuera.config) · [Native raw 01](cases/C38/original/raw/native-01.bin) · [Native raw 02](cases/C38/original/raw/native-02.bin)

Selected Native readbacks: `STEP236 CBGSETG V=1 R=1`; `STEP236 CBGSETSPRITE V=1 R=1`; `STEP236 CBGSETBMAPG V=1 R=1`; `STEP236 CBGSETBUTTONSPRITE V=1 R=1`; `OBS236 V=1 R=1 A=0`.

## Boundaries

The two subsequent GCLEAR runs are separate from the historical runs even where log bytes match. Their crops were taken after screen downscaling and are not original-resolution pixel evidence. The follow-up records report owned-process cleanup; natural exit and post-error values were not observed. No new PyEmuera run or cross-engine verdict is claimed.

Rights, privacy and distribution terms for the included material remain unresolved; inclusion here is not approval to publish.
