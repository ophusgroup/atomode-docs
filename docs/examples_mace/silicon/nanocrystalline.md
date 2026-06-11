# Nanocrystalline

A 40 Å cubic silicon supercell (~3068 atoms), large crystalline grains with amorphous boundaries.

[`silicon_nanocrystalline_generate.py`](../../_static/mace/silicon/nanocrystalline_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/silicon/nanocrystalline_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/silicon/nanocrystalline_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/silicon/nanocrystalline_energy_curve.png
:alt: Silicon Nanocrystalline MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -4.856 |
| after cleanup | -5.028 |
| after MACE | -5.182 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/silicon/nanocrystalline_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/silicon/nanocrystalline_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/silicon/nanocrystalline_bond_hist.png
:alt: Silicon Nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../_static/mace/silicon/nanocrystalline_angle_hist.png
:alt: Silicon Nanocrystalline angle distributions
:width: 100%
```

```{image} ../../_static/mace/silicon/nanocrystalline_gr.png
:alt: Silicon Nanocrystalline pairwise g(r)
:width: 100%
```
