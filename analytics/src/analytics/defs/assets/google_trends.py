from datetime import datetime, timezone

import dagster as dg
import pandas as pd
from trendspyg import download_google_trends_rss


@dg.asset(
    group_name="google_trends",
    tags={"source": "google", "domain": "search_interest"},
)
def google_trends(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Trending Google searches in Australia.

    Source: Google Trends via trendspyg RSS feed, public, real-time (~0.2s)
    Marketing use: **What message** — trending topics reveal timely content
        opportunities. When a trend aligns with a university's programs (e.g.
        AI trending → Computer Science), it signals a moment for reactive
        campaign creative.
    Format: trend titles, traffic volume, news headlines, article URLs,
        publication timestamps
    Limitations:
    - Current trends only (~10-20 results); no historical time-series
    - No keyword lookup (cannot query specific terms)
    - General trends, not filtered to education topics
    - See docs/data-sources/search-data-options.md for alternatives
    """
    df = download_google_trends_rss(geo="AU", output_format="dataframe")

    fetch_time = datetime.now(timezone.utc).isoformat()

    context.log.info(f"Fetched {len(df)} trending searches at {fetch_time}")
    context.log.info(f"Columns: {list(df.columns)}")

    context.add_output_metadata({
        "trend_count": dg.MetadataValue.int(len(df)),
        "fetch_timestamp": dg.MetadataValue.text(fetch_time),
    })

    return df
