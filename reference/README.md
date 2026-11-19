# Using the command reference

[日本語](README.ja.md) · [Open the reference](../docs/survey-browser.html) · [Glossary](glossary.html) · [Literature and sources](SOURCES.md)

For a clickable offline entry point, open [`index.html`](../index.html).

Extract the ZIP and open `docs/survey-browser.html` in a browser. No server or network connection is required. Search the 694 targets by name, explanation, or requirement. Exact names rank first. Expression functions and same-named command forms remain separate entries.

In addition to search, target kind, and verdict, a purpose-based genre filter narrows the list. Every one of the 694 targets has exactly one primary genre and, where useful, secondary genres. Primary genres always total 694; secondary genres provide duplicate membership so a target can be found from any of its genres and are included in each genre's count. The master data is `reference/genres.json` and `reference/target-genres.json`.

Saved captures have a “Pin image” action. A pinned image stays in an on-screen panel while you scroll the text, together with its case ID, record type, and role. Only one image is pinned at a time; pinning another image switches the panel, and unpinning returns the image to normal in-text display. Language switching preserves the pinned image and its case. On narrow screens the panel moves to the bottom without covering the text.

Use “Pin menu”, always visible in the upper-right corner, to keep the tab bar, search box, verdict, target-kind, genre, and count controls at the top of the screen while you scroll the list. One click toggles the pinned mode from any scroll position, so you never need to return to the top of the page first, and the same action restores normal scrolling. Normal mode is the default, the preference is stored in the browser, and language switching preserves the selected mode.

Open “Read usage, expected effects, comparisons, and evidence” on a card to read its function, syntax, arguments, independently derived examples and expected effects, recorded Native/PyEmuera comparison, requirements, and evidence, in that order. Exact-name searches open the matching entries. Related-target and case buttons provide navigation.

Japanese is the default. The language button switches explanation bodies and labels to English. In Japanese, a requirement has a plain-language explanation, a translation, and a separate disclosure for its original English and provenance attributes. Original logs, diagnostics, and source comments retain their original language.

Switching languages retains loaded list items and open disclosures. English syntax uses `syntax_en` where supplied; Japanese literals in examples are unchanged. The compatibility area points to differing conditions first and excerpts per-engine `done` fields and diagnostics only when those fields exist in saved records. It does not treat `done` as evidence of natural exit or infer state-array meanings or bug counts.

## What supports an explanation?

“Sources for this explanation” identifies the source, version, and relevant location. C# links open numbered views generated from the pinned upstream archive included here. SHA-256 values identify original member bytes before decoding or rendering. The archive and third-party notices remain available. External links are for source consultation; opening the reference does not fetch them automatically.

- `DOCUMENTED_ORIGINAL`: information in the original project's material or an actually retrieved archival replay. This does not necessarily establish each passage's author.
- `DOCUMENTED_MIRROR` / `MIRROR`: preserved or migrated documentation. Migration and original authorship are separate questions.
- `DOCUMENTED_DERIVATIVE` / `DERIVATIVE`: derivative documentation. Derivative-only features are not treated as native v24 features.
- `SOURCE_CONFIRMED`: an explanation checked against the pinned 1824+v24 implementation, not a claim that its example was newly executed.
- `NATIVE_OBSERVED` / `PYEMUERA_OBSERVED`: a result saved from an execution. Engine, inputs, settings, and conditions must be checked per record.
- `EXAMPLE_DERIVED`: an independently written example based on cited evidence. Its expected effect is separate from recorded observations.
- `UNCONFIRMED`: an explanation or condition that could not be established, with a reason stated per item.

The comparison badge preserves the original finite-scope verdict. It does not grade the example's expected effect, the completeness of the explanation, or compatibility for every input. A shared log may contain output from other cases. Native GUI functionality is distinguished from the scope of PyEmuera's CLI.

Requirement `CASE…` identifiers are aliases from the source records. The 11 aliases established by the existing public crosswalk link to public cases; other aliases remain visible with an explicit notice that no individual public mapping is available. Target-level related cases can be browsed separately, but are not assumed to map directly to each requirement.

Fourteen requirements carry a separate “Note on the historical requirement” where historical wording conflicts with the bundled source or overgeneralizes a shared rule. They concern TRY*LIST no-hit continuation, GOTO-list arguments, and compound-assignment fast paths. Notes are managed independently in `requirement-notes-input.json`; original wording, translations, and verdicts are not replaced by a newly claimed runtime result.

## Editing and regeneration

Python 3.10 or newer and the standard library are sufficient. Run these commands from the repository root. No external website or original development folder is read.

```sh
python -B tools/survey_browser/prepare_reference.py
python -B tools/survey_browser/build_survey_browser.py
python -B tools/survey_browser/prepare_reference.py --check
python -B tools/survey_browser/build_survey_browser.py --check
python -B -m unittest discover -s tests -p "test_reference*.py" -v
```

`entries-*.jsonl` are the independently authored entry inputs. `requirements-ja-*.jsonl` contain requirement translations and plain explanations. Preparation generates `entries.json`, `requirements_ja.jsonl`, `source-locations.json`, source views, and the glossary HTML. `genres.json` and `target-genres.json` are the master data for the genre filter; the build joins them with the reference and validates targets, genres, and secondary genres. Original requirement fields are checked against `evidence/694-target-trace-20261117/requirements/requirements.jsonl`; changes, omissions, or duplicate IDs stop the build.

`sources.json` indexes retrieval dates, archival URLs, versions, rights, and limitations. `glossary.json` stores bilingual terminology. Explanations are joined when generating the browser; `results/survey.json`, original requirements, observations, and verdicts are not edited.

The distribution manifest seals a completed file set. After editing or regeneration, do not claim agreement with the old manifest: audit the new publication set and create a new manifest.

## Rights and limitations

Explanations and examples are independently written using technical facts from source and literature. Cached third-party prose and literal translations of it are not distributed. MIT applies only to original material for which the project has permission; it does not relicense upstream source or third-party prose. See the [notices](../LICENSES/README.md).

Unresolved source versions, authorship, or migration identity are described in the [literature review](SOURCES.md). Finding a source, verifying saved bytes, establishing an example's validity, and independently reproducing every historical observation are separate checks.
