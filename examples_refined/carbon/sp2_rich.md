# sp²-rich

A 40 Å cubic carbon supercell (~6957 atoms), 80 % graphite / 20 % diamond grains.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/carbon/sp2_rich_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/carbon/sp2_rich_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.471 | 0.073 |
| after orient | 1.472 | 0.072 |
| after cleanup | 1.473 | 0.063 |
| after FIRE | 1.483 | 0.089 |

MACE-MP0 single point of the final structure: **-8.158 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/carbon/sp2_rich_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/carbon/sp2_rich_bond_hist.png
:alt: Carbon sp²-rich bond length distribution
:width: 100%
```

```{image} ../../figures/fire/carbon/sp2_rich_angle_hist.png
:alt: Carbon sp²-rich angle distributions
:width: 100%
```

```{image} ../../figures/fire/carbon/sp2_rich_gr.png
:alt: Carbon sp²-rich pairwise g(r)
:width: 100%
```
