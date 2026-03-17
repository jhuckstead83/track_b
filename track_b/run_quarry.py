import os
import pandas as pd

from constants import CONSTANTS
from atlas_builder import build_named_pairs, build_atlas, print_ranked_table
from dynamics import evaluate_pair_anatomy
from figures import batch_case_cards

# ============================================================
# Track B Atlas: run_quarry.py
# The Master Orchestrator with Slag Separator Filter
# ============================================================

def enrich_atlas_with_anatomy(atlas_df: pd.DataFrame, tau_soft: float = 0.05) -> pd.DataFrame:
    """Passes the atlas through the dynamics engine to append phase-tracking metrics."""
    print("Running dynamics engine across the atlas...")
    enriched_rows = []

    for _, row in atlas_df.iterrows():
        anatomy = evaluate_pair_anatomy(
            rho=row["rho"],
            p=row["best_p"],
            q=row["best_q"],
            n_lock=row["n_lock"],
            tau_scaled=row["tau_scaled"],
            tau_soft=tau_soft,
        )

        row_dict = row.to_dict()
        for window_name, metrics in anatomy.items():
            for metric_name, value in metrics.items():
                row_dict[f"{window_name}_{metric_name}"] = value

        enriched_rows.append(row_dict)

    return pd.DataFrame(enriched_rows)

def filter_theorem_redundancies(df: pd.DataFrame) -> pd.DataFrame:
    """
    The Slag Separator.
    Drops combinations governed by the Inversion Theorem and Base-Shift Identity.
    """
    filtered = df.copy()

    def is_base_shift_row(r):
        return f"_over_{r['beta_name']}" in r["alpha_name"]

    base_shift_mask = filtered.apply(is_base_shift_row, axis=1)
    filtered = filtered[~base_shift_mask]

    inv_mask = filtered["alpha_name"].str.endswith("_inv") | filtered["alpha_name"].str.startswith("inv_")
    filtered = filtered[~inv_mask]

    dropped = len(df) - len(filtered)
    print(f"[Slag Separator] Dropped {dropped} theorem-redundant pairs.")
    return filtered

def filter_trivial_exact_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops exact / trivial identities that create infinite lock scales and do not
    represent meaningful transient geometry.
    """
    filtered = df.copy()
    trivial_mask = (filtered["abs_error"] == 0) | (filtered["best_q"] <= 1)
    dropped = int(trivial_mask.sum())
    filtered = filtered[~trivial_mask]
    print(f"[Trivial Filter] Dropped {dropped} exact or q<=1 pairs.")
    return filtered

def main():
    output_dir = "quarry_output"
    cards_dir = os.path.join(output_dir, "featured_case_cards")
    os.makedirs(cards_dir, exist_ok=True)

    print("======================================================================")
    print("[SYSTEM] Booting Track B Quarry Master Survey...")
    print("======================================================================")

    names = list(CONSTANTS.keys())
    print(f"Loading {len(names)} constants from registry...")
    pairs = build_named_pairs(names, exclude_same=True, ordered=True)
    print(f"Generated {len(pairs)} ordered pairs for the hopper.")

    base_atlas_df = build_atlas(pairs, q_max=32, cf_terms=10)
    full_atlas_df = enrich_atlas_with_anatomy(base_atlas_df)

    filtered_atlas_df = filter_theorem_redundancies(full_atlas_df)
    filtered_atlas_df = filter_trivial_exact_pairs(filtered_atlas_df)

    master_path = os.path.join(output_dir, "master_atlas_ledger.csv")
    filtered_path = os.path.join(output_dir, "filtered_top50.csv")

    full_atlas_df.sort_values(["n_lock", "best_q"], ascending=[False, True]).to_csv(master_path, index=False)

    top50 = filtered_atlas_df.sort_values(["n_lock", "best_q"], ascending=[False, True]).head(50)
    top50.to_csv(filtered_path, index=False)

    print(f"Saved master ledger to: {master_path}")
    print(f"Saved filtered Top 50 to: {filtered_path}")

    print("\nFILTERED TOP 10 (Unique Skeletons Only)")
    print_ranked_table(filtered_atlas_df, top_n=10, sort_mode="lock")

    print("Generating Case Cards for the top 10 longest-locking unique pairs...")
    batch_case_cards(
        atlas_df=filtered_atlas_df,
        output_dir=cards_dir,
        top_n=10,
        sort_by="n_lock",
        descending=True,
    )

    print(f"[SYSTEM] Run complete. Exhibits saved to '{cards_dir}/'.")

if __name__ == "__main__":
    main()
