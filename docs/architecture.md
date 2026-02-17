# Architecture

## Overview

Project Zeus is a market research platform. The `analytics` project handles data orchestration using [Dagster](https://dagster.io/), following an analytics-as-code approach.

## Project Structure

```
project-zeus-market-research/
├── analytics/                  # Dagster data orchestration project
│   ├── src/analytics/
│   │   ├── definitions.py      # Entry point - auto-discovers definitions
│   │   └── defs/               # Asset, schedule, and sensor definitions
│   ├── tests/
│   ├── pyproject.toml
│   └── uv.lock
├── docs/                       # Project documentation
└── pyproject.toml              # Root project config
```

## Data Orchestration (Dagster)

The `analytics` project uses Dagster's modern `dg` CLI and project structure:

- **definitions.py** — Entry point that auto-discovers all definitions from the `defs/` folder using `load_from_defs_folder()`
- **defs/** — All assets, schedules, sensors, and components live here
- **Components** — Registered via `analytics.components.*` for reusable, YAML-configured building blocks

### Key Design Decisions

- **uv** for dependency management (fast, reproducible installs via `uv.lock`)
- **Hatchling** as the build backend
- **Dynamic definition loading** — definitions are auto-discovered, no manual registration needed
- **dg CLI** for scaffolding new definitions (assets, schedules, sensors) to maintain consistent patterns

## Embedded Analytics

Reports are treated as code artifacts using a declarative markdown-based approach. See [roadmap.md](roadmap.md) for the embedded analytics plan.

## Dependency Management

All Python dependencies are managed with `uv`. See [CLAUDE.md](../CLAUDE.md) for conventions.
