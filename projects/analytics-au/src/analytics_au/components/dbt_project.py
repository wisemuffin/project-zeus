import json
from dataclasses import dataclass

import dagster as dg
from dagster_dbt.compat import NodeStatus
from dagster_dbt.components.dbt_project.component import DbtProjectComponent
from dagster_dbt.core.dbt_cli_event import DbtFusionCliEventMessage

# Workaround for dagster-dbt 0.28.14 bug: Fusion tests return node_status="pass"
# but _get_check_passed() only checks for "success", marking all passing tests as
# failed asset checks. Fixed by also accepting "pass" status.
# Track: https://github.com/dagster-io/dagster/issues/XXXXX
_original_get_check_passed = DbtFusionCliEventMessage._get_check_passed


def _patched_get_check_passed(self) -> bool:
    return self._get_node_status() in (NodeStatus.Success, NodeStatus.Pass)


DbtFusionCliEventMessage._get_check_passed = _patched_get_check_passed


@dataclass
class AuditedDbtProjectComponent(DbtProjectComponent):
    """DbtProjectComponent that passes dagster_run_id to dbt as a var."""

    def get_cli_args(self, context: dg.AssetExecutionContext) -> list[str]:
        args = super().get_cli_args(context)
        args.extend(["--vars", json.dumps({"dagster_run_id": context.run_id})])
        return args
