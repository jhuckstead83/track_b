#!/usr/bin/env python3
"""Second-backend certificate for the global source rungs W_2, ..., W_6.

WHAT IS CERTIFIED  (Technical Dossier Sec. 74A; no zero table, no verified
height, no Riemann hypothesis)

    x = s(s-1),  R = 2s-1,  D_x = R^{-1} D_s,  L = xi'/xi,
    W_k(x) = (-1)^{k-1} D_x^{2k-1} [ x^k L(s)/R ],
    g_k(s) = s^{2k-1} W_k(s(s-1)) / (2k-1)!.

    Part A (continuum):  g_k(s) > theta_k  for every real s in [1,128],
        proved cell by cell on a complete rational partition with an
        outward-rounded Taylor bound; no point sampling is used.
    Part B (tail):  W_k(s(s-1)) > (alpha_k/2) s^{2k} / (2s-1)^{4k-1}
        for every s >= 128, by an exact rational argument.

    Since s |-> s(s-1) maps [1,oo) onto [0,oo), the two parts give
    W_k(x) > 0 for every x > 0, k = 2,...,6.

WHY IT IS A SECOND BACKEND

    The certificate of record for these rungs is evaluated in FLINT/Arb ball
    arithmetic.  This script shares no arithmetic, no special-function code
    and no computer-algebra dependency with it.  It imports nothing outside
    the Python standard library:

      * arithmetic: decimal (libmpdec) in ROUND_FLOOR, upper bounds taken by
        exact negation, so every operation is outward rounded;
      * zeta jet: Euler-Maclaurin (DLMF 25.2.9) with Lehmer's bound on the
        periodic Bernoulli function and Cauchy estimates for the Taylor
        coefficients of the remainder;
      * digamma jet: recurrence plus the Stirling series (DLMF 5.11.2) with
        the classical remainder bound |R_m(w)| <= |B_2m| / (2m (Re w)^{2m});
      * source polynomials, tail: exact integer and Fraction arithmetic.

    libmpdec guarantees correctly rounded +, -, *, / under the context
    rounding mode, and correctly rounded exp and ln to nearest; every exp/ln
    value used here is widened by 100 units in the last place, so a one-ulp
    deviation would not affect any enclosure.

USAGE
    python3 source_rungs_decimal.py --output RECEIPT.json
    python3 source_rungs_decimal.py --rungs 5,6 --digits 100 --degree 24 \
        --output RECEIPT_second.json
"""
import argparse
import decimal
import hashlib
import json
import platform
import sys
import time
from decimal import (Context, Decimal, DivisionByZero, InvalidOperation,
                     Overflow, ROUND_FLOOR, Underflow, setcontext)
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

# --------------------------------------------------------------------------
# 1.  Outward-rounded interval arithmetic over decimal (libmpdec)
# --------------------------------------------------------------------------
PREC = 0
CTX = None
REM_TARGET = None   # enclosures of the special-function remainders must stay below this
DZERO = Decimal(0)
IZERO = (DZERO, DZERO)
IONE = (Decimal(1), Decimal(1))


def init_arith(digits, remainder_target=-40):
    """Install a ROUND_FLOOR context.  Upper bounds are -(floor(-x))."""
    global PREC, CTX, REM_TARGET
    PREC = digits
    REM_TARGET = Decimal(1).scaleb(remainder_target)
    CTX = Context(prec=digits, rounding=ROUND_FLOOR, Emin=-10 ** 9, Emax=10 ** 9,
                  traps=[InvalidOperation, DivisionByZero, Overflow, Underflow])
    setcontext(CTX)


def i_add(a, b):
    return (a[0] + b[0], (a[1].copy_negate() + b[1].copy_negate()).copy_negate())


def i_sub(a, b):
    return (a[0] + b[1].copy_negate(), (a[1].copy_negate() + b[0]).copy_negate())


def i_neg(a):
    return (a[1].copy_negate(), a[0].copy_negate())


def i_mul(a, b):
    al, ah = a
    bl, bh = b
    if al >= 0:
        if bl >= 0:
            return (al * bl, (ah.copy_negate() * bh).copy_negate())
        if bh <= 0:
            return (ah * bl, (al.copy_negate() * bh).copy_negate())
        return (ah * bl, (ah.copy_negate() * bh).copy_negate())
    if ah <= 0:
        if bl >= 0:
            return (al * bh, (ah.copy_negate() * bl).copy_negate())
        if bh <= 0:
            return (ah * bh, (al.copy_negate() * bl).copy_negate())
        return (al * bh, (al.copy_negate() * bl).copy_negate())
    if bl >= 0:
        return (al * bh, (ah.copy_negate() * bh).copy_negate())
    if bh <= 0:
        return (ah * bl, (al.copy_negate() * bl).copy_negate())
    lo = al * bh
    x = ah * bl
    if x < lo:
        lo = x
    hi = (al.copy_negate() * bl).copy_negate()
    y = (ah.copy_negate() * bh).copy_negate()
    if y > hi:
        hi = y
    return (lo, hi)


def i_div(a, b):
    bl, bh = b
    if bl <= 0 <= bh:
        raise ZeroDivisionError('interval divisor contains zero')
    al, ah = a
    if bl > 0:
        lo = al / (bh if al >= 0 else bl)
        hi = (ah.copy_negate() / (bl if ah >= 0 else bh)).copy_negate()
        return (lo, hi)
    return i_div(i_neg(a), i_neg(b))


