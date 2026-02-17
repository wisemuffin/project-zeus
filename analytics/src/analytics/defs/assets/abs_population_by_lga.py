import io

import dagster as dg
import pandas as pd
import requests

ABS_API_URL = (
    "https://data.api.abs.gov.au/rest/data/"
    "ABS,ABS_ANNUAL_ERP_LGA2024,1.0.0/"
    "ERP.3.A15.+.LGA2024.A"
)


@dg.asset(
    group_name="abs_data",
    tags={"source": "abs", "domain": "demographics"},
)
def abs_population_by_lga(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Estimated Resident Population (ERP) for 15-19 year olds by LGA.

    Fetches from ABS SDMX REST API. Age group A15 (15-19 years) covers the
    approximate Year 11/12 secondary student cohort. Persons only (SEX_ABS=3).
    """
    response = requests.get(
        ABS_API_URL,
        headers={"Accept": "application/vnd.sdmx.data+csv"},
        timeout=60,
    )
    response.raise_for_status()

    df = pd.read_csv(io.StringIO(response.text))

    context.log.info(f"Fetched {len(df)} rows from ABS API")

    latest_year = df["TIME_PERIOD"].max()
    latest = df[df["TIME_PERIOD"] == latest_year]

    lga_count = latest["LGA_2024"].nunique()
    total_population = int(latest["OBS_VALUE"].sum())

    context.log.info(
        f"Latest year: {latest_year} — {lga_count} LGAs, "
        f"total 15-19 population: {total_population:,}"
    )

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "latest_year": dg.MetadataValue.text(str(latest_year)),
        "lga_count": dg.MetadataValue.int(lga_count),
        "total_population_15_19": dg.MetadataValue.int(total_population),
    })

    return df
