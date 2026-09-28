from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import product
from typing import Iterable
import pandas as pd
import json

from constants import CONSTANTS, get_constant
from rotation import rotation_number, continued_fraction, best_rational_approximation
from modulus import commensurability_mismatch

# ============================================================
# Track B Atlas: atlas_builder.py
# Master builder for Canonical Spectral Fingerprints
# ============================================================

STANDARD_MODULI = [120, 360, 720, 840, 990]

@dataclass
class PairFingerprint:
    alpha_name: str
    beta_name: str
    alpha_value: float
    beta_value: float
    rho: float
    cf_terms: str
    best_p: int
    best_q: int
    best_approx: float
    delta: float
    abs_error: float
    n_lock: float
    tau_scaled: float
    
    sym_class: str
    archetype: str
    m_profile_json: str
    
    eq_tags: str = "None"
    canonical_signature: str = ""
    
    mu_120: float = 0.0
    mu_360: float = 0.0
    mu_720: float = 0.0
    mu_840: float = 0.0
    mu_990: float = 0.0

def build_named_pairs(names: Iterable[str], exclude_same: bool = True, ordered: bool = True) -> list[tuple[str, str]]:
    names = list(names)
    if ordered:
        pairs = list(product(names, names))
        if exclude_same:
            pairs = [(a, b) for a, b in pairs if a != b]
        return pairs
    pairs = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if exclude_same and i == j: continue
            if j <= i: continue
            pairs.append((a, b))
    return pairs

def format_cf(cf: list[int]) -> str:
    if not cf: return "[]"
    if len(cf) == 1: return f"[{cf[0]}]"
    tail = ", ".join(map(str, cf[1:]))
    return f"[{cf[0]}; {tail}]"

def infer_symmetry_class(q: int) -> str:
    """Infers the geometric symmetry class from the denominator."""
    if q == 4:
        return "4-fold bilateral"
    return f"{q}-fold rotational"

def classify_archetype(q: int, eps: float, mu_720: float, mu_990: float) -> str:
    """
    Operational classifier for the 720/990 atlas.
    This is a rendering-lens convention, not a universal invariant.
    """
    if q <= 10 and mu_720 < 1e-9:
        return "CATHEDRAL SQUARE"
    if q >= 15 and mu_720 < 1e-9 and abs(eps) < 1e-4:
        return "BEHEMOTH"
    if q >= 15 and mu_990 >= 0.1:
        return "GHOST"
    return "STANDARD TRANSIENT"

def fingerprint_pair(alpha_name: str, beta_name: str, q_max: int = 32, cf_terms: int = 10) -> PairFingerprint:
    alpha_value = get_constant(alpha_name)
    beta_value = get_constant(beta_name)

    rho = rotation_number(alpha_value, beta_value)
    cf = continued_fraction(rho, max_terms=cf_terms)
    cf_str = format_cf(cf)
    best = best_rational_approximation(rho, q_max=q_max)
    
    q = best["q"]
    eps = best["delta"]
    
    # Calculate labeled JSON M-Profile
    mu_vals = {M: commensurability_mismatch(M, q) for M in STANDARD_MODULI}
    m_profile_json = json.dumps({f"mu_{M}": mu_vals[M] for M in STANDARD_MODULI}, separators=(",", ":"))
    
    sym_class = infer_symmetry_class(q)
    archetype = classify_archetype(q, eps, mu_vals[720], mu_vals[990])

    return PairFingerprint(
        alpha_name=alpha_name, beta_name=beta_name,
        alpha_value=alpha_value, beta_value=beta_value,
        rho=rho, cf_terms=cf_str,
        best_p=best["p"], best_q=best["q"], best_approx=best["approx"],
        delta=eps, abs_error=best["abs_error"], n_lock=best["n_lock"],
        tau_scaled=1.0 / (10.0 * q) if q > 0 else 0.0,
        sym_class=sym_class,
        archetype=archetype,
        m_profile_json=m_profile_json,
        mu_120=mu_vals[120], mu_360=mu_vals[360], mu_720=mu_vals[720], 
        mu_840=mu_vals[840], mu_990=mu_vals[990]
    )

def build_atlas(pairs: Iterable[tuple[str, str]], q_max: int = 32, cf_terms: int = 10) -> pd.DataFrame:
    rows = []
    for alpha_name, beta_name in pairs:
        fp = fingerprint_pair(alpha_name, beta_name, q_max=q_max, cf_terms=cf_terms)
        rows.append(asdict(fp))

    df = pd.DataFrame(rows)
    df["pair"] = df["alpha_name"] + " / " + df["beta_name"]
    df["carrier"] = df["best_p"].astype(str) + "/" + df["best_q"].astype(str)
    df["abs_delta"] = df["delta"].abs()
    return df

def print_ranked_table(df: pd.DataFrame, top_n: int = 15) -> None:
    cols = ["pair", "carrier", "n_lock", "mu_720", "mu_990", "archetype", "canonical_signature"]
    ranked = df.sort_values(["n_lock", "best_q"], ascending=[False, True])[cols].reset_index(drop=True)
    
    ranked = ranked.head(top_n).copy()
    ranked["n_lock"] = ranked["n_lock"].map(lambda x: f"{x:.1f}")
    ranked["mu_720"] = ranked["mu_720"].map(lambda x: f"{x:.2f}")
    ranked["mu_990"] = ranked["mu_990"].map(lambda x: f"{x:.2f}")

    print("=" * 140)
    print(f"TOP {top_n} PAIRS: THE TAXONOMY LEDGER")
    print("=" * 140)
    print(ranked.to_string(index=False))
    print("=" * 140)