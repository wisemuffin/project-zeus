import time

import dagster as dg
import numpy as np
import pandas as pd
from pytrends_modern import TrendReq

# All 42 Australian universities from the QILT institution scorecard.
# Names must match QILT exactly (join key to qilt_institution_scores).
UNIVERSITIES = [
    "Australian Catholic University",
    "Avondale University",
    "Bond University",
    "Central Queensland University",
    "Charles Darwin University",
    "Charles Sturt University",
    "Curtin University",
    "Deakin University",
    "Edith Cowan University",
    "Federation University Australia",
    "Flinders University",
    "Griffith University",
    "James Cook University",
    "La Trobe University",
    "Macquarie University",
    "Monash University",
    "Murdoch University",
    "Queensland University of Technology",
    "RMIT University",
    "Southern Cross University",
    "Swinburne University of Technology",
    "The Australian National University",
    "The University of Adelaide",
    "The University of Melbourne",
    "The University of Notre Dame Australia",
    "The University of Queensland",
    "The University of South Australia",
    "The University of Sydney",
    "The University of Western Australia",
    "Torrens University",
    "University of Canberra",
    "University of Divinity",
    "University of New England",
    "University of New South Wales",
    "University of Newcastle",
    "University of Southern Queensland",
    "University of Tasmania",
    "University of Technology Sydney",
    "University of Wollongong",
    "University of the Sunshine Coast",
    "Victoria University",
    "Western Sydney University",
]

# Google Trends search names — strip "The " prefix and use well-known acronyms
# where the acronym is more commonly searched than the full name.
SEARCH_NAME_OVERRIDES = {
    "Queensland University of Technology": "QUT",
    "University of Technology Sydney": "UTS",
    "University of New South Wales": "UNSW",
    "RMIT University": "RMIT",
}

# Reference keyword included in every batch to enable cross-batch normalization.
# University of Melbourne is the most-searched Australian university, giving
# a strong, stable signal in every batch.
REFERENCE_UNIVERSITY = "The University of Melbourne"
REFERENCE_SEARCH_NAME = "University of Melbourne"

BATCH_DELAY_SECONDS = 65
MAX_RETRIES = 3
RETRY_BASE_SECONDS = 120  # 2min, 4min, 8min


def _get_search_name(university: str) -> str:
    """Convert QILT official name to a Google Trends search-friendly name."""
    if university in SEARCH_NAME_OVERRIDES:
        return SEARCH_NAME_OVERRIDES[university]
    # Strip "The " prefix for cleaner search terms
    if university.startswith("The "):
        return university[4:]
    return university


def _build_batches(universities: list[str]) -> list[list[str]]:
    """Split universities into batches of up to 4 + the reference keyword (5 total).

    The reference keyword is always included in position 0 of each batch
    to allow cross-batch normalization.
    """
    # Exclude the reference university from the list (it's in every batch already)
    others = [u for u in universities if u != REFERENCE_UNIVERSITY]
    batches = []
    for i in range(0, len(others), 4):
        batch = others[i : i + 4]
        batches.append(batch)
    return batches


def _fetch_batch(
    pytrends: TrendReq,
    batch_universities: list[str],
    log: dg.DagsterLogManager,
) -> pd.DataFrame | None:
    """Fetch interest over time for one batch (4 unis + reference).

    Returns a long-format DataFrame with columns: university, search_name, date, interest.
    Returns None if all retries are exhausted.
    """
    search_names = [REFERENCE_SEARCH_NAME] + [
        _get_search_name(u) for u in batch_universities
    ]

    for attempt in range(MAX_RETRIES):
        try:
            pytrends.build_payload(search_names, geo="AU", timeframe="today 5-y")
            df = pytrends.interest_over_time()
            if df.empty:
                log.warning(f"Empty result for batch: {search_names}")
                return None

            # Drop the isPartial column
            df = df.drop(columns=["isPartial"], errors="ignore")

            # Melt from wide (one col per keyword) to long format
            df = df.reset_index()
            df = df.melt(id_vars=["date"], var_name="search_name", value_name="interest")
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
                log.error(f"Batch permanently failed after {MAX_RETRIES} attempts: {e}")
                return None