def i_mag(a):
    """Upper bound for |a| (exact)."""
    n = a[0].copy_negate()
    return n if n > a[1] else a[1]


def i_int(n):
    d = CTX.create_decimal(n)
    u = CTX.create_decimal(-n).copy_negate()
    return (d, u)


def i_frac(q):
    q = Fraction(q)
    num, den = Decimal(q.numerator), Decimal(q.denominator)
    return (num / den, (num.copy_negate() / den).copy_negate())


def _widen(v):
    """Enclose a value known to within 0.5 ulp by widening 100 ulp each way."""
    d = Decimal(1).scaleb(v.adjusted() - PREC + 3)
    return (v - d, (v.copy_negate() - d).copy_negate())


def i_exp(a):
    """exp of an interval; exp is increasing."""
    lo = _widen(a[0].exp())[0]
    hi = _widen(a[1].exp())[1]
    return (lo, hi)


def i_ln(a):
    """ln of a positive interval; ln is increasing."""
    if a[0] <= 0:
        raise ValueError('ln of non-positive interval')
    lo = _widen(a[0].ln())[0]
    hi = _widen(a[1].ln())[1]
    return (lo, hi)


def i_str(a, digits=35):
    """Midpoint +/- radius summary of an enclosure (display only).

    The midpoint is rounded down and the radius up, and the radius is then
    inflated by four units in the last place, so the printed ball still
    contains the enclosure it summarises.
    """
    fl = Context(prec=digits, rounding=ROUND_FLOOR, Emin=-10 ** 9, Emax=10 ** 9)
    ce = Context(prec=digits, rounding=decimal.ROUND_CEILING, Emin=-10 ** 9, Emax=10 ** 9)
    two = Decimal(2)
    mid = fl.divide(fl.add(a[0], a[1]), two)
    rad = ce.divide(ce.subtract(a[1], a[0]), two)
    rad = ce.add(rad, Decimal(4).scaleb(mid.adjusted() - digits + 1))
    return '[%s +/- %s]' % (mid, rad)


# --------------------------------------------------------------------------
# 2.  Truncated power series with interval coefficients
# --------------------------------------------------------------------------
def s_zero(n):
    return [IZERO] * n


def s_add(a, b):
    return [i_add(x, y) for x, y in zip(a, b)]


def s_mul(a, b, n):
    out = [IZERO] * n
    for i in range(min(len(a), n)):
        ai = a[i]
        if ai[0] == 0 and ai[1] == 0:
            continue
        for j in range(min(len(b), n - i)):
            bj = b[j]
            if bj[0] == 0 and bj[1] == 0:
                continue
            out[i + j] = i_add(out[i + j], i_mul(ai, bj))
    return out


def s_mul_linear(a, c0, c1, n):
    """a(t) * (c0 + c1 t), truncated to n coefficients."""
    out = [IZERO] * n
    for i in range(min(len(a), n)):
        ai = a[i]
        if ai[0] == 0 and ai[1] == 0:
            continue
        out[i] = i_add(out[i], i_mul(ai, c0))
        if i + 1 < n:
            out[i + 1] = i_add(out[i + 1], i_mul(ai, c1))
    return out


def s_div_linear(a, c0, c1, n):
    """a(t) / (c0 + c1 t), truncated to n coefficients (c0 must avoid zero)."""
    out = [IZERO] * n
    prev = IZERO
    for i in range(n):
        num = a[i] if i < len(a) else IZERO
        if i:
            num = i_sub(num, i_mul(prev, c1))
        prev = i_div(num, c0)
        out[i] = prev
    return out


def s_div(a, b, n):
    """a(t)/b(t), truncated to n coefficients."""
    out = [IZERO] * n
    b0 = b[0]
    for i in range(n):
        acc = a[i] if i < len(a) else IZERO
        for j in range(1, i + 1):
            bj = b[j]
            if bj[0] == 0 and bj[1] == 0:
                continue
            acc = i_sub(acc, i_mul(bj, out[i - j]))
        out[i] = i_div(acc, b0)
    return out


def s_deriv(a):
    return [i_mul(a[j], i_int(j)) for j in range(1, len(a))]


# --------------------------------------------------------------------------
# 3.  Exact constants: Bernoulli numbers, pi, logarithms
# --------------------------------------------------------------------------
def bernoulli(nmax):
    """B_0..B_nmax as exact Fractions (B_1 = -1/2)."""
    B = [Fraction(1)]
    for m in range(1, nmax + 1):
        s = sum(Fraction(comb(m + 1, j)) * B[j] for j in range(m))
        B.append(-s / (m + 1))
    return B


def _atan_inv(x, eps):
    """Enclosure of arctan(1/x) for integer x >= 2 (alternating series)."""
    total = Fraction(0)
    k = 0
    while True:
        term = Fraction(1, (2 * k + 1) * x ** (2 * k + 1))
        if term < eps:
            break
        total += term if k % 2 == 0 else -term
        k += 1
    return (total, total + term) if k % 2 == 0 else (total - term, total)


def pi_bounds(digits):
    """Rational enclosure of pi by Machin's formula."""
    eps = Fraction(1, 10 ** (digits + 12))
    a = _atan_inv(5, eps / 32)
    b = _atan_inv(239, eps / 8)
    return (16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0])


