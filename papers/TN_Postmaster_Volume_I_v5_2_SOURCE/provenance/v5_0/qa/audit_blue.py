#!/usr/bin/env python3
"""Finite checks for the Blue Team v4.1 proof-sharpening note.

These checks verify finite algebra and synthetic controls only. They do not
certify analytic continuation, infinite-rank limits, or an RH source bound.
Python standard library suffices; mpmath is optional for orientation decimals.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

counts: Counter[str] = Counter()

def check(group: str, statement: bool) -> None:
    if not statement:
        raise AssertionError(group)
    counts[group] += 1

def add(a, b, scale=F(1)):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=scale*x
    return c

def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def evaluate(p,x):
    z=F(0)
    for c in reversed(p): z=z*x+c
    return z

def polynomials(first, count):
    ps=[[F(1)],first]
    while len(ps)<count:
        ps.append(add(mul([F(2),F(-1)],ps[-1]),ps[-2],F(-1)))
    return ps

# Complex rational arithmetic: (real, imaginary).
def ca(z,w): return z[0]+w[0], z[1]+w[1]
def cn(z): return -z[0],-z[1]
def cm(z,w): return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]
def cs(z,a): return z[0]*a,z[1]*a
def ci(z):
    d=z[0]*z[0]+z[1]*z[1]
    if not d: raise ZeroDivisionError
    return z[0]/d,-z[1]/d

def sqabs(z): return z[0]*z[0]+z[1]*z[1]

P=polynomials([F(3),F(-1)],41)
for m,p in enumerate(P):
    c=mul(p,p)
    check('coefficient_alternation',all(((-1)**j)*v>0 for j,v in enumerate(c)))
    closed=(F(3**(m+1))-F(1,3**m))/2
    check('radius_three_quarters_closed_value',evaluate(p,F(-4,3))==closed)
    check('direct_Cauchy_coefficient_sum',sum(abs(v)*F(4,3)**j for j,v in enumerate(c))==closed**2)
    check('full_window_majorant',closed**2<=F(9,4)*9**m)
    # Elementary rational analytic example; Cauchy majorant has no numerical rounding.
    for b in (F(1,2), F(1), F(3)):
        for power in (1,2,3):
            target=sum(cj*comb(power+j-1,j)/(F(2)+b)**(power+j) for j,cj in enumerate(c))
            cauchy_bound=closed**2/(F(2)+b-F(3,4))**power
            check('rational_source_direct_bound',abs(target)<=cauchy_bound)

for n in range(257):
    for m in range(n//2+1):
        check('full_admissible_window',2*m<=n and 9**m<=3**n)
check('alpha3_greater_than_seven_tenths',F(12,5)**2<6)
check('cutoff_five_exact_decay',5**7>3**10)
check('alpha4_greater_than_seven_tenths',F(12,5)**2<F(29,5))
check('full_row_thirteen_exact_decay',13**7>6**10)

V=polynomials([F(1),F(-1)],18)
for i,p in enumerate(V):
    for j,q in enumerate(V):
        product=mul(p,q)
        integral=sum(c*F(comb(2*k,k),k+1) for k,c in enumerate(product))
        check('Catalan_third_kind_orthogonality',integral==int(i==j))
        eta_integral=sum(c*comb(2*k,k) for k,c in enumerate(product))
        check('anchor_Gram_and_trace_bound',eta_integral==(-1)**(i+j)*(2*min(i,j)+1))
for n in range(101):
    y=F(n,25)
    diff=1/(5*(1+6*y))-F(1,125)
    check('reserve_single_atom_lower_bound',diff==6*(4-y)/(125*(1+6*y)) and diff>=0)

# The mandatory finite synthetic spectrum, not Riemann zero data.
y0=F(4,17)
y=ci((F(147,16),F(3,2)))
t=ca((F(1),F(0)),cs(y,F(-1,2)))
F_at_y=ca(y,(-y0,F(0)))
Tprev=(F(1),F(0)); Tnow=t
for n in range(41):
    if n==0: Tn=Tprev
    elif n==1: Tn=Tnow
    else:
        Tnext=ca(cs(cm(t,Tnow),F(2)),cn(Tprev))
        Tprev,Tnow=Tnow,Tnext; Tn=Tnow
    c=cm(y,cm(cm(F_at_y,Tn),cm(F_at_y,Tn)))
    cy=cm(c,y); cy2=cm(cy,y)
    determinant=4*(c[0]*cy2[0]-cy[0]*cy[0])
    expected=-4*sqabs(c)*y[1]*y[1]
    check('isolated_pair_exact_indefiniteness',determinant==expected and determinant<0)

for beta,gamma in ((F(3,4),F(2)),(F(2,3),F(5)),(F(4,5),F(7,2)),(F(1,2),F(3))):
    rho=(beta,gamma)
    one_minus=ca((F(1),F(0)),cn(rho))
    q=cm(rho,one_minus)
    y=ci(q)
    chi=ca((F(1),F(0)),cn(ci(rho)))
    check('Li_Chebyshev_inverse_dictionary',ca(chi,ci(chi))==ca((F(2),F(0)),cn(y)))
    if beta==F(1,2): check('critical_line_unit_modulus',sqabs(chi)==1)
    else: check('off_line_radial_defect',sqabs(chi)!=1)

# Pole-cancellation and support arguments are in the written proof, not here.
try:
    import mpmath as mp
    mp.mp.dps=70
    alpha3=(mp.sqrt(6)-1)/2
    alpha4=(mp.sqrt(mp.mpf(29)/5)-1)/2
    alpha=(mp.sqrt(5)-1)/2
    orientation={
        'precision_digits':70,
        'scope':'Non-directed orientation decimals; not interval certificates.',
        'alpha3':str(alpha3),
        'full_window_20_base':str(3/mp.power(20,alpha3)),
        'full_window_5_base':str(3/mp.power(5,alpha3)),
        'full_window_20_constant':str(mp.mpf(9)/(4*mp.sqrt(6))*mp.power(20,-alpha3)*(mp.log(20)/alpha3+1/alpha3**2)),
        'alpha4':str(alpha4),
        'full_row_13_base':str(6/mp.power(13,alpha4)),
        'old_window_base':str(5/mp.power(20,alpha)*mp.power(4,mp.mpf(1)/8))
    }
except ImportError:
    orientation={'scope':'mpmath unavailable; exact checks remain sufficient.'}

record={
    'status':'PASS',
    'scope':'Finite exact identities and rational synthetic controls only.',
    'total_assertions':sum(counts.values()),
    'groups':dict(counts),
    'diagnostics':orientation,
    'written_proofs_not_certified_by_this_script':[
        'uniform complex-disk Euler-tail bound for every cutoff',
        'all-rank exact exponential reserve growth rate',
        'conditional linear absolute-norm growth',
        'any actual-source RH-forcing upper estimate'
    ],
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('SHARPENING_CHECKS.json'))
args=parser.parse_args()
args.output.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