def _normalize_across_batches(all_data: list[pd.DataFrame]) -> pd.DataFrame:
    """Normalize interest values across batches using the reference keyword.

    Each batch has its own 0-100 scale. We use the reference keyword
    (present in every batch) to compute a scale factor per batch, then
    rescale everything to a single 0-100 range.
    """
    normalized_parts = []

    # Compute median interest of reference keyword per batch
    ref_medians = []
    for batch_df in all_data:
        ref_rows = batch_df[batch_df["university"] == REFERENCE_UNIVERSITY]
        median_val = ref_rows["interest"].median()
        ref_medians.append(median_val)

    # Use the first batch's reference median as the anchor
    anchor_median = ref_medians[0]

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

    # Rescale to 0-100 where 100 = peak interest across all universities
    max_interest = combined["interest"].max()
    if max_interest > 0:
        combined["interest"] = (combined["interest"] / max_interest) * 100.0

    return combined


def _aggregate_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate weekly data to monthly averages."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby(["university", "search_name", "month"])
        .agg(interest=("interest", "mean"))
        .reset_index()
    )
    monthly["date"] = monthly["month"].dt.to_timestamp()
    monthly = monthly.drop(columns=["month"])
    monthly["interest"] = monthly["interest"].round(1)

    return monthly


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
def google_trends_interest(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Google Trends search interest over time for 42 Australian universities.

    Source: Google Trends (trends.google.com) via pytrends-modern. Relative
        search interest index (0-100) for each university name in Australia,
        aggregated to monthly granularity over a rolling 5-year window.
        Cross-batch normalized so values are comparable across all universities.
    Marketing use: **Who + Where** — reveals which university brands have the
        strongest search demand, seasonal patterns around intake periods
        (Feb/Mar and Jul/Aug spikes), and year-over-year brand momentum.
        Enables competitive benchmarking of brand awareness and timing of
        campaign bursts to align with natural search interest peaks.
    Format: university (QILT name, join key), search_name (what was searched),
        date (monthly), interest (0-100 normalized across all universities)
    Limitations:
    - Relative index, not absolute search volume — cannot compare to non-university terms
    - Google Trends batches max 5 keywords; cross-batch normalization uses
      University of Melbourne as anchor, which may introduce small scaling artifacts
    - Acronym searches (QUT, UTS, UNSW, RMIT) may capture non-university intent
    - University of Divinity and Avondale University may have very low/zero signal
    - ~11 minutes execution time due to rate-limit delays between batches
    """
    pytrends = TrendReq(hl="en-AU", tz=-600)
    batches = _build_batches(UNIVERSITIES)
    context.log.info(
        f"Fetching Google Trends for {len(UNIVERSITIES)} universities "
        f"in {len(batches)} batches"
    )

    successful_batches: list[pd.DataFrame] = []
    failed_universities: list[str] = []

    for i, batch in enumerate(batches):
        search_names = [_get_search_name(u) for u in batch]
        context.log.info(
            f"Batch {i + 1}/{len(batches)}: {search_names} + ref"
        )

        result = _fetch_batch(pytrends, batch, context.log)

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

    # Normalize across batches and aggregate to monthly
    combined = _normalize_across_batches(successful_batches)
    monthly = _aggregate_to_monthly(combined)

    # Sort for consistent output
    monthly = monthly.sort_values(["university", "date"]).reset_index(drop=True)

    # Summary stats for metadata
    uni_avg = (
        monthly.groupby("university")["interest"]
        .mean()
        .sort_values(ascending=False)
    )
    top_5 = uni_avg.head(5)
    universities_succeeded = len(monthly["university"].unique())

    context.log.info(
        f"Result: {len(monthly)} rows, {universities_succeeded} universities"
    )
    context.log.info(f"Top 5 by avg interest:\n{top_5}")

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(monthly)),
            "source_url": dg.MetadataValue.url("https://trends.google.com/trends/"),
            "universities_succeeded": dg.MetadataValue.int(universities_succeeded),
            "universities_failed": dg.MetadataValue.int(len(failed_universities)),
            "failed_list": dg.MetadataValue.text(
                ", ".join(failed_universities) if failed_universities else "none"
            ),
            "top_5_preview": dg.MetadataValue.md(
                top_5.reset_index().rename(
                    columns={"university": "University", "interest": "Avg Interest"}
                ).to_markdown(index=False, floatfmt=".1f")
            ),
        }
    )

    return monthly[["university", "search_name", "date", "interest"]]
