# Project Zeus - Market Research

## Project Mission
Project Zeus provides market research to help universities optimise digital marketing
campaigns for student acquisition. Every asset and analysis should serve one of:
- **Who** to target (demographics, age, gender segments)
- **Where** to target (geographic, state-level audience signals)
- **What message** to use (field-of-study demand, career outcome data, trending interests)

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

## Python Dependencies
- Use `uv` to manage Python environments and dependencies
- Always use `uv add <package>` to install packages (not pip)
- Use `uv run` to execute commands within the project environment
