# Project Zeus - Market Research

Market research platform to help universities optimise digital marketing campaigns for student acquisition. Combines government labour market data, admissions preferences, and population estimates to answer: **who** to target, **where** to target, and **what message** to use.

## Architecture

```
projects/
  analytics-au/     Dagster + dbt pipeline for Australia (Python, DuckDB)
reports/
  au/               Evidence.dev dashboards for Australia (Node.js, markdown-based)
docs/               Research notes and insight write-ups
```

The project is structured as a **multi-country workspace**. Each country gets its own Dagster code location (`projects/analytics-<cc>/`), DuckDB warehouse, dbt project, and Evidence reports (`reports/<cc>/`). Currently only Australia (AU) is implemented.

Dagster orchestrates dbt models that transform raw data into mart tables in a local DuckDB warehouse. Evidence reads from that same DuckDB file to render interactive reports.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 18+ and npm 7+

## Running the Analytics Pipeline (Dagster + dbt)

```bash
cd projects/analytics-au
uv sync
DAGSTER_HOME=$(pwd)/../../.dagster_home uv run dg dev
```

Open **http://localhost:3000** to access the Dagster UI. From there you can materialise assets, view lineage, and inspect run history.

To build dbt models directly (without the Dagster UI):

```bash
cd projects/analytics-au
uv run dbt build --project-dir dbt_project
```

## Running the Reports Dashboard (Evidence)

```bash
cd reports/au
npm install
npm run sources    # extract data from DuckDB into Evidence cache
npm run dev        # start the dev server
```

Open **http://localhost:3000** (or the next available port if 3000 is in use) to view the dashboard.

### Refreshing the Evidence Source Cache

Evidence caches query results as parquet files in `.evidence/template/static/data/`. It does **not** automatically detect changes in the upstream DuckDB database. You must re-run the source extraction whenever:

- You materialise assets or rebuild dbt models in the analytics pipeline
- You add a new source SQL file under `reports/au/sources/zeus/`
- You see "Table does not exist" errors in Evidence for tables you know exist in DuckDB

```bash
cd reports/au
npm run sources    # re-extracts all source queries from DuckDB
```

If the dev server is running, restart it after refreshing sources.
