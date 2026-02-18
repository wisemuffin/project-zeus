import io

import dagster as dg
import pandas as pd
import requests

UAC_EXCEL_URL = (
    "https://www.uac.edu.au/assets/documents/statistics/2024-25/"
    "UAC_Early_Bird_applicants_30Sep25_ua26-ed2.xlsx"
)

# The "Early Bird closing count" sheet has data starting at row 5 (0-indexed row 4)
# with columns: applicant_type, then year columns (2016-17 through 2025-26)
_SHEET_NAME = "Early Bird closing count"
_HEADER_ROW = 4  # 0-indexed row where year headers appear


@dg.asset(
    group_name="uac_data",
    tags={"source": "uac", "domain": "preferences", "update_frequency": "annual"},
    automation_condition=dg.AutomationCondition.on_cron("0 9 1 11 *"),
)
def uac_early_bird_closing_count(
    context: dg.AssetExecutionContext,
) -> pd.DataFrame:
    """UAC Early Bird closing count — applicant volumes by market segment over time.

    Source: UAC, Excel, public, annual (~September/October)
    Marketing use: **Who** — audience sizing by segment. Year 12 vs Non-Year 12
        split sizes the school-leaver vs mature-age markets. Year-over-year trends
        reveal whether each segment is growing or shrinking.
    Format: applicant_type, then year columns (2016-17 through 2025-26)
    Limitations:
    - Point-in-time Early Bird snapshot, not final application numbers
    - NSW/ACT only (other states: VTAC, QTAC, SATAC, TISC)
    - Static URL requires annual updating
    """
    response = requests.get(UAC_EXCEL_URL, timeout=60)
    response.raise_for_status()

    df = pd.read_excel(
        io.BytesIO(response.content),
        sheet_name=_SHEET_NAME,
        header=_HEADER_ROW,
        engine="openpyxl",
    )

    # First column is the applicant type label; rename it
    df.rename(columns={df.columns[0]: "applicant_type"}, inplace=True)

    # Drop rows where applicant_type is NaN (blank rows, footers)
    df = df.dropna(subset=["applicant_type"]).reset_index(drop=True)

    # Drop footer rows (non-data text like "As of 30/09/2025", contact info)
    data_labels = {"NSW Year 12", "ACT Year 12", "Interstate & IB Year 12",
                   "Non-Year 12", "Total"}
    df = df[df["applicant_type"].isin(data_labels)].reset_index(drop=True)

    context.log.info(f"Parsed {len(df)} rows from UAC '{_SHEET_NAME}' sheet")
    context.log.info(f"Columns: {list(df.columns)}")

    # Latest year total applicants (from the Total row, last year column)
    total_row = df[df["applicant_type"] == "Total"]
    latest_year_col = df.columns[-1]
    total_applicants = int(total_row[latest_year_col].iloc[0])

    context.add_output_metadata({
        "row_count": dg.MetadataValue.int(len(df)),
        "total_applicants": dg.MetadataValue.int(total_applicants),
        "latest_year": dg.MetadataValue.text(str(latest_year_col)),
        "source_url": dg.MetadataValue.url(UAC_EXCEL_URL),
    })

    return df
