#!/usr/bin/env python3
"""Verify the active publication package against PACKAGE_MANIFEST.json and SHA256SUMS.txt.

Optionally checks the separately published PDFs recorded under `delivered_pdfs`:
pass --pdf-dir DIR (or keep them in output/pdf/) and their SHA-256 is compared too.
"""
from pathlib import Path
import argparse, hashlib, json, sys
R = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('--pdf-dir', default=None)
args = ap.parse_args()


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def safe(name):
    p = (R / name).resolve()
    if not p.is_relative_to(R):
        raise ValueError('Unsafe manifest path: ' + name)
    return p


try:
    m = json.loads((R / 'PACKAGE_MANIFEST.json').read_text()); failures = []
    for x in m['files']:
        p = safe(x['path']); size = x.get('bytes', x.get('size'))
        if not p.is_file() or p.stat().st_size != size or digest(p) != x['sha256']:
            failures.append(x['path'])
    sums = 0
    for line in (R / 'SHA256SUMS.txt').read_text().splitlines():
        if not line:
            continue
        expected, name = line.split('  ', 1); p = safe(name); sums += 1
        if not p.is_file() or digest(p) != expected:
            failures.append('checksum: ' + name)
    pdf_report = []
    for rec in m.get('delivered_pdfs', []):
        where = [Path(args.pdf_dir) / rec['filename']] if args.pdf_dir else []
        where.append(R / 'output/pdf' / rec['filename'])
        found = next((p for p in where if p.is_file()), None)
        if found is None:
            pdf_report.append({'filename': rec['filename'], 'status': 'not present (published separately)'})
        elif digest(found) == rec['sha256']:
            pdf_report.append({'filename': rec['filename'], 'status': 'PASS'})
        else:
            pdf_report.append({'filename': rec['filename'], 'status': 'FAIL'})
            failures.append('delivered pdf: ' + rec['filename'])
    print(json.dumps({'status': 'FAIL' if failures else 'PASS', 'version': m.get('version'),
                      'manifest_members': len(m['files']), 'checksum_members': sums,
                      'delivered_pdfs': pdf_report, 'failures': failures}, indent=2))
    sys.exit(1 if failures else 0)
except (OSError, ValueError, KeyError) as e:
    print('Verification failed: ' + str(e), file=sys.stderr); sys.exit(2)
