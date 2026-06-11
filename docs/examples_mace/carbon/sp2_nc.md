# sp² nanocrystalline

A 40 Å cubic carbon supercell (~5974 atoms), graphitic (3-coordinate) grains.

[`carbon_sp2_nc_generate.py`](../../_static/mace/carbon/sp2_nc_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/carbon/sp2_nc_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/carbon/sp2_nc_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/carbon/sp2_nc_energy_curve.png
:alt: Carbon sp² nanocrystalline MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -8.172 |
| after cleanup | -8.239 |
| after MACE | -8.691 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/carbon/sp2_nc_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/carbon/sp2_nc_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/carbon/sp2_nc_bond_hist.png
:alt: Carbon sp² nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../_static/mace/carbon/sp2_nc_angle_hist.png
:alt: Carbon sp² nanocrystalline angle distributions
:width: 100%
```

```{image} ../../_static/mace/carbon/sp2_nc_gr.png
:alt: Carbon sp² nanocrystalline pairwise g(r)
:width: 100%
```
