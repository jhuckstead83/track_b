#!/usr/bin/env python3
"""Exact finite regressions and separately labelled numerical diagnostics.
Run: python audit_sine_bridge.py --output audit_results.json
Requires sympy and mpmath. No zeta-zero data or external services are used.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path
import sympy as sp
import mpmath as mp


def run() -> dict:
    counts: Counter = Counter()
    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        counts[name] += 1
    y,z,v,x=sp.symbols('y z v x')
    P=[sp.Integer(1),3-y]
    for m in range(1,18):
        P.append(sp.expand((2-y)*P[-1]-P[-2]))
    Q=[sp.Integer(0),y]
    for n in range(1,37):
        Q.append(sp.expand((2-y)*Q[-1]-Q[-2]+2*y))
    for m in range(19):
        poly=sp.Poly(P[m],y)
        for j in range(m+1):
            c=(-1)**j*sp.Rational((2*m+1)*factorial(m+j),factorial(m-j)*factorial(2*j+1))
            check('coefficient_formula',poly.nth(j)==c)
            tj=sp.prod(F(m*(m+1)-r*(r+1),2) for r in range(j))
            check('triangular_coefficient',c==(2*m+1)*(-2)**j*tj/sp.factorial(2*j+1))
        check('odd_square',sp.expand(y*P[m]**2-Q[2*m+1])==0)
        check('triangular_ode',sp.expand(y*(4-y)*sp.diff(P[m],y,2)+(6-2*y)*sp.diff(P[m],y)+m*(m+1)*P[m])==0)
        n=2*m+1
        frequencies=Counter(a+b for a in range(-m,m+1) for b in range(-m,m+1))
        for h in range(-n+1,n):
            check('fejer_frequency_counts',frequencies[h]==n-abs(h))
        check('positive_lag_triangle',sum(frequencies[h] for h in range(1,n))==n*(n-1)//2)
        if m:
            check('triangular_small_y_coefficient',poly.nth(1)/n==-F(m*(m+1),6))
    for r in range(10):
        for s in range(10):
            check('sum_difference_cross_identity',sp.expand(y*P[r]*P[s]-Q[r+s+1]+Q[abs(r-s)])==0)
    for n in range(1,11):
        kernel=sum(P[m]*P[m].subs(y,z) for m in range(n))
        rhs=P[n]*P[n-1].subs(y,z)-P[n-1]*P[n].subs(y,z)
        check('christoffel_darboux',sp.expand((z-y)*kernel-rhs)==0)
    for n in range(1,65):
        cos_sum=sum(v**(2*m+1)+v**(-2*m-1) for m in range(n))
        check('finite_half_integer_cosine_sum',sp.expand((v-1/v)*cos_sum-v**(2*n)+v**(-2*n))==0)
    for r in range(1,11):
        pf=sum((-1)**(r-j)*comb(2*r-j-1,r-1)*(x**(-j)+(-1)**j*(x+1)**(-j)) for j in range(1,r+1))
        check('reciprocal_triangular_partial_fractions',sp.cancel(pf-1/(x**r*(x+1)**r))==0)
    for k in range(1,17):
        a=2*k*(2*k-1)
        check('self_node_coordinate',1+4*a==(4*k-1)**2)
    product=sp.cos(sp.pi*sp.sqrt(1-4*x)/2)/(sp.pi*x)
    check('triangular_product_zero_value',sp.limit(product,x,0)==1)
    check('triangular_product_first_derivative',sp.limit((product-1)/x,x,0)==1)
    # Exact rational complex-pair multiplication, independent of polynomial library.
    a,b=F(147,16),F(3,2)
    den=a*a+b*b
    yr,yi=a/den,-b/den
    cr,ci=F(1),F(0)
    moments=[]
    for j in range(37):
        cr,ci=cr*yr-ci*yi,cr*yi+ci*yr
        moments.append(2*F(4,17)**(j+1)+2*cr)
        check('negative_control_positive_moment',moments[-1]>0)
    coeff=[F(sp.Poly(sp.expand(P[18]**2),y).nth(j)) for j in range(37)]
    lam=sum(c*a for c,a in zip(coeff,moments))
    check('negative_control_li37',F(-598,1000)<lam<F(-597,1000))
    beta=[F(4**j*factorial(j)**2,factorial(2*j+1)) for j in range(37)]
    filtered=[]
    for k in range(1,38):
        t=sum(coeff[j]*beta[j]**k*moments[j] for j in range(37))
        filtered.append(t)
        check('negative_control_positive_filtered_output',t>0)
    mp.mp.dps=70
    def fmt(t): return mp.nstr(t,24)
    def sinc(t): return mp.mpf(1) if t==0 else mp.sin(mp.pi*t)/(mp.pi*t)
    def dirichlet_ratio(n,t):
        return mp.mpf(2*n) if t==0 else mp.sin(n*t)/mp.sin(t/2)
    def projection(n,t,p):
        return (dirichlet_ratio(n,t-p)-dirichlet_ratio(n,t+p))/(2*mp.pi)
    grid=[mp.mpf(t) for t in ('-1','-.25','0','.4','1')]
    diagnostics={}
    diagnostics['finite_projection_direct_sum']=[]
    for n in (1,2,7,18):
        t,p=mp.mpf('0.37'),mp.mpf('1.21')
        direct=2/mp.pi*sum(mp.sin((m+mp.mpf('.5'))*t)*mp.sin((m+mp.mpf('.5'))*p) for m in range(n))
        diagnostics['finite_projection_direct_sum'].append({'N':n,'absolute_residual':fmt(abs(direct-projection(n,t,p)))})
    diagnostics['scalar_sinc_limit']=[]
    for m in (10,50,250):
        n=2*m+1
        err=max(abs((mp.mpf(1) if t==0 else mp.sin(mp.pi*t)/(n*mp.sin(mp.pi*t/n)))-sinc(t)) for t in grid)
        diagnostics['scalar_sinc_limit'].append({'m':m,'max_absolute_error':fmt(err)})
    diagnostics['bulk_projection_limit']=[]
    for n in (32,128,512):
        th=mp.pi/3
        err=max(abs(mp.pi/n*projection(n,th+mp.pi*u/n,th+mp.pi*w/n)-sinc(u-w)) for u in grid for w in grid)
        diagnostics['bulk_projection_limit'].append({'N':n,'max_absolute_error':fmt(err)})
    diagnostics['moving_height_limit']=[]
    for t in (100,1000,10000):
        t=mp.mpf(t); lg=mp.log(t/(2*mp.pi))
        n=int(mp.floor((t*t+mp.mpf('.25'))*lg/2))
        theta=lambda u: 2*mp.atan(1/(2*(t+2*mp.pi*u/lg)))
        err=max(abs(mp.pi/n*projection(n,theta(u),theta(w))-sinc(u-w)) for u in grid for w in grid)
        diagnostics['moving_height_limit'].append({'T':int(t),'N':n,'max_absolute_error':fmt(err),'error_times_T_log':fmt(err*t*lg)})
    diagnostics['boundary_projection_limit']=[]
    for n in (32,128,512):
        u,w=mp.mpf('.3'),mp.mpf('.8')
        low=mp.pi/n*projection(n,mp.pi*u/n,mp.pi*w/n)
        high=mp.pi/n*projection(n,mp.pi-mp.pi*u/n,mp.pi-mp.pi*w/n)
        diagnostics['boundary_projection_limit'].append({'N':n,'dirichlet_error':fmt(abs(low-sinc(u-w)+sinc(u+w))),'neumann_error':fmt(abs(high-sinc(u-w)-sinc(u+w)))})
    return {'exact_checks':sum(counts.values()),'exact_check_groups':dict(counts),
        'negative_control':{'li37_numerator':str(lam.numerator),'li37_denominator':str(lam.denominator),'li37_decimal_noncertified':fmt(mp.mpf(lam.numerator)/lam.denominator),'positive_filtered_outputs':len(filtered)},
        'numerical_diagnostics_only':diagnostics,
        'scope':'Finite exact regression is not the proof of the all-order identities or limiting theorems. No actual-zeta directed certificate, no historical certificate replay, no paper rebuild.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='audit_results.json'); args=ap.parse_args()
    result=run(); result['script_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_checks':result['exact_checks'],'groups':result['exact_check_groups'],'diagnostics':result['numerical_diagnostics_only']},indent=2))
