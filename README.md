# PaperPilot-Agent

PaperPilot-Agent is a local, human-in-the-loop multi-agent workflow for research baseline and benchmark planning.

## What It Does

PaperPilot-Agent turns a `project.yaml` configuration into a structured benchmark planning report. It connects paper metadata, repository paths, dataset settings, metrics, and baseline choices through a sequence of small agents that produce:

- paper and method summary signals
- repository scan notes
- baseline adapter planning
- experiment design
- runner steps
- result-analysis status
- consistency checks
- a Markdown report

## Research Workflow Problems It Helps With

- Papers often describe benchmark claims without clean execution steps.
- Method repositories may have unclear dependencies or entrypoints.
- Dataset, target, metric, split, and baseline assumptions can drift from each other.
- External baselines usually need adapters before comparison.
- Reports are easier to review when they are generated from the same workflow context as the plan.

## Core Workflow

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
outputs/report.md
```

## Agent Roles

- `PaperReaderAgent`: extracts configured paper summary, keywords, and claimed contributions.
- `CodeScannerAgent`: scans the configured local repository path for dependency and entrypoint hints.
- `BaselineBuilderAgent`: records whether each baseline is built in or needs an external adapter.
- `ExperimentDesignerAgent`: builds the task, dataset, metric, split, seed, and baseline plan.
- `RunnerPlannerAgent`: proposes runner steps, command hints, and expected outputs.
- `ResultAnalystAgent`: summarizes provided results or marks results as pending.
- `ConsistencyCheckerAgent`: checks alignment across task, metrics, dataset, baselines, and runner plan.
- `ReportGeneratorAgent`: generates the final Markdown report.

More detail is available in [docs/agents.md](docs/agents.md) and [docs/workflow.md](docs/workflow.md).

## Quickstart

```bash
git clone https://github.com/your-org/paperpilot-agent.git
cd paperpilot-agent
pip install -e .
python -m pytest
python -m paperpilot.cli run examples/toy_regression/project.yaml
```

After installation, the console script is also available:

```bash
paperpilot run examples/toy_regression/project.yaml
```

## Example

The minimal demo lives in [examples/toy_regression](examples/toy_regression). It includes a tiny CSV dataset, a `project.yaml` config, and an expected report example.

Run it from the repository root:

```bash
python -m paperpilot.cli run examples/toy_regression/project.yaml
```

The workflow writes the runtime report to:

```text
outputs/report.md
```

An example report is kept at:

```text
examples/toy_regression/expected_report.md
```

## Current Scope

- It runs local workflows from `project.yaml`.
- It includes built-in baseline examples and Markdown report generation.
- It supports human review and consistency checks.
- It does not replace researcher judgment.
- External repository execution is a planned extension.

## Roadmap

- Optional LLM-backed paper and code understanding.
- Richer repository parsing for common research code layouts.
- Adapter templates for external baselines.
- Structured local experiment runners.
- Result ingestion from CSV or JSON files.
- Stronger checks for dataset schema, metric direction, and paper-claim coverage.
- Additional task families beyond regression.

## License

MIT. See [LICENSE](LICENSE).
