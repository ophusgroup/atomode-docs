# Regen scripts

These scripts regenerate the static HTML / PNG artefacts under
`docs/_static/` that the Sphinx pages embed via `<iframe>`. Sphinx
itself does **not** run them — they're committed pre-built so the
docs build is fast and free of heavy compute dependencies.

## Layout

```
docs/_static/
  trajectories/           ← per-regime FIRE quench movies (static path)
  overview/               ← per-material 6-panel overview (static path)
  g3/                     ← per-regime g3 distribution viewers (static)
  g2_compare/             ← per-material stacked g(r) overlay (static)
  refined/
    trajectories/         ← per-regime refine + FIRE movies (refined path)
    overview/             ← per-material 2×3 static-vs-refined overview
    g3/                   ← per-regime g3 viewers ×3 (initial / after refine / after FIRE)
    g2_compare/           ← per-material g(r) overlay (3 regimes × {static, refined})
    cost_history/         ← per-regime cost-history PNGs
```

## How to run

All four scripts find `tricor` (the library) automatically:
1. preferred: `import tricor` (pip-installed in active env)
2. fallback: sibling repo at `../tricor/src/`

Run from anywhere:

```bash
# Full regen (static + refined, all materials)
python scripts/regen_static_full.py
python scripts/regen_static_overview.py
python scripts/regen_refined_full.py
python scripts/regen_refined_overview.py

# Single material/regime (static_full + refined_full only)
python scripts/regen_static_full.py --material silicon_dioxide --regime medium_range_order
python scripts/regen_refined_full.py --material carbon --regime sp3_nc
```

Wall-time on 2026 hardware (rng_seed=42, 40 Å cell):
- `regen_static_full.py` (5 mat × 6 regimes = 30 cells): **~25 min**
- `regen_static_overview.py` (5 mat × 6 regimes): **~15 min**
- `regen_refined_full.py` (5 mat × 3 regimes = 15 cells with refinement): **~30 min**
- `regen_refined_overview.py` (5 mat × 3 regimes × {static, refined}): **~25 min**

The refined runs take longer because of the SO(3) orientation-refinement
search (50 trials × 4 amplitudes × 2 rounds per grain) before the FIRE
quench.

## Why scripts live here, not in tricor itself

These are **demo scripts** that exercise the public API to produce the
docs artefacts. They are intentionally outside the library so:
- A user installing `tricor` from PyPI doesn't get demo-only paths.
- The docs repo can iterate on regen logic without bumping `tricor`.
- Tweaks to per-material parameters (grain ladders, hard-core scales,
  detector tolerances) live next to the docs they affect, not in the
  library.

## Cross-imports

`regen_static_overview.py`, `regen_refined_full.py`, and
`regen_refined_overview.py` all import the per-(material, regime)
catalogue from `regen_static_full.py` so the static and refined paths
share a single source of truth for parameters.

The cross-imports use `sys.path.insert(0, scripts/)` at the top of each
script — no `PYTHONPATH` setup required.

## Sphinx static-copy gotcha

After running these, Sphinx's incremental build sometimes does **not**
pick up the new `_static/` files into `_build/html/_static/`.
Workaround: `rsync -a docs/_static/ docs/_build/html/_static/` after
regen, or `rm -rf docs/_build && sphinx-build -b html docs docs/_build/html`
for a full rebuild.
