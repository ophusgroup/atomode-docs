# SRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), short-range order.

## Orientation refinement

<iframe src="../../_static/fire/strontium_titanate/sro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/strontium_titanate/sro_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.966 | 0.083 |
| after orient | 1.967 | 0.083 |
| after cleanup | 1.945 | 0.196 |
| after FIRE | 1.967 | 0.203 |

MACE-MP0 single point of the final structure: **-7.143 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/strontium_titanate/sro_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/strontium_titanate/sro_bond_hist.png
:alt: Strontium titanate SRO bond length distribution
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/sro_angle_hist.png
:alt: Strontium titanate SRO angle distributions
:width: 100%
```

```{image} ../../_static/fire/strontium_titanate/sro_gr.png
:alt: Strontium titanate SRO pairwise g(r)
:width: 100%
```
