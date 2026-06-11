# Copper

Copper supercells (40 × 40 × 40 Å) across the amorphous → nanocrystalline axis, refined with MACE-MP0.

## Final MACE structures

<iframe src="../../_static/mace/copper/overview.html"
        width="100%" height="660"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy across regimes

```{image} ../../_static/mace/copper/regime_ladder.png
:alt: Copper energy per atom across regimes
:width: 100%
```

## Summary

| regime | atoms | orient accepts | final E (eV/atom) |
|---|---:|---:|---:|
| [Liquid](liquid.md) | 5202 | 0 | -3.825 |
| [Amorphous](amorphous.md) | 5202 | 0 | -3.974 |
| [SRO](sro.md) | 5202 | 1 | -3.980 |
| [MRO](mro.md) | 5202 | 2 | -3.997 |
| [LRO](lro.md) | 5202 | 4 | -4.015 |
| [Nanocrystalline](nanocrystalline.md) | 5202 | 5 | -4.035 |

## Per-regime pages

```{toctree}
:maxdepth: 1

liquid
amorphous
sro
mro
lro
nanocrystalline
```