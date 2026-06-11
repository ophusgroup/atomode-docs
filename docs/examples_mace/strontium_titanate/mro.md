# MRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), medium-range order.

[`strontium_titanate_mro_generate.py`](../../_static/mace/strontium_titanate/mro_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/strontium_titanate/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/strontium_titanate/mro_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/strontium_titanate/mro_energy_curve.png
:alt: Strontium titanate MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.956 |
| after cleanup | -7.214 |
| after MACE | -7.782 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/strontium_titanate/mro_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/strontium_titanate/mro_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/strontium_titanate/mro_bond_hist.png
:alt: Strontium titanate MRO bond length distribution
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/mro_angle_hist.png
:alt: Strontium titanate MRO angle distributions
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/mro_gr.png
:alt: Strontium titanate MRO pairwise g(r)
:width: 100%
```
