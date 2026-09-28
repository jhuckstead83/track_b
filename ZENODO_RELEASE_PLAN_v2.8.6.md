# Zenodo plan for v2.8.6: the three records are live, and these are the files to swap in

28 September 2026. The author published the three records on Zenodo today, with earlier files, and will swap in the files below. **RH STATUS: OPEN.**

This plan supersedes the v2.8.5, v2.8.4, v2.8.3 and v2.8.0 plans, which are kept as released.

This environment cannot reach zenodo.org or doi.org, so Team B has not seen the published records. After each swap, open the record and compare the MD5 that Zenodo shows beside each file with the table below.

## The records

| Record | DOI | Landing page |
|---|---|---|
| TN Postmaster Volume I **v5.2** | 10.5281/zenodo.23004335 | https://zenodo.org/records/23004335 |
| *Project 51: Reading the Record Across Rules*: the Area 51 games and exhibit research | 10.5281/zenodo.23004789 | https://zenodo.org/records/23004789 |
| *The Line Game \| Surprise Is Not Meaning*, latest record | 10.5281/zenodo.23004800 | https://zenodo.org/records/23004800 |

## Files to swap in

The files are in `dist/v2.8.6/` of the repository and in the v2.8.6 papers payload.

### 23004335 · TN Postmaster v5.2

These PDFs print this record's DOI on their title pages. The earlier upload, if it was the v2.8.4 build, did not.

| file | bytes | MD5 (Zenodo shows this) | SHA-256 |
|---|---:|---|---|
| `TN_Postmaster_Volume_I_v5_2_READING_VOLUME.pdf` (101 pp) | 4,981,812 | `39d12d7490253123319b2ba5c9dd58a4` | `80367cd57966232702b69263d0b813e9d8f24ed3f0948c7bb7981ea5b451ec3e` |
| `TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.pdf` (287 pp) | 12,541,380 | `2a16d88611ce630046662494e5781cd8` | `48fbaeccbffad9013625724e6142d06fc8b9dc8d13e284610585b25f8fda890c` |
| `TN_Postmaster_Volume_I_v5_2_SOURCE.zip` | 22,774,746 | `c7906d81e51f9a898bbcb091d895c8a6` | `9163319a2c610efe0959aec023f127a3930f24686d27f9d0169dbb8c89097888` |

`qa/BUILD_BINDING.json` inside the source zip binds both PDFs by SHA-256. The site's `research/postmaster/anchors_v5_2.json` records the same two hashes.

### 23004789 · Project 51

| file | bytes | MD5 | SHA-256 |
|---|---:|---|---|
| `Project51_Area51_Research_v2_8_6.zip` | 395,292 | `2735152f32525891ba3d4b91ef53c277` | `789c42873ca89af595b28b21dd787dac3141f6671804e3f69b44818b28fae261` |

This one zip replaces the file list of the v2.8.5 plan. Its paths mirror the site, so every verifier runs in place, and its `README.md` lists the quick checks. It holds:
- 51 SEDAPS v0.4.1: the research update, certificates, verifiers and receipts, and `independent/`, which includes the new three-live loop programs;
- 51 Twins v1, with the two Prospect 51 engine files its verifier reads;
- Formula 51, without `__pycache__/`.

Add whatever the author includes for Project 51 itself.

### 23004800 · The Line Game

The author's files. Team B supplies none.

## If a file cannot be swapped

Zenodo may not let the files of a published version be replaced. In that case, publishing a new version mints a new DOI.
- **Project 51 or the Line Game.** Only the site's links would move to the new number.
- **TN Postmaster.** The v5.2 PDFs print 23004335 on their title pages, so a new version needs a one-line rebuild with the new number. `check_anchors_v5_2.py` would then fail on the old hashes until the map is regenerated, which is its job.

Send Team B the new number either way.

## Related identifiers

These are unchanged from v2.8.5.
- **Project 51 (23004789) → TN Postmaster v5.2 (23004335):** `references`. The Twins plates and the calibration draw on Dossier §§69A–69B.
- **TN Postmaster v5.2 (23004335) → Project 51 (23004789):** `isSupplementedBy`.
- **Project 51 (23004789) → Spivey, *Cycles in War*, INTEGERS 10 (2010) #G02:** `references`.
- **Project 51 (23004789) → The Line Game, concept 10.5281/zenodo.20792808:** `references`.
- **Project 51 (23004789) → *Volume I: Exact Geometry and Symbolic Foundations*** (the author's existing DOI): `references`.
- **TN Postmaster v5.2 (23004335) → arXiv:2608.13637 and arXiv:2609.02882:** `references`.
- Do not mint links among 51 SEDAPS, 51 Twins and Formula 51. They sit in the one record, so those links would point at itself.

## Version series

Each record should be a version of its concept. The Blue Team has now checked all three concept DOIs on DataCite:
- TN Postmaster **21968915**;
- The Line Game **20792808**: 17 versions (PP284 §3.1);
- Project 51 **22862811**: title matches exactly, 8 versions (PP286 §2).

Cite the concept DOI where a page means the current work, and a version DOI where it means one version.

## Correction to the v2.8.5 plan

Its last section says "`grep data-doi-pending` finds nothing". That grep also matches prose in the frozen earlier plans, such as `ZENODO_RELEASE_PLAN_v2_8_0.md` and `ZENODO_RELEASE_PLAN_v2_8_3.md` (PP286 §4). The true statement is narrower: **no `data-doi-pending` attribute remains in any page source.** The v2.8.5 plan is kept as released.
