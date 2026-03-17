from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import product
from typing import Iterable
import pandas as pd

from constants import CONSTANTS, get_constant
from rotation import rotation_number, continued_fraction, best_rational_approximation

# ============================================================
# Track B Atlas: atlas_builder.py
# Master builder for spectral fingerprint tables
# ============================================================

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

def build_named_pairs(names: Iterable[str], exclude_same: bool = True, ordered: bool = True) -> list[tuple[str, str]]:
    """Build pairs from a list of constant names."""
    names = list(names)

    if ordered:
        pairs = list(product(names, names))
        if exclude_same:
            pairs = [(a, b) for a, b in pairs if a != b]
        return pairs

    pairs = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if exclude_same and i == j:
                continue
            if j <= i:
                continue
            pairs.append((a, b))
    return pairs

def format_cf(cf: list[int]) -> str:
    if not cf:
        return "[]"
    if len(cf) == 1:
        return f"[{cf[0]}]"
    tail = ", ".join(map(str, cf[1:]))
    return f"[{cf[0]}; {tail}]"

def fingerprint_pair(alpha_name: str, beta_name: str, q_max: int = 32, cf_terms: int = 10) -> PairFingerprint:
    """Compute the spectral fingerprint for a single named pair."""
    alpha_value = get_constant(alpha_name)
    beta_value = get_constant(beta_name)

    rho = rotation_number(alpha_value, beta_value)
    cf = continued_fraction(rho, max_terms=cf_terms)
    cf_str = format_cf(cf)
    best = best_rational_approximation(rho, q_max=q_max)

    return PairFingerprint(
        alpha_name=alpha_name,
        beta_name=beta_name,
        alpha_value=alpha_value,
        beta_value=beta_value,
        rho=rho,
        cf_terms=cf_str,
        best_p=best["p"],
        best_q=best["q"],
        best_approx=best["approx"],
        delta=best["delta"],
        abs_error=best["abs_error"],
        n_lock=best["n_lock"],
        tau_scaled=1.0 / (10.0 * best["q"]) if best["q"] > 0 else 0.0,
    )

def build_atlas(pairs: Iterable[tuple[str, str]], q_max: int = 32, cf_terms: int = 10) -> pd.DataFrame:
    """Build a pandas DataFrame of fingerprints for many pairs."""
    rows = []
    for alpha_name, beta_name in pairs:
        fp = fingerprint_pair(alpha_name, beta_name, q_max=q_max, cf_terms=cf_terms)
        rows.append(asdict(fp))

    df = pd.DataFrame(rows)
    df["pair"] = df["alpha_name"] + " / " + df["beta_name"]
    df["carrier"] = df["best_p"].astype(str) + "/" + df["best_q"].astype(str)
    df["abs_delta"] = df["delta"].abs()
    return df

def print_ranked_table(df: pd.DataFrame, top_n: int = 15, sort_mode: str = "lock") -> None:
    """Pretty-print a ranked subset of the atlas."""
    cols = ["pair", "rho", "carrier", "best_q", "delta", "abs_error", "n_lock", "tau_scaled", "cf_terms"]

    if sort_mode == "lock":
        ranked = df.sort_values(["n_lock", "best_q"], ascending=[False, True])[cols].reset_index(drop=True)
        title = f"TOP {top_n} PAIRS BY LONGEST LOCK SCALE"
    else:
        ranked = df.sort_values(["abs_error", "best_q"], ascending=[True, True])[cols].reset_index(drop=True)
        title = f"TOP {top_n} PAIRS BY SMALLEST ERROR"

    ranked = ranked.head(top_n).copy()
    ranked["rho"] = ranked["rho"].map(lambda x: f"{x:.6f}")
    ranked["delta"] = ranked["delta"].map(lambda x: f"{x:.3e}")
    ranked["abs_error"] = ranked["abs_error"].map(lambda x: f"{x:.3e}")
    ranked["n_lock"] = ranked["n_lock"].map(lambda x: f"{x:.1f}" if x != float("inf") else "inf")
    ranked["tau_scaled"] = ranked["tau_scaled"].map(lambda x: f"{x:.4f}")

    print("=" * 110)
    print(title)
    print("=" * 110)
    print(ranked.to_string(index=False))
    print("=" * 110)
