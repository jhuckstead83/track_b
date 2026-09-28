#!/usr/bin/env python3
"""Numeric and symbolic replay of the load-bearing identities in
TN Postmaster Research Volume I v0.5, Definitive Master Union (16 August 2026; Zenodo 10.5281/zenodo.21968858),
synthesis layer, and of the external constant-Jacobian counterexample it records. Team B, 27 September 2026.

Needs sympy. The totient checks sieve to 10^6 (a few seconds).
"""
import math, json, sys
from fractions import Fraction
import sympy as sp

checks = []
def ok(name, cond, detail=None):
    checks.append({'check': name, 'pass': bool(cond), **({'detail': detail} if detail is not None else {})})
    print(('PASS ' if cond else 'FAIL ') + name + ('' if detail is None else '  ' + str(detail)))

# (5.1) Wilson floor gate and (6.1) the successor reduced-numerator gate
def is_prime(n): return n > 1 and all(n % p for p in range(2, int(n ** 0.5) + 1))
wil = all((math.factorial(n - 1) % n) // (n - 1) == int(is_prime(n)) for n in range(2, 400))
ok('(5.1) floor(r_n/(n-1)) = 1_P(n) for 2 <= n < 400', wil)
def U(j): return Fraction(j + 1, 2 * math.factorial(j - 1)).numerator
ok('(6.1) reduced numerator of T_j/j! is j+1 at odd primes j+1, else 1 (2 <= j < 300)',
   all(U(j) == ((j + 1) if is_prime(j + 1) and j + 1 > 2 else 1) for j in range(2, 300)))
# (5.3) Willans' formula
def W(j): return 1 if j == 1 else int(is_prime(j))
def willans(n):
    C = 0; tot = 1
    for i in range(1, 2 ** n + 1):
        C += W(i); tot += int((n / C) ** (1 / n) + 1e-12) if C <= n else 0
    return tot
ok("(5.3) Willans' formula gives p_1..p_9", [willans(n) for n in range(1, 10)] == [2, 3, 5, 7, 11, 13, 17, 19, 23])
# (8.1) odd shells
T = lambda j: j * (j + 1) // 2 if j >= 0 else 0
ok('(8.1) n^2 = T_n + T_{n-1}, 2n-1 = T_n - T_{n-2}', all(n * n == T(n) + T(n - 1) and 2 * n - 1 == T(n) - T(n - 2) for n in range(1, 500)))
# (10.4) Mobius between Theta_square and Psi_square on a sample of X
def primes_upto(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b'\x00\x00'
    for p in range(2, int(N ** 0.5) + 1):
        if s[p]: s[p * p::p] = bytearray(len(s[p * p::p]))
    return [i for i in range(N + 1) if s[i]]
P = primes_upto(10 ** 5)
theta = lambda y: sum(math.log(p) for p in P if p <= y)
psi = lambda y: sum(math.log(p) * int(math.log(y) / math.log(p) + 1e-12) for p in P if p <= y)
X = 10 ** 8
ThetaSq = lambda X: theta(math.isqrt(int(X)) + 1e-9)
PsiSq = lambda X: psi(math.sqrt(X))
lhs = PsiSq(X); rhs = sum(theta(X ** (1 / (2 * j))) for j in range(1, 60))
ok('(10.4) Psi_sq(X) = sum_j Theta_sq(X^(1/j)) at X = 10^8', abs(lhs - rhs) < 1e-6 * lhs, [round(lhs, 6), round(rhs, 6)])
# (19.4)-(19.8) conic
x, y = sp.symbols('x y')
G = 4 * x ** 2 + 7 * x * y + 4 * y ** 2 + x + y - 1
ok('(19.4) (1/2)(x-1)(y-1) = 2(x+y)^2 is G = 0', sp.expand(2 * (sp.Rational(1, 2) * (x - 1) * (y - 1) - 2 * (x + y) ** 2) + G) == 0)
Pt = {x: sp.Rational(-4, 5), y: sp.Rational(1, 5)}
Gx, Gy = sp.diff(G, x), sp.diff(G, y)
yp = -Gx / Gy
ypp = -(sp.diff(G, x, 2) * Gy ** 2 - 2 * sp.diff(G, x, y) * Gx * Gy + sp.diff(G, y, 2) * Gx ** 2) / Gy ** 3
kappa = sp.simplify(sp.Abs(ypp.subs(Pt)) / (1 + yp.subs(Pt) ** 2) ** sp.Rational(3, 2))
Q = (-1 - sp.sqrt(17)) / 8
mPQ = sp.nsimplify((0 - sp.Rational(1, 5)) / (Q + sp.Rational(4, 5)))
ok('(19.6)-(19.8) tangent slope -4/3, y\'\'=32/27, curvature 32/125, chord slope -(27+5 sqrt17)/38',
   G.subs(Pt) == 0 and yp.subs(Pt) == sp.Rational(-4, 3) and ypp.subs(Pt) == sp.Rational(32, 27) and kappa == sp.Rational(32, 125)
   and sp.simplify(mPQ + (27 + 5 * sp.sqrt(17)) / 38) == 0)
# (20.4k) Pade
t = sp.symbols('t')
R = (60 * t - 7 * t ** 3) / (60 + 3 * t ** 2)
ok('(20.4k) R_{3,2} - sin = -11 t^7/50400 + O(t^9)', sp.series(R - sp.sin(t), t, 0, 9).removeO() == -sp.Rational(11, 50400) * t ** 7)
# (20.4c)-(20.4e) totient table and mod-4 densities to 10^6
N = 10 ** 6; phi = list(range(N + 1))
for p in range(2, N + 1):
    if phi[p] == p:
        for k in range(p, N + 1, p): phi[k] -= phi[k] // p
tab = {10: '0.330000000000', 100: '0.304500000000', 1000: '0.304193000000', 10 ** 4: '0.303974870000', 10 ** 5: '0.303965075500', 10 ** 6: '0.303963552393'}
S = 0; got = {}; F4 = [0, 0, 0, 0]
for m in range(1, N + 1):
    S += phi[m]; F4[m % 4] += phi[m]
    if m in tab: got[m] = '%.12f' % ((1 + S) / m ** 2)
ok('(20.4c) R143L table F(M)/M^2 reproduces all six printed rows', got == tab)
d = [f / N ** 2 for f in F4]
ok('(20.4e) mod-4 densities 1/pi^2 (classes 1, 3) and 1/(2 pi^2) (classes 0, 2)',
   abs(d[1] - 1 / math.pi ** 2) < 2e-6 and abs(d[3] - 1 / math.pi ** 2) < 2e-6 and abs(d[0] - 0.5 / math.pi ** 2) < 2e-6 and abs(d[2] - 0.5 / math.pi ** 2) < 2e-6,
   [round(v, 7) for v in d])
# (20.4t) quintic branch values
xs = sp.symbols('xs'); b = sp.symbols('b')
disc = sp.discriminant(xs ** 5 - xs + b, xs)
ok('(20.4t) branch values of x^5 - x + b lie on |b| = 4/5^(5/4)', all(abs(abs(complex(r)) - 4 / 5 ** 1.25) < 1e-12 for r in sp.Poly(disc, b).nroots()))
# (20.5) entropy of the zeta source at sigma = 3
import mpmath as mpm
H1 = mpm.log(mpm.zeta(3)) - 3 * mpm.zeta(3, derivative=1) / mpm.zeta(3)
H2 = sum(-math.log(1 - p ** -3.0) + 3 * math.log(p) / (p ** 3.0 - 1) for p in P)
ok('(20.5) H_sigma = log zeta - sigma zeta\'/zeta = sum over primes (sigma = 3)', abs(float(H1) - H2) < 1e-9, [float(H1), H2])
# (18.1)-(18.3) the constant-Jacobian counterexample
X_, Y_, Z_ = sp.symbols('X Y Z'); u = 1 + X_ * Y_
F = sp.Matrix([u ** 3 * Z_ + Y_ ** 2 * u * (4 + 3 * X_ * Y_), Y_ + 3 * X_ * u ** 2 * Z_ + 3 * X_ * Y_ ** 2 * (4 + 3 * X_ * Y_), 2 * X_ - 3 * X_ ** 2 * Y_ - X_ ** 3 * Z_])
det = sp.expand(F.jacobian([X_, Y_, Z_]).det())
sols = sp.solve([F[0] + sp.Rational(1, 4), F[1], F[2]], [X_, Y_, Z_], dict=True)
ok('(18.2)-(18.3) det J_F = -2 identically; F = (-1/4, 0, 0) has exactly the three stated preimages',
   det == -2 and len(sols) == 3 and {(s[X_], s[Y_], s[Z_]) for s in sols} == {(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)), (-1, sp.Rational(3, 2), sp.Rational(13, 2))})
fails = [c for c in checks if not c['pass']]
json.dump({'document': 'TN Postmaster Research Volume I v0.5 synthesis (10.5281/zenodo.21968858)', 'checks': checks,
           'status': 'PASS' if not fails else 'FAIL'}, open('V05_SYNTHESIS_CHECKS.json', 'w'), indent=1)
print(f'{len(checks) - len(fails)}/{len(checks)} checks passed')
sys.exit(1 if fails else 0)
