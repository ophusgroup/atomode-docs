# Strontium titanate

Strontium titanate (SrTiO₃) is the archetypal cubic perovskite
(*a* = 3.913 Å) with three distinct sublattices: Sr at the cube corners
(12-coordinated by O), Ti at the body centre (6-coordinated by O,
forming a **TiO₆ octahedron**), and each O bridging two Ti along a
linear backbone while being surrounded by four Sr. Every panel below
renders the translucent orange TiO₆ octahedra — the motif whose
preservation across the disorder ladder drives everything else.

## Overview

All six regimes at an orthogonal 40 × 40 × 40 Å supercell, rotating in
sync. Drag any panel to orbit manually.

<iframe src="../../_static/overview/strontium_titanate.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Reference crystal

```python
from ase.io import read
atoms_ref = read('structures/SrTiO3.cif')   # 1 Sr + 1 Ti + 3 O
```

## Supercell

Only **Ti–O** is a real chemical bond in SrTiO₃. The observed short
Sr–O contact (2.77 Å) is ionic, and the Sr–Sr / Ti–Ti / Sr–Ti peaks at
*a* = 3.91 Å are pure lattice separations — treating them as bonds
would install spurious angle springs (`angle_mode_deg` for non-bond
triplets is a geometric artefact of the reference sampling) that
destroy the TiO₆ octahedra under relaxation. The new
`with_bonded_species_pairs` helper restricts the bond graph to a list
of explicit species pairs:

```python
import tricor as tc

shell_target = (
    tc.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    .with_bonded_species_pairs([('Ti', 'O')])
)

cell = tc.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(20.0, 20.0, 20.0),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell_target, grain_size=None)  # liquid - see regime pages
```

A second deliberate choice: **`angle_weight = 0`** for every SrTiO₃
regime. The octahedral vertex geometry is *bimodal* (twelve 90° pairs
plus three 180° antipodal pairs) while the shell-target extracts a
single mode per triplet. A 91° spring would force the antipodal pairs
away from 180°, tearing the octahedra apart. With bonds restricted to
Ti–O and angles switched off, the gentle bond-and-repulsion spring
network preserves whatever octahedra the Voronoi tiler lays down
without collapsing atoms at grain boundaries.

## Disorder regimes

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

| Regime | `grain_size` (Å) | `num_steps` |
|---|---|---|
| liquid                      | —    | 50 |
| amorphous                   | 8.0  | 50 |
| short-range order           | 10.0 | 50 |
| medium-range order          | 12.0 | 50 |
| extended medium-range order | 15.0 | 50 |
| nanocrystalline             | 18.0 | 50 |

Shared ordered-regime weights
(`bond_weight=0.2`, `angle_weight=0.0`, `repulsion_weight=0.3`,
`hard_core_scale=1.0`, `nonbond_push_scale=0.5`,
`displacement_sigma=0.005`) keep the initial tiled geometry intact;
the progression across panels comes from the Voronoi grain size, not
from per-regime hyper-tuning.
