# Zenodo plan for v2.8.5: three reserved DOIs, what goes where

28 September 2026. The author reserved three DOIs. They are pasted into the site as ordinary `https://doi.org/…` links, which resolve once each record is published. Until then DataCite returns 404, which is correct for a reserved DOI (PP284 §3). **After uploading, open each landing page once.** This plan supersedes the v2.8.4, v2.8.3 and v2.8.0 plans, which are kept as released.

## The records

| DOI (reserved) | Record | Upload | Where the site cites it |
|---|---|---|---|
| **10.5281/zenodo.23004335** | TN Postmaster Volume I **v5.2** | the three files of the v2.8.4 papers payload: `TN_Postmaster_Volume_I_v5_2_READING_VOLUME.pdf` (101 pp), `TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.pdf` (287 pp), `TN_Postmaster_Volume_I_v5_2_SOURCE.zip`; its `qa/BUILD_BINDING.json` binds both PDFs by SHA-256 | `research/postmaster/index.html` (source note, publication card, button, citation box, JSON-LD); the 51 Twins cite line; both `llms.txt`; `citation/catalog.json`; `site-index.json` |
| **10.5281/zenodo.23004789** | *Project 51: Reading the Record Across Rules*, the container for the Area 51 games and exhibit research | the 51 SEDAPS v0.4.1 files listed below; a zip of `area-51/twins-51/`; `research/project-51/formula51/` without `__pycache__/`; plus whatever the author adds for Project 51 itself | `area-51/sedaps-51/index.html` (research links); the 51 Twins cite line (`build-twins-page-v1.cjs`, rebuilt); `research/project-51/index.html` (latest record, the deduction link); both `llms.txt`; `citation/catalog.json`; `site-index.json` |
| **10.5281/zenodo.23004800** | *The Line Game \| Surprise Is Not Meaning*, a new version | the author's Line Game files | `research/line-game/index.html` (latest record); `llms.txt`; `citation/catalog.json`; `site-index.json` |

The version labels of the Project 51 and Line Game records were not supplied, so the site states none.

**Files for 51 SEDAPS inside the Project 51 record**, all in `area-51/sedaps-51/`:
- `RESEARCH_UPDATE_v0_4_1.md` and `RESEARCH_UPDATE_v0_4.md`;
- `past10-certificates-v0-4-1.json`, `verify-past10-v0-4-1.cjs`, `VERIFY_v0_4_1.json`;
- `count-histories-v0-4-1.cjs`, `HISTORY_COUNTS_v0_4_1.json`;
- `independent/`, including `live3_loops.c`, `live3_sync.c`, `live3_struct.c` and `LIVE3_LOOPS_RECEIPT.json`;
- `sedaps-lemma-v0-4.js`, `sedaps-v0-4.js`, `verify-sedaps-v0-4.cjs`, `VERIFY_v0_4.json`, `dstart4-certificates-v0-4.json`;
- the inherited `sedaps-core-v0-2.js` and `reachable-certificate-v0-3.json`.

## Related identifiers: outward links only

51 SEDAPS, 51 Twins and Formula 51 now sit inside one record. The cross-links the earlier plans listed between them (SEDAPS ↔ Twins, Twins → Formula 51) would be self-references. **Do not mint them** (PP284 §3a). What remains:

- **Project 51 (23004789) → TN Postmaster v5.2 (23004335):** `references`. The Twins plates and calibration draw on Dossier §§69A–69B.
- **TN Postmaster v5.2 (23004335) → Project 51 (23004789):** `isSupplementedBy`.
- **Project 51 (23004789) → Spivey, *Cycles in War*, INTEGERS 10 (2010) #G02:** `references`.
- **Project 51 (23004789) → The Line Game, concept 10.5281/zenodo.20792808:** `references`. Use the concept, since the dependence is on the work, not on one version.
- **Project 51 (23004789) → *Volume I: Exact Geometry and Symbolic Foundations*** (your existing DOI): `references`. The trapped tip is a drawing device only.
- **TN Postmaster v5.2 (23004335) → arXiv:2608.13637 and arXiv:2609.02882:** `references`. These are reference entries [121] and [66].
- Each new record should also be a new version of its concept: TN Postmaster **21968915**, Project 51 **22862811**, The Line Game **20792808**. PP284 confirmed 20792808 on DataCite as the Line Game's concept, with 17 versions.

## Concept or version

Cite the concept DOI when a page means "the current paper", and a version DOI when it means that version (PP284 §3.1). The site now follows this:
- TN Postmaster v5.2: 23004335, with version series 21968915.
- The Line Game: v7.2 citations stay on 22851517, where the text means v7.2, as in the Area 51 games that build on it. The latest record, 23004800, is named as such.

About 144 older references to the Line Game v7.2 DOI, many in homepage and UI files, still need a per-reference reading to decide concept or version. That pass is left open.

## No DOI placeholders remain

`grep data-doi-pending` finds nothing. All four earlier placeholders are now links: `tn-postmaster-v5-2`, `sedaps-51-v0-4-1`, `twins-51-v1` and `formula51-deduction`.
