# Triangular-n Postmaster, Volume I — v5.0

**17 September 2026. RH STATUS: OPEN.** Source-rung certificate release.

The two documents of this edition are published as separate files next to this package:

- `TN_Postmaster_Volume_I_v5_0_READING_VOLUME.pdf`, the continuous argument, with the single status key;
- `TN_Postmaster_Volume_I_v5_0_TECHNICAL_DOSSIER.pdf` (including three historical facsimile pages), the proofs, certificates and NO-GO material.

Their page counts and SHA-256 values are recorded in `PACKAGE_MANIFEST.json` (`delivered_pdfs`) and in `QA_RECEIPT_V5_0.md`. The package itself carries everything needed to rebuild them.

## What v5.0 adds

v5.0 claims no new RH implication, and no status changed.

- **One Reader bridge, §R10C.** "One orbit, four coordinates" joins §R7 to §R15:
  the folded point q, the resolvent pole −q, the reciprocal y = 1/q and the Li
  coordinate w = 1 − 1/s in one dictionary, with the recurrence
  Q₀ = 0, Q₁ = y, Q_{n+1} = 2y + (2−y)Q_n − Q_{n−1} that generates an orbit's
  whole Li column from the pole alone, and the interval
  Re ρ = ½ ⟺ q > ¼ ⟺ y ∈ (0,4) ⟺ |w| = 1. Nothing in it is new mathematics;
  every identity was already provable from material in the volume, and it is
  the only edition in which they appear together. Dossier (155A.4a) prints the
  matching diagonal specializations, marked as a restatement.
- **An exact replay for it.** `qa/audit_r10c_orbit.py` certifies the section in
  rational arithmetic with no floating-point comparison anywhere, including a
  calibration orbit at t = √2 whose rungs are exact rationals computed three
  independent ways.
- **A stale figure repaired, and the class of defect closed.** Figure 75's
  status panel had disagreed with §R12 for two editions — the claims were
  pixels, so text QA could not see them. `qa/figsrc/fig_status_panels.py`
  regenerates the status figures from one declared ledger, and
  `qa/audit_figure_claims.py` is a new gate that pins every cited figure by
  hash, runs forbidden-claim patterns over its OCR text, rejects uncited
  figures, and ties the printed ledger back to the §R12 table read out of the
  source at run time.
- **Figure provenance.** `qa/figsrc/` went from one generator to four; every
  figure added or redrawn this edition is reproducible from bundled source, the
  update audit checks the declared figure delta, and seven retired figures are
  archived by hash under `provenance/v50/pruned_figures/`.

The controlling source ledger is unchanged:

- `W1`: analytic;
- `W2-W6`: certified from the source (A-CAT) on the stated all-x domains;
- `W7 / F^(14)`: OPEN on the independent source channel;
- the much larger verified-height finite prefix remains a separate zero-assisted channel.

## Package policy

This package is self-contained for the current edition. It does not nest prior packages, and the two PDFs are published beside it rather than inside it (PP251 §5). Earlier editions and their evidence remain in the Zenodo version chain (concept DOI 10.5281/zenodo.21968915). `PRUNED.json` records every v4.8 member omitted here, with its size and SHA-256.

## Rebuild / verify

From this directory:

```sh
python3 qa/build_release.py both        # writes output/pdf/
python3 qa/replay_math.py               # 14 mathematical replays, including the source-rung certificate
python3 qa/audit_v50_updates.py         # logic/update audit
python3 qa/verify_v50.py                # publication verifier; add --pdf-dir DIR to check the published PDFs
python3 qa/verify_package.py            # manifest and checksums
```

`qa/source_rungs/LEGACY_COMPARISON.json` records the same comparison against the two receipts published with the 4.5 and 4.6 editions: identical tail constants, and 1,048 of their recorded cell-centre values re-computed in the second backend, all overlapping. Those receipts are named there by SHA-256; they stay in the Zenodo version chain rather than in this package.

`qa/source_rungs/README.md` documents the certificate and the exact replay commands, including the second run of each backend. `qa/source_rungs/source_rungs_decimal.py` and `qa/verify_package.py` need only CPython; `qa/source_rungs/source_rungs_arb.py` and `qa/audit_gamma_bridge.py` need `python-flint` (Arb), `sympy` and `mpmath`. PDF bytes depend on the TeX installation; `qa/ENVIRONMENT.json` records the build environment.
