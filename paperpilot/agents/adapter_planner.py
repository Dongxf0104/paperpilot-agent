from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_text


class AdapterPlannerAgent(BaseAgent):
    name = "adapter_planner"
    description = "Plans prepare/run/collect_outputs/evaluate adapter interfaces for each method."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        output_dir = Path(context["output_dir"])
        methods = context.get("baseline_plan", {}).get("plan", {}).get("methods", {})
        lines = ["# Adapter Plan", ""]
        warnings: list[str] = []
        for name, method in methods.items():
            method_warnings = method.get("risk_points", [])
            warnings.extend(method_warnings)
            lines.extend(
                [
                    f"## {name}",
                    "",
                    "### prepare",
                    "- Validate repository path, dependency files, input schema, seed, and output directory.",
                    "- Convert the configured dataset into the method-specific input format.",
                    "",
                    "### run",
                    "- Execute the confirmed entrypoint or notebook-derived command.",
                    "- Capture command, stdout/stderr, wall time, environment, and random seed.",
                    "",
                    "### collect_outputs",
                    "- Normalize raw artifacts into shared predictions/clusters, embedding/features, and runtime files.",
                    "- Preserve raw outputs under the method output directory for audit.",
                    "",
                    "### evaluate",
                    "- Compute configured metrics only after labels, predictions, and any task-specific inputs are aligned.",
                    "- Write metric values and warnings into `metrics.json`.",
                    "",
                    "Warnings:",
                    *[f"- {warning}" for warning in (method_warnings or ["No adapter warnings."])],
                    "",
                ]
            )
        output_path = write_text(output_dir / "adapter_plan.md", "\n".join(lines))
        context["adapter_plan"] = {"output_path": str(output_path), "warnings": warnings}
        context.setdefault("agent_records", []).append(
            {
                "agent": "AdapterPlannerAgent",
                "inputs": {"baseline_plan": str(context.get("baseline_plan", {}).get("output_path"))},
                "outputs": {"adapter_plan": str(output_path)},
                "warnings": warnings,
            }
        )
        return context
