# Liquid

A 40 Å cubic strontium titanate supercell (~5130 atoms), melt (thermostatted spring-network sampling).

## FIRE relaxation

<iframe src="../../_static/fire/strontium_titanate/liquid_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.021 | 0.252 |
| after orient | 2.021 | 0.252 |
| after cleanup | 1.960 | 0.230 |
| after FIRE | 1.990 | 0.200 |

MACE-MP0 single point of the final structure: **-6.968 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/strontium_titanate/liquid_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/strontium_titanate/liquid_bond_hist.png
:alt: Strontium titanate Liquid bond length distribution
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/liquid_angle_hist.png
:alt: Strontium titanate Liquid angle distributions
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/liquid_gr.png
:alt: Strontium titanate Liquid pairwise g(r)
:width: 100%
```
