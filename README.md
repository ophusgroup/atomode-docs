# tricor-docs

Documentation source and pre-rendered figures for [tricor](https://github.com/ophusgroup/tricor).

The hosted documentation is built by ReadTheDocs and available at:
**<https://tricor.readthedocs.io>**

## Repository structure

```
docs/
  index.md
  quickstart.md
  examples/            - static (generate-only) per-material case studies
  examples_mace/       - MACE-MP0 refinement examples (recommended)
  examples_refined/    - fast FIRE refinement (orientation + cleanup + FIRE)
  examples_dftb/       - DFTB+ refinement (temporarily hidden via conf.py)
  order_variety.md     - generate the full liquid → nanocrystalline ladder
  algorithms/          - mathematical description of each pipeline stage
  visualization/       - viewer + exporter reference
  api/                 - auto-generated API reference
  _static/             - pre-rendered interactive HTML viewers + figures
  conf.py
scripts/               - regeneration scripts (see scripts/README.md)
.readthedocs.yaml
pyproject.toml
```

## Why a separate repo?

The pre-rendered HTML figures for each case are ~1 MB each. Keeping them separate from the main `tricor` code repo prevents the main repo from accumulating history as figures are regenerated.

## Building locally

```bash
cd /path/to/tricor-docs
pip install -e .
pip install git+https://github.com/ophusgroup/tricor.git
sphinx-build -b html docs docs/_build
open docs/_build/index.html
```

## Regenerating figures

Interactive trajectory viewers and Plotly figures are generated locally (not during RTD build) and committed as HTML files in `docs/_static/`. See `docs/_static/README.md` for the regeneration workflow.
