# sp³-rich

A 40 Å cubic carbon supercell (~9905 atoms), 20 % graphite / 80 % diamond grains.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/carbon/sp3_rich_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/carbon/sp3_rich_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.526 | 0.061 |
| after orient | 1.529 | 0.059 |
| after cleanup | 1.533 | 0.040 |
| after FIRE | 1.538 | 0.082 |

MACE-MP0 single point of the final structure: **-8.124 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/carbon/sp3_rich_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/carbon/sp3_rich_bond_hist.png
:alt: Carbon sp³-rich bond length distribution
:width: 100%
```

```{image} ../../figures/fire/carbon/sp3_rich_angle_hist.png
:alt: Carbon sp³-rich angle distributions
:width: 100%
```

```{image} ../../figures/fire/carbon/sp3_rich_gr.png
:alt: Carbon sp³-rich pairwise g(r)
:width: 100%
```
