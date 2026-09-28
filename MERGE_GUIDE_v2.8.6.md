# Merge guide: Track B into the site, v2.8.6 (cumulative from Fork-A v2.8.2)

28 September 2026. When merging with a UI build based on v2.8.2, use this guide, not the v2.8.3, v2.8.4 or v2.8.5 guides. It covers everything Track B has changed:
- the v2.8.3 research pass;
- the v2.8.4 retarget to TN Postmaster v5.2;
- the v2.8.5 DOI links and loop results;
- the v2.8.6 title-page DOI, the new anchor checker and the three-live loop theorems.

**RH STATUS: OPEN.**

## First in the UI queue: the homepage still sends readers to v5.1

Track B leaves `index.html` untouched. It is the front door, and it links the superseded edition while the Postmaster page gives v5.2 (PP286 §3). Do this before anything else:

| `index.html` line | now | suggested |
| --- | --- | --- |
| 140–141 | `TN_Postmaster_Volume_I_v5_1_READING_VOLUME.pdf`, `…_TECHNICAL_DOSSIER.pdf` | the v5.2 files; the anchors are unchanged |
| 57 | "Triangular-n Postmaster v5.1 now has … a 281-page Technical Dossier" | v5.2, 287-page |
| 124 | `/assets/postmaster-v5-1-cover.webp` | `/assets/postmaster-v5-2-cover.webp` (added in v2.8.4), alt text v5.2 |
| 129 | chip "v5.1" | "v5.2" |
| 226 | "Postmaster edition frozen at v5.1" | "Postmaster edition v5.2" |

The v5.1 links still work, because v5.1 stays hosted.

## Before deploying

Install the **v2.8.6** papers payload, `TN_Postmaster_v5_2_PAPERS_PAYLOAD_v2_8_6.zip`, into `papers/`. It replaces the v2.8.4 payload and holds:
- `TN_Postmaster_Volume_I_v5_2_READING_VOLUME.pdf`, sha256 `80367cd579662327…`;
- `TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.pdf`, sha256 `48fbaeccbffad901…`;
- `TN_Postmaster_Volume_I_v5_2_SOURCE.zip`, sha256 `9163319a2c610efe…`;
- `anchors_v5_2.json`.

Both PDFs now print DOI 10.5281/zenodo.23004335 on the title page. Every v5.1 file stays in `papers/`.

After deploying, run this from the site root:

    python3 research/postmaster/check_anchors_v5_2.py --require-pdfs

It must pass all three checks: links, binding and pages. If it fails on binding, the installed PDFs are not the ones the map was built from.

## Rules

1. **"take v2.8.6" and "new file".** Copy the v2.8.6 file. If your build changed one of these after v2.8.2, re-apply your edit on top of the v2.8.6 copy.
2. **"merged".** Both traces edited these files, and the v2.8.6 copy holds both sets of edits. In `area-51/sedaps-51/index.html`, keep your Finance asset links.
3. **"delete".** Remove the file; it is build litter.
4. **Generated files.** Never hand-edit `area-51/twins-51/index.html` or `twins-data-v1.js`. Run `verify-twins-v1.cjs --write`, then `build-twins-page-v1.cjs --write`, then both again without `--write`.
5. **Atlas.** `atlas/index.html`, the JSON embedded in it, and `atlas/atlas-data.json` hold the same catalog three times. Edit them as a set until an atlas builder exists (PP280).
6. **Anchors.** After any change to a `#page=` link, or after installing new PDFs, run `check_anchors_v5_2.py --require-pdfs`. A rebuilt PDF fails the binding check until `anchors_v5_2.json` is regenerated from it.
7. **Frozen receipts.** Never retarget `MANIFEST_*`, `VALIDATION_*`, `release-v*`, `RELEASE_NOTES_*`, `RELEASE_CARD_*` or `docs/v2.0` files.
8. **DOIs.** The records 10.5281/zenodo.23004335, 23004789 and 23004800 are published; keep the links. Cite the concept DOI where a page means the current work, and a version DOI where it means one version.
9. **Loops.** A sentence saying loop lengths are multiples of 52 must say "two-queue loops" or "loops these deals reach". Three-live loops at 51 cards are not multiples of 52 in general (PP287).
10. **Version.** Set `area-51/research.json` `site_version` to your release number. Never reuse a number, and exclude `__pycache__/` from packages.

## Every file, with its SHA-256 (first 12 hex digits)

The full digests are in `MANIFEST_v2_8_3.json` (against v2.8.2), `MANIFEST_v2_8_4.json`, `MANIFEST_v2_8_5.json` and `MANIFEST_v2_8_6.json` (each against the release before). A dash means that the file did not exist in that version.

