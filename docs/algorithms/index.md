# Algorithms

Mathematical details of tricor's structure-generation pipeline,
ordered to match the natural flow of a build: measure the reference
crystal, lay down a Voronoi-tiled initial cell, optionally walk grain
orientations into a better-aligned basin, clean up grain-boundary
overlaps, relax (with the built-in FIRE spring network, or hand off
to the MACE-MP0 potential), and optionally synthesise a target g3
distribution against which the supercell can be compared.

```{toctree}
:maxdepth: 2

g3_distribution
supercell_generation
orientation_refinement
cleanup_sweeps
fire_relaxation
mace_mp0
fire_vs_mace
target_g3
glossary
```

| Stage | Page | What it covers |
|---|---|---|
| 1. Measure | [Three-body distribution](g3_distribution.md) | g3 + g2 histogram, reduced coordinates, `CoordinationShellTarget` extraction. |
| 2. Build | [Supercell generation](supercell_generation.md) | Voronoi grain construction: seeds → tessellation → master block tiling → cell filling → overlap removal → close-pair push → optional thermal jitter. |
| 3. Align grains | [Orientation refinement](orientation_refinement.md) | Per-grain SO(3) coordinate search that re-runs the full grain assembly per trial and keeps rotations that lower a global pair-distance cost, before the final relaxation (FIRE or MACE) runs. |
| 4. Cleanup | [Cleanup sweeps](cleanup_sweeps.md) | cKDTree `bond_relax` + `enforce_hard_core` sweeps that remove grain-boundary overlaps before the relaxer starts.  O(N log N) per iteration. |
| 5. Relax | [FIRE relaxation](fire_relaxation.md) | Bond + angle + repulsion (+ restraint) springs minimised with a simplified FIRE integrator.  This is what `Supercell.generate()` calls internally. |
| 5'. ML relax | [MACE-MP0 potential](mace_mp0.md) | The machine-learning Hamiltonian and the LBFGS / Langevin update strategies used by the MACE refinement examples. |
| — | [FIRE vs MACE-MP0](fire_vs_mace.md) | Term-by-term comparison of the two energy models, and the strategy for calibrating FIRE's spring weights against MACE from a single reference crystal. |
| 6. Compare | [Target g3 construction](target_g3.md) | Blur + blend a measured crystalline g3 toward the random limit to produce a comparison target. |
| Reference | [Glossary](glossary.md) | Disorder regimes, shell-target fields, force-term nomenclature. |
