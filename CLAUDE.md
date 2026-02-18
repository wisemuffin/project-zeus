# Project Zeus - Market Research

## Project Mission
Project Zeus provides market research to help universities optimise digital marketing
campaigns for student acquisition. Every asset and analysis should serve one of:
- **Who** to target (demographics, age, gender segments)
- **Where** to target (geographic, state-level audience signals)
- **What message** to use (field-of-study demand, career outcome data, trending interests)

## Asset Conventions
- Asset docstrings are the primary documentation (visible in Dagster UI)
- Docstrings should explain: what the data is, how it supports marketing targeting,
  key columns, and limitations
- Always add `context.add_output_metadata()` with row_count and source_url at minimum

## Insights Documentation
- When analysis models produce actionable findings, document them in `docs/insights/`
- Each insight doc should include: source models, key findings, marketing angles, and limitations

## Python Dependencies
- Use `uv` to manage Python environments and dependencies
- Always use `uv add <package>` to install packages (not pip)
- Use `uv run` to execute commands within the project environment
