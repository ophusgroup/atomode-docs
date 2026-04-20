# Diamond (nanocrystalline)

Pure sp³ endpoint: every Voronoi grain is cut from the cubic diamond
reference (Fd-3m, *a* = 3.561 Å).  Randomly rotated tetrahedral
networks meet at grain boundaries, giving a nanocrystalline diamond
panel — the cleanest tetrahedral g3 signature on the regime ladder.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=120,
    grain_size=10.0,
    grain_sources=[
        {"atoms": atoms_graphite, "species_offset": 0, "weight": 0.0},
        {"atoms": atoms_diamond,  "species_offset": 1, "weight": 1.0},
    ],
    bond_weight=2.0, angle_weight=1.0, repulsion_weight=2.0,
    hard_core_scale=0.9, nonbond_push_scale=0.8,
    displacement_sigma=0.03,
)
```

## Relaxation trajectory

Navy tetrahedra decorate every C atom whose four neighbours form a
109.5° tetrahedron; no triangles because no atoms were flagged as sp²
during grain construction.

<iframe src="../../_static/trajectories/carbon_diamond_nc.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/carbon_diamond_nc.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
