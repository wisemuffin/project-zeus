# UK Market Research Data Sources — Research & Roadmap

## Context

Project Zeus AU is built on ~18 Dagster source assets covering Australian admissions (UAC/VTAC/SATAC), labour market (Jobs & Skills Australia IVI), graduate outcomes (QILT), population (ABS), course listings (CRICOS), and Google Trends. These feed 15 dbt mart models answering Who/Where/What Message for university marketing.

This document maps the equivalent UK open data sources, prioritises them, and outlines the implementation approach for a future `projects/analytics-uk/` pipeline.

---

## AU → UK Source Mapping

### WHO to Target (Demographics / Admissions)

| AU Asset | AU Source | UK Equivalent | Publisher | Notes |
|----------|----------|---------------|-----------|-------|
| `uac_fos_by_gender` | UAC CSV | **UCAS End-of-Cycle (sector)** | UCAS | UCAS is **national** — one source replaces all 7 AU TAC assets |
| `uac_fos_by_app_type` | UAC CSV | UCAS End-of-Cycle (sector) | UCAS | Domicile (UK/EU/International) replaces AU applicant type |
| `uac_applicants_by_age` | UAC CSV | UCAS End-of-Cycle (sector) | UCAS | Same dataset, age breakdowns included |
| `uac_applicants_by_gender` | UAC CSV | UCAS End-of-Cycle (sector) | UCAS | Same dataset, gender included |
| `uac_early_bird_closing_count` | UAC CSV | UCAS In-Cycle Deadline Releases | UCAS | Snapshots at Oct/Jan/Jun deadlines |
| `vtac_fos_preferences` | Web scraping | Not needed | — | UCAS covers all of UK |
| `satac_fos_preferences` | Web scraping | Not needed | — | UCAS covers all of UK |

### WHERE to Target (Geographic / Population)

| AU Asset | AU Source | UK Equivalent | Publisher | Notes |
|----------|----------|---------------|-----------|-------|
| `abs_population_by_lga` | ABS SDMX API | **ONS Mid-Year Population Estimates** | ONS via Nomis REST API | ~361 LADs, single year of age, annual |
| `abs_lga_reference` | ABS ArcGIS REST | **ONS LAD Boundary Files** | ONS Open Geography Portal | GeoJSON, same ArcGIS REST tech |
| — | — | **POLAR4** (new) | Office for Students | HE participation quintiles by MSOA — no AU equivalent |
| — | — | **UCAS Constituency Dashboard** (new) | UCAS | 18yo entry rates by parliamentary constituency |
| — | — | **IMD 2019** (new) | GOV.UK | Deprivation indices at LSOA level, England only |

### WHAT MESSAGE to Use (Outcomes / Demand)

| AU Asset | AU Source | UK Equivalent | Publisher | Notes |
|----------|----------|---------------|-----------|-------|
| `job_market` | IVI Excel | **ONS Labour Demand (Textkernel)** | ONS | Monthly vacancies by SOC × Local Authority. ~85MB Excel |
| `job_market_occupations` | IVI Excel | ONS Labour Demand (same file) | ONS | One UK source replaces both AU assets |
| `qilt_graduate_outcomes` | QILT ZIP/Excel | **HESA Graduate Outcomes Survey** | HESA | Employment + salary at 15 months by provider × subject |
| `qilt_student_experience` | QILT ZIP/Excel | **NSS (National Student Survey)** | OfS | ~520MB ZIP, satisfaction by provider × subject |
| `qilt_institution_scores` | QILT ZIP/Excel | **TEF + Discover Uni Dataset** | OfS / DfE | TEF ratings + course-level combined data |
| `google_trends` | trendspyg RSS | **Google Trends (UK)** | Google | Identical impl, just `geo="GB"` |
| `cricos_courses` | data.gov.au CSV | **Discover Uni Dataset** | DfE | Course-level: NSS + employment + LEO salary inline |
| `occupation_fos_mapping` | Manual Python | **SOC-to-CAH Mapping** | Manual | SOC 2020 → CAH Level 1 subject groups |
| — | — | **LEO** (new) | DfE | HMRC tax-record earnings at 1/3/5/10yr. England only. Much richer than any AU salary data |
| — | — | **ASHE Earnings** (new) | ONS via Nomis | Median salary by SOC × region. REST API |
| — | — | **DfE Occupations in Demand** (new) | DfE | Official shortage occupation list + SOC lookups |

