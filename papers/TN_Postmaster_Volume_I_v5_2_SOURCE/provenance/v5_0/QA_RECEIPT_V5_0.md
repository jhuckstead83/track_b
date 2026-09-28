# QA receipt — Triangular-n Postmaster, Volume I, v5.0

**17 September 2026. RH STATUS: OPEN.**

No theorem status changed in this edition. W₁ analytic; W₂–W₆ A-CAT from the
source; W₇ / F^(14) open; the verified-height prefix up to
K_H = 4,712,664,392,502 is a separate zero-assisted channel.

## 1. Delivered artifacts

| artifact | pages | SHA-256 |
|---|---:|---|
| `TN_Postmaster_Volume_I_v5_0_READING_VOLUME.pdf` | 98 | `3fbc34457cc2e7912e59213555f4a186bab468b16c01563ad622a1cf8abf7453` |
| `TN_Postmaster_Volume_I_v5_0_TECHNICAL_DOSSIER.pdf` | 279 (276 + 3 facsimile) | `9f86bd39f60a513180b5a2f640c35a33cb3fd521e4d2deed35b7341b6cdf9a25` |

Predecessor package: v4.9,
`82b64968ab3e45a301357211af88d63fa67d0f5e0d51ad1adc4ecb0d7bb0a382`.
Both PDFs are published beside the package on the same Zenodo record (concept
DOI 10.5281/zenodo.21968915) and bound by hash in `PACKAGE_MANIFEST.json`.

## 2. Gates

| gate | result | previous edition |
|---|---|---|
| `qa/audit_v50_updates.py` | 300 / 300 | 297 / 297 |
| `qa/verify_v50.py --pdf-dir output/pdf` | 76 / 76 | 71 / 71 |
| `qa/replay_math.py` | 16 / 16 runners, 220 s | 14 / 14 |
| undefined references | 0 / 0 | 0 / 0 |
| missing characters | 0 / 0 | 0 / 0 |
| overfull boxes over 30 pt | 0 / 0 | 0 / 0 |
| pages against ceiling | 98 ≤ 99, 279 ≤ 299 | 96, 279 |

The audit is idempotent: `qa/V50_FIGURE_BASELINE.json` holds the **incoming**
v4.9 figure state and is not rewritten by the audit, so repeated runs from this
package give the same answer. The current state is written to
`qa/V50_FIGURE_STATE.json`.

## 3. New this edition

### 3.1 `qa/audit_r10c_orbit.py` — exact replay of §R10C and (155A.4a)

`e2117b6c78d10a19…`, 2.75 s, 14 / 14 checks, `qa/R10C_ORBIT.json`.

Exact arithmetic throughout: `fractions.Fraction` and sympy over **Q**. No
floating-point comparison occurs anywhere in this replay.

| check | content |
|---|---|
| R7 tie-out | `1/q = 2 + z_C + 1/z_C`; `w = −1/z_C`; hence `1/q = 2 − w − 1/w` |
| recurrence | `Q_0=0, Q_1=y, Q_{n+1}=2y+(2−y)Q_n−Q_{n−1}` reproduces `2 − wⁿ − w⁻ⁿ`, n ≤ 16 |
| printed rows | (10C.5) and (10C.9) agree with the recurrence |
| square forms | `Q_{2m+1}=y𝒫_m²` and `Q_{2m}=y(4−y)ℬ_{m−1}²`, with 𝒫_m reached twice — by the (155A.1) recurrence and by the closed coefficient formula (155A.2) |
| interval | `y ∈ (0,4] ⟺ |w| = 1`, at exact rational sample points, with the characteristic roots' modulus computed symbolically |
| calibration | `t=√2`: `q=9/4`, `y=4/9`, `w=(7−4√2i)/9`, `|w|²=1`, `Re w=7/9`; rungs Q₁…Q₈ as exact rationals, each computed three independent ways (recurrence, `2−2T_k(7/9)`, square form); odd rungs are rational squares, even rungs are not |
| document tie | the two volumes print the statements this replay certified |

