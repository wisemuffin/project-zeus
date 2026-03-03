# ADR-001: VS Code Extension for dbt Development

**Date:** 2026-03-03
**Status:** Accepted
**Decision:** Use dbt Power User (Altimate) for local dbt development in VS Code

## Context

We need a VS Code extension to support local dbt development across the team. The extension should provide SQL intelligence (autocomplete, go-to-definition), compiled SQL preview, lineage visualisation, and integrate with our dbt-core + DuckDB stack.

Two options were evaluated:

1. **dbt Power User** (Altimate) — https://docs.myaltimate.com/
2. **dbt Labs Official Extension** — https://docs.getdbt.com/docs/install-dbt-extension

## Options

### Option 1: dbt Power User (Altimate)

An open-source VS Code extension by Altimate AI.

**Pros:**
- Compatible with dbt-core (our current engine)
- Works with DuckDB connections
- Free tier covers core features: autocomplete, go-to-definition, SQL compilation preview, model-level lineage, query result preview
- Optional AI-powered features (doc generation, test generation, SQL translation) available via free API key
- Column-level lineage visualisation
- Active community and regular updates

**Cons:**
- AI features require an Altimate API key (free but external dependency)
- Third-party extension, not maintained by dbt Labs

### Option 2: dbt Labs Official Extension

The official VS Code extension from dbt Labs, powered by the dbt Fusion engine.

**Pros:**
- Official first-party support from dbt Labs
- Built-in LSP with code intelligence
- Free for up to 15 users
- No dbt Cloud account required

**Cons:**
- **Requires the dbt Fusion engine — incompatible with dbt-core**
- Our project runs dbt-core via Dagster, making this extension unusable
- Requires registration within 14 days of installation
- Newer product with less community track record

## Decision

**Use dbt Power User (Altimate).**

The official dbt extension is incompatible with our stack because it requires the dbt Fusion engine rather than dbt-core. Since our project runs dbt-core with DuckDB orchestrated by Dagster, the official extension is not an option.

dbt Power User supports dbt-core and DuckDB directly, and its free tier provides everything we need for day-to-day development.

## Consequences

- Team members should install the "Power User for dbt" extension from the VS Code marketplace
- Configure the extension to point at the relevant dbt project (e.g. `projects/analytics-au/analytics_au/dbt`)
- If the official extension adds dbt-core support in the future, this decision should be revisited
