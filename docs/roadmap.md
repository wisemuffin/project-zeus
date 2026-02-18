# Project Zeus - Market Research Roadmap

## Analysis Models (dbt)

Mart models that transform raw Dagster assets into marketing-actionable insights. Each answers a core targeting question.

### Completed

- [x] **Opportunity Gap** (`opportunity_gap`) — Which fields of study have high job demand but low student interest? Strongest messaging opportunities.
- [x] **Opportunity Gap by Gender** (`opportunity_gap_by_gender`) — Which high-gap fields skew male or female? Enables gender-targeted ad creative.
- [x] **State Demand Index** (`state_demand_index`) — Graduate vacancies per 1,000 youth by state. Identifies geographic hotspots for marketing spend.

- [x] **Audience Profile by FOS** (`audience_profile_by_fos`) — Gender, mature learner affinity, and geographic origin per field. Answers **who** to target and **where** they are.
- [x] **Trending Interests** (`trending_interests`) — Google Trends classified by FOS with opportunity gap context. Identifies timely messaging hooks.

### Planned
- [ ] **Historical demand trends** — Use `uac_early_bird_closing_count` to track year-over-year shifts in applicant volumes. Identifies growing vs declining fields for budget allocation.

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
