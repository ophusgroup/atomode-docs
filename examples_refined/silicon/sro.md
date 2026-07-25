# SRO

A 40 Å cubic silicon supercell (~3068 atoms), short-range order.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon/sro_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon/sro_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.432 | 0.205 |
| after orient | 2.434 | 0.205 |
| after cleanup | 2.443 | 0.163 |
| after FIRE | 2.410 | 0.145 |

MACE-MP0 single point of the final structure: **-4.934 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon/sro_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/silicon/sro_bond_hist.png
:alt: Silicon SRO bond length distribution
:width: 100%
```

```{image} ../../figures/fire/silicon/sro_angle_hist.png
:alt: Silicon SRO angle distributions
:width: 100%
```

```{image} ../../figures/fire/silicon/sro_gr.png
:alt: Silicon SRO pairwise g(r)
:width: 100%
```
