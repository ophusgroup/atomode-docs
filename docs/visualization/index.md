# Visualization

tricor's visualisers come in two complementary flavours:

- **Jupyter widgets** (`plot_g3`, `plot_g3_compare`, `plot_g2`,
  `plot_g2_compare`, `view_structure`) render directly in a notebook
  with live sliders, checkboxes, and species-pair dropdowns.
- **Self-contained HTML exporters** (`export_trajectory_html`,
  `export_g3_html`, `export_g2_html`, `export_g2_compare_html`,
  `export_overview_html`) bake a single structure, trajectory, or
  group of structures into one HTML file that can be opened in any
  browser or embedded in Sphinx docs via ``<iframe>``.  No server, no
  build step. The pages load Three.js from a CDN at view time.

A static PNG / MP4 / GIF exporter (`plot_structure`) and the matplotlib
loss-history plot (`plot_shell_relax`) are also documented below.

```{toctree}
:maxdepth: 1

structure_viewer
rotating_movie
trajectory_viewer
overview_viewer
relaxation_history
g2_viewer
g3_explorer
g3_comparison
g3_static
```

## At a glance

| Method | Output | Purpose |
|---|---|---|
| `cell.view_structure()` | Jupyter widget | 3D WebGL atom viewer.  Polyhedra (triangles / tetrahedra / octahedra / cuboctahedra) drawn by default for recognised materials, with live sliders for radial + angular tolerance; bonds optional; perspective / orthographic toggle. |
| `cell.plot_structure(output=...)` | MP4 / GIF / PNG | Rotating movie or static still for publication figures. |
| `cell.export_trajectory_html(path)` | HTML file | Play back the shell-relaxation trajectory in 3D, colour-coded by per-atom spring energy; supports single- or **multi-group** polyhedra overlay (e.g. sp² triangles + sp³ tetrahedra in the same carbon cell). |
| `tricor.export_overview_html(path, cells)` | HTML file | Multiple structures rendered side-by-side with synchronised rotation; same `polyhedra_groups=` support as the trajectory exporter. |
| `cell.plot_shell_relax()` | matplotlib figure | Loss-history plot from the last `generate()` or `shell_relax()` call. |
| `cell.plot_g2()` | Jupyter widget (iframe) | Single-cell g(r) viewer with species-pair dropdown + overlay-all-pairs mode. |
| `cell.export_g2_html(path)` | HTML file | Standalone g(r) viewer with species-pair dropdown + overlay-all-pairs. |
| `tricor.plot_g2_compare(cells)` | Jupyter widget (iframe) | Overlaid g(r) from multiple supercells, stacked with inline per-series labels. |
| `tricor.export_g2_compare_html(cells, path)` | HTML file | Standalone version of the compare viewer for docs embedding. |
| `cell.plot_g3()` | Jupyter widget | Browse the measured g3 as a 2D heatmap with a radial profile. |
| `cell.plot_g3_compare()` | Jupyter widget | Side-by-side comparison of the supercell against a target. |
| `cell.export_g3_html(path)` | HTML file | RdBu heatmap + pair profile g(r) of the measured g3 (single triplet or all-triplets grid). |
