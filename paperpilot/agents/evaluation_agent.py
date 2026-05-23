from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_text


class EvaluationAgent(BaseAgent):
    name = "evaluation_agent"
    description = "Generates a protocol for comparing methods with shared outputs and metrics."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        output_dir = Path(context["output_dir"])
        metric_names = context.get("metric_names", [])
        warnings = context.get("metrics_warnings", [])
        lines = [
            "# Evaluation Protocol",
            "",
            f"- Task type: {context['config'].get('task_type')}",
            f"- Configured metrics: {', '.join(metric_names) or 'none configured'}",
            "",
            "## Required Alignment",
            "- Use the same sample IDs across method outputs, labels, and optional metadata.",
            "- Record preprocessing, filtering, split, random seed, and hardware/runtime details.",
            "- Treat adapter-normalized outputs as the evaluation contract; preserve raw method outputs separately.",
            "",
            "## Required Files",
            "- predictions or cluster assignments with `sample_id`.",
            "- optional embedding/features with `sample_id`.",
            "- ground-truth labels or targets when required by metrics.",
            "- runtime metadata for each method.",
            "",
            "## Warnings",
            *[f"- {warning}" for warning in (warnings or ["No metric configuration warnings."])],
        ]
        output_path = write_text(output_dir / "evaluation_protocol.md", "\n".join(lines) + "\n")
        context["evaluation_protocol"] = {"output_path": str(output_path), "warnings": warnings}
        context.setdefault("agent_records", []).append(
            {
                "agent": "EvaluationAgent",
                "inputs": {"metrics": str(context.get("metrics_path"))},
                "outputs": {"evaluation_protocol": str(output_path)},
                "warnings": warnings,
            }
        )
        return context
