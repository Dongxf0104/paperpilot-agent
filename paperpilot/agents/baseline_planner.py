from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent


class BaselinePlannerAgent(BaseAgent):
    name = "baseline_planner"
    description = "Builds a baseline experiment plan from paper, repo, dataset, and metric checks."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        import yaml

        config = context["config"]
        output_dir = Path(context["output_dir"])
        metrics = context.get("metrics_config", {}).get("metrics", [])
        metric_names = [item.get("name", str(item)) if isinstance(item, dict) else str(item) for item in metrics]
        methods = []
        main = config.get("methods", {}).get("main_method", {})
        if main:
            methods.append({**main, "role": "main_method"})
        methods.extend({**item, "role": "baseline"} for item in config.get("methods", {}).get("baselines", []))

        plan_methods = {}
        repo_profiles = {item["name"]: item for item in context.get("repo_inspection", {}).get("profiles", [])}
        for method in methods:
            name = method.get("name", "unnamed_method")
            profile = repo_profiles.get(name, {})
            plan_methods[name] = {
                "role": method.get("role"),
                "repo_path": method.get("repo_path"),
                "inputs": {
                    "dataset": config.get("dataset", {}),
                    "paper_summary": "paper_summary.md",
                    "metrics": metric_names,
                },
                "outputs": {
                    "clusters_or_predictions": f"{name}/predictions.csv",
                    "embedding_or_features": f"{name}/embedding.csv",
                    "runtime": f"{name}/runtime.json",
                },
                "run_steps": [
                    "prepare method-specific input files",
                    "install or activate method environment",
                    "run confirmed entrypoint",
                    "normalize outputs into the shared evaluation format",
                ],
                "risk_points": profile.get("warnings", ["Repository behavior requires human confirmation."]),
            }

        plan = {
            "case_name": config.get("case_name"),
            "task_name": config.get("task_name"),
            "task_type": config.get("task_type"),
            "dataset": config.get("dataset"),
            "metrics": metrics,
            "unified_output_format": {
                "predictions_csv": ["sample_id", "prediction_or_cluster"],
                "embedding_csv": ["sample_id", "dim_1", "dim_2", "..."],
                "metrics_json": ["method", "metric", "value", "warning"],
                "runtime_json": ["method", "wall_time_seconds", "command", "environment"],
            },
            "methods": plan_methods,
            "warnings": context.get("paper_summary", {}).get("warnings", [])
            + context.get("repo_inspection", {}).get("warnings", [])
            + context.get("dataset_check", {}).get("warnings", []),
        }
        output_path = output_dir / "baseline_plan.yaml"
        output_path.write_text(yaml.safe_dump(plan, sort_keys=False, allow_unicode=True), encoding="utf-8")
        context["baseline_plan"] = {"plan": plan, "output_path": str(output_path)}
        context.setdefault("agent_records", []).append(
            {
                "agent": "BaselinePlannerAgent",
                "inputs": {
                    "paper_summary": "paper_summary.md",
                    "repo_inspection": "repo_inspection.md",
                    "dataset_check": "dataset_check.md",
                    "metrics": str(context.get("metrics_path")),
                },
                "outputs": {"baseline_plan": str(output_path)},
                "warnings": plan["warnings"],
            }
        )
        return context
