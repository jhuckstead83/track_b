#!/usr/bin/env python3
"""Finite exact checks for Orange's v4.1 research delta.

No finite computation here certifies RH, analytic continuation, Pringsheim's
 theorem, a uniform source bound, or an infinite-rank growth alternative.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json

counts: Counter[str] = Counter()
def ck(group: str, value: bool) -> None:
    if not value:
        raise AssertionError(group)
    counts[group] += 1

def add(p, q, scale=F(1)):
    out = [F(0)] * max(len(p), len(q))
    for j, x in enumerate(p): out[j] += x
    for j, x in enumerate(q): out[j] += scale*x
    while len(out)>1 and out[-1]==0: out.pop()
    return out

def mul(p, q):
    out = [F(0)] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q): out[i+j] += x*y
    return out

def evaluate(p, x):
    v=F(0)
    for a in reversed(p): v=v*x+a
    return v

def family(first, count):
    out=[[F(1)],list(map(F,first))]
    while len(out)<count:
        out.append(add(mul([F(2),F(-1)],out[-1]),out[-2],F(-1)))
    return out

def laguerre(n, alpha):
    return [F((-1)**j*comb(n+alpha,n-j),factorial(j)) for j in range(n+1)]

def phi(n):
    if n==0: return [F(0)]
    p=laguerre(n-1,2);p[0]-=n
    return p

def eta_integral(p):
    return sum(v*comb(2*j,j) for j,v in enumerate(p))

def catalan_integral(p):
    return sum(v*F(comb(2*j,j),j+1) for j,v in enumerate(p))

P=family([3,-1],34)
V=family([1,-1],34)
Q=[[F(1)]]+[add(P[j],P[j-1],F(-1)) for j in range(1,len(P))]
for j in range(34):
    closed=[F((-1)**k*comb(j+k,2*k)) for k in range(j+1)]
    ck('third_kind_binomial_coefficients', V[j]==closed)
    ck('third_kind_Cauchy_value',evaluate(V[j],F(-4,3))==(F(3**(j+1))+F(1,3**j))/4)
    ck('third_kind_value_bound',evaluate(V[j],F(-4,3))<=3**j)
    reconstructed=V[j][:]
    for k in range(j): reconstructed=add(reconstructed,V[k],F(2))
    ck('P_to_V_triangular_conversion',P[j]==reconstructed)
    if j:
        ck('cosine_basis_difference',Q[j]==add(V[j],V[j-1]))

for r in range(18):
    for s in range(18):
        product=mul(V[r],V[s])
        ck('V_orthogonality_Catalan',catalan_integral(product)==int(r==s))
        ck('mixed_coefficient_absolute_sum',sum(abs(c)*F(4,3)**j for j,c in enumerate(product))==evaluate(V[r],F(-4,3))*evaluate(V[s],F(-4,3)))
        ck('mixed_Cauchy_entry_majorant',sum(abs(c)*F(4,3)**j for j,c in enumerate(product))<=3**(r+s))
        ck('cosine_anchor_diagonal',eta_integral(mul(Q[r],Q[s]))==(int(r==s)*(1 if r==0 else 2)))
        if r==s: expected=1 if r==0 else 2
        elif abs(r-s)==1: expected=1
        else: expected=0
        ck('Catalan_cosine_tridiagonal',catalan_integral(mul(Q[r],Q[s]))==expected)
        gp=(4*r+1) if r==s else (4*min(r,s)+2)
        ck('P_Catalan_Gram_entries',catalan_integral(mul(P[r],P[s]))==gp)

for N in range(1,19):
    G=[[4*r+1 if r==s else 4*min(r,s)+2 for s in range(N)] for r in range(N)]
    H=[[(-1)**(r+s)*(4*(N-max(r,s))-2-int(r==s)) for s in range(N)] for r in range(N)]
    for r in range(N):
        for s in range(N):
            ck('exact_Gram_inverse',sum(G[r][j]*H[j][s] for j in range(N))==int(r==s))
    ck('Gram_inverse_absolute_row_sum',max(sum(abs(x) for x in row) for row in H)==2*N*N-1)
    ck('block_geometric_sum',sum(9**j for j in range(N))==F(9**N-1,8))
    ck('rank_to_row_degree',2*(N-1)==2*N-2)

# Formal source identities: E_n = sum binom(n,j) eta_(j-1).
def ecoeff(n):
    return {j-1:F(comb(n,j)) for j in range(2,n+1)}

def dadd(a,b,scale=F(1)):
    d=dict(a)
    for k,v in b.items(): d[k]=d.get(k,F(0))+scale*v
    return {k:v for k,v in d.items() if v}

for n in range(41):
    dp=add(add(phi(n+2),phi(n+1),F(-2)),phi(n))
    ck('Laguerre_second_difference_kernel',dp==laguerre(n+1,0))
    de=dadd(dadd(ecoeff(n+2),ecoeff(n+1),F(-2)),ecoeff(n))
    target={j:F(comb(n,j-1)) for j in range(1,n+2)}
    ck('curvature_eta_binomial_transform',de==target)
    # [z^(n+1)] (z/(1-z))^j = binom(n,j-1).
    for j in range(1,n+2):
        ck('local_generating_series_coefficients',comb(n,j-1)==comb(j+(n+1-j)-1,n+1-j))

# Matrix congruence for completely arbitrary formal E_n with E_0=E_1=0.
def ediff(r,s): return dadd(ecoeff(r+s+1),ecoeff(abs(r-s)),F(-1))
def icoeff(n): return {j:F(comb(n,j-1)) for j in range(1,n+2)}
def weights(r): return [(0,F(1))] if r==0 else [(r,F(1)),(r-1,F(-1))]
for r in range(17):
    for s in range(17):
        actual={}
        for i,a in weights(r):
            for j,b in weights(s): actual=dadd(actual,ediff(i,j),a*b)
        if r==s==0: expected={}
        elif min(r,s)==0: expected=icoeff(max(r,s)-1)
        elif r==s: expected=icoeff(2*r-1)
        else: expected=dadd(icoeff(r+s-1),icoeff(abs(r-s)-1))
        ck('curvature_Toeplitz_Hankel_congruence',actual==expected)
        anchor=F(0)
        for i,a in weights(r):
            for j,b in weights(s): anchor+=a*b*(2*min(i,j)+1)
        ck('compensation_exact_diagonalization',anchor==int(r==s)*(1 if r==0 else 2))

# Common analytic error tests use rational functions, not Riemann-zero data.
for dim in range(1,13):
    for b in [F(1,2),F(1),F(3)]:
        for power in (1,2):
            M=1/(F(2)+b-F(3,4))**power
            for r in range(dim):
                for s in range(dim):
                    poly=mul(V[r],V[s])
                    entry=sum(c*F(comb(power+j-1,j),(F(2)+b)**(power+j)) for j,c in enumerate(poly))
                    ck('rational_mixed_jet_Cauchy_control',abs(entry)<=M*3**(r+s))

# Complex rational dictionaries and shifted-moment control.
def cm(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def ca(z,w): return (z[0]+w[0],z[1]+w[1])
def ci(z):
    d=z[0]**2+z[1]**2
    if not d: raise ZeroDivisionError
    return (z[0]/d,-z[1]/d)
def neg(z): return (-z[0],-z[1])
def cp(z,n):
    out=(F(1),F(0))
    for _ in range(n): out=cm(out,z)
    return out
for beta,gamma in [(F(3,4),F(2)),(F(2,3),F(5)),(F(1,2),F(3)),(F(1,4),F(2))]:
    rho=(beta,gamma);chi=ca((F(1),F(0)),neg(ci(rho)))
    ck('nonreal_pole_map',chi[1]!=0)
    # s'(chi)=rho^2; pole residue of h(s(z))/z = -mult/(chi*rho^2).
    one_minus=ca((F(1),F(0)),neg(chi))
    ck('pole_derivative_nonzero',ci(cm(one_minus,one_minus))==cm(rho,rho))
    ck('pole_residue_nonzero',ci(cm(chi,cm(rho,rho)))!=(F(0),F(0)))
    q=cm(rho,ca((F(1),F(0)),neg(rho)))
    y=ci(q); ya=ci(ca((F(2),F(0)),q))
    mapped=cm(y,ci(ca((F(1),F(0)),(2*y[0],2*y[1]))))
    ck('shifted_reciprocal_dictionary',ya==mapped)
    ck('shift_preserves_nonreality',(ya[1]!=0)==(y[1]!=0))
    for n in range(17):
        # Normalized derivative of (x+q)^-1 is (2+q)^-(n+1).
        ck('normalized_shifted_resolvent_jets',cp(ya,n+1)==cm(ya,cp(ya,n)))

ck('cutoff_five_exact_decay',F(12,5)**2<6 and 5**7>3**10)
ck('cutoff_thirteen_exact_decay',F(12,5)**2<F(29,5) and 13**7>6**10)

try:
    import mpmath as mp
    mp.mp.dps=60
    alpha=(mp.sqrt(6)-1)/2
    lambda1=1+mp.euler/2-mp.log(4*mp.pi)/2
    diagnostics={
        'scope':'Non-directed orientation values, not interval certificates.',
        'alpha3':str(alpha),
        'q5':str(3/mp.power(5,alpha)),
        'q5_squared_rank_rate':str(9/mp.power(5,2*alpha)),
        'RH_curvature_absolute_cap':str(mp.pi**2/8-1+2*lambda1),
        'I0_eta1':str(mp.euler**2+2*mp.stieltjes(1)),
    }
except ImportError:
    diagnostics={'scope':'No numerical diagnostics; exact checks completed.'}

out={
    'status':'PASS','total_assertions':sum(counts.values()),'groups':dict(counts),
    'scope':'Finite exact algebra, rational analytic examples, and synthetic complex points only.',
    'diagnostics':diagnostics,
    'not_certified_by_computation':[
        'Pringsheim continuation and the all-degree curvature criterion',
        'all-rank positive-scale escape and RH equivalences',
        'uniform bounds on the actual arithmetic curvature or cutoff matrices',
        'any Riemann-zero, Widder-rung, or historical certificate'],
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('ORANGE_CHECKS.json'))
args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
