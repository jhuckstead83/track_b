import numpy as np

# ============================================================
# Track B Atlas: modulus.py
# Projection, rendering lenses, and arithmetic amplification
# ============================================================

def lane_projection(x_vals: np.ndarray, M: int) -> np.ndarray:
    """Projects continuous torus points into discrete residue lanes modulo M."""
    if M <= 0:
        raise ValueError("Modulus M must be strictly positive.")
    return np.floor(M * x_vals).astype(int) % M

def carrier_lane_projection(n_vals: np.ndarray, p: int, q: int, M: int) -> np.ndarray:
    """Projects the exact moving rational carrier into discrete residue lanes modulo M."""
    if q <= 0:
        raise ValueError("Denominator q must be strictly positive.")
    ideal_x = (n_vals * p / q) % 1.0
    return lane_projection(ideal_x, M)

def normalized_lane_error(x_vals: np.ndarray, n_vals: np.ndarray, p: int, q: int, M: int) -> float:
    """
    Computes the mean circular lane distance between the actual orbit
    and the ideal carrier, normalized by M to allow cross-modulus comparison.
    """
    if M <= 0 or q <= 0:
        raise ValueError("Modulus M and denominator q must be strictly positive.")
    if len(x_vals) == 0:
        return float("nan")

    actual_lanes = lane_projection(x_vals, M)
    ideal_lanes = carrier_lane_projection(n_vals, p, q, M)

    lane_diff = np.abs(actual_lanes - ideal_lanes)
    circ_lane_diff = np.minimum(lane_diff, M - lane_diff)

    return float(np.mean(circ_lane_diff) / M)

def is_commensurate(M: int, q: int) -> bool:
    """Checks if the modulus M perfectly accommodates the q-sector skeleton."""
    if q <= 0:
        return False
    return M % q == 0

def commensurability_mismatch(M: int, q: int) -> float:
    """
    Returns a soft diagnostic of arithmetic aliasing.
    Range: [0.0, 0.5] where 0.0 = crisp and 0.5 = maximal mismatch.
    """
    if q <= 0:
        return 0.5
    remainder = M % q
    dist_to_nearest = min(remainder, q - remainder)
    return float(dist_to_nearest / q)
