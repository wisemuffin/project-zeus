import io
import zipfile

import dagster as dg
import pandas as pd
import requests

GOS_URL = (
    "https://www.qilt.edu.au/docs/default-source/default-document-library/"
    "gos_2024_national_report_tables.zip"
)

# Sheets to extract from the GOS Excel workbook.
# Employment outcomes by study area (undergraduate, all providers, 2-year comparison)
_SHEET_EMPLOYMENT = "EMP_UG_ALL_2Y_AREA"
# Median salary by study area and gender (undergraduate, all providers, 2-year comparison)
_SHEET_SALARY = "SAL_UG_ALL_2Y_AREA_E315"

# Both sheets have 3 header rows (title, back-link, blank) then a column header row.
_HEADER_ROWS = 3


def _parse_employment(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse employment outcomes by study area from the GOS workbook."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name=_SHEET_EMPLOYMENT,
        header=_HEADER_ROWS,
        engine="openpyxl",
    )
    # First two columns are blank group label + study area name.
    # Rename them, drop the blank group column.
    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "study_area"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    # Keep only data rows (non-null study_area, exclude Total/Std dev/metadata)
    raw = raw[raw["study_area"].notna()].copy()
    raw = raw[~raw["study_area"].isin(["Total", "Standard deviation"])].copy()
    raw = raw[raw["study_area"].astype(str).str.strip() != ""].copy()

    raw.rename(
        columns={
            "Full-time employment 2023": "ft_employment_rate_prior",
            "Full-time employment 2024": "ft_employment_rate",
            "Overall employment 2023": "overall_employment_rate_prior",
            "Overall employment 2024": "overall_employment_rate",
            "Labour force participation rate 2023": "lf_participation_rate_prior",
            "Labour force participation rate 2024": "lf_participation_rate",
        },
        inplace=True,
    )

    keep = [
        "study_area",
        "ft_employment_rate",
        "ft_employment_rate_prior",
        "overall_employment_rate",
        "overall_employment_rate_prior",
        "lf_participation_rate",
        "lf_participation_rate_prior",
    ]
    df = raw[keep].copy()

    for col in keep[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["study_area"] = df["study_area"].str.strip().str.replace("\xa0", " ")
    return df.reset_index(drop=True)


def _parse_salary(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse median salary by study area and gender from the GOS workbook."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name=_SHEET_SALARY,
        header=_HEADER_ROWS,
        engine="openpyxl",
    )
    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "study_area"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    raw = raw[raw["study_area"].notna()].copy()
    raw = raw[~raw["study_area"].isin(["Total", "Standard deviation"])].copy()
    raw = raw[raw["study_area"].astype(str).str.strip() != ""].copy()

    raw.rename(
        columns={
            "Male 2024": "median_salary_male",
            "Female 2024": "median_salary_female",
            "Total 2024": "median_salary",
            "Total 2023": "median_salary_prior",
        },
        inplace=True,
    )

    keep = [
        "study_area",
        "median_salary",
        "median_salary_prior",
        "median_salary_male",
        "median_salary_female",
    ]
    df = raw[keep].copy()

    # Salaries are strings like "72,000" or "n/a" — clean to numeric
    for col in keep[1:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.strip()
            .replace("n/a", pd.NA)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["study_area"] = df["study_area"].str.strip().str.replace("\xa0", " ")
    return df.reset_index(drop=True)


@dg.asset(
    group_name="graduate_outcomes",
    tags={"source": "qilt", "domain": "graduate_outcomes", "update_frequency": "annual"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 10 *"),
)
def qilt_graduate_outcomes(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """QILT Graduate Outcomes Survey (GOS) — employment rates and salaries by study area.

    Source: Quality Indicators for Learning and Teaching (QILT), Australian
        Government. Annual survey of 117,000+ graduates 4-6 months post-completion.
    Marketing use: **What message** — provides concrete career outcome proof
        points per field of study. "X% of Engineering graduates are in full-time
        work earning a median $Y" is powerful campaign messaging. Gender salary
        splits enable targeted creative. Year-on-year changes highlight improving
        or declining fields.
    Format: study_area, ft_employment_rate, overall_employment_rate,
        lf_participation_rate, median_salary, median_salary_male,
        median_salary_female (plus prior-year columns for each)
    Limitations:
    - Undergraduate only (postgraduate data available but not yet ingested)
    - 4-6 month post-graduation snapshot (not long-term outcomes)
    - Study areas use QILT/ASCED classification, not UAC categories — requires
      mapping for joins with UAC preference data
    - Small cell sizes suppressed (n/a) for some fields × gender combinations
    - URL may change when 2025 data is published (~September 2026)
    """
    context.log.info(f"Downloading GOS report tables: {GOS_URL}")
    response = requests.get(GOS_URL, timeout=120)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        # Find the .xlsx file inside the ZIP
        xlsx_names = [n for n in zf.namelist() if n.endswith(".xlsx")]
        if not xlsx_names:
            raise RuntimeError(f"No .xlsx file found in ZIP. Contents: {zf.namelist()}")
        xlsx_bytes = zf.read(xlsx_names[0])

    context.log.info(f"Extracted {xlsx_names[0]} ({len(xlsx_bytes):,} bytes)")

    emp_df = _parse_employment(xlsx_bytes)
    sal_df = _parse_salary(xlsx_bytes)

    df = emp_df.merge(sal_df, on="study_area", how="outer")

    context.log.info(f"Parsed {len(df)} study areas with employment + salary data")

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(df)),
            "study_areas": dg.MetadataValue.int(len(df)),
            "source_url": dg.MetadataValue.url(GOS_URL),
            "survey_year": dg.MetadataValue.text("2024"),
            "preview": dg.MetadataValue.md(
                df.to_markdown(index=False, floatfmt=".1f")
            ),
        }
    )

    return df
