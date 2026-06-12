# Amorphous

A 40 Å cubic silicon supercell (~3068 atoms), fully disordered, grain-free.

## FIRE relaxation

<iframe src="../../_static/fire/silicon/amorphous_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.512 | 0.255 |
| after orient | 2.512 | 0.255 |
| after cleanup | 2.467 | 0.179 |
| after FIRE | 2.408 | 0.156 |

MACE-MP0 single point of the final structure: **-4.883 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon/amorphous_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon/amorphous_bond_hist.png
:alt: Silicon Amorphous bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon/amorphous_angle_hist.png
:alt: Silicon Amorphous angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon/amorphous_gr.png
:alt: Silicon Amorphous pairwise g(r)
:width: 100%
```