# --------------------------------------------------------------------------
# 4.  Jets of log F and of psi, with rigorous truncation bounds
# --------------------------------------------------------------------------
class Jets:
    """Euler-Maclaurin/Stirling jet engine for one precision setting.

    EM_N, EM_M       zeta: main sum length and number of Bernoulli terms
    PSI_Z, PSI_M     digamma: recurrence target and Stirling terms
    RHO              radius of the complex disc used for Cauchy estimates
    """

    def __init__(self, digits, em_n=30, em_m=20, psi_z=32, psi_m=30, rho=1):
        self.em_n, self.em_m = em_n, em_m
        self.psi_z, self.psi_m = psi_z, psi_m
        self.rho = Fraction(rho)
        self.B = bernoulli(2 * max(em_m, psi_m) + 2)
        lo, hi = pi_bounds(digits)
        self.pi = (Decimal(lo.numerator) / Decimal(lo.denominator),
                   (Decimal(-hi.numerator) / Decimal(hi.denominator)).copy_negate())
        self.log_pi = i_ln(self.pi)
        self.logs = {n: i_ln(i_int(n)) for n in range(2, em_n + 1)}
        self.two_pi = i_mul(i_int(2), self.pi)
        # coefficient tables that do not depend on the expansion point
        self._em_coeff = [i_frac(self.B[2 * j] / factorial(2 * j)
                                * Fraction(em_n) ** (1 - 2 * j))
                          for j in range(1, em_m + 1)]
        self._psi_tab = None

    # ---- zeta / F ---------------------------------------------------------
    def _em_remainder(self, c):
        """Uniform bound for the Taylor coefficients (rho = 1) of the
        Euler-Maclaurin remainder of zeta at any centre in the interval c.

        DLMF 25.2.9 with n = em_m Bernoulli terms has remainder
            -binom(s+2n, 2n+1) int_N^oo Btilde_{2n+1}(x) x^{-s-2n-1} dx,
        and |Btilde_m(x)| <= 2 zeta(m) m!/(2 pi)^m <= 4 m!/(2 pi)^m (Lehmer).
        Hence for Re s >= sigma > -2n
            |R| <= 4 |(s)_{2n+1}| N^{-sigma-2n} / ((2 pi)^{2n+1} (sigma+2n)).
        Cauchy's estimate on |s - centre| = rho bounds every Taylor
        coefficient by the maximum of |R| on that circle, divided by rho^j;
        rho = 1 is used, so the same bound serves for all coefficients.
        """
        n = self.em_m
        rho = self.rho
        # products and powers, all outward rounded
        prod = IONE
        chi = i_add(c, i_frac(rho))
        for i in range(2 * n + 1):
            prod = i_mul(prod, i_add(chi, i_int(i)))
        clo = i_sub(c, i_frac(rho))
        expo = i_add(clo, i_int(2 * n))
        power = i_exp(i_neg(i_mul(expo, self.logs[self.em_n])))
        denom = i_mul(self._pow_int(self.two_pi, 2 * n + 1), expo)
        bound = i_div(i_mul(i_int(4), i_mul(prod, power)), denom)
        return i_mag(bound)

    @staticmethod
    def _pow_int(a, e):
        out = IONE
        for _ in range(e):
            out = i_mul(out, a)
        return out

    def f_series(self, c, n):
        """Taylor coefficients 0..n-1 of F(s) = (s-1) zeta(s) at s = c + t.

        F(s) = (s-1) A(s) + N^{1-s},
        A(s) = sum_{m<=N} m^{-s} - N^{-s}/2
               + sum_{j=1}^{M} B_{2j}/(2j)! (s)_{2j-1} N^{-s-2j+1} + R.
        """
        N = self.em_n
        logN = self.logs[N]
        # m^{-s} = m^{-c} exp(-t log m)
        A = [IZERO] * n
        A[0] = IONE  # the m = 1 term
        eN = None
        for m in range(2, N + 1):
            lm = self.logs[m]
            base = i_exp(i_neg(i_mul(c, lm)))
            coef = base
            A[0] = i_add(A[0], coef)
            for j in range(1, n):
                coef = i_div(i_mul(coef, i_neg(lm)), i_int(j))
                A[j] = i_add(A[j], coef)
            if m == N:
                eN = [base]
                coef = base
                for j in range(1, n):
                    coef = i_div(i_mul(coef, i_neg(logN)), i_int(j))
                    eN.append(coef)
        # Bernoulli block: (sum_j c_j (s)_{2j-1} - 1/2) * N^{-s}
        block = [i_frac(Fraction(-1, 2))] + [IZERO] * (n - 1)
        poch = [c, IONE] + [IZERO] * (n - 2)  # (s)_1 = s
        for j in range(1, self.em_m + 1):
            if j > 1:
                poch = s_mul_linear(poch, i_add(c, i_int(2 * j - 3)), IONE, n)
                poch = s_mul_linear(poch, i_add(c, i_int(2 * j - 2)), IONE, n)
            cj = self._em_coeff[j - 1]
            for i in range(n):
                p = poch[i]
                if p[0] == 0 and p[1] == 0:
                    continue
                block[i] = i_add(block[i], i_mul(cj, p))
        A = s_add(A, s_mul(block, eN, n))
        rem = self._em_remainder(c)
        if rem > REM_TARGET:
            raise AssertionError('Euler-Maclaurin remainder too large: %s' % rem)
        remi = (rem.copy_negate(), rem)
        A = [i_add(a, remi) for a in A]
        F = s_mul_linear(A, i_sub(c, IONE), IONE, n)
        F[0] = i_add(F[0], i_mul(i_int(N), eN[0]))
        for j in range(1, n):
            F[j] = i_add(F[j], i_mul(i_int(N), eN[j]))
        return F, rem

    # ---- digamma ----------------------------------------------------------
    def _psi_tables(self, n):
        """Rational coefficient tables for the Stirling part (cached)."""
        if self._psi_tab is not None and self._psi_tab[0] >= n:
            return self._psi_tab[1][:n]
        m = self.psi_m
        tab = []
        for j in range(n):
            terms = []
            # d^j of log w at w = w0 + t/2:  (-1)^{j+1}/(j 2^j) * w0^{-j}
            if j >= 1:
                terms.append((j, Fraction((-1) ** (j + 1), j * 2 ** j)))
            # -1/(2w): -(1/2) (-1/2)^j w0^{-(j+1)}
            terms.append((j + 1, Fraction((-1) ** (j + 1), 2 ** (j + 1))))
            # -sum_i B_{2i}/(2i) w^{-2i}
            for i in range(1, m):
                cf = -self.B[2 * i] / (2 * i) * Fraction(comb(2 * i + j - 1, j)) \
                     * Fraction((-1) ** j, 2 ** j)
                terms.append((2 * i + j, cf))
            tab.append([(e, i_frac(cf)) for e, cf in terms])
        self._psi_tab = (n, tab)
        return tab

    def psi_half_series(self, c, n):
        """Taylor coefficients 0..n-1 of psi(s/2) at s = c + t."""
        z0 = i_div(c, i_int(2))
        shift = 0
        zlo = z0[0]
        while zlo + shift < self.psi_z:
            shift += 1
        w0 = i_add(z0, i_int(shift))
        v = i_div(IONE, w0)
        emax = 2 * self.psi_m + n + 2
        pw = [IONE]
        for _ in range(emax):
            pw.append(i_mul(pw[-1], v))
        out = [IZERO] * n
        for j, row in enumerate(self._psi_tables(n)):
            acc = IZERO
            for e, cf in row:
                acc = i_add(acc, i_mul(cf, pw[e]))
            out[j] = acc
        out[0] = i_add(out[0], i_ln(w0))
        # Stirling remainder, Cauchy estimate with rho (in t) -> rho/2 in w
        rew = i_sub(w0, i_frac(self.rho / 2))
        bnd = i_div(i_frac(abs(self.B[2 * self.psi_m]) / (2 * self.psi_m)),
                    self._pow_int(rew, 2 * self.psi_m))
        rem = i_mag(bnd)
        if rem > REM_TARGET:
            raise AssertionError('Stirling remainder too large: %s' % rem)
        remi = (rem.copy_negate(), rem)
        out = [i_add(a, remi) for a in out]
        # psi(z) = psi(z + shift) - sum_{i<shift} 1/(z+i)
        for i in range(shift):
            a = i_add(z0, i_int(i))
            inv = i_div(IONE, a)
            term = inv
            out[0] = i_sub(out[0], term)
            for j in range(1, n):
                term = i_div(i_mul(term, i_neg(inv)), i_int(2))
                out[j] = i_sub(out[j], term)
        return out, rem


