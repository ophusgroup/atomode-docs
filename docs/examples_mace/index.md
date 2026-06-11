# MACE-MP0 Refinement Examples

tricor-generated supercells refined with **[MACE-MP0](https://github.com/ACEsuit/mace)**, the universal machine-learning interatomic potential trained on the Materials Project DFT dataset.

The pipeline per (material, regime) is:

```
1. Voronoi tile          (cell.generate(num_steps=0))
2. Orientation refine    (cell.refine_initial_orientations)
3. Pre-MACE cleanup      (bond_relax + enforce_hard_core)
4. MACE+wall relax       (ASE LBFGS, or Langevin MD at
                          the melting point for liquid)
```

A per-pair soft wall (`scripts/_wall_calculator.py`) is added below each per-pair minimum distance to suppress MACE's near-overlap basins; it is silent above the minimum.

## Install

```bash
uv pip install torch "mace-torch>=0.3" matplotlib
```

The `medium-mpa-0` model (~76 MB) downloads automatically on first use. Each regime page links a standalone `.py` reproducer.

## Materials

```{toctree}
:maxdepth: 1

copper/index
silicon/index
carbon/index
silicon_dioxide/index
strontium_titanate/index
```