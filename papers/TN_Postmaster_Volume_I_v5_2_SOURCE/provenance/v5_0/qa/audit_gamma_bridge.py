#!/usr/bin/env python3
"""Replay for the v4.8 Euler-constant bridge (Reading Volume §R4A, Dossier §96A)
and for the classical Faulhaber checks added to §R2.

Every check below is either exact (sympy / Fraction) or a high-precision
numerical comparison whose tolerance is stated.  The certified block uses Arb
(python-flint) interval arithmetic and records the enclosures it proves.

Usage: python3 qa/audit_gamma_bridge.py --output qa/GAMMA_BRIDGE.json
Exit code 0 iff every check passes.  Nothing here bears on the Riemann
hypothesis, which remains open.
"""
from __future__ import annotations
import argparse, json, sys, time
from fractions import Fraction
from math import comb

import mpmath
from mpmath import mp, mpf, zeta, nsum, inf, quad, loggamma, log, pi, euler, binomial, harmonic, glaisher, psi
import sympy as sp

checks = []
def ck(tag, name, ok, detail=None):
    checks.append({'tag': tag, 'name': name, 'passed': bool(ok), 'detail': detail})

def s(x, n=30):
    return mpmath.nstr(x, n)

t0 = time.monotonic()
mp.dps = 60
g = +euler
L2P = log(2 * pi)
T = lambda k: mpf(k) * (k + 1) / 2
TOL = mpf(10) ** -45

# ---------------------------------------------------------------- G.1 / G.2
S1 = 1 + nsum(lambda k: (zeta(k) - 1) / T(k), [2, inf])          # sum_{k>=2} 1/T_k = 1 exactly
ck('96A.2', 'sum_{k>=2} zeta(k)/T_k = log(2 pi) - gamma', abs(S1 - (L2P - g)) < TOL, s(S1 - (L2P - g), 5))
S1m = nsum(lambda k: (zeta(k) - 1) / T(k), [2, inf])
ck('Thm 96A.3', 'sum_{k>=2} (zeta(k)-1)/T_k = log(2 pi) - 1 - gamma', abs(S1m - (L2P - 1 - g)) < TOL, s(S1m, 25))
ck('4.1', 'Mengoli: sum_{k>=2} 1/T_k = 1 (exact telescope)',
   sum(Fraction(2, k * (k + 1)) for k in range(2, 2001)) == 1 - Fraction(2, 2001))

# ---------------------------------------------------------------- G.3 truncated identity
ok = True; worst = mpf(0)
for M in range(1, 31):
    lhs = 1 + sum((2 - mpf(1) / m + 2 * (m - 1) * log(1 - mpf(1) / m)) for m in range(2, M + 1))
    # direct double sum with the truncated zeta values; the m=1 column is the exact
    # Mengoli telescope sum_{k>=2} 1/T_k = 1, the other columns converge geometrically
    direct = 1 + sum(nsum(lambda k: mpf(m) ** (-k) / T(k), [2, inf]) for m in range(2, M + 1)) if M <= 8 else lhs
    rhs = 2 * M - harmonic(M) - 2 * (M * log(M) - loggamma(M + 1))
    worst = max(worst, abs(lhs - rhs), abs(direct - rhs))
    ok &= abs(lhs - rhs) < TOL and abs(direct - rhs) < mpf(10) ** -40
ck('96A.3', 'truncated identity sum_{k>=2} zeta_M(k)/T_k = 2M - H_M - 2 log(M^M/M!) (M<=30)', ok, s(worst, 5))
M = 10 ** 6
SM = 2 * M - harmonic(M) - 2 * (M * log(M) - loggamma(M + 1))
dev = SM - (L2P - g) + mpf(1) / (3 * M) - mpf(1) / (12 * M * M)
ck('96A.3', 'Stirling limit: S_M = log(2 pi) - gamma - 1/(3M) + 1/(12M^2) + O(M^-3) at M=10^6', abs(dev) < mpf(10) ** -15, s(dev, 5))

