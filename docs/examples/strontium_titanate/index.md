# Strontium titanate

Strontium titanate (SrTiO₃) is the archetypal cubic perovskite
(*a* = 3.913 Å) with three distinct sublattices: Sr at the cube corners
(12-coordinated by O), Ti at the body centre (6-coordinated by O,
forming a **TiO₆ octahedron**), and each O bridging two Ti along a
linear backbone while being surrounded by four Sr. Every panel below
renders the translucent orange TiO₆ octahedra - the motif whose
preservation across the disorder ladder drives everything else.

## Overview

All six regimes at an orthogonal 40 × 40 × 40 Å supercell, rotating in
sync. Drag any panel to orbit manually.

<iframe src="../../_static/overview/strontium_titanate.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

g(r) per regime overlaid on a single axis - the dropdown below the
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
3.91 Å are pure lattice separations through the bonded bridge atoms - treating them as bonds would install spurious angle springs that
destroy the TiO₆ octahedra.  The shell target is built with **both**
Ti–O and Sr–O enabled as bonds:

```python
import tricor as tc

shell_target = (
    tc.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    .with_bonded_species_pairs([('Ti', 'O'), ('Sr', 'O')])
    .with_angle_triplets([('Ti', 'O', 'O'), ('O', 'Ti', 'Ti')])
)

cell = tc.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(20.0, 20.0, 20.0),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell_target, grain_size=None)  # liquid - see regime pages
```

The second line - `with_angle_triplets(...)` - silences every
Sr-centered angle spring (and every triplet involving Sr as a
neighbour).  Reason: **SrO₁₂ is geometrically identical to the Cu-FCC
cuboctahedron**, so the O-Sr-O distribution is quadri-modal at
60°/90°/120°/180° and picking any one mode would strain the others.
The Cu FCC regime ladder handles this the same way (`angle_weight =
0`, all angles dropped); SrTiO₃ does it per-triplet so the TiO₆
octahedron's single-mode 90° and the Ti-O-Ti 180° backbone angles
can still be enforced.

The Sr atoms are held in place by 12 Sr-O bond-distance springs
each - not by an angle spring.  Combined with the repulsion wall
this is sufficient to preserve the SrO₁₂ geometry under relaxation.

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
| liquid                      | - | 80  |
| amorphous                   | 8.0  | 100 |
| short-range order           | 10.0 | 100 |
| medium-range order          | 12.0 | 100 |
| extended medium-range order | 15.0 | 100 |
| nanocrystalline             | 18.0 | 100 |

Shared ordered-regime weights
(`bond_weight=0.3`, `angle_weight=0.6`, `repulsion_weight=0.4`,
`hard_core_scale=1.0`, `nonbond_push_scale=0.5`,
`displacement_sigma=0.005`) drive the Ti-centered 90° + Ti-O-Ti 180°
angle springs while the Sr-centered cuboctahedron is held by its
12 Sr-O bond-distance springs alone.  The progression across panels
comes from the Voronoi grain size, not from per-regime hyper-tuning.
