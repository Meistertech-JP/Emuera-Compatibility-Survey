# Scope, interpretation and environment

[日本語](../ja/method.md) | [Project overview](../../README.md)

The reference implementation is Emuera 1.824 +v24. The comparison target in this dataset is PyEmuera 3.0.0. A typed target distinguishes a command, an expression function and a command form even when names coincide. Static registration, source analysis, a visible screen and a runtime comparison are different kinds of evidence.

The recorded target decisions describe selected finite requirements. Native Emuera observations are the reference for future implementations; the PyEmuera comparison supports compatibility work and regression checks. Recorded differences and target diagnostics remain results. Cases with unavailable observations or unresolved execution conditions remain marked as such; success in another case does not establish their outcome. Full input-space grammar behavior and full compatibility remain outside the demonstrated scope.

The historical project used AI-assisted implementation and review with native and comparison-engine observations. An AI review performed by a different agent is not an independent review by an external human. A hash identifies retained bytes; it does not itself demonstrate semantic equality or authenticity.

The harness supports a small pure-expression plan and fixed cases for argument errors, stopping position, side effects and GUI input. Native GUI execution requires Windows. The environment record identifies the separately obtained PyEmuera 3.0.0 binary and the retained Emuera executable by SHA-256. The reference archive is distributed unmodified together with its [reference distribution guide](../../vendor/emuera/README.md); see the [component license index](../../LICENSES/README.md) for the applicable terms. See the [harness guide](../../harness/README.md), [environment record](../../manifests/environment.json) and [reference archive notices](../../vendor/emuera/README.md).

From the candidate root, `python -B results/verify.py` checks the neutral dataset, `python -B results/test_verify.py` checks the verifier with selected controls, and `python -B tools/query.py SET` looks up a target. The four representative cases have selected evidence and case-specific limits. The candidate has yet to establish independent reproduction of the complete historical survey. See the [representative differences](../../differences/representative-20261116/README.en.md), [offline checks](offline-validation.md) and [legacy reference guide](results.md#legacy-references).

`python -B tools/verify_environment.py` checks the local notice bundle, inner ZIP and configuration identity. Supply `--native <path>` and `--pyz <path>` to check extracted engine binaries as well. These checks do not execute either engine.
