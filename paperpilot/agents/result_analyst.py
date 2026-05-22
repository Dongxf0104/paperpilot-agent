from __future__ import annotations

from typing import Any

from paperpilot.agents.base import BaseAgent


class ResultAnalystAgent(BaseAgent):
    name = "result_analyst"
    description = "Summarizes provided or simulated metric results."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        results = config.get("results", [])
        metric = config["metrics"][0]

        if not results:
            results = [
                {"method": baseline["name"] if isinstance(baseline, dict) else str(baseline), metric: None}
                for baseline in config["baselines"]
            ]

        numeric = [row for row in results if isinstance(row.get(metric), (int, float))]
        lower_is_better = metric.lower() in {"mae", "mse", "rmse", "loss"}
        if numeric:
            best = min(numeric, key=lambda row: row[metric]) if lower_is_better else max(numeric, key=lambda row: row[metric])
            best_method = best["method"]
        else:
            best_method = "pending-results"

        context["best_method"] = best_method
        context["metric_summary"] = {"primary_metric": metric, "results": results}
        context["interpretation"] = (
            "Results are placeholders until runner outputs are attached."
            if best_method == "pending-results"
            else f"Best method by {metric}: {best_method}."
        )
        return context
