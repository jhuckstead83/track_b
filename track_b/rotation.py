import math
from fractions import Fraction

# ============================================================
# Track B Atlas: rotation.py
# Core arithmetic engine for logarithmic rotation numbers
# ============================================================

def frac(x: float) -> float:
    """Returns the fractional part of x in [0, 1)."""
    return x - math.floor(x)

def rotation_number(alpha: float, beta: float) -> float:
    """Calculates rho(alpha; beta) = {log(alpha) / log(beta)}."""
    if alpha <= 0 or beta <= 0 or beta == 1.0:
        raise ValueError("Invalid logarithm arguments: require alpha > 0, beta > 0, beta != 1.")
    return frac(math.log(alpha) / math.log(beta))

def continued_fraction(x: float, max_terms: int = 15, tol: float = 1e-12) -> list[int]:
    """Computes continued-fraction partial quotients for x."""
    coeffs = []
    y = x
    for _ in range(max_terms):
        a = math.floor(y)
        coeffs.append(a)
        remainder = y - a
        if abs(remainder) < tol:
            break
        y = 1.0 / remainder
    return coeffs

def convergents(cf: list[int]) -> list[Fraction]:
    """Generates rational convergents from continued-fraction quotients."""
    convs = []
    p_nm2, p_nm1 = 0, 1
    q_nm2, q_nm1 = 1, 0

    for a in cf:
        p_n = a * p_nm1 + p_nm2
        q_n = a * q_nm1 + q_nm2
        convs.append(Fraction(p_n, q_n))
        p_nm2, p_nm1 = p_nm1, p_n
        q_nm2, q_nm1 = q_nm1, q_n

    return convs

def best_rational_approximation(rho: float, q_max: int) -> dict:
    """
    Scans denominators up to q_max to find the best rational carrier.
    Returns the spectral fingerprint metrics for the carrier.
    """
    best_p, best_q = 0, 1
    min_err = float("inf")

    for q in range(1, q_max + 1):
        p = round(rho * q)
        err = abs(rho - p / q)
        if err < min_err:
            min_err = err
            best_p, best_q = p, q

    # Guard against microscopic floating-point error
    if min_err < 1e-15:
        min_err = 0.0

    delta = rho - (best_p / best_q)
    n_lock = float("inf") if min_err == 0 else 1.0 / min_err

    return {
        "p": best_p,
        "q": best_q,
        "approx": best_p / best_q,
        "delta": delta,
        "abs_error": min_err,
        "n_lock": n_lock,
    }
