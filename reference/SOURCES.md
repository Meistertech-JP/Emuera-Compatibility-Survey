# Sources and adoption limits

[日本語](SOURCES_ja.md) / [Machine-readable registry](sources.json)

Explanations and examples are independently written. This registry identifies references and limits; it does not redistribute downloaded prose or relicense third-party documentation/code as MIT. Checked November 18, 2026; acquisition times use UTC.

## Shared IDs

- SRC-NATIVE-V24: the Emuera1824+v24 source in the original ZIP nested in the vendor archive. Cite both archives, member, SHA-256 hashes and one-based lines. Entry paths are relative to src1824/Emuera/. Source inspection is distinct from native runtime observation. Vendor notices and individual third-party terms remain applicable.
- SRC-SURVEY-3: existing saved finite native/PyEmuera 3.0 comparisons. Adopt only the recorded target, fixture, version, mode, outcome and evidence locator. This task did not rerun native tests; finite matches do not establish complete compatibility.
- SRC-NATIVE-README: bundled main 1.824/private v24 readmes for version declarations, software credits and change-history leads. Software credits do not establish authorship of all Wiki pages.

## Original OSDN captures

Actual Wayback bodies were retrieved. These resolved UTC capture timestamps are not engine versions or authoring dates.

| ID | Actual capture UTC | Retrieved title |
|---|---|---|
| SRC-OSDN-FRONTPAGE | 20230303163321 | Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXCOM | 20230303163405 | excom - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXMETH | 20230303163405 | exmeth - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXOP | 20230303163446 | exop - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXFUNC | 20230303163353 | exfunc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-USERVARS | 20230303163405 | UserVars - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-RESOURCES | 20230303163405 | resources - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXHTML | 20230303163436 | exhtml - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXTENDED | 20230303163441 | extended - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |
| SRC-OSDN-EXETC | 20230303163405 | exetc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN |

Live OSDN FrontPage failed with a TLS error. The exvar replay returned HTTP 503, so no successful body or capture timestamp is claimed. CDX listings and actual page-body retrieval are separate records.

## Migration, preservation and rights

The EMEE Changelog explicitly records migration of OSDN Emuera documentation into its Wiki. Inherited Emuera/ pages, reorganized Reference/ pages and later EM+EE extensions remain distinct. Migration does not establish MinorShift's personal authorship; unknown individual authors/editors are null.

The EMEE homepage actually displays CC BY-NC 4.0 and a license link. This is recorded as a site-level declaration, not proof of authority to relicense inherited material. Downloaded prose/examples and literal translations are not included in the public candidate. Theme/icon licenses do not license documentation text.

Five original/migrated page pairs were compared: operators, function/preprocessor declarations, user variables, resources and general syntax. Their rendered text differs, including formatting and edits; they are not asserted to be byte-identical. Full original revision histories, the precise revisions used for migration and per-section authorship remain unverified.

The Era Wiki index, excom, exmeth and ERB/CSV pages were retrieved. The initial excom transport failure remains recorded alongside a single successful retry after the index became reachable. Translated/edited preserved pages do not automatically inherit official authority or verified licensing.

## Version and evidence boundaries

The old PRINT-family explanation includes an explicit ver1.736 condition, while excom also contains later annotations. It is not a single-version specification. The eramaker ERB/CSV pages warn that current Emuera differs; historical restrictions cannot be transferred directly to v24.

Commands, expression functions and functions invoked as commands remain distinct typed targets. A shared name does not establish identical arguments, result destinations, returns or errors. Private indices provide discovery leads, never automatically adopted claims. SET is an internal assignment identifier, not a directly callable instruction.

Sources were located for commands, expression functions, operators, assignment, declarations, control, PRINT, INPUT, SAVE/LOAD, CSV/ERB and GUI/sprites. This confirms material exists in each area, not complete documentation of all 694 targets. Native GUI/sprite features retain their environment conditions and are not omitted merely because a CLI does not expose them.

