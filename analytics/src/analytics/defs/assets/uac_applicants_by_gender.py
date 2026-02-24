import io

import dagster as dg
import pandas as pd
import requests

UAC_EXCEL_URL = (
    "https://www.uac.edu.au/assets/documents/statistics/2024-25/"
    "UAC_Early_Bird_applicants_30Sep25_ua26-ed2.xlsx"
)

_SHEET_NAME = "Applicants by gender"

_VALID_APPLICANT_TYPES = {
    "ACT",
    "Interstate & IB",
    "NSW",
    "Year 12 (ACT, Interstate & IB, NSW)",
    "Non-Year 12",
    "Total",
}


@dg.asset(
    group_name="uac_data",
    tags={"source": "uac", "domain": "demographics", "update_frequency": "annual", "ingestion": "file_download"},
    kinds={"python", "excel"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 11 *"),
)
def uac_applicants_by_gender(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """UAC applicants by gender — gender split across applicant segments.

    Source: UAC, Excel, public, annual (~September/October)
    Marketing use: **Who** — gender skew by segment informs ad creative and
        platform targeting. O* category (non-binary/prefer not to answer)
        introduced from 2025-26.
    Format: applicant_type, gender (Female | Male | O*), count
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

    # Row 3 (0-indexed) has the gender headers: Female, Male, O*, Total
    # Data starts at row 5 after an "Applicant type" label row at row 4
    gender_cols = [str(raw.iloc[3, c]).strip() for c in range(1, 5)]
    # gender_cols should be ['Female', 'Male', 'O*', 'Total']

    rows = []
    for i in range(5, len(raw)):
        applicant_type = raw.iloc[i, 0]
        if pd.isna(applicant_type):
            continue
        applicant_type = str(applicant_type).strip()
        if applicant_type not in _VALID_APPLICANT_TYPES:
            break

        # Melt into long format (exclude the "Total" gender column)
        for col_idx, gender in enumerate(gender_cols[:3]):
            val = pd.to_numeric(raw.iloc[i, col_idx + 1], errors="coerce")
            if pd.notna(val):
                rows.append({
                    "applicant_type": applicant_type,
                    "gender": gender,
                    "count": int(val),
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
