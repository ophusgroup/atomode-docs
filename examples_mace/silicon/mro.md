# MRO

A 40 Å cubic silicon supercell (~3068 atoms), medium-range order.

[`silicon_mro_generate.py`](../../figures/mace/silicon/mro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/mro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/mro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon/mro_energy_curve.png
:alt: Silicon MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -4.471 |
| after cleanup | -4.865 |
| after MACE | -5.104 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/mro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/mro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon/mro_bond_hist.png
:alt: Silicon MRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon/mro_angle_hist.png
:alt: Silicon MRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon/mro_gr.png
:alt: Silicon MRO pairwise g(r)
:width: 100%
```
