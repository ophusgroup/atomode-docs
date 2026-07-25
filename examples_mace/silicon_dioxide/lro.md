# LRO

A 40 Å cubic silicon dioxide supercell (~4866 atoms), long-range order.

[`silicon_dioxide_lro_generate.py`](../../figures/mace/silicon_dioxide/lro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/lro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/lro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon_dioxide/lro_energy_curve.png
:alt: Silicon dioxide LRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.977 |
| after cleanup | -7.175 |
| after MACE | -7.530 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/lro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/lro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon_dioxide/lro_bond_hist.png
:alt: Silicon dioxide LRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/lro_angle_hist.png
:alt: Silicon dioxide LRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/lro_gr.png
:alt: Silicon dioxide LRO pairwise g(r)
:width: 100%
```
