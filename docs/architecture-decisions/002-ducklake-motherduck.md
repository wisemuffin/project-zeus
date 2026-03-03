# ADR-002: DuckLake + MotherDuck for Cloud-Backed Warehouse

**Date:** 2026-03-03
**Status:** Proposed
**Decision:** Evaluate DuckLake + MotherDuck when the project needs multi-user access or multi-country deployment

## Context

Project Zeus currently uses a local DuckDB file (`analytics.duckdb`) as its warehouse. This works well for single-developer analytics — it's fast, zero-cost, and requires no infrastructure. However, as the project grows toward multi-country deployment (`analytics-uk/`, etc.) and potential multi-user collaboration, the local file approach has limitations:

- **No concurrent access** — a single DuckDB file can only have one writer at a time
- **No cloud backup** — the warehouse is a local file with no built-in replication or disaster recovery
- **No time travel** — accidental overwrites or bad materializations can't be rolled back without manual snapshots
- **No collaboration** — sharing results means sharing the file or re-materializing on each machine

DuckLake is a new open table format (MIT-licensed) that could address these limitations while preserving the DuckDB query engine the project already uses. Combined with MotherDuck (cloud-hosted DuckDB), it provides a scalable path forward.

## Options

### Option 1: Stay on Local DuckDB

Continue with the current `analytics.duckdb` file per country.

**Pros:**
- Simple — no infrastructure to manage
- Zero cost
- Sufficient for current single-developer, single-country scale
- No external dependencies

**Cons:**
- No concurrent access, cloud backup, or time travel
- Multi-country deployment means managing multiple local files
- Sharing results requires file transfer or re-materialization

### Option 2: Migrate to MotherDuck + DuckLake

Cloud-hosted DuckDB (MotherDuck) with DuckLake as the open table format for storage.

**Pros:**
- Cloud-backed storage with automatic backup and availability
- ACID transactions and time travel (query data as of any previous point)
- Collaborative access — multiple users can query the same warehouse
- Metadata stored in a SQL database (Postgres, MySQL, SQLite, or DuckDB) rather than thousands of files like Iceberg/Delta Lake — 10-100x faster metadata operations
- MIT-licensed, no vendor lock-in on the table format
- dbt integration via the existing `dbt-duckdb` adapter with `is_ducklake: true` profile config
- Scales naturally to multi-country deployment
- Reference implementation available: [motherduck-examples/dbt-ducklake](https://github.com/motherduckdb/motherduck-examples/tree/dbt-ducklake/dbt-ducklake)

**Cons:**
- SaaS dependency on MotherDuck (the DuckLake format itself is open)
- Pricing considerations at scale (MotherDuck bills on compute + storage)
- Requires changes to Dagster IO manager, dlt pipeline config, and Evidence.dev connection strings
- Additional complexity vs a local file

### Option 3: MotherDuck without DuckLake

Cloud-hosted DuckDB via MotherDuck, but without the DuckLake lakehouse layer.

**Pros:**
- Simpler migration — just change the connection string
- Cloud backup and collaborative access
- Lower complexity than full DuckLake setup

**Cons:**
- No time travel or ACID transaction guarantees across tables
- No open table format — data is in MotherDuck's proprietary storage
- Loses the key benefits that differentiate DuckLake from a plain cloud database

## Decision

**Evaluate when the project needs multi-user access or multi-country deployment.**

The current local DuckDB setup is sufficient for the project's current scale. When any of the following triggers occur, evaluate a migration to MotherDuck + DuckLake:

1. A second country (`analytics-uk/`) is added and needs a shared warehouse
2. Multiple users need concurrent read/write access
3. The project moves toward production deployment where backup and availability matter

The reference architecture at [motherduck-examples/dbt-ducklake](https://github.com/motherduckdb/motherduck-examples/tree/dbt-ducklake/dbt-ducklake) provides a proven dbt + DuckLake integration pattern to follow.

## Key DuckLake Details

- **Metadata catalog:** Uses a SQL database (Postgres, MySQL, SQLite, or DuckDB) as the metadata catalog — not file-based metadata like Iceberg or Delta Lake
- **Performance:** 10-100x faster metadata operations than file-based catalogs
- **Transactions:** Full ACID transaction support across tables
- **Time travel:** Query data as of any previous point in time
- **Open format:** MIT-licensed, supports multiple storage backends
- **dbt integration:** Works with the existing `dbt-duckdb` adapter — add `is_ducklake: true` to the profile config

## Consequences

If/when this migration proceeds, the following components would need updates:

- **Dagster IO manager** — `DuckDBPandasIOManager` connection would change from a local file path to a MotherDuck connection string with DuckLake catalog
- **dlt pipelines** — `dlt` assets currently write directly to the local `analytics.duckdb` file; pipeline destinations would need reconfiguring
- **Evidence.dev** — report connection strings would change from local DuckDB to MotherDuck
- **dbt profiles** — add `is_ducklake: true` and update the connection target
- **CI/CD** — materialization in CI would need MotherDuck credentials and network access
