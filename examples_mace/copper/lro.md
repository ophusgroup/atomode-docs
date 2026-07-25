# LRO

A 40 Å cubic copper supercell (~5202 atoms), long-range order.

[`copper_lro_generate.py`](../../figures/mace/copper/lro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/lro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/lro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/copper/lro_energy_curve.png
:alt: Copper LRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -3.710 |
| after cleanup | -3.964 |
| after MACE | -4.015 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/lro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/lro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/copper/lro_bond_hist.png
:alt: Copper LRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/copper/lro_angle_hist.png
:alt: Copper LRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/copper/lro_gr.png
:alt: Copper LRO pairwise g(r)
:width: 100%
```
