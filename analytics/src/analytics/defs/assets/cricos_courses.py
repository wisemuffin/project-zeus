import dagster as dg
import pandas as pd
import requests

_BASE = (
    "https://data.gov.au/data/dataset/"
    "e5ae7059-bfa8-4fa4-a5c0-c13cf3520193/resource"
)
_URLS = {
    "institutions": f"{_BASE}/7f6941f3-5327-4db7-b556-5f16d77f63c1/download/cricos-institutions.csv",
    "courses": f"{_BASE}/48cacf69-2082-415e-9595-f17d0c3a4af0/download/cricos-courses.csv",
    "locations": f"{_BASE}/45d29535-1360-4486-8242-3850e61b5524/download/cricos-locations.csv",
    "course_locations": f"{_BASE}/4cd2de02-8ba3-4eb2-bac2-fe272cae3f5f/download/cricos-course-locations.csv",
}

# Higher-education course levels to keep (exclude VET certificates, diplomas,
# ELICOS, Senior Secondary, Non-award, Foundation programmes).
_HE_LEVELS = {
    "Bachelor Degree",
    "Bachelor Honours Degree",
    "Bachelor/Graduate Entry Bachelor Degree",
    "Masters Degree (Coursework)",
    "Masters Degree (Extended)",
    "Masters Degree (Research)",
    "Doctoral Degree",
    "Graduate Diploma",
    "Graduate Certificate",
    "Associate Degree",
    "Advanced Diploma",
    "Higher Education Diploma",
}


def _download_csv(url: str, context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Download a CSV from data.gov.au and return as a DataFrame."""
    context.log.info(f"Downloading {url.split('/')[-1]}")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    from io import BytesIO

    # data.gov.au CSVs include a UTF-8 BOM — use utf-8-sig to strip it
    return pd.read_csv(BytesIO(resp.content), encoding="utf-8-sig")


@dg.asset(
    group_name="course_listings",
    tags={"source": "cricos", "domain": "course_listings", "update_frequency": "weekly"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 * * 1"),
)
def cricos_courses(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """CRICOS course listings — higher-education courses across Australian institutions.

    Source: Commonwealth Register of Institutions and Courses for Overseas
        Students (CRICOS), published by the Department of Education on
        data.gov.au under Creative Commons Attribution 2.5 Australia.
        Four relational CSVs (institutions, courses, locations,
        course-locations) joined into a denormalized listing.
    Marketing use: **What message + Where** — connects opportunity gap fields
        to named programs at specific institutions and campuses. Enables
        "University X offers 3 Engineering programs in NSW" style
        recommendations. Joined with QILT outcomes, supports per-program
        ROI messaging for campaign creative.
    Format: cricos_provider_code, institution_name, institution_type,
        cricos_course_code, course_name, course_level, broad_field,
        narrow_field, duration_weeks, estimated_total_cost,
        location_state, location_city
    Limitations:
    - International-student-registered courses only (most university courses
      are registered, but some domestic-only programs may be absent)
    - No ATAR/entry requirement data
    - No delivery mode (online vs on-campus)
    - ASCED field-of-study codes require mapping to UAC categories in dbt
    - Snapshot from data.gov.au — may lag the live CRICOS register by weeks
    """
    institutions = _download_csv(_URLS["institutions"], context)
    courses = _download_csv(_URLS["courses"], context)
    locations = _download_csv(_URLS["locations"], context)
    course_locs = _download_csv(_URLS["course_locations"], context)

    context.log.info(
        f"Raw counts — institutions: {len(institutions)}, "
        f"courses: {len(courses)}, locations: {len(locations)}, "
        f"course_locations: {len(course_locs)}"
    )

    # Filter out expired courses
    courses = courses[courses["Expired"].str.strip().str.lower() != "yes"].copy()
    context.log.info(f"After removing expired: {len(courses)} courses")

    # Filter to higher-education levels
    courses = courses[courses["Course Level"].isin(_HE_LEVELS)].copy()
    context.log.info(f"After HE filter: {len(courses)} courses")

    # Join course-locations for state/city per delivery site
    # course_locations has: CRICOS Provider Code, CRICOS Course Code,
    #   Location City, Location State
    df = courses.merge(
        course_locs[
            ["CRICOS Provider Code", "CRICOS Course Code", "Location City", "Location State"]
        ],
        on=["CRICOS Provider Code", "CRICOS Course Code"],
        how="left",
    )

    # Join institutions for institution type
    inst_cols = institutions[
        ["CRICOS Provider Code", "Institution Type"]
    ].drop_duplicates()
    df = df.merge(inst_cols, on="CRICOS Provider Code", how="left")

    # Select and rename output columns
    df = df.rename(
        columns={
            "CRICOS Provider Code": "cricos_provider_code",
            "Institution Name": "institution_name",
            "Institution Type": "institution_type",
            "CRICOS Course Code": "cricos_course_code",
            "Course Name": "course_name",
            "Course Level": "course_level",
            "Field of Education 1 Broad Field": "broad_field",
            "Field of Education 1 Narrow Field": "narrow_field",
            "Duration (Weeks)": "duration_weeks",
            "Estimated Total Course Cost": "estimated_total_cost",
            "Location State": "location_state",
            "Location City": "location_city",
        }
    )

    # Clean cost column — strip $ and commas, convert to numeric
    df["estimated_total_cost"] = (
        df["estimated_total_cost"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["estimated_total_cost"] = pd.to_numeric(
        df["estimated_total_cost"], errors="coerce"
    )

    df["duration_weeks"] = pd.to_numeric(df["duration_weeks"], errors="coerce")

    output_cols = [
        "cricos_provider_code",
        "institution_name",
        "institution_type",
        "cricos_course_code",
        "course_name",
        "course_level",
        "broad_field",
        "narrow_field",
        "duration_weeks",
        "estimated_total_cost",
        "location_state",
        "location_city",
    ]
    df = df[output_cols].copy()

    institution_count = df["institution_name"].nunique()
    context.log.info(
        f"Final: {len(df)} rows across {institution_count} institutions"
    )

    context.add_output_metadata(
        {
            "row_count": dg.MetadataValue.int(len(df)),
            "institution_count": dg.MetadataValue.int(institution_count),
            "source_url": dg.MetadataValue.url(
                "https://data.gov.au/data/dataset/cricos"
            ),
            "course_levels": dg.MetadataValue.md(
                df["course_level"].value_counts().to_markdown()
            ),
        }
    )

    return df
