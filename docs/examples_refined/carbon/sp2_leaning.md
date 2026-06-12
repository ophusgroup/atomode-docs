# sp²-leaning

A 40 Å cubic carbon supercell (~7939 atoms), 60 % graphite / 40 % diamond grains.

## Orientation refinement

<iframe src="../../_static/fire/carbon/sp2_leaning_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/carbon/sp2_leaning_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.472 | 0.081 |
| after orient | 1.494 | 0.072 |
| after cleanup | 1.496 | 0.063 |
| after FIRE | 1.497 | 0.087 |

MACE-MP0 single point of the final structure: **-8.178 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/carbon/sp2_leaning_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/carbon/sp2_leaning_bond_hist.png
:alt: Carbon sp²-leaning bond length distribution
:width: 100%
```

```{image} ../../_static/fire/carbon/sp2_leaning_angle_hist.png
:alt: Carbon sp²-leaning angle distributions
:width: 100%
```

```{image} ../../_static/fire/carbon/sp2_leaning_gr.png
:alt: Carbon sp²-leaning pairwise g(r)
:width: 100%
```
