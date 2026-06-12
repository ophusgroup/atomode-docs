# SRO

A 40 Å cubic copper supercell (~5202 atoms), short-range order.

## Orientation refinement

<iframe src="../../_static/fire/copper/sro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/copper/sro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.623 | 0.259 |
| after orient | 2.625 | 0.259 |
| after cleanup | 2.618 | 0.262 |
| after FIRE | 2.616 | 0.229 |

MACE-MP0 single point of the final structure: **-3.882 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/copper/sro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/copper/sro_bond_hist.png
:alt: Copper SRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/copper/sro_angle_hist.png
:alt: Copper SRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/copper/sro_gr.png
:alt: Copper SRO pairwise g(r)
:width: 100%
```
