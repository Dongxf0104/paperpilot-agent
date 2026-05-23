from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_text


class ReportWriterAgent(BaseAgent):
    name = "report_writer"
    description = "Writes the final case report and includes agent trace metadata."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        output_dir = Path(context["output_dir"])
        warnings = [
            warning
            for record in context.get("agent_records", [])
            for warning in record.get("warnings", [])
        ]
        confirmation_lines = [f"- {warning}" for warning in sorted(set(warnings))] if warnings else [
            "- No warnings were recorded."
        ]
        lines = [
            f"# PaperPilot Report: {config.get('case_name', config.get('task_name', 'baseline_planning'))}",
            "",
            "## Overview",
            f"- Task name: {config.get('task_name')}",
            f"- Task type: {config.get('task_type')}",
            f"- Mode: {config.get('mode', 'dry_run')}",
            "",
            "## Generated Artifacts",
            "- `paper_summary.md`",
            "- `repo_inspection.md`",
            "- `dataset_check.md`",
            "- `baseline_plan.yaml`",
            "- `adapter_plan.md`",
            "- `evaluation_protocol.md`",
            "- `report.md`",
            "- `smoke_test.json`",
            "",
            "## Human Confirmation Needed",
            *confirmation_lines,
            "",
            "## Agent Trace",
        ]
        for record in context.get("agent_records", []):
            lines.extend(
                [
                    f"### {record['agent']}",
                    f"- Inputs: {record['inputs']}",
                    f"- Outputs: {record['outputs']}",
                    f"- Warnings: {record.get('warnings', [])}",
                    "",
                ]
            )
        output_path = write_text(output_dir / "report.md", "\n".join(lines) + "\n")
        context["report"] = {"output_path": str(output_path), "warnings": warnings}
        context.setdefault("agent_records", []).append(
            {
                "agent": "ReportWriterAgent",
                "inputs": {
                    "paper_summary": "paper_summary.md",
                    "repo_inspection": "repo_inspection.md",
                    "dataset_check": "dataset_check.md",
                    "baseline_plan": "baseline_plan.yaml",
                    "adapter_plan": "adapter_plan.md",
                    "evaluation_protocol": "evaluation_protocol.md",
                },
                "outputs": {"report": str(output_path)},
                "warnings": warnings,
            }
        )
        return context
