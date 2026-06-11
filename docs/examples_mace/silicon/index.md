# Silicon

Silicon supercells (40 × 40 × 40 Å) across the amorphous → nanocrystalline axis, refined with MACE-MP0.

## Final MACE structures

<iframe src="../../_static/mace/silicon/overview.html"
        width="100%" height="660"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy across regimes

```{image} ../../_static/mace/silicon/regime_ladder.png
:alt: Silicon energy per atom across regimes
:width: 100%
```

## Summary

| regime | atoms | orient accepts | final E (eV/atom) |
|---|---:|---:|---:|
| [Liquid](liquid.md) | 3068 | 0 | -4.711 |
| [Amorphous](amorphous.md) | 3068 | 0 | -4.978 |
| [SRO](sro.md) | 3068 | 39 | -5.037 |
| [MRO](mro.md) | 3068 | 60 | -5.104 |
| [LRO](lro.md) | 3068 | 21 | -5.138 |
| [Nanocrystalline](nanocrystalline.md) | 3068 | 20 | -5.182 |

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