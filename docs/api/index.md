# API Reference

Top-level overview of every public symbol exported from ``tricor``,
with full signatures, parameter docs, and return types pulled
straight from the source docstrings.

```{toctree}
:maxdepth: 2

supercell
coordination_shell_target
g3_distribution
overview
```

## Public module surface

```{eval-rst}
.. currentmodule:: tricor
```

| Symbol | Kind | Purpose |
|---|---|---|
| {class}`Supercell` | class | Central disorder-generator with visualisation + export helpers. |
| {class}`CoordinationShellTarget` | class | First-shell coordination + angle targets extracted from a reference crystal.  Composable via {meth}`~CoordinationShellTarget.from_targets` into phase blends (e.g. sp²/sp³ carbon). |
| {class}`G3Distribution` | class | Stand-alone three-body g3 measurement + pairwise g2 byproduct. |
| {func}`export_overview_html` | function | Rotating multi-panel 3D grid of finished supercells. |
| {func}`export_g2_compare_html` | function | Overlaid g(r) across multiple supercells, stacked y-offset, species-pair dropdown. |
| {func}`plot_g2_compare` | function | Inline-Jupyter wrapper around {func}`export_g2_compare_html`. |

## Pipeline summary

A typical end-to-end build chains four calls:

```python
import tricor as tc
from ase.build import bulk

atoms_ref = bulk("Si", "diamond", a=5.431)
shell = tc.CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms_ref,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell, **tc.Supercell.PRESETS["MRO"])
cell.measure_g3()
```

After {meth}`~Supercell.generate` the cell carries:

- ``cell.atoms`` — the ASE ``Atoms`` object with periodic positions.
- ``cell.shell_relax_history`` — per-step bond / angle / repulsion
  losses, FIRE trajectory, and (optionally) per-atom cost vectors.
- ``cell.refine_initial_orientations_history`` — only populated when
  ``refine_orientations=True`` is passed; one entry per accepted
  rotation.
- ``cell.current_distribution`` — the most recently measured
  {class}`G3Distribution` (set by {meth}`~Supercell.measure_g3`).

From there the visualisation methods ({meth}`~Supercell.plot_g3`,
{meth}`~Supercell.view_structure`, {meth}`~Supercell.plot_shell_relax`)
render inline in Jupyter, and the export methods
({meth}`~Supercell.export_trajectory_html`,
{meth}`~Supercell.export_g3_html`,
{meth}`~Supercell.export_g2_html`) write self-contained HTML for
embedding in static sites or sharing as standalone files.
