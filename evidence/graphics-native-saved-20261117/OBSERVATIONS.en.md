# Graphics APIs: selected Emuera observations

These examples come from 13 saved fixtures run with Emuera 1.824 +v24. Each result applies to the specified input and state; it is not a complete survey of the APIs. Follow the ERB and Native log links to inspect the inputs and saved output. Native logs use UTF-16LE with a BOM.

The values obtained with `GGETCOLOR` and `SPRITEGETCOLOR` are API return values for selected points inside an image. They do not establish the pixels shown in a GUI or the contents of every pixel. Native natural exit was not observed; a `DONE` marker in a log does not establish an exit code. Results from one fixture should not be generalized to other inputs or execution environments.

## Images and selected points

- **Dimensions and color — Q.** After `GCREATE(230,4,3)` and a clear to `4279312947` (`0xFF112233`), `GWIDTH` returned `4`, `GHEIGHT` returned `3`, and `GGETCOLOR` returned `4279312947` at `(0,0)` and `(3,2)`. Coordinates `(-1,0)`, `(4,0)`, and `(0,3)` returned `-1`. Negative y was not tested in this fixture. [ERB][Q-E] · [Native log][Q-R]
- **Sprite color — QSP.** For a resource-registered 4×3 sprite, `SPRITEGETCOLOR` returned `0` at `(0,0)` and `(3,2)`, and `-1` at `(-1,0)`, `(4,0)`, and `(0,3)`. The return value `0` is not evidence that the input pixels are black. See the [sprite registration][QSP-CSV] and [pixel-encoding note][PIXEL]. [ERB][QSP-E] · [Native log][QSP-R]
- **Image file — FILE.** Loading `PIX232.BMP` into image ID 232 returned `1`; the image existed and measured 4×3. `GGETCOLOR` returned `4281640448` at `(0,0)` and `4283891853` at `(3,2)`. A second load into the existing ID returned `0`, with the same dimensions and selected values; its recorded evaluation marker was `1`. [ERB][FILE-E] · [Native log][FILE-R] · [BMP][FILE-BMP]
- **Saved image — LOAD.** After loading the BMP and saving it in slot 232, `GLOAD(233,232)` returned `1`, producing a 4×3 image with those same two point values. Loading into the existing ID returned `0`; slots `-1` and `2147483648` also returned `0` in the tested conditions. The output PNG and the separate full-pixel proof are not included, so this bundle cannot independently recheck a full-pixel round trip. [ERB][LOAD-E] · [Native log][LOAD-R]
- **Set a pixel — COLOR.** On a 3×2 image, setting `(1,1)` to `4279312947` and then `4294967295` returned `1` each time. In the selected order `(0,0)`, `(1,1)`, `(2,1)`, the values were `0,4279312947,0` and then `0,4294967295,0`. Attempts at `(-1,0)`, `(3,0)`, and `(0,2)` returned `0`; the same three selected values remained unchanged. [ERB][COLOR-E] · [Native log][COLOR-R]
- **Draw a sprite — DS.** A sprite created from a 4×3 source image was drawn to a 4×3 destination. `GDRAWSPRITE` returned `1`; `GGETCOLOR` returned `4279312947` at destination points `(0,0)` and `(3,2)`. [ERB][DS-E] · [Native log][DS-R]

## Diagnostics in the saved Native logs

- **Zero-width rectangle — FILL0.** On an existing 4×3 image, `GFILLRECTANGLE` with width `0` produced a diagnostic at ERB line 21 identifying the fourth argument, `0`, as invalid. Post-error state was not observed. [ERB][FILL0-E] · [Native log][FILL0-R]
- **Pen with two arguments — PEN2.** The call on an existing image produced `System.IndexOutOfRangeException` at ERB line 21. Post-error pen state was not observed. [ERB][PEN2-E] · [Native log][PEN2-R]
- **Pen with three arguments — PEN3.** `GSETPEN(233,4279312947,1)` produced an argument-count diagnostic at ERB line 9. This is a separate fixture from PEN2. [ERB][PEN3-E] · [Native log][PEN3-R]
- **Missing animation — ANERR.** `SPRITEANIMEADDFRAME` with the nonempty unregistered name `MISS234` produced `System.NullReferenceException` at ERB line 9. A subsequent return value or state was not observed. [ERB][ANERR-E] · [Native log][ANERR-R]
- **Animation timer boundary — TIMERERR.** `SETANIMETIMER(32768)` produced a diagnostic at ERB line 9 identifying its first argument as invalid. [ERB][TIMERERR-E] · [Native log][TIMERERR-R]

