# Nanocrystalline

A 40 Å cubic strontium titanate supercell (~5130 atoms), large crystalline grains with amorphous boundaries.

[`strontium_titanate_nanocrystalline_generate.py`](../../_static/mace/strontium_titanate/nanocrystalline_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/strontium_titanate/nanocrystalline_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/strontium_titanate/nanocrystalline_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/strontium_titanate/nanocrystalline_energy_curve.png
:alt: Strontium titanate Nanocrystalline MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -7.284 |
| after cleanup | -7.493 |
| after MACE | -7.839 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/strontium_titanate/nanocrystalline_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/strontium_titanate/nanocrystalline_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/strontium_titanate/nanocrystalline_bond_hist.png
:alt: Strontium titanate Nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/nanocrystalline_angle_hist.png
:alt: Strontium titanate Nanocrystalline angle distributions
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/nanocrystalline_gr.png
:alt: Strontium titanate Nanocrystalline pairwise g(r)
:width: 100%
```
