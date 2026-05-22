from __future__ import annotations

from typing import Any

from paperpilot.agents.base import BaseAgent


class ExperimentDesignerAgent(BaseAgent):
    name = "experiment_designer"
    description = "Builds a deterministic benchmark design from config."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        plan = {
            "task_type": config["task"]["type"],
            "dataset": config["dataset"]["path"],
            "target": config["dataset"].get("target", "y"),
            "metrics": config["metrics"],
            "baselines": config["baselines"],
            "split": config["task"].get("split", "deterministic 80/20 holdout"),
            "seed": config["task"].get("seed", 0),
        }
        context["experiment_plan"] = plan
        return context
