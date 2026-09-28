# Team B replay, 27 September 2026

`dh_twin_highprec.py` recomputes the twin's scaled rung sign function at 60 and 100 digits
(mpmath) from `../dh_twin/dh_zeros.json`, the census to height 260 (169 on-line zeros and
5 off-line pairs, double-precision ordinates):

    python3 dh_twin_highprec.py ../dh_twin/dh_zeros.json --json dh_twin_highprec_receipt.json

| quantity | 60 digits | 100 digits | Dossier §69A (40 digits) |
|---|---|---|---|
| min of W_16588 near x = 7140.067 | +1.75927385895e-4 | +1.75927385895e-4 | +1.7592739e-4 |
| W_16589 at x = 7140.066262 | -4.66009149178e-5 | -4.66009149178e-5 | -4.6600915e-5 |

Both signs are unchanged when every listed ordinate is moved by up to 1e-12 (8 random trials).
Scope: the finite zero list, not every zero of the twin. The arithmetic precision is not the
limit; the truncation to the listed zeros is the stated scope. \EVID{} in the volumes.

## Exact first failing Löwner size (28 September 2026)

`lowner_nstar.py` uses the Dossier §69A method unchanged: h(x) = x·S_f(x) from the completed
twin's logarithmic derivative, with Taylor coefficients from a 2048-point contour of radius
0.75 x₀ at 250 digits. It then runs one symmetric elimination of the 112 × 112 local matrix.
The k-th pivot is the ratio of consecutive leading minors, so the first negative pivot is the
exact first failing size N*, not a multiple of 5.

    python3 lowner_nstar.py 0.97 112 --json nstar_0.97.json      (also 1.00 and 1.03)

| centre x₀ | pivots 1 … N*−1 | N* | pivot N* | Dossier table (tested sizes) |
|---|---|---|---|---|
| 7124.38 = 0.97\|q₀\| | all positive | **105** | −1.03 × 10⁻¹⁴¹ | PSD through 100, fails at 105 |
| 7344.72 = \|q₀\| | all positive | **106** | −3.26 × 10⁻¹⁴² | PSD through 105, fails at 110 |
| 7565.07 = 1.03\|q₀\| | all positive | **107** | −1.45 × 10⁻¹⁴² | PSD through 105, fails at 110 |

The pivots at the tested sizes reproduce the Dossier's "smallest pivot" column: 1.0 × 10⁻¹⁴¹ at
N = 105 (first centre), and 1.3 × 10⁻¹⁴⁹ and 1.2 × 10⁻¹⁴⁸ at N = 110. Each run has one negative
pivot up to 112, so every section from N* to 112 has exactly one negative eigenvalue.
Positivity is still established only at these three centres. \EVID{} in the volumes, like the
table it refines.

**Robustness.** A second run changes the precision and the contour: 320 digits, 2560 points, radius 0.70 x₀.

    LOWNER_DPS=320 LOWNER_M=2560 LOWNER_RADIUS=0.7 python3 lowner_nstar.py 1.00 112 --json robust_1.00.json

At all three centres it finds the same single negative pivot, and every printed pivot agrees to six significant digits (`robust_*.json`). The signs do not depend on the discretisation.