---

## Priority Tiers

### P1 — Minimum Viable UK Pipeline

These replicate the core AU analysis (opportunity gap, audience profiles, geographic targeting):

| # | Asset Name | UK Source | Access | dlt? | AU Equivalent |
|---|-----------|-----------|--------|------|---------------|
| 1 | `ucas_sector_admissions` | UCAS End-of-Cycle CSV ZIP (~129MB) | File download | No — complex multi-CSV ZIP | 7 UAC/VTAC/SATAC assets |
| 2 | `ons_labour_demand` | ONS Textkernel Excel (~85MB) | File download | No — complex Excel | `job_market` + `job_market_occupations` |
| 3 | `hesa_graduate_outcomes` | HESA Graduate Outcomes CSV | File download | No — header parsing | `qilt_graduate_outcomes` |
| 4 | `ons_population_by_lad` | ONS via Nomis REST API | API | Yes | `abs_population_by_lga` |
| 5 | `ons_lad_reference` | ONS Open Geography Portal | API | Yes | `abs_lga_reference` |
| 6 | `soc_cah_mapping` | Manual Python dict | Hardcoded | No | `occupation_fos_mapping` |
| 7 | `google_trends_uk` | trendspyg RSS | RSS | Yes | `google_trends` |

### P2 — Enrichment (outcomes depth + institution-level)

| # | Asset Name | UK Source | Access | Value Add |
|---|-----------|-----------|--------|-----------|
| 8 | `nss_student_satisfaction` | NSS ZIP (~520MB) | File download | Satisfaction scores (replaces QILT SES) |
| 9 | `discover_uni_courses` | Discover Uni ZIP | File download | Course-level NSS + employment + LEO salary |
| 10 | `leo_graduate_earnings` | DfE LEO via EES API or CSV | API/file | HMRC tax-record salary at 1/3/5/10yr (England only) |
| 11 | `ucas_provider_admissions` | UCAS provider-level CSV ZIP (~190MB) | File download | Institution-level competitive benchmarking |
| 12 | `tef_ratings` | OfS TEF Excel/CSV | File download | Gold/Silver/Bronze teaching quality badge |

### P3 — Nice-to-Have (widening participation, advanced labour market)

| # | Asset Name | UK Source | Value Add |
|---|-----------|-----------|-----------|
| 13 | `ofs_polar4` | OfS POLAR4 Excel | HE participation quintiles by MSOA |
| 14 | `imd_2019` | GOV.UK IMD CSV | Deprivation indices (England only) |
| 15 | `ucas_constituency` | UCAS constituency CSV | 18yo entry rates by constituency |
| 16 | `ashe_earnings` | ONS ASHE via Nomis API | Salary by SOC × region |
| 17 | `dfe_occupations_in_demand` | DfE EES API/CSV | Official shortage occupation list |
| 18 | `ucas_deadline_releases` | UCAS in-cycle CSVs | Point-in-time applicant snapshots |

---

## Subject Classification: HECoS/CAH

