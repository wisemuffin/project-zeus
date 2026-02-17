import io
from datetime import date

import dagster as dg
import pandas as pd
import requests

# IVI data is published monthly. Data for month X is published in month X+1.
# The folder uses the publication month, the filename uses the data reference month.
# Example: December 2025 data → folder 2026-01, filename december_2025.
IVI_URL_TEMPLATE = (
    "https://www.jobsandskills.gov.au/sites/default/files/"
    "{pub_year}-{pub_month:02d}/"
    "internet_vacancies_anzsco_skill_level_states_and_territories_-_"
    "{data_month_name}_{data_year}.xlsx"
)


def _build_ivi_url(data_date: date) -> str:
    """Build IVI download URL for a given data reference month.

    The folder date is one month after the data month (publication lag).
    """
    pub_month = data_date.month + 1
    pub_year = data_date.year
    if pub_month > 12:
        pub_month = 1
        pub_year += 1
    return IVI_URL_TEMPLATE.format(
        pub_year=pub_year,
        pub_month=pub_month,
        data_month_name=data_date.strftime("%B").lower(),
        data_year=data_date.year,
    )


def _find_latest_ivi_url() -> tuple[str, date]:
    """Try recent months to find the latest available IVI file."""
    today = date.today()
    # Data for month X is published in X+1, so the latest possible data month
    # is last month (published this month). Try backwards up to 6 months.
    for months_back in range(1, 7):
        year = today.year
        month = today.month - months_back
        if month <= 0:
            month += 12
            year -= 1
        data_date = date(year, month, 1)
        url = _build_ivi_url(data_date)
        resp = requests.head(url, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            return url, data_date
    raise RuntimeError(
        "Could not find IVI Excel file for any of the last 6 months"
    )


@dg.asset(
    group_name="job_market",
    tags={"source": "job_market", "domain": "employment"},
)
def job_market(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Internet Vacancy Index (IVI) — online job vacancies by occupation and state.

    Downloads the latest monthly IVI Excel file from Jobs and Skills Australia.
    Parses the "Trend" sheet and melts from wide format (date columns) to long
    format with columns: level, title, state, skill_level, date, vacancies.
    """
    url, ref_date = _find_latest_ivi_url()
    ref_label = ref_date.strftime("%B %Y")
    context.log.info(f"Downloading IVI data for {ref_label}: {url}")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    raw = pd.read_excel(
        io.BytesIO(response.content),
        sheet_name="Trend",
        header=0,
        engine="openpyxl",
    )

    # Rename the identifier columns to clean names
    id_cols = list(raw.columns[:4])
    rename_map = dict(zip(id_cols, ["level", "title", "state", "skill_level"]))
    raw.rename(columns=rename_map, inplace=True)

    # All remaining columns are date values — melt to long format
    date_cols = [c for c in raw.columns if c not in rename_map.values()]
    df = raw.melt(
        id_vars=["level", "title", "state", "skill_level"],
        value_vars=date_cols,
        var_name="date",
        value_name="vacancies",
    )
    df["date"] = pd.to_datetime(df["date"])
    df["vacancies"] = pd.to_numeric(df["vacancies"], errors="coerce")

    context.log.info(f"Parsed {len(df)} rows (melted from {len(raw)} series)")

    # Latest month total vacancies (Australian total row)
    latest = df[(df["date"] == df["date"].max()) & (df["level"] == 0)]
    total_vacancies = int(latest["vacancies"].sum()) if len(latest) > 0 else 0

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "series_count": dg.MetadataValue.int(len(raw)),
        "total_vacancies_latest": dg.MetadataValue.int(total_vacancies),
        "reference_month": dg.MetadataValue.text(ref_label),
        "source_url": dg.MetadataValue.url(url),
    })

    return df
