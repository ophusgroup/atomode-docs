# MRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), medium-range order.

[`silicon_dioxide_mro_generate.py`](../../_static/mace/silicon_dioxide/mro_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/silicon_dioxide/mro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/silicon_dioxide/mro_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/silicon_dioxide/mro_energy_curve.png
:alt: Silicon dioxide MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.756 |
| after cleanup | -7.022 |
| after MACE | -7.500 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/silicon_dioxide/mro_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/silicon_dioxide/mro_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/silicon_dioxide/mro_bond_hist.png
:alt: Silicon dioxide MRO bond length distribution
:width: 100%
```

```{image} ../../_static/mace/silicon_dioxide/mro_angle_hist.png
:alt: Silicon dioxide MRO angle distributions
:width: 100%
```

```{image} ../../_static/mace/silicon_dioxide/mro_gr.png
:alt: Silicon dioxide MRO pairwise g(r)
:width: 100%
```
