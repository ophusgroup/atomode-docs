# Amorphous

SrTiO₃ with 8 Å α-perovskite grains: each Voronoi cell is barely large
enough to host one or two randomly-oriented TiO₆ motifs. Only a handful
of full octahedra survive the boundaries; everywhere else is disordered
oxygen connectivity.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=300,
    grain_size=None,
    bond_weight=0.50,
    angle_weight=0.4,
    repulsion_weight=1.1,
    hard_core_scale=1.10,
    nonbond_push_scale=0.65,
    displacement_sigma=0.008,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/srtio3_amorphous.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/srtio3_amorphous.html
:width: 100%
:::
