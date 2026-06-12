# sp²-rich

A 40 Å cubic carbon supercell (~6957 atoms), 80 % graphite / 20 % diamond grains.

## Orientation refinement

<iframe src="../../_static/fire/carbon/sp2_rich_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/carbon/sp2_rich_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.471 | 0.073 |
| after orient | 1.472 | 0.072 |
| after cleanup | 1.473 | 0.063 |
| after FIRE | 1.483 | 0.089 |

MACE-MP0 single point of the final structure: **-8.158 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/carbon/sp2_rich_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/carbon/sp2_rich_bond_hist.png
:alt: Carbon sp²-rich bond length distribution
:width: 100%
```

```{image} ../../_static/fire/carbon/sp2_rich_angle_hist.png
:alt: Carbon sp²-rich angle distributions
:width: 100%
```

```{image} ../../_static/fire/carbon/sp2_rich_gr.png
:alt: Carbon sp²-rich pairwise g(r)
:width: 100%
```