# --------------------------------------------------------------------------
# 5.  The completed logarithmic derivative and the rungs
# --------------------------------------------------------------------------
def ell_prime_series(J, c, n):
    """Taylor coefficients 0..n-1 of L(s) = xi'/xi at s = c + t.

    L = 1/s + F'/F + psi(s/2)/2 - log(pi)/2,  F(s) = (s-1) zeta(s),
    which is the pole-free form of 1/s + 1/(s-1) + zeta'/zeta + psi(s/2)/2
    - log(pi)/2.
    """
    F, em_rem = J.f_series(c, n + 1)
    if F[0][0] <= 0:
        raise AssertionError('F(s) enclosure does not stay positive')
    L = s_div(s_deriv(F), F, n)
    inv = i_div(IONE, c)
    term = inv
    L[0] = i_add(L[0], term)
    for j in range(1, n):
        term = i_mul(term, i_neg(inv))
        L[j] = i_add(L[j], term)
    psi, psi_rem = J.psi_half_series(c, n)
    two = i_int(2)
    for j in range(n):
        L[j] = i_add(L[j], i_div(psi[j], two))
    L[0] = i_sub(L[0], i_div(J.log_pi, two))
    return L, em_rem, psi_rem


def rung_series(J, c, k, degree):
    """Taylor coefficients 0..degree of g_k(s) = s^{2k-1} W_k(s(s-1))/(2k-1)!
    at s = c + t, by the repeated source operator R^{-1} D_s."""
    n = degree + 2 * k
    L, em_rem, psi_rem = ell_prime_series(J, c, n)
    # w = x^k L / R
    w = L
    cm1 = i_sub(c, IONE)
    for _ in range(k):
        w = s_mul_linear(w, c, IONE, n)
        w = s_mul_linear(w, cm1, IONE, n)
    R0 = i_sub(i_mul(i_int(2), c), IONE)
    TWO = i_int(2)
    w = s_div_linear(w, R0, TWO, n)
    for _ in range(2 * k - 1):
        w = s_div_linear(s_deriv(w), R0, TWO, len(w) - 1)
    out = w[:degree + 1]
    for _ in range(2 * k - 1):
        out = s_mul_linear(out, c, IONE, degree + 1)
    fac = i_int(factorial(2 * k - 1))
    sign = (-1) ** (k - 1)
    out = [i_div(a, fac) for a in out]
    if sign < 0:
        out = [i_neg(a) for a in out]
    return out, em_rem, psi_rem


