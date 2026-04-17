# Static g3 Viewer

Bake the measured three-body distribution of a single supercell into a
self-contained HTML file. The layout mirrors the interactive Jupyter
widget but has no live selectors - a fixed colormap and root-bond shell
window are baked in, so the file renders identically in any browser.

## Usage

```python
cell.export_g3_html("liquid_g3.html")
```

A fresh `G3Distribution` is measured on the current atoms using the grid
passed to `export_g3_html`, independent of any cached distribution on the
supercell itself. This keeps the embedded JSON small without affecting the
main measurement state.

## Layout

- **Top panel** - 2D heatmap of the reduced g3 slice
  $\tilde{g}_3(r, \phi)$ at a fixed root-bond shell, plotted in `r` vs
  $\phi$ with the diverging `RdBu_r` colormap centred at $\tilde{g}_3 = 1$
  (uniform random reference). Blue = depleted, white = uniform,
  red = enhanced.
- **Bottom panel** - pair profile $g(r) / \text{uniform}$ for the same
  triplet channel, with the root-bond integration window highlighted as an
  amber band. The band shows exactly which range of distances was summed
  over to produce the slice above.
- **Right side** - colorbar legend with tick marks at 0, 1.0, and the
  current colour max. The 1.0 label follows the white point as the maximum
  is changed.
- **Controls** - drop-down channel selector (hidden when only one triplet
  type is present) and a numeric input for the colour maximum.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `output_path` | required | File path for the generated HTML. |
| `r_max` | 10.0 | Maximum radius of the embedded g3 grid in Å. |
| `r_step` | 0.1 | Radial bin width in Å. |
| `phi_num_bins` | 45 | Number of angular bins between 0 and 180°. |
| `background_color` | `"#f7f8f5"` | CSS colour for the viewer background. |
| `title` | `""` | Optional text shown at the top of the viewer. |
| `show_progress` | `False` | If `True`, show a progress bar during the g3 measurement. |

The defaults (`50 × 45` bins per triplet channel) keep the JSON footprint
around 100 kB for monatomic systems and well under 1 MB for complex
oxides.
