import dagster as dg
import dlt
import requests
from dagster import AssetExecutionContext, AssetKey, AssetSpec
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from dagster_dlt.translator import DltResourceTranslatorData

ABS_MAPSERVER_URL = (
    "https://geo.abs.gov.au/arcgis/rest/services/ASGS2024/LGA/MapServer/0/query"
)

QUERY_PARAMS = {
    "where": "1=1",
    "outFields": "lga_code_2024,lga_name_2024,state_code_2021,state_name_2021,area_albers_sqkm",
    "returnGeometry": "false",
    "f": "json",
}


@dlt.source
def abs_lga_source():
    @dlt.resource(name="abs_lga_reference", write_disposition="replace")
    def lga_reference():
        """ABS Local Government Area reference data (2024 boundaries).

        Source: ABS MapServer REST API (ASGS 2024 LGA layer), JSON, public, annual
        Marketing use: **Where** — provides LGA names, state mapping, and land area
            for joining to population data. The area field enables computing youth
            density per km², identifying geographically compact LGAs with high youth
            concentration for efficient local ad targeting.
        Format: lga_code_2024, lga_name_2024, state_code_2021, state_name_2021,
            area_albers_sqkm
        Limitations:
        - Boundaries are 2024 edition; LGA amalgamations may cause mismatches with
          older population vintages
        - Area is Albers equal-area projection (suitable for density calculations)
        """
        response = requests.get(ABS_MAPSERVER_URL, params=QUERY_PARAMS, timeout=60)
        response.raise_for_status()

        data = response.json()
        features = data.get("features", [])
        for feature in features:
            yield feature["attributes"]

    return lga_reference


class AbsLgaTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> AssetSpec:
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            key=AssetKey("abs_lga_reference"),
            group_name="abs_data",
            tags={"source": "abs", "domain": "geography", "update_frequency": "annual", "ingestion": "api"},
            kinds={"python", "api", "dlt"},
            automation_condition=dg.AutomationCondition.on_cron("0 9 1 11 *"),
            deps=[],
            metadata={
                "source_url": dg.MetadataValue.url(ABS_MAPSERVER_URL),
            },
        )


@dlt_assets(
    dlt_source=abs_lga_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="abs_lga_reference",
        destination=dlt.destinations.duckdb("analytics.duckdb"),
        dataset_name="public",
        progress="log",
    ),
    name="abs_lga_reference",
    dagster_dlt_translator=AbsLgaTranslator(),
)
def abs_lga_reference(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
