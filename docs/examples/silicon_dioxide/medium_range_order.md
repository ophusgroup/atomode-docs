# Medium-range order

SiO₂ with 10 Å α-quartz grains: grain interiors now comfortably hold
multiple shells of tetrahedra, so clear patches of α-quartz appear
interspersed with the phase-boundary disorder.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=250,
    grain_size=17.0,
    bond_weight=1.65,
    angle_weight=1.35,
    repulsion_weight=1.3,
    hard_core_scale=0.82,
    nonbond_push_scale=0.72,
    displacement_sigma=0.011,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/sio2_mro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/sio2_mro.html"
        width="100%" height="620"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
