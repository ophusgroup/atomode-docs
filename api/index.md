# API Reference

Top-level overview of every public symbol exported from ``atomode``,
with full signatures, parameter docs, and return types pulled
straight from the source docstrings.

## Public module surface

```
.. currentmodule:: atomode
```

| Symbol | Kind | Purpose |
|---|---|---|
| `Supercell` | class | Central disorder-generator with visualisation + export helpers. |
| `CoordinationShellTarget` | class | First-shell coordination + angle targets extracted from a reference crystal.  Composable via `CoordinationShellTarget.from_targets` into phase blends (e.g. sp²/sp³ carbon). |
| `G3Distribution` | class | Stand-alone three-body g3 measurement + pairwise g2 byproduct. |
| `export_overview_html` | function | Rotating multi-panel 3D grid of finished supercells. |
| `export_g2_compare_html` | function | Overlaid g(r) across multiple supercells, stacked y-offset, species-pair dropdown. |
| `plot_g2_compare` | function | Inline-Jupyter wrapper around `export_g2_compare_html`. |

## Pipeline summary

A typical end-to-end build chains four calls:

```python
import atomode as am
from ase.build import bulk

atoms_ref = bulk("Si", "diamond", a=5.431)
shell = am.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)

cell = am.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell, **am.Supercell.PRESETS["MRO"])
cell.measure_g3()
```

After `Supercell.generate` the cell carries:

- ``cell.atoms``: the ASE ``Atoms`` object with periodic positions.
- ``cell.shell_relax_history``: per-step bond / angle / repulsion
  losses, FIRE trajectory, and (optionally) per-atom cost vectors.
- ``cell.refine_initial_orientations_history``: only populated when
  ``refine_orientations=True`` is passed; one entry per accepted
  rotation.
- ``cell.current_distribution``: the most recently measured
  `G3Distribution` (set by `Supercell.measure_g3`).

From there the visualisation methods (`Supercell.plot_g3`,
`Supercell.view_structure`, `Supercell.plot_shell_relax`)
render inline in Jupyter, and the export methods
(`Supercell.export_trajectory_html`,
`Supercell.export_g3_html`,
`Supercell.export_g2_html`) write self-contained HTML for
embedding in static sites or sharing as standalone files.
