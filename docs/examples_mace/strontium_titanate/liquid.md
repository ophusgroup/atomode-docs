# Liquid

A 40 Å cubic strontium titanate supercell (~5130 atoms), melt (Langevin MD at the melting point).

[`strontium_titanate_liquid_generate.py`](../../_static/mace/strontium_titanate/liquid_generate.py) reproduces this case.

## MACE+wall relaxation

<iframe src="../../_static/mace/strontium_titanate/liquid_mace_movie.html" width="100%" height="560"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy

```{image} ../../_static/mace/strontium_titanate/liquid_energy_curve.png
:alt: Strontium titanate Liquid MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -6.357 |
| after MACE | -6.915 |

## g₃ distributions

**After cleanup**

<iframe src="../../_static/mace/strontium_titanate/liquid_g3_cleanup.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

**After MACE**

<iframe src="../../_static/mace/strontium_titanate/liquid_g3_mace.html" width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Bond length and angle distributions

```{image} ../../_static/mace/strontium_titanate/liquid_bond_hist.png
:alt: Strontium titanate Liquid bond length distribution
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/liquid_angle_hist.png
:alt: Strontium titanate Liquid angle distributions
:width: 100%
```

```{image} ../../_static/mace/strontium_titanate/liquid_gr.png
:alt: Strontium titanate Liquid pairwise g(r)
:width: 100%
```
