# Pre-rendered figures

This directory contains pre-rendered static HTML files for embedding in the docs.
Regenerate locally and commit - they are NOT built during the RTD build.

## Structure

```
_static/
  trajectories/   - Three.js interactive 3D relaxation viewers (one per case)
    si_liquid.html
    si_amorphous.html
    ...
  figures/        - Plotly g3 distributions and profile plots
    si_liquid_g3.html
    ...
```

## Regeneration workflow

See `scripts/render_figures.py` (TODO) in the repo root for the notebook/script
that produces these files.
