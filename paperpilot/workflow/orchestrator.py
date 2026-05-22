from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents import (
    BaselineBuilderAgent,
    CodeScannerAgent,
    ConsistencyCheckerAgent,
    ExperimentDesignerAgent,
    PaperReaderAgent,
    ReportGeneratorAgent,
    ResultAnalystAgent,
    RunnerPlannerAgent,
)
from paperpilot.core.config import load_project_config
from paperpilot.core.io import write_text


class PaperPilotWorkflow:
    def __init__(self) -> None:
        self.agents = [
            PaperReaderAgent(),
            CodeScannerAgent(),
            ExperimentDesignerAgent(),
            BaselineBuilderAgent(),
            RunnerPlannerAgent(),
            ResultAnalystAgent(),
            ConsistencyCheckerAgent(),
            ReportGeneratorAgent(),
        ]

    def run(self, project_config_path: str | Path) -> dict[str, Any]:
        config = load_project_config(project_config_path)
        context: dict[str, Any] = {"config": config}
        for agent in self.agents:
            context = agent.run(context)

        output_dir = Path(config.get("outputs", {}).get("dir", "outputs"))
        report_path = output_dir / "report.md"
        write_text(report_path, context["report_markdown"])
        context["outputs"] = {"report_path": str(report_path)}
        return context
