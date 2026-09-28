# v5.2 evidence: the functional-equation twin

These are the programs and outputs behind Dossier §§69A–69B and Reading Volume §R25A. Every
number they produce is \EVID{} in the volumes, so none of it upgrades a status. The two
theorems in those sections, (TW.1) and (TW.2), do not depend on these files. Their exact
algebra is checked by `qa/check_v52_interface.py`.

The files were produced by Team B on 27 September 2026 and are copied here unchanged, with
two exceptions:
- `zero10.py`, from the working scratch directory;
- `colab/COLAB_OUTPUTS.txt`, a transcript of the Colab runs.

## Where each printed number comes from

| volume statement | file(s) |
|---|---|
| twin definition, κ, functional equation to 2e-13 (double); zero-free for σ ≥ 1.39514 | `dh_twin/dh.py`, `dh_twin/selftest.py` |
| functional equation to 1e-39; off-line zeros polished to 25 digits | Colab section A (`colab/`) |
| PP199's point 1.10078201+86.14311231i is not a zero (\|f\| = 0.576) | `dh_twin/pp199check.py` |
| census to 260 (169 on-line, 5 off-line pairs) | `dh_twin/zeros.py`, `dh_zeros.json`, `zeros_window_log.txt` |
| census 260–640 (16 off-line pairs in total, 501 on-line) | `dh_twin/zeros.py`, `dh_zeros_260_440.json`, `dh_zeros_440_640.json`; Colab section B (20 digits, 260–600) |
| sector bound k ≤ 218 (θ_max over the list, tail bound from the zero-free strip) | `dh_twin/rungs3.cjs` (`Ksector` in `rungs3_T640.json`); Colab section A at T = 260 |
| W_k > 0 at k = 219, 500, 1000, 3000, 8000, 12000 and 16588 on 0.524 ≤ x ≤ 43,264; first failure W_16589(7140.066) < 0 | `dh_twin/global_check.cjs`, `global_check_output.txt`; bisection in `rungs2.cjs`, `dh_first_failure_219_20000.json`; the 40-digit values come from Colab section A |
| first failing rung of each off-line zero (table, rows 0–9 and 11–15) | `dh_twin/rungs3.cjs`, `rungs3_T440.json`, `rungs3_T640.json` |
| row 10 (k* = 18,519,801) | `dh_twin/zero10.py` (needs `planted_zeta/planted.py` on the path) |
| ratio column and median 0.806 | `dh_twin/neighbor_law2.py` |
| c(n) of −f′/f | recomputed by Dirichlet inversion in `qa/check_v52_interface.py` |
| twin and ζ resolvents from the source formula (ζ check: λ₁ = 0.02309570896612) | `dh_twin/lowner.py` |
| Löwner/Dobsch PSD for N ≤ 64 in double precision; on-line control about 5e-6 | `dh_twin/dobsch.cjs`, `dobsch_compare.cjs`, `dobsch_twin_0.json`, `dobsch_twin_scan_log.txt` |
| Löwner/Dobsch first failure N = 105 (x0 = 7124.38) and N = 110 (±3%), at 250 digits | Colab section D (`colab/COLAB_OUTPUTS.txt`) |
| rung values rechecked at 60 and 100 digits on the T = 260 list; stable under 1e-12 shifts (Team B, 27 Sep) | `team_b_replay/dh_twin_highprec.py`, `team_b_replay/dh_twin_highprec_receipt.json` |
| exact first failing Löwner size N* at each centre, from every leading pivot (Team B, 27 Sep) | `team_b_replay/lowner_nstar.py`, `team_b_replay/nstar_*.json` |
| 90 planted ζ pairs; median ratio 0.82; 10–90% range 0.57–1.09; k*θ² spread 71× | `planted_zeta/planted.py`, `planted_summary.py`, `planted_all.json`, `planted_zeros_*.json` and `.log` |
| local exact form reproduces 16,589 from nearby zeros | `planted_zeta/planted.py`, `validate` mode |
| the earlier constant K*δ² = 0.0631 was a τ-window artifact | `planted_zeta/planted_probe.py` |

The planted runs read Platt's zeta-zero tables (`zeros_14.dat`, `zeros_5000.dat`,
`zeros_26000.dat`, `zeros_6746000.dat`, `zeros_220946000.dat` and `zeros_1000046000.dat`).
Those tables are not redistributed here. Each output file is named after the table it read.

## Superseded

`dh_twin/lowner_search.py` was a first divided-difference Löwner search. The negatives of
about 1e-11 that it reported were rounding noise. It is kept only as a record, and
`dobsch.cjs` supersedes it. `dh_twin/rungs.cjs` is the first rung scan, which
`rungs2.cjs` and `rungs3.cjs` supersede. The "k*θ² ≈ const" reading in older notes is
superseded by (TW.3).

## Running

Node 18+ runs the `.cjs` files. Python 3 runs the `.py` files, using only the standard library,
except that Colab uses mpmath. The scripts were run from a working directory in which
`dh_twin/` was named `dh/`, `planted.py` sat beside it, and Platt's tables were on
`D:\Zeroes`. To rerun them, restore that layout or edit the paths.
