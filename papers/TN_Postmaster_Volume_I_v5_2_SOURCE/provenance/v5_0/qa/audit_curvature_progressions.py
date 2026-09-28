#!/usr/bin/env python3
"""Exact finite controls for the proposed arithmetic-progression curvature lemma.

Standard library only. Synthetic rational poles are not Riemann-zero data.
The infinite meromorphic-continuation and Pringsheim arguments are written
proofs in the accompanying reconciliation, not consequences of this audit.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

C = Counter()
Z = (F(0), F(0))
ONE = (F(1), F(0))

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    C[name] += 1

def add(z, w): return (z[0]+w[0], z[1]+w[1])
def neg(z): return (-z[0], -z[1])
def sub(z, w): return add(z, neg(w))
def mul(z, w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def scale(z, a): return (a*z[0], a*z[1])
def inv(z):
    d = z[0]**2+z[1]**2
    if not d: raise ZeroDivisionError
    return (z[0]/d, -z[1]/d)
def div(z, w): return mul(z, inv(w))
def power(z, n):
    if n < 0: return power(inv(z), -n)
    ans = ONE
    while n:
        if n & 1: ans = mul(ans, z)
        z = mul(z, z)
        n //= 2
    return ans
def norm2(z): return z[0]**2+z[1]**2
def csum(zs):
    result = Z
    for z in zs: result = add(result, z)
    return result
def pmul(p, q):
    out = [Z] * (len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): out[i+j] = add(out[i+j], mul(a, b))
    return out
def peval(p, z):
    out = Z
    for a in reversed(p): out = add(mul(out, z), a)
    return out
def rational_pair(poles, residues):
    den = [ONE]
    for z in poles: den = pmul(den, [neg(z), ONE])
    num = [Z] * len(poles)
    for i, a in enumerate(residues):
        term = [a]
        for j, z in enumerate(poles):
            if j != i: term = pmul(term, [neg(z), ONE])
        for k, b in enumerate(term): num[k] = add(num[k], b)
    return num, den
def series_from_quotient(num, den, count):
    out = []
    for n in range(count):
        rhs = num[n] if n < len(num) else Z
        rhs = sub(rhs, csum(mul(den[j], out[n-j]) for j in range(1, min(n, len(den)-1)+1)))
        out.append(div(rhs, den[0]))
    return out

# Exact determinant recovery from the original blinded-output question.
d1, d2 = F(8,225), F(448,10125)
check('signed_weighted_recovery', F(33,8)*d1-F(135,32)*d2 == -F(1,25))
check('magnitudes_not_monotone', F(1,25)>d1 and d2>F(1,25))
check('independent_error_amplification', F(33,8)+F(135,32)==F(267,32))

for beta, gamma in [(F(3,4),F(2)), (F(2,3),F(5)), (F(4,5),F(7,2))]:
    rhos = [(beta,gamma),(beta,-gamma),(1-beta,gamma),(1-beta,-gamma)]
    poles = [sub(ONE, inv(rho)) for rho in rhos]
    residues = [neg(inv(mul(z, power(rho,2)))) for z,rho in zip(poles,rhos)]
    for rho,z in zip(rhos,poles):
        b,g = rho
        check('inside_disk_iff_right_half_strip', (norm2(z)<1)==(b>F(1,2)))
        check('pole_phase_formula', z[1]/z[0] == g/(g*g-b*(1-b)))
        check('phase_tangent_upper_bound', abs(z[1]/z[0]) <= abs(g)/(g*g-F(1,4)))
        check('nonzero_phase', z[1]!=0 and z[0]>0)
    num,den = rational_pair(poles,residues)
    check('real_rational_model', all(z[1]==0 for z in num+den))
    original = series_from_quotient(num,den,75)
    for z,a in zip(poles,residues):
        deriv = [(F(j)*den[j][0],F(j)*den[j][1]) for j in range(1,len(den))]
        check('original_residue_from_polynomial_quotient', div(peval(num,z),peval(deriv,z))==a)
    for h in (1,2,3):
        mapped = [power(z,h) for z in poles]
        check('no_pole_alias_in_synthetic_sector', len(set(mapped))==len(mapped))
        check('no_positive_real_image', all(z[1]!=0 for z in mapped))
        for a in range(h):
            amps = [mul(A,power(z,h-1-a)) for z,A in zip(poles,residues)]
            nn,dd = rational_pair(mapped,amps)
            sampled = series_from_quotient(nn,dd,25)
            for m,b in enumerate(sampled):
                check('decimated_coefficients_from_independent_recurrences', b==original[h*m+a])
            deriv = [scale(dd[j],F(j)) for j in range(1,len(dd))]
            for rho,z,w,A in zip(rhos,poles,mapped,amps):
                check('decimated_residue_nonzero', A!=Z)
                check('decimated_residue_from_quotient', div(peval(nn,w),peval(deriv,w))==A)
                check('zeta_dictionary_residue_formula', A==neg(div(power(z,h-2-a),power(rho,2))))
            if h==2:
                for t in (F(1,7),F(2,9),F(-1,5)):
                    tt=(t,F(0)); w=power(tt,2)
                    even=scale(add(div(peval(num,tt),peval(den,tt)),div(peval(num,neg(tt)),peval(den,neg(tt)))),F(1,2))
                    odd=div(sub(div(peval(num,tt),peval(den,tt)),div(peval(num,neg(tt)),peval(den,neg(tt)))),scale(tt,F(2)))
                    check('even_odd_filter_rational_identity', div(peval(nn,w),peval(dd,w))==(even if a==0 else odd))

# Root-of-unity aliasing warning: 1/(1+16*z*z).
bad_poles=[(F(0),F(1,4)),(F(0),F(-1,4))]
bad_residues=[inv(scale(z,F(32))) for z in bad_poles]
check('warning_poles_collide_under_square', power(bad_poles[0],2)==power(bad_poles[1],2))
check('warning_odd_residues_cancel', csum(bad_residues)==Z)
check('warning_even_residue_survives', csum(mul(z,a) for z,a in zip(bad_poles,bad_residues))==(F(1,16),F(0)))
bad = series_from_quotient([ONE],[ONE,Z,(F(16),F(0))],60)
for m in range(30):
    check('warning_odd_subsequence_zero', bad[2*m+1]==Z)
    check('warning_even_subsequence_alternates', bad[2*m]==(F((-16)**m),F(0)))

# Parity expressions in terms of H(1/(1+-t)), with arbitrary rational H.
def H(s): return add((F(2),F(0)),div(ONE,add(s,(F(3),F(0)))))
h1=H(ONE)
def I(z): return div(sub(H(inv(sub(ONE,z))),h1),z)
for t in (F(1,7),F(2,9),F(-1,5)):
    z=(t,F(0)); sm=inv(add(ONE,z)); sp=inv(sub(ONE,z))
    ev=div(sub(H(sp),H(sm)),scale(z,F(2)))
    od=div(sub(add(H(sp),H(sm)),scale(h1,F(2))),scale(power(z,2),F(2)))
    check('H_regular_part_even_identity',ev==scale(add(I(z),I(neg(z))),F(1,2)))
    check('H_regular_part_odd_identity',od==div(sub(I(z),I(neg(z))),scale(z,F(2))))

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
result={'status':'PASS','total_assertions':sum(C.values()),'groups':dict(C),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Exact finite rational identities and synthetic pole models; no actual-zeta computation.',
        'not_certified':['Infinite progression RH equivalences or meromorphic continuation',
                         'A one-sided source bound for any parity',
                         'New Riemann-zero, Li, Widder, or publication certification']}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
