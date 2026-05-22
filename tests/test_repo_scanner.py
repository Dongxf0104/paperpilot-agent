from pathlib import Path

from paperpilot.agents.code_scanner import CodeScannerAgent, inspect_method_repo
from paperpilot.core.config import load_project_config
from paperpilot.core.io import read_json


def test_inspect_method_repo_detects_fake_repo_files():
    profile = inspect_method_repo("example_method", "examples/external_method_repo")

    assert profile["repo_name"] == "example_method"
    assert profile["detected_language"] == "python"
    assert "README.md" in profile["readme_files"]
    assert "requirements.txt" in profile["dependency_files"]
    assert "train.py" in profile["candidate_entrypoints"]
    assert "configs/default.yaml" in profile["candidate_config_files"]
    assert "train.py" in profile["candidate_training_files"]
    assert "train.py" in profile["candidate_evaluation_files"]


def test_code_scanner_writes_repo_profile_and_adapter_plan():
    context = {"config": load_project_config("examples/toy_regression/project.yaml")}
    context = CodeScannerAgent().run(context)
    profile = context["repo_profiles"][0]

    profile_path = Path(profile["profile_path"])
    adapter_plan_path = Path(profile["adapter_plan_path"])

    assert profile_path.exists()
    assert adapter_plan_path.exists()
    assert read_json(profile_path)["repo_name"] == "example_method"
    plan = adapter_plan_path.read_text(encoding="utf-8")
    assert "Suggested Adapter Skeleton" in plan
    assert "Suggested Runner Command Template" in plan
