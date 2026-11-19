# Resuming after PRINTVKW and PRINTVDW

[日本語](README.ja.md) | [Machine-readable observations](observations.json)

Each command was given the numeric argument `42` on Emuera 1.824 +v24 and PyEmuera 3.0.0. Before an empty Enter, the Native screen showed `42` without the following marker; after Enter, it showed `AFTER` and the recorded state. Both engines recorded `A=0`, `RESULT=701`, and `RESULTS=SENTINEL`, and their respective history logs matched byte for byte.

| Command | Input | Native before | Native after | Saved histories |
|---|---|---|---|---|
| PRINTVKW | [ERB](PRINTVKW/fixture.erb) | [screen](PRINTVKW/before.bmp) | [screen](PRINTVKW/after.bmp) | [Native](PRINTVKW/native-history.bin) / [Py](PRINTVKW/py-history.bin) |
| PRINTVDW | [ERB](PRINTVDW/fixture.erb) | [screen](PRINTVDW/before.bmp) | [screen](PRINTVDW/after.bmp) | [Native](PRINTVDW/native-history.bin) / [Py](PRINTVDW/py-history.bin) |

Native received Enter in its input control on a private desktop. PyEmuera received an empty line on standard input at startup. Native natural exit was not observed; the owned process was terminated after observation. Both PyEmuera exit codes were zero. Input timing, pixel equivalence, and other arguments were not tested. Histories use UTF-16LE with a BOM. Configuration, PyEmuera stdout/stderr, and the machine-readable record are included.

`manifest.json` records SHA-256 and sizes. The terms for publishing survey fixtures, images and documentation remain under review.
