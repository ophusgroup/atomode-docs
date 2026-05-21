# Algorithms

Mathematical details of tricor's structure-generation pipeline,
ordered to match the natural flow of a build: measure the reference
crystal, lay down a Voronoi-tiled initial cell, optionally walk grain
orientations into a better-aligned basin, FIRE-quench with the
spring network, and (optionally) synthesise a target g3 distribution
against which the supercell can be compared.

```{toctree}
:maxdepth: 2

g3_distribution
supercell_generation
orientation_refinement
static_relaxation
large_cell_shortcut
target_g3
glossary
```

| Stage | Page | What it covers |
|---|---|---|
| 1. Measure | [Three-body distribution](g3_distribution.md) | g3 + g2 histogram, reduced coordinates, `CoordinationShellTarget` extraction. |
| 2. Build | [Supercell generation](supercell_generation.md) | Voronoi grain construction: seeds → tessellation → master block tiling → cell filling → overlap removal → close-pair push → optional thermal jitter. |
| 3. Align grains | [Orientation refinement](orientation_refinement.md) | Per-grain SO(3) coordinate search that picks rotation perturbations minimising a topology-free pair-distance score against the local environment, before the FIRE quench runs. |
| 4. Refine springs | [Static relaxation](static_relaxation.md) | FIRE-style gradient descent on the bond + angle + repulsion (+ restraint) springs.  This is what `Supercell.generate()` calls internally. |
| 4'. Large-cell shortcut | [Large-cell shortcut](large_cell_shortcut.md) | cKDTree `bond_relax` + `enforce_hard_core` sweeps that replace most of FIRE at 100³ Å and larger.  O(N log N) per iteration. |
| 5. Compare | [Target g3 construction](target_g3.md) | Blur + blend a measured crystalline g3 toward the random limit to produce a comparison target. |
| Reference | [Glossary](glossary.md) | Disorder regimes, shell-target fields, force-term nomenclature. |
