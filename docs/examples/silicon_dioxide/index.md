# Silicon dioxide

Silicon dioxide is a two-species network-former. Each Si sits at the
centre of a tetrahedron of four O neighbours (Si-O ≈ 1.61 Å), and each O
bridges two Si atoms. The reference here is α-quartz (trigonal *P*3₁21,
*a* = 4.9134 Å, *c* = 5.4052 Å) tiled into an orthogonal **20 × 20 × 20 Å**
supercell by `tricor.Supercell`.

Instead of drawing pairwise bonds, each panel renders a translucent
polyhedron around every Si whose four nearest O neighbours form a
near-ideal tetrahedron (bond length within ±15 % of 1.61 Å, all six
O-Si-O angles within ±22° of 109.47°).

## Overview

All six regimes at an orthogonal 40 × 40 × 40 Å supercell, rotating in
sync.  Drag any panel to orbit manually.

<iframe src="../../_static/overview/silicon_dioxide.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Reference crystal

```python
from ase.io import read
atoms_ref = read('structures/SiO2.cif')   # 3 Si + 6 O
```

## Supercell

`tricor.Supercell` tiles the α-quartz primitive into a Cartesian
20 × 20 × 20 Å box. The algorithm seeds Voronoi cells, tiles the
reference out to a sphere that covers the largest cell, rotates the tile
per grain (identity rotation when a single grain spans the whole box),
and filters atoms by exact convex-hull membership against each Voronoi
cell. Per-species atom counts are then pinned to the reference
stoichiometry scaled by `V_box / V_ref × relative_density` so every
regime has identical Si and O counts, and grain-boundary overlaps are
culled at `0.9 × hard_min`.

```python
import tricor as tc

# Only Si-O is a real chemical bond in SiO2.  with_cross_species_bonds_only
# zeros out same-species coordination so shell_relax doesn't treat the
# second-shell Si-Si / O-O peaks (which go through a bridging atom) as
# bonds - their ``angle_mode_deg`` is a geometric artefact, not a target.
shell_target = (
    tc.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    .with_cross_species_bonds_only()
)

cell = tc.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(20.0, 20.0, 20.0),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell_target, grain_size=None)  # liquid - see regime pages
```

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
| amorphous                   | 4.0  | 50 |
| short-range order           | 8.0  | 50 |
| medium-range order          | 10.0 | 50 |
| extended medium-range order | 14.0 | 50 |
| nanocrystalline             | 21.0 | 50 |

Relaxation weights are shared by every ordered regime
(`bond_weight=1.5`, `angle_weight=1.2`, `repulsion_weight=1.2`,
`hard_core_scale=0.8`, `nonbond_push_scale=0.7`,
`displacement_sigma=0.01`) so the visual progression across panels
comes from the initial grain tiling, not from per-regime hyper-tuning.
The liquid panel uses `angle_weight=0` so the random starting positions
aren't pulled into tetrahedral coordination by the angle spring.
