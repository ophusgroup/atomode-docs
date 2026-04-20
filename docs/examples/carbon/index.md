# Carbon

Carbon's structural axis isn't crystalline ↔ amorphous — it's **sp² ↔
sp³**.  Graphite stacks planar 3-coordinated (sp²) sheets; diamond is
the 4-coordinated (sp³) tetrahedral network.  Real carbon materials —
ta-C (tetrahedral amorphous carbon), DLC coatings, glassy carbon,
nanocrystalline diamond — sit at controlled points along that axis.

The carbon pipeline builds six regimes by mixing **Voronoi grains**:
each grain is either a rotated graphite tile (sp², 3 neighbours,
120°) or a rotated diamond tile (sp³, 4 neighbours, 109.5°), and the
mix fraction controls where on the sp²/sp³ axis the cell sits.

## Overview

All six regimes at 40 × 40 × 40 Å, rotating in sync.  Green triangles
decorate every sp² atom whose three neighbours form a 120° trigonal
planar motif; navy tetrahedra decorate every sp³ atom whose four
neighbours form a 109.5° tetrahedron.  Drag any panel to orbit
manually.

<iframe src="../../_static/overview/carbon.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

Stacked g(r) per regime — most sp²-dominant curve at the bottom, most
sp³-dominant at the top.  The pair dropdown below the plot lets you
switch between the sp²-C and sp³-C channels:

<iframe src="../../_static/g2_compare/carbon.html"
        width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Reference crystals

```python
from ase.io import read

atoms_graphite = read("docs/structures/C_graphite.cif")  # P6₃/mmc, a=2.467 Å, c=6.708 Å
atoms_diamond  = read("docs/structures/C_diamond.cif")   # Fd-3m,  a=3.561 Å
```

## Composite shell target

Carbon uses a **composite shell target** — one `CoordinationShellTarget`
per chemistry, stacked into a single object with two virtual species
(``sp2_C`` and ``sp3_C``) that share atomic number 6 but carry
distinct coordination + bond-angle targets:

```python
import tricor as tc

shell_sp2 = tc.CoordinationShellTarget.from_atoms(atoms_graphite, phi_num_bins=90)
shell_sp3 = tc.CoordinationShellTarget.from_atoms(atoms_diamond,  phi_num_bins=90)
shell_target = tc.CoordinationShellTarget.from_targets(
    {"sp2": shell_sp2, "sp3": shell_sp3}
)
```

The relaxer consults each atom's **virtual species index** (assigned
per grain during construction) so sp² atoms develop 3 bonds at 120°
and sp³ atoms develop 4 bonds at 109.5° — inside the same cell.

## Grain-level sp²/sp³ mixing

Every regime is nanocrystalline (multi-grain Voronoi).  Each grain is
sampled from graphite or diamond by the regime's ``(w_graphite,
w_diamond)`` weights:

```python
cell.generate(
    shell_target,
    grain_size=10.0,
    grain_sources=[
        {"atoms": atoms_graphite, "species_offset": 0, "weight": 0.4},
        {"atoms": atoms_diamond,  "species_offset": 1, "weight": 0.6},
    ],
    num_steps=120,
    bond_weight=2.0, angle_weight=1.0, repulsion_weight=2.0,
    hard_core_scale=0.9, nonbond_push_scale=0.8,
    displacement_sigma=0.03,
)
```

Atom count scales naturally with the regime's phase mix — diamond is
denser than graphite (0.177 vs 0.098 atoms/Å³), so diamond-dominant
regimes carry more atoms at the same box size.

## Disorder regimes

Click any regime for the full interactive trajectory viewer and g3
distribution.

```{toctree}
:maxdepth: 1

graphite
sp2_rich
sp2_leaning
sp3_leaning
sp3_rich
diamond
```

## Preset summary

| Regime | w_graphite | w_diamond | grain_size (Å) | num_steps |
|---|---|---|---|---|
| `graphite_nc`  | 1.00 | 0.00 | 10.0 | 120 |
| `sp2_rich`     | 0.80 | 0.20 | 10.0 | 120 |
| `sp2_leaning`  | 0.60 | 0.40 | 10.0 | 120 |
| `sp3_leaning`  | 0.40 | 0.60 | 10.0 | 120 |
| `sp3_rich`     | 0.20 | 0.80 | 10.0 | 120 |
| `diamond_nc`   | 0.00 | 1.00 | 10.0 | 120 |

Shell-relax weights are identical across regimes:
``bond_weight=2.0, angle_weight=1.0, repulsion_weight=2.0,
hard_core_scale=0.9, nonbond_push_scale=0.8, displacement_sigma=0.03``.
