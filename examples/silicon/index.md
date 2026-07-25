# Silicon

Silicon (diamond cubic, *a* = 5.431 Å) has 4-fold tetrahedral
coordination with a single Si-Si-Si bond angle of 109.5°.  It is the
reference case for the six disorder regimes.

## Overview

All six regimes at 40 × 40 × 40 Å, rotating in sync. Drag any panel to orbit
manually.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/overview/silicon.html
:width: 100%
:::

g(r) per regime overlaid on a single axis. The dropdown below the
plot switches species pair; the legend identifies each curve by the
regime it was measured from:

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g2_compare/silicon.html
:width: 100%
:::

## Reference crystal

```python
from ase.build import bulk
atoms = bulk('Si', 'diamond', a=5.431)
```

## Disorder regimes

Click any regime for the full interactive trajectory viewer and g3 distribution.

## Preset summary

``liquid`` and ``nanocrystalline`` keep the library
``atomode.Supercell.PRESETS`` defaults; the in-between regimes use
explicit per-cell parameters tuned so the polyhedron count walks a
clear ladder from disordered (liquid → ~110 tetrahedra detected at
the polyhedra-detector tolerances `bond_length_tol=0.10`,
`angle_tol_deg=18`) through to crystalline (NC → ~1300).

| Preset | `num_steps` | Grain (Å) | `bond_weight` | `angle_weight` | `repulsion_weight` | `hard_core_scale` | `nonbond_push_scale` | `displacement_sigma` |
|---|---|---|---|---|---|---|---|---|
| `liquid`              | 100 | -    | 0.4  | 0.5  | 0.5  | 0.75 | 0.7  | -    |
| `amorphous`           | 120 | -    | 0.6  | 0.20 | 1.3  | 0.86 | 0.45 | 0.12 |
| `SRO`                 | 180 | 8.0  | 1.5  | 0.5  | 1.8  | 0.91 | 0.60 | 0.06 |
| `MRO`                 | 200 | 12.0 | 2.0  | 0.8  | 2.2  | 0.93 | 0.75 | 0.04 |
| `LRO`                 | 200 | 15.0 | 2.4  | 1.0  | 2.3  | 0.93 | 0.85 | 0.035 |
| `nanocrystalline`     | 150 | 20.0 | 3.0  | 1.5  | -    | -    | -    | 0.02 |
