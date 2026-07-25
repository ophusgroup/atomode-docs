# MRO

A 40 Å cubic copper supercell (~5202 atoms), medium-range order.

[`copper_mro_generate.py`](../../figures/mace/copper/mro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/mro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/mro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/copper/mro_energy_curve.png
:alt: Copper MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -3.486 |
| after cleanup | -3.935 |
| after MACE | -3.997 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/mro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/copper/mro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/copper/mro_bond_hist.png
:alt: Copper MRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/copper/mro_angle_hist.png
:alt: Copper MRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/copper/mro_gr.png
:alt: Copper MRO pairwise g(r)
:width: 100%
```
