# 3D Structure Viewer

Interactive WebGL viewer in Jupyter, built on Three.js via
[anywidget](https://anywidget.dev).

```python
cell.view_structure()
```

## Default behaviour

For recognised materials (Si / C, Cu, SiO₂, SrTiO₃, …) the viewer
picks a coordination polyhedron and renders it as a translucent mesh
around every atom whose first shell passes the detector, with no bond
cylinders by default:

| Species | Polyhedron | Centre-vertex bond | Scale |
|---|---|---|---|
| Si / C (diamond) | tetrahedron | 2.35 / 1.54 Å (self) | 0.5 (vertices at bond midpoints) |
| C (graphite, sp²) | triangle (3-sub-triangle fan, 120°) | 1.42 Å (self) | 0.5 |
| Cu | cuboctahedron (FCC 12-coord) | 2.56 Å (self) | 0.5 |
| SiO₂ | SiO₄ tetrahedron | 1.61 Å (Si → O) | 1.0 |
| SrTiO₃ | TiO₆ octahedron | 1.96 Å (Ti → O) | 1.0 |

For **blended materials** (sp²/sp³ carbon; SiO₂/Si₃N₄ mixes, …) pass
`polyhedra_groups=[...]` to `export_overview_html` or
`export_trajectory_html`. Each entry carries its own `kind`
(``triangles``, ``tetrahedra``, ``octahedra``, ``cuboctahedra``),
colour, opacity, and an optional `virtual_species` filter that
restricts detection to atoms flagged with that shell-target species
index.  See [Carbon](../examples/carbon/index.md) for a worked
example where green sp²-C triangle fans and navy sp³-C tetrahedra
render in the same scene.

Override with the ``polyhedra=`` kwarg:

```python
# Explicit kind + tolerances
cell.view_structure(polyhedra={
    'kind': 'octahedra',
    'center_symbol': 'Ti', 'vertex_symbol': 'O',
    'bond_length': 1.96, 'bond_length_tol': 0.15,
    'angle_tol_deg': 18.0, 'scale': 1.0,
})

# Disable polyhedra, show bonds instead
cell.view_structure(polyhedra=False, show_bonds=True)
```

## Live controls

All sliders recompute on release, pushing the result back through the
anywidget traitlet bridge so the 3D scene updates without a full
rebuild:

- **Drag** to rotate, **scroll** to zoom, **right-click drag** to pan.
- **Atom size** – sphere radius scale factor (default 0.2).
- **Bond radius** / **bond cutoff** – when bonds are shown.
- **Bond type checkboxes** – per species-pair visibility.
- **Polyhedra controls** – a group of four sliders (shown when the
  polyhedra kind has been auto-detected or explicitly set):
  - **bond length (Å)** – radial centre of the first-shell window;
    dragging this moves the polyhedra in and out as more / fewer atoms
    pass the distance test.
  - **radial tolerance (fraction)** – 2 % – 40 %; widens the accepted
    band around `bond_length`.
  - **angle tolerance (°)** – 1° – 45°; controls how much the local
    shell can deviate from the ideal polyhedral angles (109.47° for
    tets, 90° for octahedra, FCC spectrum for cuboctahedra).
  - **polyhedra scale** – 0.2 – 1.0; shrinks the rendered polyhedron
    toward its centre.  `scale=0.5` places vertices at bond midpoints
    (natural for single-species cases where the "vertices" are just
    neighbouring atoms); `scale=1.0` sits vertices on the neighbour
    atoms themselves (natural for cation-anion motifs like SiO₄).
  - **polyhedra opacity** – 0.05 – 0.95 (default 0.2).
- **Slab x / y / z** dual-range sliders – clip the view to a fractional
  coordinate range.
- **Show cell / Show bonds / Show polyhedra** checkboxes – toggle each
  overlay independently; combinations are fine (e.g. polyhedra **and**
  bonds for debugging the first-shell detector).
- **Orthographic** checkbox – swaps between `PerspectiveCamera(fov=45°)`
  and an `OrthographicCamera` whose frustum is computed from the cube's
  bounding sphere.  Parallel lattice planes read as parallel in ortho
  mode, which makes cubic crystalline panels easier to interpret.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `polyhedra` | `True` (auto-pick) | Config dict; `True` / `None` auto-picks from species, `False` disables.  See table above for auto-pick rules. |
| `atom_scale` | 0.2 | Sphere radius scale factor (`covalent_radius × scale`). |
| `bond_cutoff` | from `shell_target.max_pair_outer` | Maximum bond length (Å). |
| `bond_radius` | 0.08 | Cylinder radius for bonds (Å). |
| `show_bonds` | **False** | Render bonds.  Auto-default flipped to False once polyhedra became the primary overlay. |
| `show_cell` | True | Render cell outline. |
| `orthographic` | False | Start in orthographic mode. |
| `slab_x`, `slab_y`, `slab_z` | `(0, 1)` | Fractional range to display. |

Colours come from ASE's jmol colour scheme; the polyhedra colour
defaults to a material-specific hint (blue for Si-tets, orange for
Ti-octa, copper-orange for Cu-cubocta, …).

## Example: silicon MRO

Here is the live widget as rendered from `tc.Supercell.PRESETS["MRO"]`
on Si at 40 × 40 × 40 Å. The blue tetrahedra mark Si atoms whose four
nearest neighbours pass the 109.5° / 2.35 Å first-shell filter, with
the tets shrunk to half-size so their corners meet at Si-Si bond
midpoints:

<iframe src="../_static/trajectories/si_mro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

(The embedded viewer above is the exported trajectory version; the
notebook `view_structure()` widget uses the same Three.js scene +
controls on a single final frame.)
