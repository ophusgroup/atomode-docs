# MRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), medium-range order.

## Orientation refinement

<iframe src="../../_static/fire/silicon_dioxide/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/silicon_dioxide/mro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.616 | 0.039 |
| after orient | 1.616 | 0.037 |
| after cleanup | 1.624 | 0.043 |
| after FIRE | 1.705 | 0.064 |

MACE-MP0 single point of the final structure: **-7.301 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon_dioxide/mro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon_dioxide/mro_bond_hist.png
:alt: Silicon dioxide MRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon_dioxide/mro_angle_hist.png
:alt: Silicon dioxide MRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon_dioxide/mro_gr.png
:alt: Silicon dioxide MRO pairwise g(r)
:width: 100%
```
