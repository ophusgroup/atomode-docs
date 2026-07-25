# Module-level exporters

Module-level helpers for rendering finished supercells into
self-contained HTML viewers that can be opened in any browser or
embedded via ``<iframe>``.  See
[Visualization](../visualization/index.md) for the high-level
descriptions and rendered examples.

#### `export_overview_html(output_path: 'str', cells_and_labels, *, grid_cols: 'int' = 3, atom_scale: 'float' = 0.17, bond_radius: 'float' = 0.07, bond_color=(0.95, 0.1, 0.1), background_color: 'str' = '#f7f8f5', title: 'str' = '', subtitle: 'str' = '', bond_cutoff_scale: 'float' = 1.2, max_bonds_per_atom: 'int' = 4, bond_length_tol: 'float' = 0.1, ideal_angle_deg: 'float' = 109.47, bond_angle_tol_deg: 'float' = 18.0, tetrahedra: 'dict | None' = None, tetrahedra_color=(0.35, 0.45, 0.95), tetrahedra_opacity: 'float' = 0.45, octahedra: 'dict | None' = None, octahedra_color=(0.95, 0.55, 0.25), octahedra_opacity: 'float' = 0.4, cuboctahedra: 'dict | None' = None, cuboctahedra_color=(0.55, 0.35, 0.85), cuboctahedra_opacity: 'float' = 0.4, polyhedra_groups: "'list[dict] | None'" = None) -> 'str'`

Export a 3D grid of supercells as a self-contained, auto-rotating HTML viewer.

Each panel renders the final atom positions of one
:class:`Supercell` using ASE element colours and black outlines.
All panels share a single auto-rotating camera; dragging any
panel pauses the rotation and lets the user orbit manually.
Bonds are rendered by default; passing one of the polyhedra
kwargs (``tetrahedra``, ``octahedra``, ``cuboctahedra``,
``polyhedra_groups``) replaces bonds with translucent polyhedra.

**Parameters**
output_path : str
    Filesystem path for the written HTML file.
cells_and_labels : list of (Supercell, str)
    Pairs of supercells and their panel-title labels, rendered
    left-to-right then top-to-bottom into a ``grid_cols``-wide
    grid.
grid_cols : int, optional
    Number of panels per row.  Default ``3``.
atom_scale : float, optional
    Multiplier applied to ASE covalent radii when sizing atom
    spheres.  Default ``0.17``.
bond_radius : float, optional
    Cylinder radius (Å) for rendered bonds.  Default ``0.07``.
bond_color : tuple of float, optional
    RGB triplet (each in [0, 1]) for bond colour.  Default red
    ``(0.95, 0.1, 0.1)``.
background_color : str, optional
    CSS colour string for the panel background.  Default
    ``"#f7f8f5"`` (off-white).
title, subtitle : str, optional
    Headline + sub-line text rendered above the grid.
bond_cutoff_scale : float, optional
    Bond search radius is ``shell_target.pair_peak ×
    bond_cutoff_scale``.  Default ``1.2``.
max_bonds_per_atom : int, optional
    Per-atom cap on bonds drawn (after the angle filter).
    Default ``4``.
bond_length_tol : float, optional
    Acceptance window around ``pair_peak`` for the bond filter
    (fraction).  Default ``0.10`` (±10 %).
ideal_angle_deg, bond_angle_tol_deg : float, optional
    Reject bonds whose 4-NN angles deviate more than
    ``bond_angle_tol_deg`` from ``ideal_angle_deg``.  Default
    ``109.47°`` ± ``18°`` (tetrahedral).  Set
    ``bond_angle_tol_deg=180`` to disable the angle filter (e.g.
    FCC metals where 60°/90°/120° angles all matter).
tetrahedra : dict, optional
    Switch panels to tetrahedron rendering.  Dict keys:
    ``center_symbol`` (default ``"Si"``), ``vertex_symbol``
    (default ``"O"``), ``bond_length`` (default auto-detected
    from atoms), ``bond_length_tol`` (default ``0.15``),
    ``ideal_angle_deg`` (default ``109.47``), ``angle_tol_deg``
    (default ``25.0``), ``scale`` (vertex shrink factor;
    default ``0.5`` for same-element, ``1.0`` for
    cross-species).
tetrahedra_color : tuple of float, optional
    RGB triplet for tetrahedron faces.  Default navy
    ``(0.35, 0.45, 0.95)``.
tetrahedra_opacity : float, optional
    Face opacity in [0, 1].  Default ``0.45``.
octahedra, octahedra_color, octahedra_opacity : dict / tuple / float, optional
    Octahedron variant — same dict keys as ``tetrahedra``.
cuboctahedra, cuboctahedra_color, cuboctahedra_opacity : dict / tuple / float, optional
    Cuboctahedron variant (12-vertex FCC close-packed shell).
