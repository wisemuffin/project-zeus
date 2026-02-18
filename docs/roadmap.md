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
- [ ] Download and explore GOS report tables to understand sheet structure
- [ ] Build Dagster asset for GOS data (employment rates & salaries by field of study)
- [ ] Build Dagster asset for SES data (student satisfaction by field of study)
- [ ] Create dbt staging models to standardise QILT field-of-study names to UAC categories
- [ ] Build mart model: **graduate_outcomes_by_fos** — joins GOS employment/salary data with opportunity gap analysis
- [ ] Build mart model: **institution_scorecard** — per-university satisfaction + outcomes for competitive benchmarking

### Priority 2: QTAC (Queensland Tertiary Admissions Centre)

**Source:** [qtac.edu.au](https://www.qtac.edu.au/) | **Owner:** QLD consortium
**Access:** TBD — need to investigate published statistics
**Coverage:** QLD / Northern NSW (1,800+ courses)

Would extend UAC-style preference analysis to Queensland, covering Australia's two largest higher-ed markets.

- [ ] Investigate QTAC published statistics and data availability
- [ ] Assess whether data format is comparable to UAC for unified staging models

### Priority 3: Other Accessible Platforms

| Platform | Data | Status |
|----------|------|--------|
| **CourseSeeker** ([courseseeker.edu.au](https://www.courseseeker.edu.au/)) | National course listings across all institutions | Not yet investigated |
| **VTAC / SATAC / TISC** | State-level admissions stats for VIC, SA, WA | Not yet investigated — each TAC publishes differently |
| **Good Universities Guide** ([gooduniversitiesguide.com.au](https://www.gooduniversitiesguide.com.au/)) | University ratings & rankings | Not yet investigated |

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

### Next Steps

- [ ] Evaluate Evidence.dev as the embedded analytics platform
- [ ] Define initial set of reports/dashboards to embed
- [ ] Set up database-level row-level security policies
- [ ] Prototype iframe embedding in the application
- [ ] Implement theming to match product branding
