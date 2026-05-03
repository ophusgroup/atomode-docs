# Multi-Cell Overview

Render a grid of finished structures side-by-side with synchronised
rotation. Useful for comparing how the same material looks across the full
disorder spectrum, or for showing several materials at once.

## Usage

```python
import tricor as tc

cells = []
for name in ["liquid", "amorphous", "SRO", "MRO",
             "LRO", "nanocrystalline"]:
    cell = tc.Supercell.from_atoms(atoms, (40, 40, 40), rng_seed=42)
    cell.generate(shell_target, **tc.Supercell.PRESETS[name])
    cells.append((cell, name))

tc.export_overview_html("silicon_overview.html", cells)
```

Each entry in `cells_and_labels` is a `(Supercell, label)` pair. Labels
are rendered as text badges in the top-left corner of each panel.

## Features

- **One WebGL context, many scenes**: each panel renders into its own
  viewport using `setScissor` / `setViewport`, so even six structures in
  one file stay responsive.
- **Synchronised rotation**: all panels share a single camera. The
  structure auto-rotates at ~14°/s. Dragging any panel pauses the spin and
  lets the user orbit manually; the spin resumes ~0.5 s after release.
- **Aspect-aware framing**: the camera distance is recomputed every frame
  to fit each cube's bounding sphere, so cubes stay in-frame whether the
  iframe is tall or wide.
- **Cartoon style**: ASE jmol colours for atoms, thin black outlines, red
  bonds.
- **Tetrahedral bond filter**: only bonds that sit inside
  ±`bond_length_tol` of the first-neighbour distance *and* whose 4 nearest
  neighbours subtend angles within `bond_angle_tol_deg` of
  `ideal_angle_deg` are drawn. Atoms that fail either test contribute no
  bonds, so disordered regimes naturally show fewer bonds than crystalline
  ones.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `output_path` | required | File path for the generated HTML. |
| `cells_and_labels` | required | Iterable of `(Supercell, label)` pairs. |
| `grid_cols` | 3 | Number of columns in the grid. Rows are inferred. |
| `atom_scale` | 0.18 | Multiplier on each atom's covalent radius. |
| `bond_radius` | 0.07 | Bond cylinder radius in Å. |
| `bond_color` | `(0.95, 0.1, 0.1)` | RGB bond colour in `[0, 1]`. |
| `background_color` | `"#f7f8f5"` | CSS colour for the viewport. |
| `title` | `""` | Unused; text should go in the surrounding page. |
| `subtitle` | `""` | Unused; text should go in the surrounding page. |
| `bond_cutoff_scale` | 1.2 | Bond search cutoff = `shell_target.pair_peak × bond_cutoff_scale`. |
| `max_bonds_per_atom` | 4 | Maximum bonds kept per atom before the angular filter. |
| `bond_length_tol` | 0.10 | Accept bonds within `±tol` of the ideal first-neighbour distance. |
| `ideal_angle_deg` | 109.47 | Ideal angle for the tetrahedral check (Si-like). |
| `bond_angle_tol_deg` | 18.0 | Maximum deviation of any pairwise angle from the ideal. |
| `tetrahedra` / `octahedra` / `cuboctahedra` | `None` | Single-group polyhedra config (one kind per scene). Dict of detector keys (`center_symbol`, `vertex_symbol`, `bond_length`, `bond_length_tol`, `ideal_angle_deg`, `angle_tol_deg`, `scale`). |
| `polyhedra_groups` | `None` | Multi-group polyhedra: list of dicts, each with a `kind` ∈ `{"triangles", "tetrahedra", "octahedra", "cuboctahedra"}` plus the single-group keys. Use for carbon-style sp²/sp³ blends where both triangles and tetrahedra must render in the same scene. |

For a non-tetrahedral material, set `ideal_angle_deg` and
`bond_angle_tol_deg` appropriately, or disable the angular filter by
setting `bond_angle_tol_deg` to a large value (e.g. 90).

(multi-group-polyhedra)=
## Multi-group polyhedra (carbon sp²/sp³)

For materials with a phase mix, pass a `polyhedra_groups` list so
each group runs its own detector and renders with its own colour.
Each group may also carry `virtual_species=N` to restrict detection
to atoms flagged with that shell-target species index (see
`Supercell.generate(..., grain_sources=...)`):

```python
tc.export_overview_html(
    "carbon_overview.html",
    cells,
    polyhedra_groups=[
        dict(kind="triangles",   center_symbol="C", vertex_symbol="C",
             bond_length=1.42, ideal_angle_deg=120.0, angle_tol_deg=22.0,
             virtual_species=0, scale=0.5,
             color=(0.25, 0.65, 0.35), opacity=0.85),   # sp² green
        dict(kind="tetrahedra",  center_symbol="C", vertex_symbol="C",
             bond_length=1.54, ideal_angle_deg=109.47, angle_tol_deg=22.0,
             virtual_species=1, scale=0.5,
             color=(0.20, 0.30, 0.75), opacity=0.65),   # sp³ navy
    ],
)
```

The `triangles` kind emits a 4-vertex motif ``[centre, j, k, l]``
rendered as three sub-triangles all anchored at the centre
(``(i, j, k)``, ``(i, k, l)``, ``(i, l, j)``), so the mesh always
touches the parent atom even at unequal bond lengths after relax.
