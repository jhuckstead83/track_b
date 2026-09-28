# Zenodo plan for v2.8.7: the Project 51 and Line Game sets, in order

28 September 2026. Team B (Track B). **RH STATUS: OPEN.**

This plan supersedes the v2.8.6 plan for records 23004789 and 23004800. The TN Postmaster record 23004335 is unchanged: use the v2.8.6 plan for it.

The author will post each set as an update to the same record, keeping the same DOI.

## Did any file change since before v5.2?

No. All nine files now on these two records are byte-identical to the files in the earlier records, and to the site's copies:
- Line Game v7.5: 10.5281/zenodo.22943070;
- Project 51 v0.4 with Telescope 51 v0.7: 10.5281/zenodo.22985771.

Their titles and version labels are unchanged:
- Line Game v7.5, 22 September, corrected 24 September;
- Project 51 v0.4 and Telescope 51 v0.7, 26 September;
- the 51 SEDAPS v0.1 note;
- the Formula 51 method, 26 September.

None of them prints its own record DOI, so no title page is out of date. The Line Game v7.5 paper cites TN Postmaster v5.1 (22844194) and the concept 21968915. That is a pinned citation of the version it used, and it can stay.

## Order and names

Upload in this order. The two-digit prefixes keep the order if Zenodo sorts files by name. Renaming is safe: the site links the record pages, never a Zenodo file name. A file marked "kept" is byte-identical to the one on the record now, under the new name.

### 10.5281/zenodo.23004800 · The Line Game | Surprise Is Not Meaning

| # | file | bytes | MD5 (Zenodo shows this) | what it is | action |
|---|---|---:|---|---|---|
| 01 | `01_The_Line_Game_Surprise_Is_Not_Meaning_v7_5.pdf` | 394,900 | `c3933b667c178dcef7f66d5b33a004af` | same file as Surprise_Is_Not_Meaning_v7_5.pdf, renamed | kept |
| 02 | `02_The_Line_Game_v7_5_Card_Symbols.pdf` | 424,068 | `f67dddeeb4b7ff45cf979292d7075dac` | v7.5 with the card string drawn as suit symbols (page 4); it was in 22985771 and is in neither new record | optional, add back |
| 03 | `03_Playing_Cards_Field_Guide.pdf` | 90,365 | `765575a059d64538ecaebbecdad327f5` | unchanged | kept |
| 04 | `04_Playing_Cards_Printable_Set.pdf` | 60,677 | `9053b21196899e599d4cee86e08ba33e` | unchanged | kept |
| 05 | `05_Exact_Card_String.txt` | 2,011 | `52111e9a6b50bd1fc9e1eb9e4e2220f9` | unchanged | kept |

Team B has no new Line Game paper. Only file 02 is an addition, and it is optional: it is the v7.5 edition that draws the card string as suit symbols.

### 10.5281/zenodo.23004789 · Project 51: Reading the Record Across Rules

| # | file | bytes | MD5 (Zenodo shows this) | what it is | action |
|---|---|---:|---|---|---|
| 01 | `01_Project_51_v0_4.pdf` | 282,784 | `59cf73a53598cebb0e01e9db8c884b6e` | the Project 51 paper, working draft v0.4 | kept |
| 02 | `02_Telescope_51_v0_7.pdf` | 274,025 | `1b6dd6fa13dd814c2df323b9c09d1790` | Telescope 51, working draft v0.7 | kept |
| 03 | `03_51_SEDAPS_v0_4_1_Research_Update.pdf` | 185,719 | `961c37d74a61d9b7eddefb43a55595f3` | 51 SEDAPS v0.4.1: turn-count filter, history counts, loop theorems (rigid three-live loops at 51 cards, period formula) | new |
| 04 | `04_51_Twins_v1_Exhibit.pdf` | 660,987 | `44aa3d0aa8a35959f6b7c99deee95a3a` | the 51 Twins plates and status ledger, printed from the site page | new |
| 05 | `05_51_Twins_v1_Calibration_Report.pdf` | 181,046 | `c07a5528ad7cb2684ee4c0a4a1e9bcf8` | the Davenport-Heilbronn twin calibration numbers | new |
| 06 | `06_Formula_51_Concise_Method_2026-09-26.pdf` | 217,546 | `5ca8972e22ba88a798438d3a0a3fce62` | Formula 51 method record | kept |
| 07 | `07_Formula_51_Band_and_Deduction.pdf` | 104,178 | `a5e066409935eec008312a7aceae69f3` | the 588-radix band, the repaired uniqueness deduction, the independent recomputation | new |
| 08 | `08_51_SEDAPS_v0_1_Working_Note.pdf` | 147,100 | `8a270c82293a22956993fea295f5be3b` | same file as 51_SEDAPS_v0_1.pdf, renamed; the historical v0.1 note | kept |
| 09 | `09_Project51_Area51_Research_v2_8_7.zip` | 395,262 | `71b4ae7dd70220536d74af7b4fa69e9a` | code, certificates, verifiers and receipts; the verifiers run in place | new |
| 10 | `10_Project_51_Review_2026-09-26.zip` | 4,099,359 | `a8c408fd1fd2f94caac42843aa43490e` | same file as "Project_51_Review_2026-09-26 (1).zip", with the download suffix dropped | kept |

**The five new files:**
- 03, 04, 05 and 07 are readable PDFs of research that was published only as site pages or Markdown.
- Each new PDF names the record on its title block, as *Project 51* DOI 10.5281/zenodo.23004789, and says RH STATUS: OPEN.
- 04 is the 51 Twins exhibit printed from the site page.
- 09 replaces the v2.8.6 research zip. It is identical except for the corrected 51 Twins ledger layout.

## After posting

Open each record and compare the MD5 shown beside every file with the tables above. Chromium stamps a creation time into each PDF it writes, so the new PDFs match these MD5s only as shipped. If you rebuild one, re-check its MD5.
