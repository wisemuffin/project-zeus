import dagster as dg
import pandas as pd
import requests
from bs4 import BeautifulSoup

VTAC_SECTION_D_URL = (
    "https://vtac.edu.au/statistics/stats20-21/stats2020-21-sectiond.html"
)


@dg.asset(
    group_name="vtac_data",
    tags={"source": "vtac", "domain": "preferences", "update_frequency": "annual", "ingestion": "web_scraping"},
    kinds={"python", "scraping"},
)
def vtac_fos_preferences(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """VTAC field-of-study first preferences by gender (Victoria).

    Source: VTAC annual statistics Section D (Table D1), HTML, public, annual
    Marketing use: **What message** + **Where** — Victorian applicant preference
        shares by field and gender, enabling cross-state comparison with UAC
        (NSW/ACT). Differences reveal state-specific demand signals for
        geo-targeted campaigns.
    Format: field_of_study, gender (Female | Male | Total), first_preferences,
        preference_share (0-1), total_offers, enrolments
    Limitations:
    - 2020-21 data (latest confirmed year with full Section D tables)
    - Victoria only (~25% of national applicants)
    - ASCED broad field classification (11 fields + Mixed Field Programs)
    - HTML table requires parsing; structure may change between years
    """
    response = requests.get(VTAC_SECTION_D_URL, timeout=60)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # The page has multiple tables; the first is a title-only table.
    # Find the data table by looking for one that contains "Female" in a cell.
    table = None
    for t in soup.find_all("table"):
        if t.find(string=lambda s: s and "Female" in s):
            table = t
            break
    if table is None:
        raise ValueError(f"No data table found at {VTAC_SECTION_D_URL}")

    rows = table.find_all("tr")

    parsed_rows = []
    current_field = None

    for row in rows:
        cells = row.find_all(["td", "th"])
        texts = [c.get_text(strip=True) for c in cells]

        if not texts or len(texts) < 2:
            continue

        first_cell = texts[0]

        # Skip header rows
        if first_cell in ("ASCED Field of Interest", "First Preferences", ""):
            # Check if this is actually a gender sub-row with empty first cell
            if first_cell == "" and len(texts) >= 7:
                gender_candidate = texts[0] if texts[0] in ("Female", "Male", "Total") else None
                if gender_candidate is None:
                    continue
            else:
                continue

        # Detect field-of-study header rows vs gender data rows.
        # Gender-only rows (Male/Total) have 8 cells: gender + 7 data columns.
        # Field name rows have 9 cells: field + gender(Female) + 7 data columns.
        if first_cell in ("Female", "Male", "Total"):
            gender = first_cell
            data_cells = texts[1:]
        elif len(texts) >= 9 and texts[1] in ("Female", "Male", "Total"):
            # Field name + gender data in the same row
            current_field = first_cell
            gender = texts[1]
            data_cells = texts[2:]
        else:
            # Field-of-study name only (no inline gender data)
            current_field = first_cell
            continue

        if current_field is None:
            continue

        # Parse numeric columns: First Preferences, % of FP, Total Offers, Enrolments
        try:
            first_prefs = _parse_int(data_cells[0])
            pref_share = _parse_float(data_cells[1]) / 100  # Convert % to decimal
            total_offers = _parse_int(data_cells[2])
            enrolments = _parse_int(data_cells[3])
        except (IndexError, ValueError):
            context.log.warning(
                f"Skipping malformed row: field={current_field}, gender={gender}"
            )
            continue

        parsed_rows.append({
            "field_of_study": current_field,
            "gender": gender,
            "first_preferences": first_prefs,
            "preference_share": pref_share,
            "total_offers": total_offers,
            "enrolments": enrolments,
        })

    df = pd.DataFrame(parsed_rows)

    if df.empty:
        raise ValueError("Parsed zero rows from VTAC Section D table")

    context.log.info(f"Parsed {len(df)} rows from VTAC Section D (Table D1)")

    n_fields = df["field_of_study"].nunique()
    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "fields_of_study": dg.MetadataValue.int(n_fields),
        "source_url": dg.MetadataValue.url(VTAC_SECTION_D_URL),
    })

    return df


def _parse_int(val: str) -> int:
    return int(val.replace(",", "").strip())


def _parse_float(val: str) -> float:
    return float(val.replace(",", "").strip())
