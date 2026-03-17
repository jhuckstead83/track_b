# Transient Rational Locking in Modular Logarithmic Orbits

This repository studies the arithmetic dynamics of transient rational locking in modular logarithmic orbits. It demonstrates that apparent geometric skeletons observed in modular projections are not fundamental structural properties of the constants themselves, but rather predictable, transient shadows of rational approximants to logarithmic rotation numbers.

Their visual persistence is governed by a torus-sawtooth dephasing law, and their visual clarity is dictated by the arithmetic commensurability of the rendering modulus.

The fog resolves not into metaphysics, but into mechanics.

## Quickstart

```bash
pip install -r requirements.txt
python track_b/run_quarry.py
```

## Repository Architecture

The project is strictly divided into two wings:

- **`paper/` (Track A)**: the frozen manuscript, publication figures, and Overleaf-ready source.
- **`track_b/` (The Quarry)**: a modular, vectorized Python survey engine designed to mine, fingerprint, and rank new constant pairs.

## Structural Laws

1. **Torus-Sawtooth Dephasing Law**: the orbit shadows a moving rational carrier with a phase error that follows a periodic wraparound cycle on the torus.
2. **Modulus as Lens, Not Composer**: the discrete modulus acts only as a rendering grid. It amplifies or blurs intrinsic geometry based on divisibility, but composes none of it.
3. **Inversion Symmetry of Spectral Fingerprints**: inverting the numerator constant preserves the lock scale, sector count, and geometric stability of the original orbit.
4. **Base-Shift Identity of Derived Numerators**: evaluating a derived ratio `(alpha/beta)` against its own denominator base `beta` reproduces the exact fingerprint of the bare numerator.

## Featured Exhibits

- **Flagship Octagon**: `e / pi -> 7/8`
- **Pentagon Respawn**: `sqrt(7) / (pi/sqrt(2)) -> 2/5`
- **Cathedral Square**: `catalan / sqrt(2) -> 3/4`
- **High-q Ghost**: `euler_gamma / pi -> 13/25`
- **Behemoth**: `sqrt(7) / pi -> 17/20`

## Included Bundles

- `paper/Constants_Analysis.tex` and compiled PDF
- all Track B Python modules under `track_b/`
- notes for inversion symmetry and base-shift identity
- uploaded publication packaging report files in `docs/`

## Publication Notes

- GitHub repository target: https://github.com/jhuckstead83
- ORCID provided by user: https://orcid.org/0009-0007-0234-2177

Please review author-display metadata before Zenodo release if you want a fully polished `CITATION.cff` with your preferred full name formatting.

## Future Work

A natural next branch is `future-work/nonstandard-bases` for angle/circle inheritance, zeta-family expansions, and semiconvergent-specific scans.
