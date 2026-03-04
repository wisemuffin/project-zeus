import xml.etree.ElementTree as ET
import zipfile
from io import BytesIO

import dagster as dg
import pandas as pd
import requests

PIVOT_URL = (
    "https://www.education.gov.au/download/19507/"
    "perturbed-student-enrolments-pivot-table-2024/41971/document/xlsx"
)

_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _extract_pivot_cache(xlsx_bytes: bytes) -> pd.DataFrame:
    """Extract flat records from an Excel pivot cache.

    Excel pivot tables store the underlying data in
    xl/pivotCache/pivotCacheRecords1.xml with shared-item lookups defined in
    pivotCacheDefinition1.xml.  This function parses both to reconstruct
    the original record set without needing to open the file in Excel.
    """
    with zipfile.ZipFile(BytesIO(xlsx_bytes), "r") as zf:
        defn_xml = zf.read("xl/pivotCache/pivotCacheDefinition1.xml")
        defn_root = ET.fromstring(defn_xml)

        fields: list[dict] = []
        for cf in defn_root.findall(f".//{_NS}cacheField"):
            name = cf.get("name")
            shared = cf.find(f"{_NS}sharedItems")
            if shared is not None and shared.get("count"):
                lookup = [s.get("v") for s in shared]
            else:
                lookup = None
            fields.append({"name": name, "lookup": lookup})

        recs_xml = zf.read("xl/pivotCache/pivotCacheRecords1.xml")
        recs_root = ET.fromstring(recs_xml)

        rows: list[dict] = []
        for rec in recs_root.findall(f"{_NS}r"):
            row: dict = {}
            for i, child in enumerate(rec):
                field = fields[i]
                tag = child.tag.replace(_NS, "")
                if tag == "x":
                    row[field["name"]] = field["lookup"][int(child.get("v"))]
                elif tag == "n":
                    row[field["name"]] = float(child.get("v"))
                elif tag == "s":
                    row[field["name"]] = child.get("v")
                else:
                    row[field["name"]] = None
            rows.append(row)

    return pd.DataFrame(rows)


_KEEP_COLUMNS = [
    "year",
    "institution",
    "state",
    "citizenship",
    "commencing",
    "broad_course_level",
    "detailed_course_level",
    "gender",
    "mode_of_attendance",
    "special_course",
    "type_of_attendance",
    "broad_field_of_education_primary",
    "broad_field_of_education_secondary",
    "enrolment_count",
]


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise column names and types for DuckDB storage."""
    # Normalize spaces to underscores first (2024 file uses underscored names)
    df.columns = df.columns.str.replace(" ", "_")

    df = df.rename(columns={
        "Year": "year",
        "Institution": "institution",
        "State": "state",
        "Citizenship": "citizenship",
        "Commencing": "commencing",
        "Broad_Course_Level": "broad_course_level",
        "Detailed_Course_Level": "detailed_course_level",
        "Gender": "gender",
        "Mode_Of_Attendance": "mode_of_attendance",
        "Special_Course": "special_course",
        "Type_Of_Attendance": "type_of_attendance",
        "Broad_Field_of_Education_Primary": "broad_field_of_education_primary",
        "Broad_Field_of_Education_Secondary": "broad_field_of_education_secondary",
        "Enrolment_Count": "enrolment_count",
    })

    # Keep only the 14 columns we need (drop per-FoE count columns from 2024 file)
    df = df[[c for c in _KEEP_COLUMNS if c in df.columns]]

    df["enrolment_count"] = pd.to_numeric(df["enrolment_count"], errors="coerce")

    return df


@dg.asset(
    group_name="higher_education_enrolments",
    tags={
        "source": "det",
        "domain": "higher_education_enrolments",
        "update_frequency": "annual",
        "ingestion": "file_download",
    },
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 10 *"),
)
def det_he_enrolments(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """DET Higher Education Student Enrolments — institution × field × citizenship × mode.

    Source: Department of Education, Australian Government. Perturbed Student
        Enrolments Pivot Table 2024. Covers all Table A universities plus
        non-university HE providers (2020-2024, ~235K records).
    Marketing use: **Who** and **Where** — shows domestic vs international
        enrolment mix by field and institution. Enables messaging like "Your
        Engineering faculty is 45% international — here's how to diversify
        your domestic pipeline" or "External mode grew 30% — target working
        adults". Mode of attendance data supports online vs on-campus
        targeting decisions.
    Format: institution, year, broad_field_of_education, citizenship,
        mode_of_attendance, gender, course_level, enrolment_count
    Limitations:
    - Covers 2020-2024 (5 years). Counts are perturbed (small random
      adjustments) for disclosure control — totals are accurate but
      individual cells may differ slightly from true values.
    - Enrolment counts are pre-aggregated across dimensions in the pivot
      cache — some cross-tab combinations have small cell sizes.
    - Field of education uses ASCED broad categories (13 fields) — requires
      mapping for joins with UAC preference data.
    - "Non-University Higher Education Providers" are grouped as one entity.
    """
    context.log.info(f"Downloading DET HE enrolments pivot table: {PIVOT_URL}")
    response = requests.get(PIVOT_URL, timeout=120)
    response.raise_for_status()

    context.log.info(
        f"Downloaded {len(response.content):,} bytes, extracting pivot cache..."
    )
    df = _extract_pivot_cache(response.content)
    df = _clean_dataframe(df)

    context.log.info(
        f"Extracted {len(df):,} records: "
        f"{df['institution'].nunique()} institutions, "
        f"{sorted(df['year'].dropna().unique())} years"
    )

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "institutions": dg.MetadataValue.int(df["institution"].nunique()),
        "years": dg.MetadataValue.text(
            f"{int(df['year'].min())}-{int(df['year'].max())}"
        ),
        "source_url": dg.MetadataValue.url(PIVOT_URL),
        "fields_of_education": dg.MetadataValue.text(
            ", ".join(sorted(df["broad_field_of_education_primary"].dropna().unique()))
        ),
        "preview": dg.MetadataValue.md(
            df.groupby(["year", "citizenship"])["enrolment_count"]
            .sum()
            .reset_index()
            .to_markdown(index=False, floatfmt=",.0f")
        ),
    })

    return df
