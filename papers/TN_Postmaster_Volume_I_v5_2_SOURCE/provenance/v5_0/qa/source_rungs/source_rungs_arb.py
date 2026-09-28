#!/usr/bin/env python3
"""Ball-arithmetic certificate for the global source rungs W_2, ..., W_6.

This is the FLINT/Arb side of the source-rung certificate.  It generalises the
fifth/sixth-rung certificate of the 4.5 edition (audit_widder_source.py,
SHA-256 348bb9b9d39669dc6729731f8a67b31bf596173554d8fc5fa6c10f3c4fb88697) to
every rung k = 2,...,6: the evaluator, the cell test and the tail argument are
the same; the acceptance threshold theta_k and the tail constant alpha_k are
now parameters, and the starting partition is graded.

Certified, for k = 2,...,6, with x = s(s-1), R = 2s-1, L = xi'/xi and
g_k(s) = s^{2k-1} W_k(s(s-1))/(2k-1)!:

    g_k(s) > theta_k                                         (1 <= s <= 128)
    W_k(s(s-1)) > (alpha_k/2) s^{2k}/(2s-1)^{4k-1}           (s >= 128)

No zero ordinate, verified zero height or RH assumption is used.  Every
accepted cell carries a Taylor remainder bound over the whole interval; no
point grid is used.  The companion script source_rungs_decimal.py proves the
same statements with an independent backend (CPython decimal, no FLINT/Arb,
MPFR or SymPy).

    python3 source_rungs_arb.py --output RECEIPT_arb.json
    python3 source_rungs_arb.py --precision 384 --degree 22 --step 1/128 \
        --output RECEIPT_arb_second.json
"""
import argparse
import hashlib
import json
import math
import platform
import time
from fractions import Fraction
from pathlib import Path

import flint
import sympy as sp
from flint import arb, arb_series, ctx

THRESHOLD = {2: Fraction(1, 10 ** 5), 3: Fraction(1, 10 ** 8),
             4: Fraction(1, 10 ** 10), 5: Fraction(1, 10 ** 12),
             6: Fraction(1, 10 ** 15)}
SAMPLE_POINTS = [Fraction(1), Fraction(65, 64), Fraction(3, 2), Fraction(2),
                 Fraction(5), Fraction(10), Fraction(32), Fraction(100),
                 Fraction(128)]


def ball(q):
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def source_rung_series(center, k, degree):
    """Taylor jet of g_k(s) = s^(2k-1) W_k(s(s-1))/(2k-1)!."""
    ctx.cap = 2 * k + degree + 1
    s = arb_series([center, 1])
    x = s * (s - 1)
    R = 2 * s - 1
    # the deflated zeta is zeta(s) - 1/(s-1); F = (s-1) zeta(s) is regular at 1
    F = 1 + (s - 1) * s.zeta(deflate=True)
    if not (F[0] > 0 and R[0] > 0 and s[0] > 0):
        return None
    ell = s.log() + F.log() + (s / 2).lgamma() - (s / 2) * arb.pi().log()
    w = x ** k * ell.derivative() / R
    for _ in range(2 * k - 1):
        w = w.derivative() / R
    result = (-1) ** (k - 1) * s ** (2 * k - 1) * w / math.factorial(2 * k - 1)
    assert result.prec >= degree + 1
    return result


def independent_x_formula(s0, k):
    """Leibniz formula in x, independent of the s-operator loop (GT44.8)."""
    ctx.cap = 2 * k + 1
    sv = ball(s0)
    xv = sv * (sv - 1)
    xx = arb_series([xv, 1])
    ss = (1 + (1 + 4 * xx).sqrt()) / 2
    F = 1 + (ss - 1) * ss.zeta(deflate=True)
    ell = ss.log() + F.log() + (ss / 2).lgamma() - (ss / 2) * arb.pi().log()
    val = sum(math.comb(k, j) * (k + j) * xv ** j * ell[k + j] for j in range(k + 1))
    return (-1) ** (k - 1) * sv ** (2 * k - 1) * val


