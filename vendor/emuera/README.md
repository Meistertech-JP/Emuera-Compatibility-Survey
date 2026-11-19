# Emuera reference distribution

[日本語](README.ja.md)

`Emuera1824-v24-with-notices.zip` contains the retained `Emuera1824+v24.zip` and its accompanying Japanese and English notices in a single distribution unit. Read either notice before use. If distributing the retained ZIP, carry the notices with it; do not distribute the inner ZIP separately as a project asset.

| File | SHA-256 |
|---|---|
| Outer archive | `b0c2bd639868728e8b0b591c3da3d323a4537209300fb74d3829def4837cea85` |
| Retained inner ZIP | `fd0dd5b83ab3f929e69de0b9af739fa9bf785b6f510b30d11aaf44db35af182a` |
| `Emuera1824+v24.exe` inside the inner ZIP | `14cf28c137c6b76396c4d02fcb23ba6a31132301ce1fe0fcbab8c9f1c29d8964` |

Extract the outer archive, then extract the inner ZIP to a separate working directory. Python can extract the outer archive with `python -m zipfile -e Emuera1824-v24-with-notices.zip <destination>`. Hash the files again before invoking the [comparison harness](../../harness/README.md). Preserve the original archives; run tests against disposable copies.

The notices describe the evidence connecting the retained ZIP to the preserved `493` distribution. The original 7z and this inner ZIP are different containers. The content comparison does not establish identical archive bytes or the complete history by which the ZIP was created.

This distribution unit keeps the original ZIP unmodified and ships it together with the bilingual notices. The inner ZIP is never repacked or altered, and the provenance limits stated in the notices remain in force. See the [component license index](../../LICENSES/README.md) for the terms covering the rest of the project.
