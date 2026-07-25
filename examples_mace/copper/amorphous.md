# Amorphous

A 40 Å cubic copper supercell (~5202 atoms), fully disordered, grain-free.

[`copper_amorphous_generate.py`](../../figures/mace/copper/amorphous_generate.py) reproduces this case.

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/amorphous_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/copper/amorphous_energy_curve.png
:alt: Copper Amorphous MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -3.880 |
| after MACE | -3.974 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/amorphous_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/amorphous_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/copper/amorphous_bond_hist.png
:alt: Copper Amorphous bond length distribution
:width: 100%
```

```{image} ../../figures/mace/copper/amorphous_angle_hist.png
:alt: Copper Amorphous angle distributions
:width: 100%
```

```{image} ../../figures/mace/copper/amorphous_gr.png
:alt: Copper Amorphous pairwise g(r)
:width: 100%
```
