#!/usr/bin/env python3
"""Independent finite audit of the Orange/Green comparison.

Uses symbolic polynomial identities and exact rational examples only.
No finite assertion certifies the infinite RH equivalences or a prime bound.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from pathlib import Path
import sympy as s

counts: Counter[str] = Counter()

def check(group: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(group)
    counts[group] += 1

y,x,z,r,m=s.symbols('y x z r m')

# Arbitrary finite source jets; no eta formula or arithmetic sign is assumed.
curv=[s.Symbol('i'+str(k)) for k in range(20)]
seq=[s.Integer(0),s.Integer(0)]
for k in range(20):
    seq.append(2*seq[-1]-seq[-2]+curv[k])
for n in range(2,22):
    check('arbitrary_curvature_telescope',s.expand(seq[n]-sum((n-1-k)*curv[k] for k in range(n-1)))==0)
    check('triangular_weight_sum',sum(n-1-k for k in range(n-1))==n*(n-1)//2)

# Endpoint test: adding an unremoved linear anchor changes the initial data.
anchor=s.Symbol('a')
for n in range(2,17):
    raw=seq[n]+n*anchor
    check('linear_anchor_is_not_in_curvature',s.expand(raw-n*anchor-sum((n-1-k)*curv[k] for k in range(n-1)))==0)
    check('missing_initial_slope_negative_control',s.expand(raw-sum((n-1-k)*curv[k] for k in range(n-1)))==n*anchor)

# Cosine congruence, including first row and the complete compensation.
delta=s.Symbol('delta')
G=[s.Symbol('g'+str(k)) for k in range(20)]
cstar=s.Symbol('cstar')
aseq=[s.Integer(0),cstar]
for k in range(20): aseq.append(2*aseq[-1]-aseq[-2]+G[k])
for d in range(1,9):
    B=s.eye(d)
    for j in range(1,d):
        B[j,j]=1/s.sqrt(2);B[j,j-1]=-1/s.sqrt(2)
    E=s.Matrix(d,d,lambda i,j:seq[i+j+1]-seq[abs(i-j)])
    H=s.Matrix(d,d,lambda i,j:2*min(i,j)+1)
    R=s.Matrix(d,d,lambda i,j:aseq[i+j+1]-aseq[abs(i-j)])
    CE=B*E*B.T;CH=B*H*B.T;CR=B*R*B.T
    J=lambda k:s.Integer(0) if k==0 else curv[k-1]
    A=lambda k:2*cstar if k==0 else G[k-1]
    for i in range(d):
        for j in range(d):
            if i==j==0: e=s.Integer(0); rr=cstar
            elif min(i,j)==0: e=J(max(i,j))/s.sqrt(2);rr=A(max(i,j))/s.sqrt(2)
            else:e=(J(i+j)+J(abs(i-j)))/2;rr=(A(i+j)+A(abs(i-j)))/2
            check('cosine_arithmetic_entries',s.expand(CE[i,j]-e)==0)
            check('cosine_reserve_entries',s.expand(CR[i,j]-rr)==0)
            check('compensation_identity_matrix',s.simplify(CH[i,j])==int(i==j))

# The tridiagonal cosine Gram has precisely the Chebyshev eigenvalues.
for d in range(1,10):
    J=s.zeros(d)
    for k in range(d-1):
        a=1/s.sqrt(2) if k==0 else s.Rational(1,2)
        J[k,k+1]=a;J[k+1,k]=a
    characteristic=J.charpoly(z).as_expr()
    check('cosine_Gram_characteristic_polynomial',s.expand(characteristic-s.chebyshevt(d,z)/2**(d-1))==0)

# One rational pole of a logarithmic derivative, composed by s=1/(1-z).
local=(-m/(1/(1-z)-r)+m/(1-r))/z
closed=m/((1-r)*(1-r+r*z))
check('rational_generating_function_identity',s.factor(local-closed)==0)
zr=1-1/r
res=s.limit((z-zr)*closed,z,zr)
check('genuine_pole_residue',s.factor(res+m/(zr*r*r))==0)

# Independently compare exact binomial coefficients to the rational pole series.
for rho in [s.Rational(3,4)+2*s.I,s.Rational(1,4)+2*s.I,s.Rational(2,3)+3*s.I]:
    u=s.simplify(1-rho)
    # Work in the rational complex field to prevent symbolic rounding.
    eta=[s.expand_complex(-(-1)**j/u**(j+1)).expand() for j in range(15)]
    for n in range(13):
        direct=sum(comb(n,j-1)*eta[j] for j in range(1,n+2))
        geometric=(-rho)**n/u**(n+2)
        check('curvature_coefficients_from_rational_poles',s.simplify(direct-geometric)==0)

# The previous Green constant is exact and never worse than Orange's bound.
for d in range(1,41):
    vals=[(Q(3**(j+1))+Q(1,3**j))/4 for j in range(d)]
    exact=sum(v*v for v in vals)
    previous=Q(9,128)*(9**d-Q(1,9**d))+Q(3*d,8)
    orange=Q(9**d-1,8)
    check('previous_exact_mixed_block_constant',exact==previous)
    check('Orange_coarse_constant_is_valid',previous<=orange)
    check('same_row_rank_schedule',2*(d-1)+1==2*d-1)
    check('same_simple_error_budget',orange<=Q(9,8)*3**(2*d-2))
check('constant_ratio_limit',Q(9,128)/Q(1,8)==Q(9,16))

# Shifted spectral values and derivative moments of a rational conjugate model.
q=s.Symbol('q')
check('shifted_reciprocal_map',s.factor((1/q)/(1+2/q)-1/(2+q))==0)
source=1/(x+2+s.I)+1/(x+2-s.I)
ys=[1/(4+s.I),1/(4-s.I)]
for k in range(12):
    jet=(-1)**k*s.diff(source,x,k).subs(x,2)/s.factorial(k)
    atom=sum(t**(k+1) for t in ys)
    check('shifted_resolvent_jet_identity',s.simplify(jet-atom)==0)
p=y-s.Rational(4,17)
negative=s.simplify(sum(t*p.subs(y,t)**2 for t in ys))
check('nonreal_shifted_negative_direction',negative==-s.Rational(8,4913))

# The whole-source cutoff error has the stated sign.
S=1/x+1/(x+6)-1/(x+3)
PX=1/(x+5);P=1/(x+3)
SX=1/x+1/(x+6)-PX
f=P-PX
check('completed_cutoff_error_sign',s.factor(S-SX+f)==0)
for k in range(12):
    dd=(-1)**k*s.diff(SX-S,x,k).subs(x,2)/s.factorial(k)
    ff=(-1)**k*s.diff(f,x,k).subs(x,2)/s.factorial(k)
    check('defect_error_sign_in_jets',s.simplify(dd-ff)==0)

# A limsup is not an arbitrary-cofinal individual-sample theorem.
# This is a rational generating-function countermodel, not actual zeta data.
coeff=lambda n:0 if n%2 else (-1)**(n//2)*4**n
for j in range(30):
    check('sparse_scalar_warning_model',coeff(2*j+1)==0)
    check('both_scalar_signs_in_warning_model',coeff(4*j)>0 and coeff(4*j+2)<0)

check('recovery_decay_exact',5**7>3**10 and s.Rational(12,5)**2<6)
check('whole_row_decay_exact',13**7>6**10 and s.Rational(12,5)**2<s.Rational(29,5))

result={'status':'PASS','total_assertions':sum(counts.values()),'groups':dict(counts),
 'exact_negative_control':{'model':'q=2+i,2-i; a=2; p(y)=y-4/17','K2_p':str(negative)},
 'scope':'Finite symbolic identities and rational synthetic models; no actual-prime bound or infinite-order theorem is numerically certified.',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
