# Long-range order

SiO₂ with 14 Å α-quartz grains: each grain is now large enough to hold
several shells of intact SiO₄ tetrahedra, so crystalline patches cover
most of the cell. The remaining disorder sits at the grain boundaries
where rotated tiles meet.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=250,
    grain_size=20.0,
    bond_weight=1.7,
    angle_weight=1.4,
    repulsion_weight=1.3,
    hard_core_scale=0.82,
    nonbond_push_scale=0.72,
    displacement_sigma=0.01,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/sio2_lro.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/sio2_lro.html
:width: 100%
:::
