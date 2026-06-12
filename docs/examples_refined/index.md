# Fast FIRE Refinement

tricor-generated supercells relaxed with the built-in [FIRE spring network](../algorithms/fire_relaxation.md).  FIRE is orders of magnitude faster than [MACE-MP0 refinement](../examples_mace/index.md) at lower accuracy, and is the practical option for cells of 100³ Å and larger (see [cost and convergence](../algorithms/fire_relaxation.md#cost-and-convergence)).  Each final structure is scored with a MACE-MP0 single point, so the FIRE and MACE pipelines can be compared directly.

The pipeline per (material, regime) is:

```
1. Voronoi tile          (cell.generate(num_steps=0))
2. Orientation refine    (cell.refine_initial_orientations)
3. Cleanup               (bond_relax + enforce_hard_core)
4. FIRE relaxation       (cell.shell_relax), or
   thermostatted sampling (cell.thermal_relax) for liquid
```

Shell targets are **MACE-calibrated** when the optional `mace-torch` dependency is installed (`shell.calibrate_to_mace()`): per-pair bond stiffness, per-triplet angle stiffness, Morse anharmonicity, and the hard-core wall are measured from the MACE-MP0 potential on the reference crystal, which improves accuracy over the hand-tuned defaults.  Without `mace-torch` the pipeline runs identically on the registry weights.  Carbon's composite sp²/sp³ target runs uncalibrated.

## Materials

```{toctree}
:maxdepth: 1

copper/index
silicon/index
carbon/index
silicon_dioxide/index
strontium_titanate/index
```