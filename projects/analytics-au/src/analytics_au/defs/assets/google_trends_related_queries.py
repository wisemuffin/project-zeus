import time

import dagster as dg
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


def _fetch_batch_related_queries(
    pytrends: TrendReq,
    batch_universities: list[str],
    log: dg.DagsterLogManager,
) -> pd.DataFrame | None:
    """Fetch related queries (top and rising) for one batch (4 unis + reference).

    Returns a long-format DataFrame with columns: university, search_name,
    related_query, query_type, value. Returns None if all retries are exhausted.
    """
    search_names = [REFERENCE_SEARCH_NAME] + [
        _get_search_name(u) for u in batch_universities
    ]

    for attempt in range(MAX_RETRIES):
        try:
            pytrends.build_payload(search_names, geo="AU", timeframe="today 5-y")
            result = pytrends.related_queries()

            rows = []
            search_to_qilt = {REFERENCE_SEARCH_NAME: REFERENCE_UNIVERSITY}
            for u in batch_universities:
                search_to_qilt[_get_search_name(u)] = u

            for search_name, tables in result.items():
                # Skip reference keyword results
                if search_name == REFERENCE_SEARCH_NAME:
                    continue

                university = search_to_qilt.get(search_name)
                if university is None:
                    continue

                for query_type in ("top", "rising"):
                    df = tables.get(query_type)
                    if df is None or df.empty:
                        continue

                    for _, row in df.iterrows():
                        rows.append(
                            {
                                "university": university,
                                "search_name": search_name,
                                "related_query": row["query"],
                                "query_type": query_type,
                                "value": str(row["value"]),
                            }
                        )

            if not rows:
                log.warning(f"No related queries for batch: {search_names}")
                return None

            return pd.DataFrame(rows)

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
def google_trends_related_queries(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """Google Trends related queries (top and rising) for 42 Australian universities.

    Source: Google Trends (trends.google.com) via pytrends-modern.
        related_queries() returns the top and rising queries associated with
        each university search term in Australia over a 5-year window.
        Top queries are ranked by search volume (0-100 index). Rising queries
        show growth percentage or "Breakout" for terms with massive growth.
    Marketing use: **What message** — reveals what prospective students search
        alongside university names. Top queries expose brand associations and
        common search paths. Rising queries identify emerging interests and
        trending topics that can inform ad copy and content strategy.
    Format: university (QILT name, join key), search_name (what was searched),
        related_query (the associated search term), query_type (top/rising),
        value (relevance score 0-100 for top, growth % or "Breakout" for rising)
    Limitations:
    - No cross-batch normalization needed — each keyword's queries are independent
    - Rising queries may be ephemeral and change between materializations
    - "Breakout" values indicate >5000% growth but exact magnitude is unknown
    - Acronym searches (QUT, UTS, UNSW, RMIT) may surface unrelated queries
    - Small universities may have no related queries at all
    - ~11 minutes execution time due to rate-limit delays between batches
    """
    pytrends = TrendReq(hl="en-AU", tz=-600)
    batches = _build_batches(UNIVERSITIES)
    context.log.info(
        f"Fetching Google Trends related queries for {len(UNIVERSITIES)} "
        f"universities in {len(batches)} batches"
    )

    successful_batches: list[pd.DataFrame] = []
    failed_universities: list[str] = []

    for i, batch in enumerate(batches):
        search_names = [_get_search_name(u) for u in batch]
        context.log.info(
            f"Batch {i + 1}/{len(batches)}: {search_names} + ref"
        )

        result = _fetch_batch_related_queries(pytrends, batch, context.log)

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
            "All Google Trends related queries batches failed. No data retrieved. "
            "Google may be rate-limiting — try again later."
        )

    combined = pd.concat(successful_batches, ignore_index=True)

    # Sort for consistent output
    combined = combined.sort_values(
        ["university", "query_type", "related_query"]
    ).reset_index(drop=True)

    universities_succeeded = len(combined["university"].unique())
    top_count = len(combined[combined["query_type"] == "top"])
    rising_count = len(combined[combined["query_type"] == "rising"])

    context.log.info(
        f"Result: {len(combined)} rows, {universities_succeeded} universities, "
        f"{top_count} top queries, {rising_count} rising queries"
    )

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(combined)),
            "source_url": dg.MetadataValue.url("https://trends.google.com/trends/"),
            "universities_succeeded": dg.MetadataValue.int(universities_succeeded),
            "universities_failed": dg.MetadataValue.int(len(failed_universities)),
            "failed_list": dg.MetadataValue.text(
                ", ".join(failed_universities) if failed_universities else "none"
            ),
            "top_queries_count": dg.MetadataValue.int(top_count),
            "rising_queries_count": dg.MetadataValue.int(rising_count),
        }
    )

    return combined[
        ["university", "search_name", "related_query", "query_type", "value"]
    ]
