import dagster as dg
import pandas as pd
import requests

NCVER_URL = (
    "https://www.ncver.edu.au/__data/assets/excel_doc/0045/9697824/"
    "Historical-time-series-of-Government-funded-of-VET-1981-to-2024.xlsx"
)

_STATE_MAP = {
    "NSW": "NSW",
    "Vic.": "VIC",
    "Qld": "QLD",
    "SA": "SA",
    "WA": "WA",
    "Tas.": "TAS",
    "NT": "NT",
    "ACT": "ACT",
    "Australia": "Australia",
}
_STATES = list(_STATE_MAP.keys())


def _parse_table1(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse Table 1: VET students by gender and state/territory, 1981-2024.

    The sheet has four sections stacked vertically: Males, Females, Other, Total.
    Each section header appears in column index 3.  Data rows have a 4-digit
    year in column 2 and state values in columns 3-11.  Values are in thousands.
    """
    raw = pd.read_excel(
        xlsx_bytes,
        sheet_name="1",
        header=None,
        engine="openpyxl",
    )

    rows: list[dict] = []
    current_gender: str | None = None
    gender_labels = {"Males": "male", "Females": "female", "Other": "other", "Total": "total"}

    for i in range(6, len(raw)):
        c3 = raw.iloc[i, 3]

        # Detect section headers
        if pd.notna(c3) and str(c3).strip() in gender_labels:
            current_gender = gender_labels[str(c3).strip()]
            continue

        if current_gender is None:
            continue

        c2 = raw.iloc[i, 2]
        if pd.isna(c2):
            continue

        year_str = str(c2).strip()
        if not year_str.isdigit() or len(year_str) != 4:
            continue

        year = int(year_str)

        for j, state in enumerate(_STATES):
            val = raw.iloc[i, 3 + j]
            if pd.isna(val):
                continue
            val_str = str(val).strip()
            if val_str in (".", "-", ""):
                continue
            try:
                thousands = float(val_str)
                rows.append({
                    "year": year,
                    "state": _STATE_MAP[state],
                    "gender": current_gender,
                    "students_thousands": thousands,
                    "students": round(thousands * 1000),
                })
            except ValueError:
                continue

    return pd.DataFrame(rows)


@dg.asset(
    group_name="vet_enrolments",
    tags={
        "source": "ncver",
        "domain": "vet_enrolments",
        "update_frequency": "annual",
        "ingestion": "file_download",
    },
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 9 *"),
)
def ncver_vet_students(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """NCVER Government-funded VET students by state and gender, 1981-2024.

    Source: National Centre for Vocational Education Research (NCVER),
        Historical time series of government-funded VET. Table 1: Students by
        gender and state/territory. Covers all government-funded VET (TAFE and
        other providers) across Australia.
    Marketing use: **Where** and **What message** — provides competitive context
        for university marketing. VET enrolment trends show which states have
        growing vocational sectors (potential market share threat for universities)
        and enable messaging like "Unlike VET, a degree in [field] offers X%
        higher salary and Y% better employment". Also shows gender trends in
        vocational vs higher education.
    Format: year, state, gender, students_count
    Limitations:
    - Government-funded students only (excludes fee-for-service VET)
    - No field-of-education breakdown (available in Table 10 but only from 2002
      and with limited state coverage)
    - Values are rounded to nearest thousand (source reports in '000s)
    - "Other" gender category only has data from 2019 onwards
    - URL may change when 2025 data is published (~August 2026)
    """
    context.log.info(f"Downloading NCVER historical time series: {NCVER_URL}")
    response = requests.get(NCVER_URL, timeout=120)
    response.raise_for_status()

    context.log.info(
        f"Downloaded {len(response.content):,} bytes, parsing Table 1..."
    )
    df = _parse_table1(response.content)

    context.log.info(
        f"Parsed {len(df):,} records: "
        f"{df['year'].min()}-{df['year'].max()}, "
        f"{df['state'].nunique()} states"
    )

    # Summary for metadata
    latest_year = df["year"].max()
    latest_total = df[
        (df["year"] == latest_year) & (df["state"] == "Australia") & (df["gender"] == "total")
    ]["students"].sum()

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "year_range": dg.MetadataValue.text(
            f"{df['year'].min()}-{df['year'].max()}"
        ),
        "source_url": dg.MetadataValue.url(NCVER_URL),
        "latest_year_total": dg.MetadataValue.text(
            f"{latest_year}: {latest_total:,.0f} students (national)"
        ),
        "preview": dg.MetadataValue.md(
            df[
                (df["state"] == "Australia") & (df["gender"] == "total")
            ].tail(10).to_markdown(index=False, floatfmt=",.0f")
        ),
    })

    return df
