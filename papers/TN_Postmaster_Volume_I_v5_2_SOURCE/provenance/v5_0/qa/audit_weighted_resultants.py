#!/usr/bin/env python3
"""Exact, standard-library audit for the 2026-09-12 Green Team delta.

This checks finite algebra and counterexamples. It does not certify zeta zeros,
the all-order prime bound, or the analytic continuation theorem in the note.
Run: python3 audit_weighted_resultants.py --output audit_results.json
"""
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path


def beta(j):
    return F(4**j * math.factorial(j)**2, math.factorial(2*j + 1))


def triangular(j):
    return F(j*(j+1), 2)


def determinant(matrix):
    a = [list(map(F, row)) for row in matrix]
    ans = F(1)
    for i in range(len(a)):
        p = next((p for p in range(i, len(a)) if a[p][i]), None)
        if p is None:
            return F(0)
        if p != i:
            a[p], a[i] = a[i], a[p]
            ans = -ans
        pivot = a[i][i]
        ans *= pivot
        for r in range(i+1, len(a)):
            factor = a[r][i]/pivot
            for c in range(i+1, len(a)):
                a[r][c] -= factor*a[i][c]
    return ans


def hankel(mu, size, depth):
    return [[mu[i+j]*beta(i+j)**depth for j in range(size)]
            for i in range(size)]


def histograms(size):
    counts = Counter()
    for p in itertools.permutations(range(size)):
        inv = sum(p[i] > p[j] for i in range(size) for j in range(i+1, size))
        h = [0]*(2*size-1)
        for i, pi in enumerate(p):
            h[i+pi] += 1
        counts[tuple(h)] += (-1)**inv
    return {h:c for h,c in counts.items() if c}


def rate(hist):
    return math.prod(beta(j)**v for j,v in enumerate(hist))


def elementary(rates):
    e = [F(1)] + [F(0)]*len(rates)
    for n,r in enumerate(rates, 1):
        for j in range(n, 0, -1):
            e[j] += r*e[j-1]
    return e


def amplitudes(mu, hist):
    a = defaultdict(F)
    for h, c in hist.items():
        a[rate(h)] += c*math.prod(mu[j]**v for j,v in enumerate(h))
    return a


def exact_string(x):
    return str(x.numerator) if x.denominator == 1 else str(x)


def odd_square_coefficients(m):
    d = [F((-1)**j*(2*m+1)*math.factorial(m+j),
           math.factorial(m-j)*math.factorial(2*j+1)) for j in range(m+1)]
    c = [F(0)]*(2*m+1)
    for i,a in enumerate(d):
        for j,b in enumerate(d):
            c[i+j] += a*b
    return c


