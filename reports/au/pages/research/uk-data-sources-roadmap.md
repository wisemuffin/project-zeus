---
title: UK Data Sources Roadmap
---

Comprehensive mapping of UK open data sources for extending Project Zeus to the UK market. Maps each Australian source asset to its UK equivalent, prioritises implementation, and outlines the approach for a future `projects/analytics-uk/` pipeline.

Project Zeus AU is built on ~18 Dagster source assets covering Australian admissions (**UAC/VTAC/SATAC**), labour market (**Jobs & Skills Australia** IVI), graduate outcomes (**QILT**), population (**ABS**), course listings (**CRICOS**), and **Google Trends**. These feed 15 dbt mart models answering Who/Where/What Message for university marketing.

## AU → UK Source Mapping

### WHO to Target (Demographics / Admissions)

| AU Asset | UK Equivalent | Publisher | Notes |
|----------|---------------|-----------|-------|
| `uac_fos_by_gender` | **UCAS End-of-Cycle (sector)** | UCAS | UCAS is **national** — one source replaces all 7 AU TAC assets |
| `uac_fos_by_app_type` | UCAS End-of-Cycle (sector) | UCAS | Domicile (UK/EU/International) replaces AU applicant type |
| `uac_applicants_by_age` | UCAS End-of-Cycle (sector) | UCAS | Same dataset, age breakdowns included |
| `uac_applicants_by_gender` | UCAS End-of-Cycle (sector) | UCAS | Same dataset, gender included |
| `uac_early_bird_closing_count` | UCAS In-Cycle Deadline Releases | UCAS | Snapshots at Oct/Jan/Jun deadlines |
| `vtac_fos_preferences` | Not needed | — | UCAS covers all of UK |
| `satac_fos_preferences` | Not needed | — | UCAS covers all of UK |

### WHERE to Target (Geographic / Population)

| AU Asset | UK Equivalent | Publisher | Notes |
|----------|---------------|-----------|-------|
| `abs_population_by_lga` | **ONS Mid-Year Population Estimates** | ONS via Nomis REST API | ~361 LADs, single year of age, annual |
| `abs_lga_reference` | **ONS LAD Boundary Files** | ONS Open Geography Portal | GeoJSON, same ArcGIS REST tech |
| — | **POLAR4** (new) | Office for Students | HE participation quintiles by MSOA — no AU equivalent |
| — | **IMD 2019** (new) | GOV.UK | Deprivation indices at LSOA level, England only |

### WHAT MESSAGE to Use (Outcomes / Demand)

| AU Asset | UK Equivalent | Publisher | Notes |
|----------|---------------|-----------|-------|
| `job_market` | **ONS Labour Demand (Textkernel)** | ONS | Monthly vacancies by SOC x Local Authority (~85MB Excel) |
| `qilt_graduate_outcomes` | **HESA Graduate Outcomes Survey** | HESA | Employment + salary at 15 months by provider x subject |
| `qilt_student_experience` | **NSS (National Student Survey)** | OfS | ~520MB ZIP, satisfaction by provider x subject |
| `google_trends` | **Google Trends (UK)** | Google | Identical impl, just `geo="GB"` |
| `cricos_courses` | **Discover Uni Dataset** | DfE | Course-level: NSS + employment + LEO salary inline |
| — | **LEO** (new) | DfE | HMRC tax-record earnings at 1/3/5/10yr. England only. Much richer than any AU salary data |

## Priority Tiers

### P1 — Minimum Viable UK Pipeline

These replicate the core AU analysis (opportunity gap, audience profiles, geographic targeting):

| # | Asset Name | UK Source | Access | dlt? |
|---|-----------|-----------|--------|------|
| 1 | `ucas_sector_admissions` | UCAS End-of-Cycle CSV ZIP (~129MB) | File download | No — complex multi-CSV ZIP |
| 2 | `ons_labour_demand` | ONS Textkernel Excel (~85MB) | File download | No — complex Excel |
| 3 | `hesa_graduate_outcomes` | HESA Graduate Outcomes CSV | File download | No — header parsing |
| 4 | `ons_population_by_lad` | ONS via Nomis REST API | API | Yes |
| 5 | `ons_lad_reference` | ONS Open Geography Portal | API | Yes |
| 6 | `soc_cah_mapping` | Manual Python dict | Hardcoded | No |
| 7 | `google_trends_uk` | trendspyg RSS | RSS | Yes |

### P2 — Enrichment

