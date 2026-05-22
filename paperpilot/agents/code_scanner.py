from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent


class CodeScannerAgent(BaseAgent):
    name = "code_scanner"
    description = "Detects repository entrypoints and dependency hints."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        repo_path = Path(config["inputs"]["repository"])
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

        context["detected_entrypoints"] = entrypoints
        context["detected_dependencies"] = dependencies
        context["risk_notes"] = risks
        return context
