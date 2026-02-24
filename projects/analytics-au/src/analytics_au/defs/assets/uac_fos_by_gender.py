import io

import dagster as dg
import pandas as pd
import requests

UAC_EXCEL_URL = (
    "https://www.uac.edu.au/assets/documents/statistics/2024-25/"
    "UAC_Early_Bird_applicants_30Sep25_ua26-ed2.xlsx"
)

_SHEET_NAME = "FOS of 1st pref by gender"


@dg.asset(
    group_name="uac_data",
    tags={"source": "uac", "domain": "preferences", "update_frequency": "annual", "ingestion": "file_download"},
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 11 *"),
)
def uac_fos_by_gender(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """UAC field-of-study of first preference by gender.

    Source: UAC, Excel, public, annual (~September/October)
    Marketing use: **What message** — gender skew by field reveals targeting
        opportunities. E.g. Engineering ~18.5% of male first prefs vs ~4% female
        informs gendered campaign creative and messaging.
    Format: field_of_study, gender (Female | Male), share (decimal proportion)
    Limitations:
    - Shares are proportions (0-1); values below 0.5% reported as 0
    - Field names are abbreviated differently from "FOS by app type" sheet
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

    # Row 4 (0-indexed) has the header:
    # "Field of study of first preference", "Female", "Male", "Total"
    # Data rows start at row 5. Skip "Total" row and footer.
    gender_cols = ["Female", "Male"]

    rows = []
    for i in range(5, len(raw)):
        fos = raw.iloc[i, 0]
        if pd.isna(fos):
            continue
        fos = str(fos).strip()
        if fos in ("Total", "") or fos.startswith("*") or fos.startswith("As of"):
            continue
        if fos.startswith("If you"):
            break

        for col_idx, gender in enumerate(gender_cols):
            val = raw.iloc[i, col_idx + 1]
            # Handle "<0.5%" string values → 0
            share = pd.to_numeric(val, errors="coerce")
            if pd.isna(share):
                share = 0.0
            rows.append({
                "field_of_study": fos,
                "gender": gender,
                "share": float(share),
            })

    df = pd.DataFrame(rows)

    context.log.info(f"Parsed {len(df)} rows from UAC '{_SHEET_NAME}' sheet")

    n_fields = df["field_of_study"].nunique()
    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "fields_of_study": dg.MetadataValue.int(n_fields),
        "source_url": dg.MetadataValue.url(UAC_EXCEL_URL),
    })

    return df
