from __future__ import annotations

from pathlib import Path
from typing import Any

from paperpilot.agents.base import BaseAgent
from paperpilot.core.io import write_text


DEPENDENCY_FILES = {"requirements.txt", "environment.yml", "environment.yaml", "setup.py", "pyproject.toml"}
ENTRYPOINT_NAMES = {"main.py", "train.py", "run.py", "demo.py", "evaluate.py"}


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _files(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return sorted(path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts)


class RepoInspectorAgent(BaseAgent):
    name = "repo_inspector"
    description = "Inspects local method repositories for dependencies, entrypoints, examples, and warnings."

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        config = context["config"]
        output_dir = Path(context["output_dir"])
        case_root = Path(context["case_root"])
        methods = [config.get("methods", {}).get("main_method", {})]
        methods.extend(config.get("methods", {}).get("baselines", []))

        profiles: list[dict[str, Any]] = []
        lines = ["# Repository Inspection", ""]
        for method in methods:
            name = method.get("name", "unnamed_method")
            repo_path = case_root / method.get("repo_path", "")
            repo_files = _files(repo_path)
            readmes = [path for path in repo_files if path.name.lower().startswith("readme")]
            dependencies = [path for path in repo_files if path.name in DEPENDENCY_FILES]
            entrypoints = [
                path
                for path in repo_files
                if path.suffix.lower() in {".py", ".ipynb"}
                and (path.name in ENTRYPOINT_NAMES or "example" in path.as_posix().lower() or "tutorial" in path.as_posix().lower())
            ]
            warnings: list[str] = []
            if not repo_path.exists():
                warnings.append(f"Repository path does not exist: {repo_path}")
            elif not repo_files:
                warnings.append(f"Repository path is empty or has no inspectable files: {repo_path}")
            if not dependencies:
                warnings.append("No dependency file was detected.")
            if not entrypoints:
                warnings.append("No obvious runnable entrypoint or tutorial was detected.")

            profile = {
                "name": name,
                "repo_path": str(repo_path),
                "exists": repo_path.exists(),
                "readme_files": [_rel(path, repo_path) for path in readmes],
                "dependency_files": [_rel(path, repo_path) for path in dependencies],
                "candidate_entrypoints": [_rel(path, repo_path) for path in entrypoints],
                "warnings": warnings,
                "needs_human_confirmation": bool(warnings),
            }
            profiles.append(profile)
            lines.extend(
                [
                    f"## {name}",
                    f"- Path: `{repo_path}`",
                    f"- Exists: {profile['exists']}",
                    f"- README files: {', '.join(profile['readme_files']) or 'none detected'}",
                    f"- Dependency files: {', '.join(profile['dependency_files']) or 'none detected'}",
                    f"- Candidate entrypoints: {', '.join(profile['candidate_entrypoints']) or 'none detected'}",
                    f"- needs_human_confirmation: {profile['needs_human_confirmation']}",
                    "",
                    "### Warnings",
                    *[f"- {warning}" for warning in (warnings or ["No repository warnings."])],
                    "",
                ]
            )

        output_path = write_text(output_dir / "repo_inspection.md", "\n".join(lines))
        warnings = [warning for profile in profiles for warning in profile["warnings"]]
        context["repo_inspection"] = {"profiles": profiles, "warnings": warnings, "output_path": str(output_path)}
        context.setdefault("agent_records", []).append(
            {
                "agent": "RepoInspectorAgent",
                "inputs": {"methods": methods},
                "outputs": {"repo_inspection": str(output_path)},
                "warnings": warnings,
            }
        )
        return context
