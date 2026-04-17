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

## What is a rooted three-body distribution?

For every atom $i$ and every pair of neighbours $(j, k)$ the code records
the three scalars

- $r_{ij}$, the distance from $i$ to the "root" neighbour $j$,
- $r_{ik}$, the distance from $i$ to the "partner" neighbour $k$,
- $\phi_{jik}$, the angle at the central atom $i$.

Accumulated over all central atoms of the relevant species, this gives a
four-index histogram $g_3^{t}(r_j, r_k, \phi)$ for every triplet type $t$
(e.g. `Si | Si Si`). "Rooted" means the distribution is conditioned on one
of the two bonds - the **root bond** - sitting in a specific radial shell.

The 2D viewer shows a slice of the full distribution: the root-bond length
$r_j$ is integrated over a user-chosen shell window (usually the first
neighbour peak), leaving a 2D map of $(r_k, \phi)$. This is the quantity
plotted in the heatmap.

## How to read the static viewer embedded in the case studies

- **Upper panel**: the 2D slice $g_3(r, \phi)$ for a fixed root-bond shell.
  Axes are partner-bond distance $r$ (horizontal) and angle $\phi$
  (vertical, 0-180 degrees). The diverging RdBu_r colormap has white at
  $g = 1$ (uniform random reference), blue for depleted, red for enhanced.
- **Lower panel**: the pair profile $g(r)$, i.e. the full two-body
  correlation function for the same triplet channel.
  - The **amber band labelled "root bond"** is the radial shell that was
    integrated over to produce the slice above. Any peak that falls inside
    this band is "the root bond"; peaks outside it appear as vertical
    stripes in the 2D slice at the corresponding partner-bond distance.
  - The dashed line at $g = 1$ marks the uniform density reference.
- The static viewer displays the distribution measured **after**
  relaxation; the interactive Jupyter widget can be invoked at any point
  in the workflow.

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
