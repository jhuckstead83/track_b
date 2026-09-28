# v5.0 — publication delta

**17 September 2026. RH STATUS: OPEN.** One Reader bridge exposed, one stale
figure repaired, one new class of audit.

v5.0 claims no new RH implication. No theorem status changed. W₁ is analytic,
W₂–W₆ are A-CAT from the source, W₇ / F^(14) is open, and the verified-height
prefix remains a separate zero-assisted channel.

## 1. The bridge that was already there

Reading Volume §R7 has long carried

$$\frac1q = 2 + z_C + \frac1{z_C},\qquad z_C=\frac{s}{1-s},$$

and §R15 has long carried Li's coefficients in the coordinate
$w=1-1/\rho$. The two coordinates are one line apart — $w=-z_C^{-1}$ — but no
edition said so, and a reader met the resolvent pole in §R10 and the Li
sequence in §R15 with nothing between them.

**New §R10C, "One orbit, four coordinates,"** closes that gap. For one folded
orbit it puts $q$, the pole $-q$, the reciprocal $y=1/q$ and the Li coordinate
$w$ into one dictionary, notes that (7.2) rewrites as $1/q = 2-w-w^{-1}$, and
derives the recurrence

$$Q_0=0,\quad Q_1=y,\quad Q_{n+1}=2y+(2-y)Q_n-Q_{n-1}$$

so that the pole position alone generates the orbit's whole Li column. It then
states the interval $\Re\rho=\tfrac12 \iff q>\tfrac14 \iff y\in(0,4) \iff |w|=1$
and closes by citing the square factorizations of Dossier §155A.

Nothing in §R10C is new mathematics. Every identity in it was already provable
from material in the volume; what is new is that they are in one place, in one
order, with one figure.

**Dossier (155A.4a)** now prints the diagonal specializations of the two product
identities already proved there,

$$Q_{2m+1}(y)=y\,\mathcal P_m(y)^2,\qquad Q_{2m}(y)=y(4-y)\,\mathcal B_{m-1}(y)^2,$$

the second being the case $r=s=m-1$ of (155A.4). It is a restatement, marked as
one.

**New replay `qa/audit_r10c_orbit.py`** certifies the section in exact
arithmetic — no floating-point comparison anywhere in it. Fourteen checks: the
R7 tie-out, the recurrence against $2-w^n-w^{-n}$ to $n=16$, the printed rows,
both square forms with $\mathcal P_m$ reached twice (by the (155A.1) recurrence
and by the closed coefficient formula of (155A.2)), the interval, and a
calibration orbit at $t=\sqrt2$ where $q=9/4$, $y=4/9$, $w=(7-4\sqrt2\,i)/9$ and
the rungs are exact rationals computed three independent ways. It also checks
that the two volumes print the statements it certified.

## 2. The figure that had gone stale

**Figure 75's status panel disagreed with §R12 and had for two editions.** It
read `W₂–W₄ source A-CAT`, `W₅ zero-assisted`, `W₅: source proof OPEN / F^(10)
route`, and omitted W₆ entirely, while the controlling table said W₂–W₆ are
A-CAT from the source and the open source rung is W₇ ⇝ F^(14). Text QA could
not see it, because the claims were pixels.

A sweep of all 90 bundled figures found two more defects of the same kind, both
cosmetic: `v26c_source_depth` printed "v4.5 source frontier" although its table
was correct, and `v30_rh_equivalence_map` was titled "v3.0". Five figures were
bundled but cited by neither volume.

v5.0 repairs all of it and removes the cause.

- `qa/figsrc/fig_status_panels.py` regenerates figure 75 and the source-depth
  table from **one declared ledger**, transcribed from §R12; the equivalence
  map's title band is repainted from an archived original, so its eleven claim
  boxes are never re-transcribed.
- `qa/audit_figure_claims.py` is a new audit. It pins every cited figure by
  SHA-256, runs forbidden-claim patterns over its recorded OCR text, re-runs OCR
  when tesseract is present, fails on any figure the documents do not cite, and
  ties the printed ledger back to the §R12 table read out of the source at run
  time. It is the check that would have caught this.
- `qa/audit_v50_updates.py` gained the declared figure delta: the set of figures
  added, retired and redrawn in this edition is named in the audit, and anything
  else fails. The incoming baseline is not rewritten, so the audit answers the
  same way every time it is run from this package.

## 3. Figures added and retired

| figure | action |
|---|---|
| `figure75A_r10c_one_orbit_four_coordinates.png` | added, generator bundled — the §R10C picture |
| `figure74_safe_axis_and_self_dual.png` | added, generator bundled |
| `figure74_s_sigma_it_fold_atlas.png` | retired; its first two panels are now drawn better, and for a moving orbit, by §R10C's figure |
| `v29_even_triangle_geometry.png` | retired; the identity it drew is stated algebraically in §R1A |
| five uncited figures | retired |
| `figure75`, `v26c_source_depth`, `v30_rh_equivalence_map` | redrawn |

Every retired figure is archived under `provenance/v50/pruned_figures/` and
recorded by hash.

## 4. Gates

audit 300/300 (was 297), verifier 76/76 (was 71), replays 16 (was 14), 0 undefined
references / 0 missing characters / 0 overfull boxes in both volumes.

Pages 98 / 279 against targets 90 / 275 and ceilings 99 / 299. The Reading
Volume gained two pages net: §R10C and its figure, less the two retired
figures.

$$\boxed{\text{RIEMANN HYPOTHESIS: OPEN}}$$
