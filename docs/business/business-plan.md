# Project Zeus — Business Plan

> **Last updated:** 2026-02-18
> **Status:** Draft

## Executive Summary

Project Zeus is a market research platform that helps Australian universities optimise
digital marketing campaigns for student acquisition. It combines publicly available
government data sources — job vacancy data, university admissions preferences, graduate
outcomes, student satisfaction surveys, and search trend signals — into actionable
targeting intelligence that answers three questions:

- **Who** to target (demographics, age, gender segments)
- **Where** to target (geographic, state-level audience signals)
- **What message** to use (field-of-study demand, career outcomes, trending interests)

The platform is designed for university marketing teams who currently rely on gut instinct,
siloed data, or expensive consulting engagements to make campaign targeting decisions.
Project Zeus replaces that with transparent, data-backed recommendations updated from
authoritative public sources.

---

## Problem

Australian universities spend significant budgets on digital marketing to attract domestic
students, but targeting decisions are often made without rigorous market intelligence:

1. **No single source of truth.** Job vacancy data, student preference trends, graduate
   outcomes, and search behaviour live in separate government datasets that are difficult
   to combine. Most university marketing teams don't have the data engineering capability
   to join and analyse them.

2. **Expensive alternatives.** The incumbent approach is either large consulting
   engagements or full-service enrolment marketing platforms (see [Competitive
   Landscape](#competitive-landscape) below) that bundle research with campaign execution
   at high cost. Smaller institutions are priced out.

3. **Stale and generic insight.** When market research does exist, it's often annual
   reports with national-level averages. University marketers need state-level, field-of-study-level, and demographic-level granularity to make decisions about specific campaigns.

4. **Misallocated spend.** Without demand signals, universities over-invest in fields
   where student interest already exceeds job market demand (e.g., Natural & Physical
   Sciences) and under-invest in fields with genuine opportunity gaps (e.g., Health, IT,
   Management & Commerce).

---

## Solution

Project Zeus is an analytics platform that ingests, standardises, and models public
government datasets into marketing-ready insights. It is built on an analytics-as-code
architecture (Dagster + dbt + DuckDB) with embedded reporting via Evidence.dev.

### Core Capabilities

| Capability | What It Delivers | Data Sources |
|---|---|---|
| **Opportunity Gap Analysis** | Fields of study where job demand exceeds student interest — the strongest "study this, jobs are waiting" messaging opportunities | IVI job vacancies, UAC first preferences |
| **Audience Profiling** | Gender split, mature learner affinity, and geographic origin per field of study — defines **who** to target | UAC preference demographics |
| **State Demand Index** | Graduate vacancies per 1,000 youth by state — identifies **where** to allocate marketing spend | IVI vacancies, ABS population data |
| **State × FOS Demand** | State-level demand by field of study with specialisation skew vs national average — pinpoints regional campaign opportunities | IVI vacancies |
| **Trending Interests** | Google Trends topics classified by field of study with opportunity gap context — identifies timely messaging hooks | Google Trends, opportunity gap model |
| **Historical Demand Trends** | 10-year applicant volumes by segment with YoY growth and CAGR — shows which fields are growing vs declining | UAC Early Bird data |
| **Graduate Outcomes** | Employment rates, median salaries (with gender split), and salary growth per field — evidence for career outcome messaging | QILT Graduate Outcomes Survey |
| **Institution Scorecard** | Per-university satisfaction and employment metrics — competitive benchmarking across 43 universities | QILT SES + GOS data |

### Delivery Format

Insights are delivered as interactive, embedded analytics dashboards (Evidence.dev) that
can be integrated into a client-facing web application. Reports are version-controlled
code artifacts — not manually configured dashboards — enabling rapid iteration, theming
to client branding, and row-level security at the database layer.

---

## Market Opportunity

### Target Market

Australian universities and higher education providers that run digital marketing
campaigns for student recruitment. The addressable market includes:

- **43 Australian universities** (primary target — 38 public, 5 private)
- **7 university colleges** (TEQSA-registered, emerging institutions)
- **156 non-university higher education providers** (secondary target)
- **University marketing agencies and Tertiary Admissions Centres** (channel partners)

Total TEQSA-registered higher education providers: **~206** (as at June 2024).

### The Australian Higher Education Sector

The sector generated **$45.2 billion in revenue in 2024**, up 13% from $40.0B in 2023.
Total enrolled students reached **1,676,077** — comprising 1,086,789 domestic students
and 481,851 onshore international students (a record high).

| Metric | Value | Year |
| --- | --- | --- |
| Total sector revenue | $45.2 billion | 2024 |
| Total enrolled students | 1,676,077 | 2024 |
| Domestic students | 1,086,789 (+1.0% YoY) | 2024 |
| International students (onshore) | 481,851 (+17.7% YoY) | 2024 |
| International student fee revenue | $12.3 billion (27% of total) | 2024 |
| Government funding share | ~47% ($21.2B) | 2024 |
| Education export value (all sectors) | $51.5 billion | 2024 |

Sources: Department of Education — [Finance 2024](https://www.education.gov.au/download/19832/finance-2024-financial-reports-higher-education-providers/43005/2024-university-finance-summary-information/pdf), [2024 Student Statistics](https://www.education.gov.au/higher-education-statistics/student-data/selected-higher-education-statistics-2024-student-data/key-findings-2024-higher-education-student-statistics), [TEQSA Annual Report 2023–24](https://www.teqsa.gov.au/sites/default/files/2024-10/teqsa-annual-report-2023-24.pdf)

### Marketing Spend

Australian public universities spent **$363 million on advertising, marketing, and
promotion in 2023** (Australia Institute). This represents roughly **0.9% of total
sector revenue** — well below global benchmarks where university marketing spend averages
a median of **5.3% of revenue** (with a mean of 11.9%).

This likely understates true marketing-related expenditure. Agent commissions for
international students (typically 20–25% of first-year tuition), digital marketing
embedded in other budgets, and consultancy fees are not captured in the headline figure.
Australian universities spent a further **~$410 million on consultancy services** in 2023.

Marketing efficiency varies enormously across the sector. In 2023, revenue return per
dollar of marketing spend ranged from **$24 (Charles Darwin University) to well above
the national average of $117** (HECG).

For comparison, in the US:
- Universities dedicate a median of **5.3% of revenue** to marketing (mean: 11.9%)
- Average cost per new student (professional/online programs): **$2,849** (UPCEA 2024)
- The global enrolment management software market is valued at **~$1.4 billion** (2024),
  projected to reach **$2.8–3.0 billion by 2030–33** at a ~9% CAGR

Sources: [Australia Institute — Elective Spending at Australian Universities](https://australiainstitute.org.au/report/elective-spending-at-australian-universities/), [HECG — Marketing Dollar Analysis](https://he-cg.com/which-universities-are-attracting-the-most-students-for-their-marketing-dollar/), [UPCEA — 2024 Marketing Survey](https://upcea.edu/key-findings-from-2024-upcea-marketing-survey/), [Verified Market Reports — Enrollment Management Software](https://www.verifiedmarketreports.com/product/enrollment-management-software-market/)

### Why Now — Converging Pressures

Five structural forces are converging to make data-driven marketing intelligence more
urgent for Australian universities than at any point in the sector's history.

#### 1. International student revenue is being capped

The Australian Government imposed hard caps on new international student commencements:
**270,000 in 2025** (of which 145,000 at public universities) and **295,000 in 2026**.
These caps are estimated to **reduce university revenue by $600 million annually**. New
international commencements dropped 15% to 190,799 by October 2025, and the share of
Chinese students — formerly 36% of international enrolments — has fallen to 23%.

Universities can no longer rely on growing international fees to cross-subsidise
operations. The pivot to domestic recruitment is not optional.

Sources: [SBS News — Student Caps](https://www.sbs.com.au/news/article/the-government-has-revealed-international-student-caps-from-2025-whats-been-announced/lu4rn9059), [ANU Analysis](https://cass.anu.edu.au/news/government-will-cap-new-international-students-270000-2025-number-may-not-be-reached)

#### 2. Domestic participation is structurally depressed

Domestic enrolments in 2024 (1,086,789) only just returned to 2019 levels after years of
post-COVID decline. Domestic commencing undergraduates hit their lowest point in a decade
in 2023, down 8.9% from the 2017 peak.

School-leaver demand remains **~3% below the mid-2010s peak** despite a growing Year 12
cohort. Key drivers:

- **Strong labour market** — low unemployment reduces the opportunity cost of not studying
- **VET/TAFE growth** — 508,000+ enrolments under the Fee-Free TAFE scheme since Jan 2023
- **Trade wages matching graduate salaries** — newly qualified electricians command a
  median of $75,000, comparable to entry-level graduate wages
- **"Degree doubt"** — growing scepticism about university ROI as graduate full-time
  employment rates slipped from 79% (2023) to 74% (2024)
- **HECS-HELP anxiety** — the 2023 indexation spike of 7.1% caused significant public
  backlash (partially addressed by a 20% reduction in outstanding HELP debt in Nov 2024)

Universities cannot wait for students to arrive — they must actively convince prospective
students that a degree is worth the investment.

Sources: [Andrew Norton — School-leaver interest](https://andrewnorton.id.au/2025/07/14/despite-an-increase-in-applications-for-the-2024-academic-year-school-leaver-interest-in-higher-education-remains-below-mid-2010s-levels/), [Dept of Education — 2024 Key Findings](https://www.education.gov.au/higher-education-statistics/student-data/selected-higher-education-statistics-2024-student-data/key-findings-2024-higher-education-student-statistics)

#### 3. The Universities Accord creates a use-it-or-lose-it funding dynamic

The Universities Accord (February 2024) — the most significant sector review in 15
years — committed **$2.5 billion** to a new Managed Growth Funding system commencing
January 2026, with a target of **80% of working-age Australians holding a tertiary
qualification by 2050**. This includes **82,000 additional funded university places by
2035**.

The critical dynamic: universities will receive Domestic Student Profiles allocating
funded places. Institutions that **under-enrol against their profile will see funding
maintained only in nominal terms** — a real-terms cut. This creates a direct financial
incentive to invest in recruitment to fill allocated places.

Meanwhile, real funding per Commonwealth-supported student has **fallen ~6% since 2017**
despite student growth, compressing margins further.

Sources: [Dept of Education — Managed Growth Funding](https://www.education.gov.au/australian-universities-accord/accord-202425-budget-and-myefo-measures/managed-growth-funding), [Universities Accord Final Report Summary](https://www.education.gov.au/download/17995/australian-universities-accord-final-report-summary-report/36761/australian-universities-accord-final-report-summary-report/pdf)

#### 4. Regional and mid-tier institutions face existential pressure

The competitive dynamics are most acute for non-Group-of-Eight institutions:

- **Federation University** announced 200 staff cuts (20% of workforce) due to enrolment
  and funding pressures
- **University of Canberra** forecast a $36 million deficit in 2024
- 11 universities proposed at least **2,091 job losses** in late 2024
- In Queensland, only **2 of 7 universities** recorded a profit in 2023

These institutions — Project Zeus's primary target — are the most likely to seek
cost-effective, data-driven alternatives to expensive consulting engagements or
full-service marketing platforms.

Sources: [Nature — Falling Enrolments](https://www.nature.com/articles/d41586-024-03638-1), [Federation University — City Flight](https://www.federation.edu.au/about/news/news/city-flight-is-blocking-australias-education-goals--regional-universities-need-urgent-investment-now/)

#### 5. Digital marketing maturity is low — creating whitespace

A Siteimprove survey found that while 90% of Australian higher ed digital marketers
believe they are investing in digital, **zero respondents said their digital elements are
fully integrated** across the institution or used to drive marketing decisions. The sector
is spending on marketing without the targeting intelligence to direct it effectively.

This is exactly the gap Project Zeus fills — not more marketing spend, but smarter
allocation of existing spend through data-backed targeting.

Sources: [MARKETECH APAC — Digital Marketing Lagging Behind](https://marketech-apac.com/digital-marketing-in-australias-higher-education-lagging-behind-report/), [Universities Australia — Critical Challenges](https://universitiesaustralia.edu.au/wp-content/uploads/2024/11/UA091-Critical-challenges-in-Australias-university-sector_v2.pdf)

---

## Competitive Landscape

### EAB (Education Advisory Board) — The US Incumbent

> Full analysis: [EAB Competitor Analysis](/docs/research/eab-competitor-analysis.md)

EAB is the dominant player in the US higher education enrolment marketing space, serving
**2,500+ institutions** with estimated annual revenue of **~$175M–$214M USD**. Their
product suite spans the full student lifecycle:

| Product | Scale | Relevance to Zeus |
|---|---|---|
| **Enroll360** | 1,200+ partner schools | **Direct competitor** — full-funnel enrolment marketing with data-driven audience targeting, AI-powered personalisation, and 13 specialist teams per partner |
| **Navigate360** | 850+ institutions, 10M+ students | CRM that would *consume* targeting intelligence like Zeus produces |
| **Appily** | 3M+ students, 4,000+ college profiles | Proprietary first-party demand capture — a data moat Zeus cannot replicate |
| **Edify** | 250+ institutions | Data platform with 200+ higher-ed-specific definitions — a packaging model Zeus could learn from |
| **Adult Learner** | 200+ partners | Separate segment with distinct targeting needs |
| **Strategic Advisory** | 2,100+ partners | Consulting and research at scale |

#### EAB's Strengths

- **Scale and integration.** EAB bundles market research, campaign execution, CRM, lead
  generation, and advisory into a single ecosystem. Switching costs are high.
- **Proprietary data.** Appily gives EAB first-party student intent signals at massive
  scale (3M+ students, 1.5B+ interactions/year). This cannot be replicated with public
  data alone.
- **Service model.** Dedicated Strategic Leaders with 13 specialist teams per partner —
  EAB positions as an outsourced marketing department, not a tool.
- **Performance claims.** 16% average enrolment increase, 6.3x higher enrolment
  likelihood for Cultivate campaigns.

#### EAB's Limitations (Zeus's Opportunity)

- **US/Canada focus.** EAB does not serve the Australian market, leaving a geographic gap.
- **Opaque methodology.** EAB's audience strategies are proprietary black boxes.
  Universities can't inspect the logic, validate the data sources, or adapt the methodology
  to their institutional context.
- **Bundled pricing.** Full-service pricing excludes smaller institutions. Not every
  university needs (or can afford) an outsourced marketing department.
- **No Australian data.** EAB's models are built on US datasets (SAT scores, Common App
  data, College Board feeds). They have no coverage of Australian government data sources
  like IVI, UAC, QILT, or ABS.

### Other Competitors (Australian Market)

| Competitor | Type | Overlap with Zeus |
|---|---|---|
| **Management consulting firms** (EY, Deloitte, etc.) | Project-based consulting | Produce one-off market reports; not productised, not continuously updated |
| **Good Universities Guide** | Lead gen + advertising | Provides institutional rankings; doesn't offer targeting intelligence |
| **StudySelect / CourseFinder** | Lead gen | Demand capture channels, not research tools |
| **In-house analytics teams** | Internal | Some Group of Eight universities have strong internal capabilities; most don't |

### Competitive Positioning

Project Zeus occupies a distinct position: **upstream targeting intelligence** from
transparent public data sources, delivered as a continuously updated data product rather
than a one-off consulting engagement.

| Dimension | EAB | Consulting Firms | Project Zeus |
|---|---|---|---|
| **Geography** | US/Canada | Global (project basis) | Australia |
| **Data transparency** | Proprietary / opaque | Varies | Public sources, methodology visible |
| **Update frequency** | Continuous (real-time campaigns) | One-off / annual | Continuous (automated pipelines) |
| **Scope** | Full-funnel (research → execution) | Research and strategy | Upstream targeting research |
| **Price point** | High (full-service) | High (consulting rates) | Lower (data product) |
| **Client capability required** | Low (EAB executes) | Low (consultant delivers) | Medium (client acts on insights) |

---

## Business Model

### Revenue Model Options

The business model is still being validated. Three potential approaches, not mutually
exclusive:

#### Option A: SaaS Subscription

Universities subscribe for ongoing access to the analytics platform and dashboards.

- **Pricing:** Tiered by institution size or number of report modules
- **Pros:** Predictable recurring revenue; aligns with continuous data updates
- **Cons:** Requires a polished self-service product; longer sales cycle

#### Option B: Insights-as-a-Service

Deliver periodic research reports and targeting recommendations, combining automated
analysis with human interpretation.

- **Pricing:** Per-report or retainer
- **Pros:** Lower product maturity required; higher perceived value per engagement
- **Cons:** Less scalable; consulting-adjacent

#### Option C: Embedded Analytics (White-Label)

License the data models and visualisations to platforms that already serve universities
(CRMs, marketing agencies, TACs).

- **Pricing:** Platform licensing or revenue share
- **Pros:** Leverages existing distribution; avoids direct university sales
- **Cons:** Lower margin; dependent on partner relationships

### Cost Structure

Project Zeus is built on open-source and low-cost infrastructure:

- **Data sources:** Free (all government open data)
- **Compute:** DuckDB (local/embedded), Dagster (open-source orchestration)
- **Reporting:** Evidence.dev (open-source embedded analytics)
- **Hosting:** Minimal — cloud hosting costs scale with usage, not data volume
- **Primary cost:** Development time and domain expertise

---

## Go-to-Market Strategy

### Phase 1: Validate with Pilot Institutions (Current)

- Build the complete data platform with all core analysis models
- Create the Evidence.dev report suite demonstrating each targeting dimension
- Approach **2–3 mid-tier Australian universities** (not Group of Eight, who may have
  internal capabilities) for pilot engagements
- Validate willingness to pay and identify which insights drive the most value

### Phase 2: Productise

- Package insights into repeatable report modules (opportunity gap, audience profiles,
  state demand, graduate outcomes)
- Build self-service dashboard access with institution-specific filtering
- Implement row-level security and embed analytics into a client-facing application
- Develop white-label theming for institutional branding

### Phase 3: Scale

- Expand data sources (CRICOS course listings, QTAC, VTAC/SATAC/TISC)
- Add institution-specific recommendations ("promote your [X] degree because...")
- Explore channel partnerships with university marketing agencies or TACs
- Consider international expansion (UK UCAS data, Canadian equivalents)

---

## Current Traction

### Product Status

The core data platform is built and operational:

- **8 analysis models** completed and producing insights (opportunity gap, audience
  profiles, state demand, trending interests, historical demand, graduate outcomes,
  institution scorecard, state × FOS demand)
- **6 interactive report pages** built in Evidence.dev with data source attribution
- **Automated data pipelines** via Dagster ingesting IVI, UAC, ABS, Google Trends,
  and QILT datasets
- **DuckDB warehouse** with standardised staging models mapping across different
  government classification systems (ANZSCO, ASCED, UAC FOS categories)

### Planned Next Steps

- Ingest CRICOS course data to connect opportunity gaps to specific programs
- Prototype embedded analytics (iframe integration with row-level security)
- Develop pilot engagement materials for university marketing teams

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Universities don't pay for insight alone** — they want execution (campaign management, lead gen) | Medium | High | Position as complementary to existing agencies/platforms; explore embedded/white-label model |
| **Data source availability changes** — government datasets could be restructured or discontinued | Low | High | Multiple independent sources reduce single-source dependency; automated pipeline monitoring |
| **EAB enters Australia** — the incumbent decides to expand geographically | Low | Medium | First-mover advantage with AU-specific data and relationships; EAB's US data models don't transfer directly |
| **In-house analytics teams replicate the work** — Group of Eight universities build internally | Medium | Low | Target mid-tier institutions without data teams; maintain speed-to-insight advantage through productisation |
| **Small addressable market** — 43 universities is a limited customer base | High | Medium | Expand to non-university providers (~90), marketing agencies, and TACs; consider adjacent markets (vocational, international) |

---

## Appendices

- [EAB Competitor Analysis](/docs/research/eab-competitor-analysis.md)
- [Student Search Platforms](/docs/insights/student-search-platforms.md)
- [Opportunity Gap Analysis](/docs/insights/opportunity-gap.md)
- [Product Roadmap](/docs/roadmap.md)
- [Architecture](/docs/architecture.md)
