# Nanocrystalline

A 40 Å cubic copper supercell (~5202 atoms), large crystalline grains with amorphous boundaries.

[`copper_nanocrystalline_generate.py`](../../figures/mace/copper/nanocrystalline_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/copper/nanocrystalline_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/copper/nanocrystalline_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/copper/nanocrystalline_energy_curve.png
:alt: Copper Nanocrystalline MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -3.878 |
| after cleanup | -3.997 |
| after MACE | -4.035 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/copper/nanocrystalline_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/copper/nanocrystalline_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/copper/nanocrystalline_bond_hist.png
:alt: Copper Nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../figures/mace/copper/nanocrystalline_angle_hist.png
:alt: Copper Nanocrystalline angle distributions
:width: 100%
```

```{image} ../../figures/mace/copper/nanocrystalline_gr.png
:alt: Copper Nanocrystalline pairwise g(r)
:width: 100%
```
