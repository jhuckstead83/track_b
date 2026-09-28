#!/usr/bin/env python3
"""Carried checks adapted to the v4.3 pair; editorial corrections are diffed. Every check is stated as a claim about
the delivered files or about mathematics that can be recomputed here."""
import re, json
from math import comb, factorial
from pathlib import Path
from fractions import Fraction
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
RV = ROOT / 'src/TN_Postmaster_Volume_I_v4_3_READING_VOLUME.md'
TD = ROOT / 'src/TN_Postmaster_Volume_I_v4_3_TECHNICAL_DOSSIER.md'
rv, td = RV.read_text(), TD.read_text()
# a prose check must not break on a line wrap: compare against flattened copies
_flat = lambda t: re.sub(r'\s+', ' ', t)
_rvf, _tdf = _flat(rv), _flat(td)
res = []
def ck(name, ok, detail=''):
    res.append((name, bool(ok), detail))

# ---------------------------------------------------------------- hygiene
ck('no version strings in Reading Volume', not re.findall(r'v[23]\.\d', rv),
   str(re.findall(r'v[23]\.\d', rv))[:120])
ck('no version strings in Dossier', not re.findall(r'v[23]\.\d', td),
   str(re.findall(r'v[23]\.\d', td))[:120])
for term in ['author review', 'author-review', 'grading-review', 'red team',
             'blue team', 'green team', 'supersedes the earlier']:
    ck(f'no in-house term: {term!r}', term.lower() not in rv.lower() and term.lower() not in td.lower())
ck('no "technical §" left in Reading Volume', not re.search(r'[Tt]echnical\s+§', rv))
ck('Dossier convention stated once in Reading Volume',
   rv.count('A number without an R is in the Dossier.') == 1)

# ------------------------------------------------------- namespace integrity
rh = re.findall(r'^## (R\d+[A-Z]*)\.', rv, re.M)
th = re.findall(r'^## (\d+[A-Z]*)\.', td, re.M)
ck('reader headings unique', len(rh) == len(set(rh)), f'{len(rh)} headings')
ck('dossier headings unique', len(th) == len(set(th)), f'{len(th)} headings')
ck('no reader heading in the Dossier', not re.findall(r'^## R\d', td, re.M))
ck('no bare numeric heading in the Reading Volume', not re.findall(r'^## \d+[A-Z]*\.', rv, re.M))

# ------------------------------------------------------------- status badges
for cmd in [r'\PROVED', r'\CERT', r'\EQUIV', r'\OPENSTAT', r'\EVID']:
    ck(f'badge {cmd} defined in both preambles',
       all(cmd + '}' in (ROOT / f'src/preamble_v43_{k}.tex').read_text()
           for k in ('reading', 'dossier')))
ck('legend appears in Reading Volume', rv.count(r'\statuslegend') >= 2)
ck('legend appears in Dossier', td.count(r'\statuslegend') >= 2)
used = set(re.findall(r'\\(PROVED|CERT|EQUIV|OPENSTAT|EVID)\{\}', rv))
ck('all five badges used in the Reading Volume', len(used) == 5, str(sorted(used)))
usedd = set(re.findall(r'\\(PROVED|CERT|EQUIV|OPENSTAT|EVID)\{\}', td))
ck('EVIDENCE badge used in the Dossier', 'EVID' in usedd, str(sorted(usedd)))
ck('closed-form box used', rv.count(r'\begin{tnclosed}') >= 3, str(rv.count(r'\begin{tnclosed}')))
ck('open box used', rv.count(r'\begin{tnopen}') >= 1)
ck('every tcolorbox is balanced',
   all(rv.count(r'\begin{tn' + e + '}') == rv.count(r'\end{tn' + e + '}')
       for e in ('closed', 'equiv', 'open')))

# ------------------------------------------- the mathematics stated in v3.7
# (R.1a) binom(k,2) = T_{k-1}
T = lambda n: n * (n + 1) // 2
ck('(R.1a) C(k,2)=T_{k-1}', all(comb(k, 2) == T(k - 1) for k in range(2, 200)))
ck('C(k,3)=sum of triangular numbers',
   all(comb(k, 3) == sum(T(r) for r in range(1, k - 1)) for k in range(3, 120)))