# ---------------------------------------------------------------- G.4 interval masses
mp.dps = 40
ok = True; worst = mpf(0)
for m in range(1, 21):
    series = nsum(lambda k: mpf(m) ** (-k) / T(k), [2, inf])
    closed = mpf(1) if m == 1 else 2 - mpf(1) / m + 2 * (m - 1) * log(1 - mpf(1) / m)
    integral = quad(lambda x: ((x - (m - 1)) / x) ** 2, [m - 1, m]) if m > 1 else quad(lambda x: mpf(1), [0, 1])
    worst = max(worst, abs(series - closed), abs(integral - closed))
    ok &= abs(series - closed) < mpf(10) ** -30 and abs(integral - closed) < mpf(10) ** -30
ck('96A.4', 'sum_{k>=2} m^{-k}/T_k = int_{m-1}^{m} ({x}/x)^2 dx, closed form, m=1..20', ok, s(worst, 5))

# ---------------------------------------------------------------- G.5 fractional-part norm and Plancherel
mp.dps = 30
tail_sum = nsum(lambda m: 2 - mpf(1) / m + 2 * (m - 1) * log(1 - mpf(1) / m), [2, inf])
ck('96A.5', 'int_0^inf ({x}/x)^2 dx = 1 + sum_m(interval masses) = log(2 pi) - gamma',
   abs(1 + tail_sum - (log(2 * pi) - euler)) < mpf(10) ** -25, s(1 + tail_sum, 25))
# numerical sanity check of the Mellin-Plancherel form (not a certificate):
# (1/2pi) int_R |zeta(1/2+it)|^2/(1/4+t^2) dt, integrated to |t|<=Tcut plus the
# second-moment tail model int_Tcut^inf (log(t/2pi)+2gamma)/t^2 dt / pi.
mp.dps = 15
Tcut = 200
grid = [0] + [0.5 * j for j in range(1, 2 * Tcut + 1)]
body = mpmath.quad(lambda t: abs(zeta(mpf(1) / 2 + 1j * t)) ** 2 / (mpf(1) / 4 + t * t), grid)
tail = (log(Tcut / (2 * pi)) + 1 + 2 * euler) / Tcut
plan = (body + tail) / pi   # (1/2pi) * 2 * (body + tail)
ck('96A.5', 'Plancherel form (1/2pi) int |zeta(1/2+it)|^2/(1/4+t^2) dt ~ log(2 pi) - gamma (numerical sanity check, tol 1e-4 as printed)',
   abs(plan - (log(2 * pi) - euler)) < 1e-4, {'value': s(plan, 10), 'target': s(log(2 * pi) - euler, 10)})

# ---------------------------------------------------------------- G.6 / G.7 Raabe and digamma moment
mp.dps = 40
ck('Thm 96A.3 proof 1', 'Raabe: int_0^1 log Gamma = log(2 pi)/2', abs(quad(loggamma, [0, 1]) - log(2 * pi) / 2) < mpf(10) ** -35)
for w in (mpf('0.3'), mpf('0.7')):
    taylor = euler * w + nsum(lambda k: zeta(k) * w ** k / k, [2, inf])
    ck('Thm 96A.3 proof 1', f'log Gamma(1-w) = gamma w + sum zeta(k) w^k/k at w={w}', abs(taylor - loggamma(1 - w)) < mpf(10) ** -30)
dig = -euler - 2 * quad(lambda v: v * psi(0, v), [0, 1])
ck('Thm 96A.3 proof 2', 'digamma moment: sum zeta(k)/T_k = -gamma - 2 int_0^1 v psi(v) dv', abs(dig - (log(2 * pi) - euler)) < mpf(10) ** -30)
ck('4.5', 'Hausdorff moment (4.5): 1/T_k = int_0^1 u^{k-1} 2(1-u) du (k=1..12, exact)',
   all(Fraction(2, k * (k + 1)) == 2 * (Fraction(1, k) - Fraction(1, k + 1)) for k in range(1, 13)))

