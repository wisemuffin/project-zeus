import time

import dagster as dg
import numpy as np
import pandas as pd
from pytrends_modern import TrendReq

from analytics_au.defs.assets.google_trends_interest import (
    BATCH_DELAY_SECONDS,
    MAX_RETRIES,
    REFERENCE_SEARCH_NAME,
    REFERENCE_UNIVERSITY,
    RETRY_BASE_SECONDS,
    UNIVERSITIES,
    _build_batches,
    _get_search_name,
)


def _fetch_batch_by_state(
    pytrends: TrendReq,
    batch_universities: list[str],
    log: dg.DagsterLogManager,
) -> pd.DataFrame | None:
    """Fetch interest by region (state) for one batch (4 unis + reference).

    Returns a long-format DataFrame with columns: university, search_name,
    state_name, interest. Returns None if all retries are exhausted.
    """
    search_names = [REFERENCE_SEARCH_NAME] + [
        _get_search_name(u) for u in batch_universities
    ]

    for attempt in range(MAX_RETRIES):
        try:
            pytrends.build_payload(search_names, geo="AU", timeframe="today 5-y")
            df = pytrends.interest_by_region(resolution="REGION")
            if df.empty:
                log.warning(f"Empty result for batch: {search_names}")
                return None

            # interest_by_region returns wide format: index=region, columns=keywords
            df = df.reset_index()
            df = df.rename(columns={"geoName": "state_name"})

            # Melt from wide to long format
            df = df.melt(
                id_vars=["state_name"], var_name="search_name", value_name="interest"
            )
            df["interest"] = df["interest"].astype(float)

            # Map search names back to QILT university names
            search_to_qilt = {REFERENCE_SEARCH_NAME: REFERENCE_UNIVERSITY}
            for u in batch_universities:
                search_to_qilt[_get_search_name(u)] = u
            df["university"] = df["search_name"].map(search_to_qilt)

            return df

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BASE_SECONDS * (2**attempt)
                log.warning(
                    f"Batch failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}. "
                    f"Retrying in {wait}s..."
                )
                time.sleep(wait)
            else:
                log.error(
                    f"Batch permanently failed after {MAX_RETRIES} attempts: {e}"
                )
                return None


def _normalize_across_batches_by_state(
    all_data: list[pd.DataFrame],
) -> pd.DataFrame:
    """Normalize state-level interest across batches using the reference keyword.

    Same approach as the time-series normalization: use the reference keyword's
    median per-state values to compute a scale factor per batch, then rescale
    to a single 0-100 range.
    """
    # Compute median interest of reference keyword per batch (across all states)
    ref_medians = []
    for batch_df in all_data:
        ref_rows = batch_df[batch_df["university"] == REFERENCE_UNIVERSITY]
        median_val = ref_rows["interest"].median()
        ref_medians.append(median_val)

    # Use the first batch's reference median as the anchor
    anchor_median = ref_medians[0]

    normalized_parts = []
    for i, batch_df in enumerate(all_data):
        batch_median = ref_medians[i]
        if batch_median > 0:
            scale_factor = anchor_median / batch_median
        else:
            scale_factor = 1.0

        scaled = batch_df.copy()
        scaled["interest"] = scaled["interest"] * scale_factor
        normalized_parts.append(scaled)

    combined = pd.concat(normalized_parts, ignore_index=True)

    # Remove duplicate reference keyword rows (keep only from first batch)
    ref_mask = combined["university"] == REFERENCE_UNIVERSITY
    ref_first_batch = normalized_parts[0][
        normalized_parts[0]["university"] == REFERENCE_UNIVERSITY
    ]
    non_ref = combined[~ref_mask]
    combined = pd.concat([ref_first_batch, non_ref], ignore_index=True)

    # Rescale to 0-100 where 100 = peak interest across all universities/states
    max_interest = combined["interest"].max()
    if max_interest > 0:
        combined["interest"] = (combined["interest"] / max_interest) * 100.0

    combined["interest"] = combined["interest"].round(1)

    return combined


