# Generating Order Variety

Generate a full spectrum of supercells, from fully disordered liquid to
nanocrystalline, from a single reference crystal. The pattern below is a
good starting point for studying how the g3 distribution evolves as
structural order increases.

The pattern on this page uses the default full-FIRE pipeline at 40³ Å
(~5 k atoms per regime).  For near-DFT accuracy, relax the generated
cells with [MACE-MP0 refinement](examples_mace/index.md) instead of
FIRE.

## Setup

```python
from ase.io import read
import atomode as am

file_cif = 'Si.cif'
cell_dim_angstroms = (40, 40, 40)
r_max = 20
r_step = 0.05
phi_num_bins = 90
movie_file_name_base = 'structure_'

atoms = read(file_cif, index=0)
shell_target = am.CoordinationShellTarget.from_atoms(
    atoms,
    phi_num_bins=phi_num_bins,
)
```

## Generate all disorder regimes

```python
cases = [
    ("liquid", dict(
        num_steps=100,
        grain_size=None,
        bond_weight=0.4,
        angle_weight=0.5,
        repulsion_weight=0.5,
        hard_core_scale=0.75,
        nonbond_push_scale=0.7,
    )),
    ("amorphous", dict(
        num_steps=150,
        grain_size=6.0,
        bond_weight=1.2,
        angle_weight=0.6,
        repulsion_weight=1.5,
        hard_core_scale=0.9,
        nonbond_push_scale=0.5,
        displacement_sigma=0.08,
    )),
    ("SRO", dict(
        num_steps=200,
        grain_size=10.0,
        bond_weight=2.2,
        angle_weight=1.0,
        repulsion_weight=2.0,
        hard_core_scale=0.95,
        nonbond_push_scale=0.6,
        displacement_sigma=0.04,
    )),
    ("MRO", dict(
        num_steps=150,
        grain_size=13.0,
        bond_weight=1.9,
        angle_weight=0.9,
        repulsion_weight=2.5,
        hard_core_scale=0.95,
        nonbond_push_scale=0.7,
        displacement_sigma=0.04,
    )),
    ("LRO", dict(
        num_steps=150,
        grain_size=18.0,
        bond_weight=2.0,
        angle_weight=1.0,
        hard_core_scale=0.95,
        nonbond_push_scale=0.9,
        displacement_sigma=0.04,
    )),
    ("nanocrystalline", dict(
        num_steps=150,
        grain_size=20.0,
        bond_weight=3.0,
        angle_weight=1.5,
        displacement_sigma=0.02,
    )),
]

cells = {}
for idx, (name, kw) in enumerate(cases, start=1):
    print(f"{idx:02d} - {name}")
    cell = am.Supercell.from_atoms(
        atoms,
        cell_dim_angstroms=cell_dim_angstroms,
        r_max=r_max,
        r_step=r_step,
        phi_num_bins=phi_num_bins,
        rng_seed=42,
    )
    cell.generate(shell_target, **kw)
    cell.measure_g3()
    cells[name] = cell
```

## View g3 distributions

```python
for name, cell in cells.items():
    print(f"\n--- {name} ---")
    display(cell.plot_g3())
```

## Render movies

```python
for idx, (name, cell) in enumerate(cells.items(), start=1):
    cell.plot_structure(
        output=f"{movie_file_name_base}{idx:02d}_{name}.mp4",
        fps=60,
        duration=6.0,
        width=512,
        height=512,
    )
    print(f"  -> {movie_file_name_base}{idx:02d}_{name}.mp4")
```

## Using presets

```python
cell = am.Supercell.from_atoms(
    atoms,
    (40, 40, 40),
    rng_seed=42,
)
cell.generate(shell_target, **am.Supercell.PRESETS["MRO"])
cell.measure_g3()
cell.plot_g3()
```
