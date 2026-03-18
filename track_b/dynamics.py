import numpy as np

# ============================================================
# Track B Atlas: dynamics.py
# Orbit mechanics, phase-tracking, and window generation
# ============================================================

def orbit_points(rho: float, n_vals: np.ndarray) -> np.ndarray:
    return (n_vals * rho) % 1.0

def torus_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    diff = np.abs(a - b)
    return np.minimum(diff, 1.0 - diff)

def carrier_phase_error(rho: float, p: int, q: int, n_vals: np.ndarray) -> np.ndarray:
    x_vals = orbit_points(rho, n_vals)
    carrier_vals = (n_vals * p / q) % 1.0
    return torus_distance(x_vals, carrier_vals)

def build_anatomy_windows(n_lock: float, max_window_size: int = 50000) -> dict[str, np.ndarray]:
    """Builds evaluation windows, capped to prevent memory overflows on massive locks."""
    if np.isinf(n_lock) or n_lock < 1:
        return {
            "Crystal": np.arange(1, 51),
            "Transit": np.array([], dtype=int),
            "PostCrk": np.array([], dtype=int),
        }

    crystal_end = min(max(50, int(0.1 * n_lock)), max_window_size)

    transit_start = int(0.9 * n_lock)
    transit_end = int(1.1 * n_lock)
    post_start = int(1.2 * n_lock)
    post_end = int(1.5 * n_lock)

    w_transit = np.array([], dtype=int)
    w_post = np.array([], dtype=int)

    # Omit window entirely if it begins beyond the compute cap
    if transit_start <= max_window_size:
        transit_end = min(transit_end, max_window_size)
        if transit_end >= transit_start:
            w_transit = np.arange(transit_start, transit_end + 1)

    if post_start <= max_window_size:
        post_end = min(post_end, max_window_size)
        if post_end >= post_start:
            w_post = np.arange(post_start, post_end + 1)

    return {
        "Crystal": np.arange(1, crystal_end + 1),
        "Transit": w_transit,
        "PostCrk": w_post,
    }

def coherence_from_errors(errors: np.ndarray, tau: float) -> float:
    if len(errors) == 0:
        return 0.0
    return float(np.mean(errors < tau) * 100.0)

def evaluate_pair_anatomy(
    rho: float, p: int, q: int, n_lock: float, tau_scaled: float, tau_soft: float = 0.05
) -> dict:
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