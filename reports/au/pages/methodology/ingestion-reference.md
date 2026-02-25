---
title: Data Source Ingestion Reference
---

Complete inventory of how each data source is ingested, how often it publishes new data, and how the pipeline automates refresh. This is the authoritative reference for understanding data freshness and extraction methodology across all Project Zeus sources.

## Ingestion Summary

| Source | Publisher | Extraction Method | Frequency | Dagster Cron | Geographic Scope |
|--------|-----------|-------------------|-----------|-------------|------------------|
| Google Trends | Google | RSS feed (`trendspyg`) | Every 6 hours | `0 */6 * * *` | National (AU) |
| CRICOS Courses | Dept of Education | CSV file download | Weekly | `0 9 * * 1` (Mon) | National (AU) |
| IVI Job Market (Skill Level) | Jobs & Skills Australia | Excel file download | Monthly (~1 month lag) | `0 9 15 * *` | National (AU) |
| IVI Job Market (Occupation) | Jobs & Skills Australia | Excel file download | Monthly (~1 month lag) | `0 9 15 * *` | National (AU) |
| QILT Graduate Outcomes | QILT / Dept of Education | ZIP → Excel file download | Annual (~September) | `0 9 1 10 *` | National (AU) |
| QILT Student Experience | QILT / Dept of Education | ZIP → Excel file download | Annual (~September) | `0 9 1 10 *` | National (AU) |
| QILT Institution Scorecard | QILT / Dept of Education | ZIP → Excel file download | Annual (~September) | `0 9 1 10 *` | National (AU) |
| UAC Applicants by Age | UAC | Excel file download | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Applicants by Gender | UAC | Excel file download | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Field of Study x Gender | UAC | Excel file download | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Field of Study x App Type | UAC | Excel file download | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Early Bird Closing Count | UAC | Excel file download | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| ABS LGA Reference | ABS | REST API (JSON) | Annual | `0 9 1 11 *` | National (AU) |
| ABS Population by LGA | ABS | REST API (SDMX CSV) | Annual (~12 month pub lag) | `0 9 1 11 *` | National (AU) |
| VTAC Preferences | VTAC | Web scraping (HTML table) | Annual | Manual trigger | Victoria |
| SATAC Preferences | SATAC | PDF extraction | Annual | Manual trigger | SA/NT |
| Occupation-FoS Mapping | Internal | Manual (hardcoded) | Static | N/A | N/A |

All cron schedules run in **Australia/Sydney** time.

## Extraction Methods

| Method | Sources | Technology |
|--------|---------|------------|
| **REST API** | ABS LGA Reference, ABS Population by LGA | `requests` → JSON/CSV from structured endpoints. Migrated to **dlt** for schema evolution and load tracking. |
| **File download** | UAC (5), QILT (3), IVI (2), CRICOS | `requests` + `pandas` for Excel/CSV/ZIP from static URLs. CRICOS migrated to **dlt**; UAC/QILT/IVI remain as-is due to complex parsing logic. |
| **RSS feed** | Google Trends | `trendspyg` library wrapping Google Trends RSS. Migrated to **dlt** with replace strategy for ephemeral data. |
| **Web scraping** | VTAC Preferences | `requests` + `BeautifulSoup` for HTML table parsing. Remains as-is — custom parsing IS the value. |
| **PDF extraction** | SATAC Preferences | `requests` + `pdfplumber` for PDF table parsing. Remains as-is — custom parsing IS the value. |
| **Manual** | Occupation-FoS Mapping | Hardcoded Python dict. No external source to ingest. |

### dlt-migrated sources

The following sources use **dlt** (`dagster-dlt`) for ingestion: ABS LGA Reference, ABS Population by LGA, Google Trends, CRICOS Courses. These assets use `@dlt_assets` with a custom `DagsterDltTranslator` and write directly to DuckDB, bypassing the `DuckDBPandasIOManager`.

## Source Detail

### ABS Population by LGA

**Australian Bureau of Statistics** Estimated Resident Population (ERP) for 15-19 year olds by Local Government Area. Proxy for the Year 11/12 prospective student market.

