# LRO

A 40 Å cubic copper supercell (~5202 atoms), long-range order.

## Orientation refinement

<iframe src="../../_static/fire/copper/lro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/copper/lro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.592 | 0.175 |
| after orient | 2.591 | 0.173 |
| after cleanup | 2.583 | 0.197 |
| after FIRE | 2.607 | 0.183 |

MACE-MP0 single point of the final structure: **-3.956 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/copper/lro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/copper/lro_bond_hist.png
:alt: Copper LRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/copper/lro_angle_hist.png
:alt: Copper LRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/copper/lro_gr.png
:alt: Copper LRO pairwise g(r)
:width: 100%
```
