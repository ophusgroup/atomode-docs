# Liquid

A 40 Å cubic silicon dioxide supercell (~4866 atoms), melt (Langevin MD at the melting point).

[`silicon_dioxide_liquid_generate.py`](../../figures/mace/silicon_dioxide/liquid_generate.py) reproduces this case.

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon_dioxide/liquid_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon_dioxide/liquid_energy_curve.png
:alt: Silicon dioxide Liquid MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -5.571 |
| after MACE | -6.472 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon_dioxide/liquid_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon_dioxide/liquid_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon_dioxide/liquid_bond_hist.png
:alt: Silicon dioxide Liquid bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/liquid_angle_hist.png
:alt: Silicon dioxide Liquid angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/liquid_gr.png
:alt: Silicon dioxide Liquid pairwise g(r)
:width: 100%
```
