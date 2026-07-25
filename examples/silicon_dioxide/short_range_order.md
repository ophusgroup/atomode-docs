# Short-range order

SiO₂ with 8 Å α-quartz grains: each grain interior holds a handful of
intact SiO₄ tetrahedra, but the phase-mismatched boundaries dominate the
structure so correlations decay quickly beyond the first neighbour
shell.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=250,
    grain_size=14.0,
    bond_weight=1.6,
    angle_weight=1.3,
    repulsion_weight=1.25,
    hard_core_scale=0.82,
    nonbond_push_scale=0.71,
    displacement_sigma=0.011,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/sio2_sro.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/sio2_sro.html
:width: 100%
:::
