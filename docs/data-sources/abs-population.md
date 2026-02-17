# ABS Population by LGA (Estimated Resident Population)

## Overview

Australian Bureau of Statistics (ABS) Estimated Resident Population (ERP) data broken down by Local Government Area (LGA) and 5-year age group. We use the **15-19 year** age group as a proxy for the Year 11/12 secondary student cohort — the primary prospective university student market.

## API Details

| Field | Value |
|---|---|
| Provider | Australian Bureau of Statistics |
| API | SDMX REST API |
| Dataflow | `ABS_ANNUAL_ERP_LGA2024` (v1.0.0) |
| Description | ERP by LGA, Age and Sex, 2001-2024 |
| Format | CSV (`application/vnd.sdmx.data+csv`) |
| Auth | None (public API) |
| Rate limits | None documented; be respectful with request frequency |

## Query Parameters

The data key used: `ERP.3.A15.+.LGA2024.A`

| Position | Value | Meaning |
|---|---|---|
| MEASURE | `ERP` | Estimated Resident Population |
| SEX_ABS | `3` | Persons (both sexes combined) |
| AGE | `A15` | 15-19 years |
| LGA_2024 | `+` | All LGAs (wildcard) |
| REGION_TYPE | `LGA2024` | LGA 2024 boundaries |
| FREQUENCY | `A` | Annual |

## Response Columns

`DATAFLOW`, `MEASURE`, `SEX_ABS`, `AGE`, `LGA_2024`, `REGION_TYPE`, `FREQUENCY`, `TIME_PERIOD`, `OBS_VALUE`, `UNIT_MEASURE`, `OBS_STATUS`, `OBS_COMMENT`

## Limitations

- **Age granularity**: Only 5-year age groups available (15-19), not single year of age. Cannot isolate 17-year-olds (Year 12) specifically.
- **Lag**: Data is typically released ~12 months after the reference period.
- **LGA boundaries**: Uses 2024 LGA boundaries. Historical data is concorded to current boundaries by ABS.

## Asset

- **Key**: `abs_population_by_lga`
- **Group**: `abs_data`
- **Tags**: `source:abs`, `domain:demographics`
- **File**: `analytics/src/analytics/defs/assets/abs_population_by_lga.py`
