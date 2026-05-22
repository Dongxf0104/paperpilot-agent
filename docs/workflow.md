# PaperPilot-Agent Workflow

PaperPilot-Agent turns a project configuration into a benchmark planning report. The current version is a local deterministic MVP: it plans and summarizes the workflow, but it does not yet fully parse arbitrary papers, generate adapters automatically, or execute external research repositories.

## Flow

Conceptual flow:

```text
Paper / Repo / Dataset / Metrics
        |
        v
PaperReaderAgent
        |
        v
CodeScannerAgent
        |
        v
BaselineBuilderAgent
        |
        v
ExperimentDesignerAgent
        |
        v
RunnerPlannerAgent
        |
        v
ResultAnalystAgent
        |
        v
ConsistencyCheckerAgent
        |
        v
ReportGeneratorAgent
        |
        v
Markdown Report
```

## Workflow Stages

| Stage | Input | Agent | Output | Review Question |
| --- | --- | --- | --- | --- |
| Paper understanding | Paper path, summary, claimed contributions | `PaperReaderAgent` | Paper summary and method keywords | What claim or method is this benchmark about? |
| Repository scan | Local repository path and optional `method_repos` | `CodeScannerAgent` | Entrypoints, dependency hints, repo profiles, adapter plans, risks | Is there enough repository structure to plan integration? |
| Baseline planning | Baseline list | `BaselineBuilderAgent` | Built-in or external adapter status | Which baselines are ready, and which need wrappers? |
| Experiment design | Dataset, target, task, metrics, split, seed | `ExperimentDesignerAgent` | Experiment plan | Are task, data, metrics, and baselines aligned? |
| Runner planning | Config path and experiment context | `RunnerPlannerAgent` | Command and execution steps | What should be run, and what output is expected? |
| Result analysis | Optional result rows | `ResultAnalystAgent` | Metric summary and interpretation | Are results real measurements or still pending? |
| Consistency checking | Full workflow context | `ConsistencyCheckerAgent` | Passes and warnings | Are there obvious mismatches before reporting? |
| Report generation | Full workflow context | `ReportGeneratorAgent` | Markdown report content | Can the plan be reviewed as a single artifact? |

## Minimal Demo Workflow

The `examples/toy_regression` demo uses a tiny local regression dataset and two built-in baselines. Its config lives at:

```text
examples/toy_regression/project.yaml
```

Key fields:

| Config Area | Demo Value |
| --- | --- |
| Paper source | `docs/legacy_experiments.md` |
| Repository | Current repository root, `.` |
| Dataset | `examples/toy_regression/sample_dataset.csv` |
| Target column | `y` |
| Task | `regression` |
| Split | `deterministic 80/20 holdout` |
| Metrics | `mae`, `mse`, `rmse`, `r2` |
| Baselines | `mean`, `linear_regression` |
| Method repo | `examples/external_method_repo` |
| Output directory | `outputs` |

Run from the repository root:

```bash
python -m paperpilot.cli run examples/toy_regression/project.yaml
```

Runtime output:

```text
outputs/report.md
```

Example output:

```text
examples/toy_regression/expected_report.md
```

When `method_repos` are configured, the workflow also writes:

```text
outputs/repo_profiles/example_method.json
outputs/adapter_plans/example_method_adapter_plan.md
```

The generated report should include the paper summary, method keywords, experiment plan, runner plan, pending result-analysis note, and consistency checks.

In the current implementation, baseline planning and experiment planning are both deterministic context-building steps derived from `project.yaml`. They are documented in the research workflow order above because external baseline adapters are usually considered before finalizing an experiment design.

## Planned Extensions

- Optional LLM-backed paper reading and code scanning.
- Deeper repository parsing for common research-code layouts.
- Adapter generation templates for external methods.
- Actual experiment runner backends.
- Structured result ingestion from CSV, JSON, or tracking tools.
- Stronger checks for dataset schema, metric direction, and paper-claim coverage.
