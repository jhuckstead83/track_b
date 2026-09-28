# Cerebral Graphix v2.8.7 · a layout fix, and the Project 51 and Line Game upload sets

28 September 2026. Team B (Track B). **Base: v2.8.6.** **RH STATUS: OPEN.** Deploy exactly as for v2.8.6: install the v2.8.6 papers payload into `papers/`, which is unchanged here.

No Finance, homepage, hero or game-logic file changes.

## Fixed: the 51 Twins status ledger overflowed at tablet widths

v2.8.6 introduced a layout regression on the 51 Twins status ledger.
- **Cause.** The status column never wraps, and two v2.8.6 status entries were long. That made the table 1,127 px wide at every viewport. At 1024, 800 and 700 px the page scrolled sideways.
- **Why it was missed.** The v2.8.6 render check covered only 1280 and 375 px.
- **The fix.** The status cells now read "false (CERT, PROVED)" and "OPEN at 51", and their detail moves to the "where" column. No claim or status changed.
- **Checked.** The table fits its column at every width from 640 to 1440 px. Eleven pages, including the homepage and Finance, show no horizontal overflow and no page errors at seven widths from 390 to 1440 px: 77 views.

## New: upload sets for two Zenodo records

`ZENODO_RELEASE_PLAN_v2_8_7.md` gives the full, ordered file set for *Project 51* (10.5281/zenodo.23004789) and *The Line Game* (10.5281/zenodo.23004800), with names, MD5 and SHA-256. The author posts them as updates under the same DOIs.
- **Nothing on either record changed since before v5.2.** All nine files there are byte-identical to the earlier records' files (22943070 and 22985771) and to the site's copies. No title page prints its own record DOI.
- **Project 51 gains five files:**
  - PDFs of the 51 SEDAPS v0.4.1 research update, the 51 Twins exhibit, the 51 Twins calibration report, and the Formula 51 band and deduction;
  - the v2.8.7 research zip.
- **The Line Game** keeps its four files. It can add back the v7.5 edition that draws the card string as suit symbols, which was in the earlier Project 51 record.

## Verification

See `VALIDATION_v2_8_7.json`.
