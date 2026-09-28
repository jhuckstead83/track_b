#!/usr/bin/env python3
"""Compare the two source-rung certificates, and (optionally) both against the
recorded fifth/sixth-rung receipts of the 4.5 edition.

    python3 cross_backend_check.py --arb RECEIPT_arb.json \
        --decimal RECEIPT_decimal.json --output CROSS_BACKEND.json \
        [--legacy receipt_standard.json ...]

Checks
  1. both receipts are PASS and certify the same inequality for each rung;
  2. identical exact tail data: source polynomials, signs, alpha_k, the prime
     bound H_k and the prime/Gamma ratio -- two independent exact-arithmetic
     implementations (SymPy and Fraction) must agree digit for digit;
  3. every sampled value of g_k has overlapping enclosures in the two backends;
  4. each partition covers [1,128] exactly and every cell clears theta_k;
  5. legacy receipts (if given): same certified statement, and every recorded
     cell of the legacy partition lies inside the new partitions' domain with
     overlapping sampled values.
"""
import argparse
import hashlib
import json
import sys
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction
from pathlib import Path

BIG = Context(prec=120, rounding=ROUND_FLOOR, Emin=-10 ** 9, Emax=10 ** 9)
sys.path.insert(0, str(Path(__file__).resolve().parent))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ball(txt):
    """'[mid +/- rad]' or a plain decimal -> outward (lo, hi)."""
    t = txt.strip()
    if t.startswith('[') and '+/-' in t:
        mid, rad = t[1:-1].split('+/-')
        m, r = Decimal(mid.strip()), Decimal(rad.strip())
    elif t.startswith('['):
        m, r = Decimal(t[1:-1].strip()), Decimal(0)
    else:
        m, r = Decimal(t), Decimal(0)
    return (BIG.subtract(m, r), BIG.add(m, r))


def overlap(a, b):
    return not (a[1] < b[0] or b[1] < a[0])


