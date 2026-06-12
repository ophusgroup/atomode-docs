# MRO

A 40 Å cubic silicon supercell (~3068 atoms), medium-range order.

## Orientation refinement

<iframe src="../../_static/fire/silicon/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/silicon/mro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.409 | 0.171 |
| after orient | 2.402 | 0.168 |
| after cleanup | 2.415 | 0.143 |
| after FIRE | 2.410 | 0.137 |

MACE-MP0 single point of the final structure: **-4.998 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon/mro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon/mro_bond_hist.png
:alt: Silicon MRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon/mro_angle_hist.png
:alt: Silicon MRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon/mro_gr.png
:alt: Silicon MRO pairwise g(r)
:width: 100%
```
