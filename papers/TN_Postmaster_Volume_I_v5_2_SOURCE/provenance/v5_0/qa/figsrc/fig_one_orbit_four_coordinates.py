#!/usr/bin/env python3
"""Figure for Reading Volume §R10C: one orbit in its four coordinates.

Two rows, the same orbit height, one slider moved.  Top row is on the critical
line; bottom row is the same height off it.  The four columns are the four
coordinates of (10C.1): the point s and its mirror, the fold q with the
resolvent pole -q, the Li coordinate w against the unit circle, and the rung
column Q_n generated from y = 1/q by the recurrence (10C.4).

Everything drawn is computed from beta and t by the same formulas the volume
states; nothing is fitted.  Off the line the three locks of (10C.6) fail
together, and the rung column leaves the nonnegative axis.

Usage: python3 qa/figsrc/fig_one_orbit_four_coordinates.py
   ->  figures/figure75A_r10c_one_orbit_four_coordinates.png
"""
from pathlib import Path
from fractions import Fraction

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'figures' / 'figure75A_r10c_one_orbit_four_coordinates.png'

NAVY, BLUE, TEAL, RUST, GRAY = '#173B5E', '#275DAD', '#2A9D8F', '#B84A2B', '#4B5563'
PLUM, PAPER, GRID = '#6042A6', '#FCFBF8', '#E8E5DB'

NMAX = 24
T = 1.2
ROWS = [(0.5, 'on the line:  $\\beta=\\frac{1}{2}$'),
        (0.75, 'off the line:  $\\beta=0.75$, same height')]


def orbit(beta, t):
    """every quantity in (10C.1)-(10C.7), from beta and t alone."""
    s = complex(beta, t)
    q = s * (1 - s)
    y = 1 / q
    w = 1 - 1 / s
    Q = [0.0 + 0j, y]
    for _ in range(NMAX):
        Q.append(2 * y + (2 - y) * Q[-1] - Q[-2])
    return dict(s=s, q=q, p=-q, y=y, w=w, Q=Q[1:NMAX + 1])


def calibration():
    """the exact orbit of the demo preset: t = sqrt 2, q = 9/4, y = 4/9."""
    y = Fraction(4, 9)
    Q = [Fraction(0), y]
    for _ in range(6):
        Q.append(2 * y + (2 - y) * Q[-1] - Q[-2])
    return Q[1:5]


def frame(ax, title, color):
    ax.set_title(title, fontsize=12.5, color=color, loc='left', pad=7)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor(PAPER)
    for sp in ax.spines.values():
        sp.set_color(GRID)


