import io

import dagster as dg
import pandas as pd
import requests

UAC_EXCEL_URL = (
    "https://www.uac.edu.au/assets/documents/statistics/2024-25/"
    "UAC_Early_Bird_applicants_30Sep25_ua26-ed2.xlsx"
)

_SHEET_NAME = "Applicants by age"


@dg.asset(
    group_name="uac_data",
    tags={"source": "uac", "domain": "demographics"},
)
def uac_applicants_by_age(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """UAC applicants by age — age distribution of Year 12 and Non-Year 12 applicants.

    Source: UAC, Excel, public, annual (~September/October)
    Marketing use: **Who** — age distribution informs channel selection.
        Under-19 skews toward TikTok/Instagram; 25+ toward LinkedIn/Facebook.
        Year 12 vs Non-Year 12 age profiles reveal distinct audience segments.
    Format: applicant_type (Year 12 | Non-Year 12), age_group, count
    Limitations:
    - Point-in-time Early Bird snapshot, not final numbers
    - NSW/ACT only
    - Static URL requires annual updating
    """
    response = requests.get(UAC_EXCEL_URL, timeout=60)
    response.raise_for_status()

    raw = pd.read_excel(
        io.BytesIO(response.content),
        sheet_name=_SHEET_NAME,
        header=None,
        engine="openpyxl",
    )

    # Parse the two-section structure: "Year 12" and "Non-Year 12"
    # Section headers have the applicant type in col 0 and "count" in col 1
    rows = []
    current_type = None
    for _, row in raw.iterrows():
        val0 = row.iloc[0]
        val1 = row.iloc[1]

        # Detect section headers
        if isinstance(val1, str) and val1.strip().lower() == "count":
            current_type = str(val0).strip()
            continue

        # Skip non-data rows
        if current_type is None:
            continue
        if pd.isna(val0) or str(val0).strip() == "":
            continue
        label = str(val0).strip()
        if label in ("Age group", "Field of study of first preference"):
            continue
        if label.startswith("As of") or label.startswith("If you"):
            break

        # Data row
        count = pd.to_numeric(val1, errors="coerce")
        if pd.notna(count):
            rows.append({
                "applicant_type": current_type,
                "age_group": label,
                "count": int(count),
            })

    df = pd.DataFrame(rows)

    context.log.info(f"Parsed {len(df)} rows from UAC '{_SHEET_NAME}' sheet")

    total_count = df["count"].sum()
    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "total_applicants": dg.MetadataValue.int(int(total_count)),
        "source_url": dg.MetadataValue.url(UAC_EXCEL_URL),
    })

    return df
