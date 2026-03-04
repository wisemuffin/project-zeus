import dagster as dg
import pandas as pd
import requests

_BASE_URL = "https://www.courseseeker.edu.au/search-engine/courses/course/_search"
_PAGE_SIZE = 500


def _fetch_all_courses_with_atar() -> list[dict]:
    """Paginate through the CourseSeeker Elasticsearch API to get all courses with ATAR data."""
    all_hits = []
    offset = 0

    while True:
        payload = {
            "size": _PAGE_SIZE,
            "from": offset,
            "_source": [
                "name",
                "courseCodeTac",
                "admissionCentre",
                "institutionName",
                "institution",
                "isUniversity",
                "studyArea",
                "studyAreaCode",
                "studyAreaPrimary",
                "levelOfQualificationDesc",
                "states",
                "campuses",
                "studyModes",
                "attendanceModes",
                "duration",
                "atarProfile",
                "studentProfile",
            ],
            "query": {
                "bool": {
                    "must": [
                        {"exists": {"field": "atarProfile.lowestAtarUnadjusted"}}
                    ]
                }
            },
        }

        resp = requests.post(_BASE_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break

        all_hits.extend(hits)
        offset += len(hits)

        total = data.get("hits", {}).get("total", 0)
        if offset >= total:
            break

    return all_hits


def _flatten_hit(hit: dict) -> dict:
    """Flatten an Elasticsearch hit into a flat dict for DataFrame construction."""
    src = hit["_source"]
    atar = src.get("atarProfile") or {}
    student = src.get("studentProfile") or {}

    # Extract first campus state + name
    campuses = src.get("campuses") or []
    campus_name = campuses[0].get("campusName") if campuses else None
    campus_state = campuses[0].get("state") if campuses else None

    # States list → first state
    states = src.get("states") or []
    primary_state = states[0] if states else campus_state

    return {
        "course_name": src.get("name"),
        "course_code_tac": src.get("courseCodeTac"),
        "admission_centre": src.get("admissionCentre"),
        "institution_name": src.get("institutionName"),
        "institution_code": src.get("institution"),
        "is_university": src.get("isUniversity") == "T",
        "study_area": src.get("studyArea"),
        "study_area_code": (src.get("studyAreaCode") or [None])[0],
        "study_area_primary": src.get("studyAreaPrimary"),
        "level_of_qualification": src.get("levelOfQualificationDesc"),
        "state": primary_state,
        "campus_name": campus_name,
        "study_modes": src.get("studyModes"),
        "attendance_modes": src.get("attendanceModes"),
        "duration": src.get("duration"),
        # ATAR profile
        "atar_collection_year": atar.get("collectionYear"),
        "lowest_atar_unadjusted": _safe_float(atar.get("lowestAtarUnadjusted")),
        "lowest_atar_adjusted": _safe_float(atar.get("lowestAtarAdjusted")),
        "highest_atar_unadjusted": _safe_float(atar.get("highestAtarUnadjusted")),
        "highest_atar_adjusted": _safe_float(atar.get("highestAtarAdjusted")),
        "median_atar_unadjusted": _safe_float(atar.get("medianAtarUnadjusted")),
        "median_atar_adjusted": _safe_float(atar.get("medianAtarAdjusted")),
        # Student profile (admission basis breakdown)
        "student_profile_year": student.get("collectionYear"),
        "pct_admitted_atar": _safe_float(student.get("percAdmittedAtar")),
        "pct_admitted_he": _safe_float(student.get("percAdmittedHe")),
        "pct_admitted_vet": _safe_float(student.get("percAdmittedVet")),
        "pct_admitted_other": _safe_float(student.get("percAdmittedOther")),
        "pct_international": _safe_float(student.get("percInternational")),
        "total_students": _safe_int(student.get("totalStudents")),
    }


def _safe_float(val) -> float | None:
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _safe_int(val) -> int | None:
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


@dg.asset(
    group_name="course_offerings",
    tags={
        "source": "courseseeker",
        "domain": "course_offerings",
        "update_frequency": "annual",
        "ingestion": "api",
    },
    kinds={"python", "api"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 15 1 *"),
)
def courseseeker_atar(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """CourseSeeker course data with ATAR profiles and student admission breakdown.

    Source: courseseeker.edu.au — a joint initiative of the Australian Government
        and Tertiary Admission Centres. Data sourced from the site's public
        Elasticsearch API (no authentication required). Covers ~5,300 courses
        with ATAR selection rank data across all Australian universities.
    Marketing use: **What message** — ATAR data adds entry requirement context
        to course-level marketing. "This Engineering program accepts students
        from ATAR 68 — more accessible than you might think" or identifying
        high-ATAR programs for prestige positioning. Student profile data
        shows admission basis mix (ATAR vs VET vs mature entry).
    Format: course_name, institution_name, study_area, state, ATAR profile
        (lowest/median/highest, adjusted/unadjusted), student profile
        (admission basis percentages)
    Limitations:
    - ATAR collection years vary by course (some as old as 2020)
    - Not all courses report ATAR data (~5,300 of ~10,500 total courses)
    - Student profile data is sparser than ATAR profile data
    - API is undocumented — endpoint may change without notice
    - Adjusted ATARs include equity/bonus points, unadjusted are raw scores
    """
    context.log.info("Fetching CourseSeeker courses with ATAR data...")
    hits = _fetch_all_courses_with_atar()
    context.log.info(f"Fetched {len(hits)} courses with ATAR data")

    records = [_flatten_hit(h) for h in hits]
    df = pd.DataFrame(records)

    # Filter to universities only (exclude TAFE/pathway colleges for cleaner joins)
    uni_count_before = len(df)
    df_unis = df[df["is_university"]].copy()
    context.log.info(
        f"Filtered to {len(df_unis)} university courses "
        f"(dropped {uni_count_before - len(df_unis)} non-university)"
    )

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df_unis)),
        "total_courses_with_atar": dg.MetadataValue.int(len(df)),
        "university_courses": dg.MetadataValue.int(len(df_unis)),
        "unique_institutions": dg.MetadataValue.int(
            df_unis["institution_name"].nunique()
        ),
        "source_url": dg.MetadataValue.url("https://www.courseseeker.edu.au/"),
        "preview": dg.MetadataValue.md(
            df_unis[["course_name", "institution_name", "study_area", "state",
                      "lowest_atar_unadjusted", "median_atar_unadjusted"]]
            .head(20)
            .to_markdown(index=False, floatfmt=".1f")
        ),
    })

    return df_unis
