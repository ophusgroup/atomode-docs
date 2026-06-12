# Nanocrystalline

A 40 Å cubic silicon supercell (~3068 atoms), large crystalline grains with amorphous boundaries.

## Orientation refinement

<iframe src="../../_static/fire/silicon/nanocrystalline_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/silicon/nanocrystalline_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.379 | 0.124 |
| after orient | 2.385 | 0.132 |
| after cleanup | 2.393 | 0.122 |
| after FIRE | 2.393 | 0.111 |

MACE-MP0 single point of the final structure: **-5.100 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/silicon/nanocrystalline_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/silicon/nanocrystalline_bond_hist.png
:alt: Silicon Nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../_static/fire/silicon/nanocrystalline_angle_hist.png
:alt: Silicon Nanocrystalline angle distributions
:width: 100%
```

```{image} ../../_static/fire/silicon/nanocrystalline_gr.png
:alt: Silicon Nanocrystalline pairwise g(r)
:width: 100%
```
