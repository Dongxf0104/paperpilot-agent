# PaperPilot-Agent

PaperPilot-Agent is a local MVP multi-agent workflow for turning research papers, method repositories, datasets, metrics, and baseline choices into benchmark plans, adapter notes, runner steps, consistency checks, and concise markdown reports.

It is currently a deterministic prototype: the open-source workflow runs locally from a `project.yaml` file and does not require an LLM API key.

## Why This Project Matters

Research baseline and benchmark work is often blocked by coordination rather than by a single model implementation:

- Papers describe claims and evaluation settings, but those details are not always packaged as runnable steps.
- Method repositories may have unclear entrypoints, dependencies, or assumptions.
- Datasets, targets, splits, metrics, and baseline choices need to be aligned before results are meaningful.
- External baselines usually need adapters before they can be compared fairly.
- Benchmark notes can drift from the actual configuration unless they are generated from a shared workflow context.

PaperPilot-Agent focuses on this coordination layer. It helps researchers make the planning surface explicit before investing time in full reproduction or large-scale experiment execution.

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

The workflow passes a shared context dictionary through lightweight agents. Each agent adds one layer of planning or validation, and the final report is written as markdown. In the current prototype, baseline planning and experiment planning are adjacent config-driven steps; neither executes external research code yet.

## Agent Roles

- `PaperReaderAgent`: reads configured paper metadata and extracts lightweight method keywords.
- `CodeScannerAgent`: scans a local repository path for dependency files, likely entrypoints, and repository risks.
- `BaselineBuilderAgent`: maps requested baselines to the built-in or external adapter path.
- `ExperimentDesignerAgent`: converts task, dataset, metrics, split, seed, and baselines into an experiment plan.
- `RunnerPlannerAgent`: produces expected execution steps, command suggestions, and output locations.
- `ResultAnalystAgent`: summarizes provided metric results or marks analysis as pending.
- `ConsistencyCheckerAgent`: checks whether task type, metrics, dataset, baselines, and runner plan are aligned.
- `ReportGeneratorAgent`: turns the accumulated context into a concise markdown report.

See [docs/agents.md](docs/agents.md) for detailed agent responsibilities.

## Features

- Local deterministic workflow with no required external services.
- YAML project configuration with validation.
- Built-in regression baseline examples: `mean` and `linear_regression`.
- Baseline adapter interface for wrapping external methods.
- Regression metric registry for `mae`, `mse`, `rmse`, and `r2`.
- CLI entrypoint for generating `outputs/report.md`.
- Smoke-testable minimal example under `examples/smopca_minimal`.
- Documentation designed around research benchmark planning rather than generic package usage.

## Repository Structure

```text
paperpilot/
  agents/        Rule-based workflow agents.
  baselines/     Baseline adapter interface and built-in baselines.
  core/          Config loading and file I/O helpers.
  metrics/       Metric implementations and registry.
  workflow/      Orchestrator that runs agents and writes reports.
docs/            Architecture, agent, and workflow documentation.
examples/
  smopca_minimal/  Minimal regression benchmark planning demo.
tests/           Unit and smoke tests.
outputs/         Generated report location for the demo workflow.
```

## Quickstart

```bash
git clone https://github.com/your-org/paperpilot-agent.git
cd paperpilot-agent
pip install -e ".[dev]"
python -m paperpilot.cli run examples/smopca_minimal/project.yaml
```

After installation, the console script is also available:

```bash
paperpilot run examples/smopca_minimal/project.yaml
```

Run tests with:

```bash
python -m pytest
```

## Example: `examples/smopca_minimal`

The minimal example is a small SMOPCA-inspired regression benchmark planning demo. It includes:

- `examples/smopca_minimal/project.yaml`: project configuration.
- `examples/smopca_minimal/sample_dataset.csv`: tiny local dataset with `x1`, `x2`, and target column `y`.
- `docs/legacy_experiments.md`: short paper-style motivation referenced by the config.
- Baselines: `mean` and `linear_regression`.
- Metrics: `mae`, `mse`, `rmse`, and `r2`.

Run it from the repository root:

```bash
python -m paperpilot.cli run examples/smopca_minimal/project.yaml
```

The workflow writes:

```text
outputs/report.md
```

## Expected Output Report

The generated report is intentionally concise. It currently includes:

- Paper summary.
- Method keywords.
- Experiment plan with task, dataset, metrics, and baselines.
- Runner plan steps.
- Result analysis status.
- Consistency check passes and warnings.

For the minimal demo, result analysis is marked as pending because the current workflow plans the benchmark and report; it does not yet execute full model training or import completed runner outputs automatically.

## Current Status

Implemented:

- Deterministic local agent workflow.
- CLI command for running a project config.
- YAML config loading and validation.
- Shared workflow context passed through eight agents.
- Built-in baseline adapter examples.
- Basic regression metrics.
- Minimal smoke-tested demo project.
- Markdown report generation.

Prototype boundaries:

- Repository scanning is shallow and rule-based.
- Baseline adapter generation is a plan, not automatic code synthesis.
- Result analysis uses provided config results or placeholders.
- The current runner plan describes steps but does not execute external research repositories.

## Roadmap

- Optional LLM integration for paper parsing, code understanding, and report drafting.
- Richer repository parsing for common Python research layouts.
- Adapter template generation for external baselines.
- Structured experiment runner backends.
- Import of completed result files from benchmark runs.
- More task families, including classification and clustering.
- JSON or HTML report export.
- Stronger consistency checks for dataset schema, metrics, and claims.

## Limitations

PaperPilot-Agent should be treated as an MVP workflow system, not a complete paper reproduction engine. It does not guarantee that a paper can be reproduced, that an external repository is runnable, or that baseline comparisons are scientifically valid without human review. The goal is to make benchmark planning more explicit, inspectable, and easier to iterate.

## Resume-Friendly Project Summary

PaperPilot-Agent is a local Python prototype for research baseline and benchmark planning. It orchestrates eight deterministic agents that turn paper metadata, repository paths, dataset settings, metrics, and baseline choices into an experiment plan, baseline adapter plan, runner steps, consistency checks, and a markdown report. The project includes a CLI, YAML config validation, built-in regression baseline examples, metric utilities, tests, and a minimal SMOPCA-inspired demo.
