import dagster as dg
import pandas as pd

# Digital advertising cost benchmarks per UAC field of study.
# Base: WordStream 2025 Education industry average ($6.23 USD CPC ≈ $9.50 AUD).
# Field-level adjustments estimated from relative competition intensity and
# audience size. These are directional benchmarks, not precise market rates.
_BENCHMARKS = [
    ("Agriculture, Environmental & Related Studies", 7.20, 95.00, 3.8, "WordStream 2025 + AU field estimate"),
    ("Architecture & Building", 8.50, 110.00, 3.5, "WordStream 2025 + AU field estimate"),
    ("Creative Arts", 6.80, 85.00, 4.2, "WordStream 2025 + AU field estimate"),
    ("Education", 8.00, 100.00, 3.6, "WordStream 2025 + AU field estimate"),
    ("Engineering & Related Technologies", 9.50, 125.00, 3.2, "WordStream 2025 + AU field estimate"),
    ("Food, Hospitality & Personal Services", 6.50, 80.00, 4.0, "WordStream 2025 + AU field estimate"),
    ("Health", 10.50, 140.00, 3.0, "WordStream 2025 + AU field estimate"),
    ("Information Technology", 11.00, 145.00, 2.9, "WordStream 2025 + AU field estimate"),
    ("Management & Commerce", 9.80, 130.00, 3.1, "WordStream 2025 + AU field estimate"),
    ("Natural & Physical Sciences", 7.50, 95.00, 3.7, "WordStream 2025 + AU field estimate"),
    ("Society & Culture", 7.00, 90.00, 4.0, "WordStream 2025 + AU field estimate"),
]


@dg.asset(
    group_name="reference_data",
    tags={"source": "manual", "domain": "ad_costs", "update_frequency": "annual", "ingestion": "manual"},
    kinds={"python"},
)
def ad_cost_benchmarks(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """Digital advertising cost benchmarks by UAC field of study.

    Source: Estimated from WordStream 2025 Education industry benchmarks
        ($6.23 USD CPC average) with Australian market adjustments per field.
        CPC and CPL adjusted for relative competition intensity (Health/IT
        highest, Creative Arts/Agriculture lowest).
    Marketing use: **What message** — enables ROI-adjusted field recommendations.
        "Engineering has a +12% opportunity gap AND lower CPC than Business"
        helps allocate campaign budgets where demand gaps are cheapest to address.
    Format: uac_field_of_study, estimated_cpc_aud, estimated_cpl_aud,
        estimated_ctr_pct, source_note
    Limitations:
    - Estimates, not actuals — real costs vary by campaign, creative, and targeting
    - Based on US industry averages adjusted to AUD with field-level estimates
    - Should be replaced with actual campaign data when available
    - Updated manually — check WordStream/SpyFu for latest benchmarks annually
    """
    df = pd.DataFrame(
        _BENCHMARKS,
        columns=[
            "uac_field_of_study",
            "estimated_cpc_aud",
            "estimated_cpl_aud",
            "estimated_ctr_pct",
            "source_note",
        ],
    )

    context.log.info(f"Loaded {len(df)} ad cost benchmarks")

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "avg_cpc": dg.MetadataValue.float(float(df["estimated_cpc_aud"].mean())),
        "avg_cpl": dg.MetadataValue.float(float(df["estimated_cpl_aud"].mean())),
        "preview": dg.MetadataValue.md(
            df.to_markdown(index=False, floatfmt=".2f")
        ),
    })

    return df