def draw_row(axes, beta, t, headline, last):
    m = orbit(beta, t)
    on = abs(beta - 0.5) < 1e-12

    # ---- A. the s-plane ----------------------------------------------------
    ax = axes[0]
    frame(ax, 'A.  $s$ and its mirror', RUST)
    ax.axvline(0.5, color=TEAL, ls='--', lw=1.6)
    ax.axhline(0, color=GRID, lw=1.0)
    ax.plot([beta], [t], 'o', ms=10, color=RUST, zorder=5)
    ax.plot([1 - beta], [-t], 'o', ms=9, mfc='none', mec=RUST, mew=1.6, zorder=5)
    ax.annotate('$s$', (beta, t), xytext=(9, -2), textcoords='offset points',
                color=RUST, fontsize=13)
    ax.annotate('$1-s$', (1 - beta, -t), xytext=(9, -4), textcoords='offset points',
                color=RUST, fontsize=11.5, bbox=dict(boxstyle='round,pad=0.15', fc=PAPER, ec='none', alpha=0.92))
    ax.set_xlim(0, 1); ax.set_ylim(-t * 1.55, t * 1.55)
    ax.text(0.05, 0.045, '$\\beta=%.2f$,  $t=%.1f$' % (beta, t),
            transform=ax.transAxes, color=RUST, fontsize=10.5, bbox=dict(boxstyle='round,pad=0.15', fc=PAPER, ec='none', alpha=0.92))
    ax.text(0.52, 0.93, 'critical line', transform=ax.transAxes, color=TEAL,
            fontsize=10.5)

    # ---- B. the fold plane -------------------------------------------------
    ax = axes[1]
    frame(ax, 'B.  fold $q$ and pole $-q$', BLUE)
    R = abs(m['q']) * 1.28
    ax.axhline(0, color=GRID, lw=1.0)
    ax.axvline(0, color=GRID, lw=1.0)
    ax.plot([0, R], [0, 0], color=BLUE, lw=3, alpha=0.30, solid_capstyle='butt')
    ax.plot([-R, 0], [0, 0], color=PLUM, lw=3, alpha=0.30, solid_capstyle='butt')
    ax.plot([m['p'].real, m['q'].real], [m['p'].imag, m['q'].imag],
            color=PLUM, ls=':', lw=1.3)
    ax.plot([m['q'].real], [m['q'].imag], 'o', ms=10, color=BLUE, zorder=5)
    ax.plot([m['p'].real], [m['p'].imag], 'o', ms=10, color=PLUM, zorder=5)
    ax.annotate('$q$', (m['q'].real, m['q'].imag), xytext=(6, 8),
                textcoords='offset points', color=BLUE, fontsize=13)
    ax.annotate('$-q$', (m['p'].real, m['p'].imag), xytext=(-8, -18),
                textcoords='offset points', color=PLUM, fontsize=12)
    ax.set_xlim(-R, R); ax.set_ylim(-R * 0.62, R * 0.62)
    ax.text(0.035, 0.90, '$\\Re\\,1/q=%.6f$' % (m['y'].real),
            transform=ax.transAxes, color=BLUE, fontsize=11)
    ax.text(0.035, 0.795, '$\\Im\\,1/q=%s$'
            % ('0' if on else '%.6f' % m['y'].imag),
            transform=ax.transAxes, color=(BLUE if on else RUST), fontsize=11)
    ax.text(0.035, 0.055, 'positive ray' if on else 'off the ray',
            transform=ax.transAxes, color=(BLUE if on else RUST), fontsize=11)

    # ---- C. the Li coordinate ---------------------------------------------
    ax = axes[2]
    frame(ax, 'C.  $w=1-1/s$ and $w^{-1}$', TEAL)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=GRAY, ls='--', lw=1.5)
    ax.axhline(0, color=GRID, lw=1.0); ax.axvline(0, color=GRID, lw=1.0)
    wi = 1 / m['w']
    ax.plot([0, m['w'].real], [0, m['w'].imag], color=TEAL, ls=':', lw=1.2)
    ax.plot([m['w'].real], [m['w'].imag], 'o', ms=10, color=TEAL, zorder=5)
    ax.plot([wi.real], [wi.imag], 'o', ms=9, mfc='none', mec=TEAL, mew=1.6, zorder=5)
    ax.annotate('$w$', (m['w'].real, m['w'].imag), xytext=(7, 4),
                textcoords='offset points', color=TEAL, fontsize=13)
    ax.annotate('$w^{-1}$', (wi.real, wi.imag), xytext=(7, -6),
                textcoords='offset points', color=TEAL, fontsize=11.5)
    lim = max(1.35, abs(wi) * 1.12)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect('equal', adjustable='box')
    ax.text(0.035, 0.055, '$|w|=%.6f$' % abs(m['w']), transform=ax.transAxes,
            color=(TEAL if on else RUST), fontsize=11)

    # ---- D. the rung column ------------------------------------------------
    ax = axes[3]
    frame(ax, 'D.  $Q_n$, $n=1\\ldots%d$' % NMAX, PLUM)
    vals = [z.real for z in m['Q']]
    neg = next((i + 1 for i, v in enumerate(vals) if v < 0), None)
    cols = [RUST if v < 0 else PLUM for v in vals]
    ax.bar(range(1, NMAX + 1), vals, width=0.62, color=cols, alpha=0.85)
    ax.axhline(0, color=GRAY, lw=1.1)
    ax.set_xlim(0.2, NMAX + 0.8)
    top = max(vals) * 1.34
    bot = min(min(vals) * 1.9, -top * 0.30)
    ax.set_ylim(bot, top)
    if neg is not None:
        ax.annotate('$n=%d$' % neg, (neg, vals[neg - 1]), xytext=(2, -26),
                    textcoords='offset points', color=RUST, fontsize=11,
                    ha='center', arrowprops=dict(arrowstyle='-', color=RUST, lw=1.0))
    ax.text(0.035, 0.90, '$Q_1=%.6f$' % vals[0], transform=ax.transAxes,
            color=PLUM, fontsize=11)
    ax.text(0.035, 0.795, '$\\Re\\,1/q=%.6f$' % m['y'].real,
            transform=ax.transAxes, color=BLUE, fontsize=11)
    ax.text(0.035, 0.055,
            'every rung a square' if on else 'first negative rung: $n=%d$' % neg,
            transform=ax.transAxes, color=(PLUM if on else RUST), fontsize=11)

    axes[0].text(0.0, 1.235, headline, transform=axes[0].transAxes,
                 fontsize=14.5, color=NAVY, fontweight='bold', va='bottom')


def main():
    fig, axes = plt.subplots(2, 4, figsize=(16.2, 8.4), dpi=165,
                             gridspec_kw=dict(width_ratios=[0.72, 1.12, 0.92, 1.24]))
    fig.suptitle('One orbit, four coordinates: '
                 '$s\\;\\to\\;q\\;\\to\\;-q\\;\\to\\;y=1/q\\;\\to\\;w\\;\\to\\;Q_n$',
                 color=NAVY, fontsize=19, fontweight='bold', y=0.990)
    for r, (beta, headline) in enumerate(ROWS):
        draw_row(axes[r], beta, T, headline, r == len(ROWS) - 1)

    cal = calibration()
    fig.text(0.5, 0.028,
             'Exact calibration orbit:  $t=\\sqrt{2}$, $q=9/4$, $-q=-9/4$, '
             '$y=4/9$, $w=(7-4\\sqrt{2}\\,i)/9$ with $|w|=1$;  '
             + ',  '.join('$Q_%d=%d/%d$' % (i + 1, v.numerator, v.denominator)
                          for i, v in enumerate(cal)),
             ha='center', color=GRAY, fontsize=11.5)
    fig.text(0.5, 0.0035,
             'A single orbit constrains nothing: $\\lambda_n$ sums $Q_n$ over all '
             'orbits, and RH is $\\lambda_n\\geq 0$ for every $n$.',
             ha='center', color=RUST, fontsize=11.5)

    fig.subplots_adjust(left=0.030, right=0.988, top=0.845, bottom=0.092,
                        hspace=0.52, wspace=0.17)
    fig.savefig(OUT, dpi=165, facecolor='white')
    print(OUT.name, OUT.stat().st_size)


if __name__ == '__main__':
    main()
