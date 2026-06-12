# SRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), short-range order.

## Orientation refinement

<iframe src="../../_static/fire/silicon_dioxide/sro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/silicon_dioxide/sro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.617 | 0.043 |
| after orient | 1.616 | 0.040 |
| after cleanup | 1.624 | 0.044 |
| after FIRE | 1.707 | 0.067 |

MACE-MP0 single point of the final structure: **-7.268 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon_dioxide/sro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon_dioxide/sro_bond_hist.png
:alt: Silicon dioxide SRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon_dioxide/sro_angle_hist.png
:alt: Silicon dioxide SRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon_dioxide/sro_gr.png
:alt: Silicon dioxide SRO pairwise g(r)
:width: 100%
```
