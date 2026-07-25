# LRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), long-range order.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon_dioxide/lro_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon_dioxide/lro_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.615 | 0.028 |
| after orient | 1.615 | 0.029 |
| after cleanup | 1.620 | 0.034 |
| after FIRE | 1.697 | 0.057 |

MACE-MP0 single point of the final structure: **-7.397 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon_dioxide/lro_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/silicon_dioxide/lro_bond_hist.png
:alt: Silicon dioxide LRO bond length distribution
:width: 100%
```

```{image} ../../figures/fire/silicon_dioxide/lro_angle_hist.png
:alt: Silicon dioxide LRO angle distributions
:width: 100%
```

```{image} ../../figures/fire/silicon_dioxide/lro_gr.png
:alt: Silicon dioxide LRO pairwise g(r)
:width: 100%
```
