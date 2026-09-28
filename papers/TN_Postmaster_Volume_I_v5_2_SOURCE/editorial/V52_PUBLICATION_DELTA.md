# TN Postmaster Volume I — v5.1 → v5.2 publication delta

27 September 2026. Prepared by Team B for the author. `RH STATUS: OPEN`. No status was
promoted, and no inherited status row changed. The check `qa/check_v52_interface.py`
enforces the row-level preservation.

## 1. What v5.2 adds

| where | what | status |
|---|---|---|
| Dossier §69A | The Davenport–Heilbronn twin: definition, the c(n) of −f′/f against Λ(n), a census to height 640 (501 on-line zeros, 16 off-line pairs), the sector bound k ≤ 218, first failure W₁₆₅₈₉(7140.066) < 0, the per-zero table of first failing rungs, and Löwner/Dobsch PSD through N = 100 with failure by N = 105 at 250 digits | Theorem 69A.1 (some rung fails) \PROVED{}; all numbers \EVID{} |
| Dossier §69B | Lemma 69B.1, parity (TW.1); Proposition 69B.2, the local Gaussian form (TW.2); the detection law (TW.3), k* ≈ 1.3·t²/(aδ) | (TW.1), (TW.2) \PROVED{}; (TW.3) \EVID{} |
| Dossier §69C | Theorem 69C.1, orientation annihilation; Theorem 69C.2, compact Euler-ray instability. Both are restored from v0.3 [124], where they were proved; they were absent from v0.4 to v5.1 | \PROVED{} [124] |
| Dossier §67, §69, §159, abstract, chapter table, summary | W₇ ranked against the twin; two §69 bullets; the [121] attribution; v5.2 wording | editorial |
| Dossier references | [66] title corrected, and the v2 88.76% note added; new entries [121] Alpöge–Furman, [122] Davenport–Heilbronn, [123] Spira, [124] v0.3 | [121] read at abstract level only, as the list states |
| Reader abstract, (R.2) paragraph | The twin result stated where the live pair is ranked | inline \PROVED{} and \EVID{} |
| Reader status key | Three rows: (TW.1) \PROVED{}; the twin fails some rung \PROVED{}; the twin numbers \EVID{} | as listed |
| Reader §R25 | Two NO-GO rows: the v0.3 firewalls (§69C), and the functional-equation twin (§§69A–69B) | unconditional theorems |
| Reader [66] | Title corrected to "simple **and** on the critical line", as in the arXiv title | correction |
| Reader version notes | The v5.1 and v5.0 notes are replaced by one v5.2 note. The old notes remain in `provenance/v5_1/` | editorial |

New equation tags are TW.1, TW.2 and TW.3, all in the Dossier. Tags are global, so the Reader
cites (TW.1) and (TW.3) without redefining them.

## 2. Corrections carried in this edition

1. **Reference [66].** The v5.1 title read "simple *or* on the critical line". The arXiv title
   says "simple *and* on the critical line". Its v2 adds a separate result: at least 88.76%
   of the zeros are simple *or* on the critical line. The paper re-proves the unconditional
   two-thirds theorem of Alpöge and Furman (arXiv:2608.13637), which v5.1 did not cite.
2. **PP199's twin zero** (Dossier §69A). The point 1.10078201 + 86.14311231i with
   |f| ≈ 10⁻³⁰ does not reproduce: |f| = 0.576 under the standard normalization, and 0.931
   with κ's sign reversed, which also breaks the functional equation. The census has no zero
   with σ > 1 below height 640.
3. **The "k*θ² ≈ constant" reading** from earlier Team B notes is superseded by (TW.3): on
   the same planted pairs it spreads over a factor of 71.
4. **Team B's own median.** The median ratio over the 15 resolved twin zeros is 0.806
   (printed as 0.81). The earlier "0.83" left out zero 10's separately computed k*.

## 3. Open points for the author

1. **Disagreement with the Blue Team (PP270 §6).** PP270 restates "`W₇` via `F^(14)` from the
   source is the frontier." v5.2 keeps W₇ OPEN and keeps (R.4) as \EQUIV{}. It adds that the
   twin, which has no Euler product, passes W₇ and every computed rung through W₁₆₅₈₈, so a
   source proof of W₇ extends a finite prefix rather than separating ζ from the twin. The
   two readings do not contradict each other on status, but they rank the frontier
   differently. The author should decide which ranking the program carries forward.
