# g3 Comparison

Compare the measured supercell g3 against an explicit target distribution.

## Creating a target distribution

```python
dist = tc.G3Distribution(atoms)
dist.measure_g3(
    r_max=10,
    r_step=0.1,
    phi_num_bins=90,
)
target = dist.target_g3(
    target_r_min=5.0,
    target_r_max=8.0,
    r_sigma=0.05,
    phi_sigma_deg=3.0,
)
```

See [Target g3 distribution](../algorithms/target_g3.md) for the blending math.

## Building a supercell against a target

```python
cell = tc.Supercell(
    target,
    cell_dim_angstroms=(40, 40, 40),
    relative_density=0.96,
    rng_seed=42,
)
cell.generate(
    shell_target,
    grain_size=13.0,
    bond_weight=1.9,
    angle_weight=0.9,
)
cell.measure_g3()
cell.plot_g3_compare()
```

## Widget features

- Two heatmap panels (supercell vs target) at the same radial shell.
- Overlaid radial profiles with independent colours for supercell and target.
- Shared channel selector and shell-selection slider.
- Same normalize/auto-shell toggles as `plot_g3()`.
