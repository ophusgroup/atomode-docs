# Copper

Copper is a good stress test for tricor. Its face-centred cubic structure
(*a* = 3.615 Å) has twelve-fold close-packed coordination and four distinct
first-shell bond angles (60°, 90°, 120°, 180°). The built-in
`Supercell.PRESETS` dictionary is tuned for covalent silicon, so copper is
run here with material-specific parameters that keep the angle springs
weak and rely on bond + repulsion springs to shape the local environment.

## Reference crystal

```python
from ase.build import bulk
atoms = bulk("Cu", "fcc", a=3.615)
```

## Regimes covered

Three regimes are currently documented. Small-grain short- and
medium-range-order configurations for close-packed systems need additional
overlap-removal tuning and are deferred.

```{toctree}
:maxdepth: 1

liquid
amorphous
nanocrystalline
```

## Overview

All three regimes at 40 × 40 × 40 Å, rotating in sync. Drag any panel to
orbit manually. The tetrahedral bond filter used in the silicon overview
is disabled here - copper's first shell spans many angles, so bonds are
drawn whenever they fall inside the radial tolerance (any of the 12 FCC
neighbour distances).

<iframe src="../../_static/overview/copper.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Preset parameters

Copper-specific parameter dictionaries used throughout this case. Fields
left blank use the default (`bond_weight=1.0`, `angle_weight=0.5`,
`repulsion_weight=3.0`, `hard_core_scale=1.0`, `nonbond_push_scale=1.0`).

| Regime | `num_steps` | `grain_size` (Å) | `bond_weight` | `angle_weight` | `repulsion_weight` | `hard_core_scale` | `nonbond_push_scale` | `displacement_sigma` |
|---|---|---|---|---|---|---|---|---|
| liquid          | 100 | —    | 0.4 | 0.08 | 0.5 | 0.75 | 0.7 | —    |
| amorphous       | 120 | —    | 1.3 | 0.10 | 1.5 | 0.9  | 0.6 | —    |
| nanocrystalline | 150 | 14.0 | 2.2 | 0.30 | 2.0 | 0.95 | 0.8 | 0.02 |

Angle weights are roughly an order of magnitude smaller than the silicon
presets because the FCC first-shell angular distribution is multimodal -
forcing all triplets toward a single target angle would fight the natural
geometry.
