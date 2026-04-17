# Generating Order Variety

Generate a full spectrum of supercells - from fully disordered liquid to
nanocrystalline - from a single reference crystal. The pattern below is a
good starting point for building training sets for machine-learning
potentials or for studying how the g3 distribution evolves as structural
order increases.

## Setup

```python
from ase.io import read
import tricor as tc

file_cif = 'Si.cif'
cell_dim_angstroms = (40, 40, 40)
r_max = 20
r_step = 0.05
phi_num_bins = 90
movie_file_name_base = 'structure_'

atoms = read(file_cif, index=0)
shell_target = tc.CoordinationShellTarget.from_atoms(
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
    ("MRO_more", dict(
        num_steps=150,
        grain_size=18.0,
        bond_weight=2.0,
        angle_weight=1.0,
        hard_core_scale=0.95,
        nonbond_push_scale=0.9,
        displacement_sigma=0.04,
    )),
    ("nanocrystalline_10", dict(
        num_steps=200,
        grain_size=15.0,
        bond_weight=2.8,
        angle_weight=1.3,
        displacement_sigma=0.02,
    )),
    ("nanocrystalline_20", dict(
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
    cell = tc.Supercell.from_atoms(
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
cell = tc.Supercell.from_atoms(
    atoms,
    (40, 40, 40),
    rng_seed=42,
)
cell.generate(shell_target, **tc.Supercell.PRESETS["MRO"])
cell.measure_g3()
cell.plot_g3()
```

## SiC binary example

The presets above are tuned for monatomic silicon, but the same workflow
applies unchanged to binary and higher-species systems. Below is an MRO
supercell of zincblende silicon carbide:

```python
from ase.build import bulk

atoms_sic = bulk("SiC", "zincblende", a=4.36)
shell_target_sic = tc.CoordinationShellTarget.from_atoms(
    atoms_sic,
    phi_num_bins=90,
)

cell_sic = tc.Supercell.from_atoms(
    atoms_sic,
    cell_dim_angstroms=(30, 30, 30),
    r_max=10,
    r_step=0.2,
    phi_num_bins=90,
    rng_seed=42,
)
cell_sic.generate(shell_target_sic, **tc.Supercell.PRESETS["MRO"])
cell_sic.measure_g3()
cell_sic.plot_g3()
```

The per-species-pair coordination targets (e.g. Si-C = 4, Si-Si = 0 in
zincblende) are handled automatically by `CoordinationShellTarget`.
