# PaperPilot-Agent

PaperPilot-Agent is a local multi-agent workflow for research baseline and benchmark work. It helps researchers turn papers, method repositories, datasets, metrics, and baseline choices into executable experiment plans, adapter plans, runner steps, result analysis, and concise reports.

The current open-source version is deterministic and rule-based by default. It does not require an LLM API key, so it can run locally in a fresh checkout and pass tests without external services.

## Why This Exists

Reproducing research baselines is often less about one model and more about coordination:

- papers describe claims, but not always executable steps
- method repositories vary in structure and entrypoints
- datasets and metrics must match the task
- third-party baselines need adapters before they can be compared fairly
- benchmark results need a repeatable summary and consistency checks

PaperPilot-Agent provides a small, inspectable workflow for that coordination layer.

## Agent Workflow

```text
project.yaml
   |
   v
PaperReader -> CodeScanner -> ExperimentDesigner -> BaselineBuilder
   |              |                 |                    |
   v              v                 v                    v
RunnerPlanner -> ResultAnalyst -> ConsistencyChecker -> ReportGenerator
   |
   v
outputs/report.md
```

## Agent Roles

- `PaperReaderAgent`: summarizes paper inputs and extracts method keywords.
- `CodeScannerAgent`: inspects the configured repository path and reports likely entrypoints, dependencies, and risks.
- `ExperimentDesignerAgent`: creates a task-aware experiment plan from dataset, metrics, and baselines.
- `BaselineBuilderAgent`: converts baseline config into adapter integration notes.
- `RunnerPlannerAgent`: proposes commands, execution steps, and expected outputs.
- `ResultAnalystAgent`: summarizes provided or simulated metric results.
- `ConsistencyCheckerAgent`: checks that claims, metrics, baselines, dataset, and runner plan line up.
- `ReportGeneratorAgent`: writes a markdown report from the full workflow context.

## Why LLM APIs Are Optional

PaperPilot-Agent is designed to fit local research workflows. Some users will run it from Cursor, Windsurf, VS Code, or another IDE agent. Others may later connect hosted or local LLM providers. This project keeps the core workflow deterministic first, with clear interfaces where richer LLM-backed behavior can be added later.

## Install

```bash
git clone https://github.com/your-org/paperpilot-agent.git
cd paperpilot-agent
pip install -e ".[dev]"
```

## Run The Demo

```bash
python -m paperpilot.cli run examples/smopca_minimal/project.yaml
```

Or, after installation:

```bash
paperpilot run examples/smopca_minimal/project.yaml
```

The demo writes:

```text
outputs/report.md
```

## Run Tests

```bash
python -m pytest -q
```

## Add Your Own Baseline

Implement the adapter interface:

```python
from paperpilot.baselines.adapters import BaseBaselineAdapter

class MyMethodBaseline(BaseBaselineAdapter):
    def fit(self, X, y):
        ...

    def predict(self, X):
        ...
```

Then register it:

```python
from paperpilot.baselines.registry import register_baseline

register_baseline("my_method", MyMethodBaseline)
```

Third-party paper methods can be wrapped this way without mixing their source code into the core package.

## Current Status

Implemented:

- deterministic local agent workflow
- YAML project config loading and validation
- baseline adapter interface
- `MeanBaseline`
- `LinearRegressionBaseline`
- regression metrics: MAE, MSE, RMSE, R2
- CLI entrypoint
- smoke-testable demo project

Planned:

- richer repository scanners
- optional LLM provider adapters
- classification and clustering metrics
- experiment execution backends
- structured report export
- adapter templates for common research code layouts
