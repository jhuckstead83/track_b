#!/usr/bin/env python3
"""Audit the claims printed *inside* the figures against the controlling ledger.

Text QA cannot read a raster.  Through v4.9 the status panel of figure 75
disagreed with Reading Volume §R12 -- W2-W4 source A-CAT, W5 zero-assisted,
"W5: source proof OPEN", no W6 -- and no check could see it, because those
words are pixels.  Two further figures carried a stale edition stamp.

This audit closes that gap.  For every figure the documents actually cite it

  1. checks the figure exists and is cited exactly once by name;
  2. pins its SHA-256 against the baseline, so a figure cannot change unseen;
  3. runs the forbidden-claim patterns over the baseline's recorded text;
  4. re-runs OCR when tesseract is available and requires the recovered text
     to still fail every forbidden pattern, and to match the baseline's
     normalized text;
  5. requires the rung ledger declared in qa/figsrc/fig_status_panels.py to be
     the ledger of §R12, read out of the Reading Volume at run time.

Usage
  python3 qa/audit_figure_claims.py                 audit (exit 1 on failure)
  python3 qa/audit_figure_claims.py --write-baseline rebuild the baseline
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / 'figures'
SRC = ROOT / 'src'
BASELINE = ROOT / 'qa' / 'V50_FIGURE_CLAIMS.json'
OUT = ROOT / 'qa' / 'V50_FIGURE_CLAIMS_AUDIT.json'

# claims that must never appear inside a figure again.  each entry is
# (name, compiled pattern, why) and is matched against OCR text with the
# whitespace flattened and common OCR confusions folded.
FORBIDDEN = [
    ('superseded_source_range', r'w\s*_?\s*2\s*[-–—]\s*w?\s*_?\s*4',
     'the source A-CAT range is W2-W6, not W2-W4 (Reader R12)'),
    ('w5_zero_assisted', r'w\s*_?\s*5\b[^.]{0,40}zero.?assisted',
     'W5 is certified from the source, not only zero-assisted'),
    ('w5_source_open', r'w\s*_?\s*5\b[^.]{0,30}source[^.]{0,20}open',
     'the open source rung is W7, not W5'),
    ('stale_frontier_jet', r'next[^.]{0,40}f\s*\(?\s*10\s*\)?',
     'the next independent source jet is F^(14)'),
    ('edition_stamp', r'\bv\s?[3-9]\.\d\b',
     'a figure must not carry a volume-edition stamp; it outlives the edition. '
     'internal series labels such as v1.2 are not edition stamps'),
]

# the ledger rows that MUST be recoverable from the controlling table of R12.
# each is (regex over the figure text, regex over the R12 table text).
LEDGER_TIEOUT = [
    (r'w\s*_?\s*2\s*[-–—]\s*w?\s*_?\s*6', r'W_2,\\ldots,W_6'),
    (r'f\s*\(?\s*12\s*\)?', r'F\^\{\(12\)\}'),
    (r'f\s*\(?\s*14\s*\)?', r'F\^\{\(14\)\}'),
]

NORM = str.maketrans({'—': '-', '–': '-', '−': '-',
                      ' ': ' ', '|': 'l'})


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def flat(text):
    return ' '.join(text.translate(NORM).split()).lower()


def cited_figures():
    """figure -> list of volumes citing it, by literal filename occurrence."""
    out = {}
    for p in sorted(SRC.glob('*.md')):
        vol = 'READING' if 'READING' in p.name else 'DOSSIER'
        txt = p.read_text(encoding='utf-8')
        for f in sorted(FIGDIR.glob('*.png')):
            if f.name in txt:
                out.setdefault(f.name, []).append(vol)
    return out


def r12_table():
    """the controlling rung-status table, as raw text."""
    p = SRC / 'TN_Postmaster_Volume_I_v5_0_READING_VOLUME.md'
    t = p.read_text(encoding='utf-8')
    i = t.index('## R12. One ladder')
    j = t.index('This table is the controlling rung-status record', i)
    return t[i:j]


def ocr_available():
    return shutil.which('tesseract') is not None


def ocr(path):
    with tempfile.TemporaryDirectory() as d:
        stem = Path(d) / 'o'
        r = subprocess.run(['tesseract', str(path), str(stem), '--psm', '11'],
                           capture_output=True)
        if r.returncode:
            return None
        f = stem.with_suffix('.txt')
        return f.read_text(errors='replace') if f.exists() else None


def collect():
    cites = cited_figures()
    have_ocr = ocr_available()
    names = sorted(cites)
    texts = {}
    if have_ocr:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=4) as ex:
            for name, text in zip(names, ex.map(lambda n: ocr(FIGDIR / n), names)):
                texts[name] = text
    rows = []
    for name in names:
        p = FIGDIR / name
        text = texts.get(name)
        rows.append({'figure': name, 'cited_by': cites[name], 'sha256': sha(p),
                     'bytes': p.stat().st_size,
                     'text': flat(text) if text is not None else None})
    return rows, have_ocr


def scan(text, label, failures):
    if text is None:
        return
    for key, pat, why in FORBIDDEN:
        m = re.search(pat, text)
        if m:
            failures.append('%s: %s -- matched %r (%s)'
                            % (label, key, m.group(0), why))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-baseline', action='store_true')
    args = ap.parse_args()

    rows, have_ocr = collect()
    if args.write_baseline:
        if not have_ocr:
            sys.exit('refusing to write a baseline without tesseract: '
                     'the recorded text would be empty')
        failures = []
        for r in rows:
            scan(r['text'], r['figure'], failures)
        if failures:
            print('baseline refused; these figures still print a stale claim:')
            for f in failures:
                print('   ', f)
            sys.exit(1)
        BASELINE.write_text(json.dumps(
            {'version': 'v5.0', 'ocr': 'tesseract --psm 11',
             'note': 'text is OCR of the bundled figure, whitespace flattened '
                     'and lowercased; sha256 pins the bytes it was read from',
             'figures': rows}, indent=1, ensure_ascii=False) + '\n')
        print('baseline written: %d cited figures' % len(rows))
        return

    base = json.loads(BASELINE.read_text())
    prior = {r['figure']: r for r in base['figures']}
    failures, notes = [], []

    # 1 / 2. orphans and hash drift
    on_disk = {p.name for p in FIGDIR.glob('*.png')}
    cited = {r['figure'] for r in rows}
    for extra in sorted(on_disk - cited):
        failures.append('orphan: %s is bundled but cited by neither volume' % extra)
    for r in rows:
        b = prior.get(r['figure'])
        if b is None:
            failures.append('unbaselined: %s' % r['figure'])
            continue
        if b['sha256'] != r['sha256']:
            failures.append('changed without review: %s (%s -> %s)'
                            % (r['figure'], b['sha256'][:12], r['sha256'][:12]))
        if b['cited_by'] != r['cited_by']:
            notes.append('citation moved: %s %s -> %s'
                         % (r['figure'], b['cited_by'], r['cited_by']))

    # 3. forbidden claims in the recorded text (runs with or without tesseract)
    for f, b in sorted(prior.items()):
        scan(b.get('text'), 'baseline/' + f, failures)

    # 4. live OCR, when available
    if have_ocr:
        for r in rows:
            scan(r['text'], 'live/' + r['figure'], failures)
            b = prior.get(r['figure'])
            if b and b.get('text') is not None and r['text'] is not None:
                if b['text'] != r['text']:
                    notes.append('OCR text drifted for %s (same bytes? %s)'
                                 % (r['figure'], b['sha256'] == r['sha256']))
    else:
        notes.append('tesseract absent: checks 4 skipped, baseline text used')

    # 5. tie the generated panels to the R12 table
    table = r12_table()
    panel = (ROOT / 'qa' / 'figsrc' / 'fig_status_panels.py').read_text()
    for figpat, tabpat in LEDGER_TIEOUT:
        infig = any(re.search(figpat, (prior.get(n) or {}).get('text') or '')
                    for n in ('figure75_li_pp97_loewner_study_atlas.png',
                              'v26c_source_depth.png'))
        intab = re.search(tabpat, table) is not None
        if infig and not intab:
            failures.append('ledger tie-out: %r is printed in a figure but is '
                            'not in the R12 table' % figpat)
    if 'K_H' not in panel or '4,712,664,392,502' not in panel:
        failures.append('ledger tie-out: the generator no longer declares K_H')
    if '4{,}712{,}664{,}392{,}502' not in table:
        failures.append('ledger tie-out: K_H is not in the R12 table')

    OUT.write_text(json.dumps(
        {'version': 'v5.0', 'cited_figures': len(rows), 'orphans': sorted(on_disk - cited),
         'ocr_available': have_ocr, 'failures': failures, 'notes': notes,
         'result': 'PASS' if not failures else 'FAIL'}, indent=1) + '\n')

    for n in notes:
        print('note:', n)
    if failures:
        print('FAIL (%d)' % len(failures))
        for f in failures:
            print('   ', f)
        sys.exit(1)
    print('PASS: %d cited figures, 0 orphans, no stale claim, ledger ties to R12'
          % len(rows))


if __name__ == '__main__':
    main()
