from __future__ import annotations

from typing import Any

from paperpilot.agents.base import BaseAgent


class ReportGeneratorAgent(BaseAgent):
    name = "report_generator"
    description = "Generates a markdown report from workflow context."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        method_repo_lines = [
            f"- {profile['repo_name']}: profile `{profile['profile_path']}`, adapter plan `{profile['adapter_plan_path']}`"
            for profile in context.get("repo_profiles", [])
        ]
        if not method_repo_lines:
            method_repo_lines = ["- No local method repositories configured."]
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
            "## Local Method Repositories",
            *method_repo_lines,
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
