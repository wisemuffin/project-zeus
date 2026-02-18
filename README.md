# Project Zeus - Market Research

Market research platform to help universities optimise digital marketing campaigns for student acquisition. Combines Australian Government labour market data, UAC application preferences, and ABS population estimates to answer: **who** to target, **where** to target, and **what message** to use.

## Architecture

```
analytics/          Dagster + dbt pipeline (Python, DuckDB)
reports/            Evidence.dev dashboards (Node.js, markdown-based)
docs/               Research notes and insight write-ups
```

Dagster orchestrates dbt models that transform raw data into mart tables in a local DuckDB warehouse. Evidence reads from that same DuckDB file to render interactive reports.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 18+ and npm 7+

## Running the Analytics Pipeline (Dagster + dbt)

```bash
cd analytics
uv sync
DAGSTER_HOME=$(pwd)/.dagster_home uv run dg dev
```

Open **http://localhost:3000** to access the Dagster UI. From there you can materialise assets, view lineage, and inspect run history.

To build dbt models directly (without the Dagster UI):

```bash
cd analytics
uv run dbt build --project-dir dbt_project
```

## Running the Reports Dashboard (Evidence)

```bash
cd reports
npm install
npm run sources    # extract data from DuckDB into Evidence cache
npm run dev        # start the dev server
```

Open **http://localhost:3000** (or the next available port if 3000 is in use) to view the dashboard.

After updating dbt models, re-run `npm run sources` to refresh the Evidence data cache.
