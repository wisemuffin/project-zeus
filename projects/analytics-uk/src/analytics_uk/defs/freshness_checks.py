from datetime import timedelta

import dagster as dg
from analytics_uk.defs.assets.google_trends_uk import google_trends_uk

realtime_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[google_trends_uk],
    lower_bound_delta=timedelta(hours=12),
    deadline_cron="0 */6 * * *",
    timezone="Europe/London",
)
