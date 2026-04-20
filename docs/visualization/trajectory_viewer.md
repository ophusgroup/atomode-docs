# Trajectory Viewer

Export the full shell-relaxation trajectory as a self-contained HTML file
with interactive playback.

## Capturing the trajectory

Per-step positions and a per-atom cost history are only stored if
`capture_trajectory=True` is passed through to `shell_relax`:

```python
cell.generate(
    shell_target,
    capture_trajectory=True,
    **tc.Supercell.PRESETS["MRO"],
)
cell.export_trajectory_html("mro_trajectory.html")
```

The trajectory is stored on `cell.shell_relax_history["trajectory"]`
(shape `(num_steps + 1, num_atoms, 3)`, float32) and the per-atom cost on
`cell.shell_relax_history["atom_cost"]` (shape `(num_steps + 1, num_atoms)`).

## Features

- **Playback controls**: play / pause, restart, loop, bounce (ping-pong),
  speed slider, and a frame scrubber.
- **Per-atom cost colouring**: atoms and bonds are coloured through the
  Turbo colormap by each atom's accumulated spring-network cost at that
  frame. The colour range is frozen for the whole trajectory and is shown
  as a vertical legend to the right of the canvas. Bonds take the mean
  cost of their two endpoints.
- **Cartoon shading**: shiny Phong atoms and toon-shaded bonds, each with a
  thin black back-face outline so that individual atoms and bonds stay
  crisp against the structural background.
- **Periodic-image bond wrapping**: bond cylinders use the minimum-image
  displacement across periodic boundaries.
- **Pointer interaction**: drag to rotate, scroll to zoom.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `output_path` | required | File path for the generated HTML. |
| `bond_cutoff` | from `shell_target` | Maximum bond length in Å. Defaults to `shell_target.pair_peak.max() × 1.2`. |
| `atom_scale` | 0.32 | Multiplier on each atom's covalent radius. |
| `bond_radius` | 0.06 | Bond cylinder radius in Å. |
| `background_color` | `"#f7f8f5"` | CSS colour for the viewer background. |
| `title` | `""` | Optional text shown at the top of the viewer. |
| `tetrahedra` / `octahedra` / `cuboctahedra` | `None` | Single-group polyhedra overlay (supersedes bonds). Detector dict with `center_symbol`, `vertex_symbol`, `bond_length`, `bond_length_tol`, `ideal_angle_deg`, `angle_tol_deg`, `scale`. |
| `polyhedra_groups` | `None` | Multi-group polyhedra list (sp²/sp³ carbon blends etc.). Same entry shape as `export_overview_html`; each dict may carry a `virtual_species` filter keyed to `Supercell._atom_shell_species_index`. Suppresses bonds automatically. |
| `show_bonds` | `None` | Auto-picks: `True` when no polyhedra are requested, `False` when the legacy single-group or `polyhedra_groups` is set. |

## Embedding in documentation

The file is fully self-contained and loads Three.js from a CDN, so it can
be dropped into a Sphinx docs tree and embedded with a plain `<iframe>`:

```html
<iframe src="../_static/trajectories/mro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
```
