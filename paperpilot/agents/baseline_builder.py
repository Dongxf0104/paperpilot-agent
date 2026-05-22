from __future__ import annotations

from typing import Any

from paperpilot.agents.base import BaseAgent


class BaselineBuilderAgent(BaseAgent):
    name = "baseline_builder"
    description = "Plans baseline adapter integration."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        baselines = context["config"]["baselines"]
        adapter_plan = []
        for baseline in baselines:
            name = baseline["name"] if isinstance(baseline, dict) else str(baseline)
            adapter_plan.append(
                {
                    "baseline": name,
                    "adapter_interface": "BaseBaselineAdapter.fit/predict/evaluate",
                    "status": "built-in" if name in {"mean", "linear_regression"} else "external-adapter-required",
                }
            )
        context["baseline_adapter_plan"] = adapter_plan
        return context
