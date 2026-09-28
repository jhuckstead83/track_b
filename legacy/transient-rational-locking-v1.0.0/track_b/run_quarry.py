import os
import pandas as pd

from constants import CONSTANTS
from atlas_builder import build_named_pairs, build_atlas, print_ranked_table
from dynamics import evaluate_pair_anatomy
from figures import batch_case_cards

# ============================================================
# Track B Atlas: run_quarry.py
# The Master Orchestrator (Deterministic Canonical Output)
# ============================================================

def enrich_atlas_with_anatomy(atlas_df: pd.DataFrame, tau_soft: float = 0.05) -> pd.DataFrame:
    print("Running dynamics engine across the atlas...")
    enriched_rows = []
    for _, row in atlas_df.iterrows():
        anatomy = evaluate_pair_anatomy(
            rho=row["rho"], p=row["best_p"], q=row["best_q"],
            n_lock=row["n_lock"], tau_scaled=row["tau_scaled"], tau_soft=tau_soft
        )
        row_dict = row.to_dict()
        for window_name, metrics in anatomy.items():
            for metric_name, value in metrics.items():
                row_dict[f"{window_name}_{metric_name}"] = value
        enriched_rows.append(row_dict)
    return pd.DataFrame(enriched_rows)

def tag_and_filter_redundancies(df: pd.DataFrame, tol: float = 1e-9) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Theorem-aware separator:
    Detects equivalence via rho2 = ±rho1 + k together with matching carrier data,
    then assigns human-readable tags and keeps a deterministic representative.
    """
    df = df.copy()
    df["eq_tags"] = "None"

    # Deterministic representative priority
    df = df.sort_values(
        by=["n_lock", "abs_delta", "best_q", "best_p", "pair"],
        ascending=[False, True, True, True, True]
    ).reset_index(drop=True)

    kept_indices = []
    seen = []

    for idx, row in df.iterrows():
        tag = None

        for prev_idx in seen:
            prev = df.loc[prev_idx]

            same_q = row["best_q"] == prev["best_q"]
            same_abs_delta = abs(abs(row["delta"]) - abs(prev["delta"])) < tol

            same_skeleton = (
                same_q and (
                    row["best_p"] == prev["best_p"] or
                    row["best_p"] == prev["best_q"] - prev["best_p"]
                )
            )

            rho_diff = row["rho"] - prev["rho"]
            rho_sum = row["rho"] + prev["rho"]

            same_class = abs(rho_diff - round(rho_diff)) < tol
            inversion_class = abs(rho_sum - round(rho_sum)) < tol

            if same_skeleton and same_abs_delta and same_class:
                tag = f"Phase-equivalent shadow of {prev['pair']}"
                break

            if same_skeleton and same_abs_delta and inversion_class:
                tag = f"Inversion partner of {prev['pair']}"
                break

        if tag is None:
            kept_indices.append(idx)
            seen.append(idx)
        else:
            df.at[idx, "eq_tags"] = tag

    df["canonical_signature"] = df.apply(
        lambda r: f"C = ({r['best_q']}, {r['delta']:.3e}, {r['m_profile_json']}, {r['sym_class']}, {r['eq_tags']}) | Archetype: {r['archetype']}",
        axis=1
    )

    clean_df = df.loc[kept_indices].copy()
    dropped = len(df) - len(clean_df)
    print(f"[Slag Separator] Tagged {dropped} theorem-redundant pairs via rho-equivalence.")

    return df, clean_df

def main():
    output_dir = "quarry_output"
    cards_dir = os.path.join(output_dir, "featured_case_cards")
    os.makedirs(cards_dir, exist_ok=True)
    
    print("======================================================================")
    print("[SYSTEM] Booting Track B Quarry Canonical Survey...")
    print("======================================================================")
    
    # Intake
    names = list(CONSTANTS.keys())
    print(f"Loading {len(names)} constants from registry...")
    pairs = build_named_pairs(names, exclude_same=True, ordered=True)
    print(f"Generated {len(pairs)} ordered pairs for the hopper.")
    
    # Engine
    base_atlas_df = build_atlas(pairs, q_max=32, cf_terms=10)
    
    # Filter out Permanent Analytical Locks (The Vacuum States)
    base_atlas_df = base_atlas_df[
        (base_atlas_df["best_q"] > 1) & (base_atlas_df["abs_error"] > 1e-15)
    ].copy()
    
    full_atlas_df = enrich_atlas_with_anatomy(base_atlas_df)
    
    # Taxonomic Tagging and Filtering
    full_tagged_df, clean_atlas_df = tag_and_filter_redundancies(full_atlas_df)
    
    # Export
    master_path = os.path.join(output_dir, "master_canonical_ledger.csv")
    filtered_path = os.path.join(output_dir, "filtered_unique_taxonomy.csv")
    
    full_tagged_df.sort_values("n_lock", ascending=False).to_csv(master_path, index=False)
    
    # Preserve the canonical deterministic order for the top 50
    top50 = clean_atlas_df.head(50)
    top50.to_csv(filtered_path, index=False)
    
    print(f"Saved full tagged ledger to: {master_path}")
    print(f"Saved filtered taxonomy to: {filtered_path}\n")
    
    print_ranked_table(clean_atlas_df, top_n=15)
    
    print(f"\nGenerating Case Cards for the top 10 longest-locking unique canonical classes...")
    batch_case_cards(atlas_df=clean_atlas_df, output_dir=cards_dir, top_n=10, sort_by="n_lock", descending=True)
    
    print(f"[SYSTEM] Run complete. Exhibits saved to '{cards_dir}/'.")

if __name__ == "__main__":
    main()