#!/usr/bin/env python3
"""Regenerate every bundled figure that prints a rung-status claim.

One edition, one ledger.  The dictionary LEDGER below is the only place a
rung status appears in figure source; it is transcribed from the controlling
table of Reading Volume §R12 and is checked against that table by
qa/audit_figure_claims.py.  Before v5.0 these panels were opaque rasters with
no generator, and figure 75 silently disagreed with §R12 for two editions.

Emits
  figures/figure75_li_pp97_loewner_study_atlas.png   full regeneration
  figures/v26c_source_depth.png                      full regeneration
  figures/v30_rh_equivalence_map.png                 title band restamped from
                                                     the archived original

Usage: python3 qa/figsrc/fig_status_panels.py [--check]
With --check nothing is written; the emitted bytes are compared with what is
already in figures/.
"""
from pathlib import Path
import argparse
import hashlib
from math import comb

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / 'figures'
ARCHIVE = ROOT / 'provenance' / 'v50' / 'figures'

NAVY, BLUE, TEAL, RUST, GRAY = '#173B5E', '#275DAD', '#2A9D8F', '#B84A2B', '#4B5563'
PAPER, GRID, GREENBG, REDBG = '#FCFBF8', '#E8E5DB', '#EAF3EF', '#FBEEE9'

plt.rcParams.update({'font.size': 12.0, 'axes.titlecolor': NAVY,
                     'figure.facecolor': 'white'})

K_H = '4,712,664,392,502'

# ---------------------------------------------------------------- the ledger
# transcribed from Reading Volume §R12, "This is the position, stated once".
LEDGER = [
    (r'$W_1$',                    'PROVED', 'analytic source, $F^{(2)}$'),
    (r'$W_2$–$W_6$',              'PROVED', 'source A-CAT, one certificate,\n$F^{(12)}$ (Dossier §74A)'),
    (r'$W_k$, $7\leq k\leq K_H$', 'PROVED', 'zero-assisted,\nverified height (§R13)'),
    (r'$W_k$, $k>K_H$',           'OPEN',   '—'),
    ('all orders / all nodes',    'OPEN',   'RH-equivalent sign'),
]
SOURCE_FRONTIER = 'source frontier: the next independent rung is $W_7\\to F^{(14)}$.'

# source-depth table: rung, boundary, source jet, global sign, independent source
DEPTH = [
    (r'$W_1$', r'$\mu_0$', r'$F^{(2)}$',  'PROVED', 'analytic'),
    (r'$W_2$', r'$\mu_1$', r'$F^{(4)}$',  'PROVED', 'A-CAT'),
    (r'$W_3$', r'$\mu_2$', r'$F^{(6)}$',  'PROVED', 'A-CAT'),
    (r'$W_4$', r'$\mu_3$', r'$F^{(8)}$',  'PROVED', 'A-CAT'),
    (r'$W_5$', r'$\mu_4$', r'$F^{(10)}$', 'PROVED', 'A-CAT'),
    (r'$W_6$', r'$\mu_5$', r'$F^{(12)}$', 'PROVED', 'A-CAT'),
]


def pascal_rows(n=6):
    """Reading Volume (15.2): mu_{k-1} = sum_j (-1)^{j+1} C(2k, k-j) lambda_j."""
    return [[(-1) ** (j + 1) * comb(2 * k, k - j) for j in range(1, k + 1)]
            for k in range(1, n + 1)]


def _table(ax, rows, widths, header, fontsize=11.5, statuscol=None):
    """Draw a simple table; statuscol tints PROVED/OPEN rows."""
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    n = len(rows) + 1
    h = 1.0 / n
    x = np.concatenate([[0], np.cumsum(widths)])
    ax.add_patch(plt.Rectangle((0, 1 - h), 1, h, fc=NAVY, ec='none'))
    for c, txt in enumerate(header):
        ax.text((x[c] + x[c + 1]) / 2, 1 - h / 2, txt, ha='center', va='center',
                color='white', fontsize=fontsize, fontweight='bold')
    for r, row in enumerate(rows):
        y0 = 1 - (r + 2) * h
        bg = PAPER
        if statuscol is not None:
            bg = REDBG if row[statuscol].strip() == 'OPEN' else GREENBG
        ax.add_patch(plt.Rectangle((0, y0), 1, h, fc=bg, ec=GRID, lw=0.8))
        for c, txt in enumerate(row):
            col = RUST if txt.strip() == 'OPEN' else (TEAL if txt.strip() == 'PROVED' else NAVY)
            ax.text((x[c] + x[c + 1]) / 2, y0 + h / 2, txt, ha='center', va='center',
                    color=col, fontsize=fontsize,
                    fontweight='bold' if txt.strip() in ('OPEN', 'PROVED') else 'normal',
                    linespacing=1.25)


