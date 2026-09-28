# Cerebral Graphix v2.8.6 · the DOIs are live, the title pages carry them, and three-live loops exist at 51 cards

28 September 2026. Team B (Track B). **Base: v2.8.5.** **RH STATUS: OPEN.**

**Deploy.** Install the **v2.8.6** papers payload into `papers/` (it replaces the v2.8.4 payload), then deploy the site, then run:

    python3 research/postmaster/check_anchors_v5_2.py --require-pdfs

No Finance, homepage, hero or game-logic file changes.

## The three records are published

The author published the three records on Zenodo on 28 September 2026, with earlier files, and will swap in the v2.8.6 files.
- `citation/catalog.json` now marks them `published`, and `site-index.json` drops "(reserved DOI)".
- **What to swap in.** `ZENODO_RELEASE_PLAN_v2_8_6.md` lists each file with the MD5 that Zenodo displays and its SHA-256. For Project 51 it now supplies one upload-ready zip, `Project51_Area51_Research_v2_8_6.zip`. Its paths mirror the site, so every verifier runs in place, and it was tested that way.
- **If a swap is refused.** The plan also says what happens if Zenodo will not replace files on a published version.

## TN Postmaster v5.2: the DOI on both title pages

- **The change.** Both title pages now print `DOI 10.5281/zenodo.23004335`, as a link, under `RH STATUS: OPEN`. It is one line in each title block; neither master changed.
- **Rebuild facts:**
  - Reading Volume 101 pages, still exactly at its ceiling;
  - Technical Dossier 287 pages;
  - all 22 named anchors on the same pages, re-extracted from the new PDFs by heading;
  - `qa/check_v52_interface.py` 74/74;
  - `provenance/v5_1`, `v5_0` and `v50` byte-identical.
- **New hashes.** Reading Volume `80367cd5…`, Dossier `48fbaecc…`, source zip `9163319a…`. They are recorded in `anchors_v5_2.json` and in the source's `qa/BUILD_BINDING.json`.
- **Ordering.** The rebuild ran before PP286 arrived. The anchors were nonetheless re-derived from the new PDFs rather than assumed, and the new checker below passes on them.

## The anchor checker now checks pagination (PP286 §0)

PP286 found that `check_anchors_v5_2.py` never opened a PDF. It compared the links with a map written from the same build, so a re-pagination would have passed. It now runs three checks and reports which of them ran:
1. **links.** Every `#page=` link names a mapped page, as before.
2. **binding.** The installed PDFs have the SHA-256 the map was built from, and so does `qa/BUILD_BINDING.json` inside the installed source zip.
3. **pages.** With PyMuPDF installed, it re-derives every heading's page from the PDFs.

The test matrix:

| installed | result |
|---|---|
| no papers | links only; `--require-pdfs` fails |
| the v2.8.6 payload | all three pass |
| the v2.8.4 PDFs | binding fails |
| a blank page inserted into the Reading Volume | binding and pages fail, and the report names each moved target, e.g. `part_IV` 44 → 45 |

## Correction: the Dossier's 278 versus 281 pages

The v2.8.5 notes said the v5.1 rebuild has 278 pages against the published 281, and put that down to the TeX version. **That was wrong.**
- **The cause.** The build appends the three historical facsimile pages to a 278-page body. The published v5.1 receipt records exactly that: 278 body pages, 281 in all.
- **The rebuild matches.** The rebuild's final PDF also has 281 pages. The 278 was its body PDF, which is where the anchor baseline was read.
- **The anchors are safe.** The facsimile goes at the end, after p. 278, so it cannot move an anchor, the deepest of which is p. 266.
- **What was not checked.** The rebuild's TeX differs from the published build's, which ran on a newer pandoc and TeX Live 2025, so the published v5.1 PDF was not compared with it page by page. Its six anchor pages were set on the site against the published PDF, and the rebuild reproduces all six. The 37.5 MB v5.1 package could not be fetched here, so a direct lookup in the published PDF remains with the Blue Team, as PP286 offered.

## 51 SEDAPS: loops that keep three queues live exist at 51 cards

All of this is in `RESEARCH_UPDATE_v0_4_1.md` §2.
- **Construction theorem (PROVED).** Take a state in packet form whose partial tails have lengths 0, 1 and 2, with at least one whole packet per queue, and whose packet heads are the K = n/3 − 1 largest cards.
  - On such a state the head always wins, and the next state has the same form.
  - The step can be undone inside the set, so the turn permutes the set and every such state lies on a three-live loop.
  - With the rigidity theorem this gives an exact answer: *a rigid three-live loop exists if and only if 3 divides n and n ≥ 12.*
  - The site's own engine replays a 51-card witness on the shipped deck. It returns after 180 turns with three queues live throughout.
- **Period theorem (PROVED).** On a rigid loop the winner depends only on the phases, so every card moves by a fixed permutation of positions. The period is 3·lcm(k_A, k_B, k_C, k_A+k_B+1, k_B+k_C+1, k_C+k_A+1) or 3·lcm(k_A, k_B, k_C, K+1, K+2), where the k are whole-packet counts and the choice depends on seating orientation.
  - It is checked against the permutation and against play for every shape from n = 12 to 51.
- **At 51 cards.** There are exactly 29 rigid periods, from 180 to 64,260.
  - Only 6 are multiples of 52. All 19 periods PP287 collected are on the list.
  - All 29 are multiples of 18, and that is proved. It holds at 51 only: the gcd is 3 at 12 cards.
- **n = 12 by a second method.** `live3_rigid12.c` enumerates every rigid-shape state and reproduces the census exactly: 1,036,800 loops of length 9 and 108,864 of length 60. So every loop at 12 cards is rigid.
  - The length-60 loops occur only when the heads are the top three cards.
- **Q1 and Q2 kept apart (PP285 §3).**
  - *Existence:* yes at every multiple of 3 from 12, and no at 13 or at 11 and below. 14 and the other non-multiples of 3 are untested.
  - *Reachability from a fair deal:* only a synchronised loop could be reached. The whole-packet search is complete for those (PP285 §2), and it finds none at 9, 12 or 15 cards. **Open at 51.**
  - PP285's lemma that every turn playing the global maximum is rigid is recorded.
  - A 3,000-sample probe at 51 is quantified as C: it excludes a density above about 0.1% at about 95%.

## "A multiple of 52" is now scoped to two-queue loops (PP287)

The multiple-of-52 law is proved for two-queue loops, which are all that the 2,000 seeded deals reach. It is false for three-live loops.
- **Where the scope was added.** Twins Plate IV's lead, chips and ledger; the SEDAPS page note; both `llms.txt`; and the check name in `verify-sedaps-v0-4.cjs`.
- **The v0.4 receipt.** `VERIFY_v0_4.json` was regenerated, and only that name changed.
- **The lesson** is written beside the n ≤ 11 census lesson: a pattern confirmed by sampling is a fact about the sample.

## Smaller fixes

- The header comments of `live3_sync.c`, `live3_struct.c` and `live3_loops.c` were stale copies of `live3_packet.c`'s. They now describe each program, and the `independent/` README lists every program.
- `area-51/research.json` `site_version` is 2.8.6, and the sitemap dates the changed pages 2026-09-28.

## For the UI session, first in the queue

The homepage links the v5.1 PDFs at `index.html` lines 140–141, and names v5.1 in prose at lines 57, 124, 129 and 226. It is the front door, so it should move before anything else (PP286 §3). The merge guide lists the suggested edits.

## Verification

See `VALIDATION_v2_8_6.json`.
