# MRO

A 40 Å cubic copper supercell (~5202 atoms), medium-range order.

## Orientation refinement

<iframe src="../../_static/fire/copper/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/copper/mro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.608 | 0.218 |
| after orient | 2.606 | 0.215 |
| after cleanup | 2.602 | 0.234 |
| after FIRE | 2.611 | 0.208 |

MACE-MP0 single point of the final structure: **-3.918 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/copper/mro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/copper/mro_bond_hist.png
:alt: Copper MRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/copper/mro_angle_hist.png
:alt: Copper MRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/copper/mro_gr.png
:alt: Copper MRO pairwise g(r)
:width: 100%
```
