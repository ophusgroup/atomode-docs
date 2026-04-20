# API Reference

```{toctree}
:maxdepth: 2

supercell
coordination_shell_target
g3_distribution
overview
```

## Public module surface

At a glance — the full list of symbols exposed from `tricor`:

| Symbol | Kind | Purpose |
|---|---|---|
| {class}`tricor.Supercell` | class | Central disorder-generator with visualisation + export helpers. |
| {class}`tricor.CoordinationShellTarget` | class | First-shell coordination + angle targets extracted from a reference crystal.  Composable via `from_targets` into phase blends (e.g. sp²/sp³ carbon). |
| {class}`tricor.G3Distribution` | class | Three-body g3 measurement + pairwise g2 byproduct. |
| {func}`tricor.export_overview_html` | function | Rotating multi-panel 3D grid of finished supercells. |
| {func}`tricor.export_g2_compare_html` | function | Overlaid g(r) across multiple supercells, stacked y-offset, species-pair dropdown. |
| {func}`tricor.plot_g2_compare` | function | Inline-Jupyter wrapper around {func}`export_g2_compare_html`. |
