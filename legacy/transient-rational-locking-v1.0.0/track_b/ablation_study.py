import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from modulus import commensurability_mismatch

# ============================================================
# Track B Atlas: ablation_study.py
# Tests the hypothesis that Ghost-ness is extrinsic by
# varying the rendering lens against fixed torus dynamics.
# ============================================================

COMPOSITE_LENSES = [120, 180, 240, 360, 420, 480, 540, 600, 720, 840, 900, 960, 990]

def classify_under_new_lens(q: int, delta: float, best_mu: float) -> str:
    if q <= 10 and best_mu < 1e-9:
        return "CATHEDRAL SQUARE"
    if q >= 15 and best_mu < 1e-9 and abs(delta) < 1e-4:
        return "BEHEMOTH"
    if q >= 15 and best_mu >= 0.1:
        return "GHOST"
    return "STANDARD TRANSIENT"

def candidate_moduli(m_max: int, composite_only: bool = False) -> list[int]:
    if composite_only:
        return [m for m in COMPOSITE_LENSES if m <= m_max]
    return list(range(1, m_max + 1))

def best_modulus_for_q(q: int, moduli: list[int]) -> tuple[int, float]:
    best_m = moduli[0]
    best_mu = commensurability_mismatch(best_m, q)
    for m in moduli[1:]:
        mu = commensurability_mismatch(m, q)
        if mu < best_mu:
            best_m = m
            best_mu = mu
            if best_mu == 0.0:
                break
    return best_m, best_mu

def run_ablation(
    df: pd.DataFrame,
    moduli: list[int],
    exact_threshold: float = 1e-9,
    mode_label: str = "unrestricted",
    max_modulus: int = 1000,
) -> pd.DataFrame:
    results = []

    for _, row in df.iterrows():
        q = int(row["best_q"])
        delta = float(row["delta"])
        mu_720 = float(row.get("mu_720", 0.5))
        mu_990 = float(row.get("mu_990", 0.5))
        original_mu_ref = min(mu_720, mu_990)

        best_m, best_mu = best_modulus_for_q(q, moduli)
        ablated_archetype = classify_under_new_lens(q, delta, best_mu)

        migrates_to_exact = best_mu < exact_threshold
        migrates_to_better = (best_mu <= 0.25 * original_mu_ref) if original_mu_ref > 0 else False

        notes = "No change"
        if migrates_to_exact:
            notes = "Exact Match"
        elif migrates_to_better:
            notes = "Substantial Improvement"

        results.append({
            "pair": row["pair"],
            "best_p": int(row["best_p"]),
            "best_q": q,
            "delta": delta,
            "n_lock": float(row["n_lock"]),
            "original_archetype": row["archetype"],
            "original_mu_720": mu_720,
            "original_mu_990": mu_990,
            "original_best_mu": original_mu_ref,
            "best_modulus_under_cap": best_m,
            "best_mu_under_cap": best_mu,
            "ablated_archetype": ablated_archetype,
            "ghost_migrates_to_exact": (row["archetype"] == "GHOST") and migrates_to_exact,
            "notes": notes,
            "mode": mode_label,
            "max_modulus": max_modulus,
        })

    return pd.DataFrame(results)

def write_summary(ablation_df: pd.DataFrame, output_dir: str, mode_str: str, m_max: int) -> None:
    ghosts = ablation_df[ablation_df["original_archetype"] == "GHOST"]
    total_ghosts = len(ghosts)
    exact_migrations = int(ghosts["ghost_migrates_to_exact"].sum())
    improved_ghosts = len(ghosts[ghosts["notes"] == "Substantial Improvement"])

    summary = f"""# Ablation Study: Rendering Lens Variation
**Mode:** {mode_str} ($M \\le {m_max}$)

## Core Hypothesis
Ghost-ness is extrinsic to the rendering lens, not intrinsic to the torus orbit.

## Results
* **Total Canonical Ghosts tested:** {total_ghosts}
* **Ghosts migrated to EXACT commensurability ($\\mu = 0$):** {exact_migrations}
* **Ghosts showing substantial improvement:** {improved_ghosts}

## Interpretation
Holding the torus dynamics fixed while varying only the rendering modulus leaves the intrinsic lock scale unchanged but can sharply reduce commensurability mismatch. Any resulting reclassification therefore reflects lens ecology rather than a change in torus mechanics.
"""
    with open(os.path.join(output_dir, "ablation_summary.md"), "w", encoding="utf-8") as f:
        f.write(summary)

def plot_migration(ablation_df: pd.DataFrame, output_path: str) -> None:
    ghosts = ablation_df[ablation_df["original_archetype"] == "GHOST"].copy()
    if len(ghosts) == 0:
        print("No Ghosts found to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        ghosts["best_q"], ghosts["original_best_mu"],
        color="purple", label="Original mismatch", s=60, zorder=3
    )
    ax.scatter(
        ghosts["best_q"], ghosts["best_mu_under_cap"],
        color="gold", label="Optimized mismatch", s=60, zorder=3
    )

    for _, row in ghosts.iterrows():
        ax.annotate(
            "",
            xy=(row["best_q"], row["best_mu_under_cap"]),
            xytext=(row["best_q"], row["original_best_mu"]),
            arrowprops=dict(arrowstyle="->", color="gray", lw=1.4, alpha=0.7),
        )

    ax.set_title("Ghost Migration Under Lens Ablation", fontsize=14)
    ax.set_xlabel("Spatial Resolution (Denominator $q$)", fontsize=12)
    ax.set_ylabel(r"Commensurability mismatch ($\mu$)", fontsize=12)
    ax.set_ylim(-0.05, 0.55)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.savefig(output_path.replace(".png", ".pdf"), bbox_inches="tight")
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Run the lens-variation ablation study.")
    parser.add_argument("--input", type=str, required=True, help="Path to filtered_unique_taxonomy.csv")
    parser.add_argument("--output", type=str, default="quarry_output/ablation_study", help="Output directory")
    parser.add_argument("--max-modulus", type=int, default=1000, help="Maximum modulus to test")
    parser.add_argument("--composite-only", action="store_true", help="Restrict to curated composite lenses")
    parser.add_argument("--exact-threshold", type=float, default=1e-9, help="Tolerance for exact commensurability")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    mode_str = "Curated Composites" if args.composite_only else "Unrestricted"
    mode_label = "composite_only" if args.composite_only else "unrestricted"

    print("==========================================================")
    print(f"[ABLATION STUDY] Loading frozen census from: {args.input}")
    df = pd.read_csv(args.input)

    print(f"[ABLATION STUDY] Search Mode: {mode_str} up to M={args.max_modulus}")
    moduli = candidate_moduli(args.max_modulus, args.composite_only)

    results_df = run_ablation(
        df,
        moduli,
        exact_threshold=args.exact_threshold,
        mode_label=mode_label,
        max_modulus=args.max_modulus,
    )

    out_csv = os.path.join(args.output, "ablation_results.csv")
    results_df.to_csv(out_csv, index=False)

    ghosts_out = os.path.join(args.output, "ghost_migration_only.csv")
    results_df[results_df["ghost_migrates_to_exact"]].to_csv(ghosts_out, index=False)

    write_summary(results_df, args.output, mode_str, args.max_modulus)

    plot_path = os.path.join(args.output, "ghost_migration_plot.png")
    plot_migration(results_df, plot_path)

    print("==========================================================")
    print(f"Ablation complete. Outputs saved to: {args.output}")
    print("==========================================================")

if __name__ == "__main__":
    main()