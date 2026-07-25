# MRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), medium-range order.

[`strontium_titanate_mro_generate.py`](../../figures/mace/strontium_titanate/mro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/mro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/mro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/strontium_titanate/mro_energy_curve.png
:alt: Strontium titanate MRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.956 |
| after cleanup | -7.214 |
| after MACE | -7.782 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/mro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/strontium_titanate/mro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/strontium_titanate/mro_bond_hist.png
:alt: Strontium titanate MRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/mro_angle_hist.png
:alt: Strontium titanate MRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/mro_gr.png
:alt: Strontium titanate MRO pairwise g(r)
:width: 100%
```
