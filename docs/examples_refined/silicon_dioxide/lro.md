# LRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), long-range order.

## Orientation refinement

<iframe src="../../_static/fire/silicon_dioxide/lro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/silicon_dioxide/lro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.615 | 0.028 |
| after orient | 1.615 | 0.029 |
| after cleanup | 1.620 | 0.034 |
| after FIRE | 1.697 | 0.057 |

MACE-MP0 single point of the final structure: **-7.397 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon_dioxide/lro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon_dioxide/lro_bond_hist.png
:alt: Silicon dioxide LRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon_dioxide/lro_angle_hist.png
:alt: Silicon dioxide LRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon_dioxide/lro_gr.png
:alt: Silicon dioxide LRO pairwise g(r)
:width: 100%
```
