# Visualization

tricor provides two families of visualisers:

- **Jupyter widgets** (`plot_g3`, `plot_g3_compare`, `view_structure`) render
  directly in a notebook with live controls.
- **Self-contained HTML exporters** (`export_trajectory_html`,
  `export_g3_html`, `export_overview_html`) bake a structure, trajectory, or
  set of structures into a single HTML file that can be opened in any
  browser or embedded in documentation.

The static PNG, MP4, and GIF exporter (`plot_structure`) and the matplotlib
loss history (`plot_shell_relax`) are also documented below.

```{toctree}
:maxdepth: 1

g3_explorer
g3_comparison
structure_viewer
trajectory_viewer
g3_static
overview_viewer
rotating_movie
relaxation_history
```

## At a glance

| Method | Output | Purpose |
|---|---|---|
| `cell.plot_g3()` | Jupyter widget | Browse the measured g3 as a 2D heatmap with a radial profile. |
| `cell.plot_g3_compare()` | Jupyter widget | Side-by-side comparison of the supercell against a target. |
| `cell.view_structure()` | Jupyter widget | 3D WebGL atom / bond viewer with slab clipping. |
| `cell.export_trajectory_html(path)` | HTML file | Play back the shell-relaxation trajectory in 3D, colour-coded by per-atom cost. |
| `cell.export_g3_html(path)` | HTML file | Static RdBu heatmap + pair-profile plot of the measured g3. |
| `tricor.export_overview_html(path, cells)` | HTML file | Multiple structures rendered side-by-side with synchronised rotation. |
| `cell.plot_structure(output=...)` | MP4 / GIF / PNG | Rotating movie or static still for publication figures. |
| `cell.plot_shell_relax()` | matplotlib figure | Loss-history plot from the last `generate()` or `shell_relax()` call. |
