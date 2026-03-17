import math

# ============================================================
# Track B Atlas: constants.py
# Registry of mathematical constants for orbit generation
# ============================================================

CONSTANTS = {
    # Baseline
    "pi": math.pi,
    "e": math.e,
    "phi": (1.0 + math.sqrt(5.0)) / 2.0,
    "sqrt2": math.sqrt(2.0),
    "sqrt3": math.sqrt(3.0),
    "log2": math.log(2.0),

    # Tier 1 / roots / logs / named constants
    "zeta3": 1.202056903159594,
    "catalan": 0.915965594177219,
    "euler_gamma": 0.577215664901532,
    "sqrt5": math.sqrt(5.0),
    "sqrt7": math.sqrt(7.0),
    "sqrt11": math.sqrt(11.0),
    "log3": math.log(3.0),
    "log10": math.log(10.0),

    # Angle / circle family and custom scalar
    "pi_over_2": math.pi / 2.0,
    "pi_over_3": math.pi / 3.0,
    "pi_over_4": math.pi / 4.0,
    "two_pi": 2.0 * math.pi,
    "inv_pi": 1.0 / math.pi,
    "pi_over_sqrt2": math.pi / math.sqrt(2.0),

    # Golden / silver families
    "phi_inv": 2.0 / (1.0 + math.sqrt(5.0)),
    "silver": 1.0 + math.sqrt(2.0),
    "silver_inv": math.sqrt(2.0) - 1.0,

    # Derived / cross-breed constants
    "ln_phi": math.log((1.0 + math.sqrt(5.0)) / 2.0),
    "e_over_pi": math.e / math.pi,
    "pi_over_e": math.pi / math.e,
    "sqrt2_over_pi": math.sqrt(2.0) / math.pi,
    "phi_over_pi": ((1.0 + math.sqrt(5.0)) / 2.0) / math.pi,
}

def get_constant(name: str) -> float:
    if name not in CONSTANTS:
        raise ValueError(f"Constant '{name}' not found in registry.")
    return CONSTANTS[name]
