# Project Zeus - Market Research Roadmap

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
