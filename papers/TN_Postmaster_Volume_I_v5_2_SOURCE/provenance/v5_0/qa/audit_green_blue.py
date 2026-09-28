#!/usr/bin/env python3
"""Independent finite checks for the Lighthouse/Blue merge review.

Exact arithmetic checks identities and finite synthetic controls. It does not
certify infinite-rank theorems, prime-error estimates, or an RH proof.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import json

COUNTS: Counter[str] = Counter()
def check(group: str, truth: bool) -> None:
    if not truth:
        raise AssertionError(group)
    COUNTS[group] += 1

def pm(m: int) -> list[Q]:
    return [Q((-1)**j * (comb(m+j+1,2*j+1)+comb(m+j,2*j+1)))
            for j in range(m+1)]

def vm(m: int) -> list[Q]:
    return [Q((-1)**j * comb(m+j,2*j)) for j in range(m+1)]

def mul(p: list[Q], q: list[Q]) -> list[Q]:
    ans=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): ans[i+j]+=a*b
    return ans

def ev(p, x):
    ans=0
    for c in reversed(p): ans=ans*x+c
    return ans

def combine(polys: list[list[Q]], coeffs: list[Q]) -> list[Q]:
    ans=[Q(0)]*max(map(len,polys))
    for p,c in zip(polys,coeffs):
        for j,a in enumerate(p): ans[j]+=c*a
    return ans

def catalan(j: int) -> Q:
    return Q(comb(2*j,j),j+1)

def catalan_integral(p: list[Q]) -> Q:
    return sum((a*catalan(j) for j,a in enumerate(p)),Q(0))

def eta_integral(p: list[Q]) -> Q:
    return sum((a*comb(2*j,j) for j,a in enumerate(p)),Q(0))

def component_integral(p: list[Q], ell: int) -> Q:
    a=ell*(ell-1); moments=[Q(1,ell)]
    for j in range(1,len(p)):
        moments.append((catalan(j-1)-moments[-1])/a)
    return sum((c*v for c,v in zip(p,moments)),Q(0))/(2*ell-1)

@dataclass(frozen=True)
class CQ:
    r: Q
    i: Q=Q(0)
    def __add__(self, other):
        b=other if isinstance(other,CQ) else CQ(Q(other))
        return CQ(self.r+b.r,self.i+b.i)
    __radd__=__add__
    def __neg__(self): return CQ(-self.r,-self.i)
    def __sub__(self, other): return self+(-other if isinstance(other,CQ) else -Q(other))
    def __rsub__(self, other): return -self+other
    def __mul__(self, other):
        b=other if isinstance(other,CQ) else CQ(Q(other))
        return CQ(self.r*b.r-self.i*b.i,self.r*b.i+self.i*b.r)
    __rmul__=__mul__
    def inv(self):
        n=self.r*self.r+self.i*self.i
        if not n: raise ZeroDivisionError('zero complex rational')
        return CQ(self.r/n,-self.i/n)
    def __truediv__(self, other):
        b=other if isinstance(other,CQ) else CQ(Q(other))
        return self*b.inv()
    def __pow__(self, n: int):
        if n<0: return self.inv()**(-n)
        ans=CQ(Q(1)); b=self
        while n:
            if n&1: ans=ans*b
            b=b*b; n//=2
        return ans
    def conjugate(self): return CQ(self.r,-self.i)
    def abs2(self): return self.r*self.r+self.i*self.i


def main() -> dict:
    P=[pm(j) for j in range(33)]
    V=[vm(j) for j in range(33)]
    for j in range(33):
        check('closed_P_at_minus_four_thirds',ev(P[j],Q(-4,3))==(Q(3**(j+1))-Q(1,3**j))/2)
        check('closed_V_at_minus_four_thirds',ev(V[j],Q(-4,3))==(Q(3**(j+1))+Q(1,3**j))/4)
        check('V_alternating_coefficients',all((-1)**k*c>0 for k,c in enumerate(V[j])))
        check('P_to_V_basis',combine(V[:j+1],[Q(2)]*j+[Q(1)])==P[j])
        check('V_value_geometric_bound',ev(V[j],Q(-4,3))<=3**j)
    for r in range(17):
        for s in range(17):
            pp=mul(P[r],P[s]); vv=mul(V[r],V[s])
            expected=4*r+1 if r==s else 4*min(r,s)+2
            check('Catalan_P_Gram',catalan_integral(pp)==expected)
            check('Catalan_V_orthogonality',catalan_integral(vv)==int(r==s))
            check('arcsine_P_Gram',eta_integral(pp)==2*min(r,s)+1)
            check('arcsine_V_Gram',eta_integral(vv)==(-1)**(r+s)*(2*min(r,s)+1))
            check('mixed_P_absolute_coefficients',sum(abs(c)*Q(4,3)**j for j,c in enumerate(pp))==ev(P[r],Q(-4,3))*ev(P[s],Q(-4,3)))
            check('mixed_V_absolute_coefficients',sum(abs(c)*Q(4,3)**j for j,c in enumerate(vv))==ev(V[r],Q(-4,3))*ev(V[s],Q(-4,3)))
    for n in range(1,25):
        G=[[4*r+1 if r==s else 4*min(r,s)+2 for s in range(n)] for r in range(n)]
        I=[[(-1)**(r+s)*(4*(n-max(r,s))-2-int(r==s)) for s in range(n)] for r in range(n)]
        for r in range(n):
            for s in range(n):
                check('Lighthouse_inverse_matrix',sum(G[r][k]*I[k][s] for k in range(n))==int(r==s))
        check('inverse_row_sum',max(sum(abs(a) for a in row) for row in I)==2*n*n-1)
        check('arcsine_trace',sum(2*j+1 for j in range(n))==n*n)
        S=sum((ev(V[j],Q(-4,3))**2 for j in range(n)),Q(0))
        check('mixed_block_S_closed',S==Q(9,128)*(Q(9**n)-Q(1,9**n))+Q(3*n,8))
        check('mixed_block_S_upper',S<=Q(9**n-1,8))
    for N in range(0,129):
        M=N//2+1
        check('maximal_mixed_block_degree',2*(M-1)<=N)
        check('block_rate_comparison',9**M<=9*3**N)
        check('old_diagonal_admissibility',2*(N//2)<=N)
    check('exact_alpha3_comparison',Q(12,5)**2<6)
    check('exact_alpha4_comparison',Q(12,5)**2<Q(29,5))
    check('cutoff5_decay',5**7>3**10)
    check('cutoff13_decay',13**7>6**10)
    check('block_constant_conversion',Q(1125,8)==Q(125,2)*Q(9,4))
    # Generic real polynomials, and one positive reserve component. No prime data.
    for n in range(1,11):
        S=sum((ev(V[j],Q(-4,3))**2 for j in range(n)),Q(0))
        for seed in range(7):
            a=[Q(((seed+3)*(j+2))%11-5,j+1) for j in range(n)]
            if not any(a): a[0]=Q(1)
            p=combine(V[:n],a); p2=mul(p,p)
            C=catalan_integral(p2); Rc=component_integral(p2,3)
            check('finite_lower_reserve_test',Rc>=C/125 and C==sum(t*t for t in a))
            check('finite_compensation_test',eta_integral(p2)<=n*n*C)
            for c in (Q(1,3),Q(1),Q(5)):
                y=1/(2+c)
                source=abs(y*ev(p,y)**2)
                disk=1/(2+c-Q(3,4))
                check('rational_source_normalized_block',source<=125*S*disk*Rc)
    # Tied dominant conjugate pairs and a strictly smaller mode.
    ws=[CQ(Q(1),Q(1)),CQ(Q(1,5),Q(7,5)),CQ(Q(1),Q(1,2))]
    ys=[2-w-w.inv() for w in ws]
    check('tied_maximal_mode',ws[0].abs2()==ws[1].abs2()>ws[2].abs2()>1)
    y0,y1,y2=ys
    annihilator=[y1.abs2(),-2*y1.r,Q(1)]
    check('annihilator_at_tie',ev(annihilator,y1)==CQ(Q(0)))
    check('annihilator_at_selected',ev(annihilator,y0)!=CQ(Q(0)))
    for n in range(21):
        w=ws[0]
        T=(w**n+w**(-n))/2
        c=y0*(ev(annihilator,y0)*T)**2
        b00=2*c.r; b01=2*(c*y0).r; b11=2*(c*y0*y0).r
        determinant=b00*b11-b01*b01
        check('tied_pair_exact_two_signs',determinant==-4*c.abs2()*y0.i*y0.i and determinant<0)
        # Both normalizations describe exactly the same outside radius.
        phi=-w
        check('Lighthouse_Blue_root_sign',phi+phi.inv()==y0-2)
    for rho in [CQ(Q(3,4),Q(2)),CQ(Q(2,3),Q(5)),CQ(Q(1,2),Q(3))]:
        q=rho*(1-rho); y=q.inv(); w=1-rho.inv()
        check('actual_fold_coordinate_identity',w+w.inv()==2-y)
    return {'status':'PASS','total_assertions':sum(COUNTS.values()),
            'groups':dict(COUNTS),
            'scope':'Independent finite algebra; synthetic mode tests and rational analytic examples only.',
            'not_certified':['all-rank or limit statements by computation','actual-zero certificates','the signed prime-error bound'],
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    result=main()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
