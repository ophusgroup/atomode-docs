# Module-level exporters

Module-level helpers for rendering finished supercells into
self-contained HTML viewers that can be opened in any browser or
embedded via ``<iframe>``.  See
[Visualization](../visualization/index.md) for the high-level
descriptions and rendered examples.

## Multi-cell overview

```{eval-rst}
.. autofunction:: tricor.export_overview_html
```

## g(r) comparison across supercells

Overlay the pair-correlation function g(r) from multiple supercells on
a single axis, with a dropdown to switch species pair and an inline
per-series label.  The [compare mode of the g(2) viewer](
../visualization/g2_viewer.md#compare-mode) stacks curves with a small
vertical offset so the six-regime ladders shown on each example page
stay legible.

```{eval-rst}
.. autofunction:: tricor.export_g2_compare_html
.. autofunction:: tricor.plot_g2_compare
```
