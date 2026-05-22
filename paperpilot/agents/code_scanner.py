from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_json, write_text


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "data",
    "datasets",
    "outputs",
    "checkpoints",
    "logs",
}
DEPENDENCY_FILES = {"requirements.txt", "environment.yml", "setup.py", "pyproject.toml"}
ENTRYPOINT_FILES = {"main.py", "train.py", "run.py", "test.py"}
CONFIG_DIRS = {"configs", "config"}
SCRIPT_DIRS = {"scripts"}
EXAMPLE_DIRS = {"examples", "example"}
DATA_HINTS = ("data", "dataset", "loader", "dataloader", "input")
TRAINING_HINTS = ("train", "trainer", "fit", "model")
EVALUATION_HINTS = ("eval", "evaluate", "metric", "test", "score")


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _readme_head(path: Path, max_lines: int = 12) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    return "\n".join(line.strip() for line in lines[:max_lines] if line.strip())


def _looks_like_python_cli(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "argparse" in text or "click." in text or "typer." in text or "if __name__ == \"__main__\"" in text


def _matches_any(value: str, hints: tuple[str, ...]) -> bool:
    lowered = value.lower()
    return any(hint in lowered for hint in hints)


def _file_matches_any(path: Path, hints: tuple[str, ...]) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return False
    return any(hint in text for hint in hints)


def _iter_repo_files(repo_path: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_path.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def inspect_method_repo(repo_name: str, repo_path: str | Path) -> dict[str, Any]:
    root = Path(repo_path)
    warnings: list[str] = []
    if not root.exists() or not root.is_dir():
        return {
            "repo_name": repo_name,
            "repo_path": str(root),
            "detected_language": "unknown",
            "dependency_files": [],
            "candidate_entrypoints": [],
            "candidate_config_files": [],
            "candidate_data_files": [],
            "candidate_training_files": [],
            "candidate_evaluation_files": [],
            "readme_files": [],
            "readme_head": "",
            "integration_notes": ["Repository path could not be inspected."],
            "warnings": [f"Repository path does not exist locally: {root}"],
        }

    files = _iter_repo_files(root)
    readme_files = [path for path in files if path.name.lower().startswith("readme")]
    dependency_files = [path for path in files if path.name in DEPENDENCY_FILES]
    python_files = [path for path in files if path.suffix == ".py"]
    yaml_files = [path for path in files if path.suffix.lower() in {".yml", ".yaml"}]

    candidate_entrypoints = [
        path
        for path in python_files
        if path.name in ENTRYPOINT_FILES or path.parent.name in SCRIPT_DIRS or _looks_like_python_cli(path)
    ]
    candidate_config_files = [
        path
        for path in yaml_files
        if path.parent.name.lower() in CONFIG_DIRS or "config" in path.name.lower()
    ]
    candidate_config_files.extend(
        path for path in files if path.parent.name.lower() in CONFIG_DIRS and path not in candidate_config_files
    )
    candidate_data_files = [
        path
        for path in files
        if _matches_any(_relative(path, root), DATA_HINTS)
        or (path.suffix == ".py" and _file_matches_any(path, DATA_HINTS))
    ]
    candidate_training_files = [
        path
        for path in python_files
        if _matches_any(_relative(path, root), TRAINING_HINTS) or _file_matches_any(path, TRAINING_HINTS)
    ]
    candidate_evaluation_files = [
        path
        for path in python_files
        if _matches_any(_relative(path, root), EVALUATION_HINTS) or _file_matches_any(path, EVALUATION_HINTS)
    ]

    if not readme_files:
        warnings.append("No README file was found; human review may need to start from source files.")
    if not dependency_files:
        warnings.append("No dependency file was found; installation steps require manual review.")
    if not candidate_entrypoints:
        warnings.append("No obvious CLI entrypoint was found.")
    if not candidate_config_files:
        warnings.append("No obvious config file was found.")

    detected_language = "python" if python_files else "unknown"
    readme_head = _readme_head(readme_files[0]) if readme_files else ""
    integration_notes = [
        "Inspect this profile before writing an adapter; detected files are candidates, not guarantees.",
        "Confirm expected dataset format, target column, metric direction, and train/eval command behavior manually.",
    ]
    if candidate_entrypoints:
        integration_notes.append("Start review from candidate entrypoints and trace data loading plus result writing.")

    return {
        "repo_name": repo_name,
        "repo_path": str(root),
        "detected_language": detected_language,
        "dependency_files": [_relative(path, root) for path in dependency_files],
        "candidate_entrypoints": [_relative(path, root) for path in candidate_entrypoints],
        "candidate_config_files": [_relative(path, root) for path in sorted(set(candidate_config_files))],
        "candidate_data_files": [_relative(path, root) for path in candidate_data_files],
        "candidate_training_files": [_relative(path, root) for path in candidate_training_files],
        "candidate_evaluation_files": [_relative(path, root) for path in candidate_evaluation_files],
        "readme_files": [_relative(path, root) for path in readme_files],
        "readme_head": readme_head,
        "integration_notes": integration_notes,
        "warnings": warnings,
    }


def render_adapter_plan(profile: dict[str, Any]) -> str:
    entrypoints = profile["candidate_entrypoints"] or ["human-review-required"]
    dependencies = profile["dependency_files"] or ["human-review-required"]
    configs = profile["candidate_config_files"] or ["human-review-required"]
    data_files = profile["candidate_data_files"] or ["human-review-required"]
    warnings = profile["warnings"] or ["No scanner warnings; still verify behavior manually."]
    command_entry = entrypoints[0]

    lines = [
        f"# Adapter Plan: {profile['repo_name']}",
        "",
        "This plan is a human-in-the-loop inspection artifact. It suggests where to look first, but it does not prove that the method is runnable or scientifically comparable.",
        "",
        "## What The Repo Appears To Do",
        profile["readme_head"] or "No README summary was detected. Review source files manually.",
        "",
        "## How It Might Be Installed",
        *[f"- Review `{item}`" for item in dependencies],
        "",
        "## Likely Command Entrypoints",
        *[f"- `{item}`" for item in entrypoints],
        "",
        "## Expected Data Inputs",
        *[f"- Candidate data-related file or path: `{item}`" for item in data_files],
        "",
        "## Candidate Config Files",
        *[f"- `{item}`" for item in configs],
        "",
        "## Unknowns Requiring Human Review",
        *[f"- {item}" for item in warnings],
        "- Confirm dataset schema, split behavior, random seed handling, metrics, and output format.",
        "",
        "## Suggested Adapter Skeleton",
        "```python",
        "from paperpilot.baselines.adapters import BaseBaselineAdapter",
        "",
        f"class {profile['repo_name'].title().replace('_', '')}Adapter(BaseBaselineAdapter):",
        "    def fit(self, X, y):",
        "        # Prepare data and call the external method repo.",
        "        return self",
        "",
        "    def predict(self, X):",
        "        # Load method outputs or call inference code.",
        "        raise NotImplementedError",
        "```",
        "",
        "## Suggested Runner Command Template",
        "```bash",
        f"python {command_entry} --config <config_path> --data <dataset_path> --output <output_dir>",
        "```",
        "",
    ]
    return "\n".join(lines)


class CodeScannerAgent(BaseAgent):
    name = "code_scanner"
    description = "Detects repository entrypoints, dependency hints, and local method repo profiles."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        repo_path = Path(config["inputs"]["repository"])
        output_dir = Path(config.get("outputs", {}).get("dir", "outputs"))
        entrypoints: list[str] = []
        dependencies: list[str] = []
        risks: list[str] = []

        if repo_path.exists() and repo_path.is_dir():
            for candidate in ("pyproject.toml", "setup.py", "requirements.txt"):
                if (repo_path / candidate).exists():
                    dependencies.append(candidate)
            for pattern in ("*.py", "scripts/*.py"):
                entrypoints.extend(str(path) for path in repo_path.glob(pattern))
        else:
            risks.append(f"Repository path does not exist locally: {repo_path}")

        if not entrypoints:
            entrypoints = ["adapter-provided baseline entrypoint"]

        repo_profiles: list[dict[str, Any]] = []
        adapter_plan_paths: list[str] = []
        for item in config.get("method_repos", []):
            name = str(item.get("name", Path(item.get("path", "method_repo")).name))
            path = item.get("path")
            if not path:
                risks.append(f"Method repo '{name}' has no path.")
                continue
            profile = inspect_method_repo(name, path)
            profile_path = output_dir / "repo_profiles" / f"{name}.json"
            adapter_path = output_dir / "adapter_plans" / f"{name}_adapter_plan.md"
            write_json(profile_path, profile)
            write_text(adapter_path, render_adapter_plan(profile))
            profile["profile_path"] = str(profile_path)
            profile["adapter_plan_path"] = str(adapter_path)
            repo_profiles.append(profile)
            adapter_plan_paths.append(str(adapter_path))

        context["detected_entrypoints"] = entrypoints
        context["detected_dependencies"] = dependencies
        context["risk_notes"] = risks
        context["repo_profiles"] = repo_profiles
        context["adapter_plan_paths"] = adapter_plan_paths
        return context
