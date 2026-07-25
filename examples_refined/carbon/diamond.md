# Diamond

A 40 Å cubic carbon supercell (~10887 atoms), nanocrystalline diamond.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/carbon/diamond_orient_movie.html
:width: 100%
:::

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/carbon/diamond_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.538 | 0.050 |
| after orient | 1.538 | 0.051 |
| after cleanup | 1.544 | 0.018 |
| after FIRE | 1.545 | 0.073 |

MACE-MP0 single point of the final structure: **-8.285 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/fire/carbon/diamond_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/carbon/diamond_bond_hist.png
:alt: Carbon Diamond bond length distribution
:width: 100%
```

```{image} ../../figures/fire/carbon/diamond_angle_hist.png
:alt: Carbon Diamond angle distributions
:width: 100%
```

```{image} ../../figures/fire/carbon/diamond_gr.png
:alt: Carbon Diamond pairwise g(r)
:width: 100%
```
