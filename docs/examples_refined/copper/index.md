# Copper

Copper supercells (40 × 40 × 40 Å) across the amorphous → nanocrystalline axis, relaxed with the FIRE spring network.

## Final FIRE structures

<iframe src="../../_static/fire/copper/overview.html"
        width="100%" height="660"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy across regimes

MACE-MP0 single-point energy of each FIRE-relaxed structure — directly comparable to the [MACE refinement](../../examples_mace/copper/index.md) ladder.

```{image} ../../_static/fire/copper/regime_ladder.png
:alt: Copper FIRE structures scored with MACE
:width: 100%
```

## Summary

| regime | atoms | orient accepts | bond σ (Å) | MACE SP (eV/atom) |
|---|---:|---:|---:|---:|
| [Liquid](liquid.md) | 5202 | 0 | 0.301 | -3.812 |
| [Amorphous](amorphous.md) | 5202 | 0 | 0.241 | -3.854 |
| [SRO](sro.md) | 5202 | 1 | 0.229 | -3.882 |
| [MRO](mro.md) | 5202 | 2 | 0.208 | -3.918 |
| [LRO](lro.md) | 5202 | 4 | 0.183 | -3.956 |
| [Nanocrystalline](nanocrystalline.md) | 5202 | 5 | 0.156 | -3.994 |

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