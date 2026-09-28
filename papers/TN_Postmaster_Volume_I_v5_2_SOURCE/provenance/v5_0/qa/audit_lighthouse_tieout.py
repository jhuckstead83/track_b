#!/usr/bin/env python3
"""Exact finite regressions for the Lighthouse tie-out.
All pass/fail arithmetic uses Fraction or integers. Optional mpmath output
is separately labelled diagnostic and never decides an assertion.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from math import comb, factorial
from pathlib import Path

counts: Counter[str] = Counter()

def check(category: str, statement: bool) -> None:
    if not statement:
        raise AssertionError(category)
    counts[category] += 1

def cat(m: int) -> int:
    return comb(2*m,m)//(m+1)

def tri(n: int) -> int:
    return n*(n+1)//2

def add(a, b):
    out=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): out[i]+=x
    for i,x in enumerate(b): out[i]+=x
    return out

def scale(a, c): return [c*x for x in a]

def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def polys(n):
    out=[[F(1)]]
    if n==0: return out
    out.append([F(3),F(-1)])
    for k in range(1,n):
        out.append(add(mul([F(2),F(-1)],out[-1]),scale(out[-2],F(-1))))
    return out

def apply(p,mom): return sum((x*mom[i] for i,x in enumerate(p)),F(0))

def determinant(a):
    a=[row[:] for row in a]
    ans=F(1)
    for i in range(len(a)):
        if not a[i][i]:
            k=next((k for k in range(i+1,len(a)) if a[k][i]),None)
            if k is None: return F(0)
            a[i],a[k]=a[k],a[i]; ans=-ans
        p=a[i][i]; ans*=p
        for j in range(i+1,len(a)):
            t=a[j][i]/p
            for k in range(i+1,len(a)): a[j][k]-=t*a[i][k]
    return ans

def reserve_component(n,ell):
    t=1-F(1,ell)
    return t**n-1+F(n,ell)

def main(outpath):
    table=[]
    for m in range(101):
        C=cat(m); T=tri(2*m+1)
        check('Catalan integrality',C==comb(2*m,m)-comb(2*m,m+1))
        B=factorial(m)**2*C
        check('odd factorial factorization',factorial(2*m+1)==T*B)
        beta=F(4**m*factorial(m)**2,factorial(2*m+1))
        check('Catalan Beta product',beta*F(C,4**m)==F(1,T))
        check('product-law moments',F(2,2*m+1)-F(1,m+1)==F(1,T))
        check('Catalan-density moments',F(4*comb(2*m,m)-comb(2*m+2,m+1),2)==C)
        # Coefficient from x*cos(x) - x^2*sin(x)/2.
        rhs=F((-1)**m,factorial(2*m))
        if m: rhs+=F((-1)**m,2*factorial(2*m-1))
        check('weighted sine coefficients',rhs==F((-1)**m*tri(2*m+1),factorial(2*m+1)))
        if m<=6: table.append({'m':m,'Catalan':C,'odd_index':2*m+1,'reduced_denominator':B,'beta':str(beta)})

    P=polys(9)
    arcs=[F(comb(2*j,j)) for j in range(20)]
    omega=[arcs[j+1]/2 for j in range(19)]
    for r in range(10):
        for s in range(10):
            f=mul(P[r],P[s]); h=2*min(r,s)+1
            check('arcsine reflected Gram',apply(f,arcs)==h)
            check('sine orthogonality Gram',apply(f,omega)==int(r==s))

    # Independent routes: moment recurrence for the Catalan resolvent,
    # versus finite Fourier/Poisson formula in the reflected basis.
    for ell in list(range(3,24,2))+[F(3,2),F(5,2),F(11,3)]:
        ell=F(ell); t=1-1/ell; a=ell*(ell-1)
        M=[1/ell]
        for j in range(1,19): M.append((cat(j-1)-M[-1])/a)
        for r in range(10):
            for s in range(10):
                h=2*min(r,s)+1; L=r+s+1; d=abs(r-s)
                gram=apply(mul(P[r],P[s]),M)/(2*ell-1)
                fourier=2*h/(2*ell-1)-(t**d-t**L)
                check('Catalan resolvent versus Fourier Gram',gram==fourier)
                c=1/(ell*(2*ell-1))
                shifted=reserve_component(L,ell)-reserve_component(d,ell)+c*h
                check('reserve-component accounting',gram==shifted)
        for y in [F(1,100),F(1,3),F(1),F(3),F(4)]:
            poisson=(1-t*t)/((1-t)**2+t*y)
            check('density identity',2/(2*ell-1)-y*poisson/2==(4-y)/(2*(2*ell-1)*(1+a*y)))
            check('density nonnegativity',(4-y)/(2*(2*ell-1)*(1+a*y))>=0)

    finite_ells=[3,5,7,9,11,13]
    G=[]
    for r in range(8):
        row=[]
        for s in range(8):
            h=2*min(r,s)+1; L=r+s+1; d=abs(r-s)
            row.append(sum((F(2*h,2*ell-1)-(1-F(1,ell))**d+(1-F(1,ell))**L for ell in finite_ells),F(0)))
        G.append(row)
    leading=[]
    for n in range(1,9):
        det=determinant([row[:n] for row in G[:n]])
        check('finite positive comparison leading minors',det>0)
        leading.append(str(det))

    # Rational elementary enclosure proving lambda_1 < 1/16.
    log2lower=2*(F(1,3)+F(1,3*3**3)+F(1,5*3**5))
    log3lower=2*(F(1,2)+F(1,3*2**3)+F(1,5*2**5))
    H32=sum((F(1,k) for k in range(1,33)),F(0))
    pilower=4*sum((F((-1)**k,2*k+1) for k in range(8)),F(0))
    check('elementary pi lower bound',pilower>3)
    check('Euler constant bound',H32-5*log2lower<F(3,5))
    check('log 12 lower bound',2*log2lower+log3lower>F(99,40))
    check('lambda1 upper bound',1+F(3,10)-F(99,80)==F(1,16))
    check('original reserve negative witness',F(3,8)-3*(F(1,9)+F(1,25))==F(-47,600))
    check('critical anchor above lambda1',sum((F(1,ell*(2*ell-1)) for ell in [3,5,7,9]),F(0))>F(1,10))

    # Off-diagonal bookkeeping for arbitrary exact data, distinct from
    # any assertion about an evaluated zeta source.
    lam=[F(0)]+[F(((-1)**n)*(n*n+3),n+1) for n in range(1,18)]
    ellset=[3,5,7,9]; c0=F(1,43)
    astar=sum((F(1,ell*(2*ell-1)) for ell in ellset),F(0))
    A=[c0*n+sum((reserve_component(n,ell) for ell in ellset),F(0)) for n in range(18)]
    E=[A[n]-lam[n] for n in range(18)]
    delta=astar-c0
    for r in range(9):
        for s in range(9):
            L=r+s+1; d=abs(r-s); h=L-d
            reserve=A[L]-A[d]+delta*h
            defect=E[L]-E[d]+delta*h
            check('full source-difference preservation',reserve-defect==lam[L]-lam[d])

    diagnostics={}
    try:
        import mpmath as mp
        mp.mp.dps=60
        lam1=1+mp.euler/2-mp.log(4*mp.pi)/2
        star=mp.pi/4+mp.log(2)/2-1
        g2=mp.pi**2/8-1
        g3=mp.mpf(7)*mp.zeta(3)/8-1
        R=mp.matrix([[lam1,lam1+g2],[lam1+g2,3*lam1+3*g2-g3]])
        diagnostics={'label':'high-precision floating-point orientation only; not interval certificates',
            'lambda1':mp.nstr(lam1,48),'critical_anchor':mp.nstr(star,48),
            'anchor_shift':mp.nstr(star-lam1,48),
            'original_reserve_y_squared':mp.nstr(6*lam1-3*g2-g3,48),
            'original_reserve_det2':mp.nstr(mp.det(R),48)}
    except ImportError:
        diagnostics={'label':'mpmath unavailable; exact audit unaffected'}

    result={'status':'PASS','exact_assertions':sum(counts.values()),'categories':dict(counts),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'small_odd_slice':table,'positive_comparison_finite_ells':finite_ells,
        'leading_determinants':leading,
        'rational_bounds':{'log2_lower':str(log2lower),'log3_lower':str(log3lower),
             'gamma_upper':str(H32-5*log2lower),'pi_lower':str(pilower),
             'reserve_witness_strict_upper':'-47/600'},
        'diagnostics':diagnostics,
        'scope':'Finite algebra regressions only. Infinite-rank positivity and sharpness rest on the written measure proof. No actual-source all-order domination, RH proof, historical certificate replay, or PDF build.'}
    Path(outpath).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','exact_assertions','categories','diagnostics']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='audit_results.json')
    args=parser.parse_args()
    main(args.out)
