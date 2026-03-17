import numpy as np

# ============================================================
# Track B Atlas: dynamics.py
# Orbit mechanics, phase-tracking, and window generation
# ============================================================

def orbit_points(rho: float, n_vals: np.ndarray) -> np.ndarray:
    """Generates the exact fractional orbit x_n = {n * rho}."""
    return (n_vals * rho) % 1.0

def torus_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Calculates the shortest distance on the circular torus."""
    diff = np.abs(a - b)
    return np.minimum(diff, 1.0 - diff)

def carrier_phase_error(rho: float, p: int, q: int, n_vals: np.ndarray) -> np.ndarray:
    """
    Computes the exact carrier-tracking error epsilon_n between the orbit
    and the moving rational target {p*n/q}.
    """
    x_vals = orbit_points(rho, n_vals)
    carrier_vals = (n_vals * p / q) % 1.0
    return torus_distance(x_vals, carrier_vals)

def build_anatomy_windows(n_lock: float) -> dict[str, np.ndarray]:
    """
    Generates standardized 'Crystal', 'Transit', and 'PostCrk'
    iteration windows based on the lock scale.
    """
    if np.isinf(n_lock) or n_lock < 1:
        return {
            "Crystal": np.arange(1, 51),
            "Transit": np.array([], dtype=int),
            "PostCrk": np.array([], dtype=int),
        }

    w_crystal = np.arange(1, max(50, int(0.1 * n_lock)) + 1)
    w_transit = np.arange(int(0.9 * n_lock), int(1.1 * n_lock) + 1)
    w_post = np.arange(int(1.2 * n_lock), int(1.5 * n_lock) + 1)

    return {
        "Crystal": w_crystal,
        "Transit": w_transit,
        "PostCrk": w_post,
    }

def coherence_from_errors(errors: np.ndarray, tau: float) -> float:
    """Returns the percentage of errors strictly below threshold tau."""
    if len(errors) == 0:
        return 0.0
    return float(np.mean(errors < tau) * 100.0)

def evaluate_pair_anatomy(
    rho: float,
    p: int,
    q: int,
    n_lock: float,
    tau_scaled: float,
    tau_soft: float = 0.05,
) -> dict:
    """
    Runs a full diagnostic sweep on a given pair across its anatomy windows.
    Returns mean error and lock percentages for scaled and soft thresholds.
    """
    windows = build_anatomy_windows(n_lock)
    results = {}

    for w_name, n_vals in windows.items():
        if len(n_vals) == 0:
            results[w_name] = {
                "n_start": None,
                "n_end": None,
                "count": 0,
                "mean_err": float("nan"),
                "lock_scaled_pct": 0.0,
                "lock_soft_pct": 0.0,
            }
            continue

        errors = carrier_phase_error(rho, p, q, n_vals)

        results[w_name] = {
            "n_start": int(n_vals[0]),
            "n_end": int(n_vals[-1]),
            "count": int(len(n_vals)),
            "mean_err": float(np.mean(errors)),
            "lock_scaled_pct": coherence_from_errors(errors, tau_scaled),
            "lock_soft_pct": coherence_from_errors(errors, tau_soft),
        }

    return results
