#!/usr/bin/env python3
"""v5.0 logic/update audit for the two Markdown masters.

Carries every v4.8 gate forward and adds the v5.0 gates: the consolidated
source-rung statement (one row in the master key, one table in Reader §R12,
one certificate in Dossier §74A), the removal of the per-certificate run
notes, and the bundled certificate itself -- its scripts, its four receipts
and the two cross-backend comparisons are checked here against the printed
thresholds and constants, including an independent re-verification of the
partitions from the receipt data.
"""
from pathlib import Path
from decimal import Context, Decimal, ROUND_FLOOR
from fractions import Fraction
import hashlib, json, re

WIDE = Context(prec=80, rounding=ROUND_FLOOR, Emin=-10 ** 9, Emax=10 ** 9)


def lower_of(text):
    """Lower endpoint of a receipt value: '[mid +/- rad]' or a plain decimal."""
    x = text.strip()
    if x.startswith('[') and '+/-' in x:
        mid, rad = x[1:-1].split('+/-')
        return WIDE.subtract(Decimal(mid.strip()), Decimal(rad.strip()))
    return Decimal(x.strip('[]').strip())

ROOT = Path(__file__).resolve().parents[1]
rv = ROOT / 'src/TN_Postmaster_Volume_I_v5_0_READING_VOLUME.md'
td = ROOT / 'src/TN_Postmaster_Volume_I_v5_0_TECHNICAL_DOSSIER.md'
r = rv.read_text(); t = td.read_text(); both = r + '\n' + t
flat = ' '.join(r.split()); tflat = ' '.join(t.split()); bflat = flat + ' ' + tflat
checks = []


