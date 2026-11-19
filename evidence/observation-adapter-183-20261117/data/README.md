# 183-case finite observation projection

This finite-scope index preserves case roles, the recorded observations, verdicts and unobserved limits. Shared mode records are not independent executions per case. Source paths and case text referring to private working records are represented by local reference IDs.

`references.json` distinguishes included derivatives from references not included. In case records, original source-declared SHA fields refer to the original source, whereas the SHA in `references.json` identifies the included derivative. A receipt can differ from its source. `ref:R...` is an index identifier, not a file path or a claim that a withheld source is available.

The included bytes are selected Native log, public stdout, input fixtures/config and selected-field receipts; stderr files, original receipts and other source materials are not generally included; case records can include excerpts of stderr diagnostics. Actual execution, natural termination, target reach, or universal equivalence is not inferred. Native2 for ISNUMERIC_I64_OVERFLOW uses a different recovery receipt and is not represented as a standard mode.

Rights, ownership, confidentiality, licensing and final public distribution need separate approval. The case records may retain original narrative or diagnostic text. The manifest checks consistency relative to its pins; it does not authenticate origin. Source-to-projection mapping is kept separately in private.