def build_figure75():
    fig = plt.figure(figsize=(11.6, 13.6), dpi=190)
    fig.suptitle('Li coefficients $\\to$ boundary moments $\\to$ matrix compatibility',
                 color=NAVY, fontsize=19.5, fontweight='bold', y=0.978)
    fig.text(0.5, 0.945, 'Exact dictionaries; distinct positivity proofs',
             ha='center', color=GRAY, fontsize=14)

    gs = fig.add_gridspec(2, 2, left=0.075, right=0.955, top=0.888, bottom=0.075,
                          hspace=0.44, wspace=0.18, height_ratios=[1.0, 0.92])

    # ---- A. central-Pascal rows -------------------------------------------
    ax = fig.add_subplot(gs[0, 0])
    rows = pascal_rows(6)
    M = np.full((6, 6), np.nan)
    for i, row in enumerate(rows):
        M[i, :len(row)] = row
    sgn = np.sign(M) * np.log10(np.abs(M) + 1)
    ax.imshow(sgn, cmap='RdBu', vmin=-3.2, vmax=3.2)   # positive blue, negative red
    for i in range(6):
        for j in range(6):
            if not np.isnan(M[i, j]):
                shade = 'white' if abs(sgn[i, j]) > 2.1 else NAVY
                ax.text(j, i, '%d' % M[i, j], ha='center', va='center',
                        color=shade, fontsize=12)
    ax.set_xticks(range(6), ['$\\lambda_%d$' % (j + 1) for j in range(6)], fontsize=13)
    ax.set_yticks(range(6), ['$\\mu_%d$' % i for i in range(6)], fontsize=13)
    ax.tick_params(length=0, colors=NAVY)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title('A.  Central-Pascal rows', fontsize=15, pad=12)
    ax.text(0.5, -0.115, r'$W_k(0)/(2k-1)!\;=\;\mu_{k-1}$', ha='center',
            va='top', transform=ax.transAxes, color=NAVY, fontsize=13.5)
    ax.text(0.5, -0.205, r'$\mu_{k-1}=\sum_j(-1)^{j+1}\binom{2k}{k-j}\lambda_j$',
            ha='center', va='top', transform=ax.transAxes, color=GRAY, fontsize=12)

    # ---- B. moment indices add --------------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title('B.  Moment indices add', fontsize=15, pad=12)
    ax.text(0.09, 0.755, '$H_3=$', fontsize=19, color=NAVY, va='center')
    cw, ch = 0.165, 0.115
    for i in range(3):
        for j in range(3):
            x0, y0 = 0.30 + cw * j, 0.87 - ch * (i + 1)
            ax.add_patch(plt.Rectangle((x0, y0), cw, ch,
                                       fc=(GREENBG if i == j else '#EDF3F9'),
                                       ec=GRID, lw=1.0))
            ax.text(x0 + cw / 2, y0 + ch / 2, '$\\mu_%d$' % (i + j), ha='center',
                    va='center', fontsize=16, color=NAVY)
    ax.text(0.5, 0.435, 'Diagonal: normalized\n$W_1(0),\\,W_3(0),\\,W_5(0)$',
            ha='center', va='center', color=GRAY, fontsize=12.5)
    ax.text(0.5, 0.275, '$C_N(0)=D_NH_ND_N$', ha='center', va='center',
            color=NAVY, fontsize=15)
    ax.text(0.5, 0.115, 'Same inertia. Positive entries\nalone do not prove PSD.',
            ha='center', va='center', color=RUST, fontsize=12.5)

    # ---- C. status, from the ledger ---------------------------------------
    ax = fig.add_subplot(gs[1, 0])
    ax.set_title('C.  Status: controlled by Reader §R12', fontsize=15, pad=12)
    _table(ax, LEDGER, [0.33, 0.21, 0.46], ['rungs', 'sign', 'proof channel'],
           fontsize=10.5, statuscol=1)
    ax.text(0.5, -0.075, '$K_H=%s$, fixed at (13.6).' % K_H.replace(',', '{,}'),
            ha='center', va='top', transform=ax.transAxes, color=GRAY, fontsize=11.5)
    ax.text(0.5, -0.155, 'All rungs at once is the Riemann hypothesis.',
            ha='center', va='top', transform=ax.transAxes, color=RUST, fontsize=11.5)

    # ---- D. completed source ----------------------------------------------
    ax = fig.add_subplot(gs[1, 1])
    ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title('D.  Completed source', fontsize=15, pad=12)
    for y, txt, size, col in [(0.80, '$h=xS_\\xi$', 19, NAVY),
                              (0.635, '$[\\mathcal{L}_h]_{ii}=W_1(x_i)$', 17, NAVY),
                              (0.485, '$\\mathcal{L}_h=L_\\Gamma-L_P$', 17, NAVY)]:
        ax.text(0.5, y, txt, ha='center', va='center', fontsize=size, color=col)
    ax.text(0.5, 0.315, 'All finite positive node sets:\n$\\mathcal{L}_h\\succeq 0$',
            ha='center', va='center', color=RUST, fontsize=13)
    ax.text(0.5, 0.175, 'RH-equivalent: OPEN', ha='center', color=RUST,
            fontsize=14, fontweight='bold')
    ax.text(0.5, 0.045, 'Finite matrix gates through\nrank eight remain certified.',
            ha='center', va='center', color=GRAY, fontsize=12)

    return fig, FIG / 'figure75_li_pp97_loewner_study_atlas.png'


