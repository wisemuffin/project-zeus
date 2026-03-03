# ADR-003: MetricFlow / dbt Semantic Layer Deferred

**Date:** 2026-03-03
**Status:** Deferred
**Decision:** Capture metric definitions in the data ontology glossary instead of MetricFlow; revisit when blockers are resolved

## Context

Project Zeus has ~25 computed metrics across 18 mart models (opportunity_gap, value_score, interest_momentum, etc.). The dbt semantic layer (MetricFlow) is the standard way to centrally define metrics in dbt projects, providing consistent definitions across BI tools and preventing metric drift.

We evaluated whether to adopt MetricFlow for Project Zeus.

## Why Not Now

### 1. Python version incompatibility

`dbt-metricflow` requires Python <3.13. Our project runs Python 3.13+ with dbt-core 1.11.6. Adopting MetricFlow would require downgrading to dbt-core 1.10.x and pinning Python to 3.12, which conflicts with other dependencies and our upgrade trajectory.

```
# As of March 2026:
dbt-metricflow ~= 0.7.x → requires dbt-core ~= 1.10.x, python < 3.13
Our stack: dbt-core 1.11.6, python 3.13
```

### 2. Evidence reports query DuckDB directly

Our Evidence.dev reports run SQL against DuckDB — they don't go through MetricFlow's query API. Adding MetricFlow wouldn't change how reports access data. We'd need to either rewrite Evidence queries to use the MetricFlow CLI as a proxy, or maintain both direct SQL and MetricFlow definitions (defeating the purpose).

### 3. Snapshot-grain data is a poor fit

MetricFlow is designed for time-grained fact tables where it adds significant value: time-spine joins, cumulative metrics, derived metrics across time windows. Most of our mart tables are snapshot-grain aggregates:

| Model | Rows | Grain |
|---|---|---|
| opportunity_gap | 10 | field_of_study |
| state_demand_index | 8 | state |
| field_value_proposition | 10 | field_of_study |
| institution_scorecard | ~42 | institution |
| historical_demand_trends | 5 | applicant_type |

These are pre-computed summary tables, not the raw time-series facts that MetricFlow's time-spine and cumulative features are built for. The overhead of defining semantic models, dimensions, and entities for tables with 5-42 rows would exceed the benefit.

## What We Do Instead

Metric definitions live in `docs/ontology/glossary.yml` — a YAML file with:
- Plain-language definition
- Exact formula (matching the SQL in mart models)
- Unit (decimal, percentage, AUD, category, etc.)
- Source models (which marts contain this metric)
- Domain (which business domain it belongs to)

This provides the same "single source of truth" benefit as MetricFlow for documentation purposes, without the runtime dependency.

## When to Revisit

Adopt MetricFlow when **all three** conditions are met:

1. `dbt-metricflow` supports Python 3.13+ and dbt-core 1.11+
2. Evidence.dev adds native MetricFlow/semantic layer integration (or we move to a BI tool that queries via MetricFlow)
3. The project adds time-series fact tables (e.g. monthly vacancy snapshots, weekly trend data) where MetricFlow's time-spine features add genuine value

The glossary.yml format was designed as a migration path — metric names, formulas, and model references can be translated to MetricFlow semantic model YAML when the time comes.

## Consequences

- Metric definitions are maintained manually in `docs/ontology/glossary.yml` and must be kept in sync with mart SQL
- No runtime metric validation — formula consistency is verified by code review, not by MetricFlow's query engine
- If a metric formula changes in SQL but not in the glossary, there's no automated warning (a validation script could address this later)