@dg.asset(
    group_name="google_trends",
    tags={
        "source": "google",
        "domain": "search_interest",
        "update_frequency": "monthly",
        "ingestion": "api",
    },
    kinds={"python", "api"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 * *"),
)
def google_trends_interest_by_state(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """Google Trends state-level search interest for 42 Australian universities.

    Source: Google Trends (trends.google.com) via pytrends-modern.
        interest_by_region(resolution='REGION') returns relative search interest
        (0-100) by Australian state/territory for each university name.
        Cross-batch normalized so values are comparable across all universities.
    Marketing use: **Where** — reveals geographic concentration of search demand
        for each university brand. Identifies states where a university is
        well-known vs. unknown, enabling geo-targeted campaign allocation.
        Combined with quality metrics in university_brand_awareness mart to
        find high-quality universities with weak brand presence in specific states.
    Format: university (QILT name, join key), search_name (what was searched),
        state_name (full Google Trends state name), interest (0-100 normalized)
    Limitations:
    - Relative index, not absolute search volume
    - Cross-batch normalization uses University of Melbourne as anchor
    - Acronym searches may capture non-university intent
    - Small states (NT, ACT, TAS) may have noisy/zero signals
    - Single snapshot (no time dimension) — represents ~5-year aggregate
    - ~11 minutes execution time due to rate-limit delays between batches
    """
    pytrends = TrendReq(hl="en-AU", tz=-600)
    batches = _build_batches(UNIVERSITIES)
    context.log.info(
        f"Fetching Google Trends by state for {len(UNIVERSITIES)} universities "
        f"in {len(batches)} batches"
    )

    successful_batches: list[pd.DataFrame] = []
    failed_universities: list[str] = []

    for i, batch in enumerate(batches):
        search_names = [_get_search_name(u) for u in batch]
        context.log.info(
            f"Batch {i + 1}/{len(batches)}: {search_names} + ref"
        )

        result = _fetch_batch_by_state(pytrends, batch, context.log)

        if result is not None:
            successful_batches.append(result)
            context.log.info(f"Batch {i + 1} succeeded: {len(result)} rows")
        else:
            failed_universities.extend(batch)
            context.log.warning(f"Batch {i + 1} failed: {batch}")

        # Delay between batches to avoid rate limiting (skip after last batch)
        if i < len(batches) - 1:
            context.log.info(f"Waiting {BATCH_DELAY_SECONDS}s before next batch...")
            time.sleep(BATCH_DELAY_SECONDS)

    if not successful_batches:
        raise RuntimeError(
            "All Google Trends batches failed. No data retrieved. "
            "Google may be rate-limiting — try again later."
        )

    # Normalize across batches
    combined = _normalize_across_batches_by_state(successful_batches)

    # Sort for consistent output
    combined = combined.sort_values(
        ["university", "state_name"]
    ).reset_index(drop=True)

    # Summary stats for metadata
    uni_avg = (
        combined.groupby("university")["interest"]
        .mean()
        .sort_values(ascending=False)
    )
    top_5 = uni_avg.head(5)
    universities_succeeded = len(combined["university"].unique())
    states_found = sorted(combined["state_name"].unique())

    context.log.info(
        f"Result: {len(combined)} rows, {universities_succeeded} universities, "
        f"{len(states_found)} states: {states_found}"
    )
    context.log.info(f"Top 5 by avg state interest:\n{top_5}")

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(combined)),
            "source_url": dg.MetadataValue.url("https://trends.google.com/trends/"),
            "universities_succeeded": dg.MetadataValue.int(universities_succeeded),
            "universities_failed": dg.MetadataValue.int(len(failed_universities)),
            "failed_list": dg.MetadataValue.text(
                ", ".join(failed_universities) if failed_universities else "none"
            ),
            "states_found": dg.MetadataValue.text(", ".join(states_found)),
            "top_5_preview": dg.MetadataValue.md(
                top_5.reset_index()
                .rename(
                    columns={
                        "university": "University",
                        "interest": "Avg State Interest",
                    }
                )
                .to_markdown(index=False, floatfmt=".1f")
            ),
        }
    )

    return combined[["university", "search_name", "state_name", "interest"]]
