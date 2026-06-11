# Amorphous

A 40 Å cubic silicon supercell (~3068 atoms), fully disordered, grain-free.

[`silicon_amorphous_generate.py`](../../_static/mace/silicon/amorphous_generate.py) reproduces this case.

## MACE+wall relaxation

<iframe src="../../_static/mace/silicon/amorphous_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/silicon/amorphous_energy_curve.png
:alt: Silicon Amorphous MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -4.594 |
| after MACE | -4.978 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/silicon/amorphous_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/silicon/amorphous_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/silicon/amorphous_bond_hist.png
:alt: Silicon Amorphous bond length distribution
:width: 100%
```

```{image} ../../_static/mace/silicon/amorphous_angle_hist.png
:alt: Silicon Amorphous angle distributions
:width: 100%
```

```{image} ../../_static/mace/silicon/amorphous_gr.png
:alt: Silicon Amorphous pairwise g(r)
:width: 100%
```
