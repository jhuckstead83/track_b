#!/usr/bin/env python3
"""Site check for TN Postmaster v5.2 page anchors (PP277 section 2, PP279 section 3.1, PP286 section 0).

Three checks, and the report says which of them ran:

1. links    Every #page=N link into a v5.2 volume names a page listed in anchors_v5_2.json.
            This catches a hand-edited href. On its own it cannot catch a re-pagination,
            because the map and the links were written from the same build.
2. binding  The installed PDF in papers/ has the SHA-256 the map was built against, and so does
            qa/BUILD_BINDING.json inside papers/TN_Postmaster_Volume_I_v5_2_SOURCE.zip.
            A rebuilt PDF therefore fails here until the map is regenerated from it.
3. pages    With PyMuPDF installed, each target's heading is found again in the installed PDF,
            by the rule that made the map (first line after the front matter that starts with
            the heading, in a heading-sized font), and must sit on the page the map records.

Only checks 2 and 3 say anything about pagination, and they need the papers payload installed.
Without it the report reads "not run" for them, and a pass means link integrity only.

Run from the site root:
    python3 research/postmaster/check_anchors_v5_2.py                 # runs what it can
    python3 research/postmaster/check_anchors_v5_2.py --require-pdfs  # fails unless all three ran
"""
import hashlib, json, os, re, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, 'anchors_v5_2.json'), encoding='utf-8'))
VOLS = {'reading': A['reading'], 'dossier': A['dossier']}
PAPERS = 'papers'
SOURCE_ZIP = os.path.join(PAPERS, 'TN_Postmaster_Volume_I_v5_2_SOURCE.zip')
BINDING_IN_ZIP = 'TN_Postmaster_Volume_I_v5_2/qa/BUILD_BINDING.json'
# Minimum heading font size per target: the rule extract_anchors.py used to write the map.
MIN_SIZE = {'start_here': 16, 'part_I': 16, 'part_II': 16, 'source_note_R6A': 12, 'part_III': 16,
            'folded_state_contract': 11, 'part_IV': 16, 'R12': 12, 'part_V': 16, 'part_VI': 16,
            'part_VII': 16, 'R23': 12, 'R24': 12, 'part_VIII': 16, 'summary': 16}
FRONT = 4  # front-matter pages (title, contents) never hold a target

report, failures = {}, []

# 1. links
pages = {v['file']: {t['page'] for t in v['targets'].values()} for v in VOLS.values()}
pat = re.compile(r'/papers/(TN_Postmaster_Volume_I_v5_2_(?:READING_VOLUME|TECHNICAL_DOSSIER)\.pdf)#page=(\d+)')
seen, unnamed = 0, []
for d, _, fs in os.walk('.'):
    for f in fs:
        if not f.endswith(('.html', '.json')) or re.search(r'MANIFEST|VALIDATION|release-v', f): continue
        p = os.path.join(d, f); s = open(p, encoding='utf-8', errors='replace').read()
        for m in pat.finditer(s):
            seen += 1
            if int(m.group(2)) not in pages[m.group(1)]: unnamed.append((p, m.group(0)))
report['links'] = {'anchors_checked': seen, 'named_targets': sum(len(v['targets']) for v in VOLS.values()),
                   'unnamed': unnamed}
if unnamed or not seen: failures.append('links')

# 2. binding
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
installed = {k: os.path.join(PAPERS, v['file']) for k, v in VOLS.items()}
if all(os.path.isfile(p) for p in installed.values()):
    rows = {}
    if os.path.isfile(SOURCE_ZIP):
        with zipfile.ZipFile(SOURCE_ZIP) as z:
            for r in json.loads(z.read(BINDING_IN_ZIP)):
                rows[os.path.basename(r['pdf'])] = r['pdf_sha256']
    b = {}
    for k, v in VOLS.items():
        got = sha(installed[k])
        b[k] = {'map': v['sha256'][:16], 'installed_pdf': got[:16],
                'build_binding': rows.get(v['file'], 'no source zip')[:16],
                'ok': got == v['sha256'] and rows.get(v['file']) == v['sha256']}
    report['binding'] = b
    if not all(x['ok'] for x in b.values()): failures.append('binding')
else:
    report['binding'] = 'not run: papers/ does not hold both v5.2 PDFs'

# 3. pages
try:
    import pymupdf
except ImportError:
    pymupdf = None
if pymupdf is None:
    report['pages'] = 'not run: PyMuPDF is not installed'
elif isinstance(report['binding'], str):
    report['pages'] = 'not run: papers/ does not hold both v5.2 PDFs'
else:
    moved = []
    for k, v in VOLS.items():
        doc = pymupdf.open(installed[k])
        if doc.page_count != v['pages']: moved.append((k, 'page count', v['pages'], doc.page_count))
        L = []
        for i in range(doc.page_count):
            for blk in doc[i].get_text('dict')['blocks']:
                for ln in blk.get('lines', []):
                    t = ''.join(s['text'] for s in ln['spans']).strip()
                    if t: L.append((i + 1, t, max(s['size'] for s in ln['spans'])))
        for name, t in v['targets'].items():
            if name == 'reference_11':
                ref = min((p for p, s, z in L if p > FRONT and s.startswith('References') and z >= 16), default=None)
                hit = next((p for p, s, z in L if ref and p >= ref and s.startswith('11. ')), None)
            else:
                size = MIN_SIZE.get(name, 20)
                hit = next((p for p, s, z in L if p > FRONT and s.startswith(t['heading']) and z >= size), None)
            if hit != t['page']: moved.append((k, name, t['page'], hit))
    report['pages'] = {'targets_checked': sum(len(v['targets']) for v in VOLS.values()), 'moved': moved}
    if moved: failures.append('pages')

ran = [c for c in ('links', 'binding', 'pages') if not isinstance(report[c], str)]
if '--require-pdfs' in sys.argv and len(ran) < 3: failures.append('require-pdfs')
report['checks_run'] = ran
report['result'] = 'FAIL: ' + ', '.join(failures) if failures else 'PASS (' + ', '.join(ran) + ')'
print(json.dumps(report, indent=1))
sys.exit(1 if failures else 0)
