# sp³-leaning

A 40 Å cubic carbon supercell (~8922 atoms), 40 % graphite / 60 % diamond grains.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/carbon/sp3_leaning_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/carbon/sp3_leaning_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.506 | 0.073 |
| after orient | 1.512 | 0.068 |
| after cleanup | 1.514 | 0.056 |
| after FIRE | 1.516 | 0.089 |

MACE-MP0 single point of the final structure: **-8.125 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/carbon/sp3_leaning_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/carbon/sp3_leaning_bond_hist.png
:alt: Carbon sp³-leaning bond length distribution
:width: 100%
```

```{image} ../../figures/fire/carbon/sp3_leaning_angle_hist.png
:alt: Carbon sp³-leaning angle distributions
:width: 100%
```

```{image} ../../figures/fire/carbon/sp3_leaning_gr.png
:alt: Carbon sp³-leaning pairwise g(r)
:width: 100%
```
