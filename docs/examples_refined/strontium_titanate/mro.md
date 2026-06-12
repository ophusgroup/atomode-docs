# MRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), medium-range order.

## Orientation refinement

<iframe src="../../_static/fire/strontium_titanate/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/strontium_titanate/mro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.963 | 0.069 |
| after orient | 1.961 | 0.057 |
| after cleanup | 1.930 | 0.157 |
| after FIRE | 1.965 | 0.183 |

MACE-MP0 single point of the final structure: **-7.373 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/strontium_titanate/mro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/strontium_titanate/mro_bond_hist.png
:alt: Strontium titanate MRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/mro_angle_hist.png
:alt: Strontium titanate MRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/mro_gr.png
:alt: Strontium titanate MRO pairwise g(r)
:width: 100%
```