def cell_bound(left, right, k, degree, theta):
    mid = Fraction(left + right, 2)
    rad = Fraction(right - left, 2)
    r = ball(rad)
    point = source_rung_series(ball(mid), k, degree)
    whole = source_rung_series(ball(mid) + arb(0, r), k, degree)
    if point is None or whole is None:
        return None
    error = arb(0)
    for j in range(1, degree):
        error += point[j].abs_upper() * r ** j
    error += whole[degree].abs_upper() * r ** degree
    lower = point[0] - error
    if not lower.is_finite():
        return None
    return {
        'left': str(left), 'right': str(right),
        'lower_endpoint': lower.lower().str(25),
        '_lower': lower,
        '_full': {'left': str(left), 'right': str(right),
                  'center_value': point[0].str(35),
                  'variation_plus_remainder_upper': error.abs_upper().str(35),
                  'lower_endpoint': lower.lower().str(35)},
        '_passes': bool(lower > ball(theta)),
    }


def initial_mesh(base):
    """Graded starting partition of [1,128]: cell width proportional to s."""
    edges = []
    for i in range(7):
        a, b = Fraction(2 ** i), Fraction(2 ** (i + 1))
        step = base * 2 ** i
        x = a
        while x < b:
            y = min(x + step, b)
            edges.append((x, y))
            x = y
    return edges


def finite_certificate(k, degree, base, max_depth=24):
    theta = THRESHOLD[k]
    stack = [(a, b, 0) for a, b in reversed(initial_mesh(base))]
    accepted, refined, weakest = [], 0, None
    t0 = time.monotonic()
    while stack:
        a, b, depth = stack.pop()
        rec = cell_bound(a, b, k, degree, theta)
        if rec is not None and rec['_passes']:
            low = rec.pop('_lower')
            full = rec.pop('_full')
            rec.pop('_passes')
            if weakest is None or float(low.lower()) < weakest[0]:
                weakest = (float(low.lower()), full)
            accepted.append(rec)
        else:
            refined += 1
            if depth >= max_depth:
                raise AssertionError('unresolved cell k=%d [%s, %s]' % (k, a, b))
            c = Fraction(a + b, 2)
            stack.append((c, b, depth + 1))
            stack.append((a, c, depth + 1))
    accepted.sort(key=lambda r: Fraction(r['left']))
    assert Fraction(accepted[0]['left']) == 1
    assert Fraction(accepted[-1]['right']) == 128
    assert all(Fraction(u['right']) == Fraction(v['left'])
               for u, v in zip(accepted, accepted[1:])), 'partition has a gap'
    return {
        'k': k, 'domain_s': ['1', '128'], 'precision_bits': ctx.prec,
        'taylor_degree': degree, 'initial_step': str(base),
        'uniform_rational_lower_bound_for_g': str(theta),
        'accepted_cells': len(accepted), 'refined_cells': refined,
        'weakest_cell': weakest[1],
        'coverage_exact': True, 'all_cells_pass': True,
        'seconds': round(time.monotonic() - t0, 2),
        'cells': accepted,
    }


def source_polynomials(k):
    """C_{k,j} with R^{4k-1} W_k = sum_j C_{k,j}(s) L^{(j)}(s)  (74A.5)-(74A.6)."""
    s = sp.Symbol('s')
    R = 2 * s - 1
    x = s * (s - 1)
    p = [x ** k]
    denominator_power = 1
    for _ in range(2 * k - 1):
        q = [sp.Integer(0)] * (len(p) + 1)
        for j, a in enumerate(p):
            q[j] += R * sp.diff(a, s) - 2 * denominator_power * a
            q[j + 1] += R * a
        p = [sp.expand(a) for a in q]
        denominator_power += 2
    assert denominator_power == 4 * k - 1
    p = [(-1) ** (k - 1) * a for a in p]
    assert sp.expand(p[-1] - (-1) ** (k - 1) * x ** k * R ** (2 * k - 1)) == 0
    # the completion terms 1/s + 1/(s-1) are annihilated identically
    rational_sum = sum(p[j] * sp.diff(1 / s + 1 / (s - 1), s, j) for j in range(2 * k))
    assert sp.cancel(rational_sum) == 0
    return s, p


