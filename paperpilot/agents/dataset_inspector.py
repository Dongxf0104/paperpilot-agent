from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_text


class DatasetInspectorAgent(BaseAgent):
    name = "dataset_inspector"
    description = "Checks local dataset structure and likely label/coordinate/data files."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        output_dir = Path(context["output_dir"])
        case_root = Path(context["case_root"])
        dataset_config = config.get("dataset", {})
        dataset_path = case_root / dataset_config.get("path", "")
        files = sorted(path for path in dataset_path.rglob("*") if path.is_file()) if dataset_path.exists() else []
        data_files = [path for path in files if path.suffix.lower() in {".csv", ".tsv", ".h5", ".hdf5", ".mtx", ".npz", ".npy"}]
        label_files = [path for path in files if any(token in path.name.lower() for token in ("label", "annotation", "truth", "target"))]
        coordinate_files = [path for path in files if any(token in path.name.lower() for token in ("coord", "spatial", "position", "location"))]
        warnings: list[str] = []
        if not dataset_path.exists():
            warnings.append(f"Dataset path does not exist: {dataset_path}")
        elif not files:
            warnings.append(f"Dataset path is empty: {dataset_path}")
        if not data_files:
            warnings.append("No common data files were detected.")
        if not label_files:
            warnings.append("No explicit label/annotation file was detected.")
        if not coordinate_files:
            warnings.append("No explicit coordinate/spatial position file was detected.")

        summary = {
            "name": dataset_config.get("name", "unnamed_dataset"),
            "path": str(dataset_path),
            "exists": dataset_path.exists(),
            "file_count": len(files),
            "data_files": [path.relative_to(dataset_path).as_posix() for path in data_files] if dataset_path.exists() else [],
            "label_file_candidates": [path.relative_to(dataset_path).as_posix() for path in label_files] if dataset_path.exists() else [],
            "coordinate_file_candidates": [path.relative_to(dataset_path).as_posix() for path in coordinate_files] if dataset_path.exists() else [],
            "warnings": warnings,
            "needs_human_confirmation": bool(warnings),
        }
        lines = [
            "# Dataset Check",
            "",
            f"- Name: {summary['name']}",
            f"- Path: `{summary['path']}`",
            f"- Exists: {summary['exists']}",
            f"- File count: {summary['file_count']}",
            f"- Data files: {', '.join(summary['data_files']) or 'none detected'}",
            f"- Label candidates: {', '.join(summary['label_file_candidates']) or 'none detected'}",
            f"- Coordinate candidates: {', '.join(summary['coordinate_file_candidates']) or 'none detected'}",
            f"- needs_human_confirmation: {summary['needs_human_confirmation']}",
            "",
            "## Warnings",
            *[f"- {warning}" for warning in (warnings or ["No dataset warnings."])],
        ]
        output_path = write_text(output_dir / "dataset_check.md", "\n".join(lines) + "\n")
        context["dataset_check"] = {**summary, "output_path": str(output_path)}
        context.setdefault("agent_records", []).append(
            {
                "agent": "DatasetInspectorAgent",
                "inputs": {"dataset": dataset_config},
                "outputs": {"dataset_check": str(output_path)},
                "warnings": warnings,
            }
        )
        return context
