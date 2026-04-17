# Quick Start

## Installation

```bash
git clone https://github.com/ophusgroup/tricor.git
cd tricor
uv sync
```

## Minimal example

Generate a silicon supercell using one of the built-in presets, inspect its
g3 distribution, and render a rotating movie:

```python
from ase.build import bulk
import tricor as tc

# 1. Reference crystal and first-shell target
atoms = bulk("Si", "diamond", a=5.431)
shell_target = tc.CoordinationShellTarget.from_atoms(
    atoms,
    phi_num_bins=90,
)

# 2. Create the empty supercell
cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10,
    r_step=0.1,
    phi_num_bins=90,
    rng_seed=42,
)

# 3. Generate a medium-range-order structure
cell.generate(shell_target, **tc.Supercell.PRESETS["MRO"])

# 4. Measure and view the three-body distribution
cell.measure_g3()
cell.plot_g3()

# 5. Interactive 3D viewer (Jupyter)
cell.view_structure()

# 6. Export a rotating MP4
cell.plot_structure(output="structure.mp4")
```

## Presets

Recommended parameter sets for silicon are available as
`Supercell.PRESETS`. Each value is a keyword dictionary that can be expanded
directly into `generate()`:

```python
cell.generate(shell_target, **tc.Supercell.PRESETS["MRO"])
```

Available keys, in order of increasing structural order:

| Preset | Grain seed (Å) | Notes |
|---|---|---|
| `liquid` | — | No grains; fully random starting positions. |
| `amorphous` | 6 | Short-range tetrahedral network. |
| `SRO` | 10 | Short-range order. |
| `MRO` | 13 | Medium-range order. |
| `MRO_more` | 18 | Extended medium-range order. |
| `nanocrystalline_10` | 15 | Nanocrystalline grains with well-defined boundaries. |
| `nanocrystalline_20` | 20 | Larger grains; the cell must be at least ~30 Å on each side. |

See the [preset summary table](examples/silicon/index.md#preset-summary) on
the silicon examples page for the full set of parameter values.

## Accessing the structure

After `generate()`, the ASE `Atoms` object is available at `cell.atoms`:

```python
cell.atoms.write("supercell.cif")
cell.atoms.write("supercell.xyz")

positions = cell.atoms.positions      # (N, 3) array
numbers = cell.atoms.numbers          # (N,) array of atomic numbers
cell_matrix = cell.atoms.cell.array   # (3, 3) cell vectors
```

## Exporting interactive HTML

Three self-contained HTML viewers can be generated from a supercell for use
in documentation, presentations, or web pages:

```python
# Captures per-step positions and per-atom cost during relaxation
cell.generate(shell_target, capture_trajectory=True, **tc.Supercell.PRESETS["MRO"])

cell.export_trajectory_html("mro_trajectory.html")
cell.export_g3_html("mro_g3.html")

# Side-by-side grid of multiple structures, synced rotation
tc.export_overview_html(
    "overview.html",
    [(cell, "MRO")],
)
```

Each file is a single HTML document that loads Three.js from a CDN; no
server is required to view it. See
[Trajectory viewer](visualization/trajectory_viewer.md),
[Static g3 viewer](visualization/g3_static.md), and
[Multi-cell overview](visualization/overview_viewer.md) for the full set of
options.

## Next steps

- [Examples](examples/index.md): case studies for several materials, with
  interactive trajectory and g3 viewers embedded.
- [Generating order variety](order_variety.md): batch generation of all
  disorder regimes for a single material.
- [Algorithms](algorithms/index.md): mathematical details of grain
  construction, shell relaxation, and target g3 construction.
- [API reference](api/index.md): every public class and function.
