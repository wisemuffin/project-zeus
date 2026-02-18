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

- **43 Australian universities** (the primary target)
- **~90 non-university higher education providers** (secondary)
- **Tertiary Admissions Centres** (potential channel partners)

### Market Sizing Indicators

- Australian university marketing budgets are not publicly disclosed at scale, but
  individual institutions are known to spend **$1M–$10M+ annually** on student
  recruitment marketing depending on size and ambition.
- The total Australian higher education market was valued at **~$45B AUD** in 2024 (DESE),
  making even fractional marketing intelligence spend a meaningful category.
- EAB — the closest US analogue — generates an estimated **~$175M–$214M USD** annually
  across its full product suite, demonstrating the revenue potential of the broader
  category (though EAB operates at significantly larger scale across 2,500+ US/Canadian
  institutions).

### Why Now

- **Post-COVID enrolment recovery** is uneven across fields, creating urgency for
  data-driven reallocation of marketing budgets.
- **Government data availability** has improved significantly — QILT, IVI, and UAC
  datasets are now freely accessible, but no product synthesises them.
- **Rising competition** for domestic students as international enrolment patterns shift,
  pushing universities to optimise domestic acquisition.

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
