import io
import re
import zipfile

import dagster as dg
import pandas as pd
import requests

GOS_URL = (
    "https://www.qilt.edu.au/docs/default-source/default-document-library/"
    "gos_2024_national_report_tables.zip"
)
SES_URL = (
    "https://www.qilt.edu.au/docs/default-source/default-document-library/"
    "ses_2024_national_report_tables.zip"
)


def _extract_xlsx(url: str) -> bytes:
    """Download a QILT ZIP and return the .xlsx file contents."""
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        xlsx_names = [n for n in zf.namelist() if n.endswith(".xlsx")]
        if not xlsx_names:
            raise RuntimeError(f"No .xlsx in ZIP from {url}")
        return zf.read(xlsx_names[0])


def _extract_point_estimate(value: str) -> float | None:
    """Extract the point estimate from 'XX.X (lower, upper)' format."""
    if pd.isna(value) or str(value).strip() == "":
        return None
    s = str(value).strip()
    # Match leading number before any parenthetical CI
    m = re.match(r"^([\d,]+(?:\.\d+)?)", s.replace(" ", ""))
    if m:
        return float(m.group(1).replace(",", ""))
    return None


def _parse_institution_column(
    xlsx_bytes: bytes, sheet_name: str, value_col_name: str
) -> pd.DataFrame:
    """Parse a QILT institution-level sheet with CI format into institution + value."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name=sheet_name,
        header=3,
        engine="openpyxl",
    )
    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "institution"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    raw = raw[raw["institution"].notna()].copy()
    raw = raw[~raw["institution"].str.contains("All Universities|Total", na=False)].copy()
    raw = raw[raw["institution"].astype(str).str.strip() != ""].copy()

    # The third column is the value column (with CIs)
    val_col = [c for c in raw.columns if c != "institution"][0]
    raw[value_col_name] = raw[val_col].apply(_extract_point_estimate)
    raw["institution"] = raw["institution"].str.strip()

    return raw[["institution", value_col_name]].reset_index(drop=True)


def _parse_ses_institutions(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse SES satisfaction by institution, extracting point estimates from CIs."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name="FOCUS_UG_UNI_1Y_INST_CI",
        header=3,
        engine="openpyxl",
    )
    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "institution"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    raw = raw[raw["institution"].notna()].copy()
    raw = raw[~raw["institution"].str.contains("All Universities|Total", na=False)].copy()
    raw = raw[raw["institution"].astype(str).str.strip() != ""].copy()
    raw["institution"] = raw["institution"].str.strip()
    # Strip trailing whitespace and normalise non-breaking spaces in column names
    raw.columns = [
        c.strip().replace("\xa0", " ") if isinstance(c, str) else c
        for c in raw.columns
    ]

    ses_rename = {
        "Skills Development": "skills_development",
        "Peer Engagement *": "peer_engagement",
        "Teaching Quality and Engagement": "teaching_quality",
        "Student Support and Services *": "student_support",
        "Learning Resources": "learning_resources",
        "Quality of entire educational experience": "overall_quality",
    }

    for old_name, new_name in ses_rename.items():
        if old_name in raw.columns:
            raw[new_name] = raw[old_name].apply(_extract_point_estimate)

    keep = ["institution"] + list(ses_rename.values())
    return raw[[c for c in keep if c in raw.columns]].reset_index(drop=True)


@dg.asset(
    group_name="institution_scores",
    tags={"source": "qilt", "domain": "institution_benchmarking", "update_frequency": "annual", "ingestion": "file_download"},
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 10 *"),
)
def qilt_institution_scores(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """QILT institution scorecard — satisfaction, employment, and salary per university.

    Source: Quality Indicators for Learning and Teaching (QILT), Australian
        Government. Combines Student Experience Survey (SES) satisfaction
        indicators with Graduate Outcomes Survey (GOS) employment rates and
        median salaries. Covers all 42 Australian universities.
    Marketing use: **Competitive benchmarking** — enables per-university
        comparisons ("your overall quality score is 80.5% vs sector average
        76.4%") and identifies strengths/weaknesses to emphasise in campaigns.
    Format: institution, skills_development, peer_engagement, teaching_quality,
        student_support, learning_resources, overall_quality (all % positive),
        ft_employment_rate (%), median_salary ($)
    Limitations:
    - Undergraduate only (postgraduate available but not yet ingested)
    - SES and GOS may have slightly different institution lists
    - Values with <5 respondents suppressed (appear as null)
    - University of Divinity typically has too few respondents for most metrics
    - URLs may change when 2025 data is published (~September 2026)
    """
    context.log.info("Downloading SES and GOS institution data...")

    ses_bytes = _extract_xlsx(SES_URL)
    context.log.info("SES extracted")

    gos_bytes = _extract_xlsx(GOS_URL)
    context.log.info("GOS extracted")

    # SES: 6 satisfaction indicators by institution
    ses_df = _parse_ses_institutions(ses_bytes)
    context.log.info(f"Parsed {len(ses_df)} institutions from SES")

    # GOS: FT employment rate by institution
    fte_df = _parse_institution_column(
        gos_bytes, "FTE_UG_UNI_1Y_INST_FIG", "ft_employment_rate"
    )
    context.log.info(f"Parsed {len(fte_df)} institutions from GOS (employment)")

    # GOS: Median salary by institution
    sal_df = _parse_institution_column(
        gos_bytes, "SAL_UG_UNI_1Y_INST_FIG", "median_salary"
    )
    context.log.info(f"Parsed {len(sal_df)} institutions from GOS (salary)")

    # Merge all three on institution name
    df = ses_df.merge(fte_df, on="institution", how="outer")
    df = df.merge(sal_df, on="institution", how="outer")

    context.log.info(f"Combined scorecard: {len(df)} institutions")

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(df)),
            "source_url": dg.MetadataValue.url("https://www.qilt.edu.au/"),
            "survey_year": dg.MetadataValue.text("2024"),
            "preview": dg.MetadataValue.md(
                df.to_markdown(index=False, floatfmt=".1f")
            ),
        }
    )

    return df
