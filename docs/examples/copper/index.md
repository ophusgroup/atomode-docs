# Copper

Copper is a good stress test for tricor. Its face-centred cubic structure
(*a* = 3.615 Å) has twelve-fold close-packed coordination and four distinct
first-shell bond angles (60°, 90°, 120°, 180°). The built-in
`Supercell.PRESETS` dictionary is tuned for covalent silicon, so copper is
run here with material-specific parameters that keep the angle springs
weak and rely on bond + repulsion springs to shape the local environment.

## Overview

All six regimes at 40 × 40 × 40 Å, rotating in sync. Drag any panel to
orbit manually. The tetrahedral bond filter used in the silicon overview
is disabled here - copper's first shell spans many angles, so bonds are
drawn whenever they fall inside the radial tolerance (any of the twelve
FCC neighbour distances).

<iframe src="../../_static/overview/copper.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Reference crystal

```python
from ase.build import bulk
atoms = bulk("Cu", "fcc", a=3.615)
```

## Disorder regimes

Click any regime for the full interactive trajectory viewer and g3
distribution.

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

Copper-specific parameter dictionaries used throughout this case. Fields
left blank use the default (`bond_weight=1.0`, `angle_weight=0.5`,
`repulsion_weight=3.0`, `hard_core_scale=1.0`, `nonbond_push_scale=1.0`).

| Regime | `num_steps` | `grain_size` (Å) | `bond_weight` | `angle_weight` | `repulsion_weight` | `hard_core_scale` | `nonbond_push_scale` | `displacement_sigma` |
|---|---|---|---|---|---|---|---|---|
| liquid                       | 30  | —    | 0.05 | 0.00 | 0.2 | 0.60 | 0.30 | —     |
| amorphous                    | 30  | 5.0  | 0.3  | 0.00 | 0.5 | 0.80 | 0.50 | 0.05  |
| short-range order            | 40  | 8.0  | 0.5  | 0.05 | 0.7 | 0.85 | 0.60 | 0.03  |
| medium-range order           | 60  | 10.0 | 1.0  | 0.10 | 1.2 | 0.90 | 0.80 | 0.02  |
| extended medium-range order  | 100 | 14.0 | 1.5  | 0.20 | 1.5 | 0.92 | 0.90 | 0.015 |
| nanocrystalline              | 150 | 21.0 | 1.5  | 0.20 | 1.5 | 0.94 | 0.95 | 0.01  |

Angle springs are turned off in the liquid and amorphous regimes because
the FCC first-shell angular distribution is multimodal (60°, 90°, 120°,
180°) - a single-target angle spring would fight the natural geometry.
SRO through extended MRO turn the angle spring back on at progressively
higher weight. The `nonbond_push_scale` value ramps from 0.5 (liquid) to
1.0 (extended MRO) so the effective first-shell radius progressively
approaches the reference `pair_peak` - this is what drives the increasing
bond count visible across the overview panels.  Only nanocrystalline uses
explicit Voronoi grain construction; the others start from random
positions and rely on the spring network alone.
