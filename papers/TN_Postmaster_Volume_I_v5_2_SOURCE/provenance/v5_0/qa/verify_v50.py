#!/usr/bin/env python3
"""v5.0 publication verifier.

Binds the active v5.0 sources to the built PDFs, checks the page ceilings and
the recorded page counts, requires the update audit and all sixteen
mathematical replays to pass -- including the two source-rung certificate runs
and their cross-backend comparison -- and checks the status firewalls in the
PDF text itself. When the PDFs have been moved out of the package (PP251 §5),
pass --pdf-dir to point at the separately published files.
"""
from pathlib import Path
import argparse, hashlib, json, re
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('--pdf-dir', default=None, help='directory holding the two v5.0 PDFs (default: as recorded in the build bindings)')
args = ap.parse_args()
checks = []


def ck(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


rv = ROOT / 'src/TN_Postmaster_Volume_I_v5_0_READING_VOLUME.md'
td = ROOT / 'src/TN_Postmaster_Volume_I_v5_0_TECHNICAL_DOSSIER.md'
r = rv.read_text(); t = td.read_text()
rows = json.loads((ROOT / 'qa/BUILD_BINDING.json').read_text())
ck('two build bindings', len(rows) == 2 and {x['tag'] for x in rows} == {'reading', 'dossier'})
RECORDED = {'reading': 98, 'dossier': 279}      # pages recorded for this edition
CEILING = {'reading': 99, 'dossier': 299}       # standing hard ceilings
TARGET = {'reading': 90, 'dossier': 275}        # standing targets (informational)
texts = {}
for row in rows:
    tag = row['tag']; src = ROOT / row['source']
    pdf = (Path(args.pdf_dir) / Path(row['pdf']).name) if args.pdf_dir else ROOT / row['pdf']
    ck(f'{tag}: v5.0 source path', 'v5_0' in str(src))
    ck(f'{tag}: source hash bound', sha(src) == row['src_sha256'])
    ck(f'{tag}: preamble hash bound', sha(ROOT / f'src/preamble_v50_{tag}.tex') == row['preamble_sha256'])
    ck(f'{tag}: pdf present', pdf.is_file(), str(pdf))
    if not pdf.is_file():
        continue
    ck(f'{tag}: pdf hash bound', sha(pdf) == row['pdf_sha256'])
    ck(f'{tag}: zero undefined refs', row['undefined_refs'] == 0)
    ck(f'{tag}: zero missing characters', row['missing_characters'] == 0)
    ck(f'{tag}: zero overfull boxes', row['overfull_boxes_pt'] == [])
    with fitz.open(pdf) as doc:
        n = len(doc)
        ck(f'{tag}: page count equals the recorded count', n == RECORDED[tag], n)
        ck(f'{tag}: under the hard ceiling', n <= CEILING[tag], (n, CEILING[tag], 'target', TARGET[tag]))
        full = '\n'.join(p.get_text() for p in doc)
        texts[tag] = ' '.join(full.split())
        sample = ' '.join(doc[i].get_text() for i in range(min(10, n)))
        ck(f'{tag}: v5.0 visible', 'v5.0' in sample)
        ck(f'{tag}: RH open visible', 'RH OPEN' in sample.upper() or 'RIEMANN HYPOTHESIS REMAINS OPEN' in sample.upper())
        ck(f'{tag}: PDF metadata subject says v5.0', 'v5.0' in (doc.metadata.get('subject') or ''))
ck('combined page count', sum(x['pages'] for x in rows) == sum(RECORDED.values()), sum(x['pages'] for x in rows))

up = json.loads((ROOT / 'qa/V50_UPDATE_AUDIT.json').read_text())
ck('v5.0 update audit passes', up['passed'] == up['total'], up.get('failed'))
ledger = json.loads((ROOT / 'qa/MATH_REPLAY_LEDGER.json').read_text())
ck('sixteen mathematical replays recorded', len(ledger) == 16, len(ledger))
names = [x['name'] for x in ledger]
ck('the source-rung certificate is re-executed by the replay suite',
   {'source_rungs_arb', 'source_rungs_decimal', 'source_rungs_cross_backend'} <= set(names)
   and names.index('source_rungs_cross_backend') > names.index('source_rungs_decimal')
   and len(set(names)) == 16)
ck('the v5.0 replays are in the suite',
   {'r10c_orbit', 'figure_claims'} <= set(names), sorted(set(names)))
ck('the R10C replay is exact and passing',
   json.loads((ROOT / 'qa/R10C_ORBIT.json').read_text())['result'] == 'PASS')
ck('the figure-claims audit is passing with no orphan figure',
   (lambda f: f['result'] == 'PASS' and not f['orphans'])(
       json.loads((ROOT / 'qa/V50_FIGURE_CLAIMS_AUDIT.json').read_text())))
ck('all mathematical replays exit zero', all(x['exit_code'] == 0 for x in ledger), [(x['name'], x['exit_code']) for x in ledger if x['exit_code']])
for x in ledger:
    ck(f"replay script hash current: {x['name']}", sha(ROOT / x['command'][1]) == x['script_sha256'])
gb = json.loads((ROOT / 'qa/GAMMA_BRIDGE.json').read_text())
ck('gamma-bridge receipt: all checks pass', gb['passed'] == gb['total'] and gb['total'] >= 57, (gb['passed'], gb['total']))
ck('gamma-bridge receipt carries certified enclosures', gb.get('certified_enclosures', {}).get('prec_bits') == 256)

# firewalls in the Markdown masters
ck('single master status legend', r.count('\\statuslegend') == 1 and t.count('\\statuslegend') == 0)
ck('R25 consolidated no-go ledger', '## R25. No-go ledger and the surviving corridor' in r)
ck('R23 plural route frontier', '## R23. The first unsupported lines, by route' in r)
ck('R13A two classical inputs', r'$\zeta(1+it)\ne0$' in r and 'Finiteness of the zero count below any fixed height' in r)
ck('source frontier W1-W6 and W7 open', r'$W_1,\ldots,W_6>0$ for all $x>0$, from the source' in r
   and r'$W_7\rightsquigarrow F^{(14)}$ from the independent source' in r)
cross = json.loads((ROOT / 'qa/source_rungs/CROSS_BACKEND.json').read_text())
ck('source-rung certificate: cross-backend comparison passes', cross['status'] == 'PASS')
for name in ('RECEIPT_arb.json', 'RECEIPT_decimal.json', 'RECEIPT_arb_second.json', 'RECEIPT_decimal_second.json'):
    rec = json.loads((ROOT / 'qa/source_rungs' / name).read_text())
    ck('source-rung receipt PASS: ' + name, rec['status'] == 'PASS'
       and sorted(x['k'] for x in rec['finite']) == [2, 3, 4, 5, 6])
ck('stale W4-open sentence absent', 'Global fourth-rung positivity' not in r + t and '$W_4(x)>0$ remains open' not in r + t)
for name, text in [('reading', r), ('dossier', t)]:
    tags = re.findall(r'\\tag\{([^}]+)\}', text)
    ck(f'{name}: unique equation tags', len(tags) == len(set(tags)))

# firewalls and new material in the rendered PDFs
if 'reading' in texts:
    x = texts['reading']
    ck('Reading PDF: R4A present', "R4A. Euler’s constant on the triangular coordinate" in x or "R4A. Euler's constant on the triangular coordinate" in x)
    ck('Reading PDF: lineage table and glossary present', 'Where this work sits in the classical literature' in x and 'Working vocabulary' in x)
    ck('Reading PDF: status legend words present', all(w in x for w in ['PROVED', 'CERTIFIED', 'RH-EQUIVALENT', 'OPEN', 'EVIDENCE']))
    ck('Reading PDF: W7 source row and RH OPEN footer', 'from the independent source' in x and 'RH OPEN' in x)
    ck('Reading PDF: the rung status is stated once, without run notes',
       'This is the position, stated once' in x and 'two independent arithmetic backends' in x
       and 'no later than 23 August 2026' not in x and 'still owed' not in x and 'not retained' not in x)
    ck('Reading PDF: recomputed C bounds printed', '8.00193804616020' in x and '8.00193804616021' in x)
    ck('Reading PDF: references run to 120', re.search(r'120\. D\. W\. DeTemple and S\.-H\. Wang', x) is not None)
if 'dossier' in texts:
    x = texts['dossier']
    ck('Dossier PDF: §96A present', "96A. Euler’s constant" in x or "96A. Euler's constant" in x)
    ck('Dossier PDF: one source-rung certificate, no run notes',
       'One certificate for the source rungs' in x and 'source_rungs_decimal.py' in x
       and 'still owed' not in x and 'not rerun' not in x and 'not retained' not in x)
    drow = [row for row in rows if row['tag'] == 'dossier'][0]
    ck('Dossier PDF: three facsimile pages appended and bound', drow['pages'] == drow['body_pages'] + 3
       and drow.get('facsimile_sha256') == sha(ROOT / 'src/facsimile_pages_11_13.pdf'))

out = {'total': len(checks), 'passed': sum(c['passed'] for c in checks),
       'failed': [c['name'] for c in checks if not c['passed']], 'checks': checks}
(ROOT / 'qa/V50_VERIFY.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'total': out['total'], 'passed': out['passed'], 'failed': out['failed']}, indent=2, ensure_ascii=False))
raise SystemExit(0 if not out['failed'] else 1)