polyhedra_groups : list of dict, optional
    Multi-group polyhedra (e.g. sp²/sp³ carbon) — list of
    per-group dicts each with ``kind`` (one of
    ``"triangles"``, ``"tetrahedra"``, ``"octahedra"``,
    ``"cuboctahedra"``), ``center_symbol``, ``vertex_symbol``,
    ``color``, ``opacity``, plus optional ``virtual_species``
    for filtering by ``Supercell._atom_shell_species_index``.

**Returns**
str
    The HTML written to ``output_path``.

**Examples**
>>> import atomode as tc
>>> cells = [(cell_amorphous, "amorphous"),
...          (cell_mro, "MRO"),
...          (cell_nc, "NC")]
>>> tc.export_overview_html("overview.html", cells, grid_cols=3,
...                          tetrahedra=dict(center_symbol="Si",
...                                          vertex_symbol="Si"))

#### `export_g2_compare_html(cells_and_labels, output_path: "'str | None'" = None, *, r_max: 'float' = 10.0, r_step: 'float' = 0.05, background_color: 'str' = '#f7f8f5', title: 'str' = '', show_progress: 'bool' = False, sample_fraction: 'float' = 1.0, sample_rng_seed: 'int | None' = None) -> 'str'`

Export a g(r) overlay viewer comparing multiple supercells.

Every cell must share the same set of species (same reference
material).  One g(r) curve is drawn per cell for the currently
selected species pair; the dropdown in the viewer switches which
pair is shown and a legend identifies each cell by its label.

**Parameters**
cells_and_labels
    Accepts any of:

    * ``dict[str, Supercell]`` - keys become legend labels
    * ``list[tuple[Supercell, str]]``
    * ``list[Supercell]`` - each ``cell.label`` is used
output_path
    Path to write the HTML file.  When ``None`` the HTML string is
    returned instead (for :func:`IPython.display.HTML` / inline
    display); see :func:`plot_g2_compare` for a ready-made Jupyter
    wrapper.
r_max, r_step
    Radial grid for the measurements.  Finer ``r_step`` gives
    smoother curves; 0.05 A is a good default.
background_color, title
    Cosmetic.
show_progress
    Forwarded to each :meth:`Supercell.measure_g3` call (used under
    the hood; ``phi_num_bins`` is set low for speed).

**Returns**
str
    Resolved output path when ``output_path`` was provided,
    otherwise the HTML source string.

#### `plot_g2_compare(cells_and_labels, *, r_max: 'float' = 10.0, r_step: 'float' = 0.05, title: 'str' = '', height: 'int' = 480, show_progress: 'bool' = False, sample_fraction: 'float' = 1.0, sample_rng_seed: 'int | None' = None)`

Inline Jupyter display of the g(r) overlay-compare viewer.

Convenience wrapper around :func:`export_g2_compare_html` that
packages the HTML as an :class:`IPython.display.HTML` object so
you can do ``tc.plot_g2_compare(cells)`` in a notebook cell.

**Parameters**
cells_and_labels : list of (Supercell, str) or dict
    Either a list of ``(supercell, label)`` pairs or a
    ``{label: supercell}`` dict.  Each cell's g(r) becomes one
    curve in the overlay.  See :func:`export_g2_compare_html`
    for full input-shape details.
r_max : float, optional
    Maximum radial distance (Å) plotted on the x-axis.  Default
    ``10.0``.
r_step : float, optional
    Bin width (Å) of the g(r) histogram.  Default ``0.05``.
title : str, optional
    Title text rendered above the viewer.  Default ``""``.
height : int, optional
    Iframe height (pixels) of the rendered viewer in Jupyter.
    Default ``480``.
show_progress : bool, optional
    Display a tqdm progress bar while the per-cell g(r)
    histograms are built.  Default ``False``.

**Returns**
IPython.display.HTML
    The viewer wrapped in an iframe and ready for inline
    display in a Jupyter cell.

## Multi-cell overview

Supports **multi-group polyhedra** via the `polyhedra_groups=`
kwarg, where each entry is a dict
`{kind, center_symbol, vertex_symbol, bond_length, ...,
virtual_species, color, opacity}` and `kind` is one of
`"triangles"`, `"tetrahedra"`, `"octahedra"`, `"cuboctahedra"`.
Use it for sp²/sp³ carbon blends where green triangle fans and
navy tetrahedra render side-by-side; see the
[Multi-Cell Overview page](../visualization/overview_viewer.md).
## g(r) comparison across supercells

Overlay the pair-correlation function g(r) from multiple supercells on
a single axis, with a dropdown to switch species pair and an inline
per-series label.  The
[compare mode of the g(2) viewer](../visualization/g2_viewer.md#compare-mode)
stacks curves with a small vertical offset so the six-regime ladders
shown on each example page stay legible.
