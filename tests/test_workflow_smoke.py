from pathlib import Path

from paperpilot.workflow import PaperPilotWorkflow


def test_workflow_generates_report():
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "examples" / "smopca_minimal" / "project.yaml"

    context = PaperPilotWorkflow().run(config_path)
    report_path = repo_root / "outputs" / "report.md"

    assert report_path.exists()
    assert "PaperPilot Report: smopca_minimal" in report_path.read_text(encoding="utf-8")
    assert context["outputs"]["report_path"] == "outputs\\report.md" or context["outputs"]["report_path"] == "outputs/report.md"
