# Quick Start

## Installation

```bash
git clone https://github.com/ophusgroup/tricor.git
cd tricor
uv sync
```

## Minimal example

```python
from ase.build import bulk
import tricor as tc

# 1. Reference crystal
atoms = bulk('Si', 'diamond', a=5.431)
shell_target = tc.CoordinationShellTarget.from_atoms(
    atoms,
    phi_num_bins=90,
)

# 2. Create supercell
cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10,
    r_step=0.1,
    phi_num_bins=90,
    relative_density=0.96,
    rng_seed=42,
)

# 3. Generate structure (medium-range order example)
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=13.0,
    bond_weight=1.9,
    angle_weight=0.9,
    repulsion_weight=2.5,
    hard_core_scale=0.95,
    nonbond_push_scale=0.7,
    displacement_sigma=0.04,
)

# 4. Measure and view g3
cell.measure_g3()
cell.plot_g3()

# 5. Interactive 3D viewer
cell.view_structure()

# 6. Export movie
cell.plot_structure(output='structure.mp4')
```

## Using presets

Recommended parameter sets for Si are available as `Supercell.PRESETS`:

```python
cell = tc.Supercell.from_atoms(
    atoms,
    (40, 40, 40),
    rng_seed=42,
)
cell.generate(shell_target, **tc.Supercell.PRESETS["MRO"])
```

Available presets: `liquid`, `amorphous`, `SRO`, `MRO`, `MRO_more`, `nanocrystalline_10`, `nanocrystalline_20`.

## Accessing the structure

After `generate()`, the ASE Atoms object is available at `cell.atoms`:

```python
cell.atoms.write('supercell.cif')
cell.atoms.write('supercell.xyz')

positions = cell.atoms.positions      # (N, 3) array
numbers = cell.atoms.numbers          # (N,) array of atomic numbers
cell_matrix = cell.atoms.cell.array   # (3, 3) cell vectors
```

## Next steps

- See [Examples](examples/index.md) for full case studies of 4 different materials.
- See [Generating Order Variety](order_variety.md) for generating all 7 disorder regimes at once.
- See [Algorithms](algorithms/index.md) for the mathematical details.
