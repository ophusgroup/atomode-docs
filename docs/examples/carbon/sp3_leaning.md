# sp³-leaning mixed

40% graphite grains, 60% diamond grains.  Diamond-style tetrahedra
begin to dominate the centre of the cell while graphitic sheets
persist at the grain boundaries, close in character to the
industrially-relevant ta-C and DLC coatings.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=14.0,
    grain_sources=[
        {"atoms": atoms_graphite, "species_offset": 0, "weight": 0.40},
        {"atoms": atoms_diamond,  "species_offset": 1, "weight": 0.60},
    ],
    bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0,
    hard_core_scale=0.92, nonbond_push_scale=0.85,
    displacement_sigma=0.02,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/carbon_sp3_leaning.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/carbon_sp3_leaning.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
