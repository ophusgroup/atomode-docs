# Regen scripts

These scripts regenerate the pre-rendered artefacts under
`docs/_static/` (interactive HTML viewers, movies, figures) and the
generated Markdown pages that embed them. Sphinx itself does **not**
run them — the artefacts are committed pre-built so the docs build is
fast and free of heavy compute dependencies.

## Scripts by docs section

| docs section | regenerate artefacts | regenerate pages |
|---|---|---|
| Static Examples (`docs/examples/`) | `regen_static_full.py`, `regen_static_overview.py` | hand-written pages |
| MACE-MP0 Refinement (`docs/examples_mace/`) | `regen_mace_examples.py` | `build_mace_docs.py` |
| Fast FIRE Refinement (`docs/examples_refined/`) | `regen_fire_examples.py` | `build_fire_docs.py` |
| DFTB+ (hidden, `docs/examples_dftb/`) | `regen_dftb_examples.py` | hand-written pages |

`_wall_calculator.py` is a shared helper (soft minimum-distance wall
for MACE relaxations); `regen_fire_examples.py` and
`build_fire_docs.py` import the per-material registry from
`regen_mace_examples.py`, so the MACE and FIRE sections share a
single source of truth for material parameters. The cross-imports use
`sys.path.insert(0, scripts/)` — no `PYTHONPATH` setup required.

## Output layout

```
docs/_static/
  trajectories/    ← per-regime FIRE quench movies (Static Examples)
  overview/        ← per-material 6-panel overviews (Static Examples)
  g3/              ← per-regime g3 viewers (Static Examples)
  g2_compare/      ← per-material stacked g(r) overlays (Static Examples)
  mace/            ← MACE-MP0 section artefacts (movies, figures, JSON summaries)
  fire/            ← FIRE section artefacts (movies, figures, JSON summaries)
  dftb/            ← DFTB+ section artefacts (section hidden via conf.py)
```

## How to run

All scripts find `tricor` (the library) automatically: preferred is
`import tricor` from the active environment, with a fallback to the
sibling repo at `../tricor/src/`. The MACE and FIRE regen scripts
additionally need `mace-torch` (the FIRE pipeline falls back to
uncalibrated springs without it, but the MACE single-point scores in
the pages require it).

```bash
# Full regen of one section's artefacts, then its pages
python scripts/regen_mace_examples.py
python scripts/build_mace_docs.py

python scripts/regen_fire_examples.py
python scripts/build_fire_docs.py

# Single material / regime
python scripts/regen_fire_examples.py --material silicon_dioxide --regime sro
```

Expect hours for a full 5-material regen of either refinement section
on CPU (the MACE relaxations and single points dominate); the
`build_*.py` page generators only read the committed JSON summaries
and run in seconds.

## Why scripts live here, not in tricor itself

These are **demo scripts** that exercise the public API to produce the
docs artefacts. They are intentionally outside the library so:
- A user installing `tricor` from PyPI doesn't get demo-only paths.
- The docs repo can iterate on regen logic without bumping `tricor`.
- Per-material parameters (grain ladders, hard-core scales, weights)
  live next to the docs they affect, not in the library.

## Sphinx static-copy gotcha

After running these, Sphinx's incremental build sometimes does **not**
pick up the new `_static/` files into `_build/html/_static/`.
Workaround: `rsync -a docs/_static/ docs/_build/html/_static/` after
regen, or `rm -rf docs/_build && sphinx-build -b html docs docs/_build/html`
for a full rebuild.
