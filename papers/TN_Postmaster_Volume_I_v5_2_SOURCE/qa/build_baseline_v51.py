#!/usr/bin/env python3
"""Rebuild the v5.1 Reading Volume from provenance/v5_1 in this environment.

Page counts depend on the pandoc/TeX versions. v5.1 recorded 101 Reader pages
under pandoc 3.x and TeX Live 2025. Running this next to build_release.py lets
the v5.2 count be compared like-for-like. Output: qa/BASELINE_V51.json.
Usage: python3 qa/build_baseline_v51.py [reading|dossier|both]
"""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tmp' / 'baseline_v51'
which = sys.argv[1] if len(sys.argv) > 1 else 'reading'

if BASE.exists():
    shutil.rmtree(BASE)
(BASE / 'src').mkdir(parents=True)
(BASE / 'qa').mkdir()
for p in (ROOT / 'provenance/v5_1/src').glob('*'):
    if p.suffix in ('.md', '.tex') and not p.name.startswith('compiled_'):
        shutil.copy2(p, BASE / 'src' / p.name)
shutil.copy2(ROOT / 'src/facsimile_pages_11_13.pdf', BASE / 'src/facsimile_pages_11_13.pdf')
shutil.copytree(ROOT / 'figures', BASE / 'figures')
script = (ROOT / 'qa/build_release.py').read_text(encoding='utf-8')
script = script.replace('TN_Postmaster_Volume_I_v5_2_', 'TN_Postmaster_Volume_I_v5_1_').replace('preamble_v52_', 'preamble_v51_')
(BASE / 'qa/build_release.py').write_text(script, encoding='utf-8')
subprocess.run([sys.executable, str(BASE / 'qa/build_release.py'), which], cwd=BASE, check=True)
out = {}
for tag in (['reading', 'dossier'] if which == 'both' else [which]):
    r = json.loads((BASE / 'qa' / f'BUILD_{tag.upper()}.json').read_text())
    out[tag] = {'pages': r['pages'], 'recorded_v51_pages': {'reading': 101, 'dossier': 281}[tag]}
(ROOT / 'qa/BASELINE_V51.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
