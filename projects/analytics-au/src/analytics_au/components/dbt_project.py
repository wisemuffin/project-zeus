import json
from dataclasses import dataclass

import dagster as dg
from dagster_dbt.components.dbt_project.component import DbtProjectComponent


@dataclass
class AuditedDbtProjectComponent(DbtProjectComponent):
    """DbtProjectComponent that passes dagster_run_id to dbt as a var."""

    def get_cli_args(self, context: dg.AssetExecutionContext) -> list[str]:
        args = super().get_cli_args(context)
        args.extend(["--vars", json.dumps({"dagster_run_id": context.run_id})])
        return args