def run():
    checks = Counter()
    def check(group, statement):
        if not statement:
            raise AssertionError(group)
        checks[group] += 1

    mu = list(map(F, [1, F(4,5), F(3,5)]))
    d = [determinant(hankel(mu, 2, k)) for k in range(7)]
    check('example', d[:3] == [F(-1,25), F(8,225), F(448,10125)])
    check('example', abs(d[1]) < abs(d[0]) < abs(d[2]))
    check('example', F(33,8)*d[1]-F(135,32)*d[2] == d[0])
    check('example', F(33,8)+F(135,32) == F(267,32))
    check('single_output_ambiguity', determinant(hankel([F(1),F(0),F(1,15)],2,1)) == d[1])
    check('single_output_ambiguity', determinant(hankel([F(1),F(0),F(1,15)],2,0)) > 0)
    for k in range(5):
        check('two_mode_recurrence', d[k+2] == F(44,45)*d[k+1]-F(32,135)*d[k])
    for m0,m1,m2 in itertools.product([F(-2,3),F(0),F(1,4),F(3,2)], repeat=3):
        ds = [determinant(hankel([m0,m1,m2],2,k)) for k in range(3)]
        check('blind_recovery', ds[0] == F(33,8)*ds[1]-F(135,32)*ds[2])
    for j in range(101):
        ratio = beta(j+1)**2/(beta(j)*beta(j+2))
        check('triangular_curvature', ratio == 1-1/triangular(2*j+3))
        check('strict_log_convexity', F(0) < ratio < F(1))
    for i in range(51):
        check('adjacent_diagonal_damping', beta(2*i+1)**2/(beta(2*i)*beta(2*i+2)) == 1-1/triangular(4*i+3))
    for n in range(1,31):
        check('curvature_product_telescope', math.prod(1-1/triangular(2*j+3) for j in range(n)) == F(2*n+3,3*(n+1)))
        product = math.prod(1-1/triangular(4*i+3) for i in range(n))
        pochhammer = math.prod(F(2*i+1,2)*F(4*i+5,4)/(F(4*i+3,4)*F(i+1)) for i in range(n))
        check('quarter_gamma_finite_product', product == pochhammer)

    counts = []
    inversion = {}
    for n in range(1,10):
        hist = histograms(n)
        for h in hist:
            check('histogram_degree', sum(h) == n and sum(j*v for j,v in enumerate(h)) == n*(n-1))
        rates = sorted({rate(h) for h in hist})
        raw_log_product = sum(math.log10(1+1/float(r)) for r in rates)
        max_rate = max(rates)
        normalized_log_product = sum(math.log10(1+float(max_rate/r)) for r in rates)
        def log10_minus_one(log_product):
            return log_product + math.log10(1-10**(-log_product))
        counts.append({'rank':n, 'permutations':math.factorial(n),
                       'nonzero_histograms':len(hist), 'distinct_rates':len(rates),
                       'log10_raw_inverse_error_amplifier_approx':log10_minus_one(raw_log_product),
                       'log10_max_rate_normalized_inverse_error_amplifier_approx':log10_minus_one(normalized_log_product)})
        if n <= 5:
            for sample in range(3):
                moments = [F((j+1)*(sample+2)%11-4, j+2) for j in range(2*n-1)]
                amps = amplitudes(moments,hist)
                for k in range(5):
                    check('determinant_mode_expansion', determinant(hankel(moments,n,k)) == sum(c*r**k for r,c in amps.items()))
        if n <= 4:
            e = elementary(rates)
            size = len(rates)
            weights = [(-1)**(j+1)*e[size-j]/e[size] for j in range(1,size+1)]
            moments = [F((j+1)*5%13-6,j+2) for j in range(2*n-1)]
            values = [determinant(hankel(moments,n,k)) for k in range(size+1)]
            check('general_blind_inverse', values[0] == sum(w*v for w,v in zip(weights,values[1:])))
            check('general_characteristic_recurrence', sum((-1)**j*e[j]*values[size-j] for j in range(size+1)) == 0)
            amp = sum(abs(w) for w in weights)
            check('inverse_condition_identity', amp == math.prod(1+1/r for r in rates)-1)
            inversion[str(n)] = {'modes':size,'weights':[exact_string(w) for w in weights],
                                  'absolute_error_amplifier':exact_string(amp),
                                  'log10_absolute_error_amplifier':math.log10(amp.numerator)-math.log10(amp.denominator)}

    # An indefinite Hankel block with every diagonal entry positive.
    # Exact leading-principal determinants certify the claimed finite PD cases.
    indefinite = [F(1),F(4,5),F(3,5),F(1,2),F(2,5)]
    depth_rows = []
    for k in range(12):
        minors = [determinant(hankel(indefinite,n,k)) for n in range(1,4)]
        depth_rows.append({'depth':k,'leading_minors':[exact_string(v) for v in minors],
                           'positive_definite':all(v>0 for v in minors)})
    check('finite_rank_masking', depth_rows[0]['positive_definite'] is False)
    check('finite_rank_masking', depth_rows[-1]['positive_definite'] is True)

    # The supplied polynomial model, not the zeta source: one positive real
    # folded node (multiplicity two) and a conjugate nonreal pair.
    power = [F(2),F(1568,7395)]
    for j in range(2,41):
        power.append(F(1568,7395)*power[-1]-F(256,22185)*power[-2])
    model_mu = [2*F(4,17)**(j+1)+power[j+1] for j in range(40)]
    check('polynomial_model', all(v>0 for v in model_mu))
    check('polynomial_model', determinant(hankel(model_mu,3,0)) == F(-5525080289312768,2933603532835112189840625))
    negative_witnesses = []
    for k in range(5):
        for n in range(1,13):
            val = determinant(hankel(model_mu,n,k))
            if val < 0:
                negative_witnesses.append({'depth':k,'first_negative_leading_rank_within_search':n,
                                           'determinant':exact_string(val)})
                check('fixed_depth_negative_witness', val < 0)
                break
        else:
            negative_witnesses.append({'depth':k,'first_negative_leading_rank_within_search':None})

    li_audit = []
    for m in list(range(9))+[18]:
        c = odd_square_coefficients(m)
        rates = [beta(j) for j in range(2*m+1)]
        e = elementary(rates)
        size = len(rates)
        weights = [(-1)**(j+1)*e[size-j]/e[size] for j in range(1,size+1)]
        values = [sum(a*model_mu[j]*beta(j)**k for j,a in enumerate(c)) for k in range(size+1)]
        check('odd_Li_blind_inverse', values[0] == sum(w*v for w,v in zip(weights,values[1:])))
        check('odd_square_alternation', all((-1)**j*a>0 for j,a in enumerate(c)))
        amp = sum(abs(w) for w in weights)
        check('odd_Li_condition_identity', amp == math.prod(1+1/r for r in rates)-1)
        if m == 1:
            check('lambda3_weights', weights == [F(35,8),F(-99,16),F(45,16)])
        if m == 18:
            check('negative_model_lambda37', values[0] < 0)
            check('positive_outputs_hide_negative_model_lambda37', all(v>0 for v in values[1:]))
        li_audit.append({'m':m,'Li_index':2*m+1,'matrix_rank':m+1,'scalar_modes':size,
                         'blind_weights':[exact_string(w) for w in weights],
                         'absolute_error_amplifier':exact_string(amp),
                         'log10_absolute_error_amplifier_approx':math.log10(amp.numerator)-math.log10(amp.denominator),
                         'unfiltered_value_exact':exact_string(values[0]),
                         'unfiltered_value_approx':float(values[0]),
                         'filtered_depths_tested':[1,size],
                         'all_tested_positive_depth_values_positive':all(v>0 for v in values[1:]),
                         'first_filtered_value_approx':float(values[1])})

    # Direct coefficient verification of the B_k differential equation.
    for k in range(1,7):
        for j in range(1,41):
            check('hypergeometric_ode_coefficients',
                  j*F(2*j+1,2)**k*beta(j)**k == j**(k+1)*beta(j-1)**k)

    # A rank-3 modal formula, independently enumerated.
    expected3 = {F(1024,4725), F(256,1575), F(256,1225), F(512,2835), F(512,3375)}
    check('rank3_rates', set(rate(h) for h in histograms(3)) == expected3)
    return {
        'status':'PASS', 'arithmetic':'fractions.Fraction; exact integer/rational comparisons',
        'scope':'Finite algebra only. Analytic theorems require their written proofs; no RH or source-cap certification.',
        'checks':dict(checks), 'total_checks':sum(checks.values()),
        'example':[{'depth':k,'determinant':exact_string(v),'approximation':float(v)} for k,v in enumerate(d)],
        'rank_mode_counts':counts, 'blind_inverse':inversion,
        'masking_rank3_example':{'moments':[exact_string(v) for v in indefinite],'depths':depth_rows},
        'polynomial_model_fixed_depth_witnesses':negative_witnesses,
        'odd_Li_blind_recovery':li_audit,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','total_checks','checks','example','rank_mode_counts']},indent=2))