# ---------------------------------------------------------------- G.8 - G.10 Ramanujan and the mirror
e = sp.symbols('e')
K = 10
Fser = sp.series(e / 2 - sp.log(1 + e) / 2 - sum(sp.bernoulli(2 * k) * e ** (2 * k) / (2 * k) for k in range(1, K + 1)), e, 0, 2 * K + 1).removeO()
mirror = sp.expand(sp.series(Fser.subs(e, -e / (1 + e)), e, 0, 2 * K + 1).removeO() - Fser)
ck('96A.1', 'F(n)=psi(n+1)-(1/2)log(n(n+1)) is formally invariant under n -> -1-n (order 20)', mirror == 0)
u = 2 * e ** 2 / (1 + e)
Rs = sp.symbols('R1:%d' % (K + 1))
ans = sp.series(sum(Rs[k - 1] * u ** k for k in range(1, K + 1)), e, 0, 2 * K + 1).removeO()
sol = sp.solve(sp.Poly(sp.expand(Fser - ans), e).all_coeffs(), Rs, dict=True)
R = [sol[0][r] for r in Rs] if len(sol) == 1 else None
expectR = [sp.Rational(1, 12), sp.Rational(-1, 120), sp.Rational(1, 630), sp.Rational(-1, 1680), sp.Rational(1, 2310),
           sp.Rational(-191, 360360), sp.Rational(29, 30030), sp.Rational(-2833, 1166880), sp.Rational(140051, 17459442),
           sp.Rational(-6525613, 193993800)]
ck('96A.1a', 'Ramanujan coefficients varrho_1..varrho_10 (overdetermined system consistent)', R == expectR, [str(x) for x in (R or [])])
# centered variable: F = sum c_m u^{-2m}, u = n + 1/2
U = sp.symbols('U', positive=True)
cm = [((1 - sp.Integer(2) ** (1 - 2 * m)) * sp.bernoulli(2 * m) + sp.Integer(2) ** (-2 * m)) / (2 * m) for m in range(1, K + 1)]
Fu = sp.series(Fser.subs(e, 1 / (U - sp.Rational(1, 2))), U, sp.oo, 2 * K + 1).removeO()
Fu_expected = sum(cm[m - 1] * U ** (-2 * m) for m in range(1, K + 1))
diffu = sp.expand(sp.series(Fu - Fu_expected, U, sp.oo, 2 * K + 1).removeO())
ck('96A.1', 'centered coefficients c_m = [(1-2^{1-2m})B_{2m} + 2^{-2m}]/(2m) (m<=10)', diffu == 0, [str(c) for c in cm[:4]])
ck('96A.1', 'odd Bernoulli polynomials vanish at 1/2 (k<=21)', all(sp.bernoulli(k, sp.Rational(1, 2)) == 0 for k in range(1, 22, 2)))
mp.dps = 40
for n in (5, 10, 40):
    Tn = mpf(n * (n + 1)) / 2
    val = harmonic(n) - log(2 * Tn) / 2 - sum(mpf(int(sp.numer(R[k]))) / int(sp.denom(R[k])) / Tn ** (k + 1) for k in range(6))
    bound = abs(mpf(int(sp.numer(R[6]))) / int(sp.denom(R[6]))) / Tn ** 7
    ck('96A.1a', f'numerical Ramanujan check n={n}: |error| <= |varrho_7|/T_n^7', abs(val - euler) <= bound, s(val - euler, 5))
ck('Cor 96A.2', 'coefficient trap: varrho_1=-zeta(-1), varrho_2=-zeta(-3), varrho_3!=-zeta(-5)',
   R[0] == -sp.zeta(-1) and R[1] == -sp.zeta(-3) and R[2] != -sp.zeta(-5), [str(-sp.zeta(-5))])
# DeTemple/Wang centering: psi(u+1/2) - log u is even in u

# ---------------------------------------------------------------- G.11 simplex ladder
mp.dps = 40
logA = log(glaisher)
named = {2: log(2 * pi) - euler,
         3: mpf(3) / 2 * log(2 * pi) - 6 * logA - euler,
         4: 2 * log(2 * pi) - 12 * logA + 3 * zeta(3) / pi ** 2 - euler}
def moment_closed(m):
    val = log(2 * pi) / (2 * (m + 1))
    for j in range(1, m + 1):
        fall = 1
        for i in range(j - 1):
            fall *= (m - i)
        val -= fall * (-1) ** j * (zeta(-j, derivative=1) + harmonic(j) * zeta(-j)) / mpmath.factorial(j)
    return val
