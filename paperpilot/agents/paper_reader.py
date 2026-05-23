from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_text


def _extract_pdf_text(path: Path, max_pages: int = 3) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if not path.exists():
        return "", [f"Paper file does not exist: {path}"]
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        return "", ["pypdf is not installed; PDF text extraction was skipped."]
    try:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages[:max_pages])
        if len(reader.pages) > max_pages:
            warnings.append(f"Only the first {max_pages} PDF pages were sampled.")
        if not text.strip():
            warnings.append("PDF parser returned empty sampled text.")
        return text.strip(), warnings
    except Exception as exc:
        return "", [f"PDF parsing failed: {exc}"]


class PaperReaderAgent(BaseAgent):
    name = "paper_reader"
    description = "Extracts lightweight paper summary signals from config."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        if context.get("workflow_type") == "baseline_planning":
            return self._run_baseline_planning(context)

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

    def _run_baseline_planning(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        output_dir = Path(context["output_dir"])
        case_root = Path(context["case_root"])
        paper_paths = [case_root / item for item in config.get("papers", [])]
        warnings: list[str] = []
        summaries: list[dict[str, Any]] = []
        for path in paper_paths:
            text, parser_warnings = _extract_pdf_text(path)
            warnings.extend(parser_warnings)
            summaries.append(
                {
                    "path": str(path),
                    "exists": path.exists(),
                    "sampled_text_chars": len(text),
                    "summary": f"Configured paper source: {path.name}",
                    "needs_human_confirmation": bool(parser_warnings or not text),
                }
            )

        if not paper_paths:
            warnings.append("No papers were configured.")

        lines = ["# Paper Summary", ""]
        for item in summaries:
            lines.extend(
                [
                    f"## {Path(item['path']).name}",
                    f"- Path: `{item['path']}`",
                    f"- Exists: {item['exists']}",
                    f"- Summary: {item['summary']}",
                    f"- Sampled text chars: {item['sampled_text_chars']}",
                    f"- needs_human_confirmation: {item['needs_human_confirmation']}",
                    "",
                ]
            )
        lines.extend(["## Warnings", *[f"- {warning}" for warning in (warnings or ["No paper warnings."])]])
        output_path = write_text(output_dir / "paper_summary.md", "\n".join(lines) + "\n")
        context["paper_summary"] = {"papers": summaries, "warnings": warnings, "output_path": str(output_path)}
        context.setdefault("agent_records", []).append(
            {
                "agent": "PaperReaderAgent",
                "inputs": {"papers": [str(path) for path in paper_paths]},
                "outputs": {"paper_summary": str(output_path)},
                "warnings": warnings,
            }
        )
        return context
