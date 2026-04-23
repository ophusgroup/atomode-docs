# Silicon

Silicon (diamond cubic, a = 5.431 A). 4-fold tetrahedral coordination with Si-Si-Si bond angle of 109.5 degrees. The reference case for the six disorder regimes.

## Overview

All six regimes at 40 × 40 × 40 Å, rotating in sync. Drag any panel to orbit
manually.

<iframe src="../../_static/overview/silicon.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

g(r) per regime overlaid on a single axis - the dropdown below the
plot switches species pair; the legend identifies each curve by the
regime it was measured from:

<iframe src="../../_static/g2_compare/silicon.html"
        width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Reference crystal

```python
from ase.build import bulk
atoms = bulk('Si', 'diamond', a=5.431)
```

## Disorder regimes

Click any regime for the full interactive trajectory viewer and g3 distribution.

```{toctree}
:maxdepth: 1

liquid
amorphous
short_range_order
medium_range_order
extended_medium_range_order
nanocrystalline
```

## Preset summary

All values come from ``tricor.Supercell.PRESETS``.  ``initial grain diameter``
is the target size passed to the Voronoi seeder; the grain size after
relaxation is typically slightly smaller.  Fields left blank use the default
(``bond_weight=1.0``, ``angle_weight=0.5``, ``repulsion_weight=3.0``,
``hard_core_scale=1.0``, ``nonbond_push_scale=1.0``, ``step_size=0.1``).

| Preset | Initial grain diameter (Å) | `num_steps` | `bond_weight` | `angle_weight` | `repulsion_weight` | `hard_core_scale` | `nonbond_push_scale` | `displacement_sigma` | `step_size` |
|---|---|---|---|---|---|---|---|---|---|
| `liquid`              | - | 100 | 0.4 | 0.5 | 0.5 | 0.75 | 0.7 | - | - |
| `amorphous`           | 6.0  | 150 | 1.2 | 0.6 | 1.5 | 0.9  | 0.5 | 0.08 | - |
| `SRO`                 | 10.0 | 200 | 2.2 | 1.0 | 2.0 | 0.95 | 0.6 | 0.04 | - |
| `MRO`                 | 13.0 | 150 | 1.9 | 0.9 | 2.5 | 0.95 | 0.7 | 0.04 | - |
| `MRO_more`            | 18.0 | 150 | 2.0 | 1.0 | - | 0.95 | 0.9 | 0.04 | - |
| `nanocrystalline`     | 20.0 | 150 | 3.0 | 1.5 | - | - | - | 0.02 | - |