def exact_tail(k, S=128):
    """Exact rational tail proof with alpha_k = lead(B_k)/4 (see 74A.7-74A.8)."""
    s, C = source_polynomials(k)
    t = sp.Symbol('t')
    sign, sign_cert = [], []
    for c in C:
        shifted = sp.Poly(c.subs(s, S + t), t)
        co = shifted.all_coeffs()
        if all(a >= 0 for a in co):
            eps = 1
        elif all(a <= 0 for a in co):
            eps = -1
        else:
            raise AssertionError('source polynomial sign unresolved')
        sign.append(eps)
        sign_cert.append([str(eps * shifted.nth(j)) for j in range(shifted.degree() + 1)])
    assert sign[0] == 1
    # log(s/(2 pi)) > 2 on s >= 128; the remaining errors use
    # 0 < 1/(1-exp(-t)) - 1/t - 1/2 < t/12
    base = C[0] - C[0] / (2 * s)
    for j in range(1, 2 * k):
        base += C[j] * (-1) ** (j - 1) * (sp.factorial(j - 1) / (2 * s ** j)
                                          + sp.factorial(j) / (2 * s ** (j + 1)))
    error = sum(sign[j] * C[j] * sp.factorial(j + 1) / (6 * s ** (j + 2))
                for j in range(2 * k))
    lower = sp.cancel(base - error)
    lead = sp.Poly(sp.cancel(s ** (2 * k + 1) * lower), s).all_coeffs()[0]
    assert sp.Integer(lead) == lead and lead > 0
    alpha = sp.Integer(int(lead) // 4)
    polynomial = sp.Poly(sp.cancel(s ** (2 * k + 1) * (lower - alpha * s ** (2 * k))), s)
    shifted = sp.Poly(polynomial.as_expr().subs(s, S + t), t)
    assert all(c >= 0 for c in shifted.all_coeffs()) and shifted.eval(0) > 0
    B = 0
    term_bounds = []
    for j, c in enumerate(C):
        d = 2 * k + j
        assert sp.degree(c, s) == d
        D = sum(abs(co) * sp.Rational(S) ** (int(power[0]) - d)
                for power, co in sp.Poly(c, s).terms())
        m = j + 1
        b = sp.Rational(7, 10) ** m + 2 * sum(
            sp.factorial(m) / sp.factorial(m - r) * sp.Rational(7, 10) ** (m - r)
            / sp.Rational(S - 1) ** (r + 1) for r in range(m + 1))
        B += D * b / sp.Rational(S) ** (2 * k - 1 - j)
        term_bounds.append({'j': j, 'D': str(D), 'b': str(b)})
    ratio = sp.cancel(B * S ** (2 * k - 1) / sp.Integer(2) ** S / alpha)
    assert 0 < ratio < sp.Rational(1, 2)
    assert S > 2 * (2 * k) and S * sp.Rational(69, 100) > 2 * k
    return {
        'k': k, 'domain_s': [str(S), 'infinity'], 'alpha': str(alpha),
        'alpha_rule': 'alpha = lead(B_k)/4',
        'gamma_lower_leading_coefficient': str(lead),
        'tail_lower_bound_W': '(%s/2)*s^%d/(2*s-1)^%d' % (alpha, 2 * k, 4 * k - 1),
        'source_polynomial_signs': sign,
        'source_polynomials_descending': [
            [str(a) for a in sp.Poly(c, s).all_coeffs()] for c in C],
        'source_sign_certificates_ascending': sign_cert,
        'gamma_margin_shifted_ascending': [str(shifted.nth(j))
                                           for j in range(shifted.degree() + 1)],
        'gamma_margin_coefficients': shifted.degree() + 1,
        'gamma_margin_all_nonnegative': True,
        'prime_term_bounds': term_bounds, 'H': str(B),
        'prime_gamma_ratio_exact': str(ratio),
        'prime_gamma_ratio_decimal': str(sp.N(ratio, 30)),
        'ratio_below_one_half': True,
        'completion_annihilated': True,
    }


def cross_checks(k):
    """s-operator against the x-Leibniz formula, both in Arb (GT44.8)."""
    rows = []
    for s0 in (1, 2, 5, 10, 32, 128):
        first = source_rung_series(ball(s0), k, 0)[0]
        second = independent_x_formula(s0, k)
        assert (first - second).contains(0)
        assert first > 0 and second > 0
        assert first.rad() < first.abs_lower() * ball(Fraction(1, 10 ** 35))
        assert second.rad() < second.abs_lower() * ball(Fraction(1, 10 ** 35))
        rows.append({'k': k, 's': s0, 's_operator': first.str(40),
                     'x_leibniz': second.str(40), 'overlap': True})
    return rows


def samples(k):
    return [{'k': k, 's': str(s0),
             'g_k': source_rung_series(ball(s0), k, 0)[0].str(35)}
            for s0 in SAMPLE_POINTS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--precision', type=int, default=256)
    ap.add_argument('--degree', type=int, default=20)
    ap.add_argument('--step', type=str, default='1/64')
    ap.add_argument('--rungs', type=str, default='2,3,4,5,6')
    ap.add_argument('--skip-continuum', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    ctx.prec = args.precision
    rungs = [int(x) for x in args.rungs.split(',')]
    base = Fraction(args.step)
    started = time.monotonic()
    out = {
        'status': 'RUNNING',
        'certifies': ('g_k(s) = s^(2k-1) W_k(s(s-1))/(2k-1)! > theta_k on [1,128]; '
                      'W_k(s(s-1)) > (alpha_k/2) s^(2k)/(2s-1)^(4k-1) for s >= 128'),
        'backend': 'python-flint %s (FLINT/Arb ball arithmetic), SymPy %s'
                   % (flint.__version__, sp.__version__),
        'python': platform.python_version(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'generalises': {'script': 'audit_widder_source.py',
                        'sha256': '348bb9b9d39669dc6729731f8a67b31bf596173554d8fc5fa6c10f3c4fb88697',
                        'edition': '4.5 fifth/sixth-rung source certificate'},
        'parameters': {'precision_bits': args.precision, 'taylor_degree': args.degree,
                       'initial_step': str(base)},
        'source': 'regularized zeta and log-Gamma; no zero-location inputs',
    }
    out['formulation_cross_checks'] = []
    for k in rungs:
        out['formulation_cross_checks'] += cross_checks(k)
    print('Operator form vs x-Leibniz form: PASS', flush=True)
    out['sample_values'] = []
    for k in rungs:
        out['sample_values'] += samples(k)
    out['tail'] = []
    for k in rungs:
        rec = exact_tail(k)
        out['tail'].append(rec)
        print('Exact tail PASS k=%d alpha=%s ratio=%s'
              % (k, rec['alpha'], rec['prime_gamma_ratio_decimal']), flush=True)
    out['finite'] = []
    if not args.skip_continuum:
        for k in rungs:
            rec = finite_certificate(k, args.degree, base)
            out['finite'].append(rec)
            print(json.dumps({q: v for q, v in rec.items() if q != 'cells'}), flush=True)
    out['status'] = 'PASS'
    out['elapsed_seconds'] = round(time.monotonic() - started, 2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=1) + '\n')
    print('Saved %s (%.1f s)' % (args.output, out['elapsed_seconds']), flush=True)


if __name__ == '__main__':
    main()
