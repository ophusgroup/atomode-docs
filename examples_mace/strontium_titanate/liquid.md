# Liquid

A 40 Å cubic strontium titanate supercell (~5130 atoms), melt (Langevin MD at the melting point).

[`strontium_titanate_liquid_generate.py`](../../figures/mace/strontium_titanate/liquid_generate.py) reproduces this case.

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/liquid_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/strontium_titanate/liquid_energy_curve.png
:alt: Strontium titanate Liquid MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -6.357 |
| after MACE | -6.915 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/liquid_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/liquid_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/strontium_titanate/liquid_bond_hist.png
:alt: Strontium titanate Liquid bond length distribution
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/liquid_angle_hist.png
:alt: Strontium titanate Liquid angle distributions
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/liquid_gr.png
:alt: Strontium titanate Liquid pairwise g(r)
:width: 100%
```
