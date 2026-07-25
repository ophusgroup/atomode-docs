# G3Distribution

Stand-alone three-body distribution measurer / target builder.
Most users will use `atomode.Supercell.measure_g3` rather than
constructing this directly; it's exposed here for users who need
finer control over the histogram axes or who want to compute g3
against a non-cell ASE atoms object.

```python
class atomode.G3Distribution
```

### Measurement

#### `measure_g3(r_max: 'float | None' = None, r_step: 'float | None' = None, phi_num_bins: 'int' = 90, plot_g3: 'bool' = False, return_g3: 'bool' = False, show_progress: 'bool' = False, progress_label: 'str | None' = None, backend: 'str' = 'auto', sample_fraction: 'float' = 1.0, sample_rng_seed: 'int | None' = None) -> 'np.ndarray | tuple[np.ndarray, np.ndarray, np.ndarray]'`

Measure the raw rooted three-body distribution.

**Parameters**
r_max
    Maximum radial distance included in the radial histogram grid.
r_step
    Radial bin width. `r_max / r_step` must be an integer.
phi_num_bins
    Number of angular bins spanning 0 to pi.
plot_g3
    If `True`, prepare the measured object for immediate inspection with
    `plot_g3()`.
return_g3
    If `True`, also return the radial and angular bin centers along with the
    measured raw histogram.
show_progress
    If `True`, display a simple text progress bar while the origin-centered
    triplet histograms are accumulated.  (Progress reporting is only
    emitted by the pure-numpy path; the numba path runs too fast to
    need it.)
progress_label
    Optional label shown next to the progress bar.
backend
    Which accumulation kernel to use.  One of:

    - ``"auto"`` *(default)* - use numba if available, fall back to
      the pure-numpy loop otherwise.
    - ``"numba"`` - require the numba-parallel kernel.  Raises
      ``RuntimeError`` if numba is not installed.
    - ``"python"`` - force the original numpy implementation.  Slower
      but self-contained; handy as a reference.

    The two backends produce ``g2count`` bit-for-bit identical and
    ``g3count`` that differ by less than ~3e-5 of the total count -
    only a handful of triplets flip between adjacent phi bins from
    floating-point ULP drift at bin boundaries.

**Returns**
np.ndarray or tuple
    The raw non-reduced histogram with shape
    `(num_triplets, num_r, num_r, phi_num_bins)`. If `return_g3` is `True`,
    this method returns `(g3, r, phi)` where `r` and `phi` are the radial and
    angular bin centers.

### Target construction

#### `target_g3(*, target_r_min: 'float', target_r_max: 'float', r_sigma: 'float | None' = None, r_sigma_at: 'float | None' = None, phi_sigma_deg: 'float | None' = None, label: 'str | None' = None, **kwargs: 'Any') -> "'G3Distribution'"`

Construct a transformed target distribution from the current raw g3.

The target is built in reduced coordinates, where the random reference
distribution is proportional to `r01^2 * r02^2 * sin(phi)`. The source
distribution is first reduced by this ideal-density factor, optionally
blurred in `phi` and in the two radial directions, and then smoothly mixed
toward `1.0` between `target_r_min` and `target_r_max`. The returned object
stores the transformed result back in the original raw, non-reduced form.

**Parameters**
target_r_min
    Radius where the smooth transition away from the measured reduced
    distribution begins.
target_r_max
    Radius where the reduced target has fully transitioned to the random
    limit of `1.0`.
r_sigma
    Radial blur width, in Angstrom, evaluated at `r_sigma_at`. The effective
    radial blur grows linearly with radius. If `r_sigma_at` is omitted,
    `r_sigma` is interpreted as a linear slope so that `sigma_r(r) = r_sigma * r`.
r_sigma_at
    Shared reference radius where the radial blur equals `r_sigma` and the
    angular blur equals `phi_sigma_deg`. If omitted, both blur widths grow
    linearly from zero using `r_sigma` and `phi_sigma_deg` as slopes.
phi_sigma_deg
    Angular Gaussian blur width in degrees, evaluated at `r_sigma_at`.
    Reflection is used at `phi = 0` and `phi = 180` degrees. If
    `r_sigma_at` is omitted, `phi_sigma_deg` is interpreted as a linear
    slope so that `sigma_phi(r) = phi_sigma_deg * r`.
label
    Optional label for the returned target distribution.

**Returns**
G3Distribution
    A new distribution containing the transformed raw target histogram.

### Inline visualisation

#### `plot_g3(pair: 'int | str' = 0, *, normalize: 'bool' = True)`

Return an interactive anywidget explorer for a rooted triplet channel.

**Parameters**
pair
    Either the integer triplet index or a triplet label such as
    `"Si-Si-C"`, where the center atom is shown in the middle.
normalize
    If `True`, display reduced-density views that approach `1.0` in the
    random long-range limit.

**Returns**
G3PlotWidget
    Interactive widget with a `(phi, r)` slice view and a linked rooted
    two-body shell selector.
