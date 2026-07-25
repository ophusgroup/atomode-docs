# Liquid

SiO₂ in the liquid regime: random Si and O positions at the correct
density and 2:1 O:Si ratio, followed by a short shell relaxation to
enforce the hard-core exclusion. Essentially no intact SiO₄ tetrahedra
survive.

## Parameters

See [Silicon dioxide](index.md#reference-crystal) for the α-quartz
reference and supercell construction. Then:

```python
cell.generate(
    shell_target,
    num_steps=120,
    grain_size=None,
    bond_weight=0.5,
    angle_weight=0.0,
    repulsion_weight=1.5,
    hard_core_scale=1.05,
    nonbond_push_scale=0.6,
    displacement_sigma=0.01,
)
```

Liquid keeps ``angle_weight=0`` so the random starting positions aren't
pulled into tetrahedral geometry by the angle spring.

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-data/trajectories/sio2_liquid.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-data/g3/sio2_liquid.html
:width: 100%
:::
