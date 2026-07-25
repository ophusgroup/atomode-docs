# SRO

A 40 Å cubic strontium titanate supercell (~5130 atoms), short-range order.

[`strontium_titanate_sro_generate.py`](../../figures/mace/strontium_titanate/sro_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/strontium_titanate/sro_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/strontium_titanate/sro_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/strontium_titanate/sro_energy_curve.png
:alt: Strontium titanate SRO MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.313 |
| after cleanup | -6.829 |
| after MACE | -7.704 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/strontium_titanate/sro_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-data/mace/strontium_titanate/sro_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/strontium_titanate/sro_bond_hist.png
:alt: Strontium titanate SRO bond length distribution
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/sro_angle_hist.png
:alt: Strontium titanate SRO angle distributions
:width: 100%
```

```{image} ../../figures/mace/strontium_titanate/sro_gr.png
:alt: Strontium titanate SRO pairwise g(r)
:width: 100%
```