for d in range(2, 10):
    series = mpf(1) / (d - 1) + nsum(lambda k: (zeta(k) - 1) / binomial(k + d - 1, d), [2, inf])
    viaq = d * (d - 1) * quad(lambda v: v ** (d - 2) * loggamma(v), [0, 1]) - euler
    viac = d * (d - 1) * moment_closed(d - 2) - euler
    ok = abs(series - viaq) < mpf(10) ** -35 and abs(series - viac) < mpf(10) ** -35
    if d in named:
        ok &= abs(series - named[d]) < mpf(10) ** -35
    ck('96A.6-96A.8', f'simplex rung d={d}: series, quadrature and (96A.7) agree to 1e-35', ok, s(series, 25))
ck('Thm 96A.5', 'Beta form 1/C(k+d-1,d) = d*B(k,d) (exact, k,d<=12)',
   all(Fraction(1, comb(k + d - 1, d)) == d * Fraction(sp.factorial(k - 1) * sp.factorial(d - 1), sp.factorial(k + d - 1)) for k in range(1, 13) for d in range(1, 13)))
KK = 399
ck('76.8', 'reciprocal simplex telescope: sum_{k<=K} 1/C(k+d-1,d) = (d/(d-1))(1 - 1/C(K+d-1,d-1)) (exact, K=399, d=2..8)',
   all(sum(Fraction(1, comb(k + d - 1, d)) for k in range(1, KK + 1)) == Fraction(d, d - 1) * (1 - Fraction(1, comb(KK + d - 1, d - 1))) for d in range(2, 9)))
# structure of the rungs in the constants log(2pi), gamma and zeta'(-j):
# gamma-coefficient -1, log(2pi)-coefficient d/2, and rung d introduces zeta'(2-d)
Lg, gg = sp.symbols('L g')
Zp = sp.symbols('Zp1:20')
ok = True
for d in range(2, 20):
    m = d - 2
    mom = Lg / (2 * (m + 1)) - sum(sp.ff(m, j - 1) * (-1) ** j / sp.factorial(j) * (Zp[j - 1] + sp.harmonic(j) * sp.zeta(-j))
                                  for j in range(1, m + 1))
    E = sp.expand(d * (d - 1) * mom - gg)
    ok &= E.coeff(gg) == -1 and E.coeff(Lg) == sp.Rational(d, 2)
    ok &= all(E.coeff(Zp[j - 1]) != 0 for j in range(1, m + 1)) and all(E.coeff(Zp[j - 1]) == 0 for j in range(m + 1, 20))
ck('96A.8', "in the constants log(2pi), gamma, zeta'(-j): gamma-coefficient -1, log(2pi)-coefficient d/2, rung d adds zeta'(2-d) (d<=19)", ok)
ck('96A.8', "zeta'(-2) = -zeta(3)/(4 pi^2) and zeta'(-4) = 3 zeta(5)/(4 pi^4)",
   abs(zeta(-2, derivative=1) + zeta(3) / (4 * pi ** 2)) < mpf(10) ** -35 and abs(zeta(-4, derivative=1) - 3 * zeta(5) / (4 * pi ** 4)) < mpf(10) ** -35)
ck('96A.7', 'moment int_0^1 u logGamma = log(2pi)/4 - log A',
   abs(quad(lambda v: v * loggamma(v), [0, 1]) - (log(2 * pi) / 4 - logA)) < mpf(10) ** -35)

# ---------------------------------------------------------------- denominator coefficients (155G.1)
# B(z) = z zeta(1/(1-z)) = (1-z) + sum_n (-1)^n gamma_n z^{n+1} (1-z)^{-n} / n!  (Laurent series at s=1)
mp.dps = 30
stj = [mpmath.stieltjes(n) for n in range(0, 24)]
def bden(N):
    if N == 0:
        return mpf(1)
    if N == 1:
        return stj[0] - 1
    return sum((-1) ** n * stj[n] / mpmath.factorial(n) * binomial(N - 2, N - 1 - n) for n in range(1, N))
