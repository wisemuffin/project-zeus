# UAC Preferences Data (Early Bird Applicants)

## Overview

University Admissions Centre (UAC) Early Bird domestic undergraduate application statistics. Provides applicant counts by category (Year 12, non-Year 12), field of study, and gender for NSW/ACT institutions.

## Data Source

| Field | Value |
|---|---|
| Provider | University Admissions Centre (UAC) |
| Format | Excel (.xlsx) |
| URL | `https://www.uac.edu.au/assets/documents/statistics/2024-25/UAC_Early_Bird_applicants_30Sep25_ua26-ed2.xlsx` |
| Auth | None (public download) |
| Update frequency | Annually (early bird data published ~September/October) |

## Data Contents

- Applicant counts by category (Year 12, non-Year 12, international)
- Breakdown by field of study
- Gender distribution
- Year-over-year comparison data

## Limitations

- **Single snapshot**: Early Bird data is a point-in-time snapshot, not final application numbers
- **NSW/ACT only**: UAC covers NSW and ACT institutions; other states use different admissions centres (VTAC, QTAC, SATAC, TISC)
- **File URL changes**: The URL includes the year and edition number, which changes annually and needs manual updating

## Asset

- **Key**: `uac_preferences`
- **Group**: `uac_data`
- **Tags**: `source:uac`, `domain:preferences`
- **File**: `analytics/src/analytics/defs/assets/uac_preferences.py`
