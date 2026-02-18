import io
import zipfile

import dagster as dg
import pandas as pd
import requests

SES_URL = (
    "https://www.qilt.edu.au/docs/default-source/default-document-library/"
    "ses_2024_national_report_tables.zip"
)

_SHEET_BY_AREA = "FOCUS_UG_ALL_1Y_AREA"
_HEADER_ROWS = 3

_COLUMN_NAMES = {
    "Focus areas: Skills Development": "skills_development",
    "Focus areas: Peer Engagement *": "peer_engagement",
    "Focus areas: Teaching Quality and Engagement": "teaching_quality",
    "Focus areas: Student Support and Services *": "student_support",
    "Focus areas: Learning Resources": "learning_resources",
    "Questionnaire item: Overall Educational Experience": "overall_quality",
}


def _parse_ses_by_area(xlsx_bytes: bytes) -> pd.DataFrame:
    """Parse SES satisfaction indicators by study area."""
    raw = pd.read_excel(
        io.BytesIO(xlsx_bytes),
        sheet_name=_SHEET_BY_AREA,
        header=_HEADER_ROWS,
        engine="openpyxl",
    )
    cols = list(raw.columns)
    raw.rename(columns={cols[0]: "_group", cols[1]: "study_area"}, inplace=True)
    raw.drop(columns=["_group"], inplace=True)

    raw = raw[raw["study_area"].notna()].copy()
    raw = raw[~raw["study_area"].isin(["Total", "Standard deviation"])].copy()
    raw = raw[raw["study_area"].astype(str).str.strip() != ""].copy()

    # Strip trailing whitespace from column names (QILT Excel has trailing spaces)
    raw.columns = [c.strip() if isinstance(c, str) else c for c in raw.columns]
    rename = {k: v for k, v in _COLUMN_NAMES.items() if k in raw.columns}
    raw.rename(columns=rename, inplace=True)

    keep = ["study_area"] + list(rename.values())
    df = raw[keep].copy()

    for col in list(rename.values()):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["study_area"] = df["study_area"].str.strip().str.replace("\xa0", " ")
    return df.reset_index(drop=True)


@dg.asset(
    group_name="student_experience",
    tags={"source": "qilt", "domain": "student_experience", "update_frequency": "annual"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 10 *"),
)
def qilt_student_experience(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """QILT Student Experience Survey (SES) — satisfaction by study area.

    Source: Quality Indicators for Learning and Teaching (QILT), Australian
        Government. Annual survey of 258,000+ students across all Australian
        universities and non-university providers.
    Marketing use: **What message** — satisfaction scores enable claims like
        "92% of Education students rate teaching quality positively". Comparing
        across fields highlights relative strengths and weaknesses.
    Format: study_area, skills_development, peer_engagement, teaching_quality,
        student_support, learning_resources, overall_quality (all % positive)
    Limitations:
    - Undergraduate only (postgraduate available but not yet ingested)
    - Percentages are % positive rating (agree/strongly agree), not means
    - Study areas use QILT/ASCED classification — requires mapping for UAC joins
    - Peer Engagement and Student Support items were revised in 2023
    - URL may change when 2025 data is published (~September 2026)
    """
    context.log.info(f"Downloading SES report tables: {SES_URL}")
    response = requests.get(SES_URL, timeout=120)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        xlsx_names = [n for n in zf.namelist() if n.endswith(".xlsx")]
        if not xlsx_names:
            raise RuntimeError(f"No .xlsx file found in ZIP. Contents: {zf.namelist()}")
        xlsx_bytes = zf.read(xlsx_names[0])

    context.log.info(f"Extracted {xlsx_names[0]} ({len(xlsx_bytes):,} bytes)")

    df = _parse_ses_by_area(xlsx_bytes)
    context.log.info(f"Parsed {len(df)} study areas with satisfaction data")

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(df)),
            "source_url": dg.MetadataValue.url(SES_URL),
            "survey_year": dg.MetadataValue.text("2024"),
            "preview": dg.MetadataValue.md(
                df.to_markdown(index=False, floatfmt=".1f")
            ),
        }
    )

    return df
