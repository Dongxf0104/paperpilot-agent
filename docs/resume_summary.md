# Resume Summary

## 中文简历项目描述

PaperPilot-Agent 是一个面向科研 baseline / benchmark 工作流的本地 multi-agent 原型系统。项目通过八个确定性 agent，将论文摘要、方法仓库、数据集配置、评价指标和 baseline 选择组织成实验计划、baseline adapter 计划、runner 步骤、一致性检查和 Markdown 报告。当前版本强调本地可运行、可测试、可解释的 MVP 工作流，而不是宣称自动复现任意论文。

可用于简历的一句话版本：

> 构建 PaperPilot-Agent，本地 multi-agent 科研 benchmark 规划工具，将 paper/repo/dataset/metric/baseline 配置转换为实验计划、adapter plan、运行步骤、一致性检查和可提交的 Markdown 报告，并配套 CLI、测试、CI 和最小 demo。

## English Resume Description

PaperPilot-Agent is a local multi-agent prototype for research baseline and benchmark workflows. It orchestrates eight deterministic agents to transform paper metadata, repository paths, dataset settings, metrics, and baseline choices into experiment plans, baseline adapter plans, runner steps, consistency checks, and concise Markdown reports. The current version is an MVP focused on local planning, testability, and transparent workflow structure rather than fully automatic paper reproduction.

Resume-ready version:

> Built PaperPilot-Agent, a local multi-agent workflow for research benchmark planning that converts paper/repo/dataset/metric/baseline configuration into experiment plans, adapter plans, runner steps, consistency checks, and Markdown reports, with CLI support, tests, CI, and a minimal reproducible demo.

## Highlights For AI Agent / AI Application Roles

- Designed a multi-agent workflow with explicit agent responsibilities and shared context passing.
- Built a local CLI-first prototype that runs without hosted LLM dependencies.
- Modeled a realistic AI-for-research workflow around baseline planning, benchmark execution planning, report generation, and consistency checking.
- Added adapter-oriented architecture for future integration of external research baselines.
- Kept the system testable with deterministic behavior, smoke tests, and GitHub Actions CI.
- Documented MVP boundaries clearly, including planned LLM integration, richer repository parsing, and adapter generation.

## How To Explain This Project In Interviews

Start with the problem: research benchmarks are difficult because papers, repositories, datasets, metrics, and baseline choices are often disconnected.

Then explain the design: PaperPilot-Agent breaks the workflow into eight small agents. Each agent adds a specific layer of context, such as paper summary, repository hints, baseline adapter status, experiment design, runner steps, result analysis, consistency checks, and final report generation.

Be honest about scope: the current version is a local deterministic MVP. It does not automatically reproduce arbitrary papers or execute third-party repositories. Its value is in making the benchmark planning process explicit, inspectable, and easy to extend.

Close with future direction: the same architecture can support optional LLM paper parsing, deeper code scanning, adapter template generation, and structured experiment runners.

## Technical Keywords

- Python
- CLI tooling
- Multi-agent workflow
- Local AI workflow prototype
- Research benchmark planning
- Baseline adapter planning
- Experiment planning
- Benchmark execution planning
- Report generation
- Consistency checking
- YAML configuration
- Pytest
- GitHub Actions CI
- MVP system design
