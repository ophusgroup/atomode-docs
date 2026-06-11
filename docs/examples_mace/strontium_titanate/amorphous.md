# Amorphous

A 40 Å cubic strontium titanate supercell (~5130 atoms), fully disordered, grain-free.

[`strontium_titanate_amorphous_generate.py`](../../_static/mace/strontium_titanate/amorphous_generate.py) reproduces this case.

## MACE+wall relaxation

<iframe src="../../_static/mace/strontium_titanate/amorphous_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/strontium_titanate/amorphous_energy_curve.png
:alt: Strontium titanate Amorphous MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -6.357 |
| after MACE | -7.567 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/strontium_titanate/amorphous_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/strontium_titanate/amorphous_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/strontium_titanate/amorphous_bond_hist.png
:alt: Strontium titanate Amorphous bond length distribution
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/amorphous_angle_hist.png
:alt: Strontium titanate Amorphous angle distributions
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/amorphous_gr.png
:alt: Strontium titanate Amorphous pairwise g(r)
:width: 100%
```
