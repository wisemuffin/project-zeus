# Job Market Data (Internet Vacancy Index)

## Overview

Monthly Internet Vacancy Index (IVI) data from Jobs and Skills Australia. Tracks online job vacancy counts by ANZSCO occupation group, skill level, and state/territory. Provides labour market demand signals to identify which career pathways (and corresponding university courses) are most relevant.

## Data Source

| Field | Value |
|---|---|
| Provider | Jobs and Skills Australia (Australian Government) |
| Dataset | Internet Vacancy Index (IVI) |
| Format | Excel (.xlsx) |
| URL pattern | `https://www.jobsandskills.gov.au/sites/default/files/{year}-{month}/internet_vacancies_anzsco_skill_level_states_and_territories_-_{month_name}_{year}.xlsx` |
| Auth | None (public download) |
| Update frequency | Monthly |

## URL Construction

The download URL is date-based. Example for January 2026:

```
https://www.jobsandskills.gov.au/sites/default/files/2026-01/
internet_vacancies_anzsco_skill_level_states_and_territories_-_january_2026.xlsx
```

The asset automatically tries the current month and works backwards up to 4 months to find the latest available file.

## Data Contents

- **ANZSCO occupation groups** — occupation classifications at various levels
- **Skill level** — occupational skill level (1-5)
- **State/territory breakdown** — vacancy counts by Australian state
- **Monthly counts** — point-in-time vacancy counts

## Limitations

- **Online vacancies only**: IVI counts vacancies posted on major job boards; does not capture all job openings (e.g. word-of-mouth, agency-only roles)
- **Lag**: Data for a given month is typically published 1-2 months later
- **File URL changes**: If Jobs and Skills Australia changes their URL structure, the URL builder will need updating
- **Large file**: The Excel file can be several MB with multiple sheets

## Asset

- **Key**: `job_market`
- **Group**: `job_market`
- **Tags**: `source:job_market`, `domain:employment`
- **File**: `analytics/src/analytics/defs/assets/job_market.py`
