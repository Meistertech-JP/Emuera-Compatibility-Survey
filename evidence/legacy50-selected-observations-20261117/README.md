# Selected Native and PyEmuera observations: 27 typed targets

[日本語](README.ja.md)

This bundle presents selected observations from two existing comparisons. The typed target is the pair of `kind` and `name`; the same name in expression and command form counts as two targets. The observations are limited to the listed conditions. They are not a general compatibility verdict.

- **GETTER251 — 14 targets, 23 cases:** expression functions `GETDEFCOLOR`, `GETDEFBGCOLOR`, `GETFOCUSCOLOR`, `GETSTYLE`, `GETFONT`, `CURRENTALIGN`; and command forms of those six plus `ISSKIP` and `PRINTCLENGTH`. The expression and command fixtures each have two Native runs and one PyEmuera run. Six cases involving configured default colors are `different_scoped`; the other 17 are `matched_scoped`.
- **OPNORMAL273 — 13 operators, 4 cases:** `+`, `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `^^`, `!&`, `&`, `|`, `^`. Four fixtures each connect two retained Native runs with one later PyEmuera run. The 71 selected markers match across the three runs for each fixture; the original case verdicts are `matched_scoped`.

The same run ID in multiple rows identifies **one shared run**, not separate executions. The operator runs include the observed short-circuit conditions `0&&ZZ_BAD()` → `VALUE=0 BADCOUNT=0` and `0!&ZZ_BAD()` → `VALUE=1 BADCOUNT=0` in both Native runs and the PyEmuera run. In these conditions the right-hand helper was not called; its return value or an error was not observed. Other guards, post-fatal state, diagnostic equivalence and broader inputs are outside this selection.

PyEmuera exited with code 0 in these runs. Native reached the recorded completion markers but natural exit and an exit code were not observed; the owned process was stopped after observation. Reaching a marker is not proof of natural exit. The PyEmuera operator runs also recorded a nonfatal OUTPUTLOG warning, preserved in the JSON. GETFONT used explicit font-name restoration; no-argument SETFONT is a separate unresolved case. Rendering, pixels, all configurations and arbitrary display histories were not established.

The earlier acceptance sheets for these typed targets remain unidentified: these later observations do not restore or replace them. The raw logs, fixtures and receipts are **not included**. Raw hashes and line numbers identify referenced records but a reader of this bundle cannot check those records against the projection without obtaining them separately. Source pointers similarly refer to source documents absent from the bundle. Rights and privacy clearance for the source material and this projection have not been established. The manifest records file consistency, not authenticity or permission to publish.

## Reading the JSON

Open [selected-observations.json](selected-observations.json). In `getter.cases`, each case contains its `target`, `condition`, original verdict and three `observations`. A getter `state.value` is a string; `condition.value_type` distinguishes integer and string values. `RESULT0`, `RESULT1`, and `RESULTS` are the recorded result slots. `preceding_setups_in_shared_run` records earlier changes in that same fixture.

In `operator_normal.cases`, `marker_observations` associates each selected marker with its own target, condition statements, referenced helpers, and three observed lines. `VALUE` is the expression result; `COUNT` is the instrumented helper-call count; `ORDER` records the helper-call sequence; `BADCOUNT` is the deliberately failing helper's call count. The top-level `runs` table describes the shared runs and their termination limits. `comparison_pointer` and `register_pointer` locate rows in separate source documents, not inside this JSON.

For example, from the extracted bundle directory, the first command prints the configured default-foreground case and all three observations. The second prints the `&&` short-circuit marker and its condition:

```sh
python -c "import json; d=json.load(open('selected-observations.json',encoding='utf-8')); c=next(x for x in d['getter']['cases'] if x['case_id']=='GETTER251_expression_0'); print(c['target'],c['condition']); [print(o['run_id'],o['state']) for o in c['observations']]"
python -c "import json; d=json.load(open('selected-observations.json',encoding='utf-8')); c=next(x for x in d['operator_normal']['cases'] if x['case_id']=='OPNORMAL273_E140'); m=next(x for x in c['marker_observations'] if x['marker']=='LOG20'); print(m)"
```

## Check this file set

Extract all four files into an otherwise empty directory and run this standard-library check from that directory with Python 3.8 or later. It checks the exact four names and the size and SHA-256 of the three files listed in the manifest. The manifest cannot authenticate itself; compare its SHA-256 with a separately trusted value if authenticity matters. This short check is for this flat bundle, not a general archive or security validator.

```sh
python -c "import json,hashlib,pathlib,sys; p=pathlib.Path('.'); names={'README.md','README.ja.md','selected-observations.json','file-set-manifest.json'}; check=lambda ok: None if ok else sys.exit('FAILED'); check({x.name for x in p.iterdir()}==names and all(not (p/n).is_symlink() for n in names)); m=json.loads((p/'file-set-manifest.json').read_text(encoding='utf-8')); f=m['files']; check(m['schema']=='selected-file-set.v1' and m['roots']==['bundle'] and m['manifest_location']=={'root':'bundle','path':'file-set-manifest.json'} and len(f)==3 and {e['path'] for e in f}==names-{'file-set-manifest.json'}); [check(e['root']=='bundle' and (p/e['path']).stat().st_size==e['size'] and hashlib.sha256((p/e['path']).read_bytes()).hexdigest()==e['sha256']) for e in f]; print('OK: 4 names, 3 file sizes and SHA-256 digests')"
```
