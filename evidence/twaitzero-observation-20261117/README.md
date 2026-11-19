# Recorded observation: TWAIT 0,1

[日本語](README.ja.md)

Case `TWAITZERO01` compares a single `TWAIT 0,1` condition in Emuera1824+v24 and PyEmuera 3.0.0. The recorded verdict is `different_scoped`.

The [ERB fixture](fixture/ERB/TWAITZERO01.ERB) prints `BEFORE_TWAIT_ZERO`, executes `TWAIT 0,1`, and prints `AFTER_TWAIT_ZERO` if execution continues. The probe set the isolated Native input control to `42` and posted Enter key-down and key-up messages. The PyEmuera run used `--debug --wait` and an [empty input tape](fixture/inputs.txt). The [configuration](fixture/emuera.config) is from the saved run.

The Native [cropped screen](raw/native-after-input-crop.png), recorded as captured after the probe's three-second wait following the Enter posts, showed `BEFORE_TWAIT_ZERO` but not `AFTER_TWAIT_ZERO`. The harness then performed a process termination procedure; natural termination and the exit code were not observed. The screen alone does not establish when the posted input was consumed or which internal TWAIT stage had been reached.

PyEmuera printed `BEFORE_TWAIT_ZERO` to [stdout](raw/pyemuera-stdout.bin) and stopped on line 3 with `E_UNSUPPORTED`. The [stderr](raw/pyemuera-stderr.bin) diagnostic says that nonpositive TWAIT with input disabled would wait forever. Its recorded exit code was 1.

This case does not cover negative time, flag 0, other positive durations, argument side effects, or the whole GUI. The Native image is a crop of the displayed text; by itself it does not prove when input was accepted or that the process exited. The original comparison and input-event receipt are not included in this bundle, so the included hashes alone cannot authenticate the historical environment or execution.

The recorded Native executable SHA-256 is `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964`; the PyEmuera 3.0.0 pyz SHA-256 is `8a7b3697b97155c4dc994c8349c6756bb0401000d3bbccd8e85ff046e3774b35`. Neither executable is included.

`manifest.json` records the size and SHA-256 of the included files. It checks file integrity; it does not authenticate the historical execution or the distributor.

The [original Emuera license](licenses/Emuera1824-v24-license-original.txt), [PyEmuera license](licenses/PyEmuera-3.0.0-LICENSE.txt), and [PyEmuera third-party notices](licenses/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md) concern the original engine distributions. They do not by themselves apply one set of terms to all screenshots, logs, and survey fixtures.