| # | Asset Name | UK Source | Value Add |
|---|-----------|-----------|-----------|
| 8 | `nss_student_satisfaction` | NSS ZIP (~520MB) | Satisfaction scores (replaces QILT SES) |
| 9 | `discover_uni_courses` | Discover Uni ZIP | Course-level NSS + employment + LEO salary |
| 10 | `leo_graduate_earnings` | DfE LEO via EES API or CSV | HMRC tax-record salary at 1/3/5/10yr (England only) |
| 11 | `ucas_provider_admissions` | UCAS provider-level CSV ZIP (~190MB) | Institution-level competitive benchmarking |
| 12 | `tef_ratings` | OfS TEF Excel/CSV | Gold/Silver/Bronze teaching quality badge |

### P3 — Nice-to-Have

| # | Asset Name | UK Source | Value Add |
|---|-----------|-----------|-----------|
| 13 | `ofs_polar4` | OfS POLAR4 Excel | HE participation quintiles by MSOA |
| 14 | `imd_2019` | GOV.UK IMD CSV | Deprivation indices (England only) |
| 15 | `ucas_constituency` | UCAS constituency CSV | 18yo entry rates by constituency |
| 16 | `ashe_earnings` | ONS ASHE via Nomis API | Salary by SOC x region |
| 17 | `dfe_occupations_in_demand` | DfE EES API/CSV | Official shortage occupation list |
| 18 | `ucas_deadline_releases` | UCAS in-cycle CSVs | Point-in-time applicant snapshots |

## Subject Classification: HECoS/CAH

UK uses **HECoS** (Higher Education Classification of Subjects) grouped via the **Common Aggregation Hierarchy (CAH)**: 23 broad groups at Level 1 (vs AU's ~12 UAC fields), 35 intermediate at Level 2, 167 detailed at Level 3. All UK sources align on CAH natively — **no cross-taxonomy mapping needed** within the UK pipeline. The finer 23-group granularity is an advantage.

## Key Differences from AU

| Aspect | AU | UK | Impact |
|--------|-----|-----|--------|
| Admissions body | 5+ state TACs | 1 national body (UCAS) | **Simpler** — 1 source replaces 7 assets |
| Salary data | QILT survey (4-6mo, self-reported) | LEO tax records (1/3/5/10yr, HMRC) | **Much richer** — enables salary trajectory charts |
| Coverage gaps | National (ABS) | England-only for LEO, IMD, TEF | Must flag `coverage_scope` in marts |
| Subject taxonomy | ~12 UAC fields | 23 CAH Level 1 groups | More granular; self-contained |
| Geography | 8 states → ~550 LGAs | 12 regions → ~361 LADs | Richer hierarchy; POLAR4/IMD add socioeconomic layer |
| Dataset sizes | ~1-15MB per source | ~85-520MB per source | May need chunked reads |

## dbt Mart Models (UK Equivalents)

| AU Mart | UK Mart | Key Change |
|---------|---------|------------|
| `opportunity_gap` | `opportunity_gap` | CAH subjects, SOC-to-CAH mapping |
| `audience_profile_by_fos` | `audience_profile_by_subject` | Domicile replaces applicant_type; adds ethnicity |
| `state_demand_index` | `region_demand_index` | 12 UK regions replace 8 AU states |
| `state_fos_demand` | `region_subject_demand` | Regions x CAH subjects |
| `audience_density_by_lga` | `audience_density_by_lad` | LADs replace LGAs |
| `graduate_outcomes_by_fos` | `graduate_outcomes_by_subject` | HESA data; add LEO salary columns |
| `trending_interests` | `trending_interests` | CAH keyword matching |
| `institution_scorecard` | `institution_scorecard` | NSS + HESA + TEF rating |
| `historical_demand_trends` | `historical_demand_trends` | UCAS 10yr; UK/EU/International segments |

**New UK-only marts:** `salary_trajectories_by_subject` (LEO 1/3/5/10yr earnings, P2), `widening_participation_targeting` (POLAR4 x LAD x UCAS entry rates, P3), `deprivation_opportunity` (IMD x LAD x vacancy density, P3).

This is a research document only. Implementation would begin with scaffolding `projects/analytics-uk/` and `reports/uk/`, then building P1 assets one at a time following the AU patterns.

<Details title="Data Sources">

- **UCAS** — Data and Analysis, End-of-Cycle Data Resources. Sector-level (~129MB) and provider-level (~190MB) CSV ZIPs.
- **ONS** — Office for National Statistics. Labour Demand (Textkernel), Mid-Year Population Estimates (Nomis API), LAD boundary files (Open Geography Portal), ASHE earnings.
- **HESA** — Higher Education Statistics Agency. Graduate Outcomes Survey.
- **OfS** — Office for Students. NSS (National Student Survey), POLAR4, TEF ratings.
- **DfE** — Department for Education. Discover Uni dataset, LEO (Longitudinal Education Outcomes), occupations in demand.
- **GOV.UK** — IMD 2019 (Index of Multiple Deprivation).
- **Google Trends** — Identical trendspyg implementation with `geo="GB"`.
- All source URLs verified as of February 2026.

</Details>
