import io
from datetime import date

import dagster as dg
import pandas as pd
import requests

# ANZSCO2 occupations-by-state IVI file follows the same publication-lag pattern
# as the skill-level file, but with a different filename stem.
IVI_ANZSCO2_URL_TEMPLATE = (
    "https://www.jobsandskills.gov.au/sites/default/files/"
    "{pub_year}-{pub_month:02d}/"
    "internet_vacancies_anzsco2_occupations_states_and_territories_-_"
    "{data_month_name}_{data_year}.xlsx"
)


def _build_ivi_anzsco2_url(data_date: date) -> str:
    """Build ANZSCO2 IVI download URL for a given data reference month.

    The folder date is one month after the data month (publication lag).
    """
    pub_month = data_date.month + 1
    pub_year = data_date.year
    if pub_month > 12:
        pub_month = 1
        pub_year += 1
    return IVI_ANZSCO2_URL_TEMPLATE.format(
        pub_year=pub_year,
        pub_month=pub_month,
        data_month_name=data_date.strftime("%B").lower(),
        data_year=data_date.year,
    )


def _find_latest_ivi_anzsco2_url() -> tuple[str, date]:
    """Try recent months to find the latest available ANZSCO2 IVI file."""
    today = date.today()
    for months_back in range(1, 7):
        year = today.year
        month = today.month - months_back
        if month <= 0:
            month += 12
            year -= 1
        data_date = date(year, month, 1)
        url = _build_ivi_anzsco2_url(data_date)
        resp = requests.head(url, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            return url, data_date
    raise RuntimeError(
        "Could not find ANZSCO2 IVI Excel file for any of the last 6 months"
    )


@dg.asset(
    group_name="job_market",
    tags={"source": "job_market", "domain": "employment"},
)
def job_market_occupations(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """Internet Vacancy Index (IVI) — job vacancies by ANZSCO2 occupation and state.

    Source: Jobs and Skills Australia, Excel, public, monthly
    Marketing use: **What message** — occupation-level job demand (e.g. "Medical
        Practitioners and Nurses", "ICT Professionals") mapped back to degree
        programs enables career-outcome campaign messaging. Shows students which
        occupations have growing demand.
    Format: level, anzsco_code, title, state, date, vacancies (long format)
    Limitations:
    - Online vacancies only (not all job openings)
    - Data published 1-2 months after reference month
    - URL structure may change if publisher updates their site
    """
    url, ref_date = _find_latest_ivi_anzsco2_url()
    ref_label = ref_date.strftime("%B %Y")
    context.log.info(f"Downloading ANZSCO2 IVI data for {ref_label}: {url}")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    raw = pd.read_excel(
        io.BytesIO(response.content),
        sheet_name="Trend",
        header=0,
        engine="openpyxl",
    )

    # First 4 columns are: Level, ANZSCO_CODE, Title, State
    id_cols = list(raw.columns[:4])
    rename_map = dict(zip(id_cols, ["level", "anzsco_code", "title", "state"]))
    raw.rename(columns=rename_map, inplace=True)

    # Remaining columns are date values — melt to long format
    date_cols = [c for c in raw.columns if c not in rename_map.values()]
    df = raw.melt(
        id_vars=["level", "anzsco_code", "title", "state"],
        value_vars=date_cols,
        var_name="date",
        value_name="vacancies",
    )
    df["date"] = pd.to_datetime(df["date"])
    df["vacancies"] = pd.to_numeric(df["vacancies"], errors="coerce")

    context.log.info(f"Parsed {len(df)} rows (melted from {len(raw)} series)")

    # Latest month total vacancies
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
