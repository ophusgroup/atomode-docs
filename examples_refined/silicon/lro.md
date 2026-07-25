# LRO

A 40 Å cubic silicon supercell (~3068 atoms), long-range order.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon/lro_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon/lro_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.396 | 0.155 |
| after orient | 2.399 | 0.155 |
| after cleanup | 2.405 | 0.132 |
| after FIRE | 2.398 | 0.125 |

MACE-MP0 single point of the final structure: **-5.044 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon/lro_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/silicon/lro_bond_hist.png
:alt: Silicon LRO bond length distribution
:width: 100%
```

```{image} ../../figures/fire/silicon/lro_angle_hist.png
:alt: Silicon LRO angle distributions
:width: 100%
```

```{image} ../../figures/fire/silicon/lro_gr.png
:alt: Silicon LRO pairwise g(r)
:width: 100%
```
