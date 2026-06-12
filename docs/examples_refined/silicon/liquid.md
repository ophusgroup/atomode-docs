# Liquid

A 40 Å cubic silicon supercell (~3068 atoms), melt (thermostatted spring-network sampling).

## FIRE relaxation

<iframe src="../../_static/fire/silicon/liquid_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.512 | 0.255 |
| after orient | 2.512 | 0.255 |
| after cleanup | 2.467 | 0.179 |
| after FIRE | 2.413 | 0.155 |

MACE-MP0 single point of the final structure: **-4.815 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon/liquid_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon/liquid_bond_hist.png
:alt: Silicon Liquid bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon/liquid_angle_hist.png
:alt: Silicon Liquid angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon/liquid_gr.png
:alt: Silicon Liquid pairwise g(r)
:width: 100%
```
