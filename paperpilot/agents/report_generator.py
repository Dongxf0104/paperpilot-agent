from __future__ import annotations

from typing import Any

from paperpilot.agents.base import BaseAgent


class ReportGeneratorAgent(BaseAgent):
    name = "report_generator"
    description = "Generates a markdown report from workflow context."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        lines = [
            f"# PaperPilot Report: {config['project']['name']}",
            "",
            "## Paper Summary",
            context.get("paper_summary", ""),
            "",
            "## Method Keywords",
            ", ".join(context.get("method_keywords", [])),
            "",
            "## Experiment Plan",
            f"- Task: {context['experiment_plan']['task_type']}",
            f"- Dataset: {context['experiment_plan']['dataset']}",
            f"- Metrics: {', '.join(context['experiment_plan']['metrics'])}",
            f"- Baselines: {', '.join(item['name'] if isinstance(item, dict) else str(item) for item in config['baselines'])}",
            "",
            "## Runner Plan",
            *[f"- {step}" for step in context.get("execution_steps", [])],
            "",
            "## Result Analysis",
            context.get("interpretation", ""),
            "",
            "## Consistency Checks",
            *[f"- PASS: {check}" for check in context.get("passed_checks", [])],
            *[f"- WARN: {warning}" for warning in context.get("warnings", [])],
            "",
        ]
        context["report_markdown"] = "\n".join(lines)
        return context
