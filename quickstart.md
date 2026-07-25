# Quick Start

## Installation

```bash
pip install atomode
```

Or to install the development checkout:

```bash
git clone https://github.com/ophusgroup/atomode.git
cd atomode
uv sync                # or: pip install -e '.[test]'
```

`atomode` requires Python ≥ 3.10.  ``numba`` is a hard dependency
(installed automatically) and powers both the parallel ``measure_g3``
kernel and the ``thermal_relax`` / grain-orientation-refinement
features.

## Minimal example

Generate a silicon MRO supercell, inspect its three-body distribution,
and open the interactive 3D viewer:

```python
from ase.build import bulk
import atomode as am

# 1. Reference crystal and first-shell target
atoms = bulk("Si", "diamond", a=5.431)
shell_target = am.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

# 2. Create the empty supercell
cell = am.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10,
    r_step=0.1,
    phi_num_bins=90,
    rng_seed=42,
)

# 3. Generate a medium-range-order structure
cell.generate(shell_target, **am.Supercell.PRESETS["MRO"])

# 4. Measure and view the three-body distribution
cell.measure_g3()
cell.plot_g3()

# 5. Interactive 3D viewer (Jupyter); blue Si tetrahedra by default
cell.view_structure()
```

## Presets

`Supercell.PRESETS` provides tuned keyword dictionaries for silicon in
six disorder regimes.  Expand any entry directly into `generate`:

```python
cell.generate(shell_target, **am.Supercell.PRESETS["MRO"])
```

Available keys, in order of increasing structural order:

| Preset | Grain size (Å) | Notes |
|---|---|---|
| `liquid` | - | No grains; fully random starting positions. |
| `amorphous` | 6 | Short-range tetrahedral network with 6 Å grains. |
| `SRO` | 10 | Short-range order. |
| `MRO` | 13 | Medium-range order. |
| `LRO` | 18 | Long-range order. |
| `nanocrystalline` | 20 | Few large grains per cell (≈ 8 grains in a 40 Å cube). |

See the [preset summary table](examples/silicon/index.md#preset-summary)
on the silicon examples page for the full parameter values.

## Multi-species materials

For binary / ternary materials, `from_atoms` keeps only the real
chemical bonds: species pairs whose first-shell peak is a lattice
separation through a bridging atom (Si-Si in SiO₂, Ti-Ti in SrTiO₃)
are zeroed automatically (`auto_filter_lattice_artifacts=True`), so
`shell_relax` cannot develop spurious second-shell bonds.
`with_cross_species_bonds_only()` and `with_bonded_species_pairs(...)`
set the bond graph explicitly when the automatic rule is not what
you want.

Multi-modal shells need an explicit angle whitelist.  In SrTiO₃ the
SrO₁₂ cuboctahedron has O-Sr-O modes at 60°/90°/120°/180° — no single
target angle fits — so keep only the single-mode Ti-centred 90° and
Ti-O-Ti 180° springs:

```python
shell_target = (
    am.CoordinationShellTarget.from_atoms(atoms_sto, phi_num_bins=90)
    .with_angle_triplets([("Ti", "O", "O"), ("O", "Ti", "Ti")])
)
```

## Phase blends (sp²/sp³ carbon, etc.)

For materials with a controllable phase mix (sp² ↔ sp³ carbon, a
polymer/ceramic boundary, etc.), extract one shell target per
chemistry and combine them with `from_targets`:

```python
from ase.io import read
atoms_g = read("docs/structures/C_graphite.cif")
atoms_d = read("docs/structures/C_diamond.cif")

shell_sp2 = am.CoordinationShellTarget.from_atoms(atoms_g, phi_num_bins=90)
shell_sp3 = am.CoordinationShellTarget.from_atoms(atoms_d, phi_num_bins=90)
shell_target = am.CoordinationShellTarget.from_targets(
    {"sp2": shell_sp2, "sp3": shell_sp3},
)

# 50/50 graphite/diamond grains, assigned at Voronoi-grain time
cell.generate(
    shell_target,
    grain_size=10.0,
    grain_sources=[
        {"atoms": atoms_g, "species_offset": 0, "weight": 0.5},  # sp²
        {"atoms": atoms_d, "species_offset": 1, "weight": 0.5},  # sp³
    ],
    num_steps=120, bond_weight=2.0, angle_weight=1.0,
    repulsion_weight=2.0, hard_core_scale=0.9,
    nonbond_push_scale=0.8, displacement_sigma=0.03,
)
```

Each atom inherits a virtual-species index (0 = sp², 1 = sp³) from
its grain, and the relaxer pulls each atom toward the coordination +
angle target of its source chemistry.  See the
[Carbon example](examples/carbon/index.md) for the full regime
ladder.

## Regime-ladder comparison

Building the same material across every preset and comparing the
results side-by-side is a standard atomode workflow:

```python
cells = {}
for name in ["liquid", "amorphous", "SRO", "MRO", "LRO", "nanocrystalline"]:
    c = am.Supercell.from_atoms(atoms, cell_dim_angstroms=(40, 40, 40),
                                r_max=10, r_step=0.1, phi_num_bins=90,
                                rng_seed=42)
    c.generate(shell_target, **am.Supercell.PRESETS[name])
    cells[name] = c

# Overlaid g(r) stack (most disordered bottom, most ordered top)
am.plot_g2_compare(cells, r_max=8.0, title="Silicon regime ladder")

# Synchronised rotating 3D grid
am.export_overview_html("overview.html", list(cells.items()))
```

## Accessing the structure

After `generate()`, the ASE `Atoms` object is at `cell.atoms`:

```python
cell.atoms.write("supercell.cif")

positions   = cell.atoms.positions      # (N, 3)
numbers     = cell.atoms.numbers        # (N,)
cell_matrix = cell.atoms.cell.array     # (3, 3)
```

## Exporting interactive HTML

Every visualiser has a standalone-HTML counterpart that bakes the scene
into one file; no server is required to view it.

```python
# Trajectory playback needs capture_trajectory=True during generate()
cell.generate(shell_target, capture_trajectory=True, **am.Supercell.PRESETS["MRO"])

cell.export_trajectory_html("mro_trajectory.html")
cell.export_g3_html("mro_g3.html")
cell.export_g2_html("mro_g2.html")
```

See the [Visualization](visualization/index.md) section for the full
set of viewers (3D structure, rotating movies, trajectory playback,
multi-panel overview, g(r), g3).

## Next steps

- [Static Examples](examples/index.md): case studies across materials, with
  interactive viewers embedded.
- [Generating order variety](order_variety.md): batch generation of
  every disorder regime for a single material.
- [Algorithms](algorithms/index.md): mathematical details of grain
  construction, shell relaxation, and target-g3 construction.
- [API reference](api/index.md): every public class and function.
