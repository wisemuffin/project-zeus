import csv
import io

import dagster as dg
import dlt
import requests
from dagster import AssetExecutionContext, AssetKey, AssetSpec
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from dagster_dlt.translator import DltResourceTranslatorData

ABS_API_URL = (
    "https://data.api.abs.gov.au/rest/data/"
    "ABS,ABS_ANNUAL_ERP_LGA2024,1.0.0/"
    "ERP.3.A15.+.LGA2024.A"
)


@dlt.source
def abs_population_source():
    @dlt.resource(name="abs_population_by_lga", write_disposition="replace")
    def population_by_lga():
        """Estimated Resident Population (ERP) for 15-19 year olds by LGA.

        Source: ABS SDMX REST API, CSV, public, annual (~12-month lag)
        Marketing use: **Where** — population counts by Local Government Area size
            the prospective student market geographically. High-population LGAs
            indicate where to concentrate geo-targeted digital campaigns.
        Format: DATAFLOW, MEASURE, SEX_ABS, AGE, LGA_2024, REGION_TYPE, FREQUENCY,
            TIME_PERIOD, OBS_VALUE, UNIT_MEASURE, OBS_STATUS, OBS_COMMENT
        Limitations:
        - Age granularity is 5-year groups only (15-19); cannot isolate Year 12
        - ~12-month publication lag
        - Uses 2024 LGA boundaries (historical data concorded by ABS)
        """
        response = requests.get(
            ABS_API_URL,
            headers={"Accept": "application/vnd.sdmx.data+csv"},
            timeout=60,
        )
        response.raise_for_status()

        reader = csv.DictReader(io.StringIO(response.text))
        for row in reader:
            yield row

    return population_by_lga


class AbsPopulationTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            key=AssetKey("abs_population_by_lga"),
            group_name="abs_data",
            tags={"source": "abs", "domain": "demographics", "update_frequency": "annual", "ingestion": "api"},
            kinds={"python", "api", "dlt"},
            automation_condition=dg.AutomationCondition.on_cron("0 9 1 11 *"),
            deps=[],
            metadata={
                "source_url": dg.MetadataValue.url(ABS_API_URL),
            },
        )


@dlt_assets(
    dlt_source=abs_population_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="abs_population_by_lga",
        destination=dlt.destinations.duckdb("analytics.duckdb"),
        dataset_name="public",
        progress="log",
    ),
    name="abs_population_by_lga",
    dagster_dlt_translator=AbsPopulationTranslator(),
)
def abs_population_by_lga(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