# --------------------------------------------------------------------------
# 6.  Exact source polynomials (74A.5)-(74A.6) and the analytic tail
# --------------------------------------------------------------------------
def _rat_str(q, digits):
    """Upper decimal rendering of a positive rational (display only)."""
    c = Context(prec=digits, rounding=decimal.ROUND_CEILING, Emin=-10 ** 9, Emax=10 ** 9)
    return str(c.divide(Decimal(q.numerator), Decimal(q.denominator)))


def p_add(a, b):
    n = max(len(a), len(b))
    return p_trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                   for i in range(n)])


def p_trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def p_scale(a, c):
    return p_trim([c * x for x in a])


def p_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return p_trim(out)


def p_deriv(a):
    return p_trim([i * a[i] for i in range(1, len(a))]) if len(a) > 1 else [0]


def p_pow(a, e):
    out = [1]
    for _ in range(e):
        out = p_mul(out, a)
    return out


def p_shift(a, c):
    """a(c + t) by Horner; exact for integer or Fraction c."""
    out = [0]
    for coef in reversed(a):
        out = p_add(p_mul(out, [c, 1]), [coef])
    return out


POLY_R = [-1, 2]          # R = 2s - 1
POLY_X = [0, -1, 1]       # x = s(s-1)


def source_polynomials(k):
    """C_{k,j} with R^{4k-1} W_k = sum_j C_{k,j}(s) L^{(j)}(s)  (74A.5)-(74A.6).

    The recurrence is the product rule for R^{-1} D_s applied to
    P(s) L^{(j)}(s) R^{-m}: it produces R P' - 2m P and R P (index j+1),
    with m = 1, 3, 5, ..., 4k-3.
    """
    P = [p_pow(POLY_X, k)]
    for r in range(2 * k - 1):
        Q = [[0] for _ in range(len(P) + 1)]
        for j, a in enumerate(P):
            Q[j] = p_add(Q[j], p_add(p_mul(POLY_R, p_deriv(a)),
                                     p_scale(a, -2 * (2 * r + 1))))
            Q[j + 1] = p_add(Q[j + 1], p_mul(POLY_R, a))
        P = Q
    sign = (-1) ** (k - 1)
    C = [p_scale(a, sign) for a in P]
    # structural checks
    assert len(C) == 2 * k
    assert C[-1] == p_scale(p_mul(p_pow(POLY_X, k), p_pow(POLY_R, 2 * k - 1)), sign)
    for j, c in enumerate(C):
        assert len(c) - 1 == 2 * k + j, 'degree of C_%d' % j
    # the completion terms 1/s + 1/(s-1) are annihilated:
    # sum_j C_j (-1)^j j! [s^{-j-1} + (s-1)^{-j-1}] = 0, cleared by s^{2k}(s-1)^{2k}
    acc = [0]
    sm1 = [-1, 1]
    for j, c in enumerate(C):
        w = (-1) ** j * factorial(j)
        acc = p_add(acc, p_scale(p_mul(c, p_mul(p_pow([0, 1], 2 * k - j - 1),
                                                p_pow(sm1, 2 * k))), w))
        acc = p_add(acc, p_scale(p_mul(c, p_mul(p_pow([0, 1], 2 * k),
                                                p_pow(sm1, 2 * k - j - 1))), w))
    assert acc == [0], 'completion terms are not annihilated'
    return C


def operator_identity_checks(k, C):
    """Independent test of (74A.6) on polynomial data.

    For S(x) = x^m, i.e. L(s) = R(s) x^m, the left side is known in closed
    form: (-1)^{k-1} D_x^{2k-1}[x^{k+m}] = (-1)^{k-1} (k+m)!/(k+m-2k+1)!
    x^{m-k+1} when k+m >= 2k-1, and 0 otherwise.
    """
    rows = []
    for m in range(0, 2 * k + 3):
        L = p_mul(POLY_R, p_pow(POLY_X, m))
        lhs = [0]
        d = L
        for j in range(2 * k):
            lhs = p_add(lhs, p_mul(C[j], d))
            d = p_deriv(d)
        e = k + m
        if e >= 2 * k - 1:
            coef = factorial(e) // factorial(e - (2 * k - 1))
            rhs = p_scale(p_mul(p_pow(POLY_R, 4 * k - 1),
                                p_pow(POLY_X, e - (2 * k - 1))),
                          (-1) ** (k - 1) * coef)
        else:
            rhs = [0]
        assert lhs == rhs, 'operator identity failed at k=%d, m=%d' % (k, m)
        rows.append({'test_function': 'S(x) = x^%d' % m, 'identity': True})
    return rows


