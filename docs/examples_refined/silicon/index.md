# Silicon

Silicon supercells (40 × 40 × 40 Å) across the amorphous → nanocrystalline axis, relaxed with the FIRE spring network.

## Final FIRE structures

<iframe src="../../_static/fire/silicon/overview.html"
        width="100%" height="660"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy across regimes

MACE-MP0 single-point energy of each FIRE-relaxed structure — directly comparable to the [MACE refinement](../../examples_mace/silicon/index.md) ladder.

```{image} ../../_static/fire/silicon/regime_ladder.png
:alt: Silicon FIRE structures scored with MACE
:width: 100%
```

## Summary

| regime | atoms | orient accepts | bond σ (Å) | MACE SP (eV/atom) |
|---|---:|---:|---:|---:|
| [Liquid](liquid.md) | 3068 | 0 | 0.155 | -4.815 |
| [Amorphous](amorphous.md) | 3068 | 0 | 0.156 | -4.883 |
| [SRO](sro.md) | 3068 | 38 | 0.145 | -4.934 |
| [MRO](mro.md) | 3068 | 60 | 0.137 | -4.998 |
| [LRO](lro.md) | 3068 | 21 | 0.125 | -5.044 |
| [Nanocrystalline](nanocrystalline.md) | 3068 | 20 | 0.111 | -5.100 |

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