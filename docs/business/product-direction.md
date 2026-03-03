# Product Direction: Evidence.dev as the Product

> **Last updated:** 2026-03-03
> **Status:** Draft — documents the current POC approach

## Decision

**Use Evidence.dev as the product platform.** Do not build a separate website or custom
web application for the POC or early pilot phase.

## Context

The question was whether to build a customer-facing website to deliver personalised
university marketing briefs, or to use the existing Evidence.dev report suite as the
product.

We considered three options:

| Option | What it means | Verdict |
|---|---|---|
| **Custom website** (React/Next.js) | Build a separate web app with university login, dashboards, report generation | Rejected — duplicates Evidence, delays sales by months, adds engineering cost before validating demand |
| **Evidence.dev as the product** | Use the existing 40-page report suite with a new per-university brief page as the demo and delivery platform | **Selected** — already built, interactive, deployable as static site |
| **PDF-only briefs** | Generate static PDF reports per university, no interactive product | Partially adopted — PDFs serve a role in cold outreach but are not the product |

## Why Evidence, Not a Custom Website

### 1. The product already exists

Evidence.dev gives us 40 interactive report pages, charts, maps, searchable tables, and
a DuckDB backend — all version-controlled and deployable as a static site. Building a
React app to replicate this would take months and produce an inferior first version.

### 2. The demo IS the product

In a sales walkthrough, we screen-share the Evidence dashboard and show a university
their own data live. Interactive filtering, drill-downs, the full report suite — that's
what proves the product is real and worth paying for. A static PDF can't do this.

### 3. Zero infrastructure complexity

Evidence builds to static HTML + Parquet files. It can be hosted on any static hosting
service (Netlify, Vercel, S3, GitHub Pages) with no backend, no database connection at
runtime, and no server to maintain. The data is baked in at build time.

### 4. Iteration speed

Adding a new analysis, chart, or report section is a markdown file with SQL queries.
No frontend/backend coordination, no API endpoints, no state management. We can respond
to pilot customer feedback in hours, not weeks.

### 5. Staying upstream of execution

Per our [integration strategy](integration-strategy.md), we are the intelligence layer —
not a marketing execution platform. Evidence is perfectly suited to this: it delivers
data and recommendations that universities act on with their own tools. We don't need
user accounts, campaign management, or CRM integration.

## Where a Custom Website Would Make Sense (Later)

A custom web application becomes necessary when:

- **Multi-tenancy with access control** — multiple universities each seeing only their
  own data. Evidence doesn't have built-in authentication or row-level security.
- **Self-service onboarding** — a university signs up, selects their institution, and
  gets an instant dashboard. Currently this requires us to generate and deploy.
- **White-label branding** — each university sees reports styled with their brand colours
  and logo. Evidence supports theming but not per-tenant theming.
- **API access** — universities want to pull Zeus data into their own BI tools
  programmatically.

These are Phase 2/3 needs. They require paying customers to justify the investment.

## Product Delivery by Sales Stage

The product takes different forms depending on where a prospect is in the sales funnel:

### Cold Outreach: PDF Brief

**Format:** Personalised marketing intelligence brief (PDF or well-formatted email
attachment)

**Purpose:** Get a meeting. The brief demonstrates value before any commercial
conversation — "Here's what the public data says about your competitive position."

**How it's produced:** Use the Evidence university brief page to pull data, then write
1-2 pages of narrative interpretation per university. The narrative (identifying the
"story" in the data, crafting campaign recommendations) is the human value-add that
differentiates us from raw data.

**Example:** [University of Wollongong brief](example-brief-uow.md)

### Sales Walkthrough: Live Evidence Dashboard

**Format:** Screen-shared Evidence.dev dashboard with the university brief page selected

**Purpose:** Prove the product is real, interactive, and continuously updated. Show
the prospect their data live, drill into specific fields, explore the state demand
map, browse their course portfolio.

**How it's produced:** Already built. Select the university from the dropdown.

### Pilot Engagement: Hosted Evidence Instance

**Format:** Private URL to an Evidence.dev deployment, potentially with a simple
password gate (e.g., Cloudflare Access or Netlify password protection)

**Purpose:** Ongoing access to the full report suite for the duration of the pilot.
The university's marketing team can explore data independently, screenshot charts for
internal presentations, and export targeting data.

**How it's produced:** Deploy Evidence as a static site. For the first 1-2 pilots,
a single deployment with institution-level filtering is sufficient. Per-tenant
deployments can come later if needed.

### Scaled Product: Custom Application (Future)

**Format:** Multi-tenant web application with authentication, per-university views,
and potentially API access

**Purpose:** Support 5-10+ customers simultaneously with proper access control and
self-service. This is the Phase 2/3 product.

**How it's produced:** Not yet determined. Options include wrapping Evidence in an
authentication layer, building a custom frontend that queries the same DuckDB models,
or migrating to a SaaS analytics platform. The decision should be informed by what
pilot customers actually need.

## Current Product Architecture

```
DuckDB warehouse (analytics.duckdb)
    ↓
dbt models (marts schema) — 20+ analysis models
    ↓
Evidence SQL sources — extract mart data to Parquet
    ↓
Evidence.dev pages — 40+ interactive report pages
    ↓
Static site deployment — HTML + Parquet, no backend
```

### Key pages for the sales process

| Page | Purpose | URL |
|---|---|---|
| **University Brief** | Per-university intelligence (dropdown selector) | `/university-brief` |
| **Brand Awareness** | Interest vs quality scatter, state map | `/audiences/brand-awareness` |
| **Institution Scorecard** | Satisfaction + employment benchmarks | `/audiences/institution-scorecard` |
| **Course Listings** | Program portfolio with opportunity context | `/audiences/course-listings` |
| **Opportunity Gap** | National field prioritisation | `/insights/opportunity-gap` |
| **Landing Page** | Overview + navigation | `/` |

## What We're Not Building (Yet)

| Capability | Why not now |
|---|---|
| **User accounts / login** | No multi-tenant need with 1-2 pilots; password-protect the URL instead |
| **Report generation / PDF export** | The narrative interpretation is manual and valuable; automate later when the format stabilises |
| **CRM integration** | Per [integration strategy](integration-strategy.md) — we stay upstream |
| **Custom branding per university** | Evidence supports one theme; per-tenant theming is a Phase 3 feature |
| **Mobile app** | Evidence is responsive; no separate app needed |
| **API endpoints** | No customer has asked for programmatic access yet |

## Principles

1. **Ship what we have.** The Evidence report suite is the product. Don't rebuild it in
   a different framework before validating that anyone wants to pay for it.
2. **Narrative is the differentiator.** The hand-written interpretation of the data
   (campaign recommendations, competitive positioning stories) is what makes a brief
   valuable, not the charts. Don't try to fully automate this.
3. **Build for the next 2 customers, not the next 20.** Every architectural decision
   should be justified by current or imminent need, not hypothetical scale.
4. **Evidence is disposable.** If we outgrow it, the valuable assets are the dbt models
   and DuckDB warehouse, not the report pages. Evidence pages are markdown files — they
   can be rebuilt in any frontend framework using the same data layer.
