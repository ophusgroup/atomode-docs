# atomode

Generate disordered atomic supercells guided by three-body (g3) distributions, spanning the full spectrum from liquid to nanocrystalline.

Silicon, liquid → nanocrystalline. See [Static Examples → Silicon](examples/silicon/index.md).

:::{iframe} https://ophusgroup.github.io/atomode-data/overview/silicon.html
:width: 100%
:::

## Overview

atomode builds periodic supercells with controllable disorder, from fully liquid to nanocrystalline, by combining Voronoi grain construction with spring-network relaxation. The resulting structures are characterized by their rooted three-body (g3) distributions, which capture both radial and angular correlations.

**Key features:**

- Rapidly generate structures from liquid to nanocrystalline with a single call
- Voronoi grain construction with per-species-pair bond topology
- Interactive g3 distribution widgets for Jupyter (Three.js + anywidget)
- Self-contained HTML exporters for trajectories, g3 heatmaps, and multi-cell overviews
- Rotating MP4 / GIF movie export for publication figures
- Works with any crystal structure (Si, SiC, oxides, metals, etc.)

## Refining generated structures

atomode generates the initial supercell; a separate relaxation step
turns it into a physically realistic structure. Two worked pipelines
are documented, in order of accuracy:

- **[MACE-MP0 refinement](examples_mace/index.md)** *(recommended)* —
  relax with a universal machine-learning potential. Near-DFT
  accuracy, minutes per ~5000-atom cell on a laptop CPU.
- **[Fast FIRE refinement](examples_refined/index.md)** — the built-in
  spring-network FIRE quench. Orders of magnitude faster than MACE at
  reduced accuracy, and the only option that stays practical at
  100³ Å and larger.
  Optionally calibrate the springs against MACE with one call
  (`shell.calibrate_to_mace()`) — Morse anharmonicity, per-pair
  stiffness, and the hard-core wall are measured from the MACE
  potential on the reference crystal, improving accuracy at zero
  extra relaxation cost.
