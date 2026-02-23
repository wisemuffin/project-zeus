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

### Investigated (No Action)

| Platform | Finding |
|----------|---------|
| **QTAC** ([qtac.edu.au](https://www.qtac.edu.au/)) | No FOS preference data published. Only ATAR scaling reports (PDFs). Parked. |
| **TISC** ([tisc.edu.au](https://www.tisc.edu.au/)) | No FOS data found. Has a formal data request process. |
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

- [x] **Evaluate Evidence.dev** — Scaffolded local Evidence project in `reports/`, connected to DuckDB warehouse, built MVP dashboard with opportunity gap, gender, and state demand visualisations.

### Report Pages

- [x] **Opportunity Gap Dashboard** (`pages/index.md`) — BigValue cards, vacancy vs preference bar charts, gender skew, state demand density. Covers opportunity_gap, opportunity_gap_by_gender, and state_demand_index marts.
- [x] **Audience Profiles** (`pages/audience-profiles.md`) — Who to target per field: gender split, mature learner index, geographic origin (NSW/ACT/interstate draw). Sources from audience_profile_by_fos mart.
- [x] **Trending Interests** (`pages/trending-interests.md`) — Google Trends matched to fields of study with opportunity gap context and marketing signals. Sources from trending_interests mart.
- [x] **Historical Demand** (`pages/historical-demand.md`) — 10-year applicant volume trends by segment with YoY growth, CAGR, and recovery ratios. Sources from historical_demand_trends mart.
- [x] **Graduate Outcomes** (`pages/graduate-outcomes.md`) — Salary by gender, FT employment rates (YoY), marketing signal matrix, salary gender gap. Sources from graduate_outcomes_by_fos mart + QILT GOS data.
- [x] **Institution Scorecard** (`pages/institution-scorecard.md`) — Per-university satisfaction vs employment scatter, satisfaction indicators, full scorecard with sector comparison. Sources from institution_scorecard mart + QILT SES/GOS data.
- [x] **State Preference Comparison** (`pages/state-preferences.md`) — Cross-state comparison of field-of-study preferences across NSW/ACT (UAC), Victoria (VTAC), and SA/NT (SATAC). Grouped bar charts, divergence table, gender split by state. Sources from stg_national_fos_preferences.

### Future

- [ ] Set up database-level row-level security policies
- [ ] Prototype iframe embedding in the application
- [ ] Implement theming to match product branding
