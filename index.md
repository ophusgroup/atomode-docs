# atomode - atomic order-to-disorder engine

Generate atomistic supercells across the full order-to-disorder spectrum (amorphous, short- and medium-range order, nanocrystalline, and single crystal) at any size, by seeding Voronoi grains and refining them into physically realistic structures with a machine-learning potential (MACE-MP0) or a fast spring-network quench.

Silicon, liquid → nanocrystalline. See [Static Examples → Silicon](examples/silicon/index.md).

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/overview/silicon.html
:width: 100%
:::

## Overview

atomode builds periodic supercells across the order-to-disorder spectrum by seeding Voronoi grains and refining them into physically realistic structures, either with a fast spring-network (FIRE) quench or with the MACE-MP0 machine-learning potential for near-DFT accuracy. Grain size and density set the local order, from a single amorphous network up to large, well-aligned crystallites. Pair (g2) and rooted three-body (g3) distributions are provided to characterize the result.

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
