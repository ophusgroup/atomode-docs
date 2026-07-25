# Graphite (nanocrystalline)

Pure sp² endpoint: every Voronoi grain is cut from the hexagonal
graphite reference (P6₃/mmc, *a* = 2.467 Å, *c* = 6.708 Å).  Randomly-
rotated sheets meet at grain boundaries, producing a nanocrystalline
graphite panel where in-plane C-C bonds at 1.42 Å dominate but
interlayer 3.4 Å gaps are preserved through the repulsion term.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=14.0,
    grain_sources=[
        {"atoms": atoms_graphite, "species_offset": 0, "weight": 1.00},
        {"atoms": atoms_diamond,  "species_offset": 1, "weight": 0.00},
    ],
    bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0,
    hard_core_scale=0.92, nonbond_push_scale=0.85,
    displacement_sigma=0.02,
)
```

## Relaxation trajectory

Green triangles decorate every C atom whose three neighbours form a
clean 120° trigonal planar motif.

:::{iframe} https://ophusgroup.github.io/atomode-data/trajectories/carbon_graphite_nc.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-data/g3/carbon_graphite_nc.html
:width: 100%
:::
