# Track B — Area 51 research (Team B)

Track B is the Area 51 research line of Cerebral Graphix: the papers, the interactive HTML
exhibits and games, and the programs that check them. Author: Jeffery Lyn Huckstead
([ORCID 0009-0007-0234-2177](https://orcid.org/0009-0007-0234-2177)). **RH STATUS: OPEN.**
Nothing here is evidence for or against the Riemann hypothesis.

This release is **v2.8.5** (28 September 2026). It adds the author's reserved DOIs as links and new results on three-live loops. Before it, v2.8.3 placed the Track B research pass
(corrections, independent replays, and new results) on the Fork-A v2.8.2 site, which carries
the Finance and homepage work. v2.8.4 built the TN Postmaster v5.2 PDFs and pointed the site's
research pages at them. The live site is published from the full site package. This
repository holds the Track B parts of it, plus the paper sources and the verification programs.
It does not hold the Finance pages or the homepage. Track B's working draft of 27 September
was labelled "v2.8.1"; that label was never released, and the only v2.8.1 is Fork-A's.

Status words are used exactly: **PROVED** (argument given), **CERT** (explicit object
replayed by the shipped rule), **COMPUTED** (exhaustive search resting on a proved lemma),
**EVID** (sampled or numerical, not a theorem), **OPEN**.

## What is here

| Path | Contents |
| --- | --- |
| `site/area-51/` | the Area 51 lab: Invariant, Blackjack 51, Telescope 51, Memory 51, Prospect 51, **51 SEDAPS**, the **51 Twins** exhibit and its calibration report |
| `site/research/` | research pages: Project 51 and Formula 51, the Line Game, TN Postmaster |
| `site/atlas/`, `site/citation/`, `site/llms.txt`, `site/sitemap.xml`, `site/site-index.*`, `site/_headers`, `site/assets/postmaster-v5-2-cover.webp` | the research atlas, the citation catalog, and the index and header files these pages feed |
| `papers/TN_Postmaster_Volume_I_v5_2_SOURCE/` | TN Postmaster Volume I v5.2, source edition: Markdown masters, build scripts, interface check (67/67), twin evidence, v5.1 and v5.0 provenance |
| `verification/` | independent replays and audits (see below) |
| `dist/v2.8.5/` | full site (without `papers/`) and cumulative research delta |
| `dist/v2.8.4/` | the papers payload (v5.2 PDFs, source zip, page anchors), unchanged in v2.8.5: install it into `papers/` first; plus the v2.8.4 site archives |
| `dist/v2.8.3/` | the v2.8.3 archives |
| `RELEASE_NOTES_v2.8.4.md`, `MERGE_GUIDE_v2.8.4.md` (cumulative from Fork-A v2.8.2), `MANIFEST_v2.8.4.json`, `VALIDATION_v2.8.4.json`, and the v2.8.3 counterparts | what changed, how to merge it with later UI work, file hashes, and the checks run |
| `legacy/transient-rational-locking-v1.0.0/` | the earlier Track B release (Transient Rational Locking), kept as it was |

The game pages use root-relative paths (`/area-51/...`, `/assets/...`). To play them, unpack
the full site package at a web root and serve it over HTTP.

## Results in this release

**51 SEDAPS: the turn count is part of the filter (v0.4.1).**
- The certified turn-85 present has four legal pasts.
- 01 and 11 fail the mod-3 clock at every turn (PROVED).
- Past 10 is reached from 17–17–17 deals at elapsed turns 24, 27, 30 and 33, and at no other turn (CERT + COMPUTED).
- So at turn 85 exactly one past comes from a fair deal, and no history bit is needed. Without the turn count, two pasts survive and one bit decides.
- The search is a proof (PROVED, §1.1 of the v0.4.1 update). For a start state with at least two live queues, the predecessor list is complete and the shape test is necessary. The lemma's header now states that scope, because terminal states fail the test yet are reachable.
- Independent returns: the Blue Team replayed the certificates (PP274), reproduced the turn-84 exclusion exactly (PP275: 336 states, lowest turn 66) and audited the proof (PP276).
- Files: `site/area-51/sedaps-51/past10-certificates-v0-4-1.json`, `verify-past10-v0-4-1.cjs`.

**Exact history counts.**
- Below turn 17, a three-live state that passes the shape test is reached by exactly t!/(a! b! c!) deals, where a, b, c are its packet counts (PROVED).
- So the turn-32 present with four pasts is reached by exactly 484,731,472 fair deals. The count is confirmed deal by deal for three of its four pasts.

**Loop periods.**
- Once one queue empties, the rule is War with the winning card placed first.
- For odd decks its loops alternate winners (Spivey, *Cycles in War*, 2010).
- Alternation forces the period L = 2·lcm(α/2, (n+1)/2, (n−1−α)/2), a multiple of n + 1 (PROVED).
- At 51 cards the formula allows exactly 12 lengths, and those are exactly the 12 seen in 2,000 seeded deals.
- Complete censuses of every state through 11 cards (3.11 × 10⁹ states) find no loop with three live queues.
- **At 12 cards such loops exist**: 1,145,664 of them, of lengths 9 and 60 (CERT). The smallest is A = 6 0 1, B = 2 10 7 3, C = 4 8 11 5 9.
- Every one of them is rigid: on each turn exactly one queue plays a packet head, and that head wins. A proved theorem says no equal deal ever reaches a rigid loop, at any n.
- An exhaustive search of synchronised states (the only kind an equal deal reaches) finds no loop at 9, 12 or 15 cards.
- None exists at 13 cards either: all 12,454,041,600 packet-form states lose a queue within 26 turns.
- For the 51-card game the open question is: can a fair deal reach a loop that keeps three queues live?

**Formula 51.**
- The self-description proof had a false ceiling step; it is repaired, and the conclusion stands.
- An independent recomputation reproduces all 588 band tables.
- It also replays, as the requested second return, two Blue Team results: the 257-radix trailing-minimum window and the polar-fibre closed form.

**51 Twins and TN Postmaster v5.2.**
- The Davenport–Heilbronn twin has the reflection F(s) = F(1 − s) of completed zeta, but a different Gamma factor.
- The rung failure at k = 16,589 is computed on a finite zero list. It reproduces at 60 and 100 digits.
- Löwner sizes: the published table tested steps of 5. Read pivot by pivot, the exact first failing sizes are N* = 105, 106 and 107 at the three centres (confirmed at 320 digits).
- The v5.2 PDFs are built: Reader 101 pages, Dossier 287; interface check 74/74. All 22 page anchors the site uses keep their v5.1 pages.
- "No finite rung prefix decides RH" was an overclaim and is replaced.

**Deep history.**
- The v0.5 Definitive Union synthesis (Zenodo 10.5281/zenodo.21968858) replays 13/13.
- The v5.0 source-rung certificates W₂–W₆ were re-executed for the first time since v5.0. Both backends reproduce their shipped receipts, at the shipped parameters and at the second parameter set.

## Verification

| Program | Checks |
| --- | --- |
| `node site/area-51/sedaps-51/verify-sedaps-v0-4.cjs --decks` | SEDAPS v0.4 certificates, clock, remnant, deck sweep |
| `node site/area-51/sedaps-51/count-histories-v0-4-1.cjs --brute` | exact history counts, with a deal-by-deal cross-check |
| `site/area-51/sedaps-51/independent/live3_loops.c` | every packet-form state, played until a queue empties; catalogues three-live loops |
| `node site/area-51/sedaps-51/verify-past10-v0-4-1.cjs` | the four past-10 certificates, every elapsed turn, and the lemma's scope on 2,000 deals |
| `python3 site/area-51/sedaps-51/independent/sedaps_independent.py` | independent Python replay of all SEDAPS certificates |
| `site/area-51/sedaps-51/independent/census2.c` (and `census_alt.c`, `census_deals.c`) | complete state censuses; OEIS A400411 cross-check |
| `node site/area-51/twins-51/verify-twins-v1.cjs` | rebuilds the Twins data byte for byte |
| `python3 site/area-51/twins-51/evidence/dh_twin_highprec.py site/area-51/twins-51/evidence/dh-zeros-T260.json` | twin rung signs at 60 and 100 digits |
| `python3 site/research/project-51/formula51/f51_independent.py site/research/project-51/formula51/f51_band.json` | Formula 51, all radices, independently |
| `python3 papers/TN_Postmaster_Volume_I_v5_2_SOURCE/qa/check_v52_interface.py` | TN Postmaster v5.2 interface check, 67/67 |
| `python3 verification/deep_history/v05_synthesis_checks.py` | v0.5 synthesis identities and the constant-Jacobian counterexample |
| `verification/deep_history/` receipts | v5.0 certificate re-execution (both parameter sets) |
| `python3 papers/TN_Postmaster_Volume_I_v5_2_SOURCE/provenance/v5_2/evidence/team_b_replay/lowner_nstar.py 0.97` | exact first failing Löwner size (about 16 minutes per centre) |

Requirements: Node 18+, Python 3.11 with `mpmath` and `sympy`; `python-flint` 0.9.0 for the
v5.0 Arb certificate; a C compiler for the censuses.

## Licence

Research text, papers, figures and data: CC BY 4.0, attribution to Jeffery Lyn Huckstead /
Cerebral Graphix. The legacy engine code under `legacy/` is MIT (`LICENSE`). Third-party
material keeps its own terms (see `site/area-51/prospect-51/THIRD_PARTY_NOTICES.txt`).

## Citation

See `CITATION.cff`. Paper DOIs: TN Postmaster Volume I concept
[10.5281/zenodo.21968915](https://doi.org/10.5281/zenodo.21968915) (v5.2 =
[10.5281/zenodo.23004335](https://doi.org/10.5281/zenodo.23004335), reserved; v5.1 =
10.5281/zenodo.22844194); the Area 51 games and exhibit research are in *Project 51: Reading the
Record Across Rules*, [10.5281/zenodo.23004789](https://doi.org/10.5281/zenodo.23004789) (reserved); The Line Game concept 10.5281/zenodo.20792808 (latest record
[10.5281/zenodo.23004800](https://doi.org/10.5281/zenodo.23004800), reserved; v7.5 = 10.5281/zenodo.22943070); Project 51 concept 10.5281/zenodo.22862811 (v0.4 =
10.5281/zenodo.22985771).
