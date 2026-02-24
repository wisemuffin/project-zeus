import dagster as dg
import pandas as pd
import requests

ABS_MAPSERVER_URL = (
    "https://geo.abs.gov.au/arcgis/rest/services/ASGS2024/LGA/MapServer/0/query"
)

QUERY_PARAMS = {
    "where": "1=1",
    "outFields": "lga_code_2024,lga_name_2024,state_code_2021,state_name_2021,area_albers_sqkm",
    "returnGeometry": "false",
    "f": "json",
}


@dg.asset(
    group_name="abs_data",
    tags={"source": "abs", "domain": "geography", "update_frequency": "annual", "ingestion": "api"},
    kinds={"python", "api"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 11 *"),
)
def abs_lga_reference(context: dg.AssetExecutionContext) -> pd.DataFrame:
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
    rows = [f["attributes"] for f in features]

    df = pd.DataFrame(rows)

    context.log.info(f"Fetched {len(df)} LGA reference rows from ABS MapServer")

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "states": dg.MetadataValue.int(df["state_code_2021"].nunique()),
        "source_url": dg.MetadataValue.url(ABS_MAPSERVER_URL),
    })

    return df
