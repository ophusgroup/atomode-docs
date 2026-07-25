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

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/srtio3_sro.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/srtio3_sro.html
:width: 100%
:::
