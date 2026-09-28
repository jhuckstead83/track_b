import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Publication Figures for:
# "Transient Rational Locking in Modular Logarithmic Orbits"
# Final camera-ready version
# ============================================================

def get_rho(alpha: float, beta: float) -> float:
    return (math.log(alpha) / math.log(beta)) % 1.0

def torus_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    diff = np.abs(a - b)
    return np.minimum(diff, 1.0 - diff)

def carrier_phase_error(rho: float, p: int, q: int, n_vals: np.ndarray) -> np.ndarray:
    x_vals = (n_vals * rho) % 1.0
    carrier_vals = (n_vals * p / q) % 1.0
    return torus_distance(x_vals, carrier_vals)

def orbit_points(rho: float, n_vals: np.ndarray) -> np.ndarray:
    return (n_vals * rho) % 1.0

def lock_scale(rho: float, p: int, q: int) -> float:
    delta = rho - (p / q)
    if abs(delta) < 1e-15:
        return float("inf")
    return 1.0 / abs(delta)

CASES = [
    {"label": r"$(e,\pi)\to 7/8$", "alpha": math.e, "beta": math.pi, "p": 7, "q": 8},
    {"label": r"$(\sqrt{2},\pi)\to 3/10$", "alpha": math.sqrt(2), "beta": math.pi, "p": 3, "q": 10},
    {"label": r"$(\log 2,\pi)\to 17/25$", "alpha": math.log(2), "beta": math.pi, "p": 17, "q": 25},
]
for case in CASES:
    case["rho"] = get_rho(case["alpha"], case["beta"])
    case["delta"] = case["rho"] - case["p"] / case["q"]
    case["n_lock"] = lock_scale(case["rho"], case["p"], case["q"])

def make_figure1_sawtooth(output_path="figure1_sawtooth.png", dpi=300):
    fig, ax = plt.subplots(figsize=(10, 6.5))
    t_max = 1.6
    n_samples = 2500
    t_vals = np.linspace(0.0, t_max, n_samples)

    styles = [
        {"lw": 2.5, "zorder": 4, "alpha": 0.90},
        {"lw": 2.0, "zorder": 3, "alpha": 0.85},
        {"lw": 1.5, "zorder": 2, "alpha": 0.80},
    ]

    for idx, case in enumerate(CASES):
        n_lock = case["n_lock"]
        n_vals = np.maximum(1, np.round(t_vals * n_lock).astype(int))
        eps = carrier_phase_error(case["rho"], case["p"], case["q"], n_vals)
        legend_label = (
            f"{case['label']}   "
            f"$\\delta={case['delta']:.3e}$, "
            f"$N_{{\\mathrm{{lock}}}}\\approx {case['n_lock']:.0f}$"
        )
        ax.plot(
            t_vals, eps,
            linewidth=styles[idx]["lw"], alpha=styles[idx]["alpha"],
            zorder=styles[idx]["zorder"], label=legend_label,
        )

    ax.axhline(0.5, linestyle="--", linewidth=1, alpha=0.5, color="gray")
    ax.axvspan(0.0, 0.1, color="steelblue", alpha=0.06)
    ax.axvspan(0.9, 1.1, color="slategray", alpha=0.06)
    ax.axvspan(1.2, 1.5, color="indianred", alpha=0.06)

    ax.text(0.05, 0.515, "Crystal", fontsize=10, color="dimgray")
    ax.text(1.00, 0.515, "Transit", fontsize=10, color="dimgray", ha="center")
    ax.text(1.35, 0.515, "Post-Crack", fontsize=10, color="dimgray", ha="center")

    ax.set_xlim(0, t_max)
    ax.set_ylim(0, 0.55)
    ax.set_xlabel(r"Normalized iteration $n/N_{\mathrm{lock}}$", fontsize=11)
    ax.set_ylabel(r"Carrier-tracking error $\epsilon_n = \|n\delta\|_{\mathbb{T}}$", fontsize=11)
    ax.set_title("Figure 1. Torus-sawtooth dephasing law for the empirical trio", fontsize=13)
    ax.grid(True, alpha=0.25)

    ax.legend(frameon=False, fontsize=10, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1)
    fig.subplots_adjust(bottom=0.25)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    fig.savefig(output_path.replace(".png", ".pdf"), bbox_inches="tight")
    plt.close(fig)

def _add_polar_panel(ax, rho, p, q, n_vals, panel_title):
    x_vals = orbit_points(rho, n_vals)
    angles = 2 * np.pi * x_vals
    radius = np.ones_like(angles)
    spoke_angles = 2 * np.pi * np.arange(q) / q
    for theta in spoke_angles:
        ax.plot([theta, theta], [0, 1.08], linestyle="--", linewidth=1.0, alpha=0.5)

    sc = ax.scatter(
        angles, radius, c=n_vals, s=12, alpha=0.85,
        edgecolors="none", zorder=3, cmap="plasma"
    )
    ax.set_ylim(0, 1.1)
    ax.set_yticklabels([])
    ax.set_xticks(spoke_angles)
    if q <= 10:
        ax.set_xticklabels([f"{k}/{q}" for k in range(q)], fontsize=8)
    else:
        ax.set_xticklabels([])
    ax.grid(alpha=0.25)
    ax.set_title(panel_title, fontsize=9, pad=12)
    return sc

def make_figure2_polar(output_path="figure2_polar_trio.png", dpi=300):
    fig, axes = plt.subplots(3, 2, figsize=(11, 14), subplot_kw={"projection": "polar"})
    for row, case in enumerate(CASES):
        rho = case["rho"]
        p = case["p"]
        q = case["q"]
        n_lock = case["n_lock"]
        n_crystal = np.arange(1, max(50, int(0.1 * n_lock)) + 1)
        n_post = np.arange(int(1.2 * n_lock), int(1.5 * n_lock) + 1)

        left_title = f"{case['label']}\nCrystal: 1 <= n <= {n_crystal[-1]}"
        right_title = f"{case['label']}\nPost-Crack: {n_post[0]} <= n <= {n_post[-1]}"

        _add_polar_panel(axes[row, 0], rho, p, q, n_crystal, left_title)
        sc2 = _add_polar_panel(axes[row, 1], rho, p, q, n_post, right_title)

        cbar = fig.colorbar(sc2, ax=axes[row, 1], fraction=0.038, pad=0.07)
        cbar.set_label("Iteration n", rotation=270, labelpad=13)
        cbar.ax.tick_params(labelsize=8)

    fig.suptitle("Figure 2. Dual-window polar projections", fontsize=14, y=0.96, fontweight="bold")
    fig.subplots_adjust(top=0.90, bottom=0.05, hspace=0.45, wspace=0.25)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    fig.savefig(output_path.replace(".png", ".pdf"), bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    make_figure1_sawtooth("figure1_sawtooth.png", dpi=300)
    make_figure2_polar("figure2_polar_trio.png", dpi=300)
    print("Saved publication figures.")
