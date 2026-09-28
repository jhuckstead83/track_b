#!/usr/bin/env python3
"""Figure for Reading Volume §R4A: Euler's constant on the triangular coordinate.

Panel A: the fractional-part mass on each unit interval equals the reciprocal-
triangular zeta term  sum_{k>=2} m^{-k}/T_k ; the masses add to log(2 pi) - gamma.
Panel B: centered at the half-step, the harmonic numbers expand in powers of 1/T_n
(Ramanujan); the uncentered expansion keeps an odd term.

Usage: python3 qa/figsrc/fig_gamma_bridge.py  ->  figures/v48_gamma_bridge.png
"""
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpmath import mp, mpf, harmonic, log, euler, pi

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'figures' / 'v48_gamma_bridge.png'
NAVY, BLUE, TEAL, RUST, GRAY = '#173B5E', '#275DAD', '#2A9D8F', '#B84A2B', '#4B5563'
AXBG, GRID = '#FCFBF8', '#E8E5DB'
plt.rcParams.update({'font.size': 12.5, 'axes.edgecolor': GRAY, 'axes.labelcolor': GRAY,
                     'xtick.color': GRAY, 'ytick.color': GRAY, 'axes.facecolor': AXBG,
                     'axes.titlecolor': NAVY, 'axes.titlesize': 15})

mp.dps = 30
G = float(euler)
L = float(log(2 * pi) - euler)

def mass(m):
    return 1.0 if m == 1 else 2 - 1 / m + 2 * (m - 1) * math.log(1 - 1 / m)

fig, (a, b) = plt.subplots(1, 2, figsize=(12.6, 4.7), dpi=210)
fig.suptitle("Euler's constant on the triangular coordinate", color=NAVY, fontsize=19, fontweight='bold', y=0.985)

# ---- panel A
x = np.linspace(1e-6, 8, 4000)
y = ((x - np.floor(x)) / x) ** 2
for m in range(1, 9):
    xs = np.linspace(m - 1 + 1e-9, m - 1e-9, 300)
    ys = ((xs - (m - 1)) / xs) ** 2
    a.fill_between(xs, 0, ys, color=(TEAL if m % 2 else BLUE), alpha=0.28, lw=0)
a.plot(x, y, color=NAVY, lw=1.6)
labels = {m: ('1' if m == 1 else f'{mass(m):.4f}') for m in range(1, 5)}
for m, txt in labels.items():
    # labels sit above each hump (peak (1/m)^2 at the right end), staggered so they never touch a curve
    ypos = {1: 0.45, 2: 0.30, 3: 0.175, 4: 0.115}[m]
    a.annotate(txt, xy=(m - 0.5, ypos), ha='center', fontsize=10, color=NAVY,
               bbox=dict(boxstyle='round,pad=0.12', fc='#FCFBF8', ec='none', alpha=0.9) if m > 1 else None)
a.set_xlim(0, 8); a.set_ylim(0, 1.08)
a.set_xlabel('$x$'); a.set_ylabel(r'$(\{x\}/x)^2$')
a.set_title('A.  one unit interval, one triangular zeta term', loc='center')
a.text(1.55, 0.86, r'mass on $[m-1,m]\;=\;\Sigma_{k\geq2}\; m^{-k}/T_k$', color=NAVY, fontsize=13.5)
a.text(1.55, 0.70, r'all masses: $\Sigma_{k\geq2}\;\zeta(k)/T_k\;=\;\log 2\pi-\gamma_{\rm E}$', color=RUST, fontsize=13.5)
a.text(1.55, 0.58, f'$= {L:.10f}$', color=RUST, fontsize=13.5)
a.grid(color=GRID, lw=0.8)

# ---- panel B
ns = [int(v) for v in np.unique(np.round(np.logspace(0, 3, 60)).astype(int))]
R = [mpf(1) / 12, mpf(-1) / 120, mpf(1) / 630]
def centered_err(n, K):
    Tn = mpf(n) * (n + 1) / 2
    v = harmonic(n) - log(2 * Tn) / 2 - sum(R[k] / Tn ** (k + 1) for k in range(K)) - euler
    return abs(float(v))
unc = [abs(float(harmonic(n) - log(n) - euler)) for n in ns]
b.loglog(ns, unc, color=GRAY, lw=2.0, ls='--', label=r'$|H_n-\log n-\gamma_{\rm E}|$, keeps the odd term $1/2n$')
cols = [BLUE, TEAL, RUST]
for K, c in zip(range(3), cols):
    lab = r'$|H_n-\frac{1}{2}\log 2T_n-\gamma_{\rm E}|$' if K == 0 else rf'after {K} term' + ('s' if K > 1 else '') + r' in $1/T_n$'
    b.loglog(ns, [centered_err(n, K) for n in ns], color=c, lw=2.2, label=lab)
b.set_xlabel('$n$'); b.set_ylabel('error')
b.set_title(r'B.  centered at $n+\frac{1}{2}$, only powers of $1/T_n$ remain', loc='center')
b.text(1.15, 8, r'$H_n\sim\gamma_{\rm E}+\frac{1}{2}\log 2T_n+\frac{1}{12T_n}-\frac{1}{120T_n^2}+\frac{1}{630T_n^3}-\cdots$', color=NAVY, fontsize=13)
b.legend(loc='lower left', fontsize=10.5, frameon=False)
b.set_ylim(1e-26, 1e3)
b.grid(color=GRID, lw=0.8, which='major')

fig.subplots_adjust(top=0.855, bottom=0.135, left=0.065, right=0.99, wspace=0.17)
fig.savefig(OUT, dpi=210, facecolor='white')
print(OUT, OUT.stat().st_size)
