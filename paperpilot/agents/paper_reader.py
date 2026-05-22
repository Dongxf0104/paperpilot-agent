from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent


class PaperReaderAgent(BaseAgent):
    name = "paper_reader"
    description = "Extracts lightweight paper summary signals from config."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        paper = config["inputs"]["paper"]
        summary = paper.get("summary") if isinstance(paper, dict) else None
        paper_path = paper.get("path") if isinstance(paper, dict) else str(paper)

        if not summary and paper_path:
            path = Path(paper_path)
            summary = f"Configured paper source: {path.name or paper_path}"
        summary = summary or "No paper summary provided."

        text = summary.lower()
        keywords = [
            keyword
            for keyword in ("baseline", "benchmark", "regression", "representation", "spatial", "multi-omics")
            if keyword in text
        ]
        if not keywords:
            keywords = [config["task"]["type"]]

        context["paper_summary"] = summary
        context["method_keywords"] = keywords
        context["claimed_contributions"] = paper.get("claimed_contributions", []) if isinstance(paper, dict) else []
        return context
