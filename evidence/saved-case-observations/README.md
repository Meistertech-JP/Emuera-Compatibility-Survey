# Saved case observations

[日本語](README.ja.md)

The [observation dataset](observations.json) contains excerpts for 1,780 main scenarios from saved comparison records and execution logs. The [browser](../../docs/survey-browser.html) includes the 1,075 results already available, for a total of 2,855 of 2,898 main scenarios. For the remaining 43 cases, an early test attempt yielded no usable observation.

The excerpts are associated with a frozen case ID using a matching comparison row, case-specific marker, or the recorded test condition. Relevant log lines are stored in UTF-8 JSON. Where available, excerpts identify the source by SHA-256 and point to the applicable JSON record. The observed engines and conditions vary by case.

The `registry_sha256` field identifies the frozen register. Viewing an excerpt, verifying the original artifact, and running the original condition are separate checks. The [legacy locator](../legacy226-source-locator-20261118/README.md) reports which source artifacts are available.
