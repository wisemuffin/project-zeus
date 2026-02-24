import tempfile

import dagster as dg
import pandas as pd
import pdfplumber
import requests

SATAC_FOS_URL = (
    "https://www.satac.edu.au/documents/"
    "undergraduate-first-preferences-and-total-offers-by-broad-field-of-study-2025"
)

# Groups appear in this order in the PDF; we sum the first two for domestic totals
GROUP_ORDER = ["Current Year 12", "Non-Year 12", "International"]
DOMESTIC_GROUPS = {"Current Year 12", "Non-Year 12"}

HEADER_MARKER = "ASCED Field of interest"


@dg.asset(
    group_name="satac_data",
    tags={"source": "satac", "domain": "preferences", "update_frequency": "annual", "ingestion": "pdf_extraction"},
    kinds={"python", "pdf"},
)
def satac_fos_preferences(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """SATAC field-of-study first preferences by gender (SA/NT).

    Source: SATAC annual statistics PDF, 2025, public, annual
    Marketing use: **What message** + **Where** — South Australian / Northern
        Territory applicant preference shares by field and gender. Extends the
        national cross-state comparison alongside UAC (NSW/ACT) and VTAC (VIC),
        bringing coverage to ~72% of Australian applicants.
    Format: field_of_study, gender (Female | Male | Total), first_preferences,
        preference_share (0-1), total_offers
    Limitations:
    - 2025 data only (single year, no historical trend)
    - SA/NT only (~7% of national applicants)
    - ASCED broad field classification (10 fields — Food/Hospitality absent in SA)
    - PDF table extraction with pdfplumber; layout may change between years
    - Year 12 + Non-Year 12 summed to produce domestic totals (no single combined
      table in source)
    """
    # Download PDF (URL redirects to S3-hosted file)
    response = requests.get(SATAC_FOS_URL, timeout=60, allow_redirects=True)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp.flush()

        tables_by_group = _extract_tables(tmp.name, context)

    # Keep only domestic groups and sum across them
    domestic_tables = [
        tables_by_group[g] for g in DOMESTIC_GROUPS if g in tables_by_group
    ]

    if not domestic_tables:
        raise ValueError(
            f"No domestic applicant tables found. Groups found: {list(tables_by_group)}"
        )

    context.log.info(
        f"Summing domestic groups: {[g for g in DOMESTIC_GROUPS if g in tables_by_group]}"
    )

    combined = pd.concat(domestic_tables, ignore_index=True)

    # Sum first_preferences and total_offers across Year 12 + Non-Year 12
    df = (
        combined.groupby(["field_of_study", "gender"], as_index=False)
        .agg({"first_preferences": "sum", "total_offers": "sum"})
    )

    # Compute preference_share from summed counts (per gender group)
    for gender in df["gender"].unique():
        mask = df["gender"] == gender
        total = df.loc[mask, "first_preferences"].sum()
        if total > 0:
            df.loc[mask, "preference_share"] = df.loc[mask, "first_preferences"] / total

    df = df[["field_of_study", "gender", "first_preferences", "preference_share", "total_offers"]]

    if df.empty:
        raise ValueError("Parsed zero rows from SATAC PDF")

    context.log.info(f"Parsed {len(df)} rows from SATAC field-of-study preferences")

    n_fields = df["field_of_study"].nunique()
    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "fields_of_study": dg.MetadataValue.int(n_fields),
        "source_url": dg.MetadataValue.url(SATAC_FOS_URL),
    })

    return df


def _extract_tables(
    pdf_path: str, context: dg.AssetExecutionContext
) -> dict[str, pd.DataFrame]:
    """Extract field-of-study tables from the PDF, keyed by applicant group.

    The PDF has 3 applicant-group tables (Current Year 12, Non-Year 12,
    International) that each span 2 pages. We flatten all extracted tables
    into a single row stream and split groups on the summary "Total" row
    that ends each group.
    """
    # Collect all table rows across all pages in order
    all_rows: list[list[str]] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    cleaned = [_clean(c) for c in row]
                    # Skip header rows (repeated on each page)
                    if cleaned[0] == HEADER_MARKER:
                        continue
                    all_rows.append(cleaned)

    # Split rows into groups by "Total" summary rows
    # Each group ends with a "Total" field row (3 sub-rows: Female/Male/Total)
    groups: list[list[dict]] = []
    current_group: list[dict] = []
    current_field: str | None = None

    for cells in all_rows:
        first = cells[0]
        gender = cells[1] if len(cells) > 1 else ""

        # Row with field name in first column (+ Female data in same row)
        if first and first != "Total":
            current_field = first
            # This row also contains Female data
            if gender == "Female" and len(cells) >= 6:
                try:
                    current_group.append({
                        "field_of_study": current_field,
                        "gender": "Female",
                        "first_preferences": _parse_int(cells[2]),
                        "total_offers": _parse_int(cells[5]),
                    })
                except (ValueError, IndexError):
                    context.log.warning(f"Skipping malformed Female row: {cells}")

        # Continuation row (None in first column, Male or Total in second)
        elif not first and gender in ("Male", "Total"):
            if current_field is None:
                continue
            try:
                current_group.append({
                    "field_of_study": current_field,
                    "gender": gender,
                    "first_preferences": _parse_int(cells[2]),
                    "total_offers": _parse_int(cells[5]),
                })
            except (ValueError, IndexError):
                context.log.warning(f"Skipping malformed {gender} row: {cells}")

        # "Total" summary field — ends this group
        elif first == "Total":
            if current_group:
                groups.append(current_group)
                context.log.info(
                    f"Group {len(groups)}: {len(current_group)} data rows"
                )
                current_group = []
                current_field = None

    # Catch any trailing group
    if current_group:
        groups.append(current_group)

    # Map groups to named labels
    tables_by_group: dict[str, pd.DataFrame] = {}
    for i, group_rows in enumerate(groups):
        if i < len(GROUP_ORDER):
            name = GROUP_ORDER[i]
            tables_by_group[name] = pd.DataFrame(group_rows)
            context.log.info(f"{name}: {len(group_rows)} rows parsed")

    return tables_by_group


def _clean(val: str | None) -> str:
    """Clean cell value: strip whitespace, carriage returns, and newlines."""
    if val is None:
        return ""
    return val.replace("\r", " ").replace("\n", " ").strip()


def _parse_int(val: str) -> int:
    return int(val.replace(",", "").replace(" ", "").replace("%", "").strip())
