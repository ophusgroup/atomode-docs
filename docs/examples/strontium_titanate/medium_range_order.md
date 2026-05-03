# Medium-range order

SrTiO₃ with 14 Å grains: grain interiors comfortably hold multiple
linked TiO₆ octahedra, so distinct perovskite patches now stand out
against the phase-boundary disorder.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=350,
    grain_size=14.0,
    bond_weight=0.9,
    angle_weight=0.7,
    repulsion_weight=1.2,
    hard_core_scale=1.10,
    nonbond_push_scale=0.75,
    displacement_sigma=0.005,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_mro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_mro.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
