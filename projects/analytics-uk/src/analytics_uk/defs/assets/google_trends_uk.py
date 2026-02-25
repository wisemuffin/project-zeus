import dagster as dg
import dlt
from dagster import AssetExecutionContext, AssetKey, AssetSpec
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from dagster_dlt.translator import DltResourceTranslatorData
from trendspyg import download_google_trends_rss


@dlt.source
def google_trends_uk_source():
    @dlt.resource(name="google_trends_uk", write_disposition="replace")
    def trends():
        """Trending Google searches in the United Kingdom.

        Source: Google Trends via trendspyg RSS feed, public, real-time (~0.2s)
        Marketing use: **What message** — trending topics reveal timely content
            opportunities. When a trend aligns with a university's programmes (e.g.
            AI trending → Computer Science), it signals a moment for reactive
            campaign creative.
        Format: trend titles, traffic volume, news headlines, article URLs,
            publication timestamps
        Limitations:
        - Current trends only (~10-20 results); no historical time-series
        - No keyword lookup (cannot query specific terms)
        - General trends, not filtered to education topics
        """
        df = download_google_trends_rss(geo="GB", output_format="dataframe")
        yield from df.to_dict("records")

    return trends


class GoogleTrendsUkTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            key=AssetKey("google_trends_uk"),
            group_name="google_trends",
            tags={
                "source": "google",
                "domain": "search_interest",
                "update_frequency": "6h",
                "ingestion": "rss",
            },
            kinds={"python", "rss", "dlt"},
            automation_condition=dg.AutomationCondition.on_cron("0 */6 * * *"),
            deps=[],
        )


@dlt_assets(
    dlt_source=google_trends_uk_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="google_trends_uk",
        destination=dlt.destinations.duckdb("analytics.duckdb"),
        dataset_name="public",
        progress="log",
    ),
    name="google_trends_uk",
    dagster_dlt_translator=GoogleTrendsUkTranslator(),
    op_tags={"dagster/concurrency_key": "duckdb_dlt"},
)
def google_trends_uk(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
