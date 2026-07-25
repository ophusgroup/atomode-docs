# MRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), medium-range order.

[`silicon_dioxide_mro_generate.py`](../../figures/mace/silicon_dioxide/mro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/mro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/mro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon_dioxide/mro_energy_curve.png
:alt: Silicon dioxide MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.756 |
| after cleanup | -7.022 |
| after MACE | -7.500 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/mro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/mro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon_dioxide/mro_bond_hist.png
:alt: Silicon dioxide MRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/mro_angle_hist.png
:alt: Silicon dioxide MRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/mro_gr.png
:alt: Silicon dioxide MRO pairwise g(r)
:width: 100%
```
