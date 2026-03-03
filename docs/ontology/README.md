# Project Zeus Data Ontology

This directory provides a single reference for understanding the entire data landscape of Project Zeus — what domains exist, how entities connect across domains, and what business terms mean.

## Why This Exists

The project has 7 data domains, 18 mart models, 20 staging models, and 20 source tables. Each is individually documented (dbt schema.yml descriptions, Dagster asset docstrings, insight docs). But there was no single place to understand:

- **What domains exist** and what question each answers
- **How data connects** across domains (shared entities, join keys)
- **What metrics mean** (formulas, units, which models contain them)

This ontology fills that gap.

## Files

| File | Purpose |
|---|---|
| [`entities.yml`](entities.yml) | 6 shared entities (field_of_study, institution, state, applicant_type, occupation_title, lga) with canonical sources, allowed values, and cross-model aliases |
| [`glossary.yml`](glossary.yml) | ~25 business metrics with plain-language definitions, exact formulas, units, and source models |
| [`domains.yml`](domains.yml) | 7 data domains with exhaustive model lists, source organisations, and links to insight docs and report pages |
| [`relationships.md`](relationships.md) | Mermaid ER diagram, cross-domain join paths, and documentation of critical crosswalks (QILT→UAC, ANZSCO→FOS, ASCED→UAC mappings) |

## How It Relates to Other Documentation

| Documentation | What It Covers | Ontology Adds |
|---|---|---|
| **dbt schema.yml** | Per-model descriptions, column definitions, tests | `meta:` tags linking each model to its domain, targeting dimension, and primary entity |
| **Dagster docstrings** | Per-asset what/use-case/limitations | Nothing — ontology doesn't duplicate asset docs |
| **Insight docs** (`docs/insights/`) | Analysis findings, marketing angles | `domains.yml` links insight docs to their parent domain |
| **Evidence reports** (`reports/au/pages/`) | Interactive dashboards | `domains.yml` links report pages to their parent domain |

## Maintenance Rules

When the data model changes, update the ontology to stay in sync:

1. **New mart model** → Add to the appropriate domain in `domains.yml`. Add any new metrics to `glossary.yml`.
2. **New staging model** → Add to the appropriate domain in `domains.yml`.
3. **New entity or join key** → Add to `entities.yml`. Update `relationships.md` if it creates a new cross-domain join path.
4. **New metric column** → Add to `glossary.yml` with definition, formula, unit, and source models.
5. **New domain** → Add to `domains.yml` with all required fields. Update the ER diagram in `relationships.md`.
6. **Renamed model/column** → Update references in all ontology files.

These rules are also captured in the project's `CLAUDE.md` to ensure they're followed during development.

## Querying the Ontology via dbt

Each mart model has a `meta:` block in `models/marts/schema.yml`:

```yaml
- name: opportunity_gap
  meta:
    domain: employment_and_opportunity_gap
    targeting_dimension: [what_message]
    primary_entity: field_of_study
    grain: field_of_study
```

This makes domain membership queryable:

```bash
# List all models in a domain
dbt ls --select "config.meta.domain:geography" --output json

# List all models targeting "where"
dbt ls --select "config.meta.targeting_dimension:where" --output json
```

## Design Decisions

- **YAML over database** — The ontology lives in version-controlled YAML files, not a database catalog. This keeps it lightweight, reviewable in PRs, and close to the code.
- **No MetricFlow** — `dbt-metricflow` requires Python <3.13 and would downgrade dbt-core. Most mart tables are snapshot-grain (not time-series facts), which is a poor fit for MetricFlow. Metric definitions in `glossary.yml` provide a migration path if MetricFlow becomes viable later.
- **Exhaustive model assignment** — Every staging and mart model belongs to exactly one domain. This prevents "orphan" models that aren't discoverable through the ontology.