def exact_tail(k, C, S=128):
    """Exact rational proof of  W_k(s(s-1)) > (alpha/2) s^{2k}/(2s-1)^{4k-1}
    for s >= S, with alpha = lead(B_k)/4.

    Gamma part:  psi(z) = log z - 1/(2z) - E(z),  E(z) = int_0^oo e^{-zt} r(t) dt,
    r(t) = 1/(1-e^{-t}) - 1/t - 1/2 = sum_{n>=1} 2t/(t^2+4 pi^2 n^2) in (0, t/12),
    so |E^{(j)}(z)| <= (j+1)!/(12 z^{j+2}) and, at z = s/2,
        C_j psi^{(j)}(s/2)/2^{j+1}
            = C_j (-1)^{j-1}[(j-1)!/(2 s^j) + j!/(2 s^{j+1})] - err,
        |err| <= |C_j| (j+1)!/(6 s^{j+2}).
    For j = 0 also log(s/(2 pi)) > 2 on s >= 128 (128 > 2 pi e^2 = 46.4...).

    Prime part: Lambda(n) <= log n and (log t)^m t^{-s} decreases for t >= 2,
    so P_j(s) = sum_n Lambda(n)(log n)^j n^{-s} <= 2^{-s} b_{j+1} with
        b_m = (log 2)^m + 2 sum_{r=0}^m m!/(m-r)! (log 2)^{m-r}/(s-1)^{r+1},
    bounded above using log 2 < 7/10 and s >= S.
    """
    eps, sign_cert = [], []
    for c in C:
        sh = p_shift(c, S)
        if all(x >= 0 for x in sh):
            eps.append(1)
        elif all(x <= 0 for x in sh):
            eps.append(-1)
        else:
            raise AssertionError('sign of a source polynomial is not constant on the tail')
        sign_cert.append([str(eps[-1] * x) for x in sh])
    assert eps[0] == 1, 'C_0 must be positive on the tail'

    n0 = 2 * k + 1

    def lift(c, e):
        """c(s) * s^e as a polynomial (e may be negative when divisible)."""
        if e >= 0:
            return [Fraction(x) for x in ([0] * e + list(c))]
        assert all(x == 0 for x in c[:-e]), 'not a polynomial'
        return [Fraction(x) for x in c[-e:]]

    B = lift(C[0], n0)
    B = p_add(B, p_scale(lift(C[0], n0 - 1), Fraction(-1, 2)))
    for j in range(1, 2 * k):
        f = (-1) ** (j - 1)
        B = p_add(B, p_scale(lift(C[j], n0 - j), Fraction(f * factorial(j - 1), 2)))
        B = p_add(B, p_scale(lift(C[j], n0 - j - 1), Fraction(f * factorial(j), 2)))
    for j in range(2 * k):
        B = p_add(B, p_scale(lift(C[j], n0 - j - 2),
                             Fraction(-eps[j] * factorial(j + 1), 6)))
    lead = B[-1]
    assert lead.denominator == 1 and lead > 0
    alpha = int(lead) // 4
    margin = p_add(B, [Fraction(0)] * (n0 + 2 * k) + [Fraction(-alpha)])
    shifted = p_shift(margin, Fraction(S))
    assert all(x >= 0 for x in shifted) and shifted[0] > 0, 'Gamma margin not positive'

    H = Fraction(0)
    term_bounds = []
    log2 = Fraction(7, 10)
    for j, c in enumerate(C):
        d = 2 * k + j
        D = sum(abs(Fraction(a)) * Fraction(S) ** (i - d) for i, a in enumerate(c))
        m = j + 1
        b = log2 ** m + 2 * sum(Fraction(factorial(m), factorial(m - r))
                                * log2 ** (m - r) / Fraction(S - 1) ** (r + 1)
                                for r in range(m + 1))
        H += D * b / Fraction(S) ** (2 * k - 1 - j)
        term_bounds.append({'j': j, 'D': str(D), 'b': str(b)})
    ratio = H * Fraction(S) ** (2 * k - 1) / Fraction(2) ** S / Fraction(alpha)
    assert 0 < ratio < Fraction(1, 2), 'prime part does not stay below half the Gamma margin'
    assert S > 2 * (2 * k) and S * Fraction(69, 100) > 2 * k
    return {
        'k': k, 'domain_s': [str(S), 'infinity'], 'alpha': str(alpha),
        'alpha_rule': 'alpha = lead(B_k)/4',
        'gamma_lower_leading_coefficient': str(lead),
        'tail_lower_bound_W': '(%d/2) s^%d/(2s-1)^%d' % (alpha, 2 * k, 4 * k - 1),
        'source_polynomial_signs': eps,
        'source_polynomials_ascending': [[str(a) for a in c] for c in C],
        'source_sign_certificates_ascending': sign_cert,
        'gamma_margin_shifted_ascending': [str(a) for a in shifted],
        'gamma_margin_coefficients': len(shifted),
        'gamma_margin_all_nonnegative': True,
        'prime_term_bounds': term_bounds, 'H': str(H),
        'prime_gamma_ratio_exact': str(ratio),
        'prime_gamma_ratio_decimal': _rat_str(ratio, 30),
        'ratio_below_one_half': True,
        'completion_annihilated': True,
    }


# --------------------------------------------------------------------------
# 7.  Continuum certificate
# --------------------------------------------------------------------------
THRESHOLD = {2: Fraction(1, 10 ** 5), 3: Fraction(1, 10 ** 8),
             4: Fraction(1, 10 ** 10), 5: Fraction(1, 10 ** 12),
             6: Fraction(1, 10 ** 15)}
