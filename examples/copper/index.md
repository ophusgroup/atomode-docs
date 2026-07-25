# Copper

Copper is a good stress test for atomode. Its face-centred cubic structure
(*a* = 3.615 Å) has twelve-fold close-packed coordination and four distinct
first-shell bond angles (60°, 90°, 120°, 180°). The built-in
`Supercell.PRESETS` dictionary is tuned for covalent silicon, so copper is
run here with material-specific parameters that keep the angle springs
weak and rely on bond + repulsion springs to shape the local environment.

## Overview

All six regimes at 40 × 40 × 40 Å, rotating in sync. Drag any panel to
orbit manually. The tetrahedral bond filter used in the silicon overview
is disabled here because copper's first shell spans many angles, so bonds are
drawn whenever they fall inside the radial tolerance (any of the twelve
FCC neighbour distances).

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/overview/copper.html
:width: 100%
:::

g(r) per regime overlaid on a single axis. The legend identifies
each curve by the regime it was measured from:

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g2_compare/copper.html
:width: 100%
:::

## Reference crystal

```python
from ase.build import bulk
atoms = bulk("Cu", "fcc", a=3.615)
```

## Disorder regimes

Click any regime for the full interactive trajectory viewer and g3
distribution.

## Preset summary

Copper-specific parameter dictionaries used throughout this case. Fields
left blank use the default (`bond_weight=1.0`, `angle_weight=0.5`,
`repulsion_weight=3.0`, `hard_core_scale=1.0`, `nonbond_push_scale=1.0`).

| Regime | `num_steps` | `grain_size` (Å) | `bond_weight` | `angle_weight` | `repulsion_weight` | `hard_core_scale` | `nonbond_push_scale` | `displacement_sigma` |
|---|---|---|---|---|---|---|---|---|
| liquid                       |  40 | -    | 0.04 | 0.00 | 0.45 | 0.78 | 0.38 | -     |
| amorphous                    | 100 | -    | 0.35 | 0.00 | 0.85 | 0.88 | 0.60 | -     |
| short-range order            | 100 |  7.0 | 0.6  | 0.00 | 1.0  | 0.88 | 0.65 | 0.06  |
| medium-range order           | 120 |  9.0 | 0.85 | 0.00 | 1.3  | 0.89 | 0.72 | 0.045 |
| long-range order             | 140 | 12.5 | 1.1  | 0.00 | 1.6  | 0.91 | 0.82 | 0.03  |
| nanocrystalline              | 200 | 18.0 | 1.5  | 0.00 | 2.0  | 0.94 | 0.95 | 0.01  |

Angle springs are turned off everywhere (`angle_weight=0`) because
the FCC first-shell angular distribution is multimodal (60°, 90°,
120°, 180°), so a single-target angle spring would fight the natural
geometry.  Order is built up by progressively stiffer bond and
repulsion springs, larger Voronoi grains, and tighter
`hard_core_scale` / `nonbond_push_scale` instead.  `bond_weight`
walks 0.04 → 1.5 across the ladder; `nonbond_push_scale` walks
0.38 → 0.95 so the effective first-shell radius progressively
approaches the reference `pair_peak`.  Liquid + amorphous use no
grains; SRO through nanocrystalline grow the Voronoi grain size
from 7 Å → 18 Å.
