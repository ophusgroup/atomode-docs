# Amorphous

A 40 Å cubic silicon supercell (~3068 atoms), fully disordered, grain-free.

[`silicon_amorphous_generate.py`](../../figures/mace/silicon/amorphous_generate.py) reproduces this case.

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/amorphous_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon/amorphous_energy_curve.png
:alt: Silicon Amorphous MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after cleanup | -4.594 |
| after MACE | -4.978 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/amorphous_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/amorphous_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon/amorphous_bond_hist.png
:alt: Silicon Amorphous bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon/amorphous_angle_hist.png
:alt: Silicon Amorphous angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon/amorphous_gr.png
:alt: Silicon Amorphous pairwise g(r)
:width: 100%
```
