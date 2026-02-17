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

    Uses trendspyg RSS feed to fetch current trending searches. Returns ~10-20
    trending topics with traffic volume, news headlines, and article URLs.
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
