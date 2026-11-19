# Verification requirements index (provisional candidate)

This proposed index attributes 3,359 verification requirements for 694 typed targets to a frozen source. It is not an approved release. Words such as `review` preserve source conditions; they do not represent completed results or instructions to perform new runs. Existing observations mentioned in source wording remain attributed to that source, not reproduced or proven by this index.

Each `requirements.jsonl` row has a typed target, original text SHA-256, recorded case relationships and text. `verbatim` preserves source wording; `neutralized` makes a limited editorial change. The original hash is computed over the UTF-8 text; it does not independently establish authenticity, rights, or an observed result. The source and its original pointers are not included; `source_record_id` is a key for a separately held crosswalk.

The `existing_projection` in `targets.jsonl` refers to a separately maintained result. Its `pointer` is a JSON Pointer within the result pinned by SHA-256 in `index.json`, not an original source pointer. That result is not included in this requirements directory; it is in the results directory of the same candidate distribution unit. Some roles are labels derived by the index from the original ledger, case registry, and prior alias decisions; their semantics have not been independently reaudited. Cases and roles do not establish independent execution.

Technical case IDs in the text retain their original spelling. `case-id-crosswalk.json` maps only the 11 exact IDs recognized in reviewed text and present in the pinned result to case aliases. Ranges and abbreviated references have not been partially rewritten. A source shorthand for a case group is retained without asserting its exact membership. Historical labels and case references do not themselves establish publication of evidence or independent confirmation of observations.

Verify offline with the Python 3 standard library and pins obtained through an independently trusted channel. If the separately maintained result is available, its pinned SHA and case IDs can also be checked:

```text
python verify.py --manifest-sha256 <manifest SHA256> --verifier-sha256 <verify.py SHA256>
python verify.py --manifest-sha256 <manifest SHA256> --verifier-sha256 <verify.py SHA256> --survey <survey.json>
```

The manifest excludes itself; pins must be trusted separately. Mechanical content and privacy scans are not exhaustive guarantees. Copyright ownership and permission remain undetermined; content, rights, and privacy require separate review before distribution.