SAMPLE_POINTS = [Fraction(1), Fraction(65, 64), Fraction(3, 2), Fraction(2),
                 Fraction(5), Fraction(10), Fraction(32), Fraction(100),
                 Fraction(128)]


def cell_bound(J, left, right, k, degree):
    """Rigorous lower bound for g_k on [left, right] (Taylor with remainder).

    With m the midpoint, r the radius, p_j the enclosed Taylor coefficients at
    m and Q_degree the enclosure of g_k^{(degree)}(xi)/degree! over the whole
    cell, Taylor's theorem with Lagrange remainder gives, for every s in the
    cell,
        g_k(s) >= p_0 - sum_{j=1}^{degree-1} |p_j| r^j - |Q_degree| r^degree.
    """
    mid = Fraction(left + right, 2)
    rad = Fraction(right - left, 2)
    point, em1, ps1 = rung_series(J, i_frac(mid), k, degree)
    whole, em2, ps2 = rung_series(J, i_hull(left, right), k, degree)
    r = i_frac(rad)
    err = IZERO
    rp = IONE
    for j in range(1, degree):
        rp = i_mul(rp, r)
        m = i_mag(point[j])
        if m:
            err = i_add(err, i_mul((m, m), rp))
    rp = i_mul(rp, r)
    m = i_mag(whole[degree])
    err = i_add(err, i_mul((m, m), rp))
    lower = i_sub(point[0], (err[1], err[1]))
    short = Context(prec=25, rounding=ROUND_FLOOR, Emin=-10 ** 9, Emax=10 ** 9)
    return {
        'left': str(left), 'right': str(right),
        'lower_endpoint': str(short.plus(lower[0])),
        '_lower': lower[0],
        '_center': i_str(point[0]),
        '_err': str(err[1]),
        '_rem': max(em1, em2, ps1, ps2),
    }


def i_hull(a, b):
    lo = i_frac(a)[0]
    hi = i_frac(b)[1]
    return (lo, hi)


def initial_mesh(base):
    """Graded starting partition of [1,128]: cell width proportional to s.

    Dyadic blocks [2^i, 2^{i+1}] carry cells of width base * 2^i, so every
    endpoint is an exact dyadic rational and the refinement stays exact.
    """
    edges = []
    for i in range(7):
        a, b = Fraction(2 ** i), Fraction(2 ** (i + 1))
        step = base * 2 ** i
        x = a
        while x < b:
            y = min(x + step, b)
            edges.append((x, y))
            x = y
    return edges


def finite_certificate(J, k, degree, base_step, max_depth=24, verbose=False):
    theta = THRESHOLD[k]
    theta_dec = Decimal(theta.numerator) / Decimal(theta.denominator)
    stack = [(a, b, 0) for a, b in reversed(initial_mesh(base_step))]
    accepted, refined, weakest, worst_rem = [], 0, None, Decimal(0)
    t0 = time.monotonic()
    while stack:
        a, b, depth = stack.pop()
        rec = cell_bound(J, a, b, k, degree)
        low = rec.pop('_lower')
        worst_rem = max(worst_rem, rec.pop('_rem'))
        center, err = rec.pop('_center'), rec.pop('_err')
        if low > theta_dec:
            accepted.append(rec)
            if weakest is None or low < weakest[0]:
                weakest = (low, a, b, {'left': str(a), 'right': str(b),
                                       'center_value': center,
                                       'variation_plus_remainder_upper': err,
                                       'lower_endpoint': str(low)})
            if verbose and len(accepted) % 200 == 0:
                print('    k=%d %d cells, at s=%s, %.0fs' %
                      (k, len(accepted), float(b), time.monotonic() - t0), flush=True)
        else:
            refined += 1
            if depth >= max_depth:
                raise AssertionError('unresolved cell k=%d [%s, %s]' % (k, a, b))
            c = Fraction(a + b, 2)
            stack.append((c, b, depth + 1))
            stack.append((a, c, depth + 1))
    accepted.sort(key=lambda r: Fraction(r['left']))
    assert Fraction(accepted[0]['left']) == 1
    assert Fraction(accepted[-1]['right']) == 128
    assert all(Fraction(u['right']) == Fraction(v['left'])
               for u, v in zip(accepted, accepted[1:])), 'partition has a gap'
    assert all(Decimal(r['lower_endpoint']) > theta_dec for r in accepted)
    return {
        'k': k, 'domain_s': ['1', '128'], 'digits': PREC,
        'taylor_degree': degree, 'initial_step': str(base_step),
        'uniform_rational_lower_bound_for_g': str(theta),
        'accepted_cells': len(accepted), 'refined_cells': refined,
        'weakest_cell': weakest[3],
        'largest_special_function_remainder': str(worst_rem),
        'coverage_exact': True, 'all_cells_pass': True,
        'seconds': round(time.monotonic() - t0, 2),
        'cells': accepted,
    }