## Sprite position

The following two fixtures register the sprite at `(10,-20)`. Each applies `(3,-4)`, `(3,-4)`, then `(-16,28)`; each call returned `1`. The coordinates are reported by sprite position APIs, not observed GUI locations. [Resource registration][MOVE-CSV]

- **Move — MOVE.** The recorded positions were `(13,-24)` → `(16,-28)` → `(0,0)`. [ERB][MOVE-E] · [Native log][MOVE-R]
- **Set position — SETPOS.** The recorded positions were `(3,-4)` → `(3,-4)` → `(-16,28)`. [ERB][SETPOS-E] · [Native log][SETPOS-R]

The [Japanese observations][JA] and [input and raw reference list][REFS] describe further saved cases. Rights, publication terms, and privacy review for these materials remain unresolved.

[Q-E]: assets/Q/inputs/ERB/SEARCHBOUND01.ERB
[Q-R]: assets/Q/raw/native-01.bin
[QSP-E]: assets/QSP/inputs/ERB/SEARCHBOUND01.ERB
[QSP-R]: assets/QSP/raw/native-01.bin
[QSP-CSV]: assets/QSP/inputs/resources/SPRITES230.csv
[PIXEL]: support/pixel-encoding.json
[FILE-E]: assets/FILE/inputs/ERB/SEARCHBOUND01.ERB
[FILE-R]: assets/FILE/raw/native-01.bin
[FILE-BMP]: assets/FILE/inputs/resources/PIX232.BMP
[LOAD-E]: assets/LOAD/inputs/ERB/SEARCHBOUND01.ERB
[LOAD-R]: assets/LOAD/raw/native-01.bin
[COLOR-E]: assets/COLOR/inputs/ERB/GRAPHICS231.ERB
[COLOR-R]: assets/COLOR/raw/native-01.bin
[DS-E]: assets/DS/inputs/ERB/SEARCHBOUND01.ERB
[DS-R]: assets/DS/raw/native-01.bin
[FILL0-E]: assets/FILL0/inputs/ERB/GRAPHICS233.ERB
[FILL0-R]: assets/FILL0/raw/native-01.bin
[PEN2-E]: assets/PEN2/inputs/ERB/GRAPHICS233.ERB
[PEN2-R]: assets/PEN2/raw/native-01.bin
[PEN3-E]: assets/PEN3/inputs/ERB/GRAPHICS233.ERB
[PEN3-R]: assets/PEN3/raw/native-01.bin
[ANERR-E]: assets/ANERR/inputs/ERB/SEARCHBOUND01.ERB
[ANERR-R]: assets/ANERR/raw/native-01.bin
[TIMERERR-E]: assets/TIMERERR/inputs/ERB/SEARCHBOUND01.ERB
[TIMERERR-R]: assets/TIMERERR/raw/native-01.bin
[MOVE-E]: assets/MOVE/inputs/ERB/SEARCHBOUND01.ERB
[MOVE-R]: assets/MOVE/raw/native-01.bin
[MOVE-CSV]: assets/MOVE/inputs/resources/SPRITES221.csv
[SETPOS-E]: assets/SETPOS/inputs/ERB/SEARCHBOUND01.ERB
[SETPOS-R]: assets/SETPOS/raw/native-01.bin
[JA]: OBSERVATIONS_ja.md
[REFS]: REFERENCES_ja.md
