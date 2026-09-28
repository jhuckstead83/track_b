#!/usr/bin/env python3
"""Pin the first failing Löwner size N* of the Davenport-Heilbronn twin (Team B, 27 Sep 2026).

Same source-formula method as Colab section D of TEAM_B_long_runs.ipynb (h(x) = x S_f(x) from the
completed twin's logarithmic derivative, Taylor coefficients by a 2048-point contour of radius 0.75 x0
at 250 digits). Difference: one symmetric elimination of the Nmax x Nmax local matrix; its k-th pivot
is the ratio of consecutive leading minors, so the first negative pivot index is the exact first
failing size N*, not a multiple of 5.
Usage: python3 lowner_nstar.py 0.97 [Nmax=112] [--json out.json]
Optional environment: LOWNER_DPS (250), LOWNER_M (2048), LOWNER_RADIUS (0.75), for a robustness rerun.
"""
import sys, time, json
import mpmath as mp
import os
DPS = int(os.environ.get('LOWNER_DPS', '250')); MPTS = int(os.environ.get('LOWNER_M', '2048')); FRAC = os.environ.get('LOWNER_RADIUS', '0.75')
mp.mp.dps = DPS
frac_x = sys.argv[1]; NMAX = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 112
K = (mp.sqrt(10 - 2*mp.sqrt(5)) - 2) / (mp.sqrt(5) - 1)
COEF = {1: 1, 2: K, 3: -K, 4: -1}
def fD(s):  return mp.power(5, -s) * sum(c * mp.zeta(s, mp.mpf(r)/5) for r, c in COEF.items())
def fDp(s): return -mp.log(5)*fD(s) + mp.power(5, -s) * sum(c * mp.zeta(s, mp.mpf(r)/5, 1) for r, c in COEF.items())
def h_twin(x):
    R = mp.sqrt(1 + 4*x); s = (1 + R)/2
    return x * (mp.log(5/mp.pi)/2 + mp.digamma((s+1)/2)/2 + fDp(s)/fD(s)) / R
def taylor_coeffs(x0, nmax, M=None, frac=None):
    M = M or MPTS; frac = mp.mpf(frac or FRAC)
    r = frac * x0
    vals = [h_twin(x0 + r*mp.expj(2*mp.pi*k/M)) for k in range(M)]
    out = []
    for n in range(nmax + 1):
        c = mp.fsum(vals[k]*mp.expj(-2*mp.pi*k*n/M) for k in range(M)) / M
        out.append(mp.re(c) * (x0/r)**n)
    return out
def pivots(A):
    A = [row[:] for row in A]; n = len(A); piv = []
    for k in range(n):
        p = A[k][k]; piv.append(p)
        for i in range(k+1, n):
            m = A[i][k] / p
            for j in range(k+1, n): A[i][j] -= m * A[k][j]
    return piv
s0 = mp.mpc('0.8085171824566377', '85.69934848537758')
q0 = s0 * (1 - s0); r0 = abs(q0)
x0 = r0 * mp.mpf(frac_x); t0 = time.time()
c = taylor_coeffs(x0, 2 * NMAX)
t1 = time.time()
A = [[c[i + j + 1] for j in range(NMAX)] for i in range(NMAX)]
piv = pivots(A)
neg = [k + 1 for k, p in enumerate(piv) if p < 0]
first = neg[0] if neg else None
rep = {'centre_factor': frac_x, 'x0': mp.nstr(x0, 12), 'Nmax': NMAX, 'dps': DPS, 'contourPoints': MPTS, 'radius': FRAC + ' x0',
       'coefficientSeconds': round(t1 - t0), 'firstNegativePivot_N': first,
       'negativePivotIndices': neg[:10],
       'pivots_95_to_112': [[k + 1, mp.nstr(piv[k], 6)] for k in range(94, min(NMAX, 112))],
       'meaning': 'leading sections N < N* are positive definite; the N* section has one negative eigenvalue'}
print(json.dumps(rep, indent=1), flush=True)
if '--json' in sys.argv:
    json.dump(rep, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