bvals = [bden(N) for N in range(0, 24)]
ck('155G', 'b_1^den = gamma - 1 < 0 (exact from the Laurent expansion at s=1)', abs(bvals[1] - (euler - 1)) < mpf(10) ** -25 and bvals[1] < 0, s(bvals[1], 12))
# independent evaluation by the Cauchy integral on |z| = 1/2 (no Stieltjes constants)
Mpts = 256
zpts = [mpf('0.5') * mpmath.exp(2j * pi * k / Mpts) for k in range(Mpts)]
fv = [z * zeta(1 / (1 - z)) for z in zpts]
cau = [(sum(v * mpmath.exp(-2j * pi * k * N / Mpts) for k, v in enumerate(fv)) / Mpts / mpf('0.5') ** N).real for N in range(0, 24)]
ck('155G', 'Stieltjes-constant and Cauchy-integral coefficients agree (N<=23, 1e-12)', all(abs(a - b) < mpf(10) ** -12 for a, b in zip(bvals, cau)))
ck('155G', 'numerically b_2..b_16 > 0 > b_17 (sign pattern printed in 155G and R17I; b_17 itself is directed elsewhere)',
   all(bvals[N] > 0 for N in range(2, 17)) and bvals[17] < 0, [s(bvals[N], 6) for N in (2, 16, 17)])

# ---------------------------------------------------------------- G.13 lambda_1 and the balanced identity
mp.dps = 30
lam1 = 1 + euler / 2 - log(4 * pi) / 2
xi = lambda z: z * (z - 1) / 2 * pi ** (-z / 2) * mpmath.gamma(z / 2) * zeta(z)
d1 = mpmath.diff(xi, mpf(1), h=mpf('1e-10')) / xi(mpf(1) + mpf('1e-25'))
ck('96A.9', "xi'/xi(1) = lambda_1 = 1 + gamma/2 - log(4 pi)/2 (Davenport's -B)", abs(d1 - lam1) < mpf(10) ** -15, s(d1, 20))
ck('96A.9', 'balanced identity (log 2pi - gamma) + 2 lambda_1 = 2 - log 2', abs((log(2 * pi) - euler) + 2 * lam1 - (2 - log(2))) < mpf(10) ** -28)
mp.dps = 20
zs = [mpmath.zetazero(n).imag for n in range(1, 101)]
part = sum(1 / (mpf(1) / 4 + t * t) for t in zs)
Tm = (zs[-1] + mpmath.zetazero(101).imag) / 2
approx = part + (log(Tm / (2 * pi)) + 1) / (2 * pi * Tm)
ck('96A.9', 'first 100 zeros + smooth tail reproduce lambda_1 to 1e-5 (numerical)', abs(approx - lam1) < 1e-5, s(approx, 10))