Calibration values of record: `Q₁ = 4/9 = (2/3)²`, `Q₂ = 128/81`,
`Q₃ = 2116/729 = (46/27)²`, `Q₄ = 25088/6561`, `Q₅ = 232324/59049 = (482/243)²`.

### 3.2 `qa/audit_figure_claims.py` — the check for claims that are pixels

`ba1173d03accbbf7…`, 55 s, PASS on 85 cited figures, 0 orphans.

Through v4.9, figure 75's status panel disagreed with the controlling table of
§R12 and no gate could see it, because the claims were rendered text. This
audit closes that class of defect:

1. every cited figure exists and is pinned by SHA-256 against
   `qa/V50_FIGURE_CLAIMS.json`;
2. forbidden-claim patterns run over the recorded OCR text — a superseded
   source-rung range, `W₅` described as zero-assisted, `W₅: source proof OPEN`,
   `F^(10)` named as the next jet, or any volume-edition stamp;
3. the same patterns run over **live** OCR when tesseract is present, and the
   recovered text must match the recorded text;
4. a figure bundled but cited by neither volume fails the audit;
5. the ledger printed in the generated panels is tied back to the §R12 table,
   read out of the Reading Volume source at run time, including K_H.

Recorded with tesseract 5.3.4, `--psm 11`. Without tesseract the audit still
runs checks 1, 2, 4 and 5 from the recorded text and says so in its output.

### 3.3 Figure provenance

`qa/figsrc/` grew from one generator to four. Every figure this edition added or
redrew is now reproducible from bundled source, and the audit requires that:

| figure | generator |
|---|---|
| `figure75_li_pp97_loewner_study_atlas.png` | `fig_status_panels.py` |
| `v26c_source_depth.png` | `fig_status_panels.py` |
| `v30_rh_equivalence_map.png` | `fig_status_panels.py` (title band only, repainted from the archived original) |
| `figure75A_r10c_one_orbit_four_coordinates.png` | `fig_one_orbit_four_coordinates.py` |
| `figure74_safe_axis_and_self_dual.png` | `fig_safe_axis_and_self_dual.py` |

`fig_status_panels.py` declares the rung ledger **once**, transcribed from §R12,
and both status panels derive from it. `--check` re-emits and compares bytes.

Seven figures were retired: the four-panel fold atlas (its first two panels are
now drawn for a moving orbit by the §R10C figure), one decorative geometry
figure whose identity is stated algebraically in §R1A, and five figures that
were bundled but cited by neither volume. All seven are archived by hash under
`provenance/v50/pruned_figures/` and recorded in `PRUNED.json`.

## 4. What the documents gained

- Reading Volume **§R10C**, "One orbit, four coordinates", with one figure.
  Nothing in it is new mathematics; every identity was already available in the
  volume, and the section states them in one place with one firewall paragraph.
- Reading Volume §R7 and §R15 gained cross-references to it.
- Dossier **(155A.4a)**, the diagonal specializations of the two product
  identities already proved in §155A, marked as a restatement.

## 5. Environment

Python 3.11.15, python-flint 0.9.0 (Arb), mpmath 1.3.0, SymPy 1.14.0,
matplotlib 3.10.9, Pillow 12.2.0, tesseract 5.3.4, pandoc 3.1.3,
pdfTeX 3.141592653-2.6-1.40.25 (TeX Live 2023/Debian). `SOURCE_DATE_EPOCH` is
fixed by the build. `qa/ENVIRONMENT.json` records the build environment;
`qa/MATH_REPLAY_LEDGER.json` records every replay with its script hash.

PDF bytes depend on the TeX installation. The source-rung certificate scripts
and `qa/verify_package.py` need only CPython except `source_rungs_arb.py` and
`audit_gamma_bridge.py`, which need python-flint, SymPy and mpmath;
`audit_figure_claims.py` uses tesseract when present.

$$\boxed{\text{RIEMANN HYPOTHESIS: OPEN}}$$
