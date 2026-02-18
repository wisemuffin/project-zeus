import subprocess
from pathlib import Path

import dagster as dg

# Evidence source queries map 1:1 to these dbt mart models.
_MART_MODELS = [
    "audience_profile_by_fos",
    "graduate_outcomes_by_fos",
    "historical_demand_trends",
    "institution_scorecard",
    "opportunity_gap",
    "opportunity_gap_by_gender",
    "state_demand_index",
    "state_fos_demand",
    "trending_interests",
    "university_course_listings",
]

_REPORTS_DIR = Path(__file__).resolve().parents[5] / "reports"


@dg.asset(
    deps=_MART_MODELS,
    group_name="reports",
    tags={"domain": "reporting"},
    automation_condition=dg.AutomationCondition.any_deps_updated(),
)
def evidence_cache(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    """Refresh the Evidence source cache from DuckDB mart tables.

    Runs `npx evidence sources` in the reports/ directory, which re-extracts
    all source SQL queries into parquet files that Evidence serves to the
    browser. This asset depends on every dbt mart model so it automatically
    refreshes whenever upstream data changes.

    Use case: keeps the Evidence dashboard in sync with the analytics pipeline
    without manual intervention.
    """
    context.log.info(f"Running evidence sources in {_REPORTS_DIR}")

    result = subprocess.run(
        ["npx", "evidence", "sources"],
        cwd=_REPORTS_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )

    context.log.info(result.stdout)
    if result.stderr:
        context.log.warning(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"evidence sources failed (exit {result.returncode}):\n{result.stderr}"
        )

    # Count loaded sources from stdout (lines like "source_name ✔ Finished, wrote N rows.")
    loaded = [line for line in result.stdout.splitlines() if "Finished" in line]

    return dg.MaterializeResult(
        metadata={
            "sources_refreshed": dg.MetadataValue.int(len(loaded)),
            "output": dg.MetadataValue.md(f"```\n{result.stdout}\n```"),
        }
    )
