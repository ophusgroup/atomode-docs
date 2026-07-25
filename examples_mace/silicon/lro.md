# LRO

A 40 Å cubic silicon supercell (~3068 atoms), long-range order.

[`silicon_lro_generate.py`](../../figures/mace/silicon/lro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/lro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/lro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon/lro_energy_curve.png
:alt: Silicon LRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -4.663 |
| after cleanup | -4.938 |
| after MACE | -5.138 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/lro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/silicon/lro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon/lro_bond_hist.png
:alt: Silicon LRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon/lro_angle_hist.png
:alt: Silicon LRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon/lro_gr.png
:alt: Silicon LRO pairwise g(r)
:width: 100%
```
