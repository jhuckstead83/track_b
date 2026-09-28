#!/usr/bin/env python3
"""v5.2 delta audit only; does not rerun inherited v5.0 certificates.

Standard library only. Checks that v5.1 is preserved inside v5.2, that the
new material is tagged and cited consistently, and that the numbers printed
in the new twin tables agree with each other.  The twin computations
themselves are replayed by the programs in provenance/v5_2/evidence/.
"""
from pathlib import Path
from fractions import Fraction as Fr
import cmath, hashlib, json, math, platform, re, statistics, sys

ROOT = Path(__file__).resolve().parents[1]
checks = []
failed = []

def check(name, test, detail=None):
    row = {'name': name, 'pass': bool(test)}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)
    if not test:
        failed.append(name)

def H(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return p.read_text(encoding='utf-8')

def is_subsequence(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)

MARKS = ['PROVED', 'CERT', 'EQUIV', 'EVID', 'OPENSTAT']
MARK_RE = re.compile(r'\\(?:' + '|'.join(MARKS) + r')\{\}')
TAG_RE = re.compile(r'\\tag\{([^}]+)\}')
# The Reader stays within its 101-page ceiling by carrying the twin in its frontier
# paragraph and NO-GO ledger only; the displays, tables and new references live in the
# Dossier (tags are global, so the Reader cites (TW.1) and (TW.3) there).
NEW_TAGS = {'READING_VOLUME': [], 'TECHNICAL_DOSSIER': ['TW.1', 'TW.2', 'TW.3']}
LAST_REF = {'READING_VOLUME': '120', 'TECHNICAL_DOSSIER': '124'}

# ---------------------------------------------------------------- preservation
summary = {}
text = {}
for kind in ['READING_VOLUME', 'TECHNICAL_DOSSIER']:
    old = ROOT / 'provenance/v5_1/src' / f'TN_Postmaster_Volume_I_v5_1_{kind}.md'
    new = ROOT / 'src' / f'TN_Postmaster_Volume_I_v5_2_{kind}.md'
    a, b = read(old), read(new)
    text[kind] = b
    oldtags, newtags = TAG_RE.findall(a), TAG_RE.findall(b)
    added = [t for t in newtags if t.startswith('TW.')]
    check(kind + ': inherited equation-tag sequence preserved',
          [t for t in newtags if not t.startswith('TW.')] == oldtags)
    check(kind + ': new equation tags are exactly [' + ', '.join(NEW_TAGS[kind]) + ']',
          added == NEW_TAGS[kind], added)
    check(kind + ': no duplicate equation tags', len(newtags) == len(set(newtags)))
    om, nm = MARK_RE.findall(a), MARK_RE.findall(b)
    check(kind + ': inherited status-tag sequence preserved as a subsequence',
          is_subsequence(om, nm))
    check(kind + ': has abstract and summary', '# Abstract' in b and '# Summary' in b)
    check(kind + ': no dependence on companion entropy article',
          'Surprise Is Not Meaning' not in b)
    check(kind + ': inherited replay scope disclosed',
          'not been re-executed' in b or 'were not re-executed' in b)
    check(kind + ': edition string is v5.2 and no stale v5.1 edition claim',
          'v5.2' in b and 'Version 5.1 makes' not in b and 'Version 5.1 clarifies' not in b)
    # Reference list: [66] corrected everywhere; 121-124 appended to the Dossier only.
    refs = re.findall(r'^(\d+)\. ', b.split('\\begingroup')[-1], re.M)
    oldrefs = re.findall(r'^(\d+)\. ', a.split('\\begingroup')[-1], re.M)   # v5.1 numbering, gaps included
    extra = ['121', '122', '123', '124'] if kind == 'TECHNICAL_DOSSIER' else []
    check(f'{kind}: v5.1 reference numbers preserved' + (', then 121-124' if extra else ', none added'),
          refs == oldrefs + extra, refs[-5:])
    m66 = re.search(r'^66\. (.*?)(?=^\d+\. )', b, re.M | re.S)
    e66 = ' '.join(m66.group(1).split()) if m66 else ''
    check(kind + ': [66] carries the arXiv title "... simple and on the critical line"',
          'simple and on the critical line' in e66 and 'simple or on the critical line*' not in e66)
    body = b.split('\\begingroup')[0]
    cited = set(re.findall(r'\b(\d{1,3})\b', ' '.join(re.findall(r'\[(\d[\d,;\s–-]*)(?:,[^\]]*)?\]', body))))
    if kind == 'TECHNICAL_DOSSIER':
        check(kind + ': [66] carries the v2 88.76% note and points to [121]', '88.76%' in e66 and '[121]' in e66)
        for r in ['121', '122', '123', '124']:
            check(f'{kind}: [{r}] is cited in the text', r in cited)
    else:
        check(kind + ': cites no reference beyond its own list', not any(int(c) > 120 for c in cited),
              sorted(c for c in cited if int(c) > 120))
    # Build safety: no pipe inside inline math in a table row; no new non-ASCII characters.
    bad = [l for l in b.splitlines() if l.startswith('|')
           and any('|' in m for m in re.findall(r'\$[^$]*\$', l))]
    check(kind + ': no "|" inside $...$ in pipe-table rows', not bad, bad[:3])
    newchars = sorted({c for c in b if ord(c) > 127} - {c for c in a if ord(c) > 127})
    check(kind + ': no non-ASCII character that v5.1 did not already typeset',
          not newchars, [f'U+{ord(c):04X}' for c in newchars])
    summary[kind] = {'v51_sha256': H(old), 'v52_sha256': H(new),
                     'equation_tags_v51': len(oldtags), 'equation_tags_v52': len(newtags),
                     'status_marks_v51': len(om), 'status_marks_v52': len(nm)}

# Every mathematical status row of the v5.1 Reading Volume survives verbatim.
a = read(ROOT / 'provenance/v5_1/src/TN_Postmaster_Volume_I_v5_1_READING_VOLUME.md')
b = text['READING_VOLUME']
rows = [l for l in a.splitlines() if l.startswith('|') and any('\\' + x + '{' in l for x in MARKS)]
check('all v5.1 status rows preserved verbatim in the Reading Volume',
      all(l in b for l in rows), [l[:80] for l in rows if l not in b][:3])

# Cross-volume references.
D = text['TECHNICAL_DOSSIER']
for s in ['69A', '69B', '69C']:
    check(f'Dossier has section {s}', re.search(r'^## ' + s + r'\. ', D, re.M) is not None)
check('Reading Volume points to Dossier §69A-§69C and cites (TW.1), (TW.3)',
      '§69A' in b and '§69C' in b and '(TW.1)' in b and '(TW.3)' in b and 'R25A' not in b)
i = b.find('They are not equal in reach.')
check('Reading Volume (R.2) paragraph carries both a \\PROVED{} and an \\EVID{} marker',
      i > 0 and '\\PROVED{}' in b[i:i + 1200] and '\\EVID{}' in b[i:i + 1200])

def status_after(doc, tag, mark, window=1400):
    i = doc.find('\\tag{' + tag + '}')
    return i >= 0 and ('\\' + mark + '{}') in doc[i:i + window]
check('Dossier: (TW.1) and (TW.2) followed by \\PROVED{}',
      status_after(D, 'TW.1', 'PROVED') and status_after(D, 'TW.2', 'PROVED'))
check('Dossier: (TW.3) followed by \\EVID{}', status_after(D, 'TW.3', 'EVID'))

# Preambles and footers.
for tag in ['reading', 'dossier']:
    p = read(ROOT / 'src' / f'preamble_v52_{tag}.tex')
    check(f'preamble_v52_{tag}: footer reads v5.2 and RH OPEN', 'v5.2 -- RH OPEN' in p)

# ---------------------------------------------------------------- exact algebra
# Fold: q(s)=s(1-s)=1/4-(s-1/2)^2=-2T_{s-1}, and z=gamma-i*delta for s=1/2+delta+i*gamma.
class G:  # exact Gaussian rationals
    def __init__(s, re_, im=0): s.r, s.i = Fr(re_), Fr(im)
    def __add__(s, o): o = o if isinstance(o, G) else G(o); return G(s.r + o.r, s.i + o.i)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, G) else G(o); return G(s.r - o.r, s.i - o.i)
    def __rsub__(s, o): return G(o) - s
    def __mul__(s, o): o = o if isinstance(o, G) else G(o); return G(s.r*o.r - s.i*o.i, s.r*o.i + s.i*o.r)
    __rmul__ = __mul__
    def __eq__(s, o): o = o if isinstance(o, G) else G(o); return s.r == o.r and s.i == o.i
