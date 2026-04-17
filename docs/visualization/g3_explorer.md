# g3 Explorer

After measuring the g3 distribution, view it interactively:

```python
cell.measure_g3()
cell.plot_g3()
```

Returns a Jupyter widget (anywidget) with:

- **Heatmap**: 2D slice of the g3 distribution ($r$ vs $\phi$) for a selected radial shell.
- **Radial profile**: pair correlation function with drag-to-select shell range.
- **Channel selector**: switch between triplet types (e.g. `Si | Si Si`, `C | C Si`).
- **Normalize toggle**: show raw counts or density-normalized values approaching 1.0 in the random limit.
- **Auto-shell toggle**: when unchecked, the shell selection stays fixed while switching channels.

## Parameters

```python
cell.plot_g3(pair=0, normalize=True)
```

- `pair`: triplet channel index or label (e.g. `"Si | Si Si"`).
- `normalize`: if `True`, divides out the ideal density factor so the plot shows deviation from random.

## Requirements

`measure_g3()` must be called first:

```python
cell.generate(shell_target, ...)
cell.measure_g3()       # required
cell.plot_g3()
```
