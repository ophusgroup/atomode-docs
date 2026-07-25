# sp³ nanocrystalline

A 40 Å cubic carbon supercell (~10887 atoms), diamond-like (4-coordinate) grains.

[`carbon_sp3_nc_generate.py`](../../figures/mace/carbon/sp3_nc_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/carbon/sp3_nc_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/carbon/sp3_nc_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/carbon/sp3_nc_energy_curve.png
:alt: Carbon sp³ nanocrystalline MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -8.026 |
| after cleanup | -8.181 |
| after MACE | -8.626 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/carbon/sp3_nc_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/carbon/sp3_nc_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/carbon/sp3_nc_bond_hist.png
:alt: Carbon sp³ nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../figures/mace/carbon/sp3_nc_angle_hist.png
:alt: Carbon sp³ nanocrystalline angle distributions
:width: 100%
```

```{image} ../../figures/mace/carbon/sp3_nc_gr.png
:alt: Carbon sp³ nanocrystalline pairwise g(r)
:width: 100%
```
