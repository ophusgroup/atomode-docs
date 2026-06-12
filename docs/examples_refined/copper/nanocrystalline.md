# Nanocrystalline

A 40 Å cubic copper supercell (~5202 atoms), large crystalline grains with amorphous boundaries.

## Orientation refinement

<iframe src="../../_static/fire/copper/nanocrystalline_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/copper/nanocrystalline_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 2.579 | 0.145 |
| after orient | 2.579 | 0.140 |
| after cleanup | 2.563 | 0.144 |
| after FIRE | 2.601 | 0.156 |

MACE-MP0 single point of the final structure: **-3.994 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/copper/nanocrystalline_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/copper/nanocrystalline_bond_hist.png
:alt: Copper Nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../_static/fire/copper/nanocrystalline_angle_hist.png
:alt: Copper Nanocrystalline angle distributions
:width: 100%
```

```{image} ../../_static/fire/copper/nanocrystalline_gr.png
:alt: Copper Nanocrystalline pairwise g(r)
:width: 100%
```
