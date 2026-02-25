---
title: State × Field of Study Demand
---

Which fields are strongest in which states? Where should geo-targeted campaigns focus? This analysis combines **Jobs and Skills Australia** Internet Vacancy Index data by occupation and state with **ABS** youth population estimates and an occupation-to-field-of-study mapping.

For the interactive data explorer, see [State × Field of Study Demand](/demand/state-fos-demand).

## Summary

Each state has a distinct demand profile — some over-index on certain fields relative to the national average. The `state_vs_national_skew` metric identifies these specialisations, while `vacancies_per_1k_youth` shows absolute demand density.

### State Specialisations (rank 1 field per state)

| State | Top Specialisation | State Share | National Share | Skew | Growth (12m) |
|-------|-------------------|:-----------:|:--------------:|:----:|:------------:|
| ACT | **Information Technology** | 29.0% | 10.6% | +18.4pp | -22.5% |
| NSW | Information Technology | 12.0% | 10.6% | +1.5pp | -10.5% |
| NT | **Health** | 47.8% | 36.8% | +10.9pp | -13.7% |
| QLD | Engineering | 8.8% | 7.4% | +1.5pp | -4.0% |
| SA | **Health** | 47.7% | 36.8% | +10.9pp | +1.7% |
| TAS | **Health** | 55.2% | 36.8% | +18.4pp | +4.2% |
| VIC | Management & Commerce | 19.0% | 17.6% | +1.3pp | -5.7% |
| WA | **Engineering** | 15.7% | 7.4% | +8.3pp | -4.8% |

## Key Findings

### 1. ACT is an IT outlier

Nearly 29% of ACT's mapped vacancies are in IT — almost 3x the national average (10.6%). This aligns with the public service's digital transformation agenda. However, IT vacancies are contracting sharply (-22.5%), suggesting a cyclical correction.

**Geo-targeting:** ACT is the strongest state for IT degree campaigns, but monitor the contraction. Messaging should emphasise long-term government IT careers over current hiring surges.

### 2. Health dominates smaller states

TAS (55.2%), NT (47.8%), and SA (47.7%) all have Health as their top specialisation, well above the 36.8% national average. These states have acute healthcare workforce shortages, especially in regional areas.

- **TAS** — Growing (+4.2%) and highest skew. Best state for health career messaging.
- **SA** — Growing (+1.7%) with strong absolute demand (17.4 per 1k youth).
- **NT** — Highest demand density (26.5 per 1k youth) but contracting (-13.7%).

**Geo-targeting:** Health campaigns in TAS, SA, and NT should emphasise regional demand and workforce shortage narratives.

### 3. WA is an Engineering state

Engineering accounts for 15.7% of WA's vacancies vs 7.4% nationally — more than double. Mining and resources drive this. Despite modest contraction (-4.8%), WA remains the clear geography for engineering degree promotion.

**Geo-targeting:** WA-specific engineering campaigns should reference the resources sector and higher starting salaries.

### 4. The big states (NSW, VIC, QLD) are diversified

NSW, VIC, and QLD don't over-index dramatically on any single field — their economies are diversified. This means:
- National-level campaign messaging works well in these states
- No single field dominates, so a portfolio approach across Health, IT, and Management & Commerce is appropriate

### 5. Health demand per youth is strongest in regional states

| State | Health Vacancies per 1k Youth | Growth |
|-------|:----------------------------:|:------:|
| NT | **26.5** | -13.7% |
| TAS | **17.8** | +4.2% |
| SA | **17.4** | +1.7% |
| ACT | 16.9 | -8.2% |
| NSW | 14.3 | **+26.1%** |
| QLD | 13.0 | -4.5% |
| VIC | 12.4 | +3.4% |
| WA | 12.1 | +3.4% |

NSW is notable — while its health demand density is mid-range, it grew 26.1% year-on-year, the fastest of any state. This is a strong signal for NSW-focused health campaigns.

## How to Use This Data

1. **Geo-targeted ad creative:** "TAS has the highest health workforce demand in Australia" or "WA engineering careers are booming"
2. **Budget allocation:** Weight spend towards states where the field over-indexes
3. **Regional campaigns:** Health campaigns should over-weight TAS, SA, NT where health share exceeds 45%
4. **State-specific landing pages:** Reference local demand data for credibility

<Details title="Data Sources">

- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation and state. National and state-level coverage.
- **Estimated Resident Population** — Australian Bureau of Statistics (ABS). Annual population estimates for 15-19 year olds by LGA, aggregated to state level.
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO occupation groups to broad fields of education.
- **Source models:** `state_fos_demand`, `stg_job_vacancies_by_state_fos`
- Only 9 of 12 UAC fields have mapped occupations — same coverage as the national opportunity gap.
- State-level vacancy data may be influenced by employer advertising patterns (e.g. national employers posting in one state).
- Small states (NT, ACT, TAS) have small absolute numbers — high per-capita figures should be interpreted cautiously.

</Details>
