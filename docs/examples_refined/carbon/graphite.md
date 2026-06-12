# Graphite

A 40 Å cubic carbon supercell (~5974 atoms), nanocrystalline graphite.

## Orientation refinement

<iframe src="../../_static/fire/carbon/graphite_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## FIRE relaxation

<iframe src="../../_static/fire/carbon/graphite_fire_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

| stage | bond mean (Å) | bond σ (Å) |
|---|---:|---:|
| Voronoi | 1.430 | 0.048 |
| after orient | 1.429 | 0.047 |
| after cleanup | 1.430 | 0.034 |
| after FIRE | 1.464 | 0.067 |

MACE-MP0 single point of the final structure: **-8.501 eV/atom**.

## g₃ distribution — after FIRE

<iframe src="../../_static/fire/carbon/graphite_g3_fire.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/fire/carbon/graphite_bond_hist.png
:alt: Carbon Graphite bond length distribution
:width: 100%
```

```{image} ../../_static/fire/carbon/graphite_angle_hist.png
:alt: Carbon Graphite angle distributions
:width: 100%
```

```{image} ../../_static/fire/carbon/graphite_gr.png
:alt: Carbon Graphite pairwise g(r)
:width: 100%
```