# ---------------------------------------------------------------- certified block (Arb)
cert = {}
try:
    import flint
    from flint import arb, acb, ctx
    ctx.prec = 256
    lam1_arb = 1 + arb.const_euler() / 2 - (4 * arb.pi()).log() / 2
    r1 = acb.zeta_zero(1); r2 = acb.zeta_zero(2)
    g1 = r1.imag; g2 = r2.imag
    q1 = arb(1) / 4 + g1 * g1; q2 = arb(1) / 4 + g2 * g2
    C0 = q2 * (lam1_arb - 1 / q1)
    H = arb('3000175332800')
    Cup = C0 + q2 * lam1_arb / (2 * H * H)
    E = (2 * arb.pi()).log() - arb.const_euler()
    cert = {'python_flint': flint.__version__, 'prec_bits': 256,
            'lambda_1': lam1_arb.str(30, radius=True), 'q_1': q1.str(30, radius=True), 'q_2': q2.str(30, radius=True),
            'q1_over_q2': (q1 / q2).str(20, radius=True), 'C0': C0.str(25, radius=True), 'C_upper_with_H': Cup.str(25, radius=True),
            'C_times_ratio_cubed_upper': (Cup * (q1 / q2) ** 3).str(15, radius=True),
            'log2pi_minus_gamma': E.str(30, radius=True),
            'zero_real_parts_are_one_half': [r1.real.str(10), r2.real.str(10)]}
    ck('CERT', 'lambda_1 enclosure inside the printed decimal 0.0230957089661...',
       lam1_arb > arb('0.02309570896612') and lam1_arb < arb('0.02309570896613'), cert['lambda_1'])
    ck('CERT', 'q_1 enclosure consistent with printed 200.0404548323868594...',
       q1 > arb('200.04045483238685') and q1 < arb('200.04045483238687'), cert['q_1'])
    ck('CERT', 'q_2 enclosure consistent with printed 442.1761...', q2 > arb('442.176') and q2 < arb('442.177'), cert['q_2'])
    ck('CERT', 'q_1/q_2 consistent with printed 0.4523999...', (q1 / q2) > arb('0.4523999') and (q1 / q2) < arb('0.4524'), cert['q1_over_q2'])
    ck('CERT', 'printed bounds 8.00193804616020 <= C <= 8.00193804616021 hold via C0 <= C <= C0 + q2*lambda1/(2H^2), (12.7a)',
       C0 > arb('8.00193804616020') and Cup < arb('8.00193804616021'), cert['C0'] + ' / ' + cert['C_upper_with_H'])
    tail = q2 * lam1_arb / (2 * H * H)
    ck('CERT', 'tail term q2*lambda1/(2H^2) < 6e-25 (printed)', tail < arb('6e-25'), tail.str(5, radius=True))
    ck('CERT', 'C (q1/q2)^3 lies in (0.740, 0.742) (printed 0.741)',
       (C0 * (q1 / q2) ** 3) > arb('0.740') and (Cup * (q1 / q2) ** 3) < arb('0.742'), cert['C_times_ratio_cubed_upper'])
    ck('CERT', 'C (q1/q2)^2 lies in (1.63, 1.65) (printed 1.64)',
       (C0 * (q1 / q2) ** 2) > arb('1.63') and (Cup * (q1 / q2) ** 2) < arb('1.65'), (Cup * (q1 / q2) ** 2).str(10, radius=True))
    ck('CERT', 'Arb returns the two lowest zeros with real part 1/2 (to 1e-50)', abs(r1.real - arb('0.5')) < arb('1e-50') and abs(r2.real - arb('0.5')) < arb('1e-50'))
    # independent numerical cross-check with mpmath (different code base)
    mp.dps = 40
    m1 = mpf(1) / 4 + mpmath.zetazero(1).imag ** 2
    m2 = mpf(1) / 4 + mpmath.zetazero(2).imag ** 2
    ck('CERT', 'mpmath cross-check of q_1, q_2 (40 digits)', abs(float(q1.mid()) - float(m1)) < 1e-12 and abs(float(q2.mid()) - float(m2)) < 1e-12,
       [mpmath.nstr(m1, 25), mpmath.nstr(m2, 25)])
except ImportError as exc:
    ck('CERT', 'python-flint available for the certified block', False, str(exc))

