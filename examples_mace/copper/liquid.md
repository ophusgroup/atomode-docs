# Liquid

A 40 Å cubic copper supercell (~5202 atoms), melt (Langevin MD at the melting point).

[`copper_liquid_generate.py`](../../figures/mace/copper/liquid_generate.py) reproduces this case.

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/liquid_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/copper/liquid_energy_curve.png
:alt: Copper Liquid MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -3.880 |
| after MACE | -3.825 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/liquid_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/liquid_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/copper/liquid_bond_hist.png
:alt: Copper Liquid bond length distribution
:width: 100%
```

```{image} ../../figures/mace/copper/liquid_angle_hist.png
:alt: Copper Liquid angle distributions
:width: 100%
```

```{image} ../../figures/mace/copper/liquid_gr.png
:alt: Copper Liquid pairwise g(r)
:width: 100%
```
