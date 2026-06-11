# tricor

Generate disordered atomic supercells guided by three-body (g3) distributions, spanning the full spectrum from liquid to nanocrystalline.

Silicon, liquid → nanocrystalline. See [Static Examples → Silicon](examples/silicon/index.md).

<iframe src="_static/overview/silicon.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Overview

tricor builds periodic supercells with controllable disorder, from fully liquid to nanocrystalline, by combining Voronoi grain construction with spring-network relaxation. The resulting structures are characterized by their rooted three-body (g3) distributions, which capture both radial and angular correlations.

**Key features:**

- Rapidly generate structures from liquid to nanocrystalline with a single call
- Voronoi grain construction with per-species-pair bond topology
- Interactive g3 distribution widgets for Jupyter (Three.js + anywidget)
- Self-contained HTML exporters for trajectories, g3 heatmaps, and multi-cell overviews
- Rotating MP4 / GIF movie export for publication figures
- Works with any crystal structure (Si, SiC, oxides, metals, etc.)

```{toctree}
:maxdepth: 2

quickstart
examples/index
examples_refined/index
examples_dftb/index
examples_mace/index
order_variety
large_cells
algorithms/index
visualization/index
api/index
```
