# Source-rung certificate — $W_2,\ldots,W_6>0$

This directory is the certificate behind Technical Dossier §74A and the
certified rows of Reading Volume §R12. With

    x = s(s-1),   R = 2s-1,   D_x = R^{-1} D_s,   L = xi'/xi,
    W_k(x) = (-1)^{k-1} D_x^{2k-1}[x^k L/R],
    W_k(s) = s^{2k-1} W_k(s(s-1)) / (2k-1)!     (the certified quantity),

each program proves, for k = 2, 3, 4, 5, 6 and with no zero table, no verified
zero height and no RH assumption:

| part | statement |
|---|---|
| continuum | `W_k(s) > theta_k` for every real `s` in `[1,128]`, on a complete rational partition of continuum cells |
| tail | `W_k(s(s-1)) > (alpha_k/2) s^{2k} / (2s-1)^{4k-1}` for every `s >= 128`, by exact rational arithmetic |

with

| k | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| `theta_k` | 1e-5 | 1e-8 | 1e-10 | 1e-12 | 1e-15 |
| `alpha_k` | 7 | 396 | 54,000 | 13,406,400 | 5,258,131,200 |

Since `s -> s(s-1)` maps `[1,oo)` onto `[0,oo)` and `s^{2k-1}/(2k-1)! > 0`, the
two parts give `W_k(x) > 0` for every `x > 0`.

## Two arithmetics

| file | backend |
|---|---|
| `source_rungs_arb.py` | FLINT/Arb ball arithmetic through python-flint, SymPy for the exact tail. Generalizes the fifth/sixth-rung certificate of the 4.5 edition (`audit_widder_source.py`, SHA-256 `348bb9b9…88697`) to all five rungs. |
| `source_rungs_decimal.py` | the Python standard library alone: `decimal` (libmpdec) with directed rounding, an Euler–Maclaurin jet for zeta, a Stirling jet for digamma, `Fraction` for the source polynomials and the tail. Imports no FLINT/Arb, MPFR, SymPy or mpmath. |
| `cross_backend_check.py` | compares two receipts: exact tail data digit for digit, sampled enclosures overlapping, partitions complete, every cell above `theta_k`. |

Neither program samples points: every accepted cell carries a Taylor bound
with an enclosed remainder that holds on the whole interval, and a cell that
does not clear `theta_k` is bisected and retried.

## Replay

    python3 qa/source_rungs/source_rungs_arb.py     --output qa/source_rungs/RECEIPT_arb.json
    python3 qa/source_rungs/source_rungs_decimal.py --output qa/source_rungs/RECEIPT_decimal.json
    python3 qa/source_rungs/cross_backend_check.py \
        --arb qa/source_rungs/RECEIPT_arb.json \
        --decimal qa/source_rungs/RECEIPT_decimal.json \
        --output qa/source_rungs/CROSS_BACKEND.json

`qa/replay_math.py` runs exactly these three. The bundled second receipts come
from the same programs with every material parameter changed at once:

    python3 qa/source_rungs/source_rungs_arb.py --precision 384 --degree 22 \
        --step 1/128 --output qa/source_rungs/RECEIPT_arb_second.json
    python3 qa/source_rungs/source_rungs_decimal.py --digits 100 --degree 24 \
        --step 1/128 --em-terms 40 --em-bernoulli 26 --psi-shift 40 \
        --psi-bernoulli 34 --remainder-exponent -50 \
        --output qa/source_rungs/RECEIPT_decimal_second.json
    python3 qa/source_rungs/cross_backend_check.py \
        --arb qa/source_rungs/RECEIPT_arb_second.json \
        --decimal qa/source_rungs/RECEIPT_decimal_second.json \
        --output qa/source_rungs/CROSS_BACKEND_SECOND.json

`source_rungs_arb.py` needs python-flint and SymPy (see `qa/ENVIRONMENT.json`
for the versions used here); `source_rungs_decimal.py` needs only CPython.

**The Riemann hypothesis is open.** These five rungs are a finite prefix of the
Widder criterion. The criterion quantifies over every `k`, and no finite prefix
of it is an RH statement.
