import os
import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Track B Atlas: figures.py
# Automated plotting for sawtooth, polar anatomy, and case cards
# ============================================================

DEFAULT_DPI = 220

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def pair_slug(alpha_name: str, beta_name: str) -> str:
    return f"{alpha_name}_vs_{beta_name}"

def _add_polar_panel(ax, rho: float, p: int, q: int, n_vals: np.ndarray, title: str):
    x_vals = (n_vals * rho) % 1.0
    angles = 2.0 * np.pi * x_vals
    radius = np.ones_like(angles)

    spoke_angles = 2.0 * np.pi * np.arange(q) / q
    for theta in spoke_angles:
        ax.plot([theta, theta], [0, 1.08], linestyle="--", linewidth=0.9, alpha=0.45)

    sc = ax.scatter(
        angles, radius, c=n_vals, s=14, alpha=0.85,
        edgecolors="none", cmap="plasma", zorder=3,
    )

    ax.set_ylim(0, 1.1)
    ax.set_yticklabels([])
    ax.set_xticks(spoke_angles)

    if q <= 10:
        ax.set_xticklabels([f"{k}/{q}" for k in range(q)], fontsize=7)
    else:
        ax.set_xticklabels([])

    ax.grid(alpha=0.25)
    ax.set_title(title, fontsize=9, pad=11)
    return sc

def plot_case_card(
    alpha_name: str, beta_name: str, rho: float, p: int, q: int,
    delta: float, n_lock: float, tau_scaled: float,
    output_path: str | None = None, dpi: int = DEFAULT_DPI,
):
    from dynamics import build_anatomy_windows, carrier_phase_error
    
    windows = build_anatomy_windows(n_lock)
    n_crystal = windows["Crystal"]
    n_post = windows["PostCrk"]

    fig = plt.figure(figsize=(11, 8.5))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.0], width_ratios=[1.35, 1.0, 1.0])

    # Sawtooth
    ax_saw = fig.add_subplot(gs[:, 0])
    t_max = 1.6
    if np.isinf(n_lock):
        # Surrogate window for infinite/permanent locks (The Flatline)
        t_vals = np.linspace(0.0, t_max, 100)
        eps = np.zeros_like(t_vals)
    else:
        n_samples = 2200
        t_vals = np.linspace(0.0, t_max, n_samples)
        n_vals = np.maximum(1, np.round(t_vals * n_lock).astype(int))
        eps = carrier_phase_error(rho, p, q, n_vals)

    ax_saw.plot(t_vals, eps, linewidth=2.0)
    ax_saw.axhline(0.5, linestyle="--", linewidth=1, alpha=0.5)
    ax_saw.axvspan(0.0, 0.1, alpha=0.06)
    ax_saw.axvspan(0.9, 1.1, alpha=0.06)
    ax_saw.axvspan(1.2, 1.5, alpha=0.06)
    ax_saw.set_xlim(0, t_max)
    ax_saw.set_ylim(0, 0.55)
    ax_saw.set_xlabel(r"Normalized iteration $n/N_{\mathrm{lock}}$")
    ax_saw.set_ylabel(r"Carrier-tracking error $\epsilon_n$")
    ax_saw.set_title("Torus-sawtooth dephasing", fontsize=11)
    ax_saw.grid(True, alpha=0.25)

    # Crystal polar
    ax_pol1 = fig.add_subplot(gs[0, 1], projection="polar")
    _add_polar_panel(ax_pol1, rho, p, q, n_crystal, f"Crystal\n1 <= n <= {n_crystal[-1]}")

    # Post-crack polar
    ax_pol2 = fig.add_subplot(gs[0, 2], projection="polar")
    if len(n_post) > 0:
        sc = _add_polar_panel(ax_pol2, rho, p, q, n_post, f"Post-Crack\n{n_post[0]} <= n <= {n_post[-1]}")
    else:
        ax_pol2.set_axis_off()
        sc = None

    # Text summary box
    ax_text = fig.add_subplot(gs[1, 1:])
    ax_text.axis("off")

    summary = (
        f"Pair: {alpha_name} vs {beta_name}\n"
        f"rho = {rho:.12f}\n"
        f"carrier = {p}/{q}\n"
        f"delta = {delta:.6e}\n"
        f"N_lock = {n_lock:.2f}\n"
        f"tau_scaled = {tau_scaled:.4f}\n"
        f"Crystal window: 1 to {n_crystal[-1]}\n"
        + (f"Post-Crack window: {n_post[0]} to {n_post[-1]}" if len(n_post) > 0 else "Post-Crack window: unavailable")
    )
    ax_text.text(0.02, 0.98, summary, va="top", ha="left", fontsize=11, family="monospace")

    if sc is not None:
        cbar = fig.colorbar(sc, ax=ax_pol2, fraction=0.046, pad=0.08)
        cbar.set_label("Iteration n", rotation=270, labelpad=14)
        cbar.ax.tick_params(labelsize=8)

    fig.suptitle(f"Atlas Case Card: {alpha_name} vs {beta_name}", fontsize=14, y=0.98)
    fig.subplots_adjust(top=0.90, hspace=0.35, wspace=0.28)

    if output_path is not None:
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        fig.savefig(output_path.replace(".png", ".pdf"), bbox_inches="tight")
    return fig

def batch_case_cards(atlas_df, output_dir: str, top_n: int = 10, sort_by: str = "n_lock", descending: bool = True):
    ensure_dir(output_dir)
    ranked = atlas_df.sort_values(sort_by, ascending=not descending).head(top_n)

    for _, row in ranked.iterrows():
        slug = pair_slug(row["alpha_name"], row["beta_name"])
        out_path = os.path.join(output_dir, f"{slug}_case_card.png")
        fig = plot_case_card(
            alpha_name=row["alpha_name"], beta_name=row["beta_name"],
            rho=float(row["rho"]), p=int(row["best_p"]), q=int(row["best_q"]),
            delta=float(row["delta"]), n_lock=float(row["n_lock"]),
            tau_scaled=float(row["tau_scaled"]), output_path=out_path,
        )
        plt.close(fig)