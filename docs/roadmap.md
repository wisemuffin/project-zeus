# Project Zeus - Market Research Roadmap

## Analysis Models (dbt)

Mart models that transform raw Dagster assets into marketing-actionable insights. Each answers a core targeting question.

### Completed

- [x] **Opportunity Gap** (`opportunity_gap`) — Which fields of study have high job demand but low student interest? Strongest messaging opportunities.
- [x] **Opportunity Gap by Gender** (`opportunity_gap_by_gender`) — Which high-gap fields skew male or female? Enables gender-targeted ad creative.
- [x] **State Demand Index** (`state_demand_index`) — Graduate vacancies per 1,000 youth by state. Identifies geographic hotspots for marketing spend.

- [x] **Audience Profile by FOS** (`audience_profile_by_fos`) — Gender, mature learner affinity, and geographic origin per field. Answers **who** to target and **where** they are.
- [x] **Trending Interests** (`trending_interests`) — Google Trends classified by FOS with opportunity gap context. Identifies timely messaging hooks.
- [x] **Historical Demand Trends** (`historical_demand_trends`) — 10-year UAC applicant volumes by segment with YoY growth and CAGR. Identifies growing vs declining segments for budget allocation.
- [x] **Graduate Outcomes by FOS** (`graduate_outcomes_by_fos`) — QILT graduate employment rates, median salaries (with gender split), and salary growth joined with opportunity gap and UAC preference data. Composite marketing signals classify each field as "Strong", "Demand", "Outcomes", or "Challenging".

- [x] **State × FOS Demand** (`state_fos_demand`) — State-level demand by field of study with specialisation skew vs national average. ACT over-indexes on IT, TAS/SA/NT on Health, WA on Engineering.

- [x] **University Course Listings** (`university_course_listings`) — CRICOS course data from data.gov.au joined with opportunity gap and graduate outcomes. Connects fields of study to named programs at specific institutions and campuses for program-level marketing recommendations.

- [x] **Field Value Proposition** (`field_value_proposition`) — Composite ranking of each field by opportunity gap, employment rate, and salary. Classifies into actionable tiers (No-brainer, High potential, Proven outcomes, Challenging) for prioritising campaign spend.
- [x] **Gender Opportunity Profile** (`gender_opportunity_profile`) — Gender salary gap alongside preference shares and opportunity gap in a diversity-marketing view. Supports equity-focused messaging.
- [x] **Satisfaction × Opportunity** (`satisfaction_opportunity`) — QILT SES satisfaction aggregated to field level, joined with opportunity gap and graduate outcomes. Adds student experience proof points.
- [x] **Segment Field Affinity** (`segment_field_affinity`) — Per-applicant-type field affinity showing which segments over-index on which fields. Enables segment-specific campaign messaging.
- [x] **Emerging Occupations** (`emerging_occupations`) — ANZSCO2 occupations ranked by 12-month vacancy growth, mapped to UAC fields. Identifies fast-growing occupations for messaging.
- [x] **Audience Density by LGA** (`audience_density_by_lga`) — LGA-level youth population for hyper-local geo-targeting of digital campaigns.

- [x] **Institution Enrolment Profile** (`institution_enrolment_profile`) — Institution × field enrolment profile from DET Higher Education Statistics. International share, external/online penetration, gender composition, and pipeline health (commencing share) per field, with sector benchmarks and opportunity gap context. Answers "Who" and "Where".
- [x] **VET Competition by State** (`vet_competition_by_state`) — VET sector competition context by state. VET density (students per 1k youth), growth trends, and comparison with graduate job vacancy density. Answers "Where" and "What message".

### Planned

*(none currently)*

