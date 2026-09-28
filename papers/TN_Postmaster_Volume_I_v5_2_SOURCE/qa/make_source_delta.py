#!/usr/bin/env python3
"""Write the v5.1 -> v5.2 source diffs, qa/SOURCE_DELTA.json and the evidence checksums."""
from pathlib import Path
import difflib, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

rows = []
for kind in ['READING_VOLUME', 'TECHNICAL_DOSSIER']:
    old = ROOT / 'provenance/v5_1/src' / f'TN_Postmaster_Volume_I_v5_1_{kind}.md'
    new = ROOT / 'src' / f'TN_Postmaster_Volume_I_v5_2_{kind}.md'
    a = old.read_text(encoding='utf-8').splitlines(keepends=True)
    b = new.read_text(encoding='utf-8').splitlines(keepends=True)
    diff = list(difflib.unified_diff(a, b, f'v5_1/{old.name}', f'v5_2/{new.name}', n=2))
    (ROOT / 'qa' / f'{kind}_V52.diff').write_text(''.join(diff), encoding='utf-8', newline='\n')
    rows.append({'document': kind, 'source_v51_sha256': sha(old), 'source_v52_sha256': sha(new),
                 'added_lines': sum(1 for l in diff if l.startswith('+') and not l.startswith('+++')),
                 'removed_lines': sum(1 for l in diff if l.startswith('-') and not l.startswith('---'))})
for tag in ['reading', 'dossier']:
    old = ROOT / 'provenance/v5_1/src' / f'preamble_v51_{tag}.tex'
    new = ROOT / 'src' / f'preamble_v52_{tag}.tex'
    diff = list(difflib.unified_diff(old.read_text(encoding='utf-8').splitlines(keepends=True),
                                     new.read_text(encoding='utf-8').splitlines(keepends=True),
                                     old.name, new.name, n=0))
    rows.append({'document': f'preamble_{tag}', 'source_v51_sha256': sha(old), 'source_v52_sha256': sha(new),
                 'changed_lines': [l.rstrip('\n') for l in diff if l[:1] in '+-' and l[:3] not in ('+++', '---')]})
(ROOT / 'qa/SOURCE_DELTA.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

ev = ROOT / 'provenance/v5_2/evidence'
files = sorted(p for p in ev.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt')
(ev / 'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ev).as_posix()}\n' for p in files),
                                   encoding='utf-8', newline='\n')
print(json.dumps(rows, indent=2, ensure_ascii=False))
print(f'{len(files)} evidence files hashed')