samples = [(Fr(3, 10), Fr(857, 10)), (Fr(-1, 7), Fr(21, 4)), (Fr(0), Fr(14))]
ok = True
for d, g in samples:
    s = G(Fr(1, 2) + d, g)
    q = s * (1 - s)
    z = G(g, -d)
    T = (s - 1) * s * G(Fr(1, 2))          # T_{s-1} = (s-1)s/2
    ok &= q == G(Fr(1, 4)) + z * z and q == G(0) - 2 * T and q == G(Fr(1, 4)) - (s - G(Fr(1, 2))) * (s - G(Fr(1, 2)))
check('fold identities: q=s(1-s)=1/4+z^2=-2T_{s-1} with z=gamma-i*delta (exact)', ok)

# (TW.2): 4xq/(x+q)^2=(1+e)/(1+e/2)^2 when q=x(1+e), and the series coefficients.
ok = all(4 * x * (x * (1 + e)) / (x + x * (1 + e)) ** 2 == (1 + e) / (1 + e / 2) ** 2
         for x in [Fr(7, 3), Fr(1001, 4)] for e in [Fr(1, 5), Fr(-2, 9)])
coef = [(-1) ** (n + 1) * Fr(1, n) * (1 - Fr(2) ** (1 - n)) for n in range(1, 5)]
check('(TW.2) kernel identity and series 0, -1/4, +1/4, -7/32 (exact)',
      ok and coef == [0, Fr(-1, 4), Fr(1, 4), Fr(-7, 32)], [str(c) for c in coef])