# ---------------------------------------------------------------- classical Faulhaber checks (§R2)
n, a = sp.symbols('n a')
from functools import lru_cache
Sfun = lru_cache(maxsize=None)(lambda p: sp.expand(sp.summation(sp.Symbol('k') ** p, (sp.Symbol('k'), 1, n))))
Tn = n * (n + 1) / 2
ok = True
for m in range(1, 9):
    lhs = 2 ** (m - 1) * Tn ** m
    rhs = sum(comb(m, 2 * j - 1) * Sfun(2 * m - 2 * j + 1) for j in range(1, (m + 1) // 2 + 1))
    ok &= sp.expand(lhs - rhs) == 0
ck('R2.F1', 'inverse Faulhaber: 2^{m-1} T_n^m = sum_j C(m,2j-1) S_{2m-2j+1} (m<=8)', ok)
ok = True
for m in range(1, 8):
    Sodd = Sfun(2 * m + 1)
    P = sp.Poly(sp.simplify(Sodd), n)
    # express S_{2m+1} as polynomial in a = T_n by solving
    coeffs = sp.symbols('p0:%d' % (m + 2))
    Pa = sum(coeffs[i] * a ** i for i in range(m + 2))
    sol = sp.solve(sp.Poly(sp.expand(Pa.subs(a, Tn) - Sodd), n).all_coeffs(), coeffs, dict=True)[0]
    Pa = Pa.subs(sol)
    even = sp.expand((n + sp.Rational(1, 2)) / (2 * m + 1) * sp.diff(Pa, a).subs(a, Tn))
    ok &= sp.expand(even - Sfun(2 * m)) == 0
ck('R2.F2', "Faulhaber's derivative rule S_{2m} = (n+1/2)/(2m+1) * dP_m/da (m<=7)", ok)
N = 12
G = sp.zeros(N, N)
for p in range(N):
    poly = sp.Poly(Sfun(p), n)
    for j in range(N):
        G[p, j] = poly.coeff_monomial(n ** (j + 1))
Ginv = G.inv()
A = sp.Matrix(N, N, lambda p, j: (-1) ** (p - j) * comb(p + 1, j) if j <= p else 0)
ck('R2.F3', 'inverse of the Faulhaber coefficient matrix = signed Pascal rows (-1)^{p-j} C(p+1,j) (12x12)', Ginv == A)
ck('R2.F6', 'n^{p+1} = sum_{j=0}^{p} (-1)^{p-j} C(p+1,j) S_j(n) as polynomials, p=0..12 (S_0(n)=n)',
   all(sp.expand(n ** (p_ + 1) - sum((-1) ** (p_ - j_) * sp.binomial(p_ + 1, j_) * Sfun(j_) for j_ in range(0, p_ + 1))) == 0 for p_ in range(0, 13)))
# Witula et al. (13) with r=1 and B_1 = -1/2 reads 2 n S_1 = 3 S_2 - S_1
ck('R2.F4', '(2.2a) 3 S_2 = (2n+1) T_n is the r=1 case of the product decomposition (13) of Witula et al.',
   sp.expand(2 * n * Sfun(1) - (3 * Sfun(2) - Sfun(1))) == 0 and sp.expand(3 * Sfun(2) - (2 * n + 1) * Tn) == 0)
ck('R2.F5', 'B_k = -k zeta(1-k) for k=2..16', all(sp.bernoulli(k) == -k * sp.zeta(1 - k) for k in range(2, 17)))
# Derby (Math. Gazette 2015): runs of consecutive powers that split evenly start on
# the square rail n^2 (first powers) and on the even-triangular rail T_{2n} (squares)
ck('R5C.D1', 'sum_{j=0}^{n} (n^2+j) = sum_{j=n+1}^{2n} (n^2+j) for n=1..60',
   all(sum(n2 + j for j in range(0, nn + 1)) == sum(n2 + j for j in range(nn + 1, 2 * nn + 1)) for nn in range(1, 61) for n2 in [nn * nn]))
ck('R5C.D2', 'sum_{j=0}^{n} (T_{2n}+j)^2 = sum_{j=n+1}^{2n} (T_{2n}+j)^2 for n=1..60, T_{2n}=n(2n+1)',
   all(sum((t + j) ** 2 for j in range(0, nn + 1)) == sum((t + j) ** 2 for j in range(nn + 1, 2 * nn + 1)) for nn in range(1, 61) for t in [nn * (2 * nn + 1)]))
pp = sp.symbols('p'); nn_ = sp.symbols('n', positive=True, integer=True)
jj = sp.symbols('j', integer=True)
quad_p = sp.expand(sp.summation((pp + jj) ** 2, (jj, 0, nn_)) - sp.summation((pp + jj) ** 2, (jj, nn_ + 1, 2 * nn_)))
ck('R5C.D3', '(TR.4) start is forced: LHS - RHS = p^2 - 2n^2 p - n^2(2n+1) = (p - n(2n+1))(p + n)',
   sp.expand(quad_p - (pp - nn_ * (2 * nn_ + 1)) * (pp + nn_)) == 0)
printed = pp ** 2 + 2 * nn_ ** 2 * pp - nn_ ** 2 * (2 * nn_ + 1)
ck('R5C.D4', 'misprint check: the printed sign (+2n^2 p) does not have p = n(2n+1) as a root',
   sp.expand(printed.subs(pp, nn_ * (2 * nn_ + 1))) != 0, str(sp.factor(printed.subs(pp, nn_ * (2 * nn_ + 1)))))

out = {'script': 'qa/audit_gamma_bridge.py', 'rh_status': 'OPEN', 'seconds': round(time.monotonic() - t0, 2),
       'total': len(checks), 'passed': sum(c['passed'] for c in checks),
       'failed': [c['tag'] + ' ' + c['name'] for c in checks if not c['passed']], 'certified_enclosures': cert, 'checks': checks}
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--output', default='qa/GAMMA_BRIDGE.json'); args = ap.parse_args()
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    outp = Path(args.output); outp = outp if outp.is_absolute() else root / outp
    outp.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=str) + '\n')
    print(json.dumps({k: out[k] for k in ('total', 'passed', 'failed', 'seconds')}, indent=2))
    print(json.dumps(cert, indent=2))
    sys.exit(0 if not out['failed'] else 1)