- **API endpoint:** `ABS,ABS_ANNUAL_ERP_LGA2024,1.0.0/ERP.3.A15.+.LGA2024.A`
- **Extraction:** dlt via REST API (SDMX CSV format)
- **Frequency:** Annual, ~12 month publication lag
- **Asset:** `abs_population_by_lga`

### Google Trends (Trending Searches)

Real-time trending Google searches in Australia via `trendspyg` RSS feed. Provides ~10-20 currently trending topics with traffic volume and related news.

- **Extraction:** dlt via RSS feed
- **Frequency:** Every 6 hours
- **Asset:** `google_trends`
- See [Search Data Options](/methodology/search-data-options) for alternative providers (Glimpse, Exploding Topics).

### Job Market Data (Internet Vacancy Index)

Monthly Internet Vacancy Index (IVI) from **Jobs and Skills Australia**. Two assets cover this data:

- **`job_market`** — vacancies by ANZSCO skill level and state
- **`job_market_occupations`** — vacancies by ANZSCO2 occupation group and state
- **Extraction:** `requests` + `pandas` for Excel file download
- **Frequency:** Monthly, ~1 month publication lag
- URL follows a publication-lag pattern: data for month X published in folder `{X+1}`.

### UAC Early Bird Applicant Data

**University Admissions Centre** (UAC) Early Bird domestic undergraduate application statistics. Five assets parse different sheets from the same Excel file:

- **`uac_early_bird_closing_count`** — applicant volumes by segment over time
- **`uac_applicants_by_age`** — age distribution (Year 12 vs Non-Year 12)
- **`uac_applicants_by_gender`** — gender split by applicant segment
- **`uac_fos_by_app_type`** — field-of-study preference by applicant type
- **`uac_fos_by_gender`** — field-of-study preference by gender
- **Extraction:** `requests` + `pandas` for Excel file download
- **Frequency:** Annual (~Sep/Oct)
- **Coverage:** NSW/ACT applicants only

## Freshness Monitoring

Each automated source has a staleness threshold in the pipeline's freshness checks. Dagster will flag an asset as overdue if it exceeds the expected lag:

| Cadence | Max Staleness | Assets |
|---------|--------------|--------|
| 6-hourly | 12 hours | Google Trends |
| Weekly | 14 days | CRICOS |
| Monthly | 45 days | IVI (both) |
| Annual | 400 days | QILT, UAC, ABS |

## Manual-Update Sources

**VTAC** and **SATAC** have no automated schedule — they must be triggered manually when new annual data is published. VTAC data is currently from 2020-21.

**UAC and QILT** use static download URLs that need updating each year when the publisher releases new files. Check asset docstrings for the current URLs.

## Derived Assets

The **Evidence cache** (dashboard parquet files) refreshes automatically whenever any upstream dbt mart model is updated. No manual intervention needed.

## Authoritative Documentation

Each asset's Python docstring is the source of truth for detailed field descriptions, limitations, and data quality notes. See individual files in `analytics/src/analytics/defs/assets/`.

<Details title="Data Sources">

- **Australian Bureau of Statistics (ABS)** — Estimated Resident Population API and LGA Reference via ArcGIS REST API.
- **Google** — Google Trends RSS feed for Australia via `trendspyg` library.
- **Jobs and Skills Australia** — Internet Vacancy Index (IVI) Excel files.
- **QILT / Department of Education** — Graduate Outcomes Survey, Student Experience Survey, and Institution Scorecard ZIP/Excel files.
- **University Admissions Centre (UAC)** — Early Bird applicant statistics Excel files. NSW/ACT only.
- **VTAC** — Victorian Tertiary Admissions Centre annual statistics (HTML table scraping).
- **SATAC** — South Australian Tertiary Admissions Centre annual statistics (PDF extraction).
- **CRICOS** — Commonwealth Register of Institutions and Courses for Overseas Students (CSV download).
- All extraction code located in `analytics/src/analytics/defs/assets/`.

</Details>
