# MRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), medium-range order.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon_dioxide/mro_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon_dioxide/mro_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.616 | 0.039 |
| after orient | 1.616 | 0.037 |
| after cleanup | 1.624 | 0.043 |
| after FIRE | 1.705 | 0.064 |

MACE-MP0 single point of the final structure: **-7.301 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/silicon_dioxide/mro_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/silicon_dioxide/mro_bond_hist.png
:alt: Silicon dioxide MRO bond length distribution
:width: 100%
```

```{image} ../../figures/fire/silicon_dioxide/mro_angle_hist.png
:alt: Silicon dioxide MRO angle distributions
:width: 100%
```

```{image} ../../figures/fire/silicon_dioxide/mro_gr.png
:alt: Silicon dioxide MRO pairwise g(r)
:width: 100%
```
