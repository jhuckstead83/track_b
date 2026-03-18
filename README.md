# Transient Rational Locking in Modular Logarithmic Orbits

This repository studies the arithmetic dynamics of transient rational locking in modular logarithmic orbits. It shows that apparent geometric skeletons observed in modular projections are not fundamental structural properties of the constants themselves, but rather predictable transient shadows of rational approximants to logarithmic rotation numbers.

Their visual persistence is governed by a torus-sawtooth dephasing law, and their visual clarity is dictated by the arithmetic commensurability of the rendering modulus.

The fog resolves not into metaphysics, but into mechanics.

While **Track A** establishes the mechanism (**Part I**), **Track B** develops the taxonomy (**Part II**). This repository contains the computational engine used to mine these resonances, filter mathematical redundancies, and classify the survivors into a strict “Standard Model” of Diophantine archetypes.

## Quickstart

```bash
pip install -r requirements.txt
python track_b/run_quarry.py
```

Outputs, including the master taxonomy ledger and automated visual case cards, are written to:

```text
track_b/quarry_output/
```

## Repository Architecture

The project is divided into two wings:

- **`paper/`**: manuscripts (Part I and Part II), publication figures, and Overleaf-ready LaTeX source
- **`track_b/`**: a modular Python survey engine that mines, fingerprints, and ranks constant pairs into canonical classes

## Structural Laws

The framework is governed by four core laws, which the Track B engine uses to collapse redundant observations into single **canonical forms** \(\mathcal{C}\):

1. **Torus-Sawtooth Dephasing Law**  
   The orbit shadows a rational carrier with a phase error that follows a periodic wraparound cycle on the torus.

2. **Modulus as Lens, Not Composer**  
   The discrete modulus acts only as a rendering grid. It amplifies or blurs intrinsic geometry based on divisibility, but composes none of it.

3. **Inversion Theorem**  
   Inverting the numerator constant preserves the lock scale, sector count, and geometric stability of the original orbit, up to observation-equivalence.

4. **Base-Shift Identity / Phase Equivalence**  
   Presentations that yield the same torus phase increment, or its inversion,
   \[
   \rho_2 = \pm \rho_1 + k, \qquad k \in \mathbb{Z},
   \]
   are phase-equivalent shadows of the same canonical class.

## The Taxonomic Engine

The `track_b` pipeline does not merely hunt for pretty pictures. It is a theorem-aware engine that separates:

- **intrinsic toral persistence**, governed primarily by \((q, \varepsilon)\)
- **extrinsic rendering commensurability**, governed by the \(M\)-profile

Each survivor is assigned a canonical signature of the form:

```text
C = (q, delta, M-profile, Sym, EqTags) | Archetype: ...
```

The engine currently uses an operational classifier on the standard composite rendering family \(\{120, 360, 720, 840, 990\}\).

## Visual Archetypes

Three extreme archetypes anchor the taxonomy:

- 🛕 **Cathedral Square**  
  Low spatial frequency (\(q \le 10\)) with perfect or near-perfect rendering alignment. Wide, highly legible sectors and strong visual charisma.

- 🦕 **Behemoth**  
  High spatial frequency (\(q \ge 15\)), exact or near-exact commensurability with the rendering lens, and ultra-low dephasing error. Massive, complex structures that survive for very long iteration windows.

- 👻 **Ghost**  
  High spatial frequency (\(q \ge 15\)) but strongly mismatched to the rendering lens. The toral lock is mathematically strong, but visually aliased on standard composite grids.

## Standard Model of Transient Rational Locking
### First Census

Running the engine across the standard constant registry yields an irreducible canonical survivor set. When plotted in the phase space of spatial resolution (\(q\)) versus temporal stability (\(N_{\mathrm{lock}}\)), a Dirichlet-shaped survivor floor emerges.

| Canonical Pair | Carrier (\(p/q\)) | \(N_{\mathrm{lock}}\) | \(\mu_{720}\) | \(\mu_{990}\) | Archetype |
| :--- | :--- | ---: | ---: | ---: | :--- |
| **`catalan` vs `log3`** | \(1/15\) | 62,845 | 0.00 | 0.00 | **BEHEMOTH** |
| **`euler_gamma` vs `sqrt11`** | \(13/24\) | 55,388 | 0.00 | 0.25 | **BEHEMOTH** |
| **`catalan` vs `ln_phi`** | \(3/25\) | 266,036 | 0.20 | 0.40 | GHOST |
| **`log2` vs `pi_over_4`** | \(15/29\) | 185,401 | 0.17 | 0.14 | GHOST |
| **`ln_phi` vs `phi`** | \(12/25\) | 83,732 | 0.20 | 0.40 | GHOST |
| **`log2` vs `pi_over_3`** | \(1/19\) | 74,998 | 0.11 | 0.11 | GHOST |
| **`silver_inv` vs `sqrt5`** | \(19/21\) | 54,630 | 0.29 | 0.14 | GHOST |
| **`catalan` vs `log10`** | \(17/19\) | 50,815 | 0.11 | 0.11 | GHOST |
| **`sqrt7` vs `two_pi`** | \(9/17\) | 47,531 | 0.35 | 0.24 | GHOST |
| **`pi_over_3` vs `sqrt11`** | \(1/26\) | 283,670 | 0.31 | 0.08 | STANDARD TRANSIENT |
| **`log10` vs `sqrt11`** | \(16/23\) | 66,297 | 0.30 | 0.04 | STANDARD TRANSIENT |
| **`sqrt5` vs `silver_inv`** | \(2/23\) | 65,532 | 0.30 | 0.04 | STANDARD TRANSIENT |
| **`log3` vs `catalan`** | \(13/14\) | 54,744 | 0.43 | 0.29 | STANDARD TRANSIENT |
| **`pi_over_2` vs `e`** | \(14/31\) | 33,114 | 0.23 | 0.06 | STANDARD TRANSIENT |

> Exact permanent locks, such as `e_over_pi` vs `pi_over_e -> 0/1`, are treated as **Vacuum States** and filtered from the transient taxonomy by the theorem-aware separator.

## Canonical Outputs

The Track B engine emits:

- raw phase data: `rho`, `best_p`, `best_q`, `delta`, `n_lock`
- rendering diagnostics: `mu_120`, `mu_360`, `mu_720`, `mu_840`, `mu_990`
- canonical metadata: `sym_class`, `eq_tags`, `canonical_signature`
- operational archetype classification: `CATHEDRAL SQUARE`, `BEHEMOTH`, `GHOST`, or `STANDARD TRANSIENT`

Primary output files include:

```text
track_b/quarry_output/master_canonical_ledger.csv
track_b/quarry_output/filtered_unique_taxonomy.csv
track_b/quarry_output/featured_case_cards/
```

## Included Bundles

- `paper/Constants_Analysis_Part_I.tex` and compiled PDF (mechanism)
- `paper/Constants_Analysis_Part_II.tex` and compiled PDF (taxonomy)
- all Track B Python modules under `track_b/`
- packaging and documentation artifacts under `docs/` where applicable

## Publication Notes

- **GitHub Repository:** <https://github.com/jhuckstead83/track_b>
- **ORCID:** <https://orcid.org/0009-0007-0234-2177>

Please review author-display metadata before any Zenodo release or `CITATION.cff` finalization.

## Future Work

Natural next branches include:

- nonstandard rendering bases
- angle/circle inheritance scans
- zeta-family and logarithmic-family expansions
- semiconvergent-specific surveys
- phase-space visualization and “Standard Model” chart generation
