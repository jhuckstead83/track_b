#!/usr/bin/env python3
"""Independent exact audit of common-source Beta recovery and row transport.

Standard library only. Decimal enclosures are obtained by integer floor/ceiling,
not floating-point rounding. The source example is the supplied polynomial
comparison model, NOT the Riemann zeta source. No analytic theorem or RH claim
is certified by these finite checks.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from math import comb, factorial, isqrt
from pathlib import Path


def beta(j: int) -> F:
    v = F(1)
    for r in range(j):
        v *= F(2*r+2, 2*r+3)
    return v


def add_poly(a: list[F], b: list[F], scale: F = F(1)) -> list[F]:
    out = [F(0)] * max(len(a), len(b))
    for j, v in enumerate(a): out[j] += v
    for j, v in enumerate(b): out[j] += scale*v
    return out


def p_poly(m: int) -> list[F]:
    """P_0=1, P_1=3-y, P_(m+1)=(2-y)P_m-P_(m-1)."""
    if m == 0: return [F(1)]
    p0, p1 = [F(1)], [F(3), F(-1)]
    for _ in range(1, m):
        p2 = add_poly([2*v for v in p1], [F(0)] + p1, F(-1))
        p2 = add_poly(p2, p0, F(-1))
        p0, p1 = p1, p2
    return p1


def square_coefficients(m: int) -> list[F]:
    p = p_poly(m)
    c = [F(0)]*(2*m+1)
    for i, x in enumerate(p):
        for j, y in enumerate(p): c[i+j] += x*y
    return c


def recovery_weights(rates: list[F]) -> list[F]:
    """Expand 1 - product(1-z/r) without determinant recurrences."""
    poly = [F(1)]
    for r in rates:
        poly = add_poly(poly, [F(0)] + [-v/r for v in poly])
    return [-v for v in poly[1:]]


def model_moments(count: int) -> list[F]:
    """q0=17/4 with multiplicity 2; q+=147/16+3i/2 and conjugate.

    Use an independent rational complex-pair multiplication, not the
    second-order reciprocal recurrence in the supplied audit.
    """
    qr, qi = F(147,16), F(3,2)
    den = qr*qr + qi*qi
    yr, yi = qr/den, -qi/den
    ar, ai = F(1), F(0)
    vals = []
    for j in range(count):
        ar, ai = ar*yr-ai*yi, ar*yi+ai*yr
        vals.append(2*F(4,17)**(j+1) + 2*ar)
    return vals


def interval(x: F, digits: int) -> tuple[F, F]:
    scale = 10**digits
    lo = (x.numerator*scale)//x.denominator
    hi = -((-x.numerator*scale)//x.denominator)
    return F(lo, scale), F(hi, scale)


def sqrt_interval(x: F, digits: int) -> tuple[F, F]:
    if x < 0: raise ValueError('negative radicand')
    scale = 10**digits
    n = isqrt((x.numerator*scale*scale)//x.denominator)
    lo = F(n, scale)
    return lo, lo if lo*lo == x else F(n+1, scale)


def decimal_text(x: F, digits: int) -> str:
    scaled = x*10**digits
    if scaled.denominator != 1: raise ValueError('not on decimal grid')
    n = scaled.numerator
    sign = '-' if n < 0 else ''
    raw = str(abs(n)).zfill(digits+1)
    return sign + raw[:-digits] + '.' + raw[-digits:]


def interval_json(pair: tuple[F, F], digits: int) -> dict:
    return {'lower_exact': str(pair[0]), 'upper_exact': str(pair[1]),
            'lower_decimal': decimal_text(pair[0], digits),
            'upper_decimal': decimal_text(pair[1], digits)}


def weighted_interval(weights: list[F], boxes: list[tuple[F,F]]) -> tuple[F,F]:
    lo = sum(w*(a if w >= 0 else b) for w,(a,b) in zip(weights,boxes))
    hi = sum(w*(b if w >= 0 else a) for w,(a,b) in zip(weights,boxes))
    return lo, hi


def row_from_jet(jet: list[F], a: F) -> list[F]:
    """jet[j]=f^(j)(a)/j!, B=[z^r] sum binom(N,j)a^j jet[j](1-z)^j."""
    n = len(jet)-1
    return [sum(F((-1)**r*comb(n,j)*comb(j,r))*a**j*jet[j]
                for j in range(r,n+1)) for r in range(n+1)]


def transport(c: list[F], n: int, a: F, depth: int) -> list[F]:
    return [sum(c[j]*beta(j)**depth*F(comb(r,j),comb(n,j))/a**j
                for j in range(min(r,len(c)-1)+1)) for r in range(n+1)]


def run() -> dict:
    checks = Counter()
    def check(group: str, value: bool) -> None:
        if not value: raise AssertionError(group)
        checks[group] += 1

    # Independent all-finite-index samples of the closed P_m formula.
    for m in range(31):
        p = p_poly(m)
        explicit = [F((-1)**j*(2*m+1)*factorial(m+j),
                       factorial(m-j)*factorial(2*j+1)) for j in range(m+1)]
        check('P_recurrence_vs_closed_form', p == explicit)
        c = square_coefficients(m)
        check('coefficient_signs', all((-1)**j*v > 0 for j,v in enumerate(c)))
        pneg = sum(v*F(-1,2)**j for j,v in enumerate(p))
        check('half_scale_closed_form', pneg == F(2**(m+1))-F(1,2**m))
        check('absolute_coefficient_sum', sum(abs(v)/2**j for j,v in enumerate(c)) == pneg*pneg)

    # Same-source error and exact source-row map, no imported audit functions.
    for m in range(9):
        c = square_coefficients(m)
        rates = [beta(j) for j in range(2*m+1)]
        w = recovery_weights(rates)
        for rate in rates:
            check('each_mode_recovered', sum(v*rate**k for k,v in enumerate(w,1)) == 1)
        errors = [F((-1)**j*(j+2), 7*j+11) for j in range(2*m+1)]
        output_errors = [sum(c[j]*errors[j]*beta(j)**k for j in range(2*m+1))
                         for k in range(1,2*m+2)]
        check('common_moment_error_collapse',
              sum(v*e for v,e in zip(w,output_errors)) == sum(v*e for v,e in zip(c,errors)))
        for n in (2*m, 2*m+3):
            for a in (F(2), F(3,2)):
                t0 = transport(c,n,a,0)
                ts = [transport(c,n,a,k) for k in range(1,2*m+2)]
                for r in range(n+1):
                    check('combined_transport_equals_unfiltered', sum(wk*tk[r] for wk,tk in zip(w,ts)) == t0[r])
                for sample in range(3):
                    jet = [F(((j+2)*(sample+3))%17-8,j+3) for j in range(n+1)]
                    row = row_from_jet(jet,a)
                    mu = [(-1)**j*jet[j] for j in range(2*m+1)]
                    for k,tk in enumerate([t0]+ts):
                        direct = sum(c[j]*mu[j]*beta(j)**k for j in range(2*m+1))
                        check('row_to_filtered_output', sum(x*y for x,y in zip(row,tk)) == direct)

    controls = []
    norms = []
    for m,digits in ((8,45),(18,70)):
        c = square_coefficients(m)
        mu = model_moments(2*m+1)
        w = recovery_weights([beta(j) for j in range(2*m+1)])
        values = [sum(c[j]*mu[j]*beta(j)**k for j in range(2*m+1))
                  for k in range(2*m+2)]
        boxes = [interval(v,digits) for v in values[1:]]
        check('model_all_output_intervals_positive', all(lo > 0 for lo,hi in boxes))
        exact = sum(wk*vk for wk,vk in zip(w,values[1:]))
        check('model_exact_reconstruction', exact == values[0])
        out = weighted_interval(w,boxes)
        check('model_interval_contains_exact', out[0] <= exact <= out[1])
        if m == 18:
            check('mandatory_negative_control', out[1] < 0)
        else:
            check('positive_model_lambda17', out[0] > 0)
        amp = sum(abs(v) for v in w)
        check('interval_width_budget', out[1]-out[0] <= amp/F(10**digits))
        outward = (interval(out[0],digits)[0],interval(out[1],digits)[1])
        controls.append({'Li_index':2*m+1, 'source':'polynomial comparison model, not zeta',
                         'decimal_places':digits, 'unfiltered_exact':str(exact),
                         'direct_value_interval':interval_json(interval(exact,digits),digits),
                         'reconstructed_interval':interval_json(outward,digits),
                         'inverse_amplifier_exact':str(amp),
                         'exact_interval_width':str(out[1]-out[0]),
                         'filtered_outputs':[{'depth':k,'value_exact':str(v),
                                               'interval':interval_json(box,digits)}
                                             for k,(v,box) in enumerate(zip(values[1:],boxes),1)]})
        t0=transport(c,2*m,F(2),0)
        nsq=sum(v*v for v in t0)
        root=sqrt_interval(nsq,25)
        check('transport_norm_root_enclosure', root[0]**2 <= nsq <= root[1]**2)
        norms.append({'m':m,'row_degree':2*m,'source_scale':'2',
                      'unfiltered_transport_squared_norm_exact':str(nsq),
                      'norm_interval':interval_json(root,25)})

    return {'status':'PASS','scope':'Exact finite algebra and rational directed enclosures for a polynomial model. No zeta-source interval or RH certificate.',
            'total_checks':sum(checks.values()),'checks':dict(checks),
            'model_controls':controls,'same_scale_transport_norms':norms,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','scope','total_checks','checks','script_sha256')},indent=2))
    for row in result['model_controls']:
        print('MODEL',row['Li_index'],'RECONSTRUCTED',row['reconstructed_interval']['lower_decimal'],row['reconstructed_interval']['upper_decimal'])
    for row in result['same_scale_transport_norms']:
        print('TRANSPORT_NORM',row['m'],row['norm_interval']['lower_decimal'],row['norm_interval']['upper_decimal'])
