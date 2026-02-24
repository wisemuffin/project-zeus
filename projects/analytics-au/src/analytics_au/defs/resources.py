import dagster as dg
from dagster_dlt import DagsterDltResource
from dagster_duckdb_pandas import DuckDBPandasIOManager


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "io_manager": DuckDBPandasIOManager(
                database="analytics.duckdb",
            ),
            "dlt": DagsterDltResource(),
        }
    )
