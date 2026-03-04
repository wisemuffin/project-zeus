import io
import re
import zipfile

import dagster as dg
import pandas as pd
import requests

ESS_URL = (
    "https://www.qilt.edu.au/docs/default-source/default-document-library/"
    "ess_2024_national_report_tables.zip"
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


def _extract_point_estimate(value) -> float | None:
    """Extract the point estimate from 'XX.X (lower, upper)' format."""
    if pd.isna(value) or str(value).strip() == "":
        return None
    s = str(value).strip()
    m = re.match(r"^([\d,]+(?:\.\d+)?)", s.replace(" ", ""))
    if m:
        return float(m.group(1).replace(",", ""))
    return None


def _parse_ess_by_field(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse ESS employer satisfaction by Broad Field of Education."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name="EMPSAT_ALL_UNI_1Y_BFOE",
        header=3,
        engine="openpyxl",
    )

    # First two columns are group header and field name; rename
    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "broad_field_of_education"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    raw = raw[raw["broad_field_of_education"].notna()].copy()
    raw = raw[~raw["broad_field_of_education"].str.contains(
        "All Fields|Total|All broad fields", na=False
    )].copy()
    raw = raw[raw["broad_field_of_education"].astype(str).str.strip() != ""].copy()
    raw["broad_field_of_education"] = (
        raw["broad_field_of_education"].str.strip().str.replace("\xa0", " ")
    )

    # Strip column name whitespace and non-breaking spaces
    raw.columns = [
        c.strip().replace("\xa0", " ") if isinstance(c, str) else c
        for c in raw.columns
    ]

    # Map ESS column names (with "%" suffix) to snake_case
    ess_rename = {
        "foundation skills": "foundation_skills",
        "adaptive skills": "adaptive_skills",
        "collaborative skills": "collaborative_skills",
        "technical skills": "technical_skills",
        "employability skills": "employability_skills",
        "overall satisfaction": "overall_employer_satisfaction",
    }

    for old_pattern, new_name in ess_rename.items():
        matched = [c for c in raw.columns if old_pattern in c.lower()]
        if matched:
            raw[new_name] = raw[matched[0]].apply(_extract_point_estimate)

    keep = ["broad_field_of_education"] + list(ess_rename.values())
    return raw[[c for c in keep if c in raw.columns]].reset_index(drop=True)


def _parse_ess_by_institution(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse ESS employer satisfaction by institution (3-year pooled)."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name="EMPSAT_ALL_UNI_3YP",
        header=3,
        engine="openpyxl",
    )

    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "institution"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    raw = raw[raw["institution"].notna()].copy()
    raw = raw[~raw["institution"].str.contains("All Universities|Total", na=False)].copy()
    raw = raw[raw["institution"].astype(str).str.strip() != ""].copy()
    raw["institution"] = raw["institution"].str.strip().str.replace("\xa0", " ")

    raw.columns = [
        c.strip().replace("\xa0", " ") if isinstance(c, str) else c
        for c in raw.columns
    ]

    ess_rename = {
        "foundation skills": "foundation_skills",
        "adaptive skills": "adaptive_skills",
        "collaborative skills": "collaborative_skills",
        "technical skills": "technical_skills",
        "employability skills": "employability_skills",
        "overall satisfaction": "overall_employer_satisfaction",
    }

    for old_pattern, new_name in ess_rename.items():
        matched = [c for c in raw.columns if old_pattern in c.lower()]
        if matched:
            raw[new_name] = raw[matched[0]].apply(_extract_point_estimate)

    keep = ["institution"] + list(ess_rename.values())
    return raw[[c for c in keep if c in raw.columns]].reset_index(drop=True)


@dg.asset(
    group_name="employer_satisfaction",
    tags={"source": "qilt", "domain": "employer_satisfaction", "update_frequency": "annual", "ingestion": "file_download"},
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 10 *"),
)
def qilt_employer_satisfaction_by_field(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """QILT Employer Satisfaction Survey — satisfaction by Broad Field of Education.

    Source: Quality Indicators for Learning and Teaching (QILT), Australian
        Government. Employer Satisfaction Survey (ESS) 2024 national report
        tables. Covers employer ratings of graduate skills across 6 dimensions.
    Marketing use: **What message** — adds employer-side proof points for
        marketing creative. "89% of employers rate Engineering graduates'
        technical skills positively" complements graduate employment data
        with the employer perspective.
    Format: broad_field_of_education, foundation_skills, adaptive_skills,
        collaborative_skills, technical_skills, employability_skills,
        overall_employer_satisfaction (all % positive ratings)
    Limitations:
    - Uses ASCED broad field names (not QILT 21-study-area names)
    - Values with <5 respondents suppressed (appear as null)
    - Single-year snapshot (no prior-year comparison available)
    - URL may change when 2025 data is published (~September 2026)
    """
    context.log.info("Downloading ESS employer satisfaction data...")
    xlsx_bytes = _extract_xlsx(ESS_URL)
    context.log.info("ESS ZIP extracted")

    df = _parse_ess_by_field(xlsx_bytes)
    context.log.info(f"Parsed {len(df)} fields from ESS by-field sheet")

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "source_url": dg.MetadataValue.url(
            "https://www.qilt.edu.au/surveys/employer-satisfaction-survey"
        ),
        "survey_year": dg.MetadataValue.text("2024"),
        "preview": dg.MetadataValue.md(
            df.to_markdown(index=False, floatfmt=".1f")
        ),
    })

    return df


@dg.asset(
    group_name="employer_satisfaction",
    tags={"source": "qilt", "domain": "employer_satisfaction", "update_frequency": "annual", "ingestion": "file_download"},
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 10 *"),
)
def qilt_employer_satisfaction_by_institution(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """QILT Employer Satisfaction Survey — satisfaction by institution (3-year pooled).

    Source: Quality Indicators for Learning and Teaching (QILT), Australian
        Government. Employer Satisfaction Survey (ESS) 2024 national report
        tables. 3-year pooled data for statistical reliability at institution level.
    Marketing use: **Who to target** — enables per-university employer satisfaction
        benchmarking. "Employers rate University X graduates 4.2pp above the sector
        average on technical skills" for competitive positioning.
    Format: institution, foundation_skills, adaptive_skills, collaborative_skills,
        technical_skills, employability_skills, overall_employer_satisfaction
        (all % positive ratings, 3-year pooled)
    Limitations:
    - 3-year pooled to achieve sample sizes — less responsive to recent changes
    - Not all universities have sufficient employer responses for all skill areas
    - Values with <5 respondents suppressed (appear as null)
    - URL may change when 2025 data is published (~September 2026)
    """
    context.log.info("Downloading ESS employer satisfaction data...")
    xlsx_bytes = _extract_xlsx(ESS_URL)
    context.log.info("ESS ZIP extracted")

    df = _parse_ess_by_institution(xlsx_bytes)
    context.log.info(f"Parsed {len(df)} institutions from ESS by-institution sheet")

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "source_url": dg.MetadataValue.url(
            "https://www.qilt.edu.au/surveys/employer-satisfaction-survey"
        ),
        "survey_year": dg.MetadataValue.text("2024 (3-year pooled)"),
        "preview": dg.MetadataValue.md(
            df.to_markdown(index=False, floatfmt=".1f")
        ),
    })

    return df
