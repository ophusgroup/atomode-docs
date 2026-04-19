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
| liquid                       | 30  | —    | 0.25 | 0.00 | 0.4 | 0.70 | 0.50 | —    |
| amorphous                    | 80  | —    | 0.35 | 0.00 | 0.8 | 0.78 | 0.58 | —    |
| short-range order            | 150 | —    | 1.3  | 0.10 | 1.5 | 0.90 | 0.80 | —    |
| medium-range order           | 200 | —    | 2.0  | 0.20 | 1.9 | 0.94 | 0.95 | —    |
| extended medium-range order  | 250 | —    | 2.8  | 0.35 | 2.2 | 0.96 | 1.00 | —    |
| nanocrystalline              | 150 | 18.0 | 2.4  | 0.35 | 2.0 | 0.95 | 0.90 | 0.02 |

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
