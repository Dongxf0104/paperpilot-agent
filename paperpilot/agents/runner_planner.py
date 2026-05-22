from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent


class RunnerPlannerAgent(BaseAgent):
    name = "runner_planner"
    description = "Creates runnable command and output expectations."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config_path = Path(context["config"]["_config_path"])
        command = f"paperpilot run {config_path.as_posix()}"
        context["commands"] = [command]
        context["execution_steps"] = [
            "Load and validate project configuration.",
            "Inspect paper and repository inputs.",
            "Create experiment and baseline adapter plans.",
            "Run or import benchmark results.",
            "Generate consistency-checked markdown report.",
        ]
        context["expected_outputs"] = ["outputs/report.md"]
        return context
