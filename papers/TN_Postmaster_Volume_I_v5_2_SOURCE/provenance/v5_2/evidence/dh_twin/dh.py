"""Davenport-Heilbronn twin in pure Python (complex floats, no external packages).

f(s) = sum a_n n^-s with a_n periodic mod 5: (a_1..a_5) = (1, k, -k, -1, 0),
k = (sqrt(10-2 sqrt5) - 2)/(sqrt5 - 1).  Equivalently
f = (1-ik)/2 L(s,chi) + (1+ik)/2 L(s,conj chi), chi mod 5 with chi(2)=i (odd).
Completed: F(s) = (5/pi)^(s/2) Gamma((s+1)/2) f(s); expected F(s) = F(1-s).
"""
import cmath, math
from fractions import Fraction

SQ5 = math.sqrt(5)
KAPPA = (math.sqrt(10 - 2 * SQ5) - 2) / (SQ5 - 1)
COEF = {1: 1.0, 2: KAPPA, 3: -KAPPA, 4: -1.0}

def _bernoulli(n):
    B = [Fraction(0)] * (n + 1); B[0] = Fraction(1)
    for m in range(1, n + 1):
        B[m] = -sum(math.comb(m + 1, j) * B[j] for j in range(m)) / (m + 1)
    return B
_B = _bernoulli(80)
B2 = [float(_B[2 * j]) / math.factorial(2 * j) for j in range(41)]  # B_{2j}/(2j)!

def hurwitz(s, a, N=None, M=30):
    """zeta(s, a) for real a > 0 by Euler-Maclaurin."""
    if N is None: N = 40 + int(abs(s.imag) * 0.6)
    tot = 0j
    for n in range(N): tot += (n + a) ** (-s)
    x = N + a
    xs = x ** (-s)
    tot += x ** (1 - s) / (s - 1) + xs / 2
    term = s * xs / x          # s * x^(-s-1)
    for j in range(1, M + 1):
        tot += B2[j] * term
        # next: multiply by (s+2j-1)(s+2j) / x^2
        term *= (s + 2 * j - 1) * (s + 2 * j) / (x * x)
    return tot

def f(s):
    s = complex(s)
    return 5 ** (-s) * sum(c * hurwitz(s, r / 5) for r, c in COEF.items())

def zeta(s):
    return hurwitz(complex(s), 1.0)

def loggamma(z):
    z = complex(z); shift = 0j
    while z.real < 15:
        shift -= cmath.log(z); z += 1
    s = (z - 0.5) * cmath.log(z) - z + 0.5 * math.log(2 * math.pi)
    zp = z; z2 = z * z
    for j in range(1, 20):
        s += float(_B[2 * j]) / (2 * j * (2 * j - 1)) / zp
        zp *= z2
    return s + shift

def logF(s):
    s = complex(s)
    return (s / 2) * math.log(5 / math.pi) + loggamma((s + 1) / 2) + cmath.log(f(s))

def Z(t):
    """Real-valued on the line: e^{i theta(t)} f(1/2+it) with theta from the Gamma factor."""
    s = complex(0.5, t)
    th = ((s / 2) * math.log(5 / math.pi) + loggamma((s + 1) / 2)).imag
    return (cmath.exp(1j * th) * f(s))
