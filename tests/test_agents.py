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


def test_agents_run_without_error():
    context = {"config": load_project_config("examples/smopca_minimal/project.yaml")}
    agents = [
        PaperReaderAgent(),
        CodeScannerAgent(),
        ExperimentDesignerAgent(),
        BaselineBuilderAgent(),
        RunnerPlannerAgent(),
        ResultAnalystAgent(),
        ConsistencyCheckerAgent(),
        ReportGeneratorAgent(),
    ]

    for agent in agents:
        context = agent.run(context)

    assert context["paper_summary"]
    assert context["experiment_plan"]["task_type"] == "regression"
    assert "# PaperPilot Report" in context["report_markdown"]
