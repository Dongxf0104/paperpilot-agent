from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from paperpilot.agents.adapter_planner import AdapterPlannerAgent
from paperpilot.agents.baseline_planner import BaselinePlannerAgent
from paperpilot.agents.dataset_inspector import DatasetInspectorAgent
from paperpilot.agents.evaluation_agent import EvaluationAgent
from paperpilot.agents.paper_reader import PaperReaderAgent
from paperpilot.agents.repo_inspector import RepoInspectorAgent
from paperpilot.agents.report_writer import ReportWriterAgent
from paperpilot.core.io import ensure_dir, write_text


class BaselinePlanningWorkflow:
    def __init__(self, repo_root: str | Path | None = None) -> None:
        self.repo_root = Path(repo_root or Path.cwd())
        self.agents = [
            PaperReaderAgent(),
            RepoInspectorAgent(),
            DatasetInspectorAgent(),
            BaselinePlannerAgent(),
            AdapterPlannerAgent(),
            EvaluationAgent(),
            ReportWriterAgent(),
        ]

    def init_case(self, case_name: str) -> Path:
        case_dir = self.repo_root / "cases" / case_name
        case_dir.mkdir(parents=True, exist_ok=True)
        template_path = self.repo_root / "paperpilot" / "templates" / "case_config.template.yaml"
        if template_path.exists():
            text = template_path.read_text(encoding="utf-8").replace("{{ case_name }}", case_name)
        else:
            text = _default_case_template(case_name)
        target = case_dir / "case_config.yaml"
        target.write_text(text, encoding="utf-8")
        return target

    def run(self, case_config_path: str | Path) -> dict[str, Any]:
        import yaml

        config_path = self._resolve_case_config(Path(case_config_path))
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError(f"Case config must be a mapping: {config_path}")
        output_dir = self.repo_root / config.get("output_dir", f"outputs/{config_path.parent.name}")
        ensure_dir(output_dir)
        normalized_metrics = _normalize_metrics_config(config, self.repo_root)
        context: dict[str, Any] = {
            "workflow_type": "baseline_planning",
            "case_root": str(self.repo_root),
            "case_config_path": str(config_path),
            "config": config,
            "output_dir": str(output_dir),
            "metrics_path": normalized_metrics["metrics_path"] or "",
            "metrics_config": normalized_metrics["metrics_config"],
            "metric_names": normalized_metrics["metric_names"],
            "metrics_warnings": normalized_metrics["warnings"],
            "agent_records": [],
        }
        for agent in self.agents:
            context = agent.run(context)
        smoke = self._write_smoke_test(context)
        context["smoke_test"] = smoke
        context["report_path"] = context.get("report", {}).get("output_path", str(output_dir / "report.md"))
        return context

    def _resolve_case_config(self, path: Path) -> Path:
        candidates = [path, self.repo_root / path]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        raise FileNotFoundError(path)

    def _write_smoke_test(self, context: dict[str, Any]) -> dict[str, Any]:
        output_dir = Path(context["output_dir"])
        expected_files = [
            "paper_summary.md",
            "repo_inspection.md",
            "dataset_check.md",
            "baseline_plan.yaml",
            "adapter_plan.md",
            "evaluation_protocol.md",
            "report.md",
        ]
        checks = [
            {"name": "case_config_readable", "ok": Path(context["case_config_path"]).exists()},
            {"name": "output_dir_exists", "ok": output_dir.exists()},
            *[
                {"name": f"output_exists:{name}", "ok": (output_dir / name).exists()}
                for name in expected_files
            ],
        ]
        smoke = {
            "passed": all(item["ok"] for item in checks),
            "checks": checks,
            "agent_records": context.get("agent_records", []),
        }
        write_text(output_dir / "smoke_test.json", json.dumps(smoke, indent=2, ensure_ascii=False))
        return smoke

    def reset_output_dir_for_test(self, output_dir: str | Path) -> None:
        target = self.repo_root / output_dir
        root = self.repo_root.resolve()
        resolved = target.resolve()
        if root not in resolved.parents and resolved != root:
            raise ValueError(f"Refusing to delete outside repository: {resolved}")
        if resolved.exists():
            shutil.rmtree(resolved)


def _normalize_metrics_config(config: dict[str, Any], repo_root: str | Path | None = None) -> dict[str, Any]:
    repo_root = Path(repo_root or Path.cwd())
    raw_metrics = config.get("metrics")
    warnings: list[str] = []
    metrics_path = ""
    metrics_config: dict[str, Any] = {"metrics": []}

    if isinstance(raw_metrics, dict):
        configured_path = raw_metrics.get("path", "")
        if configured_path:
            metrics_path = str(repo_root / configured_path)
            loaded_config, load_warnings = _load_metrics_file(Path(metrics_path))
            metrics_config = loaded_config
            warnings.extend(load_warnings)
        else:
            warnings.append("Metrics config is a mapping but has no `path` field.")
            inline_metrics = raw_metrics.get("metrics", [])
            metrics_config = {"metrics": inline_metrics if isinstance(inline_metrics, list) else []}
    elif isinstance(raw_metrics, list):
        metrics_config = {"metrics": raw_metrics}
    elif raw_metrics is None:
        warnings.append("No metrics were configured.")
    else:
        warnings.append(f"Unsupported metrics config type: {type(raw_metrics).__name__}")

    metric_names = _metric_names(metrics_config.get("metrics", []))
    return {
        "metrics_path": metrics_path,
        "metrics_config": metrics_config,
        "metric_names": metric_names,
        "warnings": warnings,
    }


def _load_metrics_file(path: Path) -> tuple[dict[str, Any], list[str]]:
    import yaml

    if not path.exists():
        return {"metrics": []}, [f"Metrics file does not exist: {path}"]
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"metrics": []}, [f"Metrics file must be a mapping: {path}"]
    if "metrics" not in data:
        return {**data, "metrics": []}, [f"Metrics file has no `metrics` field: {path}"]
    return data, []


def _metric_names(metrics: Any) -> list[str]:
    if not isinstance(metrics, list):
        return []
    return [item.get("name", str(item)) if isinstance(item, dict) else str(item) for item in metrics]


def _default_case_template(case_name: str) -> str:
    return f"""case_name: {case_name}
task_name: baseline_planning
task_type: "please specify task type, e.g. spatial multi-omics integration / image classification / time-series forecasting"

papers:
  - inputs/papers/your_paper.pdf

methods:
  main_method:
    name: YourMethod
    repo_path: inputs/repos/YourMethod
  baselines:
    - name: BaselineA
      repo_path: inputs/repos/BaselineA

dataset:
  name: your_dataset_name
  path: inputs/datasets/your_dataset

metrics:
  path: inputs/metrics/your_metrics.yaml

output_dir: outputs/{case_name}
mode: dry_run
"""