def ck(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def body(text):
    return text.split('\n# References')[0]


def refsec(text):
    return text.split('\n# References')[-1]


# ---------------------------------------------------------------- carried v4.7 gates
ck('single statuslegend across active documents', r.count('\\statuslegend') == 1 and t.count('\\statuslegend') == 0,
   (r.count('\\statuslegend'), t.count('\\statuslegend')))
ck('master status heading', '## Master status key — where this volume actually stands' in r)
ck('one source-rung row in the master key', r'$W_1,\ldots,W_6>0$ for all $x>0$, from the source' in r
   and r'$W_2,\ldots,W_6>0$ for all $x>0$, from the source |' not in r)
ck('W7 F14 open in master key', r'$W_7\rightsquigarrow F^{(14)}$ from the independent source' in r)
ck('Dossier points to master key', 'single master key in the Reading Volume' in t)
stale = [
    'W_5\\rightsquigarrow F^{(10)}\\ \text{by an independent source proof}',
    'first four of those need no zero data at all',
    'through the fourth, global matrix order eight',
    '$W_1,\\ldots,W_4>0$ from the source',
    'source-side $F^{(10)}$ inequality',
    'only its independent Gamma--prime proof remains open',
    'independent fifth-rung source certificate is a separate finite-order task',
    'first five differential rows',
]
for s in stale:
    ck('stale absent: ' + s[:48], s not in both)
ck('Part IV states the position once', r'$W_1,\ldots,W_6>0$ is proved from the source alone' in flat
   and 'by one bundled certificate at the next five' in flat)
ck('R13 F14 frontier', 'source-side $F^{(14)}$ inequality' in r)
ck('Dossier first six differential rows', 'first six differential rows' in t)
ck('Dossier seventh rung frontier', 'independent seventh-rung source certificate' in t and r'$W_7\rightsquigarrow F^{(14)}$' in t)
ck('front says one line per route', 'one line per route, and no reduction between the routes is known' in flat)
ck('R23 plural frontier title', '## R23. The first unsupported lines, by route' in r)
ck('R23 no proved universal reduction', 'There is no proved reduction of all surviving routes to one source inequality.' in r)
ck('implication lattice present', '**Implication lattice: direct arrows only.**' in r)
ck('implication lattice status equivalent', '| all Widder signs (R.4) | **equivalent** |' in r)
ck('implication lattice status sufficient', '| either curvature/boundary bound in (23.4) | **sufficient** |' in r)
ck('implication lattice W7 necessary not sufficient', '**necessary under RH; not sufficient**' in r)
ck('direct row-energy equivalence', r'$\Longleftrightarrow$ (BE.3)' in r)
ck('direct Loewner to Widder arrow', r'$\Longrightarrow$ the Stieltjes/Widder condition (R.4)' in r)
ck('R13A names zeta boundary nonvanishing', r'$\zeta(1+it)\ne0$' in r)
ck('R13A names finite zero count', 'Finiteness of the zero count below any fixed height' in r)
ck('R13A unbounded height conclusion', r'$|\Im\rho_n|\to\infty$' in r)
ck('R13A degrading factor tends one', r'$4\gamma_n^2/(4\gamma_n^2+1)\to1$' in r)
ck('Part VIII exists', '# Part VIII. What this approach cannot do' in r)
ck('R25 no-go ledger exists', '## R25. No-go ledger and the surviving corridor' in r)
for token in ['Theorem 22A.1', '§48C', '§49 and §69', '§161', 'Theorems 107.1 and 112.1', '§§155F–155G and (H07)']:
    ck('R25 pointer ' + token, token in r[r.index('# Part VIII.'):])
ck('R25 scope firewall', 'none is evidence for RH or against it' in flat)
ck('R22 has one NO-GO ledger row', '| NO-GO ledger |' in r)
ck('R22 old realization row removed', '| Realization constraints |' not in r)
ck('R22 old rung-test row removed', '| Rung tests as Weil functionals |' not in r)
ck('no k-star detection theorem promoted', 'k^*(\\rho)' not in r and 'k^*(\rho)' not in r)
ck('no claimed c1 gamma detection law', 'c_1\\,\\gamma' not in r)
ck('RH open reader', 'The Riemann hypothesis remains open' in r)
ck('RH open dossier', 'Riemann hypothesis is open' in t)
ck('W7 remains open text', 'all-$x$ source sign remains open' in t or 'first open source rung' in t)
ck('stale global W4-open sentence absent', 'Global fourth-rung positivity' not in both and '$W_4(x)>0$ remains open' not in both)
for name, text in [('reading', r), ('dossier', t)]:
    tags = re.findall(r'\\tag\{([^}]+)\}', text)
    heads = re.findall(r'^## ((?:R)?\d+[A-Z]*)\.', text, re.M)
    ck(f'{name}: equation tags unique', len(tags) == len(set(tags)), [x for x in set(tags) if tags.count(x) > 1])
    ck(f'{name}: heading ids unique', len(heads) == len(set(heads)), [x for x in set(heads) if heads.count(x) > 1])
    ck(f'{name}: no control chars', not any(ord(c) < 32 and c not in '\n\r\t' for c in text))
ck('global equation tags unique across both documents',
   len(set(re.findall(r'\\tag\{([^}]+)\}', r)) & set(re.findall(r'\\tag\{([^}]+)\}', t))) == 0)
ck('R.2 tag occurs once', r.count(r'\tag{R.2}') == 1, r.count(r'\tag{R.2}'))
ck('R25 section occurs once', r.count('## R25.') == 1)

# ---------------------------------------------------------------- v5.0 version strings
ck('v5.0 in both YAML subtitles', '-- v5.0"' in r[:400] and '-- v5.0"' in t[:400])
ck('v5.0 date in both YAML blocks', 'date: "17 September 2026"' in r[:600] and 'date: "17 September 2026"' in t[:600])
ck('no active v4.7 or v4.8 version label', not re.search(r'v4\.[78]', r) and not re.search(r'v4\.[78]', t))
for tag in ('reading', 'dossier'):
    pre = (ROOT / f'src/preamble_v50_{tag}.tex').read_text()
    ck(f'{tag} preamble footer and subject say v5.0', pre.count('v5.0') >= 2 and 'v4.8' not in pre)

# ---------------------------------------------------------------- Euler-constant bridge
ck('R4A heading present once', r.count("## R4A. Euler's constant on the triangular coordinate") == 1)
ck('R4A sits between R4 and R5', r.index('## R4. ') < r.index('## R4A. ') < r.index('## R5. '))
for k in range(1, 9):
    ck(f'(GA.{k}) tagged once in the Reader', r.count('\\tag{GA.%d}' % k) == 1)
ck('R4A figure label and file', '\\label{fig:gamma-bridge}' in r and '\\figref{fig:gamma-bridge}' in r
   and (ROOT / 'figures/v48_gamma_bridge.png').is_file())
ck('R4A figure source script present', (ROOT / 'qa/figsrc/fig_gamma_bridge.py').is_file())
r4a = r[r.index('## R4A. '):r.index('## R5. ')]
ck('R4A third reason for the mirror stated', 'third reason for the mirror' in ' '.join(r4a.split()))
ck('R4A no-priority statement', 'None is claimed as new' in r4a)
ck('R4A zero firewall', 'Nothing in this section concerns where the zeros lie.' in r4a
   and 'It says nothing about where the zeros are.' in ' '.join(r4a.split()))
ck('R4A warns the zeta-value pattern stops', r'not $-\zeta(-5)=1/252$' in r4a)
ck('R4A names the replay', 'qa/audit_gamma_bridge.py' in r4a)
ck('R1 points to the third role of the mirror', 'gives it a' in flat and 'third role: it is a parity of the harmonic numbers' in flat)
ck('R9 points to (GA.8)', 'by (GA.8), twice this number plus' in flat)
ck('R17I points to (GA.3) and (GA.6)', 'the constant of (GA.3) and (GA.6)' in flat)
ck('R22 row for the bridge', "| Euler's constant on the triangular coordinate |" in r)
ck('R24 row for the bridge', '| How does Euler\'s constant enter? | §R4A, (9.8) | §96A; compare §§155G–155I |' in r)
ck('96A heading present once', t.count("## 96A. Euler's constant, the reciprocal-triangular zeta series, and a simplex ladder") == 1)
ck('96A sits between 96 and 97', t.index('## 96. ') < t.index('## 96A. ') < t.index('## 97. '))
for k in ['96A.1', '96A.1a', '96A.2', '96A.2a', '96A.3', '96A.4', '96A.5', '96A.6', '96A.7', '96A.8', '96A.9']:
    ck(f'({k}) tagged once in the Dossier', t.count('\\tag{%s}' % k) == 1)
d96 = t[t.index('## 96A. '):t.index('## 97. ')]
ck('96A proves (96A.2) three ways', all(s in d96 for s in ['*First proof (Raabe).*', '*Second proof (moment form).*',
                                                          '*Third proof (triangular telescope and Stirling).*']))
ck('96A sanity check is not a certificate', 'That check is a sanity check, not a certificate' in ' '.join(d96.split()))
ck('155G points to Theorem 96A.3', 'The constant in (155G.6) is the one of Theorem 96A.3' in t)
ck('96A.5 states the recomputation without a run note',
   'These enclosures are recomputed by this edition' in ' '.join(d96.split())
   and '`qa/GAMMA_BRIDGE.json`' in d96 and 'python-flint' not in d96)
ck('Ramanujan coefficients do not reuse the Jacobian letter R', '\\varrho_k' in d96 and not re.search(r'\bR_k\b', d96))

# ---------------------------------------------------------------- recomputed enclosures tie-out
gb = json.loads((ROOT / 'qa/GAMMA_BRIDGE.json').read_text())
ck('gamma-bridge replay passes', gb['passed'] == gb['total'] and not gb['failed'], (gb['passed'], gb['total']))
cert = gb.get('certified_enclosures', {})


def arb_parts(s):
    m = re.match(r'\[([0-9.]+) \+/- ([0-9.e-]+)\]', s)
    return m.group(1), float(m.group(2))


printed = {
    'lambda_1': (r'0.0230957089661210338143102479065\pm4.8\times10^{-33}', 4.8e-33),
    'q_1': (r'200.040454832386859463365185961\pm4.1\times10^{-28}', 4.1e-28),
    'q_2': (r'442.176150574082490320460688768\pm2.1\times10^{-28}', 2.1e-28),
    'q1_over_q2': (r'0.45239991929160355477\pm2.7\times10^{-21}', 2.7e-21),
    'C0': (r'8.001938046160201229441097\pm9.7\times10^{-26}', 9.7e-26),
}
for key, (text, rad) in printed.items():
    mid, arad = arb_parts(cert.get(key, '[0 +/- 1]'))
    ck(f'96A.5 printed {key} matches the Arb receipt (digits equal, printed radius >= Arb radius)',
       text in d96 and text.split('\\pm')[0] == mid and rad >= arad, (mid, arad))
ck('R12 prints the recomputed C bounds', r'8.00193804616020\le C\le8.00193804616021' in r)
ck('R12 carried-enclosure caveat removed', 'conditional scope of the carried enclosures' not in r)
ck('R12 stale tail figures removed', r'1.4\times10^{-9}' not in r and r'C\le8.001938048' not in r)
ck('R12 tail bound printed', r'up to less than $6\times10^{-25}$' in r)

# ---------------------------------------------------------------- run notes are gone
ck('no certificate-provenance block survives in either document',
   not re.findall(r'\*\*Certificate\s+provenance', both))
run_notes = ['no later than 23 August 2026', 'a replay on a second backend is still owed',
             'second backend is still owed', 'not rerun for v4.8', 'receipts not bundled',
             'receipt not bundled', 'last executed', 'python-flint 0.9.0', 'GNU MPFR, 256-bit standard run',
             'not retained', 'last-run date', 'edition-1.2 certificate record',
             'The standard run used 256-bit Arb arithmetic', 'not the second-backend replay']
for note in run_notes:
    ck('run note absent: ' + note[:46], note.lower() not in bflat.lower())
ck('W5-W6 unsupported hash-verification claim removed', 'verifies their hashes' not in t)

# ---------------------------------------------------------------- the status is stated once
ck('R12 states the position once', '**This is the position, stated once.**' in r)
ck('R12 keeps the two proof channels apart',
   'no zero ordinate, no verified height and no use of RH' in flat
   and 'it uses verified zero locations' in flat)
ck('R12 rung table is consolidated', r'| $W_2,\ldots,W_6$ | $(2k-1)!\,\mu_{k-1}$ | \CERT{} A-CAT |' in r
   and r'| $W_5$ | $9!\,\mu_4$' not in r)
ck('R12 keeps W7 open and the all-rung statement equal to RH',
   'From $W_7$ on, the source channel is open' in flat and 'the Riemann hypothesis itself' in flat)
ck('front matter points at the bundled certificate, not at run data',
   '**Where the certificates are.**' in r and 'two independent arithmetic backends' in flat)
ck('glossary defines the certificate of record', '| **certificate of record** |' in r)

# ---------------------------------------------------------------- Dossier 74A, one certificate
ck('74A heading present once', t.count(r'## 74A. One certificate for the source rungs $W_2,\ldots,W_6$') == 1)
d74a = t[t.index('## 74A. '):t.index('## 55. ')]
ck('74A theorem covers all five rungs', r'\boxed{W_k(x)>0\qquad(k=2,3,4,5,6).}' in d74a)
ck('74A classification unchanged', '**A-CAT / SOURCE-SIDE**' in d74a)
ck('74A firewall: no zero data', 'No zero table, verified height or RH' in ' '.join(d74a.split()))
for k in range(1, 13):
    ck('(74A.%d) tagged once in the Dossier' % k, t.count('\\tag{74A.%d}' % k) == 1)
ck('74A prints the thresholds', r'\theta_k&10^{-5}&10^{-8}&10^{-10}&10^{-12}&10^{-15}' in d74a)
ck('74A prints the tail constants',
   r'| $\alpha_k$ | $7$ | $396$ | $54{,}000$ | $13{,}406{,}400$ | $5{,}258{,}131{,}200$ |' in d74a)
ck('74A prints the Taylor cell bound', r'\tag{74A.5}' in d74a and r'\sup|Q_D|\,r^D' in d74a)
ck('74A names both programs and the comparison',
   all(x in d74a for x in ['qa/source_rungs/source_rungs_arb.py',
                           'qa/source_rungs/source_rungs_decimal.py',
                           'qa/source_rungs/cross_backend_check.py']))
ck('74A states the independence of the second backend',
   'It imports neither' in d74a and 'FLINT/Arb nor MPFR, SymPy or mpmath' in ' '.join(d74a.split()))
ck('74A keeps W7 open', r"$W_7=-x^{-12}(x^{13}W_6')'>0$" in d74a and 'it is open' in d74a)
ck('74 points to the consolidated certificate', 'Section 74A proves $W_4>0$ again' in ' '.join(t.split()))
ck('36 and 37 point to the consolidated certificate',
   t.count('Section 74A proves the\nsame sign again') + t.count('Section 74A proves the same sign again') >= 2)

# ---------------------------------------------------------------- the bundled certificate itself
CERT = ROOT / 'qa/source_rungs'
theta = {2: Fraction(1, 10 ** 5), 3: Fraction(1, 10 ** 8), 4: Fraction(1, 10 ** 10),
         5: Fraction(1, 10 ** 12), 6: Fraction(1, 10 ** 15)}
alpha = {2: '7', 3: '396', 4: '54000', 5: '13406400', 6: '5258131200'}
scripts = {'source_rungs_arb.py': None, 'source_rungs_decimal.py': None,
           'cross_backend_check.py': None, 'README.md': None}
for name in scripts:
    ck('certificate file bundled: ' + name, (CERT / name).is_file())
    if (CERT / name).is_file():
        scripts[name] = sha(CERT / name)
receipts = {'RECEIPT_arb.json': 'source_rungs_arb.py',
            'RECEIPT_arb_second.json': 'source_rungs_arb.py',
            'RECEIPT_decimal.json': 'source_rungs_decimal.py',
            'RECEIPT_decimal_second.json': 'source_rungs_decimal.py'}
for name, script in receipts.items():
    path = CERT / name
    if not path.is_file():
        ck('receipt bundled: ' + name, False)
        continue
    rec = json.loads(path.read_text())
    ck(name + ': PASS', rec['status'] == 'PASS')
    ck(name + ': produced by the bundled script', rec['script_sha256'] == scripts[script])
    ck(name + ': all five rungs', sorted(x['k'] for x in rec['finite']) == [2, 3, 4, 5, 6]
       and sorted(x['k'] for x in rec['tail']) == [2, 3, 4, 5, 6])
    for fin in rec['finite']:
        k = fin['k']
        cells = fin['cells']
        gaps = (Fraction(cells[0]['left']) != 1 or Fraction(cells[-1]['right']) != 128
                or any(Fraction(u['right']) != Fraction(v['left']) for u, v in zip(cells, cells[1:])))
        ck('%s: k=%d partition tiles [1,128] exactly' % (name, k), not gaps)
        ck('%s: k=%d every cell clears the printed threshold' % (name, k),
           Fraction(fin['uniform_rational_lower_bound_for_g']) == theta[k]
           and all(lower_of(c['lower_endpoint']) > WIDE.divide(Decimal(theta[k].numerator),
                                                               Decimal(theta[k].denominator))
                   for c in cells), fin['accepted_cells'])
    for tail in rec['tail']:
        ck('%s: k=%d tail constant and handoff match the text' % (name, tail['k']),
           tail['alpha'] == alpha[tail['k']] and tail['domain_s'] == ['128', 'infinity']
           and tail['ratio_below_one_half'] and tail['completion_annihilated'])
legacy = CERT / 'LEGACY_COMPARISON.json'
ck('comparison against the previously published receipts is bundled', legacy.is_file())
if legacy.is_file():
    lc = json.loads(legacy.read_text())
    rows = [c for c in lc['checks'] if c['check'] == 'legacy receipt reproduced']
    ck('previously published receipts: same statement, same tail constants, centres re-verified',
       lc['status'] == 'PASS' and len(rows) == 2
       and all(c['tail_constants_identical'] and c['legacy_script_sha256'] ==
               '348bb9b9d39669dc6729731f8a67b31bf596173554d8fc5fa6c10f3c4fb88697'
               and all(x['all_overlap_with_decimal_backend'] for x in c['legacy_centre_spot_check'])
               for c in rows),
       [c['file'] for c in rows])
for name in ('CROSS_BACKEND.json', 'CROSS_BACKEND_SECOND.json'):
    path = CERT / name
    if not path.is_file():
        ck('cross-backend comparison bundled: ' + name, False)
        continue
    cb = json.loads(path.read_text())
    ck(name + ': PASS', cb['status'] == 'PASS' and all(c.get('result') for c in cb['checks']))
    ck(name + ': the two backends are different libraries',
       'flint' in cb['arb_receipt']['backend'].lower() and 'libmpdec' in cb['decimal_receipt']['backend'].lower())
    ck(name + ': exact tail data agree for all five rungs',
       sum(1 for c in cb['checks'] if c['check'].startswith('exact tail data identical')) == 5)
def params(name):
    path = CERT / name
    return json.loads(path.read_text()).get('parameters') if path.is_file() else None


ck('the two runs of each backend changed every material parameter',
   all(params(a) and params(b) and params(a) != params(b) for a, b in
       [('RECEIPT_arb.json', 'RECEIPT_arb_second.json'),
        ('RECEIPT_decimal.json', 'RECEIPT_decimal_second.json')]))

# ---------------------------------------------------------------- public-facing wording
jargon = ['user-supplied', 'Orthogonal_Followup', 'Zeta_Zeros_2', 'Orange source note', 'supplied Green', 'Green run',
          'hostile', 'v4.5 provenance', 'v4.5 source provenance', 'provenance/v46', 'v4.6 reconciliation',
          'v4.6 pole audit', 'v4.6 hostile audit', 'v4.6 Gamma-pole audit', 'In v4.6 those columns', 'frozen',
          'source-certified A-CAT', 'source A-CAT through', 'Heat, Stieltjes, and complete Bernstein owners',
          'global matrix owner', 'the Gamma owner and the prime owner', 'the $F^{(14)}$ owner',
          'supplied historical report', 'transcribed as supplied']
for j in jargon:
    ck('internal wording absent: ' + j, j.lower() not in both.lower())
gl = r[r.index('## Working vocabulary'):r.index('# Part I.')]
ck('Reader uses "owner" only inside the glossary', len(re.findall(r'\bowner', r, re.I)) == len(re.findall(r'\bowner', gl, re.I)) >= 1,
   len(re.findall(r'\bowner', r, re.I)))
ck('Dossier explains working-paper labels', '**Labels and vocabulary.**' in t and 'adversarial replay' in tflat)
ck('Reader glossary present once', r.count('## Working vocabulary') == 1)
ck('Reader lineage table present once, before the status key',
   r.count('## Where this work sits in the classical literature') == 1
   and r.index('## Where this work sits in the classical literature') < r.index('## Master status key'))
ck('lineage no-priority disclaimer', 'It is not a claim of priority.' in r and 'No systematic MathSciNet or zbMATH search has been made' in flat)
ck('what-changed and how-to-cite paragraphs', '**What changed in v5.0.**' in r and '10.5281/zenodo.21968915' in r
   and '**What changed in v5.0.**' in t)

# ---------------------------------------------------------------- cross-references resolve
rh = set(re.findall(r'^## (R\d+[A-Z]?)\.', r, re.M))
dh = set(re.findall(r'^#{2,3} (\d+[A-Z]?)[. ]', t, re.M))


def reader_refs(text):
    out = set()
    for m in re.finditer(r'(?:§§?|Sections?\s|Reader\s)([^.;:)\]\n]{0,80})', text):
        out.update(re.findall(r'\bR\d+[A-Z]?\b', m.group(1)))
    out.update(re.findall(r'§(R\d+[A-Z]?)', text))
    return out


def dossier_refs(text):
    out = set()
    for m in re.finditer(r'§§?\s*([0-9A-Z,\s–\-and]+)', text):
        out.update(re.findall(r'\b(\d+[A-Z]?)\b', m.group(1)))
    return out


for name, text in [('reading', r), ('dossier', t)]:
    bad = sorted(x for x in reader_refs(text) if x not in rh)
    ck(f'{name}: every Reader section reference resolves', not bad, bad)
    bad = sorted(x for x in dossier_refs(text) if x not in dh)
    ck(f'{name}: every Dossier section reference resolves', not bad, bad)
alltags = set(re.findall(r'\\tag\{([^}]*)\}', both))
for name, text in [('reading', r), ('dossier', t)]:
    cited = set(re.findall(r'\(((?:GA|96A|TR|2|4|5|9|12|94|155G)\.[0-9]+[a-z]?)\)', body(text)))
    ck(f'{name}: cited equation tags in the new material exist', all(c in alltags for c in cited),
       sorted(c for c in cited if c not in alltags))

# ---------------------------------------------------------------- references
for name, text in [('reading', r), ('dossier', t)]:
    rs = refsec(text)
    nums = [int(x) for x in re.findall(r'^\s*(\d+)\.\s', rs, re.M)]
    ck(f'{name}: references 83-120 each listed once', all(nums.count(k) == 1 for k in range(83, 121)) and max(k for k in nums if k < 1000) == 120)
    ck(f'{name}: DOIs added to Li, Bombieri-Lagarias and Keiper',
       all(d in rs for d in ['10.1006/jnth.1997.2137', '10.1006/jnth.1999.2392', '10.2307/2153215']))
    ck(f'{name}: Elaissaoui-Guennoun journal record', '10.1016/j.jnt.2019.09.025' in rs)
    ck(f'{name}: Montgomery 1973 venue', 'Proceedings of Symposia in Pure Mathematics 24' in rs)
cited_r = set()
for m in re.finditer(r'\[(\d+(?:\s*(?:,|--|–)\s*\d+)*)(?:,[^\]]*)?\]', body(r)):
    for part in re.split(r'\s*,\s*', m.group(1)):
        if '--' in part or '–' in part:
            a, b = re.split(r'--|–', part); cited_r.update(range(int(a), int(b) + 1))
        else:
            cited_r.add(int(part))
ck('every new reference 83-120 is cited in the Reading Volume body', all(k in cited_r for k in range(83, 121)),
   sorted(k for k in range(83, 121) if k not in cited_r))
ck('Ramanujan primary source cited (Berndt, Entry 9 of Chapter 38)', 'Entry 9 of Chapter 38' in flat and '[119]' in r)
ck('denominator sign statement corrected: b_1 = gamma_E - 1 < 0 in both documents',
   r'$b_1^{\rm den}=\gamma_E-1<0$' in r and r'$b_1^{\rm den}=\gamma_E-1<0$' in t
   and 'first displayed sign change' not in t and 'refutes coefficient positivity' not in r)
ck('Derby misprint recorded in text and reference', 'the quadratic printed there has the wrong sign' in flat
   and '$(p-T_{2n})(p+n)$' in r)
ck('(TR.4) consecutive-squares identity present', '\\tag{TR.4}' in r)
ck('Faulhaber classical forms (2.5)-(2.6) present', '\\tag{2.5}' in r and '\\tag{2.6}' in r and 'Jacobian of the triangular' in flat)
ck('Witula case r=1 recorded', 'case $r=1$' in flat and '[87, (13)]' in r)

# ---------------------------------------------------------------- figures
baseline = json.loads((ROOT / 'qa/V50_FIGURE_BASELINE.json').read_text())
base = {row['path']: row['sha256'] for row in baseline['files']}
cur = {}
for p in sorted((ROOT / 'figures').rglob('*')):
    if p.is_file():
        cur[p.relative_to(ROOT / 'figures').as_posix()] = sha(p)
# v5.0 is the first edition to change figures deliberately, so the delta is
# declared here and the audit requires the observed delta to equal it exactly.
# Anything else -- an unreviewed redraw, a silent drop -- still fails.
FIGURE_DELTA = {
    'added': ['figure74_safe_axis_and_self_dual.png',
              'figure75A_r10c_one_orbit_four_coordinates.png'],
    'removed': ['figure74_s_sigma_it_fold_atlas.png',
                'pringsheim_no_dominance.png',
                'v26c_reciprocal_window.png',
                'v27_bernstein_route.png',
                'v27b_energy_spectral_cases.png',
                'v29_even_triangle_geometry.png',
                'v29_prime_energy_cases.png'],
    'changed': ['figure75_li_pp97_loewner_study_atlas.png',
                'v26c_source_depth.png',
                'v30_rh_equivalence_map.png'],
}
added = sorted(set(cur) - set(base))
removed = sorted(set(base) - set(cur))
changed = sorted(k for k in set(base) & set(cur) if base[k] != cur[k])
ck('figures added match the declared v5.0 delta', added == FIGURE_DELTA['added'], added)
ck('figures removed match the declared v5.0 delta', removed == FIGURE_DELTA['removed'], removed)
ck('figures redrawn match the declared v5.0 delta', changed == FIGURE_DELTA['changed'], changed)
ck('every redrawn or added figure has a generator in qa/figsrc',
   all(any(f in g.read_text() for g in (ROOT / 'qa/figsrc').glob('*.py'))
       for f in FIGURE_DELTA['added'] + FIGURE_DELTA['changed']),
   [f for f in FIGURE_DELTA['added'] + FIGURE_DELTA['changed']
    if not any(f in g.read_text() for g in (ROOT / 'qa/figsrc').glob('*.py'))])
ck('every retired figure is archived under provenance/v50',
   all((ROOT / 'provenance/v50/pruned_figures' / f).is_file()
       for f in FIGURE_DELTA['removed']),
   [f for f in FIGURE_DELTA['removed']
    if not (ROOT / 'provenance/v50/pruned_figures' / f).is_file()])
used = set(re.findall(r'figures/([A-Za-z0-9_./-]+\.(?:png|pdf))', both))
ck('every referenced figure exists', all((ROOT / 'figures' / u).is_file() for u in used), sorted(u for u in used if not (ROOT / 'figures' / u).is_file()))
# V50_FIGURE_BASELINE.json is the INCOMING (v4.9) state and is never rewritten
# here: the declared delta above is measured against it, so the audit gives the
# same answer every time it is run from this package.  The current state is
# written beside it, and becomes the incoming baseline of the next edition.
(ROOT / 'qa/V50_FIGURE_STATE.json').write_text(json.dumps(
    {'version': 'v5.0', 'measured_against': 'qa/V50_FIGURE_BASELINE.json (v4.9)',
     'files': [{'path': k, 'sha256': v} for k, v in sorted(cur.items())]}, indent=2) + '\n')

out = {'total': len(checks), 'passed': sum(c['passed'] for c in checks),
       'failed': [c['name'] for c in checks if not c['passed']], 'checks': checks}
(ROOT / 'qa/V50_UPDATE_AUDIT.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'total': out['total'], 'passed': out['passed'], 'failed': out['failed']}, indent=2, ensure_ascii=False))
raise SystemExit(0 if not out['failed'] else 1)
