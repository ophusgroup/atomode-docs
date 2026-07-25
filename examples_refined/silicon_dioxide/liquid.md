# Liquid

A 40 Å cubic silicon dioxide supercell (~4866 atoms), melt (thermostatted spring-network sampling).

## FIRE relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon_dioxide/liquid_fire_movie.html
:width: 100%
:::

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.639 | 0.169 |
| after orient | 1.639 | 0.169 |
| after cleanup | 1.664 | 0.089 |
| after FIRE | 1.678 | 0.133 |

MACE-MP0 single point of the final structure: **-6.559 eV/atom**.

## g₃ distribution — after FIRE

:::{iframe} https://ophusgroup.github.io/atomode-data/fire/silicon_dioxide/liquid_g3_fire.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/fire/silicon_dioxide/liquid_bond_hist.png
:alt: Silicon dioxide Liquid bond length distribution
:width: 100%
```

```{image} ../../figures/fire/silicon_dioxide/liquid_angle_hist.png
:alt: Silicon dioxide Liquid angle distributions
:width: 100%
```

```{image} ../../figures/fire/silicon_dioxide/liquid_gr.png
:alt: Silicon dioxide Liquid pairwise g(r)
:width: 100%
```
