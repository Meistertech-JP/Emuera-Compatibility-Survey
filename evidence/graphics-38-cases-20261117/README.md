# 38 historical graphics cases and later GCLEAR observations

[日本語](README.ja.md) | [English case observations](CASES_en.md) | [Japanese case index](CASES_ja.md) | [Machine-readable records](cases.json)

The English case index gives a concise Native observation for each of the 38 original cases, with the original fixture, config and two Native raw files. The index also links the separate follow-up GCLEAR GUI records for two cases. Inputs and outputs reflect only the saved conditions; reported pixel values do not establish rendered pixels or an entire image.

All historical verdicts remain `unverified`. Some historical PyEmuera runs stopped at setup or load before the selected target; details differ by case. Py raw and the full original registry are not included. Historical registry text in the machine records is a neutral projection, not a full verbatim copy. The follow-up runs establish no new Py comparison or cross-engine verdict. Historical Native natural exit was not observed.

For the two GCLEAR invalid-color cases, historical classification says the Native diagnostic was unobserved, but the frozen original raw already contains it. The discrepancy's cause is unknown. The separate follow-up GUI runs used fixture and config with matching SHA-256 and also recorded the diagnostic. Their crops came from downscaled screenshots. Follow-up natural exit and post-error state were not observed.

Rights, privacy and distribution terms remain unresolved. Engines and Py comparison evidence are not included.

From this directory, verify the file set using Python 3.10 or later:

```text
python -I -B file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

The manifest verifies bytes and completeness, not authenticity, permission to publish or semantic correctness. Obtain its SHA-256 through a separately trusted channel.
