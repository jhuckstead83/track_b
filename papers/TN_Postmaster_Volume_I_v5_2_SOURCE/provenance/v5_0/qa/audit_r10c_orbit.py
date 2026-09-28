#!/usr/bin/env python3
"""Replay for Reading Volume §R10C and Dossier (155A.4a): the one-orbit chain.

Everything here is exact.  Rationals are `fractions.Fraction`, polynomials are
sympy expressions over Q, and no floating-point number is compared anywhere.

Checks
  1  R7 tie-out      1/q = 2 + z_C + 1/z_C  and  w = -1/z_C, hence
                     1/q = 2 - w - 1/w                              (10C.2)
  2  recurrence      Q_0=0, Q_1=y, Q_{n+1}=2y+(2-y)Q_n-Q_{n-1} reproduces
                     2 - w^n - w^-n for n <= N                      (10C.3-4)
  3  printed rows    (10C.5) and (10C.9) agree with the recurrence
  4  square forms    Q_{2m+1} = y P_m^2 and Q_{2m} = y(4-y) B_{m-1}^2, with
                     P_m from the (155A.1) recurrence AND from the closed
                     coefficient formula (155A.2), B_r = U_r(1-y/2) (155A.4a)
  5  interval        y in (0,4) <=> |w| = 1, at exact sample points, and the
                     characteristic roots have modulus one exactly there
  6  calibration     t = sqrt 2:  q = 9/4, y = 4/9, w = (7 - 4 sqrt2 i)/9,
                     |w|^2 = 1, and Q_1..Q_8 as exact rationals, each computed
                     three independent ways; odd rungs are rational squares
  7  document        the constants this replay certifies are the ones the two
                     volumes print

Usage: python3 qa/audit_r10c_orbit.py [--output qa/R10C_ORBIT.json]
"""
from pathlib import Path
from fractions import Fraction
import argparse
import json
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / 'src' / 'TN_Postmaster_Volume_I_v5_0_READING_VOLUME.md'
DOSSIER = ROOT / 'src' / 'TN_Postmaster_Volume_I_v5_0_TECHNICAL_DOSSIER.md'
N = 16

y, w, s = sp.symbols('y w s')
results = []


def check(name, ok, detail=''):
    results.append({'check': name, 'ok': bool(ok), 'detail': detail})
    print('%-4s %-34s %s' % ('ok' if ok else 'FAIL', name, detail), flush=True)
    return bool(ok)


