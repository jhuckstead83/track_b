# Cerebral Graphix v2.8.4 · the site points to TN Postmaster v5.2

28 September 2026. Team B (Track B). **Base: v2.8.3.** This release follows the author's decision, relayed in PP279, that the site cite v5.2. **RH STATUS: OPEN.**

It adds no Finance, homepage or hero change and no game logic. v2.8.3's notes remain the record of the research pass; this file lists only what changed after it.

## Deploy in this order

1. Restore `papers/`, then install the **papers payload** (`TN_Postmaster_v5_2_PAPERS_PAYLOAD.zip`) into it:
   - `TN_Postmaster_Volume_I_v5_2_READING_VOLUME.pdf` (101 pages);
   - `TN_Postmaster_Volume_I_v5_2_TECHNICAL_DOSSIER.pdf` (287 pages);
   - `TN_Postmaster_Volume_I_v5_2_SOURCE.zip` (the v2.8.4 source edition, with its build receipts);
   - `anchors_v5_2.json` (the named page anchors).
2. Deploy the site.

Every v5.1 file stays hosted at its own URL, and every v5.1 link keeps working. Until step 1 is done, the new v5.2 links point at files that are not there yet (PP279 §4).

## The v5.2 PDFs

- **Built** from the v5.2 source with pandoc 3.1.3 and TeX Live 2023.
  - Reading Volume: 101 pages, exactly at its ceiling.
  - Technical Dossier: 287 pages.
  - Neither has an undefined reference, a missing character, or an overfull box over 30 pt.
- **Like-for-like baseline.** The v5.1 Reader, rebuilt in the same environment, comes to its recorded 101 pages.
- **Checks.** `qa/check_v52_interface.py` passes 74/74 with the build receipts. `qa/BUILD_BINDING.json` binds both PDFs by SHA-256, and the v2.8.4 source zip carries these receipts.
- **Unchanged files.** The v5.1 and v5.0 provenance files are still byte-identical.

## Named page anchors, and the retarget

- **The extractor.** `anchors_v5_2.json` gives the page of each of the 22 targets the site links to: 16 in the Reader and 6 Dossier chapters.
  - A target is found by its printed heading, not by PDF bookmark. Bookmarks sit one page early on four v5.1 headings.
  - The same extractor reproduces all 22 v5.1 anchors from a v5.1 rebuild.
- **Every target keeps its page from v5.1 to v5.2.** So the retarget changes file names only.
- **The pages still say the same thing.** On the R12, R23 and R24 pages, the only difference between v5.1 and v5.2 is the running header. R23 still names exactly the same unsupported source estimates. Reference 11 is still the Laguerre total-variation paper (PP279 §6).
- **A checker.** `research/postmaster/check_anchors_v5_2.py` asserts that every `#page=` link into a v5.2 PDF lands on a named target: 49 links, 22 targets, none unnamed. A future re-pagination will fail this check instead of landing silently on the wrong page.

**Files retargeted, by `retarget_v52.py`** (guarded: it refuses any `MANIFEST`, `SHA256`, `VALIDATION`, `release-v`, `RELEASE_NOTES`, `RELEASE_CARD` or `docs/v2.0` path):

| File | Change |
| --- | --- |
| `research/postmaster/index.html` | PDF links and page anchors → v5.2. Title, meta tags, JSON-LD, chip, v5.2 cover (`assets/postmaster-v5-2-cover.webp`, rendered from page 1), caption, Dossier length, source package, edition block and citation → v5.2. v5.1 PDFs and packages remain linked as the previous edition. "What v5.1 changes" becomes "What v5.1 changed". |
| `atlas/index.html`, its embedded JSON, `atlas/atlas-data.json` | patched as one set, since the three copies mirror each other. Every "v5.1" there named the current edition. An atlas builder is the next increment (PP280). |
| `site-index.html`, `site-index.json` | v5.2 PDFs, source and anchors added as current; v5.1 kept as the previous edition. |
| `sitemap.xml`, `_headers` | v5.2 entries added; v5.1 entries kept. |

**Left for the UI session.** The homepage (`index.html`) still links the v5.1 Reader and Dossier and shows the v5.1 cover. Those links keep working.

**Frozen receipts, untouched.** Historical manifests, validation files and release notes that name v5.1 are unchanged, as they should be. PP279 counts 54 such references in 11 files.

## 51 SEDAPS: loops that keep three queues live, at 13 cards

- The packet-form search now covers n = 13: 12,454,041,600 states, none on a loop, every one losing a queue within 26 turns.
- So loops keeping three queues live exist at 12 cards, but not at 13 or at 11 or fewer. By the packet-form lemma, both are statements about the whole state graph.
- For the 51-card game the open question is unchanged: can an equal deal reach such a loop?

## Verification

See `VALIDATION_v2_8_4.json`.
- Rendered checks in Chromium, at 1280 × 900 and 375 × 812, cover eight pages including the atlas and the site index. No page overflowed or threw an error.
- The link check covers 917 local references. It reports 147 references to 30 targets under `papers/` separately. The two new targets are the v5.2 PDFs, which are in the payload.
- The Twins page matches its data. The anchor check passes.
