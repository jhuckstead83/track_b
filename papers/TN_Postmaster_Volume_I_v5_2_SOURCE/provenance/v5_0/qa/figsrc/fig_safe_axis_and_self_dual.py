#!/usr/bin/env python3
"""Figure for Reading Volume §R5B: the triangular safe axis and the self-dual
magnitude.

This replaces the four-panel fold atlas that earlier editions carried here.
Its first two panels -- the two involutions of s, and the real and imaginary
parts of the fold q -- are now drawn better, and for one moving orbit, by the
§R10C figure; keeping them in two places was duplication and a page of it.
The two panels that belong to this part of the argument are kept and redrawn
from their formulas.

A. the real safe axis  x = s(s-1) = 2T_{s-1}  and its inverse  R = 2s-1
B. the self-dual magnitude: x^{-sigma} = x^{-(1-sigma)} for every x exactly at
   sigma = 1/2

Usage: python3 qa/figsrc/fig_safe_axis_and_self_dual.py
   ->  figures/figure74_safe_axis_and_self_dual.png
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'figures' / 'figure74_safe_axis_and_self_dual.png'

NAVY, BLUE, TEAL, RUST, GRAY = '#173B5E', '#275DAD', '#2A9D8F', '#B84A2B', '#4B5563'
AXBG, GRID = '#FCFBF8', '#E8E5DB'
plt.rcParams.update({'font.size': 12.5, 'axes.edgecolor': GRAY,
                     'axes.labelcolor': GRAY, 'xtick.color': GRAY,
                     'ytick.color': GRAY, 'axes.facecolor': AXBG,
                     'axes.titlecolor': NAVY, 'axes.titlesize': 14.5})

fig, (a, b) = plt.subplots(1, 2, figsize=(12.6, 4.9), dpi=200)
fig.suptitle('The triangular safe axis and the self-dual magnitude',
             color=NAVY, fontsize=18, fontweight='bold', y=0.985)

# ---- A. the safe axis -------------------------------------------------------
s = np.linspace(1, 8.2, 600)
a.plot(s, s * (s - 1), color=TEAL, lw=2.4, label=r'$x=s(s-1)=2T_{s-1}$')
a.plot(s, 2 * s - 1, color=RUST, lw=2.4, label=r'$R=2s-1=\sqrt{1+4x}$')
ints = np.arange(2, 9)
a.plot(ints, ints * (ints - 1), 'o', ms=7, color=BLUE, zorder=5)
for n in ints:
    a.annotate('%d' % (n * (n - 1)), (n, n * (n - 1)), xytext=(-4, 9),
               textcoords='offset points', color=NAVY, fontsize=10.5,
               ha='center')
a.set_xlim(1, 8.3); a.set_ylim(0, 62)
a.set_xlabel(r'real safe axis  $s=\sigma>1$  ($t=0$)')
a.set_ylabel('coordinate')
a.set_title(r'A.  Triangular safe-axis chart', loc='center')
a.legend(loc='upper left', fontsize=11, frameon=False)
a.grid(color=GRID, lw=0.8)

# ---- B. the self-dual magnitude --------------------------------------------
x = np.logspace(0, 2, 400)
for sig, col, lw in [(0.3, RUST, 2.2), (0.5, BLUE, 2.6), (0.7, TEAL, 2.2)]:
    b.loglog(x, x ** (-sig), color=col, lw=lw, label=r'$x^{-%.1f}$' % sig)
b.fill_between(x, x ** -0.7, x ** -0.3, color=RUST, alpha=0.07, lw=0)
b.set_xlabel('$x$'); b.set_ylabel('magnitude')
b.set_title(r'B.  Self-dual magnitude  $x^{-1/2}=1/\sqrt{x}$', loc='center')
b.text(1.5, 0.30, r'$x^{-\sigma}=x^{-(1-\sigma)}$', color=BLUE, fontsize=13.5)
b.text(1.5, 0.215, r'for all $x$ iff $\sigma=\frac{1}{2}$', color=BLUE,
       fontsize=13.5, fontweight='bold')
b.legend(loc='upper right', fontsize=11, frameon=False, ncol=3)
b.grid(color=GRID, lw=0.8, which='major')

fig.subplots_adjust(top=0.845, bottom=0.135, left=0.075, right=0.985, wspace=0.235)
fig.savefig(OUT, dpi=200, facecolor='white')
print(OUT.name, OUT.stat().st_size)
