# Evidence Reports

Markdown-based analytics dashboards powered by [Evidence.dev](https://evidence.dev/), reading from the DuckDB warehouse produced by the Dagster + dbt pipeline in `analytics/`.

## Prerequisites

- Node.js 18+ and npm 7+
- DuckDB warehouse with materialised mart tables (run `DAGSTER_HOME=$(pwd)/.dagster_home uv run dg dev` from `analytics/` first, or `uv run dbt build --project-dir dbt_project`)

## Getting Started

```bash
npm install
npm run sources
npm run dev
```

The dev server starts at **http://localhost:3000** (or the next available port). Evidence uses npm — not uv — since it is a Node.js application.

## Key Commands

| Command | Description |
|---------|-------------|
| `npm run sources` | Pull latest data from DuckDB into Evidence cache |
| `npm run dev` | Start the local dev server with hot reload |
| `npm run build` | Build a static production site into `build/` |

## Project Structure

```
sources/zeus/
  connection.yaml           DuckDB connection config
  opportunity_gap.sql       Opportunity gap mart query
  opportunity_gap_by_gender.sql  Gender breakdown query
  state_demand_index.sql    State demand query
pages/
  index.md                  Main dashboard page
```

## Refreshing Data

After materialising new or updated dbt models, re-run `npm run sources` to refresh the Evidence data cache, then reload the dev server.
