# Static API availability references: 75 typed targets

[日本語](README.ja.md)

This directory contains a privacy-limited projection of 75 typed target records: 34 expression forms and 41 command forms, representing 41 distinct names. Each row binds a typed key to its Native function-method registration record, the independently read static PyEmuera function and command specifications, the current target ledger, shared adapter, parent matrix and typed readback. Seven command-form targets have a same-name function entry; function and command availability must not be merged.

The `native_registration` fields identify a same-name entry in the Native `FunctionMethodCreator.methodList` dictionary and its implementation signature. For a command-form typed key, this dictionary entry alone does not establish registration or routing of the command syntax itself. Command-form routing and observations require separate evidence; the recorded case roles and rejection phases below are source-reported references.

The parent matrix contains 167 target–case references. The typed readbacks select 110 of those references; 57 are not selected. The same case ID may appear under different typed targets and roles, so these references are retained separately; a shared ID alone does not prove a shared physical execution. The `reason` field records only the parent matrix selection context; `reason_not_specified` does not invent a reason. Source-reported rejection phases are transcribed from readbacks and are not independently checked against raw output in this projection.

**No fixture, runtime log, receipt, config, GUI image or engine is included or re-executed.** Every row is marked `not_reverified_raw_not_included`: parent outcome `documented_difference` is an attributed source record, not an assertion that all 75 cases were rerun, completed, or matched. The projection does not establish public runtime success, value/pixel/lifecycle equivalence, or historical authenticity. Source hashes and pointers do not allow readers without the withheld originals to verify those originals. The extracted identifiers, positions and API-name presence are facts from the specified source snapshots, not a complete implementation or all-version availability claim.

`records/targets.json` contains typed targets, source IDs and JSON pointers, static registration identifiers, function/command spec presence, and case roles. Source IDs and SHA-256 values appear in `manifest.json`; private filesystem paths and raw receipts are not published. The existing evidence for selected SPRITEMOVE/SPRITESETPOS cases is a separate artifact and must not be substituted for other targets.

With Python 3.9 or later, first verify `verify.py` using a trusted independent tool and a verifier SHA obtained through a trusted channel; obtain the manifest SHA independently as well. Then run:

```sh
python3 -I -B verify.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
python3 -I -B test_negative.py --manifest-sha256 <TRUSTED_MANIFEST_SHA256> --verifier-sha256 <TRUSTED_VERIFIER_SHA256>
```

The included verifier SHA-256 is `0d70bee333f3c61b03c1b3b76d4cc76482e994770271976a457e219ace9941a7`. Python 3.9 is the minimum due to `Path.is_relative_to`; this is not a claim that every later Python environment was tested. The verifier checks the file set, both pins, checksum, target and case-role populations and basic types, not the contents of withheld source documents. The supplied checksum is not a signature.

Native source attribution: [Emuera license](LICENSES/Emuera1824-v24-license-original.txt) and [Emuera notice](vendor/emuera/NOTICE.en.md). PyEmuera source attribution: [MIT license](LICENSES/PyEmuera-3.0.0-LICENSE.txt) and [third-party notices](LICENSES/PyEmuera-3.0.0-THIRD-PARTY-NOTICES.md). The unmodified Emuera notice was written to accompany a separate original source ZIP distribution and describes that distribution and its preservation provenance; that ZIP is not included here. It does not imply that this directory contains the ZIP. Rights holders and reuse terms for survey-created records, documents and verification code remain to be determined separately; PyEmuera MIT is not a blanket license for survey material.