def build_source_depth():
    fig = plt.figure(figsize=(13.6, 5.6), dpi=175)
    fig.suptitle('One scalar ladder, two proof channels', color=NAVY,
                 fontsize=23, fontweight='bold', y=0.945)
    ax = fig.add_axes([0.045, 0.145, 0.91, 0.70])
    _table(ax, DEPTH, [0.12, 0.24, 0.20, 0.20, 0.24],
           ['rung', 'boundary / $(2k-1)!$', 'source jet', 'global sign',
            'independent source'], fontsize=13.5, statuscol=3)
    fig.text(0.5, 0.055, SOURCE_FRONTIER, ha='center', color=GRAY, fontsize=13.5)
    return fig, FIG / 'v26c_source_depth.png'


def restamp_equivalence_map(write=True):
    """Blank and redraw only the title band of the RH-criteria map.

    The body of that figure is current; only its edition stamp was stale, so
    v5.0 repaints the top band rather than re-transcribing eleven claim boxes.
    The archived original is the input every time, so the step is idempotent.
    """
    from PIL import Image, ImageDraw, ImageFont
    target = FIG / 'v30_rh_equivalence_map.png'
    keep = ARCHIVE / 'v30_rh_equivalence_map__pre_v50_titleband.png'
    if not keep.exists():
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        keep.write_bytes(target.read_bytes())
    im = Image.open(keep).convert('RGB')
    w, h = im.size
    band = int(h * 0.070)                      # the stamped title line only
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, band], fill=(255, 255, 255))
    txt = 'THE COMPLETED OBJECT AND ITS RH CRITERIA'
    size = int(band * 0.72)
    for cand in ('DejaVuSans-Bold.ttf', 'DejaVuSans.ttf'):
        try:
            font = ImageFont.truetype(cand, size)
            break
        except OSError:
            font = None
    if font is None:
        font = ImageFont.load_default()
    box = d.textbbox((0, 0), txt, font=font)
    d.text(((w - (box[2] - box[0])) / 2, (band - (box[3] - box[1])) / 2 - box[1]),
           txt, font=font, fill=(23, 59, 94))
    if write:
        im.save(target)
    return target, im


def emit(check):
    out = []
    for builder in (build_figure75, build_source_depth):
        fig, path = builder()
        tmp = path if not check else path.with_suffix('.check.png')
        fig.savefig(tmp, dpi=fig.dpi, facecolor='white')
        plt.close(fig)
        out.append((path.name, hashlib.sha256(tmp.read_bytes()).hexdigest(),
                    tmp.stat().st_size))
        if check:
            same = tmp.read_bytes() == path.read_bytes()
            tmp.unlink()
            out[-1] = out[-1] + ('match' if same else 'DIFFERS',)
    path, _ = restamp_equivalence_map(write=not check)
    if not check:
        out.append((path.name, hashlib.sha256(path.read_bytes()).hexdigest(),
                    path.stat().st_size))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    for row in emit(args.check):
        print('  '.join(str(v) for v in row))