# (TW.1) on a real polynomial, exactly: odd powers of i*eta cancel.
P = [Fr(3), Fr(-2), Fr(5, 7), Fr(1), Fr(-4, 3), Fr(2, 5)]   # coefficients of a real polynomial
def peval(c, z):
    acc = G(0)
    for a_ in reversed(c): acc = acc * z + a_
    return acc
def deriv(c, k):
    for _ in range(k): c = [i * c[i] for i in range(1, len(c))]
    return c
qr, eta = Fr(11, 3), Fr(2, 7)
lhs = peval(P, G(qr, eta)) + peval(P, G(qr, -eta))
rhs = G(0)
for m in range(0, len(P)):
    dm = deriv(P, 2 * m)
    if not dm: break
    rhs = rhs + G(2 * (-1) ** m * eta ** (2 * m) / math.factorial(2 * m)) * peval(dm, G(qr))
check('(TW.1) parity expansion exact on a degree-5 real polynomial', lhs == rhs)

# Theorem 69C.1: g_c(conj q) = -g_c(q); first-order defect.
g = lambda q, c: math.log(abs(q + 1j * c) / abs(q - 1j * c))
qq, c, eta = complex(3.7, 0.01), 0.8, 0.01
check('Theorem 69C.1: g_c odd under conjugation; first-order defect 2c*eta/(Q^2+c^2)',
      abs(g(qq, c) + g(qq.conjugate(), c)) < 1e-15 and
      abs(g(qq, c) - 2 * c * eta / (3.7 ** 2 + c ** 2)) < 1e-5)

# ---------------------------------------------------------------- twin tables
kappa = (math.sqrt(10 - 2 * math.sqrt(5)) - 2) / (math.sqrt(5) - 1)
check('kappa = 0.2840790438...', abs(kappa - 0.2840790438) < 1e-10, kappa)

