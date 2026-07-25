# Liquid

SrTiO₃ in the liquid regime: random Sr / Ti / O positions at the
correct 1 : 1 : 3 stoichiometry and density, followed by a short shell
relaxation that enforces only the hard-core exclusion. No TiO₆
octahedra survive.

## Parameters

See [Strontium titanate](index.md#supercell) for the reference crystal
and shell-target setup. Then:

```python
cell.generate(
    shell_target,
    num_steps=200,
    grain_size=None,
    bond_weight=0.10,
    angle_weight=0.0,
    repulsion_weight=1.0,
    hard_core_scale=1.10,
    nonbond_push_scale=0.6,
    displacement_sigma=0.02,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-data/trajectories/srtio3_liquid.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-data/g3/srtio3_liquid.html
:width: 100%
:::