## Registry

Original/archive URLs, sections, versions, checked times, outcomes and adoption limits are recorded in sources.json. Downloaded bodies, headers, complete indices and typed-target mappings remain in private owner audit records.

| ID | Classification | Title | Wayback UTC | License display/status |
|---|---|---|---|---|
| SRC-NATIVE-V24 | SOURCE_CONFIRMED | Emuera1824+v24 bundled C# source | — | individual / unverified |
| SRC-SURVEY-3 | SOURCE_CONFIRMED | PyEmuera 3.0 saved finite survey and native/PyEmuera observations | — | MIT |
| SRC-NATIVE-README | DOCUMENTED_ORIGINAL | Bundled Emuera 1.824 and private Emuera1824+v24 readmes | — | individual / unverified |
| SRC-OSDN-FRONTPAGE | DOCUMENTED_ORIGINAL | Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163321 | individual / unverified |
| SRC-EMEE-EMUERA | MIRROR | Index - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-ERAGAMES-EXCOM | MIRROR | Emuera/excom - Era Wiki | — | individual / unverified |
| SRC-OSDN-EXCOM | DOCUMENTED_ORIGINAL | excom - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXMETH | DOCUMENTED_ORIGINAL | exmeth - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXOP | DOCUMENTED_ORIGINAL | exop - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163446 | individual / unverified |
| SRC-OSDN-EXFUNC | DOCUMENTED_ORIGINAL | exfunc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163353 | individual / unverified |
| SRC-OSDN-USERVARS | DOCUMENTED_ORIGINAL | UserVars - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-RESOURCES | DOCUMENTED_ORIGINAL | resources - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXHTML | DOCUMENTED_ORIGINAL | exhtml - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163436 | individual / unverified |
| SRC-EMEE-CHANGELOG-INDEX | DERIVATIVE | 変更ログ - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-REFERENCE-INDEX | DERIVATIVE | Index - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-OPERAND | MIRROR | 演算 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-EXPRESSION | MIRROR | Emueraで追加された記法 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-USER-DEFINED-VARIABLES | MIRROR | ユーザー定義の変数 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-FUNCTION | MIRROR | 関数・プリプロセッサ - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-IN-EXPRESSION-FUNCTION | MIRROR | 式中で使える関数 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-EMUERA-RESOURCES | MIRROR | リソースファイル - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-ERAMAKER-ERB-FORMAT | DERIVATIVE | eramakerのERB書式 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-ERAMAKER-CSV-FORMAT | DERIVATIVE | eramakerのCSV書式 - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-INDEX | DERIVATIVE | Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
| SRC-EMEE-REPO-README-MD | DERIVATIVE | README.md | — | individual / unverified |
| SRC-ERAGAMES-INDEX | MIRROR | Emuera - Era Wiki | — | individual / unverified |
| SRC-OSDN-EXTENDED | DOCUMENTED_ORIGINAL | extended - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163441 | individual / unverified |
| SRC-OSDN-EXETC | DOCUMENTED_ORIGINAL | exetc - Emuera - emulator of eramaker Wiki - Emuera - emulator of eramaker - OSDN | 20230303163405 | individual / unverified |
| SRC-OSDN-EXVAR | DOCUMENTED_ORIGINAL | Internet Archive: Temporarily Offline | — | individual / unverified |
| SRC-ERAGAMES-EXMETH | MIRROR | Emuera/exmeth - Era Wiki | — | individual / unverified |
| SRC-ERAGAMES-ERAMAERB | MIRROR | Emuera/eramaerb - Era Wiki | — | individual / unverified |
| SRC-ERAGAMES-ERAMACSV | MIRROR | Emuera/eramacsv - Era Wiki | — | individual / unverified |
| SRC-EMEE-REFERENCE-IF | DERIVATIVE | (S)IF - Emuera.EM+EE ドキュメント | — | CC-BY-NC-4.0 |
