import io

import dagster as dg
import pandas as pd
import requests

UAC_EXCEL_URL = (
    "https://www.uac.edu.au/assets/documents/statistics/2024-25/"
    "UAC_Early_Bird_applicants_30Sep25_ua26-ed2.xlsx"
)

_SHEET_NAME = "FOS of 1st pref by app type"


@dg.asset(
    group_name="uac_data",
    tags={"source": "uac", "domain": "preferences"},
)
def uac_fos_by_app_type(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """UAC field-of-study of first preference by applicant type.

    Source: UAC, Excel, public, annual (~September/October)
    Marketing use: **What message** — which fields of study attract which segments
        (ACT, NSW, Interstate, Non-Year 12). Combined with IVI job market data,
        reveals opportunity gaps where job demand exceeds student interest.
    Format: applicant_type, field_of_study, share (decimal proportion)
    Limitations:
    - Shares are proportions (0-1); values below 0.5% reported as 0
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

    # Sheet has 5 sections (ACT, NSW, Interstate & IB, Non-Year 12, Total).
    # Each section starts with [applicant_type] / "percent" in cols 0/1,
    # followed by "Field of study of first preference" label, then 12 data rows.
    rows = []
    current_type = None
    for _, row in raw.iterrows():
        val0 = row.iloc[0]
        val1 = row.iloc[1]

        # Detect section headers (col 1 == "percent")
        if isinstance(val1, str) and val1.strip().lower() == "percent":
            current_type = str(val0).strip()
            continue

        if current_type is None:
            continue
        if pd.isna(val0) or str(val0).strip() == "":
            continue

        label = str(val0).strip()
        if label == "Field of study of first preference":
            continue
        if label.startswith("As of") or label.startswith("If you"):
            break

        # Handle "<0.5%" string values → 0
        share = pd.to_numeric(val1, errors="coerce")
        if pd.isna(share):
            share = 0.0

        rows.append({
            "applicant_type": current_type,
            "field_of_study": label,
            "share": float(share),
        })

    df = pd.DataFrame(rows)

    context.log.info(f"Parsed {len(df)} rows from UAC '{_SHEET_NAME}' sheet")

    n_sections = df["applicant_type"].nunique()
    n_fields = df["field_of_study"].nunique()
    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "sections": dg.MetadataValue.int(n_sections),
        "fields_of_study": dg.MetadataValue.int(n_fields),
        "source_url": dg.MetadataValue.url(UAC_EXCEL_URL),
    })

    return df
