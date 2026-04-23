# g(r) Pair Distribution Viewer

Single-panel viewer for the 2-body g(r) of one supercell or a
regime-ladder comparison of several.  The same
[``g2_viewer.html``](https://github.com/ophusgroup/tricor/blob/main/src/tricor/static/g2_viewer.html)
template is used for both; behaviour is driven by whether the embedded
JSON payload contains a single ``profiles`` array (single-cell mode)
or a ``series`` list (compare mode).

## Single-cell mode

```python
# write a standalone HTML file
cell.export_g2_html("mro_g2.html", r_max=8.0, title="Si MRO g(r)")

# or view inline in Jupyter (returns IPython.display.HTML wrapping an iframe)
cell.plot_g2(r_max=8.0, title="Si MRO g(r)")
```

Controls:

- **pair dropdown** - picks which species pair is plotted.  Binary
  materials (SiO₂) show Si-Si, Si-O, O-O; ternaries (SrTiO₃) show all
  six unique pairs; single-element cases show one.
- **overlay all pairs** checkbox - draws every pair on the same axis
  with an inline legend (useful for quickly finding which pair peaks
  share radii).

A faint dashed vertical marker at the reference ``pair_peak`` from
``shell_target`` (if available) helps locate the expected first-shell
radius on the current curve.

## Compare mode

```python
cells = {
    "liquid":          cells_liquid,
    "amorphous":       cells_amorphous,
    "SRO":             cells_sro,
    "MRO":             cells_mro,
    "ext. MRO":        cells_ext_mro,
    "nanocrystalline": cells_nano,
}

# inline Jupyter display
tc.plot_g2_compare(cells, r_max=8.0, title="Silicon regime comparison")

# standalone HTML for docs / sharing
tc.export_g2_compare_html(cells, "si_g2_compare.html", r_max=8.0)
```

Behaviour:

- **Stacked y-offset.** Each series sits in its own horizontal slot
  with a small gap (offset = 35 % of the per-curve peak height).  The
  input order is preserved - passing a dict iterates insertion order - so the regen scripts' ``liquid → nanocrystalline`` order puts the
  most disordered curve at the bottom and the most ordered at the top.
  Numeric y-axis ticks are hidden in this mode because a single number
  no longer maps to one g(r) value.
- **Inline labels.** Each series label is drawn in its curve's colour
  at the near-origin anchor (r ≈ 0.3 Å), just above the curve.  No
  legend box - the labels double as the legend.
- **Per-series reference line.** A faint dashed ``g = 1`` line is
  drawn at every series's baseline so you can read off the over- /
  under-density of each regime at a glance.

### Input shapes

{func}`tricor.export_g2_compare_html` accepts any of:

```python
# dict - keys become labels (insertion order = stack order)
tc.plot_g2_compare({"liquid": c1, "MRO": c2, "NC": c3})

# list of (cell, label) tuples
tc.plot_g2_compare([(c1, "liquid"), (c2, "MRO")])

# list of cells - uses each cell.label
tc.plot_g2_compare([c1, c2, c3])
```

All supplied cells must share the same species set.  Measurements
reuse the g3 machinery under the hood (``phi_num_bins`` is set low for
speed because the compare viewer doesn't plot angular data).

## Example - silicon regime ladder

The SiO₂ example in this repo opens with exactly this compare viewer
embedded under its Overview heading; the silicon analogue is visible
on the [silicon example page](../examples/silicon/index.md).  Pair
dropdown switches which species pair is shown; the six stacked curves
identify each regime by colour and inline label.

<iframe src="../_static/g2_compare/silicon.html"
        width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>
