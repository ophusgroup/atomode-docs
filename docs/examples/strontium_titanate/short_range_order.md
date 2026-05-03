# Short-range order

SrTiO₃ with 10 Å grains: each grain interior now holds a handful of
intact TiO₆ octahedra that share O corners in the perovskite manner,
but the phase-mismatched grain boundaries still dominate the structure.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=300,
    grain_size=10.0,
    bond_weight=0.7,
    angle_weight=0.6,
    repulsion_weight=1.15,
    hard_core_scale=1.10,
    nonbond_push_scale=0.7,
    displacement_sigma=0.006,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_sro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_sro.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
