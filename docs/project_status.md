# Project Status

## Current Version

PaperPilot-Agent is an MVP / local workflow prototype for research baseline and benchmark planning.

The current release is deterministic and runs locally from a `project.yaml` file. It is meant to make benchmark planning explicit, not to fully reproduce arbitrary papers automatically.

## What Works Now

- CLI workflow: `python -m paperpilot.cli run examples/toy_regression/project.yaml`.
- YAML project config loading and validation.
- Eight-agent local workflow for paper summary, repository scanning, baseline planning, experiment planning, runner planning, result analysis, consistency checking, and report generation.
- Built-in baseline examples: `mean` and `linear_regression`.
- Regression metric utilities for `mae`, `mse`, `rmse`, and `r2`.
- Minimal toy regression demo with a tiny CSV dataset.
- Markdown report generation at `outputs/report.md`.
- Pytest smoke coverage for agents, config, baseline registry, and workflow output.
- GitHub Actions CI for tests and the minimal demo.

## What Is Intentionally Lightweight

- Agent behavior is rule-based and deterministic.
- Repository scanning checks simple local file patterns and dependency hints.
- Paper reading uses configured metadata rather than full PDF parsing.
- Baseline adapter planning reports integration status instead of generating full adapter code.
- Runner planning describes reproducible steps instead of executing external research repositories.
- Result analysis can summarize provided rows, but demo results are intentionally pending.

## What Is Not Supported Yet

- Full automatic paper reproduction.
- Automatic parsing of arbitrary PDFs.
- Deep static analysis of large external repositories.
- Automatic dependency installation for third-party methods.
- Automatic adapter synthesis for unknown baseline repositories.
- Full experiment execution backends.
- Dataset schema validation beyond config-level references.
- Result ingestion from experiment trackers or external result files.
- Hosted or local LLM provider integration.

## Roadmap

- Optional LLM-backed paper parsing and code understanding.
- Richer repository scanners for common Python research layouts.
- Adapter templates for wrapping external baselines.
- Structured runner backends for local experiments.
- CSV/JSON result ingestion.
- Stronger consistency checks for task type, metric family, dataset schema, and paper claims.
- Additional task families such as classification and clustering.
- Structured report export formats such as JSON or HTML.

## Why This Is Still Useful For Researchers

Many benchmark projects fail before model execution because assumptions are scattered across papers, repositories, datasets, metrics, and baseline choices. PaperPilot-Agent gives researchers a small local workflow that turns those pieces into one reviewable plan and report.

The MVP is useful as a planning scaffold: it records what is known, what is pending, which baselines need adapters, which commands should be run, and where consistency checks already pass or need review.
