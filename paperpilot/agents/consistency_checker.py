from __future__ import annotations

from typing import Any

from paperpilot.agents.base import BaseAgent


class ConsistencyCheckerAgent(BaseAgent):
    name = "consistency_checker"
    description = "Checks alignment among claims, baselines, metrics, data, and runner plan."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        warnings: list[str] = []
        passed: list[str] = []

        config = context["config"]
        if config["task"]["type"] == "regression" and all(metric.lower() in {"mae", "mse", "rmse", "r2"} for metric in config["metrics"]):
            passed.append("Regression task uses regression-compatible metrics.")
        else:
            warnings.append("Task type and metric family may need manual review.")

        if context.get("baseline_adapter_plan"):
            passed.append("Baseline adapter plan exists.")
        else:
            warnings.append("No baseline adapter plan was generated.")

        if context.get("experiment_plan", {}).get("dataset"):
            passed.append("Dataset path is referenced by the experiment plan.")
        else:
            warnings.append("Experiment plan has no dataset path.")

        if context.get("commands"):
            passed.append("Runner command plan exists.")
        else:
            warnings.append("Runner command plan is missing.")

        if not context.get("claimed_contributions"):
            warnings.append("No explicit paper claims were provided; report will use the summary only.")

        context["warnings"] = warnings
        context["passed_checks"] = passed
        return context
