# Graphics APIs: saved Native observations

[日本語](README.ja.md) | [Selected observations in English](OBSERVATIONS.en.md) | [Detailed observations in Japanese](OBSERVATIONS_ja.md) | [Inputs and raw files](REFERENCES_ja.md)

This collection contains inputs and saved Native logs for 34 selected conditions. Results and diagnostics apply only to the specified cases. They do not establish GUI display, all pixels, natural exit, or general compatibility with PyEmuera. The detailed observation text is in Japanese. Each `inputs` directory includes its relevant resource and CSV files; Native logs are UTF-16 with a BOM. Engines are not included.

**Rights, publication terms, and privacy review remain unresolved.** A matching manifest is an integrity check, not publication permission or proof that an observation is correct.

From this directory, use Python 3.10 or later to check the file set, SHA-256 and sizes:

```text
python -I -B file_set_manifest.py verify --manifest manifest.json --root evidence=.
```

Independent authenticity requires the manifest SHA-256 from a separate trusted channel. The original complete PNG pixel proof is not included and cannot be independently rechecked from this bundle alone.
