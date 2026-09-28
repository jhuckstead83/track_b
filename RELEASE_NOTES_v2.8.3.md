# Cerebral Graphix v2.8.3 · Track B research merge

28 September 2026. Team B (Track B, Area 51). **Base: Fork-A v2.8.2** (Finance and homepage trace, archive SHA-256 `81d5a616…0262410`). This release places the Track B research pass on that base. **RH STATUS: OPEN.**

It changes no Finance file, no homepage or hero file, and no game logic. The only script edits are status and label strings in the SEDAPS page, and one comment in the SEDAPS lemma file. It changes no TN Postmaster v5.1 or v5.0 file. Like its inputs, the full-site archive omits `papers/`; the updated `TN_Postmaster_Volume_I_v5_2_SOURCE.zip` ships beside it, to be placed in `papers/` when that folder is restored. `MERGE_GUIDE_v2_8_3.md` gives every file's before and after SHA-256, and `MANIFEST_v2_8_3.json` records the same delta in the Fork-A manifest format.

## Version numbers

- There is one v2.8.1: Fork-A's. It is kept unchanged (`RELEASE_NOTES_v2_8_1.md`, `MANIFEST_v2_8_1.json`, `VALIDATION_v2_8_1.json`), and so is Fork-A's v2.8.2.
- Track B's pass was drafted under the working label "v2.8.1" on 27 September. That label was never released, and this release replaces it. The Blue Team notes PP271–PP276 refer to that draft.
- `area-51/research.json` now reads `site_version: 2.8.3`.
- The shipped notes for v2.8.0 are left exactly as released. The corrections are recorded here.
- One build artifact was removed: `research/project-51/formula51/__pycache__/derive51.cpython-312.pyc`, which Fork-A's `MANIFEST_v2_8_1.json` listed as an added file. `__pycache__/` should be excluded from future packages.

## Merge with Fork-A's research pass

Fork-A's v2.8.1 had already revised nine of the files Track B touched. Both sets of edits are kept.

| Area | Kept from Fork-A | Added by Track B |
| --- | --- | --- |
| SEDAPS page | "Apply 17-card start + turn 85"; the Finance asset links; the "occurs at turn 84" wording | the turn-count note, turns 24/27/30/33, links to v0.4.1 |
| SEDAPS research note v0.4 | "known elapsed turn count 85" | table qualifiers, the War theorem, the lemma's scope |
| 51 Twins plates and calibration | "detected negative", "earlier sampled tests", the verifier's scope, sector-safe rungs conditional on the census | the Gamma factor, the 60/100-digit replay, the exact Löwner sizes, the War period, the new ledger rows |
| Formula 51 | its §3 repair (bounds on c) | the K/c proof, the correction note, §6, PP274's characterisation wording |

After the merge, the Twins data was rebuilt and checked (`verify-twins-v1.cjs`), and so was the page (`build-twins-page-v1.cjs`). Neither side's `index.html` was trusted.

## 51 SEDAPS v0.4.1

**The turn count is part of the filter (CERT + COMPUTED; Blue Team A-CAT).**
- v0.4 excluded past 10 of the turn-85 present by a search at turn 84 only.
- A search at every elapsed turn shows that fair 17–17–17 deals reach past 10 at turns 24, 27, 30 and 33, and at no other turn.
  - The four turns are frozen certificates (`past10-certificates-v0-4-1.json`).
  - The other turns are excluded by complete searches. The verdict is 3-periodic from turn 82 on.
- So, given the turn count, exactly one past comes from a fair deal: zero history bits. Without the turn count, two pasts survive and the leading bit decides.
- Independent returns:
  - Team B ran a Python restatement of the search.
  - PP274 replayed the four certificates.
  - PP275 ported the search separately and reproduced the turn-84 exclusion exactly: 336 states expanded, lowest turn 66, not capped.

**Why the search is a proof (PROVED, new §1.1).**
- A theorem, with its hypothesis stated: for a start state with at least two live queues, an uncapped search that finds no deal proves unreachability.
- The proof has two parts: (a) the predecessor list is complete, and (b) the shape test is necessary on reached states with at least two live queues.
- PP276 audited both parts. It replayed 5,355 emitted predecessors and found none spurious, missing or extra.
- **Scope correction (PP275).** The lemma header said "a state failing the test at turn s is unreachable at turn s". That is false for terminal states, which are reachable yet fail the test by construction.
  - The header now carries the scope. The code is unchanged.
  - A new verifier check replays the scope over 2,000 seeded deals. All 9,949,705 pairs with at least two live queues pass, and exactly the 348 terminal states fail.

