# sp³-rich mixed

20% graphite grains, 80% diamond grains.  Diamond tetrahedra dominate
the structure; residual sp² atoms live at grain boundaries as small
2D patches embedded in a 3D tetrahedral network.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=14.0,
    grain_sources=[
        {"atoms": atoms_graphite, "species_offset": 0, "weight": 0.20},
        {"atoms": atoms_diamond,  "species_offset": 1, "weight": 0.80},
    ],
    bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0,
    hard_core_scale=0.92, nonbond_push_scale=0.85,
    displacement_sigma=0.02,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/carbon_sp3_rich.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/carbon_sp3_rich.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
