# Merge guide: Track B research into the site, v2.8.3

28 September 2026. This guide is for whoever next merges UI or Finance work with the research files. **RH STATUS: OPEN.**

## What v2.8.3 is

- **Base.** v2.8.3 is Fork-A **v2.8.2** (the Finance and homepage trace) plus the Track B research pass.
- **Common ancestor.** Both traces descend from v2.8.0.
- **Files touched.** Every file this release touches is research content:
  - `area-51/sedaps-51/` and `area-51/twins-51/`;
  - `research/`, `citation/`;
  - the two `llms.txt` files, `sitemap.xml`, `area-51/research.json`, and `site-index.json` (one added record: the Line Game concept DOI);
  - three new top-level notes.
- **Files not touched.** No file under `finance/`, `assets/` or `functions/` changes, and neither does the homepage `index.html` or any other game.
- **Papers.** `papers/` is not in the archive, as in both inputs. The updated TN Postmaster v5.2 source edition ships beside it:
  - `TN_Postmaster_Volume_I_v5_2_SOURCE.zip`;
  - before: `a130320b3dd3056c0a9be13b63f1a4e305e300dfb076ccc4463ff0f224faf145` (v2.8.0);
  - after: `1eb080935f08589f0fe120826f29df2763a2def28cc406049509c64fbbc5e139`.
  - When you restore `papers/`, put this file at `papers/TN_Postmaster_Volume_I_v5_2_SOURCE.zip`.

## How to merge a later UI build with these files

1. **"take v2.8.3".** Copy the v2.8.3 file over yours, unless your build changed it after v2.8.2. In that case, re-apply your edit on top of the v2.8.3 file.
2. **"new file".** Copy it in.
3. **"merged".** Both traces edited these files. The v2.8.3 copy already contains both sets of edits, so take it. If your build changed one of them after v2.8.2, re-apply your edit to the v2.8.3 copy. In `area-51/sedaps-51/index.html`, keep your Finance asset links (`/assets/finance-mini-…`): they are the only UI lines in that file.
4. **"delete".** Remove it: it is build litter.
5. **Generated files.** Never hand-edit `area-51/twins-51/index.html` or `twins-data-v1.js`. After any change to the Twins builder or verifier, run:
   - `node area-51/twins-51/verify-twins-v1.cjs --write`
   - `node area-51/twins-51/build-twins-page-v1.cjs --write`
   - then both again without `--write`. Both must report a match.
6. **Checks.** Run the verifiers listed in `VALIDATION_v2_8_3.json`. The fast ones are:
   - `node area-51/sedaps-51/verify-sedaps-v0-4.cjs`
   - `python3 area-51/sedaps-51/independent/sedaps_independent.py`
   - `python3 research/project-51/formula51/f51_independent.py research/project-51/formula51/f51_band.json`