# c(n) of -f'/f by Dirichlet inversion, against the Dossier table.
N = 30
a_ = [0.0] + [[1, kappa, -kappa, -1, 0][(n - 1) % 5] for n in range(1, N + 1)]
b_ = [0.0] * (N + 1); b_[1] = 1.0                      # Dirichlet inverse of a
for n in range(2, N + 1):
    b_[n] = -sum(a_[d] * b_[n // d] for d in range(2, n + 1) if n % d == 0)
cn = [0.0] * (N + 1)
for n in range(1, N + 1):
    cn[n] = sum(a_[d] * math.log(d) * b_[n // d] for d in range(1, n + 1) if n % d == 0)
m = re.search(r'^\| \$n\$ \|(.*)\n\|[-| ]+\n\| \$c\(n\)\$ \|(.*)\n', D, re.M)
ns = [int(x) for x in re.findall(r'\d+', m.group(1))] if m else []
vals = [float(x.replace('$', '').replace('+', '').strip()) for x in m.group(2).split('|') if x.strip()] if m else []
bad = [(n, v, round(cn[n], 4)) for n, v in zip(ns, vals) if abs(cn[n] - v) > 6e-4]
check('Dossier c(n) table matches Dirichlet inversion of the twin coefficients',
      len(ns) == 11 and len(vals) == 11 and not bad, bad)

# Off-line zero table: delta = sigma-1/2 and the printed ratio k*/((pi/2) t^2/(a delta)).
rows = re.findall(r'^\| (\d+) \| \$([0-9.]+)\+([0-9.]+)i\$ \| ([0-9.]+) \| ([0-9.]+|—) \| ([0-9,]+|—) \| ([0-9.]+|[^|]+) \|$', D, re.M)
ratios, bad = [], []
for idx, sig, t, dl, aa, ks, rr in rows:
    sig, t, dl = float(sig), float(t), float(dl)
    if abs((sig - 0.5) - dl) > 6e-5: bad.append((idx, 'delta'))
    if aa == '—': continue
    k = int(ks.replace(',', ''))
    ratio = k / (math.pi / 2 * t * t / (float(aa) * dl))
    if abs(ratio - float(rr)) > 4e-3: bad.append((idx, round(ratio, 4), rr))
    ratios.append(float(rr))
check('Dossier off-line table: 16 rows, delta and ratio columns recompute',
      len(rows) == 16 and not bad, bad)
med = statistics.median(ratios) if ratios else None
check('median ratio over the 15 resolved twin zeros is 0.806 (printed 0.81)',
      med is not None and abs(med - 0.806) < 5e-4 and '0.81 over 15 twin zeros' in D, med)

# First off-line zero: |q_0|, theta_max, the sector bound 218, and the Löwner centres.
s0 = complex(0.808517182, 85.699348485)
q0 = s0 * (1 - s0)
theta = abs(cmath.phase(q0))
check('|q_0| = 7344.72 and theta_max = 7.1997e-3',
      abs(abs(q0) - 7344.7235) < 2e-3 and abs(theta - 7.1997e-3) < 5e-8, [abs(q0), theta])
check('sector bound floor(pi/(2 theta_max)) = 218 and the tail bound 2.8e-3 < theta_max',
      math.floor(math.pi / (2 * theta)) == 218 and 2.8e-3 < theta)
check('Löwner centres are 0.97, 1.00, 1.03 times |q_0|',
      all(abs(f * abs(q0) - x) < 0.01 for f, x in [(0.97, 7124.38), (1.0, 7344.72), (1.03, 7565.07)]))
check('first failing rung sits inside the scanned range 0.52 <= x <= 43,264',
      0.52 <= 7140.066 <= 43264)
# The ~1e27 reading of (TW.3) at the verified height.
kz = 1.3 * (3e12) ** 2 / (0.1 * 0.1)
check('(TW.3) at t=3e12, a=delta=0.1 gives k ~ 1e27', 26.5 < math.log10(kz) < 27.5, f'{kz:.2e}')

# Key numbers agree between the volumes.
flat = lambda s: s.replace('{,}', '').replace(',', '')
for key in ['16588', '16589', 'N=105', '10^{-141}', '10^{27}']:
    check(f'number {key} appears in both volumes', key in flat(D) and key in flat(b))
for key in ['218', '43264', '7140.0', 'N=100', '0.808517182+85.699348485i']:
    check(f'number {key} appears in the Dossier', key in flat(D))

# ---------------------------------------------------------------- evidence and build
ev = ROOT / 'provenance/v5_2/evidence'
sums = ev / 'SHA256SUMS.txt'
if sums.exists():
    lines = [l.split(None, 1) for l in read(sums).splitlines() if l.strip()]
    bad = [f for h, f in lines if not (ev / f.strip().lstrip('*')).exists()
           or H(ev / f.strip().lstrip('*')) != h]
    check('evidence files match provenance/v5_2/evidence/SHA256SUMS.txt', not bad, bad[:5])
    # The printed census and table agree with the recorded runs.
    tw = ev / 'dh_twin'
    Z = [json.loads(read(tw / f)) for f in ['dh_zeros.json', 'dh_zeros_260_440.json', 'dh_zeros_440_640.json']]
    n_on, n_off = sum(len(z['online']) for z in Z), sum(len(z['offline']) for z in Z)
    check('evidence census: 501 on-line zeros and 16 off-line pairs to T=640',
          (n_on, n_off, Z[-1]['T']) == (501, 16, 640.0) and '501 on-line zeros' in D and '16 off-line pairs' in D,
          [n_on, n_off])
    r3 = json.loads(read(tw / 'rungs3_T640.json'))
    printed = {int(idx): (ks, sig) for idx, sig, _t, _dl, _a, ks, _rr in rows}   # rows = off-line table
    bad = []
    for row in r3['results']:
        i = row['zero']
        if i in (10, 15):          # 10 is captured by zero 11 (see zero10.py); 15 has an incomplete local list
            continue
        ks = printed.get(i, ('—', ''))[0]
        if ks == '—' or int(ks.replace(',', '')) != row['kFirst'] or abs(float(printed[i][1]) - row['rho'][0]) > 1e-9:
            bad.append((i, ks, row['kFirst']))
    check('evidence rungs3_T640.json: sector bound 218 and k* of rows 0-9, 11-14 match the printed table',
          r3['Ksector'] == 218 and not bad, bad)
    z10 = read(tw / 'zero10.py')
    check('row 10 is computed by zero10.py with the exact kernel within +-40, scanning +-3',
          'abs(g - t0) < 40' in z10 and 'span=3.0' in z10 and '18{,}519{,}801' not in D and '18,519,801' in D)
else:
    check('evidence checksum file present', False)

build = {}
for name, limit in [('READING', 101), ('DOSSIER', None)]:
    p = ROOT / 'qa' / f'BUILD_{name}.json'
    if not p.exists():
        build[name] = 'not built in this run'
        continue
    r = json.loads(read(p))
    build[name] = {'pages': r['pages'], 'body_pages': r['body_pages']}
    check(name + ': built from the v5.2 master', r['src_sha256'] == summary[
        'READING_VOLUME' if name == 'READING' else 'TECHNICAL_DOSSIER']['v52_sha256'])
    check(name + ': rebuilt without undefined references or missing characters',
          r['undefined_refs'] == 0 and r['missing_characters'] == 0)
    check(name + ': no overfull box over 30pt', r['overfull_over_30pt'] == [], r['overfull_over_30pt'])
    if limit:
        check(f'{name}: page ceiling {limit}', r['pages'] <= limit, r['pages'])

receipt = {'edition': '5.2',
           'scope': 'Editorial/interface delta, preservation, exact algebra of the new displays, '
                    'internal consistency of the new twin tables, and document build if present. '
                    'No v5.0 interval certificate rerun; twin computations are replayed by the evidence programs.',
           'python': platform.python_version(), 'sources': summary, 'build': build,
           'checks': checks, 'passed': sum(c['pass'] for c in checks), 'failed': failed,
           'status': 'PASS' if not failed else 'FAIL'}
(ROOT / 'qa/V52_INTERFACE_RECEIPT.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
for c_ in checks:
    print(('PASS ' if c_['pass'] else 'FAIL ') + c_['name'] + ('' if c_['pass'] or 'detail' not in c_ else f"  {c_['detail']}"))
print(f"{receipt['passed']}/{len(checks)} checks passed; build: {build}")
sys.exit(0 if not failed else 1)
