# SRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), short-range order.

[`silicon_dioxide_sro_generate.py`](../../_static/mace/silicon_dioxide/sro_generate.py) reproduces this case.

## Orientation refinement

<iframe src="../../_static/mace/silicon_dioxide/sro_orient_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## MACE+wall relaxation

<iframe src="../../_static/mace/silicon_dioxide/sro_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/silicon_dioxide/sro_energy_curve.png
:alt: Silicon dioxide SRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.518 |
| after cleanup | -6.889 |
| after MACE | -7.457 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/silicon_dioxide/sro_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/silicon_dioxide/sro_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/silicon_dioxide/sro_bond_hist.png
:alt: Silicon dioxide SRO bond length distribution
:width: 100%
```

```{image} ../../_static/mace/silicon_dioxide/sro_angle_hist.png
:alt: Silicon dioxide SRO angle distributions
:width: 100%
```

```{image} ../../_static/mace/silicon_dioxide/sro_gr.png
:alt: Silicon dioxide SRO pairwise g(r)
:width: 100%
```
