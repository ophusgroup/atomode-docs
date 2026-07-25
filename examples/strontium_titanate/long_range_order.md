# Long-range order

SrTiO₃ with 18 Å grains: each grain holds several shells of intact
TiO₆ octahedra and the crystalline patches cover most of the cell.
The remaining disorder sits at the narrow seams where rotated grains
meet.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=350,
    grain_size=18.0,
    bond_weight=1.1,
    angle_weight=0.8,
    repulsion_weight=1.3,
    hard_core_scale=1.10,
    nonbond_push_scale=0.8,
    displacement_sigma=0.004,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/srtio3_lro.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/srtio3_lro.html
:width: 100%
:::
