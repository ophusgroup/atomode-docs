# LRO

A 40 Å cubic copper supercell (~5202 atoms), long-range order.

[`copper_lro_generate.py`](../../_static/mace/copper/lro_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/copper/lro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/copper/lro_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/copper/lro_energy_curve.png
:alt: Copper LRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -3.710 |
| after cleanup | -3.964 |
| after MACE | -4.015 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/copper/lro_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/copper/lro_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/copper/lro_bond_hist.png
:alt: Copper LRO bond length distribution
:width: 100%
```

```{image} ../../_static/mace/copper/lro_angle_hist.png
:alt: Copper LRO angle distributions
:width: 100%
```

```{image} ../../_static/mace/copper/lro_gr.png
:alt: Copper LRO pairwise g(r)
:width: 100%
```