def rungs(sym=y, upto=N):
    Q = [sp.Integer(0), sym]
    for _ in range(upto):
        Q.append(sp.expand(2 * sym + (2 - sym) * Q[-1] - Q[-2]))
    return Q


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='qa/R10C_ORBIT.json')
    args = ap.parse_args()

    # ---- 1. the R7 tie-out -------------------------------------------------
    zC = s / (1 - s)
    q = s * (1 - s)
    W = 1 - 1 / s
    check('R7: 1/q = 2 + zC + 1/zC',
          sp.simplify(2 + zC + 1 / zC - 1 / q) == 0)
    check('10C: w = -1/zC', sp.simplify(W + 1 / zC) == 0)
    check('10C.2: 1/q = 2 - w - 1/w',
          sp.simplify(2 - W - 1 / W - 1 / q) == 0)

    # ---- 2. recurrence vs closed form --------------------------------------
    Q = rungs()
    ysub = 2 - w - 1 / w
    bad = [n for n in range(1, N + 1)
           if sp.simplify(Q[n].subs(y, ysub) - (2 - w**n - w**(-n))) != 0]
    check('10C.4 reproduces 2 - w^n - w^-n', not bad, 'n <= %d' % N)

    # ---- 3. the rows the Reader prints -------------------------------------
    printed = {1: y, 2: 4 * y - y**2, 3: 9 * y - 6 * y**2 + y**3}
    check('10C.5 rows', all(sp.expand(Q[n] - e) == 0 for n, e in printed.items()))
    factored = {1: y, 2: y * (4 - y), 3: y * (3 - y)**2,
                4: y * (4 - y) * (2 - y)**2, 5: y * (y**2 - 5 * y + 5)**2}
    check('10C.9 factored rows',
          all(sp.expand(Q[n] - e) == 0 for n, e in factored.items()))

    # ---- 4. the square forms, both routes to P_m ---------------------------
    P = [sp.Integer(1), 3 - y]
    for _ in range(N):
        P.append(sp.expand((2 - y) * P[-1] - P[-2]))          # (155A.1)

    def d(m, j):                                              # (155A.2)
        return ((-1)**j * (2 * m + 1) * sp.factorial(m + j)
                / (sp.factorial(m - j) * sp.factorial(2 * j + 1)))
    closed = [sp.expand(sum(d(m, j) * y**j for j in range(m + 1)))
              for m in range(len(P))]
    check('155A.2 coefficient formula = 155A.1 recurrence',
          all(sp.expand(P[m] - closed[m]) == 0 for m in range(N // 2)))

    odd = [m for m in range((N - 1) // 2)
           if sp.expand(Q[2 * m + 1] - y * P[m]**2) != 0]
    check('155A.4a odd: Q_{2m+1} = y P_m^2', not odd)
    even = [m for m in range(1, N // 2)
            if sp.expand(Q[2 * m] - y * (4 - y)
                         * sp.expand(sp.chebyshevu(m - 1, 1 - y / 2))**2) != 0]
    check('155A.4a even: Q_{2m} = y(4-y) B_{m-1}^2', not even)

    # ---- 5. the interval ---------------------------------------------------
    inside, outside = [], []
    for num, den in [(1, 100), (1, 2), (2, 1), (39, 10), (4, 1), (41, 10), (9, 2)]:
        yy = sp.Rational(num, den)
        roots = sp.solve(sp.Eq(sp.Symbol('r')**2 - (2 - yy) * sp.Symbol('r') + 1, 0))
        mods = {sp.simplify(sp.Abs(r)**2) for r in roots}
        on_circle = mods == {sp.Integer(1)}
        (inside if yy <= 4 else outside).append((yy, on_circle))
    check('10C.6: |w| = 1 exactly on 0 < y <= 4',
          all(c for _, c in inside) and not any(c for _, c in outside),
          '%d in, %d out' % (len(inside), len(outside)))

    # ---- 6. the calibration orbit -----------------------------------------
    sc = sp.Rational(1, 2) - sp.I * sp.sqrt(2)
    qc = sp.simplify(sc * (1 - sc))
    wc = sp.simplify(sp.expand(1 - 1 / sc))
    cal_ok = (qc == sp.Rational(9, 4)
              and sp.simplify(1 / qc - sp.Rational(4, 9)) == 0
              and sp.simplify(sp.expand(wc * sp.conjugate(wc)) - 1) == 0
              and sp.simplify(sp.re(sp.expand(wc)) - sp.Rational(7, 9)) == 0)
    check('calibration t=sqrt2: q=9/4, y=4/9, |w|=1, Re w=7/9', cal_ok)

    yq = Fraction(4, 9)
    QF = [Fraction(0), yq]
    for _ in range(9):
        QF.append(2 * yq + (2 - yq) * QF[-1] - QF[-2])
    rows, mismatch, squares = {}, [], {}
    for k in range(1, 9):
        rec = sp.Rational(QF[k].numerator, QF[k].denominator)
        cheb = sp.nsimplify(2 - 2 * sp.chebyshevt(k, sp.Rational(7, 9)))
        poly = sp.nsimplify(Q[k].subs(y, sp.Rational(4, 9)))
        if not (rec == cheb == poly):
            mismatch.append(k)
        rows[k] = '%d/%d' % (QF[k].numerator, QF[k].denominator)
        r = sp.sqrt(rec)
        squares[k] = str(r) if r.is_rational else None
    check('calibration rungs agree three ways', not mismatch,
          'Q1..Q8 exact; Q3 = %s' % rows[3])
    check('calibration: odd rungs are rational squares',
          all(squares[k] is not None for k in (1, 3, 5, 7))
          and all(squares[k] is None for k in (2, 4, 6, 8)),
          'Q3 = (%s)^2' % squares[3])

    # ---- 7. the documents print what was certified -------------------------
    rd, do = READER.read_text(), DOSSIER.read_text()
    need_reader = ['\\boxed{\\;y=\\frac1q=2-w-\\frac1w\\;}',
                   'Q_{n+1}=2y+(2-y)\\,Q_n-Q_{n-1}',
                   'Q_3=9y-6y^2+y^3',
                   'Q_5=y\\,(y^2-5y+5)^2',
                   'Q_{2m}(y)=y(4-y)\\,\\mathcal B_{m-1}(y)^2']
    need_dossier = ['\\tag{155A.4a}',
                    'Q_{2m}(y)=y(4-y)\\,\\mathcal B_{m-1}(y)^2']
    miss = [x for x in need_reader if x not in rd] + \
           [x for x in need_dossier if x not in do]
    check('documents carry the certified statements', not miss, str(miss))

    payload = {'version': 'v5.0', 'section': 'R10C / 155A.4a', 'N': N,
               'calibration': {'t': 'sqrt(2)', 'q': '9/4', 'y': '4/9',
                               'w': '(7 - 4*sqrt(2)*I)/9', 'rungs': rows,
                               'rational_roots': squares},
               'checks': results,
               'result': 'PASS' if all(r['ok'] for r in results) else 'FAIL'}
    (ROOT / args.output).write_text(json.dumps(payload, indent=1) + '\n')
    print(payload['result'])
    sys.exit(0 if payload['result'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
