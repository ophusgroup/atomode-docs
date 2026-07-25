# Silicon dioxide

Silicon dioxide is a two-species network-former. Each Si sits at the
centre of a tetrahedron of four O neighbours (Si-O ≈ 1.61 Å), and each O
bridges two Si atoms. The reference here is α-quartz (trigonal *P*3₁21,
*a* = 4.9134 Å, *c* = 5.4052 Å) tiled into an orthogonal **40 × 40 × 40 Å**
supercell by `atomode.Supercell`.

Instead of drawing pairwise bonds, each panel renders a translucent
polyhedron around every Si whose four nearest O neighbours form a
near-ideal tetrahedron (bond length within ±15 % of 1.61 Å, all six
O-Si-O angles within ±25° of 109.47°).

## Overview

All six regimes at an orthogonal 40 × 40 × 40 Å supercell, rotating in
sync.  Drag any panel to orbit manually.

:::{iframe} https://ophusgroup.github.io/atomode-data/overview/silicon_dioxide.html
:width: 100%
:::

g(r) per regime overlaid on a single axis (most disordered curve at
the bottom, most ordered at the top). The dropdown below the plot
switches between the three species pairs in alphabetical order
(`O-O`, `O-Si`, `Si-Si`); only `O-Si` is a real chemical bond, the
other two peaks are lattice separations through a bridging atom.
The Si-O peak at 1.61 Å sharpens monotonically up the ladder; the
Si-Si and O-O second-shell peaks at 2.64 / 3.06 Å develop crystalline
fine structure (split shells) only at LRO / NC.

:::{iframe} https://ophusgroup.github.io/atomode-data/g2_compare/silicon_dioxide.html
:width: 100%
:::

## Reference crystal

```python
from ase.io import read
atoms_ref = read('structures/SiO2.cif')   # 3 Si + 6 O
```

## Supercell

`atomode.Supercell` tiles the α-quartz primitive into a Cartesian
40 × 40 × 40 Å box.  The algorithm seeds Voronoi cells, tiles the
reference out to a sphere that covers the largest cell, rotates the
tile per grain (identity rotation when ``grain_size=None``), and
filters atoms by exact convex-hull membership against each Voronoi
cell.  Per-species atom counts are then pinned to the reference
stoichiometry scaled by ``V_box / V_ref × relative_density`` so every
regime has identical Si and O counts, and grain-boundary overlaps are
culled at ``0.9 × hard_min``.

```python
import atomode as am

# Only Si-O is a real chemical bond in SiO2.  The second-shell
# Si-Si (3.06 Å) and O-O (2.64 Å) peaks are lattice separations
# through a bridging atom; ``from_atoms`` zeroes their coordination
# targets automatically (``auto_filter_lattice_artifacts=True``), so
# they install no bond springs.
shell_target = am.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)

cell = am.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell_target, grain_size=None)  # liquid; see regime pages
```

## Disorder regimes

## Preset summary

| Regime | `num_steps` | `grain_size` (Å) | `bond_weight` | `angle_weight` | `repulsion_weight` | `hard_core_scale` | `nonbond_push_scale` | `displacement_sigma` |
|---|---|---|---|---|---|---|---|---|
| liquid                      | 120 | -    | 0.50 | 0.0  | 1.5  | 1.05 | 0.60 | 0.010 |
| amorphous                   | 250 | 12.0 | 1.55 | 1.25 | 1.25 | 0.81 | 0.70 | 0.012 |
| short-range order           | 250 | 15.0 | 1.65 | 1.35 | 1.30 | 0.82 | 0.72 | 0.010 |
| medium-range order          | 300 | 20.0 | 1.65 | 1.35 | 1.30 | 0.82 | 0.72 | 0.008 |
| long-range order            | 350 | 26.0 | 1.65 | 1.35 | 1.30 | 0.82 | 0.72 | 0.006 |
| nanocrystalline             | 400 | 35.0 | 1.65 | 1.35 | 1.30 | 0.82 | 0.72 | 0.003 |

The liquid panel uses `angle_weight=0` so the random starting positions
aren't pulled into tetrahedral coordination by the angle spring; every
other regime keeps the angle spring on so SiO₄ tetrahedra form.

SRO through NC share the same bond + angle weights (1.65 / 1.35).
The order ladder is built by progressively growing the grain
(15 → 20 → 26 → 35 Å) and the relaxation budget (250 → 300 → 350 →
400 steps) while tightening ``displacement_sigma`` (0.010 → 0.008 →
0.006 → 0.003). Larger crystalline grain interiors and longer FIRE
budgets give the boundary atoms more time to settle into tetrahedral
coordination.  Larger weights saturate at the same number of
detected SiO₄ tetrahedra while distorting boundary atoms past the
0.10 / 18° detector tolerance.

The benchmark ladder (rng seed 42, 40 Å cell, 0.10 / 18° detector)
walks ≈ 668 (amorphous) → 788 (SRO) → 895 (MRO) → 1022 (LRO) → 1141
(NC) clean SiO₄ tetrahedra out of 1622 Si atoms, a monotonic 41 % →
70 % progression.