| file | rule | v2.8.0 | v2.8.2 (Fork-A) | v2.8.6 |
|---|---|---|---|---|
| `area-51/research.json` | merged | `0f4f8b2f500c` | `298a99cdd817` | `265c855e7d88` |
| `area-51/sedaps-51/RESEARCH_UPDATE_v0_4.md` | merged | `96fbd12bf0cd` | `0e0c2789d23e` | `16638efec8a3` |
| `area-51/sedaps-51/index.html` | merged | `a1e15a90e595` | `ca50d15f47ed` | `1c91d56d9126` |
| `area-51/sedaps-51/sedaps-v0-4.js` | merged | `4c09b4ec8303` | `81030df45f35` | `dfbf7c6ced5a` |
| `area-51/twins-51/build-twins-page-v1.cjs` | merged | `37509cc76c12` | `185c0eea4813` | `30e2b962e7e2` |
| `area-51/twins-51/calibration.html` | merged | `f58f6dd59e3a` | `62099a0f5e60` | `75c0ab65ea4c` |
| `area-51/twins-51/index.html` | merged | `72b2bc656569` | `635d565abadb` | `0f04ea0eeb62` |
| `area-51/twins-51/verify-twins-v1.cjs` | merged | `979f742e5f05` | `240d4c331e80` | `2e11d1e50bad` |
| `research/project-51/formula51/FORMULA51_BAND_AND_DEDUCTION.md` | merged | `1d862b7ed2fa` | `15efad2450c0` | `c157f47b4b49` |
| `_headers` | take v2.8.6 | `41b37b9ca4fa` | `41b37b9ca4fa` | `e14e747dca49` |
| `area-51/llms.txt` | take v2.8.6 | `a3486996fd9c` | `a3486996fd9c` | `6813c5c15ac1` |
| `area-51/sedaps-51/README.md` | take v2.8.6 | `6a583b9e2a11` | `6a583b9e2a11` | `492581a07a47` |
| `area-51/sedaps-51/VERIFY_v0_4.json` | take v2.8.6 | `48ae4311c64e` | `48ae4311c64e` | `5a2cd626a377` |
| `area-51/sedaps-51/sedaps-lemma-v0-4.js` | take v2.8.6 | `35ed0bba9618` | `35ed0bba9618` | `79d1d0796bc4` |
| `area-51/sedaps-51/verify-sedaps-v0-4.cjs` | take v2.8.6 | `b84cc2086042` | `b84cc2086042` | `01f39d07d71e` |
| `area-51/twins-51/twins-data-v1.js` | take v2.8.6 | `2a7d34815e4e` | `2a7d34815e4e` | `0eac2c83bbaf` |
| `atlas/atlas-data.json` | take v2.8.6 | `5b7072b2572d` | `5b7072b2572d` | `caff31ae8d91` |
| `atlas/index.html` | take v2.8.6 | `afd614101f2c` | `afd614101f2c` | `e0d4b1586412` |
| `citation/catalog.json` | take v2.8.6 | `97e321ae4324` | `97e321ae4324` | `665983c99463` |
| `llms.txt` | take v2.8.6 | `911e66b19a22` | `911e66b19a22` | `fe581ed1ce3e` |
| `research/line-game/index.html` | take v2.8.6 | `dade3ed42932` | `dade3ed42932` | `01950be1e51b` |
| `research/postmaster/index.html` | take v2.8.6 | `56ed101816c2` | `56ed101816c2` | `601258bace5f` |
| `research/project-51/index.html` | take v2.8.6 | `6e80130c914a` | `6e80130c914a` | `9adc6eb70259` |
| `site-index.html` | take v2.8.6 | `364b8a80821a` | `364b8a80821a` | `52b117bf96c7` |
| `site-index.json` | take v2.8.6 | `1cc49c52a070` | `1cc49c52a070` | `a451e217d004` |
| `sitemap.xml` | take v2.8.6 | `45abfeac5f89` | `45abfeac5f89` | `ee1c8dddc305` |
| `MANIFEST_v2_8_3.json` | new file | — | — | `240f28555e64` |
| `MANIFEST_v2_8_4.json` | new file | — | — | `59060a17d278` |
| `MANIFEST_v2_8_5.json` | new file | — | — | `27125674b967` |
| `MERGE_GUIDE_v2_8_3.md` | new file | — | — | `83884bb31a17` |
| `MERGE_GUIDE_v2_8_4.md` | new file | — | — | `38645d708132` |
| `MERGE_GUIDE_v2_8_5.md` | new file | — | — | `d2ba641785b0` |
| `RELEASE_NOTES_v2_8_3.md` | new file | — | — | `0653be91ec21` |
| `RELEASE_NOTES_v2_8_4.md` | new file | — | — | `4f70ac637ede` |
| `RELEASE_NOTES_v2_8_5.md` | new file | — | — | `deaa63cdbe08` |
| `RELEASE_NOTES_v2_8_6.md` | new file | — | — | `73a52cece04f` |
| `VALIDATION_v2_8_3.json` | new file | — | — | `588702d049cf` |
| `VALIDATION_v2_8_4.json` | new file | — | — | `15cce8bbf0bd` |
| `VALIDATION_v2_8_5.json` | new file | — | — | `fb91eab01e4c` |
| `VALIDATION_v2_8_6.json` | new file | — | — | `ce67da9decd0` |
| `ZENODO_RELEASE_PLAN_v2_8_3.md` | new file | — | — | `26468a36f0cc` |
| `ZENODO_RELEASE_PLAN_v2_8_4.md` | new file | — | — | `08d65b0c4508` |
| `ZENODO_RELEASE_PLAN_v2_8_5.md` | new file | — | — | `147ed5cd426f` |
| `ZENODO_RELEASE_PLAN_v2_8_6.md` | new file | — | — | `f6b15008a876` |
| `area-51/sedaps-51/HISTORY_COUNTS_v0_4_1.json` | new file | — | — | `45ef257c0308` |
| `area-51/sedaps-51/RESEARCH_UPDATE_v0_4_1.md` | new file | — | — | `6d22c8c5edec` |
| `area-51/sedaps-51/VERIFY_v0_4_1.json` | new file | — | — | `14f64fe2b6c9` |
| `area-51/sedaps-51/count-histories-v0-4-1.cjs` | new file | — | — | `a22ab741a44e` |
| `area-51/sedaps-51/independent/CENSUS_RECEIPT.json` | new file | — | — | `8005b301126b` |
| `area-51/sedaps-51/independent/LIVE3_LOOPS_RECEIPT.json` | new file | — | — | `92681f29670f` |
| `area-51/sedaps-51/independent/README.md` | new file | — | — | `2b427154d479` |
| `area-51/sedaps-51/independent/census2.c` | new file | — | — | `0bdaaccce8da` |
| `area-51/sedaps-51/independent/census_alt.c` | new file | — | — | `67554fb25438` |
| `area-51/sedaps-51/independent/census_deals.c` | new file | — | — | `c2903cb222e8` |
| `area-51/sedaps-51/independent/live3_construct.py` | new file | — | — | `aa1e2f6c5c36` |
| `area-51/sedaps-51/independent/live3_construct_check.cjs` | new file | — | — | `786c1f352db2` |
| `area-51/sedaps-51/independent/live3_construct_receipt.json` | new file | — | — | `641b6e599e8a` |
| `area-51/sedaps-51/independent/live3_loops.c` | new file | — | — | `f181849a7612` |
| `area-51/sedaps-51/independent/live3_packet.c` | new file | — | — | `0d70ff7a0b90` |
| `area-51/sedaps-51/independent/live3_probe51.py` | new file | — | — | `bfaa907da7b4` |
| `area-51/sedaps-51/independent/live3_probe51_receipt.json` | new file | — | — | `1594abc49ba8` |
| `area-51/sedaps-51/independent/live3_rigid12.c` | new file | — | — | `a20b2663e19d` |
| `area-51/sedaps-51/independent/live3_rigid12_receipt.json` | new file | — | — | `fb0f5e9f4a04` |
| `area-51/sedaps-51/independent/live3_rigid_period.py` | new file | — | — | `3170410e32cf` |
| `area-51/sedaps-51/independent/live3_rigid_period_receipt.json` | new file | — | — | `05eec7be3ae1` |
| `area-51/sedaps-51/independent/live3_struct.c` | new file | — | — | `b07bf719face` |
| `area-51/sedaps-51/independent/live3_sync.c` | new file | — | — | `ef05f926744d` |
| `area-51/sedaps-51/independent/sedaps_independent.py` | new file | — | — | `f7d34f2b01d6` |
| `area-51/sedaps-51/independent/sedaps_independent_receipt.json` | new file | — | — | `46d72544a865` |
| `area-51/sedaps-51/independent/war_period_sigma.py` | new file | — | — | `56838aa057fa` |
| `area-51/sedaps-51/past10-certificates-v0-4-1.json` | new file | — | — | `97a76858be9a` |
| `area-51/sedaps-51/verify-past10-v0-4-1.cjs` | new file | — | — | `78d63c0522c9` |
| `area-51/twins-51/evidence/dh_twin_highprec.py` | new file | — | — | `b9227cfd4169` |
| `area-51/twins-51/evidence/dh_twin_highprec_receipt.json` | new file | — | — | `7fe78c04670e` |
| `assets/postmaster-v5-2-cover.webp` | new file | — | — | `73bf27c044de` |
| `research/line-game/The_Line_Game_Surprise_Is_Not_Meaning_v7_5.pdf` | new file | — | — | `4bef214c475b` |
| `research/postmaster/anchors_v5_2.json` | new file | — | — | `70edd71c91d0` |
| `research/postmaster/check_anchors_v5_2.py` | new file | — | — | `00afca6bc1bd` |
| `research/project-51/Project_51_v0_4.pdf` | new file | — | — | `becd348f5cdd` |
| `research/project-51/Telescope_51_v0_7.pdf` | new file | — | — | `3a13181d422a` |
| `research/project-51/formula51/Formula_51_Concise_Method_2026-09-26.pdf` | new file | — | — | `ed97b5716a14` |
| `research/project-51/formula51/f51_independent.py` | new file | — | — | `864bca30942a` |
| `research/project-51/formula51/f51_independent_receipt.json` | new file | — | — | `3e778469fd76` |

`RH STATUS: OPEN`