UK uses **HECoS** (Higher Education Classification of Subjects) grouped via the **Common Aggregation Hierarchy (CAH)**:
- **CAH Level 1**: 23 broad groups (vs AU's ~12 UAC fields)
- **CAH Level 2**: 35 intermediate groups
- **CAH Level 3**: 167 detailed groups

All UK sources (UCAS, HESA, NSS, Discover Uni, LEO) align on CAH natively. **Use CAH Level 1 as the canonical subject join key** — no cross-taxonomy mapping needed within the UK pipeline. The finer 23-group granularity is an advantage (e.g. "Medicine" vs "Nursing" vs "Allied Health" are separate).

Full HECoS code list and CAH mappings: https://www.hesa.ac.uk/innovation/hecos

Cross-country comparison (AU↔UK) is P3 at best and would require a separate mapping asset.

---

## Key Differences from AU

| Aspect | AU | UK | Impact |
|--------|-----|-----|--------|
| Admissions body | 5+ state TACs | 1 national body (UCAS) | **Simpler** — 1 source replaces 7 assets, no union model needed |
| Salary data | QILT survey (4-6mo, self-reported) | LEO tax records (1/3/5/10yr, HMRC) | **Much richer** — enables salary trajectory charts |
| Coverage gaps | National (ABS) | England-only for LEO, IMD, TEF | Must flag `coverage_scope` in marts |
| Subject taxonomy | ~12 UAC fields | 23 CAH Level 1 groups | More granular; self-contained |
| Geography | 8 states → ~550 LGAs | 12 regions → ~361 LADs (+ MSOAs) | Richer hierarchy; POLAR4/IMD add socioeconomic layer |
| Occupation codes | ANZSCO | SOC 2020 | Different taxonomy, same mapping pattern |
| Dataset sizes | ~1-15MB per source | ~85-520MB per source | May need chunked reads |
| HE participation measure | None | POLAR4, TUNDRA | New capability — no AU equivalent |

---

## dbt Mart Models (UK Equivalents)

### Direct equivalents of AU marts

| AU Mart | UK Mart | Key Change |
|---------|---------|------------|
| `opportunity_gap` | `opportunity_gap` | CAH subjects, SOC-to-CAH mapping |
| `opportunity_gap_by_gender` | `opportunity_gap_by_gender` | UCAS gender data |
| `audience_profile_by_fos` | `audience_profile_by_subject` | Domicile replaces applicant_type; adds ethnicity |
| `state_demand_index` | `region_demand_index` | 12 UK regions replace 8 AU states |
| `state_fos_demand` | `region_subject_demand` | Regions × CAH subjects |
| `audience_density_by_lga` | `audience_density_by_lad` | LADs replace LGAs |
| `graduate_outcomes_by_fos` | `graduate_outcomes_by_subject` | HESA data; add LEO salary columns |
| `field_value_proposition` | `subject_value_proposition` | LEO 5yr salary for robust value score |
| `gender_opportunity_profile` | `gender_opportunity_profile` | LEO longitudinal gender pay gap |
| `satisfaction_opportunity` | `satisfaction_opportunity` | NSS indicators replace QILT SES |
| `segment_field_affinity` | `segment_subject_affinity` | Domicile × age segments |
| `emerging_occupations` | `emerging_occupations` | SOC groups replace ANZSCO |
| `trending_interests` | `trending_interests` | CAH keyword matching |
| `institution_scorecard` | `institution_scorecard` | NSS + HESA + TEF rating |
| `university_course_listings` | `university_course_listings` | Discover Uni (includes inline outcomes) |
| `historical_demand_trends` | `historical_demand_trends` | UCAS 10yr; UK/EU/International segments |

### New UK-only marts (P2/P3)

| Mart | Source | Priority |
|------|--------|----------|
| `salary_trajectories_by_subject` | LEO 1/3/5/10yr earnings | P2 |
| `widening_participation_targeting` | POLAR4 × LAD × UCAS entry rates | P3 |
| `deprivation_opportunity` | IMD × LAD × vacancy density | P3 |

---

## Source URLs (P1 Assets)

| Asset | URL |
|-------|-----|
| UCAS End-of-Cycle | https://www.ucas.com/data-and-analysis/undergraduate-statistics-and-reports/ucas-undergraduate-end-of-cycle-data-resources-2025 |
| ONS Labour Demand | https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/labourdemandvolumesbystandardoccupationclassificationsoc2020uk |
| HESA Graduate Outcomes | https://www.hesa.ac.uk/data-and-analysis/graduates/releases |
| ONS Population (Nomis) | https://www.nomisweb.co.uk/datasets/pestsyoala |
| ONS LAD Boundaries | https://geoportal.statistics.gov.uk/datasets/ons::local-authority-districts-may-2024-boundaries-uk-bfe-2 |
| HECoS/CAH codes | https://www.hesa.ac.uk/innovation/hecos |
| Google Trends | Same trendspyg library, `geo="GB"` |

---

## Next Step

This is a research document only. Implementation would begin with scaffolding `projects/analytics-uk/` and `reports/uk/`, then building P1 assets one at a time following the AU patterns.
