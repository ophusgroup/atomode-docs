# Liquid

A 40 Å cubic copper supercell (~5202 atoms), melt (thermostatted spring-network sampling).

## FIRE relaxation

<iframe src="../../_static/fire/copper/liquid_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.759 | 0.363 |
| after orient | 2.759 | 0.363 |
| after cleanup | 2.626 | 0.278 |
| after FIRE | 2.641 | 0.301 |

MACE-MP0 single point of the final structure: **-3.812 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/copper/liquid_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/copper/liquid_bond_hist.png
:alt: Copper Liquid bond length distribution
:width: 100%
```

```{image} ../../_static/fire/copper/liquid_angle_hist.png
:alt: Copper Liquid angle distributions
:width: 100%
```

```{image} ../../_static/fire/copper/liquid_gr.png
:alt: Copper Liquid pairwise g(r)
:width: 100%
```
