#!/usr/bin/env python3
"""Exact finite regressions for the newly integrated source-derived identities.

These checks do not certify analytic continuation, the PNT estimate, historical
zero/rung certificates, or an all-order positivity assertion. The manuscript
contains the arguments for the infinite statements. No network is used.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, factorial
import argparse, hashlib, json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
y,x,q=s.symbols('y x q')
T=lambda n:F(n*(n+1),2)
checks=[]
def ck(name,condition):
    ok=bool(condition)
    checks.append({'name':name,'passed':ok})
    if not ok: raise AssertionError(name)
def equal(a,b):return s.expand(a-b)==0
P=[s.Integer(1),3-y]
Q=[s.Integer(0),y]
B=[s.Integer(1),2-y]
for n in range(1,21):
    P.append(s.expand((2-y)*P[-1]-P[-2]))
    Q.append(s.expand((2-y)*Q[-1]-Q[-2]+2*y))
    B.append(s.expand((2-y)*B[-1]-B[-2]))
def d(m,j):return F((-1)**j*(2*m+1)*factorial(m+j),factorial(m-j)*factorial(2*j+1))
for m in range(11):
    cf=sum(s.Rational(d(m,j))*y**j for j in range(m+1))
    tri=sum((2*m+1)*(-2*y)**j*s.prod(s.Rational(T(m)-T(r)) for r in range(j))/factorial(2*j+1) for j in range(m+1))
    ck(f'155A coefficients m={m}',equal(P[m],cf))
    ck(f'155A triangular product m={m}',equal(P[m],tri))
    ck(f'155A odd square m={m}',equal(Q[2*m+1],y*P[m]**2))
    ck(f'155A even coefficients r={m}',equal(B[m],sum((-1)**j*comb(m+j+1,2*j+1)*y**j for j in range(m+1))))
for r in range(7):
    for j in range(7):
        ck(f'155A odd cross r={r},s={j}',equal(y*P[r]*P[j],Q[r+j+1]-Q[abs(r-j)]))
        ck(f'155A even cross r={r},s={j}',equal(y*(4-y)*B[r]*B[j],Q[r+j+2]-Q[abs(r-j)]))
# Congruence tested on a signed rational functional, without a positivity premise.
mu=[s.Rational((-1)**i*(i+3),i+7) for i in range(30)]
def L(poly):
    poly=s.Poly(s.expand(poly),y)
    return sum(co*mu[powers[0]] for powers,co in poly.terms())
lam=[s.Integer(0)]+[L(s.cancel(Q[n]/y)) for n in range(1,15)]
for n in range(1,7):
    H=s.Matrix(n,n,lambda i,j:mu[i+j])
    C=s.Matrix(n,n,lambda i,j:s.Rational(d(i,j)) if j<=i else 0)
    K=s.Matrix(n,n,lambda i,j:lam[i+j+1]-lam[abs(i-j)])
    ck(f'155A reflected congruence N={n}',C*H*C.T==K)
    ck(f'155A unimodularity N={n}',C.det()==(-1)**(n*(n-1)//2))
# Coalescing witness identity at rational complex q; ordinary square retained.
for m in range(7):
    for eps in (s.Rational(1,2),s.Rational(1,7)):
        for qv in (s.Rational(2),2+s.I):
            coeff=[(-1)**i/s.factorial(i)*sum(s.Rational(d(m,r))/(s.factorial(r-i)*eps**r) for r in range(i,m+1)) for i in range(m+1)]
            lhs=sum(coeff[i]/(qv+(i+1)*eps) for i in range(m+1))
            rhs=sum(s.Rational(d(m,r))/s.prod(qv+(j+1)*eps for j in range(r+1)) for r in range(m+1))
            ck(f'155A witness m={m},e={eps},q={qv}',s.simplify(lhs-rhs)==0)
# Finite source-split algebra. The PNT justification is a written proof, not this test.
g,h=s.symbols('gamma log4pi')
eta=s.symbols('eta0:14')
for n in range(1,13):
    odds=list(range(1,24,2))
    lj=1-s.Rational(n,2)*(g+h)+sum((-1)**j*comb(n,j)*sum(s.Rational(1,ell**j) for ell in odds) for j in range(2,n+1)) +n*g-sum(comb(n,j)*eta[j-1] for j in range(2,n+1))
    reserve=n*(1+g/2-h/2)+sum((1-s.Rational(1,ell))**n-1+s.Rational(n,ell) for ell in odds[1:])
    err=sum(comb(n,j)*eta[j-1] for j in range(2,n+1))
    ck(f'155B finite source-split algebra n={n}',equal(lj,reserve-err))
    ker=s.assoc_laguerre(n-1,2,x)-n
    series=sum(comb(n,j)*(-x)**(j-1)/factorial(j-1) for j in range(1,n+1))
    ck(f'155B Laguerre coefficient identity n={n}',equal(series,s.assoc_laguerre(n-1,1,x)))
    ck(f'155B integration-by-parts kernel n={n}',s.simplify(s.diff(s.exp(-x)*series,x)+s.exp(-x)*(ker+n))==0)
for n in range(16):
    kernel=lambda r:s.Integer(0) if r==0 else s.assoc_laguerre(r-1,2,x)-r
    ck(f'155B curvature kernel n={n}',equal(kernel(n+2)-2*kernel(n+1)+kernel(n),s.laguerre(n+1,x)))
    ck(f'155B triangular accumulated weights N={n+2}',sum(n+1-j for j in range(n+1))==(n+1)*(n+2)//2)
    for ell in (3,5,9):
        reserve=lambda r:(1-F(1,ell))**r-1+F(r,ell)
        ck(f'155B reserve curvature n={n},ell={ell}',reserve(n+2)-2*reserve(n+1)+reserve(n)==(1-F(1,ell))**n/F(ell**2))
# Positive descent: recurrence and the two elementary one-atom integrals.
for k in range(1,8):
    W=factorial(2*k-1)*q**k/(x+q)**(2*k)
    Wnext=factorial(2*k+1)*q**(k+1)/(x+q)**(2*k+2)
    ck(f'38A differential recurrence k={k}',s.simplify(s.diff(x**(2*k+1)*s.diff(W,x),x)+x**(2*k)*Wnext)==0)
    for xv in (F(1,2),F(3)):
        for qv in (F(2,3),F(5)):
            v=xv/(xv+qv)
            lower=F(factorial(2*k+1),2*k+1)*qv**k*v**(2*k+1)
            upper=F(factorial(2*k+1),2*k+1)*qv**(k+1)/(xv+qv)**(2*k+1)
            ck(f'38A descent one-atom k={k},x={xv},q={qv}',(lower/xv**(2*k)+upper)/(2*k)==factorial(2*k-1)*qv**k/(xv+qv)**(2*k))
# Quarter fold and the Gaussian telescope use distinct input coordinates.
ss,mm=s.symbols('s m')
ck('133A quarter fold',s.expand(4*(mm+ss/2)*(mm+(1-ss)/2)-2*mm*(2*mm+1)-ss*(1-ss))==0)
for n in range(1,31):
    ck(f'133A Gaussian adjacent scaling n={n}',2*(F(1,n)-F(1,n+1))==1/T(n))
    ck(f'133A finite telescope N={n}',sum(1/T(j) for j in range(1,n+1))==2*(1-F(1,n+1)))
# Degree-dependent sign cancellation in the R15 derivative basis.
for k in range(1,11):
    for j in range(k+1):
        coeff=(-1)**j*comb(k,j)*(-1)**(k+j-1)*F(factorial(2*k-1),factorial(k+j-1))
        ck(f'R15 derivative column sign k={k},j={j}',coeff==(-1)**(k-1)*comb(k,j)*F(factorial(2*k-1),factorial(k+j-1)))

ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'qa/INTEGRATED_BRIDGES.json');args=ap.parse_args()
result={'status':'PASS','exact_checks':len(checks),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact regressions; analytic and all-order assertions rest on the written proofs. No actual-zeta interval certificate or historical certificate replay.','checks':checks}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
