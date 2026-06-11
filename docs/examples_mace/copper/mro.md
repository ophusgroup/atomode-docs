# MRO

A 40 Å cubic copper supercell (~5202 atoms), medium-range order.

[`copper_mro_generate.py`](../../_static/mace/copper/mro_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/copper/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/copper/mro_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/copper/mro_energy_curve.png
:alt: Copper MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -3.486 |
| after cleanup | -3.935 |
| after MACE | -3.997 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/copper/mro_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/copper/mro_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/copper/mro_bond_hist.png
:alt: Copper MRO bond length distribution
:width: 100%
```

```{image} ../../_static/mace/copper/mro_angle_hist.png
:alt: Copper MRO angle distributions
:width: 100%
```

```{image} ../../_static/mace/copper/mro_gr.png
:alt: Copper MRO pairwise g(r)
:width: 100%
```