# --------------------------------------------------------------------------
# 8.  Cross-checks: the two source formulations must agree
# --------------------------------------------------------------------------
def polynomial_form_value(J, C, s0, k, digits_guard=0):
    """g_k(s0) from (74A.6): s^{2k-1}/(2k-1)! * sum_j C_j(s) L^{(j)}(s) / R^{4k-1}."""
    c = i_frac(Fraction(s0))
    n = 2 * k
    L, _, _ = ell_prime_series(J, c, n)
    acc = IZERO
    for j in range(2 * k):
        cj = IZERO
        for a in reversed(C[j]):
            cj = i_add(i_mul(cj, c), i_int(a))
        acc = i_add(acc, i_mul(cj, i_mul(L[j], i_int(factorial(j)))))
    R0 = i_sub(i_mul(i_int(2), c), IONE)
    for _ in range(4 * k - 1):
        acc = i_div(acc, R0)
    for _ in range(2 * k - 1):
        acc = i_mul(acc, c)
    return i_div(acc, i_int(factorial(2 * k - 1)))


def samples(J, k):
    out = []
    for s0 in SAMPLE_POINTS:
        v, _, _ = rung_series(J, i_frac(s0), k, 0)
        out.append({'k': k, 's': str(s0), 'g_k': i_str(v[0], 35)})
    return out


def cross_checks(J, k, C, points=(1, 2, 5, 10, 32, 128)):
    rows = []
    for s0 in points:
        a, _, _ = rung_series(J, i_frac(Fraction(s0)), k, 0)
        b = polynomial_form_value(J, C, s0, k)
        overlap = not (a[0][1] < b[0] or b[1] < a[0][0])
        assert overlap, 'formulations disagree at k=%d, s=%s' % (k, s0)
        assert a[0][0] > 0 and b[0] > 0
        rows.append({'k': k, 's': s0, 'operator_form': i_str(a[0], 30),
                     'polynomial_form': i_str(b, 30), 'overlap': True})
    return rows


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--digits', type=int, default=80)
    ap.add_argument('--degree', type=int, default=20)
    ap.add_argument('--step', type=str, default='1/64',
                    help='initial cell width on [1,2] (graded upward)')
    ap.add_argument('--rungs', type=str, default='2,3,4,5,6')
    ap.add_argument('--em-terms', type=int, default=30)
    ap.add_argument('--em-bernoulli', type=int, default=20)
    ap.add_argument('--psi-shift', type=int, default=32)
    ap.add_argument('--psi-bernoulli', type=int, default=30)
    ap.add_argument('--remainder-exponent', type=int, default=-40,
                    help='the Euler-Maclaurin and Stirling remainder enclosures '
                         'must stay below 10**this (they are propagated either way)')
    ap.add_argument('--skip-continuum', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    init_arith(args.digits, args.remainder_exponent)
    J = Jets(args.digits, args.em_terms, args.em_bernoulli,
             args.psi_shift, args.psi_bernoulli)
    rungs = [int(x) for x in args.rungs.split(',')]
    base = Fraction(args.step)
    started = time.monotonic()
    out = {
        'status': 'RUNNING',
        'certifies': ('g_k(s) = s^(2k-1) W_k(s(s-1))/(2k-1)! > theta_k on [1,128]; '
                      'W_k(s(s-1)) > (alpha_k/2) s^(2k)/(2s-1)^(4k-1) for s >= 128'),
        'backend': 'CPython decimal (libmpdec %s), ROUND_FLOOR directed rounding'
                   % decimal.__libmpdec_version__,
        'independent_of': ['FLINT/Arb', 'MPFR/GMP', 'SymPy', 'mpmath'],
        'modules_imported': sorted({'argparse', 'hashlib', 'json', 'platform', 'sys',
                                    'time', 'decimal', 'fractions', 'math', 'pathlib'}),
        'python': platform.python_version(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'parameters': {'digits': args.digits, 'taylor_degree': args.degree,
                       'initial_step': str(base), 'euler_maclaurin_N': args.em_terms,
                       'euler_maclaurin_M': args.em_bernoulli,
                       'stirling_shift_target': args.psi_shift,
                       'stirling_terms': args.psi_bernoulli,
                       'remainder_target': '1e%d' % args.remainder_exponent,
                       'cauchy_radius': str(J.rho)},
        'source': 'regularized zeta and digamma; no zero-location inputs',
    }
    polys = {}
    out['operator_identity_checks'] = []
    for k in rungs:
        C = source_polynomials(k)
        polys[k] = C
        out['operator_identity_checks'] += [dict(r, k=k)
                                            for r in operator_identity_checks(k, C)]
    print('Exact source polynomials and operator identity: PASS', flush=True)
    out['formulation_cross_checks'] = []
    for k in rungs:
        out['formulation_cross_checks'] += cross_checks(J, k, polys[k])
    print('Operator form vs polynomial form (74A.6): PASS', flush=True)
    out['sample_values'] = []
    for k in rungs:
        out['sample_values'] += samples(J, k)
    out['tail'] = [exact_tail(k, polys[k]) for k in rungs]
    for rec in out['tail']:
        print('Exact tail PASS k=%d alpha=%s ratio=%s' %
              (rec['k'], rec['alpha'], rec['prime_gamma_ratio_decimal']), flush=True)
    out['finite'] = []
    if not args.skip_continuum:
        for k in rungs:
            rec = finite_certificate(J, k, args.degree, base, verbose=args.verbose)
            out['finite'].append(rec)
            print(json.dumps({q: v for q, v in rec.items() if q != 'cells'}), flush=True)
    out['status'] = 'PASS'
    out['elapsed_seconds'] = round(time.monotonic() - started, 2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=1) + '\n')
    print('Saved %s (%.1f s)' % (args.output, out['elapsed_seconds']), flush=True)


if __name__ == '__main__':
    main()