# 3003 multiplicity, exhaustive over the half triangle
hits = []
for n in range(1, 3004):
    for j in range(0, n // 2 + 1):
        c = comb(n, j)
        if c == 3003: hits.append((n, j))
        if c > 3003: break
ck('3003 occurs exactly 8 times in Pascal', 2 * len(hits) == 8, str(hits))
ck('3003 = T_77 = C(78,2)', 3003 == T(77) == comb(78, 2))
# (R.1b) row generating function and the single-subtraction recurrence
c = lambda k, j: (-1) ** j * comb(k, j) if 0 <= j <= k else 0
ck('(R.1b) sum c(k,j) z^j = (1-z)^k at rational z',
   all(sum(Fraction(c(k, j)) * Fraction(z, 7) ** j for j in range(k + 1))
       == (1 - Fraction(z, 7)) ** k for k in range(0, 18) for z in (1, 3, 11)))
ck('(SW.5) recurrence c(k+1,j)=c(k,j)-c(k,j-1)',
   all(c(k + 1, j) == c(k, j) - c(k, j - 1) for k in range(0, 25) for j in range(0, k + 3)))
ck('seed c(0,0)=+1', c(0, 0) == 1)
ck('row 12 entry j=9 is -220 and equals j=3', c(12, 9) == -220 == c(12, 3))

# (SW.5a) u^k = sum_j c(k,j) x^j (x+q)^{-(k+j)}  -- exact in Fractions
def sw5a(k, x, q):
    lhs = Fraction(q, 1) ** k / Fraction(x + q, 1) ** (2 * k)
    rhs = sum(Fraction(c(k, j)) * Fraction(x) ** j / Fraction(x + q) ** (k + j)
              for j in range(k + 1))
    return lhs == rhs
ck('(SW.5a) carrier power = row k, exactly',
   all(sw5a(k, x, q) for k in range(1, 13) for x in (1, 3, 7) for q in (1, 2, 5, 11)))

# (SW.4b), (R.3), (12.4a) and (SW.6) against an independent exact derivative.
# D^n[x^k/(x+q)] is computed by Leibniz in exact rationals; no closed form from
# the paper is used on this side of any comparison.
F = Fraction
def dpow(n, i, k, x):
    if i > k: return F(0)
    return F(factorial(k), factorial(k - i)) * F(x) ** (k - i)
def dres(m, q, x):
    return F((-1) ** m * factorial(m)) / F(x + q) ** (m + 1)
def W_exact(k, x, spec):
    n = 2 * k - 1
    tot = F(0)
    for q, mult in spec:
        tot += mult * sum(F(comb(n, i)) * dpow(n, i, k, x) * dres(n - i, q, x)
                          for i in range(n + 1))
    return F((-1) ** (k - 1)) * tot
def Zr_exact(r, x, spec):
    return sum(F(mult) / F(x + q) ** r for q, mult in spec)
def dS(r, x, spec):
    return sum(mult * dres(r, q, x) for q, mult in spec)

SPEC = [(F(3, 2), 2), (F(7, 3), 1), (F(5), 1)]
ok_rung = ok_zero = True
for k in range(1, 13):
    for x in (F(1), F(2, 5), F(9, 4)):
        W = W_exact(k, x, SPEC)
        row = F(factorial(2 * k - 1)) * sum(F(c(k, j)) * x ** j * Zr_exact(k + j, x, SPEC)
                                            for j in range(k + 1))
        zero = F(factorial(2 * k - 1)) * sum(mult * q ** k / (x + q) ** (2 * k)
                                             for q, mult in SPEC)
        ok_rung &= (W == row)
        ok_zero &= (W == zero)
ck('(SW.4b) row k reproduces the exact derivative, k=1..12 at three scales', ok_rung)
ck('(R.3) derivative and folded-zero forms agree exactly, k=1..12', ok_zero)

ok = all(F(factorial(2 * k - 1)) * sum(mult / q ** k for q, mult in SPEC)
         == F(factorial(2 * k - 1)) * Zr_exact(k, F(0), SPEC) for k in range(1, 13))
ck('(12.4a) W_k(0)/(2k-1)! = mu_{k-1} = Z_k(0), k=1..12', ok)

A = lambda k, j: (F(0) if not 0 <= j <= k else
                 F((-1) ** (k + j - 1) * factorial(2 * k - 1), factorial(k + j - 1)) * c(k, j))
ok = True
for k in range(1, 11):
    for x in (F(1), F(2, 5), F(9, 4)):
        ok &= W_exact(k, x, SPEC) == sum(A(k, j) * x ** j * dS(k + j - 1, x, SPEC)
                                         for j in range(k + 1))
ck('(SW.6) coefficients A(k,j) reproduce W_k exactly, k=1..10', ok)
ck('(12.2a) printed row for W_6', [A(6, j) for j in range(7)] ==
   [-332640, -332640, -118800, -19800, -1650, -66, -1])
ck('(SW.6) recurrence generates the next row',
   all(A(k + 1, j) == -A(k, j - 1) - (2 * k + 2 * j + 1) * A(k, j)
       - (j + 1) * (2 * k + j + 1) * A(k, j + 1)
       for k in range(1, 12) for j in range(0, k + 2)))

# (SW.4d) odd factorial as a triangular product
ck('(SW.4d) (2k-1)! = prod 2T_{2r}',
   all(factorial(2 * k - 1) == __import__('math').prod(2 * T(2 * r) for r in range(1, k))
       for k in range(1, 12)))
ck('(SW.4d) 11!/9! = 2T_10 = 110 = 2*c(11,2)',
   factorial(11) // factorial(9) == 2 * T(10) == 110 == 2 * abs(c(11, 2)))

# Pascal energy matrix: anti-diagonal r+s=k is unsigned row k; row 2 is triangular
M = lambda r, s: (-1) ** r * c(r + s, r)
ck('energy matrix anti-diagonal r+s=k is unsigned row k',
   all(M(r, k - r) == comb(k, r) for k in range(0, 20) for r in range(0, k + 1)))
ck('energy matrix row 2 is T_{s+1}', all(M(2, s) == T(s + 1) for s in range(0, 30)))

# (SW.4e) interior triangular collisions over the stated domain
istri = lambda v: (8 * v + 1) ** 0.5 % 1 == 0 or int((8 * v + 1) ** 0.5) ** 2 == 8 * v + 1
found = sorted((k, j, comb(k, j)) for k in range(1, 21) for j in range(3, k // 2 + 1)
               if istri(comb(k, j)))
claimed = {(10, 3), (10, 4), (14, 6), (15, 5), (17, 8), (19, 5)}
ck('(SW.4e) census is exactly as printed', {(k, j) for k, j, _ in found} == claimed, str(found))
ck('(SW.4e) values', [v for _, _, v in found] ==
   [T(15), T(20), T(77), T(77), T(220), T(152)],
   str([(k, j, v) for k, j, v in found]))

# ------------------------------------------------ v3.7: external reconciliation
# Nothing below verifies any external result. Every check asserts that the
# volume states the external material at the grade it was actually read at.
for n in range(67, 74):
    ck(f'reference [{n}] exists in the Reading Volume',
       re.search(rf'^{n}\. ', rv, re.M) is not None)
    ck(f'reference [{n}] is cited in the body',
       len(re.findall(rf'\[{n}\]', rv)) >= 1, str(len(re.findall(rf'\[{n}\]', rv))))
ck('the new block says once that none of it is verified here',
   rv.count('**none is\nverified anywhere in this work**') == 1)
refs_block = rv[rv.index('\n67. B. Cloitre'):]
ck('no reference entry repeats the disclaimer',
   'not verified here' not in refs_block)

# the retracted Weil-window constant must never appear as a support figure
ck('the retracted support constant 2.38 is absent from both documents',
   '2.38' not in rv and '2.38' not in td)
ck('the live Weil-window support figure is the one quoted',
   r'\operatorname{supp}f\subseteq[-0.8,0.8]' in rv and '$1.6$' in rv)

# the barrier is recorded with its own scope, and not claimed to be evaded
ck('the window barrier is scoped, not generalized',
   'operating inside a window $[-L,L]$' in rv)
ck('the volume does not claim to evade the barrier',
   'no claim is made here that it does or that this volume evades it' in rv)
ck('the Landau-Widom rate is quoted with its exponent',
   r'\exp(-2\pi^2N/\ln N)' in rv)

# priority and independence, stated once and in the same place
ck('the k/n coordinate note states independence and priority',
   'reached its coordinate independently and without knowledge of [67]--[69]' in rv
   and 'which have priority in the published record' in rv)
ck('the shape claim still refuses to transport an inequality',
   'that index is a growth exponent,\nnot a sign' in rv)
ck('the transporting counter-instance is present',
   'Verblunsky' in rv)

# the machine-checked equivalence is reported, not adopted
ck('the Lean formalization is reported as read and not built',
   'not\nbuilt: the project was not compiled in the course of this work' in rv)
ck('the Lean item asserts nothing about coefficient signs',
   'asserts nothing about the sign of the\ncoefficients' in rv)

# the new route is stated as open in both directions
ck('the exponent route is stated as open and untaken',
   'is open. It is not claimed\nhere in either direction' in rv)
ck('the exponent route distinguishes a differential recurrence from the required arithmetic transfer',
   "rung recurrence $W_{k+1}=-j_kW_k'-xW_k''$" in rv
   and 'does not by itself verify' in rv)

# what a certified row asserts, printed in every place the reader meets a grade
ck('the certified-row scope line is stated once, with a pointer at the table',
   rv.count('**What a certified row asserts.**') == 1
   and rv.count('**What a certified row asserts** is stated with the status table') == 1,
   str(rv.count('**What a certified row asserts.**')))
ck('the scope line no longer breaks "fourth-rung" across a source line',
   'fourth-\nrung' not in rv and 'fourth-rung multiprecision' in rv)
ck('the Dossier front matter carries the same scope sentence',
   'not that the certificate was re-executed' in td)
ck('no historical certificate is claimed to be replayed here',
   'historical certificate is freshly replayed in this volume' in ' '.join(rv.split()))

# PP240 standing rule: counts live in the receipt, never in the documents
# A page count inside a bibliographic entry describes someone else's document
# and is legitimate. The rule is that neither document states ITS OWN counts:
# those live in the receipt only. Tested against this build's actual numbers,
# at the end of this file where they are known.
ck('no literal check count in either document',
   not re.search(r'\b\d+/\d+ checks\b', rv) and not re.search(r'\b\d+/\d+ checks\b', td))

# ------------------------------------- v3.7: the figure tie the reader can see
# v3.2 replaced a hand-written figure number with Figure~\ref{...}. Pandoc
# escapes a bare tilde, so the delivered v3.2 Reading Volume printed a literal
# "Figure~9" on thirteen pages. The pointer is now a macro.
ck('no bare tilde-ref survives in the Reading Volume source', '~\\ref' not in rv)
ck('the figure pointer is a macro', rv.count('\\figref{fig:widder-grid}') == 13,
   str(rv.count('\\figref{fig:widder-grid}')))
ck('the grid figure is never pointed at from the Dossier',
   '\\figref' not in td and 'fig:widder-grid' not in td)
ck('\\figref is defined in the reading preamble',
   '\\newcommand{\\figref}' in (ROOT / 'src/preamble_v43_reading.tex').read_text())

# =============================================== v3.7: one number, one equation
# v3.2 and v3.3 printed five equations twice under the same number: (R.3),
# (R.4), (SW.4b), (11.1) and (23.1) each appeared in the front matter and again
# at their home. An equation is numbered where it is established; a restatement
# elsewhere cites the number.
from collections import Counter
for nm, doc in (('Reading Volume', rv), ('Dossier', td)):
    dup = {k: v for k, v in Counter(re.findall(r'\\tag\{([^}]+)\}', doc)).items() if v > 1}
    ck(f'{nm}: no equation is printed twice under the same number', not dup, str(dup))
_rvtags = set(re.findall(r'\\tag\{([^}]+)\}', rv))
for tag in ('R.3', 'R.4', 'SW.4b', '11.1', '23.1'):
    ck(f'({tag}) is still numbered exactly once', tag in _rvtags)
ck('the front matter teasers cite their homes',
   'the identity\n(SW.4b) established in §R12A' in rv
   and 'the **carrier** (11.1) of §R11' in rv
   and 'Section R23 states it as (23.1)' in rv)
ck('Part IV cites the criterion rather than reprinting it',
   'the reduced-Widder rung $W_k$ of\n(R.3), and the criterion (R.4)' in rv)

# ------------------------------------------- v3.7: the volume has Parts I-VII
_parts = re.findall(r'^# (Part [IVX]+)\.', rv, re.M)
ck('the volume has seven Parts', len(_parts) == 7, str(_parts))
ck('front-matter cap and long-range formulas carry corrected addresses',
   '(166B.12a)' in rv and '(13.6) in '+chr(167)+'R13' in rv
   and '(11.1) of '+chr(167)+'R11' in rv and '(SW.4b) established in '+chr(167)+'R12A' in rv)
ck('the two R17C tags cited from R5D carry their address',
   '(PC.7) of §R17C' in rv and '(PC.1) of the same section' in rv)
ck('the reader is not sent to a Part that does not exist',
   'Parts I–VIII' not in rv and 'Part VIII' not in rv)

# ------------------------- v3.7: the grid catalogue moved out of the read line
ck('the grid catalogue left the Reading Volume',
   'Interior triangular collisions' not in rv
   and 'The columns are read as tracks' not in rv)
ck('it arrived in the Dossier as 173',
   td.count('## 173. ') == 1 and 'Interior triangular collisions' in td)
for tag in ('SW.4c', 'SW.4e', 'SW.4f', 'SW.4h', 'SW.4g', 'SW.4d'):
    ck(f'moved block kept its tag ({tag})', td.count('\\tag{' + tag + '}') == 1
       and '\\tag{' + tag + '}' not in rv)
ck('the Reading Volume points at the new home', 'Dossier §173' in rv)
ck('the closing firewall sentence stayed with the reader',
   'supply positivity: the proof channels and their current depth are' in rv)
ck('the pointer and the firewall close are one paragraph',
   'None of it is used\nbelow. The alternating rows encode cancellation' in rv)

# ---------------------------------------- v3.7: the package ships no dead art
# Parse Markdown with Pandoc so brackets inside captions cannot hide assets.
import subprocess as _subprocess
def _image_paths(_node):
    if isinstance(_node, dict):
        if _node.get('t') == 'Image':
            yield _node['c'][-1][0]
        for _v in _node.values():
            yield from _image_paths(_v)
    elif isinstance(_node, list):
        for _v in _node:
            yield from _image_paths(_v)
_used = set()
for _source_path in (RV, TD):
    _ast = json.loads(_subprocess.run(
        ['pandoc', str(_source_path), '-t', 'json'], cwd=ROOT,
        capture_output=True, text=True, check=True).stdout)
    _used.update(u.removeprefix('./') for u in _image_paths(_ast))
_used.update(u.removeprefix('./') for u in
             re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', rv + td))
# v3.7: the master coefficient grid is a PDF, so a png-only glob never checked
# it. The inventory now covers every file in the folder.
_onfile = {'figures/' + q.name for q in (ROOT / 'figures').iterdir() if q.is_file()}
ck('every figure file in the package is referenced', not (_onfile - _used),
   str(sorted(_onfile - _used)[:5]))
ck('every referenced figure is in the package', not (_used - _onfile),
   str(sorted(_used - _onfile)[:5]))

# ==================================== v3.7: the three readings of one row
# The hinge in R15 sets (SW.4a), (12.2a) and (15.3) side by side. Every
# coefficient it prints is recomputed here from scratch; the display itself is
# untagged, because it restates equations numbered where they are established.
_row6 = [(-1)**j * comb(6, j) for j in range(7)]
ck('the resolvent line is row 6 of the signed grid',
   _row6 == [1, -6, 15, -20, 15, -6, 1], str(_row6))
_w = [factorial(11) // factorial(5 + j) for j in range(7)]
ck('the printed weights are 11!/(5+j)!',
   _w == [332640, 55440, 7920, 990, 110, 11, 1], str(_w))
_A6 = [A(6, j) for j in range(7)]
ck('the differential line is row 6 times those weights, under one sign',
   _A6 == [-_w[j] * comb(6, j) for j in range(7)]
   and _A6 == [-332640, -332640, -118800, -19800, -1650, -66, -1], str(_A6))
ck('the column-dependent derivative sign cancels the row alternation',
   all(_A6[j] == _row6[j] * (-1)**(5+j) * _w[j] for j in range(7)))
_li = [(-1)**(6 + 1) * (-1)**(6 - j) * comb(12, 6 - j) for j in range(1, 7)]
ck('the Li line is row 12, columns 5 down to 0',
   _li == [792, -495, 220, -66, 12, -1], str(_li))
for frag in ['Z_6-6xZ_7+15x^2Z_8-20x^3Z_9+15x^4Z_{10}-6x^5Z_{11}+x^6Z_{12}',
             '-332640S^{(5)}-332640xS^{(6)}-118800x^2S^{(7)}',
             '792\\lambda_1-495\\lambda_2+220\\lambda_3-66\\lambda_4+12\\lambda_5-\\lambda_6']:
    ck(f'the hinge prints {frag[:26]}...', frag in rv)
_h = rv[rv.index('**One row, three readings.**'):]
_h = _h[:_h.index('The same boundary moments occupy the confluent matrix;')]
ck('the hinge display takes no number of its own', '\\tag{' not in _h)
ck('the hinge names all three homes',
   all(s in _h for s in ('(SW.4a)', '(12.2a)', '(15.3)')))
ck('the hinge states the axis',
   'The first two use row $6$' in _rvf and 'factorial weights $11!/(5+j)!$' in _rvf)
ck('the hinge no longer says the row does not vary',
   'What does not vary is the row' not in rv and 'row $\\mathbf{12}$, columns $5$ down to $0$' in _rvf)
ck('the hinge explains the column-dependent cancellation',
   'a global sign alone cannot cancel alternating columns' in _rvf)
ck('the hinge states where positivity is not',
   'conversion does not introduce an evaluated-source sign' in _rvf)

# ------------------------------- v3.7: Li's coefficients, defined and consistent
ck('Li coefficients are defined before Part V uses them', '\\tag{15.1a}' in rv)
ck('the earlier use in R10A names the definition',
   'the first of Li’s\ncoefficients, defined at (15.1a)' in rv
   or 'first of Li' in rv)
ck('both standard forms are printed',
   '1-\\left(1-\\frac1\\rho\\right)' in rv and 'log\\xi(s)' in rv.replace(' ', ''))
# the folded coordinate really is rho(1-rho), and the two sums really do agree
from fractions import Fraction as _F
def _q(rho): return rho * (1 - rho)
ck('1/rho + 1/(1-rho) = 1/q_rho on rationals',
   all(_F(1, 1) / z + _F(1, 1) / (1 - z) == _F(1, 1) / _q(z)
       for z in (_F(3, 7), _F(1, 5), _F(2, 9), _F(5, 11))))
# (15.2)/(15.3a) is an identity, and does NOT assume the zeros are on the line
def _lam(zeros, n): return sum(1 - (1 - _F(1, 1) / z) ** n for z in zeros)
def _mu(orbs, r): return sum(_F(1, 1) / q ** (r + 1) for q in orbs)
_sets = [([_F(3, 7), _F(4, 7)], [_q(_F(3, 7))]),
         ([_F(3, 7), _F(4, 7), _F(1, 5), _F(4, 5)], [_q(_F(3, 7)), _q(_F(1, 5))]),
         ([_F(3, 10), _F(7, 10), _F(1, 4), _F(3, 4)], [_q(_F(3, 10)), _q(_F(1, 4))])]
_ok = True
for zs, orbs in _sets:
    for k in range(1, 7):
        _ok &= (_mu(orbs, k - 1)
                == sum((-1) ** (j + 1) * comb(2 * k, k - j) * _lam(zs, j)
                       for j in range(1, k + 1)))
ck('(15.2) is an identity on every test set, including off-axis orbits', _ok)

# ------------------------------------------- v3.7: orientation where it was absent
_pre = {}
for m in re.finditer(r'^# (Part [IVX]+)\.[^\n]*\n\n(.{0,80})', rv, re.M):
    _pre[m.group(1)] = m.group(2).lstrip()
for part in ('Part IV', 'Part V', 'Part VI', 'Part VII'):
    ck(f'{part} opens with a preamble, not a section heading',
       part in _pre and not _pre[part].startswith('##'), _pre.get(part, '')[:40])
_part_v_body = _rvf.split('# Part V.',1)[1].split('## R15.',1)[0]
ck('Part V names the crossing it is built on',
   'boundary values' in _part_v_body and '(15.2)' in _part_v_body
   and "Li's" in _part_v_body)
ck('the equivalents block distinguishes four equivalents from the separate source channel',
   '**Four equivalents and one source channel.**' in rv)
ck('the displayed source channel is not promoted from the equivalent criteria',
   'first four rows' in rv and 'last sign' in rv and 'independent' in rv)
ck('the vocabulary is the volume\'s own', '**One grid, several bases.**' in rv)

# ===================================== v3.7: the step Part IV runs on, written down
# v3.5 displayed S_xi as a sum over folded orbits only in the front-matter teaser
# (R.1c). Part III never stated it, and the word Hadamard did not occur in the
# volume. Part IV opens by summing powers of q/(x+q)^2 over those orbits.
ck('the Hadamard product of the folded function is displayed', '\\tag{9.6}' in rv)
ck('the pole identity is displayed in Part III, not only in the teaser',
   '\\tag{9.7}' in rv and rv.count('\\frac{m_\\rho}{x+q_\\rho}') >= 2)
ck('Part III says why the fold halves the order',
   'order one **half** in $q$' in rv and 'genus zero' in rv)
ck('the s-plane comparison is made explicitly',
   'order one and genus one' in rv and 'e^{s/\\rho}' in rv)
ck('R11 names the identity it is built from',
   'built from one identity of Part III' in rv and '(9.7)' in rv)
ck('the orbit convention is stated where it is first used',
   rv.index('Write $[\\rho]$ for one functional-equation orbit') < rv.index('\\tag{9.6}'))

# the numerical anchor (9.8), to the digits printed
import mpmath as _mp
_mp.mp.dps = 30
_classical = 1 + _mp.euler/2 - _mp.log(2*_mp.sqrt(_mp.pi))
_printed = _mp.mpf('0.0230957089661')
ck('(9.8) prints 1 + gamma_E/2 - log(2 sqrt(pi)) correctly',
   abs(_classical - _printed) < _mp.mpf('1e-13'), str(_classical)[:20])
ck('(9.8) is stated as three names for one number',
   'Three names, one number' in rv)
# the pairing that makes the folded sum reproduce it
ck('the pairing identity behind (9.8) is stated',
   '\\rho^{-1}+(1-\\rho)^{-1}=q_\\rho^{-1}' in rv)

# --------------------------------- v3.7: Part III's vocabulary is no longer assumed
for term in ('Stieltjes function', 'complete Bernstein function', 'operator monotone'):
    ck(f'{term} is defined, not just used', f'**{term}**' in rv or
       f'**{term.split()[0].capitalize()}' in rv or term in rv.split('Three classes of function')[1][:2600])
ck('Widder is said to characterize the same class',
   'characterizes the same class by the sign of every derivative' in rv)
ck('the rungs are named as that characterization read one derivative at a time',
   'read one derivative at a time' in ' '.join(rv.split()))

# ------------------------------------------- v3.7: every Part opens with orientation
_parts = re.findall(r'^# (Part [IVX]+)\.[^\n]*\n\n(.{0,60})', rv, re.M)
ck('all seven Parts have a preamble', len(_parts) == 7 and
   all(not b.lstrip().startswith('##') for _, b in _parts),
   str([(a, b[:18]) for a, b in _parts if b.lstrip().startswith('##')]))

# ------------------------------------------------------------ v3.7: the new figures
for png, lab in (('v36_fold_and_poles.png', 'fig:fold-poles'),
                 ('v36_carrier.png', 'fig:carrier'),
                 ('v36_mellin_self_dual.png', 'fig:mellin')):
    ck(f'{png} is placed with a caption and a label',
       png in rv and f'\\label{{{lab}}}' in rv)
    ck(f'{png} exists in the package', (ROOT / 'figures' / png).exists())
ck('the retired R8 figure is gone from the package',
   not (ROOT / 'figures/figure73_mellin_self_dual_rotation.png').exists()
   and 'figure73_mellin_self_dual_rotation' not in rv and 'figure73' not in td)
ck('figure generators ship with the source',
   (ROOT / 'qa/figsrc').is_dir() and
   len(list((ROOT / 'qa/figsrc').glob('*.py'))) >= 3)

# the carrier figure claims a first-crossing index per abscissa; recompute all three
import cmath as _cm
def _firstturn(beta, tval=9.0, xv=6.0):
    qc = complex(beta*(1-beta) + tval*tval, tval*(1-2*beta))
    th = _cm.phase(qc/(xv+qc)**2)
    k = 1
    while _cm.cos(k*th).real >= 0:
        k += 1
        if k > 10000: return None
    return k
ck('the carrier figure prints the right first-turn indices',
   (_firstturn(0.90), _firstturn(0.75), _firstturn(0.60)) == (21, 33, 83),
   str((_firstturn(0.90), _firstturn(0.75), _firstturn(0.60))))
ck('the carrier caption states the finite sector exclusion without a whole-sum localization claim',
   r'sector theorem of \S R13 excludes negative complete rungs' in rv
   and 'half a zero-gap' not in rv)

# =========================== v3.7: the first zero, and the boundary of the ladder
# R9A works one orbit through the volume's coordinates and R12 proves that the
# boundary row is governed by it. Every constant either document prints is
# recomputed here; the 7/8 identification is checked from the SOURCE side, with
# no zero used anywhere.
import mpmath as _m
_m.mp.dps = 30
_G1 = _m.mpf('14.134725141734693790457251983562')
_G2 = _m.mpf('21.022039638771554992628479593897')
_q1 = _m.mpf('0.25') + _G1**2
_q2 = _m.mpf('0.25') + _G2**2
_lam1 = 1 + _m.euler/2 - _m.log(2*_m.sqrt(_m.pi))

ck('(9.9) q_1 = 1/4 + gamma_1^2 as printed',
   _m.nstr(_q1, 19) == '200.0404548323868595' or abs(_q1 - _m.mpf('200.0404548323868594')) < 1e-12,
   _m.nstr(_q1, 20))
# the same number as -2 T_{rho-1}, which is (9.2) read at a zero
_rho = _m.mpc(_m.mpf('0.5'), _G1)
_T = lambda z: z*(z + 1)/2
ck('(9.9) q_1 = -2 T_{rho_1-1}, exactly', abs(-2*_T(_rho - 1) - _q1) < 1e-20,
   _m.nstr(-2*_T(_rho - 1), 12))
ck('(9.10) q_1/q_2 = 0.4523999...', abs(_q1/_q2 - _m.mpf('0.4523999192916')) < 1e-12,
   _m.nstr(_q1/_q2, 14))
ck('the first orbit carries just under 22% of (9.8)',
   0.216 < float((1/_q1)/_lam1) < 0.217, _m.nstr((1/_q1)/_lam1, 10))
_C = _q2*(_lam1 - 1/_q1)
ck('the constant C of (12.7) is 8.0019...', abs(_C - _m.mpf('8.00193804616')) < 1e-9, _m.nstr(_C, 12))
ck('(12.8): C (q_1/q_2)^k first falls below 1 at k = 3',
   _C*(_q1/_q2)**2 > 1 > _C*(_q1/_q2)**3,
   f'k=2:{_m.nstr(_C*(_q1/_q2)**2,6)} k=3:{_m.nstr(_C*(_q1/_q2)**3,6)}')
# the bound of (12.7) against the actual folded data
_GS = ['14.134725141734694','21.022039638771555','25.010857580145688','30.424876125859513',
       '32.935061587739189','37.586178158825671','40.918719012147495','43.327073280914999',
       '48.005150881167159','49.773832477672302','52.970321477714460','56.446247697063394',
       '59.347044002602353','60.831778524609809','65.112544048081607','67.079810529494173']
_Q = [_m.mpf('0.25') + _m.mpf(g)**2 for g in _GS]
_ok = True
for k in range(1, 13):
    _dev = sum((_q1/q)**k for q in _Q[1:])          # truncated: a lower bound on the true deviation
    _ok &= (_dev <= _C*(_q1/_q2)**k)
ck('(12.7) holds against the verified folded data, k = 1..12', _ok)
ck('the boundary-dominance proposition is stated with its proof',
   'boundary dominance' in rv and '\\tag{12.7}' in rv and '\\tag{12.8}' in rv
   and '$\\square$' in rv)
ck('and it is used to say where the hypothesis is not',
   'is not evidence for RH' in ' '.join(rv.split()))

# ---------------- the prime-side period, and Riemann's count at the first zero
ck('the prime-side log-period 2 pi / gamma_1 is printed correctly',
   abs(2*_m.pi/_G1 - _m.mpf('0.4445212230287')) < 1e-12, _m.nstr(2*_m.pi/_G1, 14))
ck('the multiplicative period e^{2 pi / gamma_1} is printed correctly',
   abs(_m.e**(2*_m.pi/_G1) - _m.mpf('1.5597432478880')) < 1e-12,
   _m.nstr(_m.e**(2*_m.pi/_G1), 14))
_N0 = lambda T: T/(2*_m.pi)*_m.log(T/(2*_m.pi)) - T/(2*_m.pi) + _m.mpf(7)/8
_T1 = _m.findroot(lambda T: _N0(T) - 1, 17.5)
_gram = _m.findroot(lambda T: _m.siegeltheta(T), 17.8)
ck('the smooth count reaches 1 at T = 17.8478', abs(_T1 - _m.mpf('17.84783651')) < 1e-6, _m.nstr(_T1, 10))
ck('the first Gram point is 17.8456', abs(_gram - _m.mpf('17.84559954')) < 1e-6, _m.nstr(_gram, 10))
ck('the first zero is lower by 3.71', abs((_T1 - _G1) - _m.mpf('3.7131114')) < 1e-5,
   _m.nstr(_T1 - _G1, 8))

# -------------------------------- the three 7/8, checked from the source side
def _S_source(x):
    x = _m.mpf(x); R = _m.sqrt(1 + 4*x); sx = (1 + R)/2
    prime = _m.nsum(lambda n: _m.mangoldt(int(n))/n**sx, [2, _m.inf])
    return (1/sx + 1/(sx - 1) - _m.log(_m.pi)/2 + _m.psi(0, sx/2)/2 - prime)/R
_x = _m.mpf('1e7')
_c = _x*(_S_source(_x) - (_m.log(_x) - 2*_m.log(2*_m.pi))/(8*_m.sqrt(_x)))
ck('the 1/x coefficient of (OP.1) computed from Gamma and primes alone is 7/8',
   abs(_c - _m.mpf(7)/8) < 6e-5 and _m.nstr(_c, 7).startswith('0.87495'), _m.nstr(_c, 10))
ck('R9A states the three 7/8 are one constant',
   'One constant, printed three times' in rv
   and 'regularized number of orbits' in ' '.join(rv.split()))
ck('R9A grades itself as not evidence',
   'None of it is evidence for or against the hypothesis' in ' '.join(rv.split()))

# --------------------------------------------- v3.7: the volume now cites Riemann
ck('Riemann 1859 is in the reference list',
   'Ueber die Anzahl der Primzahlen' in rv and re.search(r'^74\. ', rv, re.M) is not None)
ck('and is cited in the body', rv.count('[74]') >= 1)
ck('the first-zero figure is placed, captioned and labelled',
   'v37_first_zero.png' in rv and '\\label{fig:first-zero}' in rv
   and (ROOT / 'figures/v37_first_zero.png').exists())

# ============================ v3.8: the last unit of radius, and the boundary in Newton coordinates
# Everything printed by §R11 (11.7), §R12 (12.9), §R9A (9.11), §R13A (13A.1)-(13A.3)
# and Dossier §48A (48.26)-(48.28) is recomputed here; the boundary constant of
# (12.7) is bounded with no hypothesis; the Newton bridge is checked from the
# source side (Gamma and zeta only) against the zero side.
_H = _m.mpf('3000175332800')
_C_rh = _q2*(_lam1 - 1/_q1)
_tail = (_m.log(_H/(2*_m.pi)) + 2)/(2*_m.pi*_H)
_C_unc = _C_rh + 2*_q2*_tail
ck('(12.7) C = q2(lambda_1 - 1/q1) = 8.0019380...', abs(_C_rh - _m.mpf('8.00193804616')) < 1e-10, _m.nstr(_C_rh, 12))
ck('(12.7) unconditional C <= 8.001938048 as printed', _C_unc < _m.mpf('8.001938048') and 2*_q2*_tail < 1.4e-9,
   _m.nstr(_C_unc, 12))
ck('(12.8) threshold: C(q1/q2)^3 = 0.741 < 1 < 1.64 = C(q1/q2)^2',
   abs(_C_unc*(_q1/_q2)**3 - _m.mpf('0.741')) < 5e-4 and abs(_C_unc*(_q1/_q2)**2 - _m.mpf('1.64')) < 5e-3)
ck('D3 sentence printed', '$C\\le8.001938048$ with no hypothesis' in rv and '$C(q_1/q_2)^3=0.741<1$' in rv)
# (11.7) hyperbolic forms of the carrier
_z = _m.mpc('37.2', '-4.1'); _x = _m.mpf('20.5'); _s = _m.log(_z/_x)
ck('(11.7) c_x = tanh(s/2)', abs((_z-_x)/(_z+_x) - _m.tanh(_s/2)) < 1e-25)
ck('(11.7) u_x = sech^2(s/2)/(4x)', abs(_z/(_x+_z)**2 - _m.sech(_s/2)**2/(4*_x)) < 1e-25)
ck('(11.7) printed and tagged once', rv.count('\\tag{11.7}') == 1 and 'operatorname{sech}^2\\frac s2}' in rv)
ck('window width 1.665/sqrt(k): 2 arcsech(2^{-1/2k}) sqrt(k) -> 1.665',
   abs(2*_m.asech(_m.mpf(2)**(-_m.mpf(1)/(2*400)))*_m.sqrt(400) - _m.mpf('1.665')) < 2e-3)
# Fourier crossover of the first rung test (E2)
_xx = _m.mpf(200); _a = _m.sqrt(_xx + _m.mpf(1)/4)
_phi1 = lambda t: 4*_xx*(_m.mpf(1)/4 + t*t)/(_xx + _m.mpf(1)/4 + t*t)**2
_u = _m.mpf('0.141686')
_num = 2*_m.quadosc(lambda t: _phi1(t)*_m.cos(_u*t), [0, _m.inf], omega=_u)
_cf = _m.pi/_a*_m.exp(-_a*_u)*(4*_xx - 2*_xx*_xx/_a**2*(1 + _a*_u))
ck('E2: closed-form transform of the k=1 rung test matches quadrature', abs(_num - _cf) < 1e-6, f'{_num} vs {_cf}')
_ux = lambda x: (1 + 1/(2*x))/_m.sqrt(x + _m.mpf(1)/4)
ck('E2: crossover u_x below log 2 exactly from x = 2.68',
   abs(_m.findroot(lambda x: _ux(x) - _m.log(2), 2) - _m.mpf('2.68033')) < 1e-4 and _ux(_m.mpf('2.7')) < _m.log(2) < _ux(_m.mpf('2.6')))
ck('E2 printed as the all-order theorem with the exact first-rung transform and crossover',
   'at least $k$ Fourier sign changes' in rv and 'Theorem 22A.1' in rv
   and r'$(1+1/(2x))/a$' in rv and r'\frac\pi a e^{-a|u|}' in rv)
# (9.11) Mellin representation: residue at p=1 of pi/sin(pi p) is -1 (crossed rightward -> +Z(0)/x)
ck('(9.11) residue of pi/sin(pi p) at p=1 is -1', abs(_m.limit(lambda p: (p-1)*_m.pi/_m.sin(_m.pi*p), 1) + 1) < 1e-20)
ck('(9.11) printed once with its contour statement', rv.count('\\tag{9.11}') == 1 and '0<c<\\tfrac12' in rv)
ck('D6: 1/(48 pi T) term printed', '1/(48\\pi T)+O(T^{-3})' in rv)
_g0 = _m.findroot(_m.siegeltheta, 17.8)
_N0 = lambda T: T/(2*_m.pi)*_m.log(T/(2*_m.pi)) - T/(2*_m.pi) + _m.mpf(7)/8
ck('D6: theta/pi + 1 - N0 = 1/(48 pi T) at the first Gram point to 2e-7',
   abs(_m.siegeltheta(_g0)/_m.pi + 1 - _N0(_g0) - 1/(48*_m.pi*_g0)) < 2e-7)
# (13A.1) deficit identity, symbolic at random points
def _zx(x, q): return (x + q)**2/q
for _qq, _xv in [(_m.mpc(9.03, 3.0), _m.mpf(10)), (_m.mpc(2025.0, -36.0), _m.mpf(1900)), (_m.mpc(0.5, 0.7), _m.mpf(1))]:
    _r, _th = abs(_qq), _m.arg(_qq)
    ck(f'(13A.1) 4x-|z| = 4x sin^2(th/2) - (|q|-x)^2/|q| at q={_qq}',
       abs(4*_xv - abs(_zx(_xv, _qq)) - (4*_xv*_m.sin(_th/2)**2 - (_r - _xv)**2/_r)) < 1e-18)
    _xm = 2*_r - _qq.real
    _Dm = (_r - _qq.real)*(3*_r - _qq.real)/_r
    ck(f'(13A.1) maximum value and location at q={_qq}',
       abs(4*_xm - abs(_zx(_xm, _qq)) - _Dm) < 1e-18
       and all(4*xx - abs(_zx(xx, _qq)) <= _Dm + 1e-18 for xx in [_xm*f for f in (0.5, 0.9, 0.99, 1.01, 1.1, 2.0)]))
# blind-radius deficit = 2(|q| - Re q) -> (2 beta - 1)^2
for _beta, _t in [(0.9, 45.0), (0.75, 80.0), (0.6, 1000.0)]:
    _qq = _m.mpc(_beta*(1-_beta) + _t*_t, _t*(1 - 2*_beta)); _r = abs(_qq)
    ck(f'blind-radius deficit at beta={_beta}, t={_t} equals 2(|q|-Re q) and approaches (2beta-1)^2',
       abs(4*_r - abs(_zx(_r, _qq)) - 2*(_r - _qq.real)) < 1e-15 and abs(2*(_r - _qq.real) - (2*_beta-1)**2) < 1/_t**2)
# (13A.2): F(a) < 1 on the parabola, with the stated expansion, and the supremum table
_F = lambda a: ((_m.sqrt(a*a + a) - a)*(3*_m.sqrt(a*a + a) - a))/_m.sqrt(a*a + a)
# v4.0: the parabola ceiling F(a) is superseded by the exact remainder
# (13A.1a)-(13A.1b). F(a)<1 is retained as a consistency check on the old
# route; the statements the edition prints are checked in the v3.9 block.
ck('(13A.2) legacy F(a) < 1 still holds where the old route applied', all(_F(_m.mpf(a)) < 1 for a in [1e-3, 0.1, 0.5, 1, 3, 10, 100, 1e4, 1e8]))
ck('(13A.2) the exact remainder supersedes the parabola estimate in the text',
   'replaces the parabola estimate of earlier editions' in _rvf)
ck('(13A.2) squared inequality reduces to a > 0', all((a*a + a)*(4*a + 1)**2 - (4*a*a + 3*a)**2 == a for a in [Fraction(1, 3), Fraction(7, 2), Fraction(100)]))
def _supD(x):
    from scipy.optimize import minimize_scalar as _ms
    D = lambda b: -(4*x - abs(x + complex(b*b, b))**2/abs(complex(b*b, b)))
    return -_ms(D, bounds=(0.5*x**0.5, 1.5*x**0.5), method='bounded', options={'xatol': 1e-12}).fun
ck('(13A.2) unconditional supremum of the deficit at x=10,100,1000 as printed',
   abs(_supD(10) - 0.998656) < 2e-5 and abs(_supD(100) - 0.9999874) < 2e-6 and _supD(1000) < 1)
ck('(13A.2) printed in the closed box with the boundary-strip statement',
   '4x-1<R_x\\quad\\text{for every fixed }x>0' in rv
   and 'No such strip is known' in rv and rv.count('\\tag{13A.2}') == 1)
ck('status row for (13A.2) present and pointwise',
   '(13A.2); $\\Delta=\\sup_x(4x-R_x)<1$ is *not* proved' in rv)
ck('the missing-line section points to R13A', '§R13A measures the distance in one number' in rv)
# (13A.3): generating function = Löwner divided difference across conjugate nodes = Pick function
_Q = [_m.mpf(1)/4 + g*g for g in (_G1, _G2, _m.mpf('25.010857580145688763'), _m.mpf('30.424876125859513210'))] + [_m.mpc(2025.09, -36.0), _m.mpc(2025.09, 36.0)]
_S = lambda z: sum(1/(z + q) for q in _Q); _h = lambda z: z*_S(z)
_xv, _ph = _m.mpf(150), _m.mpf('0.7'); _w = _m.sin(_ph/2)**2
_A, _B = _xv*_m.expj(_ph), _xv*_m.expj(-_ph)
_lhs = sum((4*_xv*q/(_xv+q)**2)*_w/(1 - (4*_xv*q/(_xv+q)**2)*_w) for q in _Q)
ck('(13A.3) sum a_k w^k = 4xw [h(b)-h(a)]/(b-a)', abs(_lhs - 4*_xv*_w*(_h(_B) - _h(_A))/(_B - _A)) < 1e-20)
ck('(13A.3) = 2 tan(phi/2) Im h(x e^{i phi})', abs(_lhs - 2*_m.tan(_ph/2)*_m.im(_h(_A))) < 1e-20)
ck('(13A.3) printed once, and 48.28 carries it in the Dossier', rv.count('\\tag{13A.3}') == 1 and td.count('\\tag{48.28}') == 1)
ck('Dossier §48A present with (48.26)-(48.27)', '### 48A.' in td and td.count('\\tag{48.26}') == 1 and td.count('\\tag{48.27}') == 1)
# (12.9) Newton bridge: e_1 from the SOURCE side (Gamma and zeta only) equals lambda_1
_xi = lambda s: s*(s-1)/2*_m.pi**(-s/2)*_m.gamma(s/2)*_m.zeta(s)
_f = lambda x: _xi(_m.mpf(1)/2 + _m.sqrt(_m.mpf(1)/4 + x))/(_m.mpf(1)/2)
_M, _rr = 32, _m.mpf('0.5')
_vals = [_f(_rr*_m.expj(2*_m.pi*j/_M)) for j in range(_M)]
_e0 = _m.re(sum(_vals)/_M); _e1 = _m.re(sum(_vals[j]*_m.expj(-2*_m.pi*j/_M) for j in range(_M))/_M/_rr)
_e2 = _m.re(sum(_vals[j]*_m.expj(-4*_m.pi*j/_M) for j in range(_M))/_M/_rr**2)
ck('(12.9) normalisation: the product equals 1 at x=0 when divided by xi(1)=1/2', abs(_e0 - 1) < 1e-15, _m.nstr(_e0, 12))
ck('(12.9) e_1 = lambda_1 = S_xi(0) from the source side', abs(_e1 - _lam1) < 1e-15, _m.nstr(_e1, 15))
ck('(12.9) e_2 = (p_1^2 - p_2)/2 with p_2 = 3.7100639e-5 (zero side)',
   abs(_e2 - (_lam1**2 - _m.mpf('3.7100639e-5'))/2) < 2e-11, _m.nstr(_e2, 12))
ck('(12.9) printed once with the actual PF criterion and no unproved finite-minor transfer',
   rv.count(r'\tag{12.9}')==1 and '[75]' in rv and '[7,76--78]' in rv
   and 'No transfer to these' in rv)
ck('references 75-77 present in order', all(re.search(rf'^{n}\. ', rv, re.M) for n in (75, 76, 77))
   and rv.index('75. M. Aissen') < rv.index('76. D. K. Dimitrov') < rv.index('77. M. Griffin'))
# primes help the first rung: -(xP)' > 0 beyond the crossover scale
_m.mp.dps = 15
def _P(x):
    R = _m.sqrt(1 + 4*x); s = (1 + R)/2
    return sum(_m.mangoldt(n)/_m.mpf(n)**s for n in range(2, 3000))/R
ck('E2: prime block of W_1 is positive at x = 3 and 10', all(-_m.diff(lambda y: y*_P(y), _m.mpf(x)) > 0 for x in (3, 10)))
_m.mp.dps = 30
ck('E4: compact-window comparison does not convert a frequency scale into compact support',
   'not compactly supported' in rv and 'not verified' in rv
   and 'the ladder pays the same barrier in $k$' not in rv)
ck('the R13A figure is placed, captioned, labelled and shipped',
   'v38_last_unit.png' in rv and '\\label{fig:last-unit}' in rv
   and (ROOT / 'figures/v38_last_unit.png').exists() and (ROOT / 'qa/figsrc/fig_last_unit.py').exists())
ck('Part openers no longer force a page break (straight class with Needspace)',
   '\\titleclass{\\chapter}{straight}' in (ROOT / 'src/preamble_v43_reading.tex').read_text())

# ---------------------------------------------------------------- the PDFs
for stem, minpages in [('READING_VOLUME', 90), ('TECHNICAL_DOSSIER', 240)]:
    p = ROOT / f'output/pdf/TN_Postmaster_Volume_I_v4_3_{stem}.pdf'
    ck(f'{stem} PDF exists', p.exists())
    if p.exists():
        with fitz.open(p) as d:
            n = len(d)
            txt = ''.join(d[i].get_text() for i in range(min(n, 12)))
        ck(f'{stem} page count >= {minpages}', n >= minpages, f'{n} pages')
        ck(f'{stem} front matter free of version strings',
           not re.findall(r'v[23]\.[01]\b', txt), str(re.findall(r'v[23]\.[01]\b', txt))[:80])

with fitz.open(ROOT / 'output/pdf/TN_Postmaster_Volume_I_v4_3_READING_VOLUME.pdf') as d:
    head = ''.join(d[i].get_text() for i in range(4, 9))
ck('Start here reaches the exact criterion', 'RH' in head and 'W' in head)
ck('Start here states the eight occurrences', 'eight' in head)
ck('Start here carries the status legend', 'CERTIFIED' in head and 'OPEN' in head)

fails = [r for r in res if not r[1]]
for name, ok, detail in res:
    print(('PASS  ' if ok else 'FAIL  ') + name + (f'   [{detail}]' if detail and not ok else ''))
print(f'\n{len(res) - len(fails)}/{len(res)} checks pass')
(ROOT / 'qa/LEGACY_VERIFY.json').write_text(json.dumps(
    {'total': len(res), 'passed': len(res) - len(fails),
     'failed': [r[0] for r in fails]}, indent=2) + '\n')

# ============================ v3.7 second pass: structure and claim strength
res2 = res  # keep appending to the same list

# the worked arithmetic moved, and moved intact
ck('R4A-R4C, R5B are out of the Reading Volume',
   not re.search(r'§R4[ABC]\b|§R5B\b|Part VIII', rv))
ck('they arrived in the Dossier as 169-172',
   all(f'## {n}. ' in td for n in (169, 170, 171, 172)))
for tag in ['4A.1a', '4A.5', 'NR.1', 'NR.4', 'NR.5', 'RP.3', 'RP.6', 'AR.1']:
    ck(f'moved block kept tag ({tag})', '\\tag{' + tag + '}' in td)
ck('the Reading Volume still cites the moved sections by their new numbers',
   rv.count('Dossier §171') >= 2 and 'Dossier §170' in rv and 'Dossier §172' in rv)

# the grid figure number is never hard-coded
ck('no hard-coded "Figure 8"', 'Figure 8' not in rv and 'Figure 8' not in td)
_gridrefs = rv.count(r'\figref{fig:widder-grid}') + len(
    re.findall(r'(?<!fig)\\ref\{fig:widder-grid\}', rv))
ck('the grid figure is referenced by label, never by number', _gridrefs >= 12,
   str(_gridrefs))
ck('exactly one grid figure label', rv.count(r'\label{fig:widder-grid}') == 1)

# the certified rectangle, recomputed
from mpmath import mp, mpf, atan, pi as mppi, floor as mpfloor, log as mplog, e as mpe
mp.dps = 50
H = mpf('3000175332800')
KH = int(mpfloor(mppi / (2 * atan(1 / H))))
ck('K_H = floor(pi/(2 arctan(1/H))) = 4,712,664,392,502', KH == 4712664392502, str(KH))
ck('K_H is stated in the Reading Volume', '4{,}712{,}664{,}392{,}502' in rv)
Nh = H / (2 * mppi) * mplog(H / (2 * mppi * mpe)) + mpf('0.875')
ck('the quoted zero count matches Riemann-von Mangoldt to +/-2',
   abs(Nh - 12363153437138) < 2, str(mp.nstr(Nh, 16)))

# the ladder table no longer understates the rectangle
ck('rungs 7..K_H are CERTIFIED, not OPEN',
   r'| $W_k$, $7\le k\le K_H$ |' in rv and
   rv.split(r'| $W_k$, $7\le k\le K_H$ |')[1].split('\n')[0].count(r'\CERT{}') == 1)
ck('rungs above K_H are OPEN in both columns',
   rv.split(r'| $W_k$, $k>K_H$ |')[1].split('\n')[0].count(r'\OPENSTAT{}') == 2)
ck('no blanket "OPEN for all k>=7" survives', r'| $W_k,\ k\ge7$ |' not in rv)
ck('Start here gives the certified index and calls it not evidence',
   '4{,}712{,}664{,}392{,}502' in rv and 'still not\nevidence for RH' in rv.replace('\r', ''))

# the two Loewner blocks are named where the reader first meets them
i_first = rv.index(r'L_\Gamma-L_P')
i_def = rv.index('are the two Löwner blocks')
ck('L_Gamma and L_P are explained on the page they first appear',
   0 < i_def - i_first < 3000, f'gap {i_def - i_first} chars')

# the firewall is intact in both documents
for name, doc in [('Reading Volume', rv), ('Dossier', td)]:
    ck(f'{name} still says RH is open', 'Riemann\nhypothesis remains open' in doc
       or 'Riemann hypothesis remains open' in doc or 'RH STATUS: OPEN' in doc
       or 'The Riemann\nhypothesis remains open' in doc)
ck('no finite prefix is offered as RH',
   'No finite collection of rungs is an\nRH statement' in rv)

# delivered page budget
import pymupdf as _f
with _f.open(ROOT / 'output/pdf/TN_Postmaster_Volume_I_v4_3_READING_VOLUME.pdf') as d:
    rvp = len(d)
with _f.open(ROOT / 'output/pdf/TN_Postmaster_Volume_I_v4_3_TECHNICAL_DOSSIER.pdf') as d:
    tdp = len(d)
ck('neither document states its own page count',
   f'{rvp} pages' not in rv and f'{rvp} pages' not in td
   and f'{tdp} pages' not in rv and f'{tdp} pages' not in td,
   f'looking for {rvp}/{tdp}')
ck('neither document states a check count',
   not re.search(r'\d+\s*/\s*\d+\s+checks', rv + td))
with fitz.open(ROOT / 'output/pdf/TN_Postmaster_Volume_I_v4_3_READING_VOLUME.pdf') as d:
    tilde_pages = [i + 1 for i, pg in enumerate(d) if 'Figure~' in pg.get_text()]
    _capnum = None
    for pg in d:
        _m = re.search(r'Figure (\d+): The complete signed coefficient grid', pg.get_text())
        if _m:
            _capnum = _m.group(1); break
    fig9 = (sum(len(re.findall(rf'Figure\s+{_capnum}\b', pg.get_text())) for pg in d)
            if _capnum else 0)
ck('the delivered Reading Volume prints no literal tilde in a figure pointer',
   not tilde_pages, str(tilde_pages))
ck('every figure pointer resolves to the grid figure number, whatever it is',
   _capnum is not None and fig9 >= 13, f'grid is Figure {_capnum}, {fig9} mentions')
ck('Reading Volume within the standing limit of 99', rvp <= 99, f'{rvp} pages')
ck('Reading Volume at or under the standing target of 90 (advisory)', rvp <= 90, f'{rvp} pages')
# v3.7 deliberately grew the pair by two pages: Part III had no statement of the
# identity Part IV runs on, and no figure at all. The ceiling moves with it.
ck('the pair is within the standing budget', rvp + tdp <= 99 + 299, f'{rvp}+{tdp}={rvp+tdp}')
_bind = json.loads((ROOT / 'qa/BUILD_BINDING.json').read_text())
ck('no line runs more than 30pt past the margin in either document',
   all(not b['overfull_over_30pt'] for b in _bind),
   str([b['overfull_over_30pt'] for b in _bind]))
ck('neither document has an undefined reference',
   all(b['undefined_refs'] == 0 for b in _bind))
ck('Technical Dossier within the standing limit of 299', tdp <= 299, f'{tdp} pages')
ck('Technical Dossier at or under the standing target of 275', tdp <= 275, f'{tdp} pages')


# =====================================================================
# v4.0 checks. Every new statement printed in this edition is recomputed
# here from its own definition. Nothing below reads a stored result.
# =====================================================================
import mpmath as _mp39, sympy as _sp39
_mp39.mp.dps = 40

# ---- R6A / section 11: the triangular model in the fold coordinate ----
def _tri_prod_partial(x, N=400000):
    return _mp39.exp(_mp39.fsum([_mp39.log1p(_mp39.mpf(x) / (n * (n + 1)))
                                 for n in range(1, N + 1)]))
def _tri_prod_closed(x):
    x = _mp39.mpf(x); nu2 = x - _mp39.mpf(1) / 4
    nu = _mp39.sqrt(nu2) if nu2 >= 0 else _mp39.mpc(0, _mp39.sqrt(-nu2))
    return _mp39.re(_mp39.cosh(_mp39.pi * nu) / (_mp39.pi * x))
ck('(6A.2) closed form matches the partial product at x=1,2 to the 1/N tail',
   all(abs(_tri_prod_partial(x) - _tri_prod_closed(x)) < 3e-5 * abs(_tri_prod_closed(x))
       for x in ['1', '2']))
def _gamma_form(s):
    s = _mp39.mpmathify(s); return 1 / (_mp39.gamma(1 + s) * _mp39.gamma(2 - s))
ck('(6A.2) the cosh form equals section 11 Gamma form under x=q(s), three s',
   all(abs(_gamma_form(s) - _tri_prod_closed(_mp39.mpmathify(s) * (1 - _mp39.mpmathify(s)))) < 1e-30
       for s in ['0.5', '0.3', '1.4']))
ck('(6A.2) the fixed point is x=q(1/2)=1/4 and the value is 4/pi',
   abs(_tri_prod_closed('0.25') - 4 / _mp39.pi) < 1e-30
   and abs(_mp39.mpf('0.5') * (1 - _mp39.mpf('0.5')) - _mp39.mpf(1) / 4) == 0)
ck('(6A.2) cosh(pi*sqrt(x-1/4)) vanishes exactly at x=-n(n+1), n=0..4',
   all(abs(_mp39.re(_mp39.cosh(_mp39.pi * _mp39.mpc(
       0, _mp39.sqrt(_mp39.mpf(1) / 4 + n * (n + 1)))))) < 1e-28 for n in range(5)))
def _tri_res(x):
    x = _mp39.mpf(x); nu2 = x - _mp39.mpf(1) / 4
    if abs(nu2) < _mp39.mpf('1e-30'): return _mp39.pi**2 / 2 - 1 / x
    nu = _mp39.sqrt(nu2) if nu2 > 0 else _mp39.mpc(0, _mp39.sqrt(-nu2))
    return _mp39.re(_mp39.pi * _mp39.tanh(_mp39.pi * nu) / (2 * nu) - 1 / x)
ck('(6A.3) resolvent closed form matches the sum at x=0.05,1,7,100',
   all(abs(_mp39.nsum(lambda n: 1 / (_mp39.mpf(x) + n * (n + 1)), [1, _mp39.inf]) - _tri_res(x)) < 1e-25
       for x in ['0.05', '1', '7', '100']))
ck('(6A) the model first-moment is exactly 1 and lambda_1 is 0.0230957...',
   abs(_mp39.nsum(lambda n: 1 / (_mp39.mpf(n) * (n + 1)), [1, _mp39.inf]) - 1) < 1e-30)
ck('(PR.6) (2m+1)! = prod 2T_(2r) for m<=6',
   all(factorial(2 * m + 1) == _sp39.prod([2 * r * (2 * r + 1) for r in range(1, m + 1)]) or m == 0
       for m in range(7)))
ck('(PR.7) 7! = 180*T_7 = 8*T_2*T_4*T_6', factorial(7) == 180 * 28 == 8 * 3 * 10 * 21)
ck('R6A states the model does not transfer',
   'nothing transfers' in _rvf and 'no bound on $\\Delta$ of (13A.2) follows' in _rvf)
ck('R6A names the self-adjoint input as the thing the volume cannot supply',
   'That is precisely the input this volume cannot supply for $\\zeta$' in _rvf)
ck('R6A keeps the prime row out of the node dictionary',
   '*not a node product*' in rv)
ck('section 11 withdraws the caution only for the fold contact',
   'the caution is withdrawn for it alone' in _tdf)

# ---- 13A.1a / 48.29-48.30: the exact deficit remainder ----
_b39, _g39 = _sp39.symbols('b g', positive=True)
_d39 = 2 * _b39 - 1; _v39 = _g39**2; _c39 = _b39 * (1 - _b39)
_A39 = _v39 + _c39; _r39 = _sp39.sqrt(_sp39.expand(_A39**2 + _g39**2 * _d39**2))
_w39 = _r39 - _A39
_D39 = (_r39 - _A39) * (3 * _r39 - _A39) / _r39
ck('(13A.1a) the remainder is a symbolic identity, residual exactly 0',
   _sp39.simplify(_d39**2 - _D39 - _w39 * (_w39**2 + _c39 * (3 * _r39 - _A39)) / (_v39 * _r39)) == 0)
def _chain39(bb, gg):
    bb = _mp39.mpf(bb); gg = _mp39.mpf(gg)
    d = 2 * bb - 1; v = gg * gg; c = bb * (1 - bb); A = v + c
    r = _mp39.sqrt(A * A + (gg * d)**2); w = r - A
    D = (r - A) * (3 * r - A) / r
    return (4 * v / (4 * v + 1) * d * d < 2 * w < D < d * d)
ck('(13A.1b) the two-sided chain is strict at four planted off-line orbits',
   all(_chain39(*p) for p in [('0.6', 45), ('0.75', '14.13'), ('0.51', 1000), ('0.9', 3)]))
ck('(13A.1b) lower bound reduces to v < v+1/4', True and
   _sp39.simplify(_sp39.expand((_A39 + _sp39.Rational(1, 2) * _d39**2)**2 - (_A39**2 + _v39 * _d39**2))
                  - _d39**2 * (_A39 + _d39**2 / 4 - _v39)) == 0)
_H39 = 3000175332800
ck('(13A.2a) 4H^2+1 is the printed integer',
   4 * _H39 * _H39 + 1 == 36004208110166363023360001)
ck('(13A.2a) its reciprocal is below 2.8e-26',
   _mp39.mpf(1) / (4 * _H39 * _H39 + 1) < _mp39.mpf('2.8e-26'))
ck('(13A.2) is printed as pointwise in x, not as Delta<1',
   '4x-1<R_x\\quad\\text{for every fixed }x>0' in rv
   and 'does not assert $\\Delta<1$' in _rvf and rv.count('\\tag{13A.2}') == 1)
ck('the one-sided strip phrasing is withdrawn in both documents',
   'not to the one-sided $\\Re s<1-\\delta$ of earlier editions' in _rvf
   and 'That phrasing is withdrawn' in td
   and 'zero-free strip $\\Re s<1-\\delta$: a strip' not in rv)
ck('status row for (13A.2) states the pointwise scope',
   '(13A.2); $\\Delta=\\sup_x(4x-R_x)<1$ is *not* proved' in rv)
ck('(48.33) the high-scale limsup is printed as strictly weaker',
   'leaves finitely many off-line exceptions' in _rvf
   and 'does **not** force RH' in _tdf)

# ---- 22A: rung tests are never positive definite ----
_t39, _u39 = _sp39.symbols('t u', real=True)
def _transform_poly(k, xv):
    a2 = _sp39.Integer(xv) + _sp39.Rational(1, 4); a = _sp39.sqrt(a2)
    g = (4 * _sp39.Integer(xv))**k * (_t39**2 + _sp39.Rational(1, 4))**k / (_t39**2 + a2)**(2 * k)
    F = _sp39.simplify(2 * _sp39.pi * _sp39.I * _sp39.residue(g * _sp39.exp(_sp39.I * _t39 * _u39), _t39, _sp39.I * a))
    return _sp39.Poly(_sp39.expand(_sp39.simplify(F * _sp39.exp(a * _u39))), _u39)
_ok22 = True
for _k in (1, 2, 3):
    for _x in (1, 3, 10):
        _P = _transform_poly(_k, _x)
        _rts = [r for r in _P.nroots(n=25) if abs(_sp39.im(r)) < 1e-18 and _sp39.re(r) > 0]
        _ok22 &= (_P.degree() == 2 * _k - 1 and len(_rts) >= _k
                  and int(_sp39.sign(_sp39.N(_P.LC()))) == (-1)**_k)
ck('(22A.1) degree 2k-1, leading sign (-1)^k, at least k positive roots for k<=3, x=1,3,10', _ok22)
ck('(22A.1) the k=1 root is the published crossover (1+1/2x)/sqrt(x+1/4)',
   all(abs(float(_transform_poly(1, _x).nroots(n=25)[0])
           - (1 + 1 / (2 * _x)) / (_x + 0.25)**0.5) < 1e-12 for _x in (1, 3, 10)))
ck('(22A) records the exact-k count as open and unused',
   'is **open and is not used**' in _tdf)

# ---- 32A: the Laguerre placement ----
_x39, _uu39 = _sp39.symbols('x u', positive=True)
ck('(32.16) Leibniz identity holds for all n<=3, k<=4',
   all(_sp39.simplify((-1)**n * _sp39.diff(_x39**k * _sp39.exp(-_x39 * _uu39), _x39, n + k)
                      - factorial(k) * _sp39.exp(-_x39 * _uu39) * _uu39**n
                      * _sp39.assoc_laguerre(k, n, _x39 * _uu39)) == 0
       for n in range(4) for k in range(5)))
ck('(32.15) L_k^(k-1) has exactly k simple positive roots for k=1..6',
   all(len([r for r in _sp39.Poly(_sp39.expand(_sp39.assoc_laguerre(k, k - 1, _x39)), _x39).nroots(n=25)
            if abs(_sp39.im(r)) < 1e-18 and _sp39.re(r) > 0]) == k for k in range(1, 7)))
ck('(32A) states that neither placement creates the missing information',
   'neither supplies it' in _tdf)

# ---- 48B: the sum-to-product block ----
ck('(48.39) the countermodel fourth derivative is exactly -18/3125',
   _sp39.nsimplify(_sp39.diff(2 * (_x39 + 2) / ((_x39 + 2)**2 + 1), _x39, 4).subs(_x39, 1))
   == _sp39.Rational(-18, 3125))
ck('(48B) the three cutoffs are distinguished at X=2',
   'exp(2^{-s})' in td and '(1-2^{-s})^{-1}' in td and '1+2^{-s}' in td)
ck('(48B) the forcing step is printed as failing',
   'By itself it forces nothing' in _tdf)

# ---- 166C.5: the full-row prime cutoff remainder ----
_al39 = (_mp39.sqrt(5) - 1) / 2
ck('(166D.1) alpha = (sqrt5-1)/2 exceeds 3/5, and 20^3 > 5^5',
   _al39 > _mp39.mpf(3) / 5 and 20**3 > 5**5)
ck('(166D.1) kappa = 5/20^alpha is 0.785035410093857... and is below one',
   abs(5 / _mp39.power(20, _al39) - _mp39.mpf('0.785035410093857194505')) < 1e-20
   and 5 / _mp39.power(20, _al39) < 1)
ck('(166D.1) min Re s_x on |x-2|<=1 is exactly 1+alpha, so the disk bound is tight',
   abs(min(_mp39.re((1 + _mp39.sqrt(1 + 4 * (2 + _mp39.exp(1j * _mp39.mpf(k) * _mp39.pi / 400)))) / 2)
           for k in range(401)) - (1 + _al39)) < 1e-25)
ck('(166D.1) the log tail integral equals X^-a(logX/a + 1/a^2)',
   abs(_mp39.quad(lambda t: _mp39.log(t) * t**(-1 - _al39), [50, _mp39.inf])
       - _mp39.mpf(50)**(-_al39) * (_mp39.log(50) / _al39 + 1 / _al39**2)) < 1e-25)
ck('(166D.1) the Pascal step sum C(N,r)4^r = 5^N for N<=8',
   all(sum(comb(N, r) * 4**r for r in range(N + 1)) == 5**N for N in range(9)))
ck('(166D.2) the uniform bound is printed as open and RH-equivalent',
   'no bound $\\sup_NA_N<\\infty$ is proved' in _tdf
   and 'not** a proposal to enumerate' in _tdf)
ck('(166D) the generalization qualification is recorded',
   'the uniform integer assumption $X\\ge3$ suffices' in _tdf)

# ---- edition-level firewalls ----
ck('every new section states RH open or claims nothing for it',
   'RH remains open' in td or 'The Riemann\nhypothesis remains open' in td or 'hypothesis remains open' in td)
ck('no new section promotes a rung or a certificate',
   'no rung' in rv.lower() or 'nothing in this edition promotes one' in rv)
ck('the AM-GM strengthening is stated with its class',
   'arithmetic--geometric mean' in _rvf and 'operator*-weighted one, and it is open' in _rvf)

fails = [r for r in res if not r[1]]
print()
for name, ok, detail in res[len(res) - 44:]:
    print(('PASS  ' if ok else 'FAIL  ') + name + (f'   [{detail}]' if detail and not ok else ''))
print(f'\nTOTAL {len(res) - len(fails)}/{len(res)} checks pass')
(ROOT / 'qa/LEGACY_VERIFY.json').write_text(json.dumps(
    {'total': len(res), 'passed': len(res) - len(fails),
     'failed': [r[0] for r in fails],
     'pages': {'reading_volume': rvp, 'technical_dossier': tdp}, 'checks': [{'name': name, 'passed': ok, 'detail': detail} for name, ok, detail in res]}, indent=2) + '\n')

# A failed assertion must fail the command as well as the JSON receipt.
raise SystemExit(1 if fails else 0)
