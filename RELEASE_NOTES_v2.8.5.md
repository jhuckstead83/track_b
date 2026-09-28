# Cerebral Graphix v2.8.5 · reserved DOIs, and why equal deals miss the loops

28 September 2026. Team B (Track B). **Base: v2.8.4.** Deploy exactly as for v2.8.4: install the v2.8.4 papers payload into `papers/` first. The payload is unchanged here. **RH STATUS: OPEN.**

No Finance, homepage, hero or game-logic file changes.

## Reserved DOIs, now links

The author reserved three DOIs. The site links them as ordinary `https://doi.org/…` links, which resolve once each record is published. Until then DataCite returns 404, as it should for a reserved DOI. **Open each landing page once after uploading.** `ZENODO_RELEASE_PLAN_v2_8_5.md` lists what to upload to each record and which related identifiers to set.

| DOI | Record | Cited on |
|---|---|---|
| 10.5281/zenodo.23004335 | TN Postmaster Volume I v5.2 | Postmaster page (source note, publication card, button, citation box, JSON-LD), 51 Twins cite line, `llms.txt`, catalog, site index |
| 10.5281/zenodo.23004789 | *Project 51: Reading the Record Across Rules*: the Area 51 games and exhibit research | 51 SEDAPS research links, 51 Twins cite line, Project 51 page and its Formula 51 link, `llms.txt`, catalog, site index |
| 10.5281/zenodo.23004800 | *The Line Game \| Surprise Is Not Meaning*, latest record | Line Game page, `llms.txt`, catalog, site index |

- **Every placeholder is filled.** All four `data-doi-pending` placeholders are now links; `grep data-doi-pending` finds none.
- **Citations name the containing work.** 51 SEDAPS, 51 Twins and Formula 51 are cited as part of *Project 51* (PP284 §3b), because they sit in that one record.
- **Self-links dropped.** The Zenodo plan no longer mints cross-links among those three.
- **Version DOIs where a version is meant.** The Area 51 games still cite Line Game v7.2 (22851517), the version they build on. The concept DOI 20792808 names all versions.
- **Not yet done.** About 144 older Line Game references, mostly in homepage and UI files, still need a per-reference choice between concept and version.

## 51 SEDAPS: the structure of three-live loops

- **Every loop at n = 12 is rigid.** A check of all 1,145,664 loops (`independent/live3_struct.c`) finds the same structure in each:
  - exactly one queue plays a packet head on each turn, and that head wins;
  - the winners rotate, each queue winning every third turn;
  - the sizes cycle through the rotations of (5, 4, 3).
  - PP283 found the same from its own enumeration.
- **Theorem (new, PROVED).** If the winning card on a three-live loop is always a packet head, the three sizes are never pairwise congruent mod 3. So no equal deal reaches the loop, for any n.
  - Proof: there are L head plays and L wins per period, so every head wins and exactly one is played per turn.
  - PP284 proves a companion case, where uniform gaps and equal post-win sizes make the sizes three consecutive integers.
- **PP283 §3 withdrawn (PP284).** Its "3 | n" assumed equal post-win sizes. In general the post-win sizes sum to n + 3, which says nothing mod 3. So n = 13 was a genuine candidate, and its complete census is a real result.
- **The game's question, stated exactly.** A fair deal can enter a three-live loop only if all three queues play packet heads on the same turns (a "synchronised" loop). `independent/live3_sync.c` searches exactly those loops:
  - n = 9: none;
  - n = 12: none;
  - n = 15 (5–5–5): none. All 10,762,752,000 states lose a queue within 27 turns, so no 5–5–5 deal ever reaches such a loop.
  - At 51 the question is OPEN. The conjecture that settles it for every n is that no member card ever wins on a three-live loop. Every loop known satisfies it.

## TN Postmaster v5.2 build: two facts for the next edition

- **The Reader is at exactly 101 pages, its ceiling.** It has no headroom, so new material must replace weaker prose, or the gate fails (PP284 §5).
- **The Dossier's added pages all come after p. 266.**
  - Against a v5.1 rebuild in the same environment, every table-of-contents entry keeps its page through p. 266.
  - The new §69A–69C start at p. 267; the summary, Part E and the references follow them.
  - So the six Dossier anchors land on the same pages by structure, not by coincidence.
  - The v5.1 rebuild has 278 pages, where the published v5.1 has 281. Page totals depend on the TeX version; the anchor pages do not.

## Verification

See `VALIDATION_v2_8_5.json`.
