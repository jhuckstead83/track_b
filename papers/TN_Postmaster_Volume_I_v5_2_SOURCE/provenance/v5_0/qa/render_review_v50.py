#!/usr/bin/env python3
"""Render the v5.0 PDFs for visual review and run two geometric page checks.

Contact sheets and full-size renders are review scratch output (written
outside the package by default); they are not a substitute for proof
verification. The geometric checks flag text drawn outside the page's
text area and body pages that are nearly empty.
"""
from pathlib import Path
import argparse, json
import pymupdf as fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=str(ROOT.parent / 'visual_v50'))
ap.add_argument('--pages', nargs='*', default=[], help='extra full-size pages, e.g. reading:18 dossier:25')
a = ap.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
STEMS = {'reading': 'READING_VOLUME', 'dossier': 'TECHNICAL_DOSSIER'}
report = {}
for tag, suffix in STEMS.items():
    pdf = ROOT / f'output/pdf/TN_Postmaster_Volume_I_v5_0_{suffix}.pdf'
    d = fitz.open(pdf)
    body_pages = json.loads((ROOT / f'qa/BUILD_{tag.upper()}.json').read_text())['body_pages']
    outside, sparse = [], []
    for i in range(body_pages):
        pg = d[i]; W, H = pg.rect.width, pg.rect.height
        for b in pg.get_text('blocks'):
            x0, y0, x1, y1 = b[:4]
            if x0 < 18 or x1 > W - 18 or y0 < 18 or y1 > H - 18:
                outside.append((i + 1, [round(v) for v in (x0, y0, x1, y1)]))
        words = len(pg.get_text('words'))
        imgs = len(pg.get_images())
        if words < 60 and imgs == 0 and 2 < i + 1 < body_pages:
            sparse.append((i + 1, words))
    sheets = []
    w, h, pad, lab, cols, rows = 230, 300, 10, 18, 6, 5
    per = cols * rows
    for start in range(0, len(d), per):
        sheet = Image.new('RGB', (cols * (w + pad) + pad, rows * (h + lab + pad) + pad), '#e4e7e9')
        draw = ImageDraw.Draw(sheet)
        for k in range(per):
            i = start + k
            if i >= len(d):
                break
            pix = d[i].get_pixmap(matrix=fitz.Matrix(.42, .42), alpha=False)
            im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples); im.thumbnail((w, h))
            x = pad + (k % cols) * (w + pad); y = pad + (k // cols) * (h + lab + pad)
            sheet.paste(im, (x, y + lab)); draw.text((x, y + 3), f'{tag} PDF {i + 1}', fill='black')
        fn = out / f'sheet_{tag}_{start + 1:03}.jpg'; sheet.save(fn, quality=85); sheets.append(fn.name)
    for spec in a.pages:
        t, n = spec.split(':')
        if t == tag:
            d[int(n) - 1].get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False).save(out / f'{tag}_{int(n):03}.png')
    report[tag] = {'pages': len(d), 'body_pages': body_pages, 'contact_sheets': sheets,
                   'text_outside_margin': outside, 'sparse_body_pages': sparse}
    print(tag, len(d), 'pages; outside-margin blocks:', len(outside), '; sparse pages:', sparse, flush=True)
    d.close()
(ROOT / 'qa/V50_VISUAL_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
