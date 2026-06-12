# Strontium titanate

Strontium titanate supercells (40 × 40 × 40 Å) across the amorphous → nanocrystalline axis, relaxed with the FIRE spring network.

## Final FIRE structures

<iframe src="../../_static/fire/strontium_titanate/overview.html"
        width="100%" height="660"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy across regimes

MACE-MP0 single-point energy of each FIRE-relaxed structure — directly comparable to the [MACE refinement](../../examples_mace/strontium_titanate/index.md) ladder.

```{image} ../../_static/fire/strontium_titanate/regime_ladder.png
:alt: Strontium titanate FIRE structures scored with MACE
:width: 100%
```

## Summary

| regime | atoms | orient accepts | bond σ (Å) | MACE SP (eV/atom) |
|---|---:|---:|---:|---:|
| [Liquid](liquid.md) | 5130 | 0 | 0.200 | -6.968 |
| [Amorphous](amorphous.md) | 5130 | 17 | 0.207 | -7.004 |
| [SRO](sro.md) | 5130 | 25 | 0.203 | -7.143 |
| [MRO](mro.md) | 5130 | 10 | 0.183 | -7.373 |
| [LRO](lro.md) | 5130 | 8 | 0.173 | -7.467 |
| [Nanocrystalline](nanocrystalline.md) | 5130 | 6 | 0.166 | -7.517 |

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