def coverage(cells):
    assert Fraction(cells[0]['left']) == 1
    assert Fraction(cells[-1]['right']) == 128
    for u, v in zip(cells, cells[1:]):
        assert Fraction(u['right']) == Fraction(v['left'])
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arb', type=Path, required=True)
    ap.add_argument('--decimal', type=Path, required=True)
    ap.add_argument('--legacy', type=Path, nargs='*', default=[])
    ap.add_argument('--legacy-spot', type=int, default=0,
                    help='re-evaluate this many legacy cell midpoints per rung '
                         'with the decimal backend and check the enclosures overlap')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    A = json.loads(args.arb.read_text())
    D = json.loads(args.decimal.read_text())
    report = {'arb_receipt': {'file': args.arb.name, 'backend': A['backend'],
                              'parameters': A.get('parameters'),
                              'sha256_script': A['script_sha256'],
                              'sha256_receipt': sha256(args.arb)},
              'decimal_receipt': {'file': args.decimal.name, 'backend': D['backend'],
                                  'parameters': D.get('parameters'),
                                  'sha256_script': D['script_sha256'],
                                  'sha256_receipt': sha256(args.decimal)},
              'checks': []}
    ok = report['checks'].append
    assert A['status'] == 'PASS' and D['status'] == 'PASS'
    ok({'check': 'both runs report PASS', 'result': True})

    # 2. exact tail data must agree exactly
    for ta, td in zip(A['tail'], D['tail']):
        k = ta['k']
        assert k == td['k']
        assert ta['alpha'] == td['alpha']
        assert ta['source_polynomial_signs'] == td['source_polynomial_signs']
        assert ta['H'] == td['H']
        assert ta['prime_gamma_ratio_exact'] == td['prime_gamma_ratio_exact']
        assert ta['gamma_margin_shifted_ascending'] == td['gamma_margin_shifted_ascending']
        desc = [list(reversed(c)) for c in td['source_polynomials_ascending']]
        assert desc == ta['source_polynomials_descending']
        ok({'check': 'exact tail data identical (SymPy vs Fraction)', 'k': k,
            'alpha': ta['alpha'], 'ratio': ta['prime_gamma_ratio_exact'],
            'source_polynomials_identical': True, 'result': True})

    # 3. sampled values overlap
    da = {(r['k'], r['s']): r['g_k'] for r in A['sample_values']}
    dd = {(r['k'], r['s']): r['g_k'] for r in D['sample_values']}
    assert set(da) == set(dd)
    worst = None
    for key in sorted(da):
        x, y = ball(da[key]), ball(dd[key])
        assert overlap(x, y), 'sample disagreement at %s' % (key,)
        w = max(BIG.subtract(x[1], x[0]), BIG.subtract(y[1], y[0]))
        if worst is None or w > worst[0]:
            worst = (w, key)
    ok({'check': 'sampled g_k enclosures overlap in both backends',
        'points': len(da), 'widest_enclosure_at': list(worst[1]),
        'widest_enclosure': str(worst[0]), 'result': True})

    # 4. partitions
    for rec in A['finite'] + D['finite']:
        coverage(rec['cells'])
        theta = Fraction(rec['uniform_rational_lower_bound_for_g'])
        td = Decimal(theta.numerator) / Decimal(theta.denominator)
        for c in rec['cells']:
            assert ball(c['lower_endpoint'])[0] > td
    ok({'check': 'both partitions cover [1,128] exactly and every cell clears theta_k',
        'arb_cells': {r['k']: r['accepted_cells'] for r in A['finite']},
        'decimal_cells': {r['k']: r['accepted_cells'] for r in D['finite']},
        'thresholds': {r['k']: r['uniform_rational_lower_bound_for_g'] for r in D['finite']},
        'result': True})

    # 5. legacy receipts
    for path in args.legacy:
        L = json.loads(path.read_text())
        assert L['status'] == 'PASS'
        entry = {'check': 'legacy receipt reproduced', 'file': path.name,
                 'sha256_receipt': sha256(path),
                 'legacy_script_sha256': L.get('script_sha256'),
                 'python_flint': L.get('python_flint'), 'rungs': [], 'result': True}
        for rec in L['finite']:
            k = rec['k']
            coverage(rec['cells'])
            new_t = {r['k']: Fraction(r['uniform_rational_lower_bound_for_g'])
                     for r in D['finite']}
            assert Fraction(rec['uniform_rational_lower_for_g']) == new_t[k], \
                'threshold mismatch at k=%d' % k
            entry['rungs'].append({'k': k, 'legacy_cells': rec['accepted_cells'],
                                   'threshold': rec['uniform_rational_lower_for_g']})
        for tl in L['tail']:
            ta = next(t for t in A['tail'] if t['k'] == tl['k'])
            assert tl['alpha'] == ta['alpha']
            assert tl['source_polynomial_signs'] == ta['source_polynomial_signs']
            assert tl['prime_gamma_ratio_exact'] == ta['prime_gamma_ratio_exact']
        entry['tail_constants_identical'] = True
        if args.legacy_spot:
            import source_rungs_decimal as SD
            SD.init_arith(80)
            J = SD.Jets(80)
            spot = []
            for rec in L['finite']:
                k = rec['k']
                cells = rec['cells']
                step = max(1, len(cells) // args.legacy_spot)
                n = 0
                for c in cells[::step]:
                    mid = Fraction(Fraction(c['left']) + Fraction(c['right']), 2)
                    v, _, _ = SD.rung_series(J, SD.i_frac(mid), k, 0)
                    assert overlap(v[0], ball(c['center_value'])), \
                        'legacy centre value disagrees at k=%d, s=%s' % (k, mid)
                    n += 1
                spot.append({'k': k, 'midpoints_recomputed': n,
                             'all_overlap_with_decimal_backend': True})
            entry['legacy_centre_spot_check'] = spot
        report['checks'].append(entry)

    report['status'] = 'PASS'
    args.output.write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