7. **Version.** Set `area-51/research.json` `site_version` to your release number. Add your own `RELEASE_NOTES`, `MANIFEST` and `VALIDATION` files. Keep the earlier ones as released, and never reuse a version number: there is exactly one v2.8.1 (Fork-A's).
8. **Packaging.** Exclude `__pycache__/` and `*.pyc`.

## Every file, with its SHA-256 (first 12 hex digits)

The full digests are in `MANIFEST_v2_8_3.json` (against v2.8.2). A dash means the file did not exist in that version.

| file | rule | v2.8.0 | v2.8.2 (base) | v2.8.3 |
|---|---|---|---|---|
| `area-51/research.json` | merged | `0f4f8b2f500c` | `298a99cdd817` | `ae4d48367819` |
| `area-51/sedaps-51/RESEARCH_UPDATE_v0_4.md` | merged | `96fbd12bf0cd` | `0e0c2789d23e` | `16638efec8a3` |
| `area-51/sedaps-51/index.html` | merged | `a1e15a90e595` | `ca50d15f47ed` | `b0c02a281741` |
| `area-51/sedaps-51/sedaps-v0-4.js` | merged | `4c09b4ec8303` | `81030df45f35` | `dfbf7c6ced5a` |
| `area-51/twins-51/build-twins-page-v1.cjs` | merged | `37509cc76c12` | `185c0eea4813` | `7bbec0f4f039` |
| `area-51/twins-51/calibration.html` | merged | `f58f6dd59e3a` | `62099a0f5e60` | `75c0ab65ea4c` |
| `area-51/twins-51/index.html` | merged | `72b2bc656569` | `635d565abadb` | `4993788e60be` |
| `area-51/twins-51/verify-twins-v1.cjs` | merged | `979f742e5f05` | `240d4c331e80` | `2e11d1e50bad` |
| `research/project-51/formula51/FORMULA51_BAND_AND_DEDUCTION.md` | merged | `1d862b7ed2fa` | `15efad2450c0` | `c157f47b4b49` |
| `area-51/llms.txt` | take v2.8.3 | `a3486996fd9c` | `a3486996fd9c` | `58c0ae705d88` |
| `area-51/sedaps-51/README.md` | take v2.8.3 | `6a583b9e2a11` | `6a583b9e2a11` | `492581a07a47` |
| `area-51/sedaps-51/sedaps-lemma-v0-4.js` | take v2.8.3 | `35ed0bba9618` | `35ed0bba9618` | `79d1d0796bc4` |
| `area-51/twins-51/twins-data-v1.js` | take v2.8.3 | `2a7d34815e4e` | `2a7d34815e4e` | `0eac2c83bbaf` |
| `citation/catalog.json` | take v2.8.3 | `97e321ae4324` | `97e321ae4324` | `000678504f02` |
| `llms.txt` | take v2.8.3 | `911e66b19a22` | `911e66b19a22` | `3b6715586961` |
| `research/line-game/index.html` | take v2.8.3 | `dade3ed42932` | `dade3ed42932` | `b991937d9ec8` |
| `research/postmaster/index.html` | take v2.8.3 | `56ed101816c2` | `56ed101816c2` | `35f93619e3a2` |
| `research/project-51/index.html` | take v2.8.3 | `6e80130c914a` | `6e80130c914a` | `8239e00e9efa` |
| `site-index.json` | take v2.8.3 | `1cc49c52a070` | `1cc49c52a070` | `0712fd954242` |
| `sitemap.xml` | take v2.8.3 | `45abfeac5f89` | `45abfeac5f89` | `c3a28455ced1` |
| `RELEASE_NOTES_v2_8_3.md` | new file | — | — | `0653be91ec21` |
| `VALIDATION_v2_8_3.json` | new file | — | — | `588702d049cf` |
| `ZENODO_RELEASE_PLAN_v2_8_3.md` | new file | — | — | `26468a36f0cc` |
| `area-51/sedaps-51/HISTORY_COUNTS_v0_4_1.json` | new file | — | — | `45ef257c0308` |
| `area-51/sedaps-51/RESEARCH_UPDATE_v0_4_1.md` | new file | — | — | `062824279cd2` |
| `area-51/sedaps-51/VERIFY_v0_4_1.json` | new file | — | — | `14f64fe2b6c9` |
| `area-51/sedaps-51/count-histories-v0-4-1.cjs` | new file | — | — | `a22ab741a44e` |
| `area-51/sedaps-51/independent/CENSUS_RECEIPT.json` | new file | — | — | `8005b301126b` |
| `area-51/sedaps-51/independent/LIVE3_LOOPS_RECEIPT.json` | new file | — | — | `0bfe5efbd806` |
| `area-51/sedaps-51/independent/README.md` | new file | — | — | `3a7fff2e23df` |
| `area-51/sedaps-51/independent/census2.c` | new file | — | — | `0bdaaccce8da` |
| `area-51/sedaps-51/independent/census_alt.c` | new file | — | — | `67554fb25438` |
| `area-51/sedaps-51/independent/census_deals.c` | new file | — | — | `c2903cb222e8` |
| `area-51/sedaps-51/independent/live3_loops.c` | new file | — | — | `786088d0daf4` |
| `area-51/sedaps-51/independent/live3_packet.c` | new file | — | — | `0d70ff7a0b90` |
| `area-51/sedaps-51/independent/sedaps_independent.py` | new file | — | — | `f7d34f2b01d6` |
| `area-51/sedaps-51/independent/sedaps_independent_receipt.json` | new file | — | — | `46d72544a865` |
| `area-51/sedaps-51/independent/war_period_sigma.py` | new file | — | — | `56838aa057fa` |
| `area-51/sedaps-51/past10-certificates-v0-4-1.json` | new file | — | — | `97a76858be9a` |
| `area-51/sedaps-51/verify-past10-v0-4-1.cjs` | new file | — | — | `78d63c0522c9` |
| `area-51/twins-51/evidence/dh_twin_highprec.py` | new file | — | — | `b9227cfd4169` |
| `area-51/twins-51/evidence/dh_twin_highprec_receipt.json` | new file | — | — | `7fe78c04670e` |
| `research/line-game/The_Line_Game_Surprise_Is_Not_Meaning_v7_5.pdf` | new file | — | — | `4bef214c475b` |
| `research/project-51/Project_51_v0_4.pdf` | new file | — | — | `becd348f5cdd` |
| `research/project-51/Telescope_51_v0_7.pdf` | new file | — | — | `3a13181d422a` |
| `research/project-51/formula51/Formula_51_Concise_Method_2026-09-26.pdf` | new file | — | — | `ed97b5716a14` |
| `research/project-51/formula51/f51_independent.py` | new file | — | — | `864bca30942a` |
| `research/project-51/formula51/f51_independent_receipt.json` | new file | — | — | `3e778469fd76` |
| `research/project-51/formula51/__pycache__/derive51.cpython-312.pyc` | delete | — | `1adb7bf9edcd` | — |

## The nine files both traces edited

| file | kept from Fork-A (v2.8.1/v2.8.2) | added by Track B |
|---|---|---|
| `area-51/research.json` | — | SEDAPS entry → v0.4.1; `site_version` → 2.8.3 (neither side's value) |
| `area-51/sedaps-51/index.html` | Finance asset links; "Apply 17-card start + turn 85"; "occurs at turn 84" | v0.4.1 note, links, DOI placeholder moved to v0.4.1 |
| `area-51/sedaps-51/sedaps-v0-4.js` | "At the known turn 85"; "start and turn count" status lines | turns 24/27/30/33; label "Not at turn 84"; audit string |
| `area-51/sedaps-51/RESEARCH_UPDATE_v0_4.md` | "known elapsed turn count 85" sentence | table qualifiers; War theorem; lemma scope |
| `area-51/twins-51/build-twins-page-v1.cjs` | "detected negative"; "earlier sampled tests"; verifier-scope note | Gamma factor; 60/100-digit rechecks; War period; ledger rows; constant footnote |
| `area-51/twins-51/index.html` | (generated) | rebuilt from the merged builder and data |
| `area-51/twins-51/verify-twins-v1.cjs` | header: "imported claims, not recomputed certificates" | Löwner fields: tested sizes and exact N* |
| `area-51/twins-51/calibration.html` | sector-safe rungs conditional; finite-census scope | Gamma factor; 60/100-digit replay; exact Löwner N*; changelog |
| `research/project-51/formula51/FORMULA51_BAND_AND_DEDUCTION.md` | §3 repair by bounds on c (credited) | K/c proof; correction note with ranges; §6; PP274 wording |

`RELEASE_NOTES_v2_8_1.md` was also in the overlap by name only. Fork-A's file is kept unchanged. Track B's draft of the same name was never released, and its content is in `RELEASE_NOTES_v2_8_3.md`.

`RH STATUS: OPEN`
