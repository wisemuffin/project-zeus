# Project Zeus - Market Research

## Project Mission
Project Zeus provides market research to help universities optimise digital marketing
campaigns for student acquisition. Every asset and analysis should serve one of:
- **Who** to target (demographics, age, gender segments)
- **Where** to target (geographic, state-level audience signals)
- **What message** to use (field-of-study demand, career outcome data, trending interests)

## Multi-Country Workspace Structure
The project is a `dg` workspace with separate code locations per country:
- `projects/analytics-au/` — Australian data pipeline (Dagster + dbt + DuckDB)
- `reports/au/` — Australian Evidence.dev dashboards
- Future countries slot in as `projects/analytics-uk/`, `reports/uk/`, etc.

Each country has its own DuckDB warehouse, dbt project, and Evidence reports.

## Asset & Model Documentation
Every Dagster asset and dbt model must document both **what it contains** and **the use case** for the data:

### Dagster Assets
- Asset docstrings are the primary documentation (visible in Dagster UI)
- Docstrings must include:
  - **What**: what the data contains (source, granularity, key columns)
  - **Use case**: how it supports marketing targeting (which of Who/Where/What message it serves)
  - **Limitations**: known caveats or data quality notes
- Always add `context.add_output_metadata()` with row_count and source_url at minimum
- Source assets must include `kinds=` for UI badges indicating ingestion method. Use two values: `"python"` plus one of:
  - `"api"` — structured REST/SDMX API
  - `"rss"` — RSS feed
  - `"csv"` — CSV file download
  - `"excel"` — Excel/ZIP file download
  - `"scraping"` — HTML table parsing
  - `"pdf"` — PDF table extraction
  - `"python"` only — hardcoded/manual data
- Source assets must also include an `"ingestion"` key in `tags={}` with one of: `api`, `rss`, `file_download`, `web_scraping`, `pdf_extraction`, `manual`

### dbt Models
- Every model must have a `description` in its schema YAML that covers:
  - **What**: what the model contains and its grain
  - **Use case**: how it supports marketing targeting decisions
- Column descriptions should clarify meaning, not just repeat the column name

## Evidence Reports
- Every report page must include a collapsible **Data Sources** section at the bottom using the `<Details title="Data Sources">` component
- The Data Sources section should list each source used on that page with: organisation name, description, geographic scope, and key limitations
- The intro paragraph on each page should name the source organisations upfront (bolded)

## Insights Documentation
- When analysis models produce actionable findings, document them in `docs/insights/`
- Each insight doc should include: source models, key findings, marketing angles, and limitations

## Data Ingestion with dlt
- Use dlt (`dagster-dlt`) for new data source assets where the extraction is straightforward
  (REST APIs, CSV/JSON file downloads, RSS feeds)
- Do NOT use dlt when the core value is custom parsing logic (complex Excel section
  detection, PDF extraction, HTML scraping with BeautifulSoup)
- dlt assets use `@dlt_assets` decorator with a custom `DagsterDltTranslator`
- dlt writes directly to DuckDB (`analytics.duckdb`, schema `public`) — these assets
  bypass the `DuckDBPandasIOManager`
- Non-dlt assets continue to return `pd.DataFrame` and use the IO manager as before
- All dlt resources must use `write_disposition="replace"` (full refresh each run)
- Resource `name=` must match the expected DuckDB table name and dbt source name
- dlt assets add `"dlt"` to `kinds=` alongside the existing method badge (e.g. `{"python", "api", "dlt"}`)

## Python Dependencies
- Use `uv` to manage Python environments and dependencies
- Always use `uv add <package>` to install packages (not pip)
- Use `uv run` to execute commands within the project environment
