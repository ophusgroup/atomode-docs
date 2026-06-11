# SRO

A 40 Å cubic copper supercell (~5202 atoms), short-range order.

[`copper_sro_generate.py`](../../_static/mace/copper/sro_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/copper/sro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/copper/sro_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/copper/sro_energy_curve.png
:alt: Copper SRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -3.241 |
| after cleanup | -3.904 |
| after MACE | -3.980 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/copper/sro_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/copper/sro_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/copper/sro_bond_hist.png
:alt: Copper SRO bond length distribution
:width: 100%
```

```{image} ../../_static/mace/copper/sro_angle_hist.png
:alt: Copper SRO angle distributions
:width: 100%
```

```{image} ../../_static/mace/copper/sro_gr.png
:alt: Copper SRO pairwise g(r)
:width: 100%
```
