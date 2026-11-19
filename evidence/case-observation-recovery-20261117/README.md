# Observation case set

This bundle contains records for 486 cases and 38 supplemental rows attached to existing cases. Of the 486 records, 95 have saved observation descriptions in the `recovered` field; that field is empty in the other 391. Other fields describe conditions and comparison scope. An empty field does not mean that the original survey made no observation. The supplements add no cases or runs. Two corrected stopped-state records are returned first in searches; the corresponding entries from the earlier 486-case snapshot remain alongside them as historical records.

Run the commands below from the bundle root (the directory containing this README, `query.py`, `verify_bundle.py`, and `manifest.json`).

```powershell
python -B query.py --case CASE_ID
python -B query.py --target 'kind:name'
python -B verify_bundle.py
python -B file_set_manifest.py verify --manifest manifest.json --root public=.
```

Typed-target searches require exact kind and name matches (case-insensitive); a bare name also matches exactly. `verify_bundle.py` checks counts, ID relationships, correction priority, and bundle query behavior. The last command checks the integrated manifest's file inventory and hashes.

The 486-observation JSONL is included as `observations.jsonl` in this bundle. The original source register, source receipts, and raw files are not included, and no retrieval route is provided here. The distributed files support consistency checks against the included manifest; a manifest or hash is not a signature or publisher authentication.

- [Japanese marker recovery guide](marker-recovery/README.ja.md)
- [English marker recovery guide](marker-recovery/README.en.md)
- [Integrated manifest](manifest.json)