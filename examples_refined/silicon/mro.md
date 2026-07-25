# MRO

A 40 Å cubic silicon supercell (~3068 atoms), medium-range order.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon/mro_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon/mro_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.409 | 0.171 |
| after orient | 2.402 | 0.168 |
| after cleanup | 2.415 | 0.143 |
| after FIRE | 2.410 | 0.137 |

MACE-MP0 single point of the final structure: **-4.998 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon/mro_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/silicon/mro_bond_hist.png
:alt: Silicon MRO bond length distribution
:width: 100%
```

```{image} ../../figures/fire/silicon/mro_angle_hist.png
:alt: Silicon MRO angle distributions
:width: 100%
```

```{image} ../../figures/fire/silicon/mro_gr.png
:alt: Silicon MRO pairwise g(r)
:width: 100%
```
