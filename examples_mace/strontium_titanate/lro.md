# LRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), long-range order.

[`strontium_titanate_lro_generate.py`](../../figures/mace/strontium_titanate/lro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/lro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/lro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/strontium_titanate/lro_energy_curve.png
:alt: Strontium titanate LRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -7.137 |
| after cleanup | -7.372 |
| after MACE | -7.818 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/lro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/lro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/strontium_titanate/lro_bond_hist.png
:alt: Strontium titanate LRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/lro_angle_hist.png
:alt: Strontium titanate LRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/lro_gr.png
:alt: Strontium titanate LRO pairwise g(r)
:width: 100%
```
