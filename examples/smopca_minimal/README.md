# SMOPCA Minimal Demo

This directory contains a tiny SMOPCA-inspired regression benchmark planning demo for PaperPilot-Agent.

Files:

- `project.yaml`: PaperPilot project configuration.
- `sample_dataset.csv`: Small local dataset with `x1`, `x2`, and target column `y`.

Run from the repository root:

```bash
python -m paperpilot.cli run examples/smopca_minimal/project.yaml
```

The workflow writes:

```text
outputs/report.md
```

This demo is intentionally minimal. It verifies the local planning and report-generation workflow; it does not claim to reproduce a full SMOPCA paper or execute an external method repository.
