# Module-level exporters

Module-level helpers for rendering finished supercells into
self-contained HTML viewers that can be opened in any browser or
embedded via ``<iframe>``.  See
[Visualization](../visualization/index.md) for the high-level
descriptions and rendered examples.

```{eval-rst}
.. currentmodule:: tricor
```

## Multi-cell overview

Supports **multi-group polyhedra** via the `polyhedra_groups=`
kwarg, where each entry is a dict
`{kind, center_symbol, vertex_symbol, bond_length, ...,
virtual_species, color, opacity}` and `kind` is one of
`"triangles"`, `"tetrahedra"`, `"octahedra"`, `"cuboctahedra"`.
Use it for sp²/sp³ carbon blends where green triangle fans and
navy tetrahedra render side-by-side; see the
[Multi-Cell Overview page](../visualization/overview_viewer.md).

```{eval-rst}
.. autofunction:: export_overview_html
```

## g(r) comparison across supercells

Overlay the pair-correlation function g(r) from multiple supercells on
a single axis, with a dropdown to switch species pair and an inline
per-series label.  The
[compare mode of the g(2) viewer](../visualization/g2_viewer.md#compare-mode)
stacks curves with a small vertical offset so the six-regime ladders
shown on each example page stay legible.

```{eval-rst}
.. autofunction:: export_g2_compare_html

.. autofunction:: plot_g2_compare
```
