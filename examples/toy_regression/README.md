# Toy Regression Demo

This directory contains the minimal PaperPilot-Agent demo. It uses a tiny local regression dataset and two built-in baselines to verify the planning and report-generation workflow.

Files:

- `project.yaml`: PaperPilot project configuration.
- `sample_dataset.csv`: Small dataset with `x1`, `x2`, and target column `y`.
- `expected_report.md`: Example report output for this demo.

Run from the repository root:

```bash
python -m paperpilot.cli run examples/toy_regression/project.yaml
```

The workflow writes the runtime report to:

```text
outputs/report.md
```

This demo is intentionally small. It does not claim to reproduce a full paper or execute an external method repository.
