# Visualization

tricor provides several ways to visualise supercells and their g3 distributions.

```{toctree}
:maxdepth: 1

g3_explorer
g3_comparison
structure_viewer
rotating_movie
relaxation_history
```

## At a glance

| Method | Use case | Interactive |
|--------|----------|-------------|
| `plot_g3()` | Browse the measured g3 in a 2D heatmap with a radial profile | Yes (Jupyter) |
| `plot_g3_compare()` | Side-by-side comparison of the supercell vs a target | Yes (Jupyter) |
| `view_structure()` | 3D WebGL atom/bond viewer with slab clipping | Yes (Jupyter) |
| `plot_structure()` | Rotating MP4 or GIF movie | No (file output) |
| `plot_shell_relax()` | Matplotlib loss history from shell_relax | No (static plot) |