2. **Theorem 69A.1 is marked \PROVED{}.** Its proof is that the argument behind (R.4) uses only
   the absolutely convergent folded resolvent together with Widder's characterization, and no
   Euler product. Please confirm this against the Dossier's proof of (R.4) before publication.
3. **Löwner N\*.** Only multiples of 5 were tested, so the first failing size at the best
   centre lies in 101–105. *Team B, 27 Sep:* `team_b_replay/lowner_nstar.py` reads every leading
   pivot of one elimination, which pins N\* exactly: 105, 106 and 107 at the three centres;
   see its receipts.
4. **The census is not interval-certified.** The implication "k ≤ 218 ⇒ positive" is proved.
   The value of θ_max rests on the computed census.
5. **The 40-digit Colab values** (W₁₆₅₈₈ = +1.7592739e-4, W₁₆₅₈₉ = −4.6600915e-5) were read
   from the Drive copy of the notebook. The pasted Colab output confirms −4.6601e-5, and the
   local double-precision scan agrees, but the 40-digit lines themselves are a transcription.
   *Team B, 27 Sep:* an independent 60- and 100-digit replay on the same zero list gives
   +1.759274e-4 and −4.660091e-5 (`team_b_replay/`), so the transcribed values are confirmed.
6. **Entry [121]** was read at abstract level only, as the Dossier's list says.
7. **"The first four off-line zeros agree with Spira [123]"** (§69A) compares against the
   published values as they are known from the literature. Spira's paper itself was not
   reopened for this package. Check the four values against his table before publication.

## 4. Page budget (Reading Volume ≤ 101 pages)

v5.1's Reader was 101 pages. Its layout matters here: chapters flow continuously
(`\titleclass{\chapter}{straight}` with `\Needspace{17\baselineskip}`), and tables are set
in `\scriptsize`. The space left at the end of each region was measured from the published
v5.1 PDF:

| region (v5.1 pages) | space left before the next forced break | v5.2 change |
|---|---|---|
| Start here → Reader's study spine (5–12) | about 170 pt on p. 12 | +11 prose lines and +3 table rows, offset by −14 prose lines in the version notes: about 0 |
| Parts VII–VIII (88–93) | about 73 pt on p. 93, plus about 160 pt on p. 94 before References must break | +2 table rows in §R25, about 70 pt |
| Summary (94) | about 160 pt | −1 line |
| References (95–101) | under 1 line on p. 101 | 0 lines: the [66] title fix is length-neutral, and entries 121–124 are in the Dossier only |

On that measurement, the expected Reader length is 101 pages. The earlier draft, with a full
§R25A in the Reader and the new references, came to about 104. Its content now lives in the
Dossier.

The Dossier has no stated ceiling. It grows by about 300 lines (§§69A–69C and the
references), roughly 6 pages on v5.1's 281.

Both counts depend on the toolchain. v5.0 used pandoc 3.1.3 with TeX Live 2023, and v5.1 used
TeX Live 2025. `qa/build_baseline_v51.py` rebuilds v5.1 in the current environment, so the
count can be compared like-for-like.

## 5. Not changed

- Every v5.1 equation tag, status marker, status row and reference number is preserved.
- The v5.0 interval certificates were not rerun.
- The figures are unchanged.
- Nothing has been deployed or deposited.

## 5. Team B wording corrections (27 September 2026)

The same day, a Team B pass tightened four statements without changing any number, tag, status
mark or reference. `qa/check_v52_interface.py` still passes 67/67 unchanged.

1. **Gamma factor.** The twin shares the reflection F(s) = F(1 − s) of completed zeta, but its
   Gamma factor is Γ((s+1)/2), that of an odd character, with conductor 5. Earlier wording said
   it had "zeta's functional equation and Gamma factor".
2. **Finite prefixes.** "So no finite rung prefix decides RH" and "cannot by itself tell ξ from
   the twin" overstated the calibration. The finite prefix W₁…W₁₆₅₈₉ does separate ξ from this
   twin. The corrected statement: a long finite prefix does not by itself rule out an off-line
   pair lying higher, or nearer the line, than the prefix can see.
3. **Löwner sizes and centres.** The sizes are first *tested* failures (steps of 5), and
   positivity holds only at the three tested centres. "Separate zeta from the twin" becomes
   "detect the twin": ζ's own Löwner sections at N ≈ 105 were not computed.
4. **Rung scope.** The rung values are computations on the finite zero list, now also replayed at
   60 and 100 digits.
