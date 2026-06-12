# Strontium titanate

Strontium titanate (SrTiO₃) is the archetypal cubic perovskite
(*a* = 3.913 Å) with three distinct sublattices: Sr at the cube corners
(12-coordinated by O), Ti at the body centre (6-coordinated by O,
forming a **TiO₆ octahedron**), and each O bridging two Ti along a
linear backbone while being surrounded by four Sr. Every panel below
renders the translucent orange TiO₆ octahedra, the motif whose
preservation across the disorder ladder drives everything else.

## Overview

All six regimes at an orthogonal 40 × 40 × 40 Å supercell, rotating in
sync. Drag any panel to orbit manually.

<iframe src="../../_static/overview/strontium_titanate.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

g(r) per regime overlaid on a single axis. The dropdown below the
plot switches between the six species pairs (Sr-Sr, Sr-Ti, Sr-O,
Ti-Ti, Ti-O, O-O):

<iframe src="../../_static/g2_compare/strontium_titanate.html"
        width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Reference crystal

```python
from ase.io import read
atoms_ref = read('structures/SrTiO3.cif')   # 1 Sr + 1 Ti + 3 O
```

## Supercell

SrTiO₃ has **two** real chemical bonds: short covalent **Ti–O**
(1.96 Å, the TiO₆ octahedron) and longer ionic **Sr–O** (2.77 Å, the
SrO₁₂ cuboctahedron).  The Sr–Sr / Ti–Ti / Sr–Ti peaks at *a* =
3.91 Å are pure lattice separations through the bonded bridge atoms;
``CoordinationShellTarget.from_atoms`` zeroes those lattice-artefact
pairs automatically (any pair whose ``pair_peak`` is not the smallest
in either its row or column).  The angle whitelist is required: the
SrO₁₂ cuboctahedron is multi-modal (60° / 90° / 120° / 180°), so no
single-target Sr-centred angle spring would converge.

```python
import tricor as tc

shell_target = (
    tc.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    .with_angle_triplets([('Ti', 'O', 'O'), ('O', 'Ti', 'Ti')])
)

cell = tc.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell_target, grain_size=None)  # liquid; see regime pages
```

The `with_angle_triplets(...)` modifier silences every
Sr-centered angle spring (and every triplet involving Sr as a
neighbour).  Reason: **SrO₁₂ is geometrically identical to the Cu-FCC
cuboctahedron**, so the O-Sr-O distribution is quadri-modal at
60°/90°/120°/180° and picking any one mode would strain the others.
The Cu FCC regime ladder handles this the same way (`angle_weight =
0`, all angles dropped); SrTiO₃ does it per-triplet so the TiO₆
octahedron's single-mode 90° and the Ti-O-Ti 180° backbone angles
can still be enforced.

The Sr atoms are held in place by 12 Sr-O bond-distance springs
each, not by an angle spring.  Combined with the repulsion wall
this is sufficient to preserve the SrO₁₂ geometry under relaxation.

## Disorder regimes

```{toctree}
:maxdepth: 1

liquid
amorphous
short_range_order
medium_range_order
long_range_order
nanocrystalline
```

## Preset summary

| Regime | `num_steps` | `grain_size` (Å) | `bond_weight` | `angle_weight` | `repulsion_weight` | `displacement_sigma` |
|---|---|---|---|---|---|---|
| liquid                      | 200 | -    | 0.10 | 0.0  | 1.0  | 0.020 |
| amorphous                   | 300 | -    | 0.50 | 0.4  | 1.1  | 0.008 |
| short-range order           | 350 | 14.0 | 1.0  | 0.7  | 1.2  | 0.005 |
| medium-range order          | 400 | 22.0 | 1.0  | 0.7  | 1.2  | 0.002 |
| long-range order            | 450 | 28.0 | 1.0  | 0.7  | 1.2  | 0.0015 |
| nanocrystalline             | 500 | 35.0 | 1.0  | 0.7  | 1.2  | 0.001 |

SRO through NC share the same bond + angle weights (1.0 / 0.7).
The order ladder is built by progressively growing the grain
(14 → 22 → 28 → 35 Å) and the relaxation budget (350 → 400 → 450 →
500 steps) while tightening ``displacement_sigma`` (0.005 → 0.001).
Larger weights *reduce* the count of detected TiO₆ octahedra by
20–30 % — the angle springs over-constrain and conflict with the
remaining cuboctahedral O-Sr-O modes.

`hard_core_scale=1.10` (shared) enforces a ~1.65 Å minimum Ti-O
separation (below the 1.96 Å Ti-O bond but well above 1.5 Å) and a
~3.7 Å minimum Sr-Sr / Ti-Ti separation that lets the cuboctahedral
SrO₁₂ network re-form during FIRE.  Dropping the wall to ``1.0`` cuts
the octahedra count 5–10 ×.  `nonbond_push_scale=0.75` (shared)
keeps the second-shell gap clean.

The Ti-centred 90° (O-Ti-O) and 180° (Ti-O-Ti) angle springs hold the
TiO₆ octahedra together; the Sr-centred cuboctahedron is held by its
12 Sr-O bond-distance springs alone (the explicit
``with_angle_triplets([('Ti','O','O'), ('O','Ti','Ti')])`` whitelist
silences every Sr-centred angle, since the O-Sr-O distribution is
quadri-modal at 60° / 90° / 120° / 180°).

The benchmark ladder (rng seed 42, 40 Å cell, 0.18 / 18° octahedra
detector, 1026 Ti atoms) walks ≈ 1 (amorphous) → 107 (SRO) → 266
(MRO) → 360 (LRO) → 490 (NC) detected TiO₆ octahedra, a monotonic
0 % → 48 % progression.
