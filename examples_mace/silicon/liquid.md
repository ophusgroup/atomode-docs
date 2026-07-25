# Liquid

A 40 Å cubic silicon supercell (~3068 atoms), melt (Langevin MD at the melting point).

[`silicon_liquid_generate.py`](../../figures/mace/silicon/liquid_generate.py) reproduces this case.

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/liquid_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon/liquid_energy_curve.png
:alt: Silicon Liquid MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -4.594 |
| after MACE | -4.711 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/liquid_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/liquid_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon/liquid_bond_hist.png
:alt: Silicon Liquid bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon/liquid_angle_hist.png
:alt: Silicon Liquid angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon/liquid_gr.png
:alt: Silicon Liquid pairwise g(r)
:width: 100%
```
