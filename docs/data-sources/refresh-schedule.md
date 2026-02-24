# Data Source Refresh Schedule

How often each source publishes new data and how we automate ingestion.

## Refresh Summary

| Source | Publisher | Frequency | Dagster Cron | Geographic Scope |
|--------|-----------|-----------|-------------|------------------|
| Google Trends | Google | Every 6 hours | `0 */6 * * *` | National (AU) |
| CRICOS Courses | Dept of Education | Weekly | `0 9 * * 1` (Mon) | National (AU) |
| IVI Job Market (Skill Level) | Jobs & Skills Australia | Monthly (~1 month lag) | `0 9 15 * *` | National (AU) |
| IVI Job Market (Occupation) | Jobs & Skills Australia | Monthly (~1 month lag) | `0 9 15 * *` | National (AU) |
| QILT Graduate Outcomes | QILT / Dept of Education | Annual (~September) | `0 9 1 10 *` | National (AU) |
| QILT Student Experience | QILT / Dept of Education | Annual (~September) | `0 9 1 10 *` | National (AU) |
| QILT Institution Scorecard | QILT / Dept of Education | Annual (~September) | `0 9 1 10 *` | National (AU) |
| UAC Applicants by Age | UAC | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Applicants by Gender | UAC | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Field of Study × Gender | UAC | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Field of Study × App Type | UAC | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| UAC Early Bird Closing Count | UAC | Annual (~Sep/Oct) | `0 9 1 11 *` | NSW/ACT |
| ABS Population by LGA | ABS | Annual (~12 month pub lag) | `0 9 1 11 *` | National (AU) |
| VTAC Preferences | VTAC | Annual | Manual trigger | Victoria |
| SATAC Preferences | SATAC | Annual | Manual trigger | SA/NT |
| Occupation–FoS Mapping | Internal | Static | N/A | N/A |

All cron schedules run in **Australia/Sydney** time.

## How freshness monitoring works

Each automated source has a staleness threshold in `analytics/src/analytics/defs/freshness_checks.py`. Dagster will flag an asset as overdue if it exceeds the expected lag:

| Cadence | Max staleness | Assets |
|---------|--------------|--------|
| 6-hourly | 12 hours | Google Trends |
| Weekly | 14 days | CRICOS |
| Monthly | 45 days | IVI (both) |
| Annual | 400 days | QILT, UAC, ABS |

## Manual-update sources

**VTAC** and **SATAC** have no automated schedule — they must be triggered manually when new annual data is published. VTAC data is currently from 2020-21.

**UAC and QILT** use static download URLs that need updating each year when the publisher releases new files. Check asset docstrings for the current URLs.

## Derived assets

The **Evidence cache** (dashboard parquet files) refreshes automatically whenever any upstream dbt mart model is updated. No manual intervention needed.

## Authoritative documentation

Each asset's Python docstring is the source of truth for detailed field descriptions, limitations, and data quality notes. See individual files in `analytics/src/analytics/defs/assets/`.
