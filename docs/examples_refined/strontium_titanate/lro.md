# LRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), long-range order.

## Orientation refinement

<iframe src="../../_static/fire/strontium_titanate/lro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/strontium_titanate/lro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.961 | 0.060 |
| after orient | 1.961 | 0.054 |
| after cleanup | 1.928 | 0.137 |
| after FIRE | 1.966 | 0.173 |

MACE-MP0 single point of the final structure: **-7.467 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/strontium_titanate/lro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/strontium_titanate/lro_bond_hist.png
:alt: Strontium titanate LRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/lro_angle_hist.png
:alt: Strontium titanate LRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/lro_gr.png
:alt: Strontium titanate LRO pairwise g(r)
:width: 100%
```