**Exact history counts (new §1.2; answers Fork-A's work packet A).**
- Below turn 17, a three-live state that passes the shape test is reached by exactly t!/(a! b! c!) deals, where a, b and c are its queues' packet counts (PROVED). So the shape test is also sufficient there.
- Above turn 17 the tree is searched, and the formula closes it.
  - The turn-32 present is reached by exactly **484,731,472** deals. Its four pasts account for 77,014,080, 179,358,976, 24,504,480 and 203,853,936.
  - The turn-85 present is reached by 69,150,842,132 deals, all through past 00.
- A deal-by-deal enumeration, with no formula, matches it in five cases, up to 24,504,480 deals (`count-histories-v0-4-1.cjs --brute`).
- A longer enumeration also confirms three of the four turn-32 pasts deal by deal (77,014,080, 179,358,976 and 24,504,480), and past 00 of the turn-35 present (54,493,296). The fourth turn-32 past exceeded its 600-million-state cap.

**The n + 1 period, for loops with two live queues (PROVED).**
- With two queues left, the rule is War with the winning card first. For odd decks its loops alternate winners (Spivey, *Cycles in War*, INTEGERS 2010, Thm 6).
- Alternation forces L = 2·lcm(α/2, (n+1)/2, (n−1−α)/2), a multiple of n + 1.
- At 51 cards the formula allows exactly the 12 observed lengths. Their gcd is exactly 52.
- Complete censuses of every state:
  - 3 queues through 11 cards (3.11 × 10⁹ states);
  - 2 queues through 12 cards;
  - the counts reproduce OEIS A400411.
- None of them finds a loop with three live queues.
- This answers Fork-A's work packet B for two-live loops. The census extends Fork-A's n = 3, 5, 7 to n = 11.
- v0.4's "every odd deck size tested (7 to 51)" was an overstatement: 12 sizes were sampled.

**Loops that keep three queues live exist at 12 cards (new, CERT).**
- Every state of such a loop is in packet form. The proof is short: a loop can never be shorter than any of its queues, because the cards are distinct. So a search over packet-form states covers the whole state graph.
- That search, `independent/live3_loops.c`, finds none for n ≤ 11, in agreement with PP281's unrestricted census.
- At n = 12 it finds 1,145,664 loops: 1,036,800 of length 9 and 108,864 of length 60. The smallest is A = 6 0 1, B = 2 10 7 3, C = 4 8 11 5 9, whose winners rotate A, B, C.
- **No equal deal reaches them.**
  - On a three-live turn all three sizes shift by −1 mod 3, so pairwise congruence is invariant.
  - Equal deals start congruent, and every n = 12 loop is incongruent.
  - Two exhaustive checks confirm it: the packet-form search restricted to congruent sizes, and PP282's unrestricted walk of 3.03 × 10⁹ states.
  - PP282 found the same loops independently.
- So the ledger carries two claims. "No three-live loop in the state graph" is false at 12. "None reachable from an equal deal" holds through 12 and is OPEN at 51.
- A census of 1.8 × 10⁹ states at n = 11 found no loop, and the next size has more than a million. That is a checkable example of the firewall: a finite search is not an all-n theorem.

## 51 Twins and the calibration report

- **Gamma factor.** The Davenport–Heilbronn twin shares the reflection F(s) = F(1 − s) of completed zeta, but not its Gamma factor: Γ((s+1)/2) and conductor 5 are those of an odd character. The plate's (5/π)^(s/2) normalisation differs from the textbook (5/π)^((s+1)/2) by a constant that cancels in both the reflection and the log-derivative. A footnote now says the choice is deliberate.
- **Rung signs.** The negative at k = 16,589 was detected on a finite list of the twin's zeros. An independent replay at 60 and 100 digits reproduces both signs, and both are stable under 10⁻¹² shifts of the zeros (`evidence/dh_twin_highprec.py`). This is still EVID, because the census and its tail are not certified. Fork-A's work packet C remains open.
- **Löwner sizes, now exact.** One elimination per centre reads every leading pivot at 250 digits, which pins the first failing size exactly:
  - N\* = **105** at 0.97|q₀|;
  - N\* = **106** at |q₀|;
  - N\* = **107** at 1.03|q₀|.
  - The pivots at the tested sizes reproduce the Dossier's printed values.
  - A second run at 320 digits, with 2,560 contour points and radius 0.70 x₀, gives the same negative pivot at each centre, and every printed pivot agrees to six digits.
  - Positivity is still established only at these three centres.
- **Finite prefixes.** "So no finite rung prefix decides RH" is replaced by "a long finite rung prefix does not by itself rule out off-line zeros".

## Formula 51

- **§3 repair.** Three independent repairs agree: Team B, PP272 and Fork-A. The conclusion N ∈ [1428, 1455] stands, and it is kept distinct from the band K = 51 ⇔ N ∈ [1177, 1764].
- **The failure count of the old step, with its range.** The old step fails for 486 radices in [588, 11172], or 513 in [1, 11172].
- **Independent recomputation.** `f51_independent.py` reproduces all 588 band tables without `derive51.py` or `unicodedata`. It also replays PP270 §4.1 and §4.2; PP274 grades both A-CAT.
- **PP274's additions.**
  - The balanced condition in one line: ⌊(N − 1176)/28⌋ = (N mod 28) − 1.
  - The seven-class picture fails at N = 1428 and N = 1429.
  - The uniqueness of 1438 is a property established in September 2026, not a record of how the radix was chosen.

## Papers of record

- The Line Game page links v7.5 (10.5281/zenodo.22943070) beside v7.2.
- The Project 51 page links the 27 September deposit (10.5281/zenodo.22985771): Project 51 v0.4, Telescope 51 v0.7 and the Formula 51 concise method. The PDFs are added to the site.
- The citation catalog gains both records. Its stale line "v5.1 does not yet have its own deposit" is corrected: v5.1 is 10.5281/zenodo.22844194.
- These DOIs come from the Blue Team's DataCite check (PP270) and the record archives. Zenodo itself was not reachable from this session.
- `site-index.json` now records the Line Game concept DOI, 10.5281/zenodo.20792808, beside the TN Postmaster one. The catalog already had it; PP281 withdrew PP278's "not recorded". Pointing the 144 "current version" references at the concept DOI is left for a separate pass, because each one needs a reading.
- The SEDAPS DOI placeholder moved to the current note: `data-doi-pending="sedaps-51-v0-4-1"` now sits on `RESEARCH_UPDATE_v0_4_1.md`. See `ZENODO_RELEASE_PLAN_v2_8_3.md`.

## TN Postmaster Volume I v5.2 (source edition)

- **Wording corrections in the Markdown masters.**
  - the Gamma factor;
  - "detect the twin" instead of "separate zeta from the twin";
  - the Löwner sizes, now with the exact N\*, and the tested centres;
  - finite prefixes.
- **What did not change.** No number, tag, status mark or reference. `qa/check_v52_interface.py` passes 67/67 and was not modified.
- **New evidence.** `provenance/v5_2/evidence/team_b_replay/` holds:
  - the 60/100-digit rung replay;
  - the exact Löwner computation with its three receipts.
- **Unchanged files.** The v5.1 and v5.0 provenance files are byte-identical.
- **Still for the author.** The Blue Team's question on the Reader's page ceiling, 99 or 101: the source README, the editorial delta and `qa/check_v52_interface.py` (`('READING', 101)`) all use 101, and the Dossier is ungated. Also still open: the four-W disclaimer, the DISCLOSED REPLAY clause, Project 51's reference [5], and which limit the 512-page union answers to. None was changed here.

## Deep history

- **v0.5 synthesis.** The synthesis layer of TN Postmaster Research Volume I v0.5 (10.5281/zenodo.21968858) replays 13 of 13 identities, and its constant-Jacobian counterexample is confirmed. Its defects are cosmetic: three LaTeX typos and one mis-titled citation.
- **v5.0 certificates.** The source-rung certificates W₂–W₆ were re-executed, at the shipped parameters and at the second parameter set. Both backends reproduce their shipped receipts, apart from timing fields.
- **The Decimal backend's rounding label is correct.** `ROUND_FLOOR` describes its arithmetic, which takes upper bounds as −floor(−x). The printed tail ratio comes from a separate display helper that rounds upward (`ROUND_CEILING`). So the Arb and Decimal logs can differ by one unit in the last printed digit, by design. The cross-backend check compares exact rationals. PP281 withdrew PP277 §0's defect.

## Fork-A's work packets (FRONTIER_HANDOFF_v0_4.md)

| Packet | State after v2.8.3 |
| --- | --- |
| A — exact history counts at the turn-32 endpoint | **answered**: 484,731,472 deals, from a proved closed form below turn 17 and a complete search above it (SEDAPS v0.4.1 §1.2). |
| B — odd-deck periods | answered for loops with two live queues: the period formula is PROVED, and alternation is published. Three-live loops exist at n = 12, but no equal deal reaches them. Odd n ≥ 13, and n = 51, are open. |
| C — twin certification at k = 16,589 | open. The 60/100-digit replay and the 10⁻¹² perturbation test are stronger numerical evidence, but not zero enclosures or a tail bound. |
| D — publication follow-through | the v5.2 PDFs were built on 28 September from this source: Reader 101 pages, Dossier 287 pages, and the interface check passes 74/74 with the build receipts. They ship in v2.8.4, together with the retarget of the site to v5.2. All DOI placeholders remain pending. |

## Verification

See `VALIDATION_v2_8_3.json`.

The local link check covers all 60 HTML pages and 910 local references. References into `papers/` are counted, not skipped: there are 140 of them, to 28 targets. They can be checked only once `papers/` is restored, and two of them point at the v5.2 source zip that ships beside this archive. Seven other references do not resolve, and all seven predate this release: three relative links in homepage snippet templates and four false positives inside minified scripts. The merge added 10 local references, and all of them resolve.

Rendered checks were run in Chromium at 1280 × 900 and 375 × 812 on the changed research pages. No page showed horizontal overflow or a page error. The only failed requests were the live Finance feed and a Google Sheet, which this environment's network policy blocks. Fork-A's Finance and homepage files are byte-identical to v2.8.2.
