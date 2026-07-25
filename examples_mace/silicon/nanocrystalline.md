# Nanocrystalline

A 40 Å cubic silicon supercell (~3068 atoms), large crystalline grains with amorphous boundaries.

[`silicon_nanocrystalline_generate.py`](../../figures/mace/silicon/nanocrystalline_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/nanocrystalline_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/nanocrystalline_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon/nanocrystalline_energy_curve.png
:alt: Silicon Nanocrystalline MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -4.856 |
| after cleanup | -5.028 |
| after MACE | -5.182 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/nanocrystalline_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon/nanocrystalline_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon/nanocrystalline_bond_hist.png
:alt: Silicon Nanocrystalline bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon/nanocrystalline_angle_hist.png
:alt: Silicon Nanocrystalline angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon/nanocrystalline_gr.png
:alt: Silicon Nanocrystalline pairwise g(r)
:width: 100%
```
