# Amorphous

A 40 Å cubic silicon dioxide supercell (~4866 atoms), fully disordered, grain-free.

[`silicon_dioxide_amorphous_generate.py`](../../figures/mace/silicon_dioxide/amorphous_generate.py) reproduces this case.

## Orientation refinement

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/amorphous_orient_movie.html
:width: 100%
:::

## MACE+wall relaxation

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/amorphous_mace_movie.html
:width: 100%
:::

## Energy

```{image} ../../figures/mace/silicon_dioxide/amorphous_energy_curve.png
:alt: Silicon dioxide Amorphous MACE energy per atom
:width: 100%
```

| stage | E (eV/atom) |
|---|---:|
| after orientation refinement | -6.157 |
| after cleanup | -6.675 |
| after MACE | -7.398 |

## g₃ distributions

**After cleanup**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/amorphous_g3_cleanup.html
:width: 100%
:::

**After MACE**

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/mace/silicon_dioxide/amorphous_g3_mace.html
:width: 100%
:::

## Bond length and angle distributions

```{image} ../../figures/mace/silicon_dioxide/amorphous_bond_hist.png
:alt: Silicon dioxide Amorphous bond length distribution
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/amorphous_angle_hist.png
:alt: Silicon dioxide Amorphous angle distributions
:width: 100%
```

```{image} ../../figures/mace/silicon_dioxide/amorphous_gr.png
:alt: Silicon dioxide Amorphous pairwise g(r)
:width: 100%
```