### Parked
- [ ] **Digital Ad Cost Benchmarks** — Google Ads CPC by education keyword to turn opportunity gaps into ROI-adjusted recommendations. No free open data source exists at keyword level. Viable paid options when ready:
  - *Google Ads API* — free to query (needs billing account with $0 spend), OAuth + developer token setup
  - *DataForSEO* — ~$50 one-time (credits don't expire), cleanest REST API, supports AU targeting
  - *SpyFu edu program* — potentially free for research, email request required
  - Category-level benchmarks available free (WordStream: Education CPC ~$6.23 USD / "degree" $18.38 AUD in 2017)

---

## New Data Sources

Platforms identified from [student search platform research](insights/student-search-platforms.md) that publish open data we can ingest. Prioritised by data richness, accessibility, and alignment with Project Zeus targeting questions.

### Priority 1: QILT (Quality Indicators for Learning and Teaching)

**Source:** [qilt.edu.au](https://www.qilt.edu.au/) | **Owner:** Australian Government (Social Research Centre)
**Access:** Free ZIP/Excel downloads — no API, but predictable URL pattern
**Coverage:** All 42 Australian universities + ~90 non-university providers
**Frequency:** Annual (published ~September each year)

QILT publishes four survey datasets as Excel report tables:

| Survey | What it measures | Key metrics | Marketing use |
|--------|-----------------|-------------|---------------|
| **Graduate Outcomes Survey (GOS)** | Employment 4-6 months post-graduation | FT employment rate, median salary, course satisfaction | "What message" — career outcome proof points by field |
| **Student Experience Survey (SES)** | Teaching quality, engagement, support | 6 satisfaction indicators (% agreement) | "What message" — student satisfaction claims |
| **GOS-Longitudinal (GOS-L)** | Employment 3 years post-graduation | Salary progression, FT employment rate | "What message" — longer-term ROI narrative |
| **Employer Satisfaction Survey (ESS)** | Employer views on graduate quality | Foundation, adaptive, collaborative, technical skills | "What message" — employer endorsement angles |

**Granularity:** Institution × Field of Study (21 study areas) × Student Level × Demographics (gender, Indigenous, disability, SES, location)

**Download URLs (2024):**
- GOS: `https://www.qilt.edu.au/docs/default-source/default-document-library/gos_2024_national_report_tables.zip`
- SES: `https://www.qilt.edu.au/docs/default-source/default-document-library/ses_2024_national_report_tables.zip`
- GOS-L: `https://qilt.edu.au/docs/default-source/default-document-library/2024_gos-l_national_report_tables.zip`
- ESS: `https://www.qilt.edu.au/docs/default-source/default-document-library/ess_2024_national_report_tables.zip`

**Implementation plan:**
- [x] Download and explore GOS report tables to understand sheet structure
- [x] Build Dagster asset for GOS data (employment rates & salaries by field of study) — `qilt_graduate_outcomes`
- [x] Build Dagster asset for SES data (student satisfaction by field of study) — `qilt_student_experience`
- [x] Build Dagster asset for institution scores (SES + GOS combined) — `qilt_institution_scores`
- [x] Create dbt staging models to standardise QILT field-of-study names to UAC categories — `stg_qilt_graduate_outcomes`, `stg_qilt_student_experience`
- [x] Build mart model: **graduate_outcomes_by_fos** — joins GOS employment/salary data with opportunity gap, gender preferences, and marketing signals
- [x] Build mart model: **institution_scorecard** — per-university satisfaction + outcomes for competitive benchmarking (43 universities)

### Priority 2: CRICOS (Course Listings)

**Source:** [data.gov.au/data/dataset/cricos](https://data.gov.au/data/dataset/cricos) | **Owner:** Australian Government (Department of Education)
**Access:** Free CSV/XLSX download, Creative Commons Attribution 2.5 Australia
**Coverage:** ~9,000 courses across all providers registered for international students
**Frequency:** Monthly updates

CRICOS provides four relational CSV files:

| File | Contents |
|------|----------|
| **CRICOS Institutions** | Provider name, CRICOS code, type, state |
| **CRICOS Courses** | Course name, level, field of study (ASCED broad + narrow), duration, fees |
| **CRICOS Locations** | Campus locations per provider |
| **CRICOS Course Locations** | Junction table linking courses to delivery locations |

**Marketing use:** Connects opportunity gap fields to named programs at specific institutions — enables "promote your [X] degree" recommendations. Joined with QILT outcomes, supports per-program ROI messaging.

**Limitations:**
- International-student-registered courses only (most university courses are registered, but some domestic-only programs may be absent)
- No ATAR/entry requirement data
- No delivery mode (online vs on-campus) — would need CourseSeeker for that
- ASCED field-of-study classification requires mapping to UAC categories (same approach as QILT staging model)

**Note:** CourseSeeker (courseseeker.edu.au) was investigated but has no public API or bulk download — it is an Angular SPA with a private backend. CRICOS is the best open alternative.

**Implementation plan:**
- [x] Download and explore CRICOS CSV structure from data.gov.au
- [x] Build Dagster asset for CRICOS data (institutions + courses + locations) — `cricos_courses`
- [x] Create dbt staging model to map ASCED fields to UAC categories — `stg_cricos_courses`
- [x] Build mart model: **university_course_listings** — courses joined with opportunity gap and graduate outcomes for program-level recommendations

### Priority 3: VTAC (Victorian Tertiary Admissions Centre)

**Source:** [vtac.edu.au/statistics](https://vtac.edu.au/statistics/) | **Owner:** VIC consortium
**Access:** Free HTML tables — annual statistics by ASCED field of study
**Coverage:** Victoria (~25% of Australian higher-ed applicants)

VTAC publishes Section D tables with field-of-study preference data using ASCED classification (same as UAC). Table D1 includes first preferences, offers, enrolments, and deferrals broken down by gender per field. Combined with UAC (NSW/ACT ~40%), this covers ~65% of the Australian applicant market.

**Implementation plan:**
- [x] Build Dagster asset to fetch and parse VTAC Section D HTML tables — `vtac_fos_preferences`
- [x] Create dbt staging model to normalise field names to canonical categories — `stg_vtac_fos_preferences`
- [x] Build national preferences union model — `stg_national_fos_preferences`
- [x] Create Evidence report page for cross-state preference comparison

### Priority 4: Other Accessible Platforms

| Platform | Data | Status |
|----------|------|--------|
| **CourseSeeker** ([courseseeker.edu.au](https://www.courseseeker.edu.au/)) | National course listings across all institutions | Investigated — no API or bulk download; Angular SPA with private backend. CRICOS used instead. |
| **SATAC** ([satac.edu.au](https://www.satac.edu.au/)) | SA/NT admissions stats | **Implemented** — `satac_fos_preferences` Dagster asset + `stg_satac_fos_preferences` staging model. Added to national union. Brings coverage to ~72%. |

### Priority 5: QTAC (Queensland Tertiary Admissions Centre)

**Source:** [qtac.edu.au](https://www.qtac.edu.au/) | **Owner:** QLD consortium
**Access:** TBD — no FOS preference data found in initial investigation, only ATAR scaling PDFs. Needs deeper research into annual reports or data request.
**Coverage:** Queensland (~20% of Australian higher-ed applicants)

Adding QTAC would bring national admissions coverage from 72% to ~92% and enable briefs for major Queensland universities (UQ, QUT, Griffith, JCU, USQ). This is the single biggest geographic gap.

**Implementation plan:**
- [ ] Re-investigate QTAC website and annual reports for FOS preference data
- [ ] If available: build Dagster asset, staging model, add to national union
- [ ] If not public: submit formal data request to QTAC

### Priority 6: TISC (Tertiary Institutions Service Centre, WA)

**Source:** [tisc.edu.au](https://www.tisc.edu.au/) | **Owner:** WA consortium
**Access:** TBD — no FOS data found in initial investigation. Has a formal data request process.
**Coverage:** Western Australia (~8% of Australian higher-ed applicants)

Would bring coverage to ~100% and enable briefs for WA universities (UWA, Curtin, Murdoch, ECU).

**Implementation plan:**
- [ ] Investigate TISC publications and data request process
- [ ] If available: build Dagster asset, staging model, add to national union

### Priority 7: CourseSeeker / ATAR & Entry Requirements

**Source:** [courseseeker.edu.au](https://www.courseseeker.edu.au/) | **Owner:** Australian Government (DESE)
**Access:** Angular SPA with private backend — no API or bulk download. CRICOS used instead for course data.

ATAR/selection rank data would add selectivity context to course recommendations (e.g. "your mid-ATAR courses in high-demand fields are your best growth opportunity"). No open data source identified yet.

**Implementation plan:**
- [ ] Research whether CourseSeeker's backend API can be reverse-engineered for ATAR data
- [ ] Investigate alternative sources: UAC course search, individual university websites
- [ ] If viable: build Dagster asset for ATAR/entry requirements, join to university_course_listings

### Priority 8: Online vs On-Campus Delivery Mode

Post-COVID, online delivery is a major differentiator for marketing targeting. CRICOS doesn't include delivery mode.

**Implementation plan:**
- [ ] Check if CRICOS data includes any delivery mode flags we missed
- [ ] Research TEQSA (Tertiary Education Quality and Standards Agency) provider register for delivery mode data
- [ ] If no bulk source: consider scraping individual university course pages (low priority)

### Priority 9: DET Higher Education Student Enrolments

**Source:** [education.gov.au/higher-education-statistics](https://www.education.gov.au/higher-education-statistics/resources/student-enrolments-pivot-table) | **Owner:** Australian Government Department of Education
**Access:** Free Excel download — pivot table with embedded cache of 201K microdata records
**Coverage:** All 47 Australian higher education institutions, 2016-2020
**Frequency:** Annual (published ~September)

The Student Enrolments Pivot Table provides institution × field × citizenship × mode of attendance × gender enrolments. This is the single richest source for per-university analysis — enables "45% of your IT enrolments are international" and "70% of your Engineering students study on-campus" insights.

**Implementation plan:**
- [x] Research DET pivot table structure and extract pivot cache XML
- [x] Build Dagster asset — `det_he_enrolments` — parses pivot cache records (201K rows)
- [x] Create dbt staging model — `stg_det_he_enrolments` — maps ASCED broad fields to UAC categories
- [x] Add to dbt sources with dagster asset_key lineage
- [x] Build mart model: **institution_enrolment_profile** — per-institution enrolment profile by field (international share, external share, gender, pipeline health)

### Priority 10: NCVER VET Historical Time Series

**Source:** [ncver.edu.au](https://www.ncver.edu.au/research-and-statistics/data) | **Owner:** National Centre for Vocational Education Research
**Access:** Free Excel download (1.5MB) — government-funded VET students 1981-2024
**Coverage:** All states/territories, gender, 44 years of data
**Frequency:** Annual (published ~August)

Provides VET enrolment trends by state and gender for competitive context. Field of education breakdown only available 2002-2014 (NCVER changed classification after 2014). Recent FoE data requires interactive DataBuilder tool (not automatable).

**Implementation plan:**
- [x] Research NCVER public data availability (historical time series, DataBuilder)
- [x] Build Dagster asset — `ncver_vet_students` — parses Table 1 (students by state/gender)
- [x] Create dbt staging model — `stg_ncver_vet_students`
- [x] Add to dbt sources with dagster asset_key lineage
- [x] Build mart model: **vet_competition_by_state** — VET vs higher-ed trend comparison by state

**Note:** NCVER website uses Cloudflare — automated downloads may fail. DataBuilder provides richer cross-tabulations (field of education × state × year) but requires interactive browser session.

### Investigated (No Action)

| Platform | Finding |
|----------|---------|
| **Good Universities Guide** ([gooduniversitiesguide.com.au](https://www.gooduniversitiesguide.com.au/)) | Repackages QILT data we already ingest directly. No additional value. |

### Not Accessible (Commercial / Paywalled)

These platforms from the student search analysis are **not viable** as data sources — their data is their product:

- **Appily / Niche / BigFuture** — US lead-gen platforms, no public data feeds
- **Common App / Coalition App** — aggregate reports only, no granular data
- **Naviance** — school-licensed CRM, no public access
- **StudySelect / Adventus.io / IDP** — commercial lead-gen, proprietary data
- **Unibuddy** — SaaS platform, no public data

---

## Embedded Analytics

**Goal:** Build embedded analytics into the platform using an analytics-as-code approach.

**Reference:** [Evidence.dev - Embedded Analytics](https://evidence.dev/blog/embedded-analytics)

### Approach

- Treat embedded analytics as a **code artifact** (declarative markdown-based reports) rather than UI-configured dashboards
- Embed reports via **iframe integration** with JWE-encrypted API endpoints — works across any web stack with no complex auth flows
- Enforce **row-level security at the database level**, removing the need to manually inject user attributes into queries

### Key Benefits

- **Version control & review** — reports are code, enabling diffs, PRs, history tracking, and rollbacks
- **Performance** — optimized query engine with intelligent caching for sub-second interactions across large datasets
- **Theming & branding** — production-ready visualization components with customizable light/dark themes
- **Security & compliance** — SOC 2 Type II, multi-region data residency support

### Completed

- [x] **Evaluate Evidence.dev** — Scaffolded local Evidence project in `reports/au/`, connected to DuckDB warehouse, built MVP dashboard with opportunity gap, gender, and state demand visualisations.

### Report Pages

- [x] **Opportunity Gap Dashboard** (`pages/index.md`) — BigValue cards, vacancy vs preference bar charts, gender skew, state demand density. Covers opportunity_gap, opportunity_gap_by_gender, and state_demand_index marts.
- [x] **Audience Profiles** (`pages/audience-profiles.md`) — Who to target per field: gender split, mature learner index, geographic origin (NSW/ACT/interstate draw). Sources from audience_profile_by_fos mart.
- [x] **Trending Interests** (`pages/trending-interests.md`) — Google Trends matched to fields of study with opportunity gap context and marketing signals. Sources from trending_interests mart.
- [x] **Historical Demand** (`pages/historical-demand.md`) — 10-year applicant volume trends by segment with YoY growth, CAGR, and recovery ratios. Sources from historical_demand_trends mart.
- [x] **Graduate Outcomes** (`pages/graduate-outcomes.md`) — Salary by gender, FT employment rates (YoY), marketing signal matrix, salary gender gap. Sources from graduate_outcomes_by_fos mart + QILT GOS data.
- [x] **Institution Scorecard** (`pages/institution-scorecard.md`) — Per-university satisfaction vs employment scatter, satisfaction indicators, full scorecard with sector comparison. Sources from institution_scorecard mart + QILT SES/GOS data.
- [x] **State Preference Comparison** (`pages/state-preferences.md`) — Cross-state comparison of field-of-study preferences across NSW/ACT (UAC), Victoria (VTAC), and SA/NT (SATAC). Grouped bar charts, divergence table, gender split by state. Sources from stg_national_fos_preferences.
- [x] **Field Value Proposition** (`pages/field-value.md`) — Composite value score ranking, tier distribution, and full ranking table. Sources from field_value_proposition mart.
- [x] **Gender Pay Gap × Opportunity** (`pages/gender-pay-gap.md`) — Salary by gender, gender gap bar chart, diversity opportunity classification. Sources from gender_opportunity_profile mart.
- [x] **Student Satisfaction × Opportunity** (`pages/student-satisfaction.md`) — Satisfaction vs employment scatter, indicator bar charts, full data table. Sources from satisfaction_opportunity mart.
- [x] **Segment Playbooks** (`pages/segment-playbooks.md`) — Dropdown-filtered segment view with affinity indices and outcomes context. Sources from segment_field_affinity mart.
- [x] **Emerging Occupations** (`pages/emerging-occupations.md`) — Vacancy growth ranking by occupation, mapped to fields. Sources from emerging_occupations mart.
- [x] **Audience Density by LGA** (`pages/audience-density.md`) — LGA-level youth population searchable by state for geo-targeting. Sources from audience_density_by_lga mart.

### Future

- [ ] Set up database-level row-level security policies
- [ ] Prototype iframe embedding in the application
- [ ] Implement theming to match product branding

---

## Infrastructure

### Planned

- [x] **Migrate to dbt Fusion engine** — Migrated from dbt-core to dbt Fusion CLI (`2.0.0-preview.143`). ~30x faster parse/compile, dialect-aware SQL validation. Moved `meta:` to `config.meta:` in sources and schema YAML for stricter validation. Rewrote `stg_uac_demand_by_year` UNPIVOT to UNION ALL for parser compatibility. Removed `dbt-duckdb` Python dependency — Fusion is a standalone binary at `~/.local/bin/dbt` with a `dbtf` wrapper script for dagster-dbt auto-detection. Added default `+severity: warn` for tests to work around Fusion null severity. All 38 models and 43 tests pass.
- [ ] **Evaluate DuckLake + MotherDuck** — Cloud-hosted DuckDB with the DuckLake open table format for ACID transactions, time travel, and collaborative access. Evaluate when the project needs multi-user access or multi-country deployment. See [ADR-002](architecture-decisions/002-ducklake-motherduck.md).
- [ ] **Adopt dbt MetricFlow / semantic layer** — Centrally define metrics (opportunity_gap, value_score, etc.) in MetricFlow semantic models instead of the current manual glossary. Currently blocked by Python 3.13 incompatibility, lack of Evidence.dev integration, and snapshot-grain data being a poor fit. Metric definitions are captured in `docs/ontology/glossary.yml` as a migration path. See [ADR-003](architecture-decisions/003-metricflow-deferred.md) for full rationale and revisit criteria.

---

## Squiz-Actionable Recommendations

**Goal:** Package Zeus's insights so they map directly to actions university marketing teams can execute in Squiz DXP — the CMS used by 15+ confirmed (and likely 22+) Australian universities. See [Squiz market research](research/squiz-university-cms.md) for full analysis.

### Phase 1: Recommendation Language

Frame Zeus report outputs using Squiz-native concepts so marketing teams can act immediately.

- [ ] **Landing page briefs per field of study** — For each high-opportunity field, generate a structured brief: target segment (who), target geography (where), headline messaging angles (career outcomes, salary, employment rate), and proof points. Designed to be handed to a Squiz content author or agency partner.
- [ ] **Personalization rule suggestions** — Translate Zeus's audience segments into Squiz personalization rules (e.g., "visitors from [LGA cluster] see [field] hero banner with [career outcome] messaging"). No technical integration — just documented rules a Squiz admin can configure.
- [ ] **A/B test hypotheses** — For each insight (opportunity gap, trending interest, emerging occupation), generate a testable hypothesis a marketing team can run in Squiz's A/B testing tool. Format: "Test [variant A] vs [variant B] for [segment] — expected lift based on [Zeus data point]."

### Phase 2: Course Finder Optimisation

Help universities make better use of Squiz's interactive course finder — often the highest-traffic prospective student page.

- [ ] **Course prominence recommendations** — Using field_value_proposition tiers and opportunity_gap data, recommend which courses to feature prominently in course finder results and category pages.
- [ ] **Course page messaging templates** — For each CRICOS course matched to a high-opportunity field, generate suggested copy blocks: career outcome stats, employment rate, salary data, and trending interest hooks.

### Phase 3: Channel Partner Enablement

Squiz implementation partners (FrontStage, Deepend, Ladoo, etc.) are the ones who build and configure university websites. They are a potential distribution channel for Zeus.

- [ ] **Research partner ecosystem** — Map which agencies serve which universities and identify potential channel partnerships or referral arrangements.
- [ ] **Create agency-facing summary format** — Condense Zeus insights into a format useful for Squiz implementation partners scoping website projects (e.g., "top 5 fields to feature for [university] based on local demand and graduate outcomes").
