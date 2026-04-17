# tricor

Generate disordered atomic supercells guided by three-body (g3) distributions, spanning the full spectrum from liquid to nanocrystalline. Designed for machine-learning training data generation.

## Overview

tricor builds periodic supercells with controllable disorder - from fully liquid to nanocrystalline - by combining Voronoi grain construction with spring-network relaxation. The resulting structures are characterized by their rooted three-body (g3) distributions, which capture both radial and angular correlations.

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
algorithms/index
visualization/index
examples/index
order_variety
api/index
```
