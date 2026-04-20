# Quick Start

## Installation

```bash
git clone https://github.com/ophusgroup/tricor.git
cd tricor
uv sync
```

## Minimal example

Generate a silicon MRO supercell, inspect its three-body distribution,
and open the interactive 3D viewer:

```python
from ase.build import bulk
import tricor as tc

# 1. Reference crystal and first-shell target
atoms = bulk("Si", "diamond", a=5.431)
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

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

# 5. Interactive 3D viewer (Jupyter) — blue Si tetrahedra by default
cell.view_structure()
```

## Presets

`Supercell.PRESETS` provides tuned keyword dictionaries for silicon in
six disorder regimes.  Expand any entry directly into `generate`:

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
| `nanocrystalline` | 20 | Single coherent grain filling a 20 Å box. |

See the [preset summary table](examples/silicon/index.md#preset-summary)
on the silicon examples page for the full parameter values.

## Multi-species materials

For binary / ternary materials the default `CoordinationShellTarget`
allows bonds between every species pair, which lets `shell_relax`
develop spurious second-shell bonds (e.g. Si-Si in SiO₂, Ti-Ti in
SrTiO₃).  Restrict bonds to the real chemical connections before
calling `generate`:

```python
# SiO2: every bond is cross-species (Si-O)
shell_target = (
    tc.CoordinationShellTarget.from_atoms(atoms_sio2, phi_num_bins=90)
    .with_cross_species_bonds_only()
)

# SrTiO3: only Ti-O is a real bond (Sr is an ionic spectator)
shell_target = (
    tc.CoordinationShellTarget.from_atoms(atoms_sto, phi_num_bins=90)
    .with_bonded_species_pairs([("Ti", "O")])
)
```

## Regime-ladder comparison

Building the same material across every preset and comparing the
results side-by-side is a standard tricor workflow:

```python
cells = {}
for name in ["liquid", "amorphous", "SRO", "MRO", "MRO_more", "nanocrystalline"]:
    c = tc.Supercell.from_atoms(atoms, cell_dim_angstroms=(20, 20, 20),
                                r_max=10, r_step=0.1, phi_num_bins=90,
                                rng_seed=42)
    c.generate(shell_target, **tc.Supercell.PRESETS[name])
    cells[name] = c

# Overlaid g(r) stack — most disordered bottom, most ordered top
tc.plot_g2_compare(cells, r_max=8.0, title="Silicon regime ladder")

# Synchronised rotating 3D grid
tc.export_overview_html("overview.html", list(cells.items()))
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
cell.generate(shell_target, capture_trajectory=True, **tc.Supercell.PRESETS["MRO"])

cell.export_trajectory_html("mro_trajectory.html")
cell.export_g3_html("mro_g3.html")
cell.export_g2_html("mro_g2.html")
```

See the [Visualization](visualization/index.md) section for the full
set of viewers (3D structure, rotating movies, trajectory playback,
multi-panel overview, g(r), g3).

## Next steps

- [Examples](examples/index.md): case studies across materials, with
  interactive viewers embedded.
- [Generating order variety](order_variety.md): batch generation of
  every disorder regime for a single material.
- [Algorithms](algorithms/index.md): mathematical details of grain
  construction, shell relaxation, and target-g3 construction.
- [API reference](api/index.md): every public class and function.
