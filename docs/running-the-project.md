# Running the Project

## Prerequisites

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

From the `projects/analytics-au/` directory:

```bash
cd projects/analytics-au
uv sync --group dev
```

This creates a `.venv` and installs all dependencies including dev tools (webserver, dg CLI).

## Development Server

Start the Dagster dev server:

```bash
cd projects/analytics-au
uv run dg dev
```

The Dagster UI will be available at **http://127.0.0.1:3000**.

The dev server runs all daemons (scheduler, sensor, backfill, etc.) and watches for code changes.

## Common Commands

```bash
# List all definitions (assets, schedules, sensors)
uv run dg list defs

# Validate definitions
uv run dg check defs

# Scaffold a new asset
uv run dg scaffold defs dagster.asset assets/my_asset.py

# Launch specific assets
uv run dg launch --assets my_asset

# Launch with upstream dependencies
uv run dg launch --assets "+my_asset"
```

## Environment Variables

Set `DAGSTER_HOME` to persist run history and storage across sessions:

```bash
export DAGSTER_HOME=/path/to/dagster_home
```

Without this, the dev server uses a temporary directory that is cleaned up on exit.
