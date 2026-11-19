# Representative differences: retained finite observations

[日本語](README.ja.md) | [Machine-readable catalog](catalog.json) | [Evidence manifest](../../evidence/representative-20261116/manifest.json)

These records describe retained observations from the survey. The actual ERB fixtures and raw output or display capture are included. The complete historical configuration, execution harness, and engine distributions are not included; independent reruns have not been performed and **reproducibility is not established**. Native natural exit and unprinted state after errors remain unknown unless observed.

## Bare `RAND`: `COLON_NORMAL_COMPAT_RAND_YES`

Under `CompatiRAND:YES`, the [fixture](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/fixture/ERB/MAIN.ERB) evaluates bare `RAND` before `RAND:0`. The [CSV inputs](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/fixture/csv/) and an [extracted setting](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/fixture/config-observed.json) are included; the extracted setting is not the full configuration.

Both [Native run 1](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/native-01-emuera.log) and [run 2](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/native-02-emuera.log) report `OBS_RAND_BARE=0`, `OBS_RAND_ZERO=0`, `AFTER`, and `DONE`. The public build's [stdout](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/public-stdout.bin) reaches `BEFORE`; its [stderr](../../evidence/representative-20261116/COLON_NORMAL_COMPAT_RAND_YES/raw/public-stderr.bin) reports `E_ARGUMENT: RAND:n requires n > 0` at line 22. The accepted finite difference is Native returning zero for bare `RAND` while PyEmuera rejects it.

The public run stops at the earlier bare `RAND` and does not reach the later `RAND:0`. Its behavior for zero is established by the separate case below.

## `RAND:0`: `COLON_RAND_ZERO_COMPAT_YES`

A [separate fixture](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/fixture/ERB/MAIN.ERB) evaluates `RAND:0` under `CompatiRAND:YES`; its [CSV inputs](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/fixture/csv/) are also included. Both [Native run 1](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/native-01-emuera.log) and [run 2](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/native-02-emuera.log) report `OBS_RAND_ZERO=0`, `AFTER`, and `DONE`. Public [stdout](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/public-stdout.bin) reaches `BEFORE`, while [stderr](../../evidence/representative-20261116/COLON_RAND_ZERO_COMPAT_YES/raw/public-stderr.bin) reports the same `E_ARGUMENT` at line 22. This is an independently observed zero case, not a continuation of the prior public run.

## `P38`: stopping at an unclosed IF

The [fixture](../../evidence/representative-20261116/P38/fixture/ERB/P38.ERB) omits both the condition and `ENDIF` from the `IF` at line 3. The Native [display capture](../../evidence/representative-20261116/P38/raw/native-display.bmp) shows loading warnings, `BEFORE`, and a line-3 error about the missing `ENDIF`. This is a screen capture, not a Native raw text log.

Public [stdout](../../evidence/representative-20261116/P38/raw/public-stdout.txt) contains `Now Loading...` only; [stderr](../../evidence/representative-20261116/P38/raw/public-stderr.txt) reports `ERB/P38.ERB:3: E_SYNTAX: Unclosed IF`, and stdout does not contain `BEFORE`. The mismatch concerns the earlier visible output and stopping point. A load-time warning may detect the problem before Native stops upon reaching the marked IF; detection and stopping are distinct.

The historical pilot inventory pins public stdout, but does not list an independently pinned stderr. The included stderr matches the retained file and current freeze ledger; this does not establish an earlier independently recorded hash. P38B, which supplies an IF condition, is a separate case.

## `GMF_LEX_LONE_EQUALS`: malformed single `=`

The [fixture](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/fixture/ERB/MAIN.ERB) contains `A=1=2` on line 4. Both [Native run 1](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/native-01-actual-final-log.bin) and [run 2](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/native-02-actual-final-log.bin) reach `GM_BEFORE`, stop at line 4, and report an unexpected assignment operator `=`, suggesting `==` for comparison.

Public [stdout](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/public-stdout.bin) also reaches `GM_BEFORE`; [stderr](../../evidence/representative-20261116/GMF_LEX_LONE_EQUALS/raw/public-stderr.bin) reports `E_SYNTAX: Unexpected expression character '=' at column 2: 1=2`. Neither side prints `GM_AFTER`. The accepted difference concerns the primary diagnostic; it does not claim full diagnostic envelope equality or post-error variable state. The source-based proposed guard was not directly instrumented.

## Evidence handling

Native logs use UTF-16; see the manifest for the encoding of each public raw stream. The included original logs and fixtures are byte-identical copies, with SHA-256 values in the manifest. Selected receipt fields were transformed into derived JSON with paths and identifying details omitted. The original-to-derived SHA and transformation records are kept privately. The P38 image is the byte-identical crop retained during the survey; the uncropped full-screen bytes were not retained.

The included partial inputs do not establish reproducibility without the complete configuration, dependencies and verified execution procedure. Engine binaries and third-party source code are not included. A final rights and privacy review remains necessary before publication.
