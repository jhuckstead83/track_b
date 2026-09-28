#!/usr/bin/env python3
"""Site check for TN Postmaster page anchors (PP277 section 2, PP279 section 3.1).

Every #page=N link into a v5.2 volume must land on a named target listed in anchors_v5_2.json,
so a re-pagination fails here instead of silently landing on the wrong page. Run from the site root:
    python3 research/postmaster/check_anchors_v5_2.py
"""
import json, os, re, sys
A = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anchors_v5_2.json'), encoding='utf-8'))
pages = {A['reading']['file']: {t['page']: n for n, t in A['reading']['targets'].items()},
         A['dossier']['file']: {t['page']: n for n, t in A['dossier']['targets'].items()}}
pat = re.compile(r'/papers/(TN_Postmaster_Volume_I_v5_2_(?:READING_VOLUME|TECHNICAL_DOSSIER)\.pdf)#page=(\d+)')
seen, bad = 0, []
for d, _, fs in os.walk('.'):
    for f in fs:
        if not f.endswith(('.html', '.json')) or re.search(r'MANIFEST|VALIDATION|release-v', f): continue
        p = os.path.join(d, f); s = open(p, encoding='utf-8', errors='replace').read()
        for m in pat.finditer(s):
            seen += 1
            if int(m.group(2)) not in pages[m.group(1)]: bad.append((p, m.group(0)))
print(json.dumps({'anchors_checked': seen, 'named_targets': sum(len(v) for v in pages.values()), 'unnamed': bad}))
sys.exit(1 if bad or not seen else 0)
