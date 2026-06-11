# Carbon

Carbon supercells (40 × 40 × 40 Å) across the sp²/sp³ mixing axis, refined with MACE-MP0.

## Final MACE structures

<iframe src="../../_static/mace/carbon/overview.html"
        width="100%" height="360"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;" loading="lazy"></iframe>

## Energy across regimes

```{image} ../../_static/mace/carbon/regime_ladder.png
:alt: Carbon energy per atom across regimes
:width: 100%
```

## Summary

| regime | atoms | orient accepts | final E (eV/atom) |
|---|---:|---:|---:|
| [sp² nanocrystalline](sp2_nc.md) | 5974 | 25 | -8.691 |
| [Mixed sp²/sp³](mixed_nc.md) | 8431 | 17 | -8.632 |
| [sp³ nanocrystalline](sp3_nc.md) | 10887 | 20 | -8.626 |

## Per-regime pages

```{toctree}
:maxdepth: 1

sp2_nc
mixed_nc
sp3_nc
```