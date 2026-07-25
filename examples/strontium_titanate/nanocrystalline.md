# Nanocrystalline

SrTiO₃ with 18 Å grains: 2 to 3 distinct perovskite grains fit in the
40 × 40 × 40 Å box, each rotated independently. The crystalline
interiors dominate the structure; only thin seams of disordered atoms
remain at the grain boundaries.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=400,
    grain_size=22.0,
    bond_weight=1.3,
    angle_weight=0.9,
    repulsion_weight=1.4,
    hard_core_scale=1.10,
    nonbond_push_scale=0.85,
    displacement_sigma=0.002,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-data/trajectories/srtio3_nanocrystalline.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-data/g3/srtio3_nanocrystalline.html
:width: 100%
:::
