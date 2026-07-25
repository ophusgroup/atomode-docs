# Diamond (nanocrystalline)

Pure sp³ endpoint: every Voronoi grain is cut from the cubic diamond
reference (Fd-3m, *a* = 3.561 Å).  Randomly rotated tetrahedral
networks meet at grain boundaries, giving a nanocrystalline diamond
panel, the cleanest tetrahedral g3 signature on the regime ladder.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=14.0,
    grain_sources=[
        {"atoms": atoms_graphite, "species_offset": 0, "weight": 0.00},
        {"atoms": atoms_diamond,  "species_offset": 1, "weight": 1.00},
    ],
    bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0,
    hard_core_scale=0.92, nonbond_push_scale=0.85,
    displacement_sigma=0.02,
)
```

## Relaxation trajectory

Navy tetrahedra decorate every C atom whose four neighbours form a
109.5° tetrahedron; no triangles because no atoms were flagged as sp²
during grain construction.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/carbon_diamond_nc.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/carbon_diamond_nc.html
:width: 100%
:::
